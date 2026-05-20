"""Logging des interactions agent vers JSONL."""

import json
import logging
from datetime import datetime, timezone

from src import config

_logger = logging.getLogger(__name__)


def log_interaction(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    question: str,
    sql_generated: str | None,
    status: str,
    latency_ms: int,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
    error_message: str | None = None,
    eval_question_id: str | None = None,
) -> None:
    """Append une ligne JSON dans le fichier de log des interactions."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "eval_question_id": eval_question_id,
        "question": question,
        "sql_generated": sql_generated,
        "status": status,
        "latency_ms": latency_ms,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(cost_usd, 6),
        "error_message": error_message,
    }

    log_path = config.LOGS_JSONL_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as e:
        _logger.error("Échec écriture log interaction : %s", e)
