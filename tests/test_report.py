"""Tests du rapport d'éval RAG : en-tête, synthèse et détail (aucune I/O hors tmp_path)."""

from datetime import datetime

import pytest

from src.rag.evaluation.models import (
    Diagnostic,
    QuestionResult,
    Report,
    RetrievalCheck,
    RetrievedChunk,
    ScoreResult,
)
from src.rag.evaluation.report import (
    hash_yaml,
    render_header,
    render_report,
    report_filename,
    summarize,
    write_report,
)


def _result(id_="RC01", type_="fait_simple", r=True, e=True, i=True, **kwargs):
    """Construit un résultat de question avec R/E/I fixés."""

    return QuestionResult(
        id=id_,
        type=type_,
        retrieval=None if r is None else RetrievalCheck(ok=r, docs_manquants=[], points_absents=[]),
        e2e=ScoreResult(passed=e, needs_review=False),
        isolated=ScoreResult(passed=i, needs_review=True),
        diagnostic=Diagnostic.SAIN,
        **kwargs,
    )


def _report(results=()):
    """Construit un rapport avec un en-tête complet."""

    return Report(
        date=datetime(2026, 10, 6, 14, 30, 0),
        yaml_hash="abc123def456",
        model="claude-sonnet-4-6",
        judge_model="claude-sonnet-4-6",
        temperature=0.0,
        k=5,
        ingestion_variant="none",
        results=list(results),
    )


def test_entete_contient_les_champs_de_reproductibilite():
    entete = render_header(_report())
    for attendu in (
        "2026-10-06T14:30:00",
        "abc123def456",
        "claude-sonnet-4-6",
        "Temperature : 0.0",
        "k : 5",
        "Variante d'ingestion : none (vérifiée contre la collection)",
        "Contexte isolé : document entier",
    ):
        assert attendu in entete


@pytest.mark.parametrize("variante", ["none", "prefix", "contextual"])
def test_nom_de_fichier_date_variante_hash(variante):
    report = _report()
    report.ingestion_variant = variante
    assert report_filename(report) == f"rag_20261006_143000_{variante}_abc123def456.md"


def test_hash_yaml_depend_du_contenu(tmp_path):
    a, b = tmp_path / "a.yml", tmp_path / "b.yml"
    a.write_text("x: 1", encoding="utf-8")
    b.write_text("x: 2", encoding="utf-8")
    assert hash_yaml(a) != hash_yaml(b) and len(hash_yaml(a)) == 12


def test_sans_reponse_exclu_du_denominateur_retrieval():
    results = [_result("RC01"), _result("RC04", "sans_reponse", r=None)]
    s = summarize(results)
    assert str(s["R"]) == "1/1" and str(s["E"]) == "2/2"
    assert str(summarize(results, "sans_reponse")["R"]) == "N/A"


def test_erreurs_io_exclues_des_scores_et_comptees():
    erreur = QuestionResult(
        id="RC02",
        type="fait_simple",
        retrieval=None,
        e2e=None,
        isolated=None,
        diagnostic=Diagnostic.ERREUR,
        error="APIConnectionError",
    )
    report = _report([_result("RC01", e=False), erreur])
    texte = render_report(report)
    assert "dont 1 en erreur d'I/O" in texte
    assert str(summarize(report.results)["E"]) == "0/1"
    assert "ERREUR d'I/O" in texte and "APIConnectionError" in texte


def test_chunks_e2e_integraux_pour_sans_reponse():
    long_texte = "mot " * 200
    chunk = RetrievedChunk(
        doc_id="NOTICE_CCN_metallurgie", chunk_index=3, score=0.81, text=long_texte
    )
    sans = _result("RC17", "sans_reponse", r=None, chunks=[chunk])
    autre = _result("RC01", chunks=[chunk])
    assert long_texte.strip() in render_report(_report([sans]))
    assert long_texte.strip() not in render_report(_report([autre]))
    assert "`NOTICE_CCN_metallurgie` #3" in render_report(_report([sans]))


def test_relecture_manuelle_signalee():
    assert "à vérifier à la main" in render_report(_report([_result()]))


def test_reponses_e2e_et_isolee_presentes_apres_le_diagnostic():
    result = _result(answer_e2e="Réponse A\nligne 2", answer_isolated="Réponse B")
    texte = render_report(_report([result]))
    assert "**Réponse e2e**" in texte and "**Réponse isolée**" in texte
    assert "> Réponse A" in texte and "> ligne 2" in texte and "> Réponse B" in texte
    assert texte.index("diagnostic :") < texte.index("**Réponse e2e**")
    assert texte.index("**Réponse e2e**") < texte.index("**Réponse isolée**")


def test_reponse_absente_affiche_aucune_y_compris_en_erreur_io():
    erreur = QuestionResult(
        id="RC02",
        type="fait_simple",
        retrieval=None,
        e2e=None,
        isolated=None,
        diagnostic=Diagnostic.ERREUR,
        error="APIConnectionError",
    )
    texte = render_report(_report([erreur, _result("RC01")]))
    assert texte.count("> (aucune)") == 4


def test_write_report_ecrit_un_fichier_par_run(tmp_path):
    path = write_report(_report([_result()]), tmp_path / "rag")
    assert path.name == "rag_20261006_143000_none_abc123def456.md"
    assert path.read_text(encoding="utf-8").startswith("# Rapport d'éval RAG")
