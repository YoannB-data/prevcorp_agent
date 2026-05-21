# PrevCorp Agent

Agent conversationnel Claude pour l'analyse de données de **prévoyance collective**. L'utilisateur pose une question en langage naturel via une interface Streamlit ; l'agent la traduit en SQL, l'exécute contre une base DuckDB et retourne un tableau de résultats avec une visualisation Plotly automatique.

## Fonctionnement

```
Question utilisateur (Streamlit)
       ↓
Few-shot selection (mots-clés)
       ↓
Injection schéma dbt + semantic layer
       ↓
Appel Claude API → génération SQL
       ↓
Exécution DuckDB (lecture seule)
  └─ Erreur SQL → retry avec feedback (max 3 tentatives)
       ↓
Résultat (DataFrame) + graphique Plotly
       ↓
Log JSONL (tokens, latence, coût)
```

## Prérequis

- Python 3.12
- [UV](https://docs.astral.sh/uv/) comme gestionnaire de paquets
- Clé API Anthropic
- Base DuckDB + manifests dbt compilés (`manifest.json` et `semantic_manifest.json`)

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
SEMANTIC_MANIFEST_PATH=/chemin/vers/semantic_manifest.json
DUCKDB_PATH=/chemin/vers/base.duckdb
```

## Utilisation

### Interface Streamlit

```bash
uv run streamlit run src/app.py
```

La sidebar affiche le score du dernier run d'évaluation et le nombre de questions posées dans la session.

### API Python

```python
from src.agent import agent_main

sql, df = agent_main("Combien de dossiers ouverts en 2024 ?")
print(df)
```

## Évaluations

```bash
uv run python evals/run_evals.py                 # suite complète
uv run python evals/run_evals.py --ids Q012 Q034 # questions spécifiques
```

Les résultats sont écrits dans `evals/reports/` (Markdown horodaté) et `evals/reports/latest.json` (lu par la sidebar Streamlit).

## Structure

```
src/
  app.py               # Interface Streamlit
  agent.py             # Orchestration Claude API, retry, logging
  config.py            # Paramètres (clés, chemins, modèle, coûts)
  schema_loader.py     # manifest.json (schéma) + semantic_manifest.json (métriques)
  duckdb_executor.py   # Exécution SQL en lecture seule
  few_shot_selector.py # Sélection d'exemples par mots-clés
  logger.py            # Log JSONL des interactions (tokens, latence, coût)
  chart_utils.py       # Détection et rendu de graphiques Plotly
  prompts/
    system_prompt.md   # Prompt système injecté dans chaque appel
    few_shot_bank.yml  # Banque d'exemples few-shot
evals/
  eval_set.yml         # Questions avec SQL de référence et mode de comparaison
  run_evals.py         # Runner d'évaluation
  reports/             # Rapports Markdown + latest.json
logs/
  interactions.jsonl   # Historique de toutes les interactions
```

## Schéma de données

Base en étoile :

| Type | Tables |
|------|--------|
| Dimensions | `dim__assures`, `dim__contrats`, `dim__entreprises`, `dim__beneficiaires` |
| Faits | `fct__dossiers`, `fct__paiements`, `fct__cotisations`, `fct__ressources`, `fct__contrats_entreprises` |

## Stack technique

- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) — client Claude API (`claude-sonnet-4-6`)
- [Streamlit](https://streamlit.io/) — interface utilisateur
- [DuckDB](https://duckdb.org/) — moteur SQL embarqué
- [Plotly](https://plotly.com/python/) — visualisations automatiques
- [pandas](https://pandas.pydata.org/) — manipulation des résultats
