# PrevCorp Agent

Assistant IA qui répond en français aux questions d'un assureur prévoyance, en choisissant lui-même sa source :
**SQL** sur l'entrepôt de données (dbt + DuckDB) ou **recherche documentaire** (RAG) sur les conditions générales et notices.
Chaque réponse est traçable (SQL affiché, documents cités), et chaque composant est mesuré par des évaluations maison versionnées.

**[▶ Démo en ligne](https://prevcorp-agent.streamlit.app/)** : si l'app dort, cliquez pour la réveiller (environ 30 secondes).



https://github.com/user-attachments/assets/04a11951-8b5b-46ca-893c-ebbc7dbf819d



> Données et documents **100 % synthétiques**. La structure s'inspire de documents publics du secteur
> (notices d'information, tableaux de garanties, conventions collectives) ; le contenu est intégralement généré.
> Aucune donnée réelle d'assureur n'est utilisée.

## En bref

- **Agent SQL** : question en français → SQL généré par Claude à partir du schéma dbt et du semantic layer → exécution DuckDB en lecture seule → tableau + graphique. Auto-correction en cas d'erreur SQL (3 tentatives max).
- **RAG** : embeddings Voyage, index Qdrant, réponse citée. Évaluation qui **sépare l'échec de recherche de l'échec de génération**.
- **Routeur** : un appel Claude classe la question (`sql` ou `rag`), puis l'orchestrateur délègue au bon pipeline.
- **Évaluations** : 67 questions SQL, 23 questions RAG, 70 questions de routing, rapports versionnés dans `evals/*/reports/baselines/`.
- **Harnais Claude Code** : `CLAUDE.md`, skill, hook de qualité. Le repo contient aussi l'outillage agentique qui a servi à le construire.

## Évaluation

| Composant | Eval set | Score | Méthode |
|---|---|---|---|
| Agent SQL | 67 questions évaluées (+16 hors périmètre) | **89,6 %** | Moyenne de 3 runs (61, 60, 59 PASS), Sonnet 4.6 |
| RAG, retrieval | 21 questions | 16/21 | Les documents attendus sont-ils dans le top 5 ? Déterministe |
| RAG, bout en bout | 23 questions | 18,3/23 | Réponse jugée par LLM, moyenne de 3 runs |
| RAG, génération isolée | 23 questions | 21,7/23 | Même juge, avec les bons documents fournis, moyenne de 3 runs |
| Routing SQL / RAG | 70 questions | 71,4 % | 100 % sur les 50 mono-source, 0 % sur les 20 hybrides |

L'écart entre « génération isolée » et « bout en bout » mesure ce que coûte le retrieval : le modèle sait répondre
quand on lui fournit les bons documents, il échoue surtout quand il ne les trouve pas.
Le point faible identifié est le **croisement de deux documents** (retrieval 4/8).

### Limites assumées

- **SQL** : une partie des questions est validée sur le nombre de lignes. Ce critère peut accepter une réponse
  fausse qui renvoie le bon nombre de lignes : le score est probablement légèrement surévalué.
- **RAG** : un seul juge LLM (Sonnet 4.6), avec un bruit observé de ±3/23 d'un run à l'autre.
- **Questions hybrides** : le routeur est binaire (SQL ou RAG). Les questions qui demandent à la fois des données
  et des documents ne sont pas traitées, d'où le 0/20, par construction.
- **Choix du modèle** : Sonnet 5.5 a été testé sur l'eval SQL et a fait moins bien (85,3 % sur 6 runs).
  Le projet reste sur Sonnet 4.6.
- **Coût** : la génération SQL injecte le schéma complet (environ 6 300 tokens par appel), contre environ 170 pour
  le routage. C'est le premier poste d'optimisation. La démo publique tourne sur une clé dédiée, plafonnée.
- **Observabilité** : seul le pipeline SQL est journalisé (JSONL). Le pipeline RAG ne l'est pas encore.

## Architecture

```
Question (Streamlit)
       ↓
Routeur (appel Claude) → sql | rag
       ↓
Orchestrateur
   ├─ Pipeline SQL
   │    Few-shot (mots-clés) + schéma dbt + semantic layer
   │    → Claude génère le SQL → DuckDB (lecture seule)
   │    └─ erreur SQL → retry avec le message d'erreur (3 tentatives max)
   │    → DataFrame + graphique Plotly
   │    → log JSONL (tokens, latence, coût)
   │
   └─ Pipeline RAG
        Embedding de la question (Voyage)
        → top-k chunks (Qdrant local, filtre optionnel par type de document)
        → Claude répond en citant ses sources
```

## Harnais de développement (Claude Code)

Le repo embarque l'outillage agentique utilisé pour le construire :

- `CLAUDE.md` : commandes, conventions et pièges connus, chargés à chaque session.
- `.claude/skills/corpus-generator/` : génère un document du corpus RAG depuis une spec.
- `.claude/settings.json` : hook `PostToolUse` qui lance ruff (tous les `.py`) et mypy (`src/` uniquement) sur
  chaque fichier écrit ou édité par l'agent. En cas d'erreur, le hook sort en exit 2 et l'agent reçoit le
  diagnostic pour se corriger.

Limite connue : mypy ne vérifie que le fichier édité, pas ses appelants. Le hook sert de feedback rapide ;
la vérification complète reste celle de la CI.

## Lancer en local

Prérequis : Python 3.12, [uv](https://docs.astral.sh/uv/), clés API Anthropic et Voyage.

```bash
git clone https://github.com/YoannB-data/prevcorp_agent.git
cd prevcorp_agent
uv sync --all-groups
uv run pre-commit install
cp .env.example .env    # puis renseigner ANTHROPIC_API_KEY et VOYAGE_API_KEY
uv run streamlit run src/app.py
```

Les données de démo (`data/demo/` : base DuckDB, manifests dbt, index Qdrant) sont versionnées et
`.env.example` pointe déjà dessus : l'app fonctionne dès le clone, sans projet dbt.

Lancer toutes les commandes depuis la racine du projet : les chemins sont relatifs au répertoire courant.

Variables optionnelles :
- `AGENT_THINKING_MODE` : mode de raisonnement de l'agent (clé de `MODEL_PARAMS` dans `src/config.py`, défaut
  `default`). Une valeur inconnue pour le modèle configuré fait échouer l'app au démarrage.
- `EDGE_BINARY` : chemin complet de l'exécutable Edge, utile uniquement sur une machine sans GTK3 pour le rendu
  HTML → PDF du corpus.

### API Python

```python
from src.orchestrator import orchestrator_main

result = orchestrator_main("Combien de dossiers ouverts en 2024 ?")
```

Pipeline SQL seul : `from src.structured.sql_agent import agent_main`, puis `sql, df = agent_main(question)`.

## Relancer les évaluations

```bash
# SQL
uv run python evals/sql/run_evals.py                 # suite complète
uv run python evals/sql/run_evals.py --ids Q012 Q034 # questions spécifiques

# RAG : retrieval (R), bout en bout (E), génération isolée (I)
uv run python evals/rag/run_evals.py [--k 5] [--variant header] [--judge-model MODELE] [--ids RC01 ...]
uv run python evals/rag/run_faithfulness.py [--k 5] [--judge-model MODELE] [--ids RC01 ...]

# Routeur
uv run python evals/routing/run_routing.py [--runs 3]
```

- Rapports horodatés dans `evals/{sql,rag,routing}/reports/`. Seuls les `baselines/` sont versionnés.
- `evals/reports/latest.json` est lu par la sidebar Streamlit (écrit uniquement sur un run SQL complet).
- `run_faithfulness.py` mesure, via un juge LLM, la part des affirmations de chaque réponse appuyées par les
  chunks récupérés.
- Les runners RAG refusent de tourner (code 2) si la collection Qdrant n'a pas été ingérée avec la variante
  `header`. Ne pas les lancer pendant que Streamlit tourne (verrou disque Qdrant). Les appels Voyage et
  Anthropic sont facturés.
- Historique des jeux de questions RAG et de leurs hashes : [evals/rag/CHANGELOG.md](evals/rag/CHANGELOG.md).

## Rafraîchir les données de la démo

`data/demo/` est un snapshot figé au moment du déploiement. Les données viennent du projet dbt
[prevcorp_dbt](https://github.com/YoannB-data/prevcorp_dbt) (génération du dataset synthétique et modélisation),
à cloner à côté de ce repo. Après une modification du projet dbt :

```powershell
# Fermer Streamlit et toute connexion DuckDB avant la copie (sinon fichier verrouillé)
# Prérequis : ~/.dbt/profiles.yml configuré (cf. README de prevcorp_dbt)
cd ..\prevcorp_dbt\prevcorp_dbt
uv run dbt build
Copy-Item dev.duckdb, target\manifest.json, target\semantic_manifest.json ..\..\prevcorp_agent\data\demo\ -Force
```

Après une modification du corpus (`data/corpus/src/`), relancer l'ingestion. Elle écrit directement dans
`data/demo/qdrant_storage/` :

```bash
uv run python -m src.rag.ingestion [--collection NOM] [--recreate]
```

## Structure

```
src/
  app.py               # Interface Streamlit
  router.py            # Classification sql / rag via Claude
  orchestrator.py      # Route puis délègue au pipeline SQL ou RAG
  config.py            # Paramètres (chemins, modèles par rôle, coûts), validés au démarrage
  llm.py               # Lecture des réponses de l'API (texte, tokens de raisonnement)
  logger.py            # Log JSONL des interactions (tokens, latence, coût)
  structured/          # Pipeline SQL
    sql_agent.py         # Appel Claude, retry, logging
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
    evaluation/          # Runner d'éval RAG (schéma du YAML, retrieval, scorers, juge, faithfulness, diagnostic, rapport)
  prompts/
    system_prompt.md     # Prompt système injecté dans chaque appel
    few_shot_bank.yml    # Banque d'exemples few-shot
evals/
  sql/                 # eval_set.yml (SQL de référence + mode de comparaison), run_evals.py, reports/
  rag/                 # eval_set.yml (23 questions, v4), run_evals.py, run_faithfulness.py, CHANGELOG.md, reports/
  routing/             # eval_set.yml (70 questions), run_routing.py, reports/
  reports/latest.json  # Score SQL lu par la sidebar Streamlit
data/
  demo/                # Snapshot de démo versionné : DuckDB, manifests dbt, stockage Qdrant
  corpus/src/          # Sources HTML du corpus, versionnées
  corpus/pdf/          # PDF du corpus (gitignorés, dérivés de src/)
scripts/               # dump_chunks.py (lecture des chunks Qdrant), diag_croisement.py (diagnostic retrieval)
logs/
  interactions.jsonl   # Historique des appels du pipeline SQL (succès et erreurs)
```

## Schéma de données

Modèle en étoile produit par le projet dbt [prevcorp_dbt](https://github.com/YoannB-data/prevcorp_dbt) :

| Type | Tables |
|------|--------|
| Dimensions | `dim__segments`, `dim__entreprises`, `dim__contrats`, `dim__assures`, `dim__beneficiaires` |
| Faits | `fct__dossiers`, `fct__paiements`, `fct__cotisations`, `fct__ressources`, `fct__contrats_entreprises` |

## Stack

- **LLM et IA** : Claude API via Anthropic SDK (Sonnet 4.6, modèles par rôle dans `src/config.py`), Voyage AI
  (`voyage-multilingual-2`), Qdrant (mode local embarqué)
- **Données** : dbt + DuckDB + MetricFlow, pandas
- **Interface** : Streamlit + Plotly
- **Corpus** : WeasyPrint (HTML → PDF, repli sur Edge headless sans GTK3), pdfplumber (extraction)
- **Qualité** : Pydantic, Ruff, mypy, pre-commit, GitHub Actions
