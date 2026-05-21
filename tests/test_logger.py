# pylint: disable=duplicate-code
"""Tests unitaires pour log_interaction() — chaque test redirige LOGS_JSONL_PATH via monkeypatch
pour ne jamais toucher le fichier de logs réel du projet."""

import json
from pathlib import Path

from src.logger import log_interaction


def _read_interactions(jsonl_path: Path) -> list[dict]:
    """Retourne toutes les lignes loggées sous forme de dicts."""
    with open(jsonl_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def test_insertion_valide(monkeypatch, tmp_path):
    """Appel complet avec tous les champs remplis : 1 ligne insérée avec les bons champs."""
    jsonl_file = tmp_path / "interactions.jsonl"
    monkeypatch.setattr("src.config.LOGS_JSONL_PATH", jsonl_file)

    log_interaction(
        question="Combien de dossiers ouverts ?",
        sql_generated="SELECT COUNT(*) FROM fct__dossiers",
        status="success",
        latency_ms=342,
        input_tokens=512,
        output_tokens=64,
        cost_usd=0.001234,
        error_message=None,
        eval_question_id="q01",
    )

    rows = _read_interactions(jsonl_file)
    assert len(rows) == 1
    row = rows[0]
    assert row["question"] == "Combien de dossiers ouverts ?"
    assert row["sql_generated"] == "SELECT COUNT(*) FROM fct__dossiers"
    assert row["status"] == "success"
    assert row["latency_ms"] == 342
    assert row["input_tokens"] == 512
    assert row["output_tokens"] == 64
    assert row["cost_usd"] == 0.001234
    assert row["error_message"] is None
    assert row["eval_question_id"] == "q01"


def test_appel_multiple(monkeypatch, tmp_path):
    """Deux appels successifs : pas d'exception, 2 lignes dans le fichier."""
    jsonl_file = tmp_path / "interactions.jsonl"
    monkeypatch.setattr("src.config.LOGS_JSONL_PATH", jsonl_file)

    log_interaction(
        question="Question 1",
        sql_generated="SELECT 1",
        status="success",
        latency_ms=100,
        input_tokens=50,
        output_tokens=10,
        cost_usd=0.0,
    )
    log_interaction(
        question="Question 2",
        sql_generated="SELECT 2",
        status="error",
        latency_ms=200,
        input_tokens=60,
        output_tokens=20,
        cost_usd=0.0,
        error_message="Timeout",
    )

    rows = _read_interactions(jsonl_file)
    assert len(rows) == 2


def test_champs_none(monkeypatch, tmp_path):
    """sql_generated, error_message et eval_question_id à None : 1 ligne insérée sans exception."""
    jsonl_file = tmp_path / "interactions.jsonl"
    monkeypatch.setattr("src.config.LOGS_JSONL_PATH", jsonl_file)

    log_interaction(
        question="Question sans SQL",
        sql_generated=None,
        status="error",
        latency_ms=50,
        input_tokens=30,
        output_tokens=5,
        cost_usd=0.0,
        error_message=None,
        eval_question_id=None,
    )

    rows = _read_interactions(jsonl_file)
    assert len(rows) == 1
    row = rows[0]
    assert row["sql_generated"] is None
    assert row["error_message"] is None
    assert row["eval_question_id"] is None
