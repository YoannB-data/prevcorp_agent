# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PrevCorp Agent** is a Claude-powered conversational agent for French employee insurance ("prévoyance collective") data. Users ask natural language questions via a Streamlit UI; a router classifies each question as `sql` (structured data query) or `rag` (document Q&A), and an orchestrator dispatches to the matching pipeline.

## Environment & Package Manager

- Python 3.12 (pinned in `.python-version`)
- **UV** is the package manager — use `uv` commands, not raw `pip`
- Environment variables loaded from `.env` via python-dotenv; required: `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `MANIFEST_PATH`, `SEMANTIC_MANIFEST_PATH`, `DUCKDB_PATH`

```bash
uv sync --all-groups                             # install dependencies (incl. dev tools)
uv run pre-commit install                        # install git hooks (once per clone)
uv run streamlit run src/app.py                  # launch Streamlit UI
uv run python evals/run_evals.py                 # run full eval suite (SQL pipeline only)
uv run python evals/run_evals.py --ids Q012 Q034 # run specific evals by ID
uv run pytest                                    # run tests
uv run pytest tests/test_foo.py::test_bar        # run a single test
uv run ruff format src/ tests/ evals/ && uv run ruff check src/ tests/ evals/  # format + lint
uv run mypy src/                                  # type checking
```

These are exactly the checks CI (`.github/workflows/ci.yml`) runs on every PR/push to `main`: `ruff format --check`, `ruff check`, `mypy src/`, `pytest tests/`.

## Architecture

```
src/
  app.py               # Streamlit UI: chat_input, history, sidebar with eval score
  router.py            # LLM call that classifies a question as "sql" or "rag"
  orchestrator.py      # orchestrator_main(): routes then delegates to sql_agent or rag.generator
  config.py            # Settings: API keys, DB path, model, token costs, paths
  logger.py            # Appends interaction records to logs/interactions.jsonl
  structured/          # SQL pipeline (DuckDB / dbt-backed)
    sql_agent.py        # Claude API orchestration: agent_main(), retry loop, logging
    schema_loader.py     # Reads dbt manifest.json (schema) + semantic_manifest.json (metrics)
    duckdb_executor.py   # Executes SQL against DuckDB in read-only mode
    few_shot_selector.py # Keyword-based few-shot selection from prompts/few_shot_bank.yml
    chart_utils.py        # Plotly chart auto-detection and rendering
  rag/                  # Document Q&A pipeline (Qdrant-backed)
    ingestion.py          # PDF → text → chunks → Voyage embeddings → Qdrant (run standalone to (re)build the index)
    retriever.py           # question → top-k relevant chunks from Qdrant
    generator.py            # chunks + question → cited answer via Claude
  prompts/
    system_prompt.md   # System prompt injected into every SQL agent call
    few_shot_bank.yml  # Few-shot examples pool (question + sql + keywords)
evals/
  eval_set.yml         # Evaluation questions with reference SQL and compare modes (SQL pipeline)
  rag_questions_draft.yml # Draft corpus of RAG-pipeline eval questions (not yet wired into run_evals.py)
  run_evals.py          # Eval runner: run_evals(), run_single_eval(), write_report()
  reports/               # Timestamped Markdown reports + latest.json (read by sidebar)
corpus/                # Source PDFs ingested into the RAG index (conditions générales, fiches, FAQ, circulaires)
qdrant_storage/        # Local (embedded) Qdrant collection, populated by src/rag/ingestion.py
logs/
  interactions.jsonl   # Append-only log: question, sql, status, tokens, cost, latency
```

**Request flow**: `orchestrator_main(question)` (`src/orchestrator.py`) → `router.route()` classifies the question via a dedicated Claude call (`sql` or `rag`) → dispatches to one of two independent pipelines, returned as a unified `OrchestratorResult`:

- **SQL pipeline** (`src/structured/sql_agent.py`): `agent_main(question)` builds a message with few-shot examples + schema + semantic layer → `_call_llm_with_retry()` → `_extract_sql()` → `execute_query()`. On SQL error: appends error + attempted SQL to the message and retries (up to `_MAX_RETRIES=3`). Logs every attempt (success or error) to JSONL. Returns `(sql_str, pd.DataFrame)`.
- **RAG pipeline** (`src/rag/generator.py`): `generate(question)` → `retriever.retrieve()` embeds the question with Voyage and queries Qdrant for top-k chunks (optionally filtered by `doc_type`) → chunks are formatted into context and sent to Claude with a citation-enforcing system prompt → returns `{question, answer, sources, chunks}`. The RAG pipeline has no eval harness or retry loop yet.

**Two distinct retry loops in the SQL pipeline** (do not confuse them):
- **Outer loop** in `agent_main` (up to `_MAX_RETRIES=3`): SQL correction — on `execute_query()` failure, the error + attempted SQL are appended to the message and Claude is called again.
- **Inner loop** in `_call_llm_with_retry`: transient API errors only (`RateLimitError`, `APITimeoutError`, `APIConnectionError`, `APIStatusError`) with exponential backoff. `AuthenticationError` is re-raised immediately (not retried).

**Important constraints**:
- In `sql_agent.py`, `_SCHEMA`, `_METRICS`, and `_SYSTEM_PROMPT` are cached at module import — changes require process restart, not just a new call.
- `few_shot_bank.yml` is **reloaded on every call** to `agent_main` (no module-level cache) — changes take effect immediately without restart.
- Schema comes from `manifest.json` (dbt nodes, `marts` layer only). Metrics come from `semantic_manifest.json` (dbt semantic layer). Both paths via env vars.
- SQL must be wrapped in a ` ```sql ``` ` fence; `_extract_sql` raises `ValueError` otherwise.
- Model: `claude-sonnet-4-6` (shared by the SQL agent, the router, and the RAG generator via `src/config.py`), `MAX_TOKENS=1024`, `temperature=0` on the SQL agent and router. Prompt caching not yet implemented.
- `agent_main` accepts an optional `eval_question_id` for traceability in the JSONL log.
- `LOGS_JSONL_PATH` (`logs/interactions.jsonl`) is relative to CWD — always launch from the project root.
- `duckdb_executor.py` opens DuckDB in **read-only mode**; any write attempt raises an error at the DB level.
- The RAG index (`qdrant_storage/`) is a local embedded Qdrant collection built by running `src/rag/ingestion.py` directly (`ingest_corpus()`); it is not rebuilt automatically when `corpus/` changes. Point IDs are deterministic hashes of `filename_chunkindex`, so re-ingestion is idempotent.

## Database Schema

The DuckDB database follows a star schema:
- **Dimensions**: `dim__assures`, `dim__contrats`, `dim__entreprises`, `dim__beneficiaires`
- **Facts**: `fct__dossiers`, `fct__paiements`, `fct__cotisations`, `fct__ressources`, `fct__contrats_entreprises`

Column descriptions come from the dbt manifest. `src/structured/schema_loader.py` is the single source of truth for schema context injected into Claude.

## Evaluation Framework

`evals/eval_set.yml` contains questions with `reference_sql` and a `compare` mode, evaluated against the SQL pipeline only (`agent_main`, not the orchestrator):
- `scalar` — single cell, exact value match (float tolerance via `math.isclose`)
- `named_scalar` — scalar value searched in any column of the agent result
- `row_count` — same number of rows
- `key_set` — same set of keys (order-insensitive, used for top_n)
- `exact_sorted` — exact shape, values and order
- `skip` — rag / hors_scope, no SQL evaluation

After a full run, `evals/reports/latest.json` is updated with `score_pct`, `passed`, `evaluated`, `date` — this is what the Streamlit sidebar reads. **`latest.json` is only written on full runs; `--ids` filtered runs skip it.**

Run evals after significant changes to `src/structured/sql_agent.py`, `src/structured/schema_loader.py`, or `src/prompts/system_prompt.md`.

`evals/rag_questions_draft.yml` is a draft question bank for the RAG pipeline; there is no runner wired up for it yet.

## Tests

`tests/conftest.py` sets dummy env vars (`os.environ.setdefault(...)`) **before pytest collects any test**. This is required because `src/config.py` calls `_require_env()` at module import time — standard `monkeypatch` fixtures arrive too late. Any new test module that imports from `src` relies on this; do not remove or defer `conftest.py`.

## Git / Commits

Un commit = une intention. Ne jamais regrouper des changements sans lien dans un seul commit.

Exemples de bons découpages :
- Nouvelle fonctionnalité agent (nouveau module Python) → 1 commit
- Modification du system prompt → 1 commit
- Correction sur un module existant → 1 commit
- Refacto Python → 1 commit

Format des messages : `type(scope): description courte`
Types courants : `feat`, `fix`, `refactor`, `docs`, `chore`

## Code Style

```bash
uv run ruff format src/ tests/ evals/   # formatage (remplace black + isort)
uv run ruff check src/ tests/ evals/    # lint
uv run mypy src/                        # type checking
```

## Conventions de commentaires

Ne commenter que le WHY non-obvious. Trois catégories :

- `# Guard - <raison>` — précondition vérifiée avant d'entrer dans la logique, échoue tôt
- `# Catch-all - <raison>` — intercepte des exceptions pour les normaliser vers un type unifié
- `# <raison>` — pour une contrainte cachée, un contournement, un invariant subtil

Ne jamais expliquer le WHAT (les noms de variables le font déjà). Pas de blocs multi-lignes.

Chaque module, classe et fonction doit avoir un docstring d'une ligne (convention du projet).

Toujours laisser une ligne vide après une docstring, avant le premier statement :

```python
def foo():
    """Fait quelque chose."""

    x = 1
```
