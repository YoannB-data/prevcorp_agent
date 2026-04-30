# PrevCorp Agent

> **Work In Progress** — projet en cours de développement.

Agent conversationnel Claude pour l'analyse de données de **prévoyance collective**. L'utilisateur pose une question en langage naturel ; l'agent la traduit en SQL, l'exécute contre une base DuckDB et retourne un résultat formaté.

## Fonctionnement

```
Question utilisateur
       ↓
Chargement du schéma (manifest dbt)
       ↓
Appel Claude API → génération SQL
       ↓
Exécution DuckDB (lecture seule)
       ↓
Résultat (DataFrame)
```

## Prérequis

- Python 3.12
- [UV](https://docs.astral.sh/uv/) comme gestionnaire de paquets
- Clé API Anthropic

## Installation

```bash
git clone <repo>
cd prevcorp_agent
uv sync
```

## Configuration

Créer un fichier `.env` à la racine :

```env
ANTHROPIC_API_KEY=sk-ant-...
MANIFEST_PATH=/chemin/vers/manifest.json
DUCKDB_PATH=/chemin/vers/base.duckdb
```

## Utilisation

```bash
uv run python -m src
```

## Structure

```
src/
  agent.py           # Orchestration principale, appel Claude API
  config.py          # Paramètres (clés, chemins, modèle)
  schema_loader.py   # Lecture du manifest dbt → contexte schéma
  duckdb_executor.py # Exécution SQL en lecture seule
  prompts/
    system_prompt.md # Prompt système injecté dans chaque conversation
evals/
  eval_set.yaml      # 63 questions d'évaluation (catégories, niveaux)
```

## Schéma de données

Base en étoile :

| Type | Tables |
|------|--------|
| Dimensions | `dim__assures`, `dim__contrats`, `dim__entreprises`, `dim__beneficiaires` |
| Faits | `fct__dossiers`, `fct__paiements`, `fct__cotisations`, `fct__ressources` |

## Évaluations

63 questions de test couvrant : `agregation`, `liste`, `filtrage_temporel`, `filtrage_entite`, `top_n`, `multi_criteres`, `dossier_individuel`, `rag`, `hors_scope`.

```bash
uv run pytest
```

## Stack technique

- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) — client Claude API
- [DuckDB](https://duckdb.org/) — moteur SQL embarqué
- [Pydantic](https://docs.pydantic.dev/) — validation de configuration
- [pandas](https://pandas.pydata.org/) — manipulation des résultats
