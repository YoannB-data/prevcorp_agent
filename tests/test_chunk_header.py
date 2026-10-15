"""Tests du header de contexte : extraction, vrais PDF, ingestion, garde de variante."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.rag import ingestion
from src.rag.evaluation.adapters import check_variant, collection_variant
from src.rag.metadata import (
    PrefixConstructionError,
    build_chunk_header,
    extract_contract_info,
    extract_title,
)
from src.rag.pdf_text import extract_text

CORPUS = Path(__file__).parent.parent / "data" / "corpus" / "pdf"
PDFS = sorted(CORPUS.glob("*.pdf"))

RESUME_TEXT = (
    "PREVCORP PRÉVOYANCE\n"
    "Résumé des garanties — Contrat n° C20077\n"
    "Convention collective nationale du transport routier — Personnel non cadre\n"
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


# ─── Extraction ────────────────────────────────────────────────────────────


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


# ─── Ingestion ───────────────────────────────────────────────────────────────


def test_ingestion_embedde_le_header_et_le_stocke_a_part(monkeypatch):
    _stub_pdf(monkeypatch, RESUME_TEXT)
    voyage, qdrant = _fake_voyage(), MagicMock()
    ingestion.ingest_pdf(Path("RESUME_C20077.pdf"), voyage, qdrant, "autre_collection")
    header = (
        "Document : Résumé des garanties C20077 | Type : résumé des garanties | "
        "Contrat : C20077 | CCN : transport routier, Personnel non cadre"
    )
    assert len(header) <= 150
    assert voyage.embed.call_args.args[0] == [
        f"{header}\nchunk brut un",
        f"{header}\nchunk brut deux",
    ]
    assert qdrant.upsert.call_args.kwargs["collection_name"] == "autre_collection"
    points = qdrant.upsert.call_args.kwargs["points"]
    assert [p.payload["text"] for p in points] == ["chunk brut un", "chunk brut deux"]
    assert {p.payload["header"] for p in points} == {header}
    assert {p.payload["ingestion_variant"] for p in points} == {"header"}


def test_resume_illisible_leve_au_lieu_de_degrader(monkeypatch):
    _stub_pdf(monkeypatch, "PREVCORP PRÉVOYANCE\nMISE EN PAGE INATTENDUE\n")
    voyage, qdrant = _fake_voyage(), MagicMock()
    with pytest.raises(PrefixConstructionError, match=r"RESUME_C20077\.pdf"):
        ingestion.ingest_pdf(Path("RESUME_C20077.pdf"), voyage, qdrant)
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
    monkeypatch.setattr(
        ingestion, "recreate_collection", lambda _q, c: calls.append(("recreate", c))
    )
    monkeypatch.setattr(
        ingestion, "ingest_corpus", lambda **kw: calls.append(("ingest", kw["collection"]))
    )
    ingestion.main(["--recreate", "--collection", "autre"])
    assert calls == [("recreate", "autre"), ("ingest", "autre")]


def test_cli_sans_recreate_ne_supprime_pas(monkeypatch):
    calls = []
    monkeypatch.setattr(ingestion, "default_clients", lambda: (MagicMock(), MagicMock()))
    monkeypatch.setattr(ingestion, "recreate_collection", lambda _q, _c: calls.append("recreate"))
    monkeypatch.setattr(ingestion, "ingest_corpus", lambda **kw: calls.append("ingest"))
    ingestion.main([])
    assert calls == ["ingest"]


def test_header_une_ligne_150_caracteres_max_sur_les_vrais_pdf():
    for pdf in PDFS:
        header = ingestion.document_header(extract_text(pdf), pdf)
        assert "\n" not in header
        assert len(header) <= 150
        assert pdf.stem not in header


def test_header_trop_long_leve_au_lieu_de_tronquer():
    with pytest.raises(PrefixConstructionError, match=r"RESUME_X\.pdf.*\(\d+ > 150"):
        build_chunk_header("T" * 200, "reglement", None, "RESUME_X.pdf")


# ─── Garde de variante ───────────────────────────────────────────────────────


def test_variante_de_collection_unique():
    assert collection_variant([{"ingestion_variant": "header"}] * 3) == "header"


def test_collection_sans_variante_refusee():
    with pytest.raises(ValueError, match="sans ingestion_variant"):
        collection_variant([{"doc_id": "a"}])


def test_collection_mixte_refusee():
    with pytest.raises(ValueError, match="mixte"):
        collection_variant([{"ingestion_variant": "header"}, {"ingestion_variant": "autre"}])


def test_variante_declaree_differente_refusee():
    with pytest.raises(ValueError, match="--variant header.*'autre'"):
        check_variant("header", "autre")
    check_variant("header", "header")
