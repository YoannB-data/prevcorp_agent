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
AGENT_MODEL = "claude-sonnet-4-6"  # agent SQL + générateur RAG
ROUTER_MODEL = "claude-sonnet-4-6"
JUDGE_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

SEMANTIC_MANIFEST_PATH = Path(_require_env("SEMANTIC_MANIFEST_PATH"))
MANIFEST_PATH = Path(_require_env("MANIFEST_PATH"))
DUCKDB_PATH = Path(_require_env("DUCKDB_PATH"))

LOGS_JSONL_PATH = Path("logs/interactions.jsonl")

LATEST_EVAL_PATH = Path(__file__).parent.parent / "evals" / "reports" / "latest.json"

# Tarifs USD / 1M tokens (input, output), vérifiés le 2026-10-16 :
# https://platform.claude.com/docs/en/about-claude/pricing (docs.claude.com y redirige)
# Haiku 5.5 : palier "prompts jusqu'à 100 000 tokens" ; au-delà, 0.50 / 2.50
MODEL_PRICES: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-haiku-5-5": (0.10, 0.50),
}


def compute_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Coût en USD d'un appel ; KeyError si le modèle n'a pas de tarif."""

    input_price, output_price = MODEL_PRICES[model]
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000
