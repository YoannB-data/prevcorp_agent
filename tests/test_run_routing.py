"""Tests du runner de routing, routeur simulé (aucun appel API)."""

import pytest

from evals.routing.load import EvalSet, RoutingCase, Seuils
from evals.routing.run_routing import render_report, run_once


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
