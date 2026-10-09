"""Tests de la faithfulness maison : parsing, score, rapport, cas N/A (sans réseau)."""

from datetime import datetime
from types import SimpleNamespace

import anthropic
import pytest

from src.rag.evaluation.faithfulness import (
    FaithfulnessResult,
    FaithfulnessRow,
    mean_score,
    parse_claims,
    render_report,
    render_row,
    report_filename,
    score_faithfulness,
)
from src.rag.evaluation.models import RetrievedChunk

CHUNKS = [RetrievedChunk(doc_id="FAQ_prevcorp", chunk_index=0, score=0.9, text="texte")]


def _judge(*reponses: str) -> tuple[SimpleNamespace, list[dict]]:
    """Juge factice qui renvoie les réponses dans l'ordre et enregistre les appels."""

    appels: list[dict] = []
    queue = list(reponses)

    def create(**kwargs):
        appels.append(kwargs)
        return SimpleNamespace(content=[anthropic.types.TextBlock(type="text", text=queue.pop(0))])

    judge = SimpleNamespace(messages=SimpleNamespace(create=create))
    return SimpleNamespace(client=judge, model="modele-test"), appels


def test_parse_claims_json_nu():
    assert parse_claims('["a", "b"]') == ["a", "b"]


def test_parse_claims_tolere_un_fence():
    assert parse_claims('```json\n["a"]\n```') == ["a"]


@pytest.mark.parametrize("raw", ["pas de json", '["a", 3]', '["  "]'])
def test_parse_claims_invalide(raw):
    with pytest.raises(ValueError):
        parse_claims(raw)


def test_score_et_non_appuyees():
    result = FaithfulnessResult(
        claims={"A1": "x", "A2": "y", "A3": "z", "A4": "w"},
        verdicts={"A1": True, "A2": False, "A3": True, "A4": True},
    )
    assert result.score == 0.75
    assert result.unsupported == ["y"]


def test_score_none_sans_affirmation():
    assert FaithfulnessResult(claims={}, verdicts={}).score is None


def test_score_faithfulness_deux_appels_a_temperature_zero():
    judge, appels = _judge('["a", "b"]', '{"A1": true, "A2": false}')
    result = score_faithfulness(judge, "q", "réponse", CHUNKS)  # type: ignore[arg-type]
    assert result.score == 0.5 and result.unsupported == ["b"]
    assert len(appels) == 2
    assert all(a["temperature"] == 0 and a["model"] == "modele-test" for a in appels)
    assert "FAQ_prevcorp" in appels[1]["messages"][0]["content"]


def test_score_faithfulness_sans_affirmation_saute_la_verification():
    judge, appels = _judge("[]")
    result = score_faithfulness(judge, "q", "Je ne sais pas.", CHUNKS)  # type: ignore[arg-type]
    assert result.score is None and len(appels) == 1


def test_score_faithfulness_verdict_manquant_leve():
    judge, _ = _judge('["a", "b"]', '{"A1": true}')
    with pytest.raises(ValueError):
        score_faithfulness(judge, "q", "réponse", CHUNKS)  # type: ignore[arg-type]


ROWS = [
    FaithfulnessRow(id="RC01", type="fait_simple", score=1.0, n_claims=2, answer="ok"),
    FaithfulnessRow(
        id="RC02", type="fait_simple", score=0.5, n_claims=2, unsupported=["faux"], answer="a\nb"
    ),
    FaithfulnessRow(id="RC03", type="sans_reponse", score=None, n_claims=0, answer="refus"),
    FaithfulnessRow(id="RC04", type="croisement", error="RuntimeError: boom"),
]


def test_mean_score_par_type_exclut_na_et_erreurs():
    assert mean_score(ROWS) == "0.75 (2 q.)"
    assert mean_score(ROWS, "fait_simple") == "0.75 (2 q.)"
    assert mean_score(ROWS, "sans_reponse") == "N/A"
    assert mean_score(ROWS, "croisement") == "N/A"
    assert mean_score([]) == "N/A"


def test_render_row_liste_les_non_appuyees():
    texte = render_row(ROWS[1])
    assert "0.50 (2 affirmations)" in texte and "  - faux" in texte
    assert "> a\n> b" in texte


def test_render_row_na_et_erreur():
    assert "N/A (aucune affirmation)" in render_row(ROWS[2])
    assert "ERREUR d'I/O" in render_row(ROWS[3])


def test_render_report_entete_synthese_et_detail():
    texte = render_report(
        ROWS,
        date=datetime(2026, 10, 9, 10, 0, 0),
        yaml_hash="abc123",
        model="m",
        judge_model="j",
        k=5,
        variant="prefix",
    )
    assert "- Variante d'ingestion : prefix" in texte
    assert "Questions : 4 dont 1 en erreur d'I/O" in texte
    assert "| fait_simple | 0.75 (2 q.) |" in texte
    assert "| sans_reponse | N/A |" in texte
    assert "### RC02 (fait_simple)" in texte


def test_report_filename():
    nom = report_filename(datetime(2026, 10, 9, 10, 0, 0), "prefix", "abc123")
    assert nom == "faithfulness_20261009_100000_prefix_abc123.md"


def test_extraction_refus_melange_aux_faits_score_les_faits():
    judge, appels = _judge(
        '["Le taux est de 50 %.", "Le concubin exige une résidence commune."]',
        '{"A1": true, "A2": true}',
    )
    reponse = "Le taux est de 50 %. Cependant, je ne trouve pas cette information."
    result = score_faithfulness(judge, "q", reponse, CHUNKS)  # type: ignore[arg-type]
    assert result.score == 1.0 and len(result.claims) == 2
    assert "mélanger refus et faits" in appels[0]["system"]


def test_extraction_prompt_ecarte_meta_documents_et_jugements_de_valeur():
    judge, appels = _judge("[]")
    score_faithfulness(judge, "q", "Le Règlement n'a pas été consulté.", CHUNKS)  # type: ignore[arg-type]
    system = appels[0]["system"]
    assert "documents consultés" in system and "jugements de valeur" in system


def test_refus_pur_reste_na():
    judge, appels = _judge("[]")
    result = score_faithfulness(judge, "q", "Je ne trouve pas cette information.", CHUNKS)  # type: ignore[arg-type]
    assert result.score is None and len(appels) == 1
