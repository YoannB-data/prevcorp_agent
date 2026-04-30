"""Chargement du schéma DuckDB pour injection dans le contexte Claude"""
import json

from src.config import MANIFEST_PATH


def load_schema() -> dict:
    """Lit le manifest dbt et retourne le schéma des modèles marts"""

    if MANIFEST_PATH is None or not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"manifest.json introuvable : {MANIFEST_PATH}")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        schema = {}

        # Itérer sur un dictionnaire
        for _, value in data["nodes"].items():
            if ("marts" in value["path"]) and (value["resource_type"] == "model"):
                table_name = value["name"]  # ex: "dim__assures"

                # Construire le dict des colonnes
                columns = {}
                for col_name, col_info in value["columns"].items():
                    columns[col_name] = col_info["description"]

                # Ajouter la table au schéma
                schema[table_name] = {
                    "description": value["description"],
                    "columns": columns,
                }
    return schema
