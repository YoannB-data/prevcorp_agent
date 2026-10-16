"""Tests du chargement de l'eval set de routing."""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from evals.routing.load import load_eval_set

META = {"seuils": {"accuracy": 0.9, "rappel_hybride": 0.8}}


def _case(qid: str, **over: str) -> dict[str, str]:
    base = {
        "id": qid,
        "question": "q ?",
        "route_attendue": "sql",
        "forme": "simple",
        "origine": "x",
        "note": "n",
    }
    return {**base, **over}


def _write(tmp_path: Path, questions: list[dict[str, str]]) -> Path:
    path = tmp_path / "set.yml"
    path.write_text(yaml.safe_dump({"meta": META, "questions": questions}), encoding="utf-8")
    return path


def test_label_invalide(tmp_path):
    with pytest.raises(ValidationError):
        load_eval_set(_write(tmp_path, [_case("A", route_attendue="graphe")]))


def test_id_duplique(tmp_path):
    with pytest.raises(ValueError, match="dupliqués"):
        load_eval_set(_write(tmp_path, [_case("A"), _case("A")]))


def test_champ_inconnu(tmp_path):
    with pytest.raises(ValidationError):
        load_eval_set(_write(tmp_path, [_case("A", route_attendu="sql")]))


def test_reponse_attendue_optionnelle(tmp_path):
    loaded = load_eval_set(_write(tmp_path, [_case("A"), _case("B", reponse_attendue="42")]))
    assert [c.reponse_attendue for c in loaded.cases] == [None, "42"]


def test_eval_set_reel():
    loaded = load_eval_set()
    assert len(loaded.cases) == 70
    assert loaded.seuils.rappel_hybride == 0.8
