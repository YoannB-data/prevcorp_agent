# Changelog des jeux de questions RAG

Le hash du YAML (nom des rapports, champ « Hash du YAML ») est le sha256 des **octets** du fichier, tronqué à 12 caractères (`hash_yaml` dans `src/rag/evaluation/report.py`). Toute modification du YAML, commentaires d'en-tête compris, change le hash : l'historique des versions est donc tenu ici et non dans les YAML.

| Version | Fichier | Hash |
|---------|---------|------|
| v1 | `rag_questions_v1_25.yml` (supprimé du dépôt, voir Réorganisation) | `ae7aed3dcc6a` |
| v2 | `rag_questions_v2_25.yml`, devenu `evals/rag/eval_set.yml` | `ddfd3583dae4` |
| v3 | `evals/rag/eval_set.yml` (jamais rejoué) | `f12821773e6c` |
| v4 | `evals/rag/eval_set.yml` | `938200a6916b` |

## v4 (2026-10-14)

23 questions (RC01 et RC21 supprimées, ids non renumérotés). Motif : revue complète des 25 questions par le subagent `eval-reviewer` (`evals/rag/reviews/review_v3.md`). Cumule les corrections v3 (RC02 à RC05), jamais rejouées seules.

- RC01 et RC21 supprimées : non discriminantes (valeur dominante du corpus ; connaissance générale de la Sécurité sociale).
- RC02 : O0 en `verif: juge` (« 3 mois » matche aussi l'ancienneté de 3 mois).
- RC05 : retrait de « Le Résumé, propre au contrat, prime » (absent des sources).
- RC09, RC10, RC13, RC22, RC24 : questions reformulées (ambiguïté ou choix binaire). RC24 : point O2 (majoration par enfant) retiré, la question vise un assuré sans enfant.
- RC11 : prémisse « régime par défaut du Règlement » retirée (l'art. 14 décrit deux modalités sans défaut). `sources_attendues` inchangées : R exige toutes les sources attendues, y ajouter le Résumé durcirait le retrieval.
- RC19 : `croisement` → `fait_simple`, source `RESUME_C20077` seule ; point O2 retiré.
- RC20 : bascule sur la 2e catégorie (75 % sur C20077 contre 100 % de base, art. 15).
- RC23 : « Selon la FAQ, » ajouté à la question.

Run de référence : `rag_20261014_111113_prefix_938200a6916b.md` (prefix, k=5) : R 15/21, E 19/23, I 22/23. Baseline précédente comparable : le run prefix `ddfd3583dae4` (v2, R 16/23, E 18/25, I 23/25), faute de run v3. Verdicts qui changent : RC11 (E KO→OK), RC19 (R KO→OK), RC22 (E KO→OK), plus la disparition de RC01 et RC21. RC11, RC19 et RC22 ont été reformulées : leur changement vient de la spécification, pas du système.

## v3 (2026-10-13)

Motif : revue de RC01 à RC05 par le subagent `eval-reviewer` (RC01 et RC02 PASS, RC03, RC04 et RC05 À REVOIR). Les 20 autres questions (RC06 à RC25) sont inchangées.

- RC02 : ajout de `points_interdits` I0 (confusion avec le jour de carence de la Sécurité sociale ou la franchise de 90 jours, `verif: juge`).
- RC03 : la `reponse_attendue` affirmait que le Règlement ne mentionne pas le concubin, ce qui est inexact (il figure dans le tableau des justificatifs, l. 153). Reformulée : la clause bénéficiaire type du Règlement ne le liste pas. O0 : formes `["concubin", "résidence commune"]`. O1 : forme `["pacte civil de solidarité"]` au lieu de `["conjoint"]`. `corpus_a_contenir` mis à jour.
- RC04 : O0 : formes `["ne trouve pas", "aucune mention", "pas d'information"]` au lieu de la phrase exacte. I0 : texte étendu à l'inférence depuis la section Assistance du Résumé, formes `["rapatriement", "assistance"]`.
- RC05 : `reponse_attendue` précise que le Résumé, propre au contrat, prime. Ajout de `points_interdits` I0 (conclut à l'absence d'écart). Les formes de O2 sont conservées : le contrôle de retrieval exige qu'une forme de chaque point obligatoire figure dans un chunk de la source attendue, donc des formes de réponse comme « écart » le feraient échouer.
- RC01 : inchangée (`chiffre_precis` interdit les points `juge`, donc pas d'interdit supplémentaire).

**Les baselines v2 (`ddfd3583dae4`) ne sont plus comparables à v3 sur RC02 à RC05** : le changement de score vient de la spécification, pas du système. Aucun run n'a été lancé sur v3 : il n'y a pas encore de baseline v3.

## Réorganisation (2026-10-13)

Déplacements sans changement de contenu : les octets des YAML sont identiques, donc les hashes aussi.

- `evals/rag_questions_v2_25.yml` → `evals/rag/eval_set.yml` (hash `ddfd3583dae4`). C'est désormais le jeu par défaut de `evals/rag/run_evals.py` et de `evals/rag/run_faithfulness.py`, qui pointaient sur v1.
- `evals/rag_questions_v1_25.yml` est supprimé du working tree. Son historique reste dans git (`git log --follow -- evals/rag_questions_v1_25.yml`) ; les baselines au hash `ae7aed3dcc6a` s'y rattachent.
- Baselines RAG : `evals/reports/rag/baselines/` → `evals/rag/reports/baselines/`. Baseline SQL : `evals/reports/sql/baselines/` → `evals/sql/reports/baselines/`.
- Ce fichier : `evals/CHANGELOG.md` → `evals/rag/CHANGELOG.md`.

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

`evals/rag/reports/baselines/` ne contient que des runs complets sur un hash de ce CHANGELOG, plus le run k=20 signalé par son suffixe `_partial`. Les chiffres des posts renvoient à ces fichiers. Les autres rapports de `evals/rag/reports/` restent ignorés par git.

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
| `rag_20261014_111113_prefix_938200a6916b.md` | `938200a6916b` (v4) | prefix | 5 |

## Dette connue

Le hash est calculé sur les octets du fichier : les commentaires d'en-tête des YAML ne peuvent pas être modifiés sans changer le hash, donc sans invalider la correspondance avec les rapports existants.

Rapport SQL de référence : `evals/sql/reports/baselines/report_20260521_130635_legacy_no_header.md` (59/67, 88,1 %). Antérieur au format actuel : pas de modèle ni de hash du YAML dans l'en-tête, donc non rattachable à un état précis du jeu de questions.
