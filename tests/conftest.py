"""Configuration pytest : variables d'environnement factices pour les tests unitaires.

Chargé par pytest avant toute collecte de tests — satisfait config.py à l'import
sans toucher les valeurs réelles si elles sont déjà définies dans l'environnement.
"""

import os

# Guard - config.py appelle _require_env() au niveau module : il faut des valeurs
# présentes avant l'import, les fixtures monkeypatch n'intervenant qu'après.
os.environ.setdefault("ANTHROPIC_API_KEY", "dummy-key-for-tests")
os.environ.setdefault("MANIFEST_PATH", "/dummy/manifest.json")
os.environ.setdefault("SEMANTIC_MANIFEST_PATH", "/dummy/semantic_manifest.json")
os.environ.setdefault("DUCKDB_PATH", "/dummy/db.duckdb")
