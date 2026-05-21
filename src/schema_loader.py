"""Chargement du schéma DuckDB pour injection dans le contexte Claude"""

import json

from src.config import MANIFEST_PATH, SEMANTIC_MANIFEST_PATH


def load_schema() -> dict[str, dict]:
    """Lit le manifest dbt et retourne le schéma des modèles marts"""

    # Guard - fichier absent ou MANIFEST_PATH non configuré
    if MANIFEST_PATH is None or not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"manifest.json introuvable : {MANIFEST_PATH}")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        schema = {}

        # Guard - manifest vide, probablement un dbt compile qui n'a pas tourné
        if not data["nodes"]:
            raise ValueError("manifest.json ne contient aucun node")

        excluded_models = {"metricflow_time_spine"}

        for _, value in data["nodes"].items():
            table_name = value["name"]  # ex: "dim__assures"
            # On ne garde que les modèles du layer marts (pas sources, tests, snapshots…)
            if (
                "marts" in value["path"]
                and value["resource_type"] == "model"
                and table_name not in excluded_models
            ):

                # Guard - colonnes vides, modèle déclaré mais pas encore documenté dans dbt
                if not value["columns"]:
                    raise ValueError(
                        f"Le modèle '{table_name}' ne contient aucune colonne"
                    )

                columns = {}
                for col_name, col_info in value["columns"].items():
                    columns[col_name] = col_info["description"]

                schema[table_name] = {
                    "description": value["description"],
                    "columns": columns,
                }

        # Guard - aucun modèle marts trouvé, manifest issu d'un autre layer (staging, seeds…)
        if not schema:
            raise ValueError(
                "manifest.json ne contient aucun modèle dans le layer marts"
            )

    return schema


def load_metrics() -> dict[str, dict]:
    """Lit le semantic_manifest dbt et retourne les métriques disponibles"""

    # Guard - fichier absent ou SEMANTIC_MANIFEST_PATH non configuré
    if SEMANTIC_MANIFEST_PATH is None or not SEMANTIC_MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"semantic_manifest.json introuvable : {SEMANTIC_MANIFEST_PATH}"
        )

    with open(SEMANTIC_MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        metrics = {}

        # Guard - semantic manifest vide, probablement un dbt parse qui n'a pas tourné
        if not data["metrics"]:
            raise ValueError("semantic_manifest.json ne contient aucune métrique")

        for metric in data["metrics"]:
            name = metric["name"]
            metrics[name] = {
                "label": metric["label"],
                "description": metric.get("description", ""),
                "type": metric["type"],
                "measure": metric["type_params"]["measure"]["name"],
            }

    return metrics
