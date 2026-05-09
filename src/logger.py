"""Logging des interactions agent vers DuckDB."""

from datetime import datetime, timezone
from pathlib import Path

import duckdb

LOGS_DB_PATH = Path("logs/logs.duckdb")

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS interactions (
    timestamp        TIMESTAMPTZ NOT NULL,
    question         TEXT        NOT NULL,
    sql_generated    TEXT,
    status           TEXT        NOT NULL,
    latency_ms       INTEGER     NOT NULL,
    input_tokens     INTEGER     NOT NULL,
    output_tokens    INTEGER     NOT NULL,
    error_message    TEXT,
    eval_question_id TEXT
)
"""

_INSERT = """
INSERT INTO interactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def log_interaction(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    question: str,
    sql_generated: str | None,
    status: str,
    latency_ms: int,
    input_tokens: int,
    output_tokens: int,
    error_message: str | None = None,
    eval_question_id: str | None = None,
) -> None:
    """Insère une ligne dans la table interactions."""
    LOGS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(LOGS_DB_PATH))
    try:
        con.execute(_CREATE_TABLE)
        con.execute(
            _INSERT,
            [
                datetime.now(timezone.utc),
                question,
                sql_generated,
                status,
                latency_ms,
                input_tokens,
                output_tokens,
                error_message,
                eval_question_id,
            ],
        )
    finally:
        con.close()
