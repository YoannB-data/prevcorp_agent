"""Tests du préfixe de contexte : constructeur, vrais PDF, ingestion, garde de variante."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.rag import ingestion
from src.rag.evaluation.adapters import check_variant, collection_variant
from src.rag.metadata import (
    ContractInfo,
    PrefixConstructionError,
    build_context_prefix,
    doc_type_from_filename,
    extract_contract_info,
    extract_title,
)
from src.rag.pdf_text import extract_text

CORPUS = Path(__file__).parent.parent / "corpus"
PDFS = sorted(CORPUS.glob("*.pdf"))
JUMEAUX = {"NOTICE_CCN_metallurgie.pdf", "NOTICE_CCN_metallurgie_distracteur.pdf"}

RESUME_TEXT = (
    "PREVCORP PRÉVOYANCE\n"
    "Résumé des garanties — Contrat n° C20077\n"
    "Convention collective nationale du transport routier — Personnel non cadre\n"
)
RESUME_PREFIX = (
    "[C20077 | résumé des garanties | Contrat C20077 — transport routier, Personnel non cadre]"
)


def _fake_voyage():
    voyage = MagicMock()
    voyage.embed.side_effect = lambda texts, **_: SimpleNamespace(
        embeddings=[[0.0] * 3] * len(texts)
    )
    return voyage


def _stub_pdf(monkeypatch, text):
    monkeypatch.setattr(ingestion, "extract_text", lambda _path: text)
    monkeypatch.setattr(ingestion, "chunk_text", lambda _t: ["chunk brut un", "chunk brut deux"])


# ─── Constructeur ────────────────────────────────────────────────────────────


def test_prefixe_avec_contrat():
    contract = ContractInfo("C20077", "transport routier", "Personnel non cadre")
    assert build_context_prefix("", "resume_contrat", contract) == RESUME_PREFIX


def test_prefixe_sans_contrat():
    prefix = build_context_prefix("RÈGLEMENT GÉNÉRAL", "reglement", None)
    assert prefix == "[RÈGLEMENT GÉNÉRAL | règlement]"


@pytest.mark.parametrize(
    ("ligne", "ccn", "categorie"),
    [
        ("du transport routier — Personnel non cadre", "transport routier", "Personnel non cadre"),
        ("de l'agriculture — Personnel non cadre", "agriculture", "Personnel non cadre"),
        ("de la métallurgie — Personnel cadre", "métallurgie", "Personnel cadre"),
        (
            "de l'enseignement privé — Ensemble du personnel",
            "enseignement privé",
            "Ensemble du personnel",
        ),
        (
            "— Santé et action sociale — Personnel cadre",
            "Santé et action sociale",
            "Personnel cadre",
        ),
    ],
)
def test_extraction_contrat_formulations_reelles(ligne, ccn, categorie):
    text = f"Résumé des garanties — Contrat n° C12345\nConvention collective nationale {ligne}\n"
    info = extract_contract_info(text, "RESUME_C12345.pdf")
    assert (info.contract_id, info.ccn, info.category) == ("C12345", ccn, categorie)


def test_contrat_introuvable_nomme_le_fichier():
    with pytest.raises(PrefixConstructionError, match=r"RESUME_X\.pdf.*Contrat n°"):
        extract_contract_info("mise en page inattendue", "RESUME_X.pdf")


def test_titre_introuvable_nomme_le_fichier():
    with pytest.raises(PrefixConstructionError, match=r"titre introuvable dans NOTICE_X\.pdf"):
        extract_title("PREVCORP PRÉVOYANCE\nTitre en casse mixte\n", "NOTICE_X.pdf")


def test_titre_ignore_la_banniere_commune():
    text = "tableau\nPREVCORP PRÉVOYANCE\nFOIRE AUX\nQUESTIONS\nContrat collectif\n"
    assert extract_title(text, "FAQ.pdf") == "FOIRE AUX QUESTIONS"


# ─── Vrais PDF du corpus ─────────────────────────────────────────────────────


@pytest.mark.skipif(not PDFS, reason="corpus/ vide (PDF gitignorés)")
def test_prefixes_des_vrais_pdf_sans_signal_artificiel():
    prefixes = {p.name: ingestion.document_prefix(extract_text(p), p) for p in PDFS}
    for pdf in PDFS:
        assert "distracteur" not in prefixes[pdf.name].lower()
        assert pdf.stem not in prefixes[pdf.name]
    if JUMEAUX <= prefixes.keys():
        jumeau, distracteur = (prefixes[name] for name in sorted(JUMEAUX))
        assert jumeau == distracteur
        # un seul doublon autorisé : la paire Métallurgie
        assert len(set(prefixes.values())) == len(prefixes) - 1
    else:
        assert len(set(prefixes.values())) == len(prefixes)
    for name, prefix in prefixes.items():
        if doc_type_from_filename(name) == "resume_contrat":
            contract_id = Path(name).stem.removeprefix("RESUME_")
            assert prefix.startswith(
                f"[{contract_id} | résumé des garanties | Contrat {contract_id}"
            )


# ─── Ingestion ───────────────────────────────────────────────────────────────


def test_variante_prefix_embedde_le_prefixe_et_stocke_le_brut(monkeypatch):
    _stub_pdf(monkeypatch, RESUME_TEXT)
    voyage, qdrant = _fake_voyage(), MagicMock()
    counts = ingestion.ingest_pdf(Path("RESUME_C20077.pdf"), voyage, qdrant, "prefix")
    assert voyage.embed.call_args.args[0] == [
        f"{RESUME_PREFIX}\nchunk brut un",
        f"{RESUME_PREFIX}\nchunk brut deux",
    ]
    points = qdrant.upsert.call_args.kwargs["points"]
    assert [p.payload["text"] for p in points] == ["chunk brut un", "chunk brut deux"]
    assert {p.payload["ingestion_variant"] for p in points} == {"prefix"}
    assert counts == (2, 2)


def test_variante_none_n_ajoute_pas_de_prefixe(monkeypatch):
    _stub_pdf(monkeypatch, RESUME_TEXT)
    voyage, qdrant = _fake_voyage(), MagicMock()
    counts = ingestion.ingest_pdf(Path("RESUME_C20077.pdf"), voyage, qdrant, "none")
    assert voyage.embed.call_args.args[0] == ["chunk brut un", "chunk brut deux"]
    points = qdrant.upsert.call_args.kwargs["points"]
    assert {p.payload["ingestion_variant"] for p in points} == {"none"}
    assert counts == (2, 0)


def test_resume_illisible_leve_au_lieu_de_degrader(monkeypatch):
    _stub_pdf(monkeypatch, "PREVCORP PRÉVOYANCE\nMISE EN PAGE INATTENDUE\n")
    voyage, qdrant = _fake_voyage(), MagicMock()
    with pytest.raises(PrefixConstructionError, match=r"RESUME_C20077\.pdf"):
        ingestion.ingest_pdf(Path("RESUME_C20077.pdf"), voyage, qdrant, "prefix")
    voyage.embed.assert_not_called()
    qdrant.upsert.assert_not_called()


def test_recreate_supprime_la_collection_existante():
    qdrant = MagicMock()
    qdrant.get_collections.return_value = SimpleNamespace(
        collections=[SimpleNamespace(name=ingestion.COLLECTION_NAME)]
    )
    ingestion.recreate_collection(qdrant)
    qdrant.delete_collection.assert_called_once_with(ingestion.COLLECTION_NAME)


def test_recreate_sans_collection_ne_supprime_rien():
    qdrant = MagicMock()
    qdrant.get_collections.return_value = SimpleNamespace(collections=[])
    ingestion.recreate_collection(qdrant)
    qdrant.delete_collection.assert_not_called()


def test_cli_recreate_precede_ingestion(monkeypatch):
    calls = []
    monkeypatch.setattr(ingestion, "default_clients", lambda: (MagicMock(), MagicMock()))
    monkeypatch.setattr(ingestion, "recreate_collection", lambda _q: calls.append("recreate"))
    monkeypatch.setattr(
        ingestion, "ingest_corpus", lambda **kw: calls.append(("ingest", kw["variant"]))
    )
    ingestion.main(["--recreate", "--variant", "prefix"])
    assert calls == ["recreate", ("ingest", "prefix")]


def test_cli_sans_recreate_ne_supprime_pas(monkeypatch):
    calls = []
    monkeypatch.setattr(ingestion, "default_clients", lambda: (MagicMock(), MagicMock()))
    monkeypatch.setattr(ingestion, "recreate_collection", lambda _q: calls.append("recreate"))
    monkeypatch.setattr(ingestion, "ingest_corpus", lambda **kw: calls.append("ingest"))
    ingestion.main([])
    assert calls == ["ingest"]


# ─── Garde de variante ───────────────────────────────────────────────────────


def test_variante_de_collection_unique():
    assert collection_variant([{"ingestion_variant": "prefix"}] * 3) == "prefix"


def test_collection_sans_variante_refusee():
    with pytest.raises(ValueError, match="sans ingestion_variant"):
        collection_variant([{"doc_id": "a"}])


def test_collection_mixte_refusee():
    with pytest.raises(ValueError, match="mixte"):
        collection_variant([{"ingestion_variant": "none"}, {"ingestion_variant": "prefix"}])


def test_variante_declaree_differente_refusee():
    with pytest.raises(ValueError, match="--variant prefix.*'none'"):
        check_variant("prefix", "none")
    check_variant("prefix", "prefix")
