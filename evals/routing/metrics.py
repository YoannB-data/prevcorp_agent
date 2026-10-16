"""Métriques de routing : fonctions pures, sans I/O ni appel API."""

from collections import defaultdict
from collections.abc import Sequence
from typing import get_args

from evals.routing.load import Forme, Route

ROUTES: tuple[Route, ...] = get_args(Route)
FORMES: tuple[Forme, ...] = get_args(Forme)
ERREUR = "erreur"

# (route attendue, route prédite ou "erreur")
Pair = tuple[str, str]


def accuracy(pairs: Sequence[Pair]) -> float:
    """Part des prédictions égales à l'attendu ; une erreur compte fausse."""

    return sum(e == p for e, p in pairs) / len(pairs)


def confusion_matrix(pairs: Sequence[Pair]) -> dict[Route, dict[Route, int]]:
    """Matrice lignes = attendu, colonnes = prédit ; les erreurs en sont exclues."""

    matrix: dict[Route, dict[Route, int]] = {e: {p: 0 for p in ROUTES} for e in ROUTES}
    for expected, predicted in pairs:
        if predicted in ROUTES:
            matrix[expected][predicted] += 1  # type: ignore[index]
    return matrix


def recall(pairs: Sequence[Pair], cls: Route) -> float | None:
    """Rappel d'une classe (une erreur compte manquée) ; None si elle n'est jamais attendue."""

    predicted = [p for e, p in pairs if e == cls]
    return predicted.count(cls) / len(predicted) if predicted else None


def precision(pairs: Sequence[Pair], cls: Route) -> float | None:
    """Précision d'une classe ; None si elle n'est jamais prédite."""

    expected = [e for e, p in pairs if p == cls]
    return expected.count(cls) / len(expected) if expected else None


def accuracy_by_forme(items: Sequence[tuple[Forme, str, str]]) -> dict[Forme, float | None]:
    """Accuracy par forme depuis des triplets (forme, attendu, prédit) ; None si forme absente."""

    grouped: dict[Forme, list[Pair]] = defaultdict(list)
    for forme, expected, predicted in items:
        grouped[forme].append((expected, predicted))
    return {f: accuracy(grouped[f]) if grouped[f] else None for f in FORMES}


def unstable_ids(predictions: dict[str, Sequence[str]]) -> list[str]:
    """IDs dont la route prédite varie selon les runs, dans l'ordre d'entrée."""

    return [qid for qid, preds in predictions.items() if len(set(preds)) > 1]


def mean_min_max(values: Sequence[float]) -> tuple[float, float, float]:
    """Moyenne, minimum et maximum."""

    return sum(values) / len(values), min(values), max(values)


def fmt_ratio(value: float | None) -> str:
    """Pourcentage à une décimale, ou « n/a » si la valeur est indéfinie."""

    return "n/a" if value is None else f"{value:.1%}"
