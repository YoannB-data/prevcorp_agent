"""Tests unitaires pour execute_query() — chaque test contrôle DUCKDB_PATH via monkeypatch
pour ne jamais toucher la base réelle du projet."""
import duckdb
import pandas as pd
import pytest

from src.duckdb_executor import execute_query


def _create_db(path):
    """Ouvre la base en écriture pour initialiser le schéma, puis la ferme."""
    with duckdb.connect(str(path)) as con:
        con.execute("CREATE TABLE test (id INTEGER, nom TEXT)")
        con.execute("INSERT INTO test VALUES (1, 'alice'), (2, 'bob')")


def test_base_absente(monkeypatch):
    """DUCKDB_PATH pointe vers un fichier inexistant : FileNotFoundError."""
    from pathlib import Path

    monkeypatch.setattr("src.duckdb_executor.DUCKDB_PATH", Path("/inexistant/db.duckdb"))
    with pytest.raises(FileNotFoundError):
        execute_query("SELECT 1")


def test_base_vide(monkeypatch, tmp_path):
    """Base DuckDB créée mais aucune table : requête sur table inconnue : ValueError."""
    db_file = tmp_path / "empty.duckdb"
    # Crée le fichier sans aucune table
    with duckdb.connect(str(db_file)):
        pass
    monkeypatch.setattr("src.duckdb_executor.DUCKDB_PATH", db_file)
    with pytest.raises(ValueError):
        execute_query("SELECT * FROM dim__assures")


def test_sql_invalide(monkeypatch, tmp_path):
    """Syntaxe SQL incorrecte : duckdb.Error wrappé en ValueError."""
    db_file = tmp_path / "db.duckdb"
    _create_db(db_file)
    monkeypatch.setattr("src.duckdb_executor.DUCKDB_PATH", db_file)
    with pytest.raises(ValueError):
        execute_query("SLECT * FORM test")


def test_sql_vide(monkeypatch, tmp_path):
    """Chaîne SQL vide : duckdb.Error wrappé en ValueError."""
    db_file = tmp_path / "db.duckdb"
    _create_db(db_file)
    monkeypatch.setattr("src.duckdb_executor.DUCKDB_PATH", db_file)
    with pytest.raises(ValueError):
        execute_query("")


def test_ecriture_interdite(monkeypatch, tmp_path):
    """Tentative d'écriture sur une base ouverte en read_only : ValueError."""
    db_file = tmp_path / "db.duckdb"
    _create_db(db_file)
    monkeypatch.setattr("src.duckdb_executor.DUCKDB_PATH", db_file)
    with pytest.raises(ValueError):
        execute_query("INSERT INTO test VALUES (3, 'charlie')")


def test_cas_valide(monkeypatch, tmp_path):
    """Requête SELECT valide : retourne un DataFrame avec les bonnes données."""
    db_file = tmp_path / "db.duckdb"
    _create_db(db_file)
    monkeypatch.setattr("src.duckdb_executor.DUCKDB_PATH", db_file)
    df = execute_query("SELECT * FROM test ORDER BY id")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "nom"]
    assert len(df) == 2
    assert df.iloc[0]["nom"] == "alice"
    assert df.iloc[1]["id"] == 2
