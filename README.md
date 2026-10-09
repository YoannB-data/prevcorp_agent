# PrevCorp Agent

Agent conversationnel Claude pour l'analyse de données de **prévoyance collective**. L'utilisateur pose une question en langage naturel via une interface Streamlit ; un routeur la classe comme question **structurée** (`sql`) ou **documentaire** (`rag`), puis l'oriente vers le pipeline correspondant :

- **SQL** : l'agent traduit la question en SQL, l'exécute contre une base DuckDB et retourne un tableau avec une visualisation Plotly automatique.
- **RAG** : la question est vectorisée (Voyage), les passages les plus proches sont retrouvés dans Qdrant, et Claude répond en citant ses sources.

## Fonctionnement

```
Question utilisateur (Streamlit)
       ↓
Routeur (appel Claude) → sql | rag
       ↓
Orchestrateur → pipeline SQL ou pipeline RAG
```

Pipeline SQL :

```
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

Pipeline RAG :

```
Embedding de la question (Voyage)
       ↓
Top-k chunks (Qdrant local, filtre optionnel par doc_type)
       ↓
Appel Claude → réponse avec citations des sources
```

## Prérequis

- Python 3.12
- [UV](https://docs.astral.sh/uv/) comme gestionnaire de paquets
- Clés API Anthropic et Voyage
- Base DuckDB + manifests dbt compilés (`manifest.json` et `semantic_manifest.json`)

## Installation

```bash
git clone <repo>
cd prevcorp_agent
uv sync --all-groups
uv run pre-commit install
```

## Configuration

Créer un fichier `.env` à la racine :

```env
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=...
MANIFEST_PATH=/chemin/vers/manifest.json
SEMANTIC_MANIFEST_PATH=/chemin/vers/semantic_manifest.json
DUCKDB_PATH=/chemin/vers/base.duckdb
```

Optionnel : `EDGE_BINARY` (chemin complet de l'exécutable Edge), utile uniquement sur une machine sans GTK3 pour le rendu HTML → PDF du corpus.

Lancer toutes les commandes depuis la racine du projet (les chemins des logs sont relatifs au répertoire courant).

## Utilisation

### Interface Streamlit

```bash
uv run streamlit run src/app.py
```

La sidebar affiche le score du dernier run d'évaluation et le nombre de questions posées dans la session.

### API Python

```python
from src.orchestrator import orchestrator_main

result = orchestrator_main("Combien de dossiers ouverts en 2024 ?")
```

Pour appeler directement le pipeline SQL : `from src.structured.sql_agent import agent_main` puis `sql, df = agent_main(question)`.

### Index RAG

L'index Qdrant (`qdrant_storage/`) n'est pas reconstruit automatiquement quand `corpus/` change :

```bash
uv run python -m src.rag.ingestion [--variant none|prefix] [--recreate]
```

## Évaluations

### SQL

```bash
uv run python evals/run_evals.py                 # suite complète
uv run python evals/run_evals.py --ids Q012 Q034 # questions spécifiques
```

Les résultats sont écrits dans `evals/reports/` (Markdown horodaté) et `evals/reports/latest.json` (lu par la sidebar Streamlit, écrit uniquement sur un run complet).

### RAG

```bash
uv run python evals/run_rag_evals.py [--k 5] [--variant none] [--ids RC01 ...]
```

Chaque question de `evals/rag_questions_v1_25.yml` est évaluée en retrieval (R), de bout en bout (E) et en génération isolée (I). Rapports dans `evals/reports/rag/`. Ne pas lancer pendant que Streamlit tourne (verrou disque Qdrant) ; les appels Voyage et Anthropic sont facturés.

Historique des jeux de questions RAG et de leurs hashes : [evals/CHANGELOG.md](evals/CHANGELOG.md).

## Harnais de développement (Claude Code)

Le repo embarque l'outillage agentique utilisé pour le construire :

- `CLAUDE.md` : commandes, conventions et pièges connus, chargés à chaque session
- `.claude/skills/corpus-generator/` : génère un document du corpus RAG depuis une spec
- `.claude/settings.json` : hook `PostToolUse` qui lance ruff (tous les `.py`) et mypy
  (`src/` uniquement) sur chaque fichier écrit ou édité par l'agent. En cas d'erreur,
  le hook sort en exit 2 et l'agent reçoit le diagnostic pour se corriger.

Limite connue : mypy ne vérifie que le fichier édité, pas ses appelants. Le hook sert
de feedback rapide ; la vérification complète reste celle de la CI.

## Structure

```
src/
  app.py               # Interface Streamlit
  router.py            # Classification sql / rag via Claude
  orchestrator.py      # Route puis délègue au pipeline SQL ou RAG
  config.py            # Paramètres (clés, chemins, modèle, coûts)
  logger.py            # Log JSONL des interactions (tokens, latence, coût)
  structured/          # Pipeline SQL
    sql_agent.py         # Orchestration Claude API, retry, logging
    schema_loader.py     # manifest.json (schéma) + semantic_manifest.json (métriques)
    duckdb_executor.py   # Exécution SQL en lecture seule
    few_shot_selector.py # Sélection d'exemples par mots-clés
    chart_utils.py       # Détection et rendu de graphiques Plotly
  rag/                 # Pipeline RAG (Qdrant)
    ingestion.py         # PDF → chunks → embeddings Voyage → Qdrant
    retriever.py         # Question → top-k chunks
    generator.py         # Chunks + question → réponse citée
    pdf_text.py          # Extraction du texte des PDF
    metadata.py          # Métadonnées des documents (doc_id, doc_type)
    eval_schema.py       # Schéma du YAML d'éval RAG
    evaluation/          # Runner d'éval RAG (retrieval, scorers, juge, faithfulness, diagnose, rapport)
  prompts/
    system_prompt.md   # Prompt système injecté dans chaque appel
    few_shot_bank.yml  # Banque d'exemples few-shot
evals/
  eval_set.yml         # Questions avec SQL de référence et mode de comparaison
  run_evals.py         # Runner d'évaluation SQL
  rag_questions_v1_25.yml # 25 questions d'éval RAG
  run_rag_evals.py     # Runner d'évaluation RAG
  reports/             # Rapports Markdown + latest.json (rag/ pour le RAG)
corpus/                # PDF du corpus (gitignorés, dérivés de corpus_src/)
corpus_src/            # Sources HTML du corpus, versionnées
qdrant_storage/        # Collection Qdrant locale
scripts/               # dump_chunks.py (lecture des chunks Qdrant)
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

- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) — client Claude API (modèle défini dans `src/config.py`)
- [Voyage AI](https://www.voyageai.com/) — embeddings pour le RAG
- [Qdrant](https://qdrant.tech/) — base vectorielle (mode local embarqué)
- [Streamlit](https://streamlit.io/) — interface utilisateur
- [DuckDB](https://duckdb.org/) — moteur SQL embarqué
- [Plotly](https://plotly.com/python/) — visualisations automatiques
- [pandas](https://pandas.pydata.org/) — manipulation des résultats
- [Ruff](https://github.com/astral-sh/ruff) — formatter + linter (remplace black, isort, flake8)
- [mypy](https://mypy-lang.org/) — type checking statique
- [pre-commit](https://pre-commit.com/) — hooks git locaux
