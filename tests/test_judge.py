"""Tests du juge LLM : parsing strict et appel (client factice, aucun réseau)."""

from types import SimpleNamespace

import anthropic
import pytest

from src.rag.eval_schema import Point, RagQuestion
from src.rag.evaluation.judge import AnthropicJudge, parse_verdicts

POINTS = [Point(id="O0", texte="t", formes=["f"], verif="juge")]


def test_parse_verdicts_json_nu():
    assert parse_verdicts('{"O0": true, "O1": false}', ["O0", "O1"]) == {"O0": True, "O1": False}


def test_parse_verdicts_tolere_un_fence():
    assert parse_verdicts('```json\n{"O0": false}\n```', ["O0"]) == {"O0": False}


@pytest.mark.parametrize("raw", ["pas de json", '{"O0": "oui"}', '{"X": true}'])
def test_parse_verdicts_invalide(raw):
    with pytest.raises(ValueError):
        parse_verdicts(raw, ["O0"])


def test_evaluate_appelle_l_api_a_temperature_zero():
    appels = []

    def create(**kwargs):
        appels.append(kwargs)
        return SimpleNamespace(
            content=[anthropic.types.TextBlock(type="text", text='{"O0": true}')]
        )

    client = SimpleNamespace(messages=SimpleNamespace(create=create))
    question = RagQuestion.model_validate(
        {
            "id": "RC01",
            "question": "q",
            "type": "fait_simple",
            "contrat_cible": None,
            "reponse_attendue": "r",
            "sources_attendues": ["FAQ_prevcorp"],
            "corpus_a_contenir": "c",
        }
    )
    judge = AnthropicJudge(client, "modele-test")  # type: ignore[arg-type]
    assert judge.evaluate(question, "réponse", POINTS) == {"O0": True}
    assert appels[0]["temperature"] == 0 and appels[0]["model"] == "modele-test"
