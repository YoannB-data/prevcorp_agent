import duckdb
import pandas as pd
from src.config import DUCKDB_PATH

def execute_query(sql: str) -> pd.DataFrame:
    """Execute a SQL query on the DuckDB datawarehouse."""
    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(f"DuckDB introuvable : {DUCKDB_PATH}")
    try:
        with duckdb.connect(str(DUCKDB_PATH), read_only=True) as con:
            return con.sql(sql).df()
    except duckdb.Error as e:
        raise ValueError(f"Erreur SQL : {e}")