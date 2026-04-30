"""Configuration : chargement des variables d'environnement et chemins"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

# Chemins
MANIFEST_PATH = Path(os.getenv("MANIFEST_PATH"))
DUCKDB_PATH = Path(os.getenv("DUCKDB_PATH"))
