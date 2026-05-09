"""Chaque fixture représente un état possible du fichier manifest.json produit par `dbt compile`.
On n'utilise que les champs réellement lus par load_schema() pour rester lisible."""

import json
from pathlib import Path

import pytest

from src.schema_loader import load_schema

# dbt compile a tourné mais n'a trouvé aucun modèle
MANIFEST_NO_NODES = {"nodes": {}}

# dbt compile a produit des nodes, mais uniquement dans le layer staging (pas marts)
MANIFEST_NO_MARTS = {
    "nodes": {
        "model.project.staging_foo": {
            "path": "staging/foo.sql",
            "resource_type": "model",
            "name": "staging_foo",
            "description": "une table staging",
            "columns": {"id": {"description": "identifiant"}},
        }
    }
}

# Modèle marts déclaré dans dbt mais pas encore documenté (columns vide)
MANIFEST_EMPTY_COLUMNS = {
    "nodes": {
        "model.project.dim__assures": {
            "path": "marts/dim__assures.sql",
            "resource_type": "model",
            "name": "dim__assures",
            "description": "table des assurés",
            "columns": {},
        }
    }
}

MANIFEST_VALID = {
    "nodes": {
        "model.project.dim__assures": {
            "path": "marts/dim__assures.sql",
            "resource_type": "model",
            "name": "dim__assures",
            "description": "table des assurés",
            "columns": {
                "id_assure": {"description": "identifiant de l'assuré"},
                "nom": {"description": "nom de l'assuré"},
            },
        }
    }
}


def test_manifest_absent(monkeypatch):
    """MANIFEST_PATH pointe vers un fichier inexistant : FileNotFoundError."""
    monkeypatch.setattr(
        "src.schema_loader.MANIFEST_PATH", Path("/inexistant/manifest.json")
    )
    with pytest.raises(FileNotFoundError):
        load_schema()


def test_manifest_sans_nodes(tmp_path, monkeypatch):
    """Manifest valide JSON mais nodes vide : ValueError signalant l'absence de nodes."""
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(MANIFEST_NO_NODES), encoding="utf-8")
    monkeypatch.setattr("src.schema_loader.MANIFEST_PATH", manifest_file)
    # match= vérifie qu'on lève bien le bon ValueError (il y en a plusieurs dans load_schema)
    with pytest.raises(ValueError, match="aucun node"):
        load_schema()


def test_manifest_sans_marts(tmp_path, monkeypatch):
    """Nodes présents mais hors layer marts (ex. staging) : ValueError sur absence de marts."""
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(MANIFEST_NO_MARTS), encoding="utf-8")
    monkeypatch.setattr("src.schema_loader.MANIFEST_PATH", manifest_file)
    with pytest.raises(ValueError, match="marts"):
        load_schema()


def test_marts_sans_colonnes(tmp_path, monkeypatch):
    """Modèle marts déclaré dans dbt mais pas encore documenté (columns: {}) : ValueError."""
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(MANIFEST_EMPTY_COLUMNS), encoding="utf-8")
    monkeypatch.setattr("src.schema_loader.MANIFEST_PATH", manifest_file)
    with pytest.raises(ValueError, match="aucune colonne"):
        load_schema()


def test_cas_valide(tmp_path, monkeypatch):
    """Manifest complet : retourne un dict avec les tables marts et leurs colonnes."""
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(MANIFEST_VALID), encoding="utf-8")
    monkeypatch.setattr("src.schema_loader.MANIFEST_PATH", manifest_file)
    schema = load_schema()
    assert "dim__assures" in schema
    assert schema["dim__assures"]["description"] == "table des assurés"
    assert "id_assure" in schema["dim__assures"]["columns"]
    assert schema["dim__assures"]["columns"]["nom"] == "nom de l'assuré"
