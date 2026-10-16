"""Tests du runner de routing, routeur simulé (aucun appel API)."""

import json

import pytest

from evals.routing.load import EvalSet, RoutingCase, Seuils
from evals.routing.run_routing import (
    build_payload,
    parse_payload,
    render_report,
    run_once,
)


def _set() -> EvalSet:
    def case(i: str, route: str) -> RoutingCase:
        return RoutingCase(
            id=i, question=i, route_attendue=route, forme="simple", origine="x", note="n"
        )

    seuils = Seuils(accuracy=0.9, rappel_hybride=0.8)
    return EvalSet(cases=[case("A", "sql"), case("B", "hybride")], seuils=seuils)


def test_value_error_devient_erreur():
    def fake(question: str) -> str:
        if question == "B":
            raise ValueError("hors sql/rag")
        return "sql"

    assert [p.predicted for p in run_once(_set(), fake)] == ["sql", "erreur"]


def test_autre_exception_plante_le_run():
    def fake(question: str) -> str:
        raise ConnectionError("réseau")

    with pytest.raises(ConnectionError):
        run_once(_set(), fake)


def test_rapport_classe_jamais_predite():
    runs = [run_once(_set(), lambda q: "sql")]
    report = render_report(_set(), runs, model="m", commit="abc", date="d")
    assert "| hybride | 0.0% | n/a |" in report
    assert "non exposés par le routeur" in report


def test_aller_retour_json_identique():
    eval_set = _set()

    def fake(question: str) -> str:
        if question == "B":
            raise ValueError("hors sql/rag")
        return "sql"

    runs = [run_once(eval_set, fake), run_once(eval_set, lambda q: "rag")]
    header = {"model": "m", "commit": "abc", "runs": 2, "date": "d"}
    direct = render_report(eval_set, runs, model="m", commit="abc", date="d")

    payload = json.loads(json.dumps(build_payload(eval_set, runs, header)))
    header_back, runs_back = parse_payload(eval_set, payload)
    again = render_report(
        eval_set,
        runs_back,
        model=header_back["model"],
        commit=header_back["commit"],
        date=header_back["date"],
    )
    assert again == direct
    assert payload["runs"][0][1]["route_predite"] == "erreur"


def test_json_d_un_autre_eval_set_refuse():
    eval_set = _set()
    payload = build_payload(eval_set, [run_once(eval_set, lambda q: "sql")], {})
    payload["runs"][0][0]["id"] = "Z"
    with pytest.raises(ValueError, match="différentes du YAML"):
        parse_payload(eval_set, payload)
