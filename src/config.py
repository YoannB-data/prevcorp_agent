"""Configuration : chargement des variables d'environnement et chemins"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    """Retourne la valeur d'une variable d'environnement requise, lève si absente."""

    val = os.getenv(name)
    if val is None:
        raise OSError(f"Variable d'environnement requise manquante : {name}")
    return val


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

SEMANTIC_MANIFEST_PATH = Path(_require_env("SEMANTIC_MANIFEST_PATH"))
MANIFEST_PATH = Path(_require_env("MANIFEST_PATH"))
DUCKDB_PATH = Path(_require_env("DUCKDB_PATH"))

LOGS_JSONL_PATH = Path("logs/interactions.jsonl")

LATEST_EVAL_PATH = Path(__file__).parent.parent / "evals" / "reports" / "latest.json"

# Pricing Anthropic — claude-sonnet-4-6
COST_PER_INPUT_TOKEN: float = 3.0 / 1_000_000  # $3 / 1M tokens
COST_PER_OUTPUT_TOKEN: float = 15.0 / 1_000_000  # $15 / 1M tokens
