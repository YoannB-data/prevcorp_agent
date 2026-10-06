"""Tests de l'orchestration du run d'éval RAG, avec fakes (ni API ni Qdrant)."""

from datetime import datetime

import pytest
import yaml

from src.rag.evaluation.models import Answer, Diagnostic, RetrievedChunk
from src.rag.evaluation.runner import run_eval

DOCS = {"RESUME_C87656", "FAQ_prevcorp", "NOTICE_CCN_metallurgie"}


def _pt(pid, formes, verif="deterministe"):
    """Construit un point valide."""

    return {"id": pid, "texte": formes[0], "formes": formes, "verif": verif}


def _questions():
    """Une question chiffrée et une sans_reponse, toutes scorables."""

    return {
        "questions": [
            {
                "id": "RC01",
                "question": "Quelle franchise ?",
                "type": "chiffre_precis",
                "contrat_cible": "C87656",
                "reponse_attendue": "90 jours",
                "sources_attendues": ["RESUME_C87656"],
                "corpus_a_contenir": "franchise",
                "points_obligatoires": [_pt("O0", ["90 jours"])],
            },
            {
                "id": "RC04",
                "question": "Rapatriement ?",
                "type": "sans_reponse",
                "contrat_cible": None,
                "reponse_attendue": "Non",
                "sources_attendues": [],
                "contexte_isole": ["RESUME_C87656"],
                "corpus_a_contenir": "absence",
                "points_obligatoires": [_pt("O0", ["pas dans les documents"], "juge")],
            },
        ]
    }


class FakeJudge:
    """Juge factice qui valide tout."""

    def evaluate(self, question, answer_text, points):
        return {p.id: True for p in points}


def _chunk(doc_id, text, index=0):
    return RetrievedChunk(doc_id=doc_id, chunk_index=index, score=0.5, text=text)


def _run(tmp_path, data=None, *, generate=None, retrieve=None, ids=None):
    """Lance run_eval avec des fakes ; generate répond selon le contexte reçu."""

    path = tmp_path / "q.yml"
    path.write_text(yaml.safe_dump(data or _questions()), encoding="utf-8")
    appels = {"retrieve": [], "generate": []}

    def default_retrieve(question, k):
        appels["retrieve"].append((question, k))
        return [_chunk("RESUME_C87656", "ITT : franchise de 90 jours")]

    def default_generate(question, chunks):
        appels["generate"].append((question, [c.doc_id for c in chunks]))
        if question == "Rapatriement ?":
            return Answer("Cette information n'est pas dans les documents.")
        return Answer("La franchise est de 90 jours.")

    report = run_eval(
        path,
        5,
        "none",
        retrieve=retrieve or default_retrieve,
        generate=generate or default_generate,
        fetch_doc_chunks=lambda doc_id: [_chunk(doc_id, "texte du document", 0)],
        judge=FakeJudge(),
        valid_doc_ids=DOCS,
        model="m",
        judge_model="j",
        ids=ids,
        now=datetime(2026, 10, 6),
    )
    return report, appels


def test_run_complet_sain(tmp_path):
    report, appels = _run(tmp_path)
    assert [r.diagnostic for r in report.results] == [Diagnostic.SAIN, Diagnostic.SAIN]
    assert report.results[1].retrieval is None  # N/A pour sans_reponse
    assert appels["retrieve"][0] == ("Quelle franchise ?", 5)
    assert len(report.yaml_hash) == 12 and report.ingestion_variant == "none"


def test_contexte_isole_est_le_document_entier_pas_le_retrieval(tmp_path):
    _, appels = _run(tmp_path)
    # 2 appels par question : e2e (retrieval) puis isolé (contexte_effectif)
    assert appels["generate"][0] == ("Quelle franchise ?", ["RESUME_C87656"])
    assert appels["generate"][3] == ("Rapatriement ?", ["RESUME_C87656"])


def test_questions_independantes_une_erreur_n_arrete_pas_le_run(tmp_path):
    def retrieve(question, k):
        if question == "Quelle franchise ?":
            raise ConnectionError("Qdrant indisponible")
        return [_chunk("NOTICE_CCN_metallurgie", "rente de conjoint")]

    report, _ = _run(tmp_path, retrieve=retrieve)
    assert report.results[0].diagnostic is Diagnostic.ERREUR
    assert "Qdrant indisponible" in (report.results[0].error or "")
    assert report.results[1].error is None


def test_alerte_sans_reponse_quand_le_retrieval_ramene_un_chunk_tentant(tmp_path):
    def generate(question, chunks):
        if question == "Rapatriement ?" and chunks[0].doc_id == "NOTICE_CCN_metallurgie":
            return Answer("Le rapatriement est couvert à 100 %.")
        return Answer("Cette information n'est pas dans les documents. 90 jours")

    class StrictJudge:
        def evaluate(self, question, answer_text, points):
            return {p.id: "pas dans les documents" in answer_text for p in points}

    path = tmp_path / "q.yml"
    path.write_text(yaml.safe_dump(_questions()), encoding="utf-8")
    report = run_eval(
        path,
        5,
        "none",
        retrieve=lambda q, k: [_chunk("NOTICE_CCN_metallurgie", "rapatriement")],
        generate=generate,
        fetch_doc_chunks=lambda d: [_chunk(d, "x")],
        judge=StrictJudge(),
        valid_doc_ids=DOCS,
        model="m",
        judge_model="j",
    )
    assert report.results[1].diagnostic is Diagnostic.ALERTE_CHUNK_TENTANT
    assert report.results[1].chunks[0].doc_id == "NOTICE_CCN_metallurgie"


def test_fail_fast_si_points_obligatoires_manquants(tmp_path):
    data = _questions()
    data["questions"][0]["points_obligatoires"] = []
    with pytest.raises(ValueError, match=r"points_obligatoires vide pour : \['RC01'\]"):
        _run(tmp_path, data)


def test_ids_filtre_les_questions(tmp_path):
    report, _ = _run(tmp_path, ids=["RC04"])
    assert [r.id for r in report.results] == ["RC04"]


def test_contexte_isole_vide_est_une_erreur(tmp_path):
    path = tmp_path / "q.yml"
    path.write_text(yaml.safe_dump(_questions()), encoding="utf-8")
    report = run_eval(
        path,
        5,
        "none",
        retrieve=lambda q, k: [_chunk("RESUME_C87656", "90 jours")],
        generate=lambda q, c: Answer("90 jours, pas dans les documents"),
        fetch_doc_chunks=lambda d: [],
        judge=FakeJudge(),
        valid_doc_ids=DOCS,
        model="m",
        judge_model="j",
    )
    assert all(r.diagnostic is Diagnostic.ERREUR for r in report.results)
    assert "contexte isolé" in (report.results[0].error or "")
