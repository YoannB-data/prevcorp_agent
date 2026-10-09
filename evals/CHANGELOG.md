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

Hashes de v1 :
- `66873617cdfb` : v1 avant correction de l'O0 de RC04 et RC17. Les rapports portant ce hash ne sont pas à utiliser.
- `ae7aed3dcc6a` : v1 corrigé, hash actuel du fichier. C'est celui des baselines du 8/10 et du 9/10.

La correction (O0 des questions `sans_reponse` réduit au seul refus, commit `5e2d1a2`) a été faite dans le working tree le 8/10 et commitée le 9/10.

## Format du rapport faithfulness

Format modifié le 9/10/2026 : le rapport liste désormais toutes les affirmations de chaque réponse avec leur verdict (`appuyée` / `NON appuyée`), et non plus seulement les NON appuyées. Le baseline antérieur `faithfulness_20261009_105818_prefix_ae7aed3dcc6a.md` n'a que la liste des NON appuyées : il n'est pas comparable ligne à ligne aux nouveaux rapports. Les runs filtrés par `--ids` portent le suffixe `_partial` et n'ont pas de moyennes.

## Rapports de référence

`evals/reports/rag/baselines/` ne contient que des runs complets sur un hash de ce CHANGELOG, plus le run k=20 signalé par son suffixe `_partial`. Les chiffres des posts renvoient à ces fichiers. Les autres rapports de `evals/reports/rag/` restent ignorés par git.

| Rapport | Hash | Variante | k |
|---------|------|----------|---|
| `rag_20261008_171336_none_ae7aed3dcc6a.md` | `ae7aed3dcc6a` (v1) | none | 5 |
| `rag_20261008_172051_prefix_ae7aed3dcc6a.md` | `ae7aed3dcc6a` (v1) | prefix | 5 |
| `rag_20261008_173416_prefix_ae7aed3dcc6a_k20_partial.md` | `ae7aed3dcc6a` (v1) | prefix | 20 (partiel) |
| `rag_20261009_101400_prefix_article_ae7aed3dcc6a.md` | `ae7aed3dcc6a` (v1) | prefix_article | 5 |
| `faithfulness_20261009_105818_prefix_ae7aed3dcc6a.md` | `ae7aed3dcc6a` (v1) | prefix | 5 |
| `rag_20261009_112048_prefix_ddfd3583dae4.md` | `ddfd3583dae4` (v2) | prefix | 5 |
| `faithfulness_20261009_140338_prefix_ddfd3583dae4_partial.md` | `ddfd3583dae4` (v2) | prefix | 5 (partiel : RC17, RC20, RC24, RC25) |
| `rag_20261009_113428_none_ddfd3583dae4.md` | `ddfd3583dae4` (v2) | none | 5 |

## Dette connue

Le hash est calculé sur les octets du fichier : les commentaires d'en-tête des YAML ne peuvent pas être modifiés sans changer le hash, donc sans invalider la correspondance avec les rapports existants.

Rapport SQL de référence : `evals/reports/sql/baselines/report_20260521_130635_legacy_no_header.md` (59/67, 88,1 %). Antérieur au format actuel : pas de modèle ni de hash du YAML dans l'en-tête, donc non rattachable à un état précis du jeu de questions.
