"""Tests des métriques de routing (fixture de 6 cas calculée à la main)."""

from evals.routing.metrics import (
    accuracy,
    accuracy_by_forme,
    confusion_matrix,
    fmt_ratio,
    mean_min_max,
    precision,
    recall,
    unstable_ids,
)

# attendu -> prédit : sql->sql, sql->rag, rag->rag, rag->rag, hybride->sql, hybride->rag
PAIRS = [
    ("sql", "sql"),
    ("sql", "rag"),
    ("rag", "rag"),
    ("rag", "rag"),
    ("hybride", "sql"),
    ("hybride", "rag"),
]


def test_accuracy():
    assert accuracy(PAIRS) == 3 / 6


def test_confusion_matrix():
    m = confusion_matrix(PAIRS)
    assert m["sql"] == {"sql": 1, "rag": 1, "hybride": 0}
    assert m["rag"] == {"sql": 0, "rag": 2, "hybride": 0}
    assert m["hybride"] == {"sql": 1, "rag": 1, "hybride": 0}


def test_rappel():
    assert recall(PAIRS, "sql") == 1 / 2
    assert recall(PAIRS, "rag") == 1.0
    assert recall(PAIRS, "hybride") == 0.0


def test_precision():
    assert precision(PAIRS, "sql") == 1 / 2
    assert precision(PAIRS, "rag") == 2 / 4


def test_classe_jamais_predite_n_a():
    assert precision(PAIRS, "hybride") is None
    assert fmt_ratio(precision(PAIRS, "hybride")) == "n/a"
    assert fmt_ratio(0.5) == "50.0%"


def test_erreur_comptee_fausse_hors_matrice():
    pairs = [("sql", "sql"), ("sql", "erreur")]
    assert accuracy(pairs) == 0.5
    assert recall(pairs, "sql") == 0.5
    assert sum(sum(row.values()) for row in confusion_matrix(pairs).values()) == 1


def test_accuracy_par_forme():
    items = [
        ("simple", "sql", "sql"),
        ("simple", "sql", "rag"),
        ("piege", "rag", "rag"),
    ]
    result = accuracy_by_forme(items)
    assert result["simple"] == 0.5
    assert result["piege"] == 1.0
    assert result["implicite"] is None


def test_instables():
    preds = {"A": ["sql", "sql", "sql"], "B": ["sql", "rag", "sql"], "C": ["rag", "erreur"]}
    assert unstable_ids(preds) == ["B", "C"]


def test_mean_min_max():
    assert mean_min_max([0.5, 1.0, 0.75]) == (0.75, 0.5, 1.0)
