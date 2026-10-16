"""Configuration : chargement des variables d'environnement et chemins"""

import os
from pathlib import Path
from typing import Any

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


# Capacités d'appel par modèle. Sonnet 5.5 renvoie un 400 sur temperature non défaut :
# https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide (section Breaking changes)
MODEL_PARAMS: dict[str, dict[str, bool]] = {
    "claude-sonnet-4-6": {"supports_temperature": True},
    "claude-sonnet-5-5": {"supports_temperature": False},
}


def _validate_models(
    roles: dict[str, str],
    prices: dict[str, tuple[float, float]],
    params: dict[str, dict[str, bool]],
) -> None:
    """Vérifie que chaque rôle a un tarif et des paramètres d'appel ; lève ValueError sinon."""

    # Guard - un modèle inconnu doit faire échouer le démarrage, pas un appel API déjà facturé
    for table_name, table in (("MODEL_PRICES", prices), ("MODEL_PARAMS", params)):
        missing = {role: model for role, model in roles.items() if model not in table}
        if missing:
            detail = ", ".join(f"{role}={model!r}" for role, model in missing.items())
            raise ValueError(f"Modèle(s) absent(s) de {table_name} : {detail}")


_validate_models(
    {"AGENT_MODEL": AGENT_MODEL, "ROUTER_MODEL": ROUTER_MODEL, "JUDGE_MODEL": JUDGE_MODEL},
    MODEL_PRICES,
    MODEL_PARAMS,
)


def sampling_kwargs(model: str, temperature: float) -> dict[str, Any]:
    """Kwargs d'échantillonnage acceptés par le modèle ; ValueError si le modèle est inconnu."""

    # Guard - un --judge-model hors table échoue ici, avant tout appel API
    if model not in MODEL_PARAMS:
        raise ValueError(f"Modèle absent de MODEL_PARAMS : {model!r}")
    return {"temperature": temperature} if MODEL_PARAMS[model]["supports_temperature"] else {}


def compute_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Coût en USD d'un appel ; KeyError si le modèle n'a pas de tarif."""

    # Le palier Haiku 5.5 au-delà de 100k tokens de prompt n'est pas géré : tarif ≤ 100k appliqué
    input_price, output_price = MODEL_PRICES[model]
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000
