"""Tests du contrôle de retrieval au niveau document et chunk."""

from src.rag.eval_schema import RagQuestion
from src.rag.evaluation.models import RetrievedChunk
from src.rag.evaluation.retrieval import check_retrieval


def _question():
    """RC01 : franchise de 90 jours, attendue dans le Résumé C87656 uniquement."""

    return RagQuestion.model_validate(
        {
            "id": "RC01",
            "question": "Quelle franchise ?",
            "type": "chiffre_precis",
            "contrat_cible": "C87656",
            "reponse_attendue": "90 jours",
            "sources_attendues": ["RESUME_C87656"],
            "corpus_a_contenir": "franchise",
            "points_obligatoires": [
                {"id": "O0", "texte": "90 jours", "formes": ["90 jours"], "verif": "deterministe"}
            ],
            "points_interdits": [
                {"id": "I0", "texte": "parents", "formes": ["parents"], "verif": "deterministe"}
            ],
        }
    )


def _chunk(doc_id, text, index=0):
    """Construit un chunk récupéré."""

    return RetrievedChunk(doc_id=doc_id, chunk_index=index, score=0.5, text=text)


def test_ok_quand_la_forme_est_dans_un_chunk_de_la_source():
    check = check_retrieval(_question(), [_chunk("RESUME_C87656", "ITT : franchise 90 jours")])
    assert check.ok


def test_bon_document_mauvais_chunk_est_ko():
    check = check_retrieval(_question(), [_chunk("RESUME_C87656", "Obsèques : 2 500 €")])
    assert not check.ok
    assert check.docs_manquants == [] and check.points_absents == ["O0"]


def test_forme_dans_un_autre_document_ne_compte_pas():
    # « 90 jours » est partagé par la FAQ : la source attendue absente reste un échec
    check = check_retrieval(_question(), [_chunk("FAQ_prevcorp", "franchise de 90 jours")])
    assert not check.ok
    assert check.docs_manquants == ["RESUME_C87656"]
    assert check.points_absents == ["O0"]


def test_forme_et_source_dans_des_chunks_differents_du_bon_document_ok():
    chunks = [_chunk("RESUME_C87656", "garanties", 0), _chunk("RESUME_C87656", "90 jours", 1)]
    assert check_retrieval(_question(), chunks).ok


def test_document_present_mais_forme_dans_un_chunk_hors_sources_ko():
    chunks = [_chunk("RESUME_C87656", "Obsèques"), _chunk("FAQ_prevcorp", "90 jours")]
    check = check_retrieval(_question(), chunks)
    assert not check.ok and check.docs_manquants == [] and check.points_absents == ["O0"]
