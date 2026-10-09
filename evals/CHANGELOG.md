# Changelog des jeux de questions RAG

Le hash du YAML (nom des rapports, champ « Hash du YAML ») est le sha256 des **octets** du fichier, tronqué à 12 caractères (`hash_yaml` dans `src/rag/evaluation/report.py`). Toute modification du YAML, commentaires d'en-tête compris, change le hash : l'historique des versions est donc tenu ici et non dans les YAML.

| Version | Fichier | Hash |
|---------|---------|------|
| v1 | `rag_questions_v1_25.yml` | `ae7aed3dcc6a` |
| v2 | `rag_questions_v2_25.yml` | `ddfd3583dae4` |

## v2 (2026-10-09)

Correction de spécification de 4 questions après les premiers résultats. Les questions RC02, RC06, RC07 et RC10 étaient typées `croisement` avec `sources_attendues: [REGLEMENT_prevcorp, RESUME_<contrat>]`, alors que la réponse attendue se trouve dans le seul Résumé du contrat.

- Type `croisement` → `fait_simple`.
- `sources_attendues` ramenées au seul Résumé : `[RESUME_C87656]` (RC02, RC07, RC10) ou `[RESUME_C39949]` (RC06).
- `corpus_a_contenir` : mention du Règlement retirée (RC02 : ligne retirée).

Les 21 autres questions sont inchangées. Le changement de score entre v1 et v2 sur ces 4 questions vient de la spécification, pas du système : ne pas comparer leurs résultats sans en tenir compte.

## v1 (2026-10-06)

Remplace v0 : `sources_attendues` en liste de `doc_id`, `contexte_isole` optionnel, `points_obligatoires` et `points_interdits` renseignés pour les 25 questions.

Note : le commit `5e2d1a2` (2026-10-09, O0 des questions `sans_reponse` réduit au seul refus) a modifié le texte de 2 points dans v1 après coup. Un rapport v1 produit avant ce commit ne correspond donc plus au hash `ae7aed3dcc6a` actuel.
