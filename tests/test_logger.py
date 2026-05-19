# pylint: disable=duplicate-code
"""Tests unitaires pour log_interaction() — chaque test contrôle LOGS_DB_PATH via monkeypatch
pour ne jamais toucher la base de logs réelle du projet."""

from pathlib import Path

import duckdb

from src.logger import log_interaction


def _read_interactions(db_path: Path) -> list:
    """Retourne toutes les lignes de la table interactions."""

    with duckdb.connect(str(db_path)) as con:
        return con.execute("SELECT * FROM interactions").fetchall()


def test_insertion_valide(monkeypatch, tmp_path):
    """Appel complet avec tous les champs remplis : 1 ligne insérée avec les bons champs."""

    db_file = tmp_path / "logs.duckdb"
    monkeypatch.setattr("src.logger.LOGS_DB_PATH", db_file)

    log_interaction(
        question="Combien de dossiers ouverts ?",
        sql_generated="SELECT COUNT(*) FROM fct__dossiers",
        status="success",
        latency_ms=342,
        input_tokens=512,
        output_tokens=64,
        error_message=None,
        eval_question_id="q01",
    )

    rows = _read_interactions(db_file)
    assert len(rows) == 1
    (
        _,
        question,
        sql_generated,
        status,
        latency_ms,
        input_tokens,
        output_tokens,
        error_message,
        eval_question_id,
    ) = rows[0]
    assert question == "Combien de dossiers ouverts ?"
    assert sql_generated == "SELECT COUNT(*) FROM fct__dossiers"
    assert status == "success"
    assert latency_ms == 342
    assert input_tokens == 512
    assert output_tokens == 64
    assert error_message is None
    assert eval_question_id == "q01"


def test_appel_multiple(monkeypatch, tmp_path):
    """Deux appels successifs : pas d'exception, 2 lignes dans la base."""

    db_file = tmp_path / "logs.duckdb"
    monkeypatch.setattr("src.logger.LOGS_DB_PATH", db_file)

    log_interaction(
        question="Question 1",
        sql_generated="SELECT 1",
        status="success",
        latency_ms=100,
        input_tokens=50,
        output_tokens=10,
    )
    log_interaction(
        question="Question 2",
        sql_generated="SELECT 2",
        status="error",
        latency_ms=200,
        input_tokens=60,
        output_tokens=20,
        error_message="Timeout",
    )

    rows = _read_interactions(db_file)
    assert len(rows) == 2


def test_champs_none(monkeypatch, tmp_path):
    """sql_generated, error_message et eval_question_id à None : 1 ligne insérée sans exception."""

    db_file = tmp_path / "logs.duckdb"
    monkeypatch.setattr("src.logger.LOGS_DB_PATH", db_file)

    log_interaction(
        question="Question sans SQL",
        sql_generated=None,
        status="error",
        latency_ms=50,
        input_tokens=30,
        output_tokens=5,
        error_message=None,
        eval_question_id=None,
    )

    rows = _read_interactions(db_file)
    assert len(rows) == 1
    _, _, sql_generated, _, _, _, _, error_message, eval_question_id = rows[0]
    assert sql_generated is None
    assert error_message is None
    assert eval_question_id is None
