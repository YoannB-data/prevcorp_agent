# Revue eval-reviewer : evals/rag/eval_set.yml

Les 25 questions de `evals/rag/eval_set.yml` ont été relues contre `data/corpus/src/` (5 résumés, Règlement, FAQ, 4 notices CCN, notice distracteur métallurgie). Toutes les valeurs de `reponse_attendue` sont exactes par rapport aux sources. Les défauts viennent des `formes`, de l'ambiguïté des questions et de la discrimination, pas des chiffres.

| id | verdict | défaut | correction proposée |
|---|---|---|---|
| RC01 | à supprimer | non discriminante | « 90 jours » est aussi la valeur de la FAQ, de C83792, de C73736 et de la notice Agriculture. Un mauvais retrieval passe donc. La question double RC07/O2. La supprimer. |
| RC02 | à corriger | critère trop lâche | O0 `"3 mois"` correspond aussi à l'ancienneté de 3 mois (Règlement art. 1.1, toutes les notices). Mettre `"carence de 3 mois"`. I0 (`"90 jours"`, `"jour de carence"`) pénalise une bonne réponse qui distingue carence et franchise. Reformuler : « affirme que la carence est de 90 jours ». |
| RC03 | à corriger | critère trop lâche | Valeurs confirmées (notice santé : concubin sous condition de résidence commune ; clause du Règlement sans concubin). O1 `"pacte civil de solidarité"` figure dans les deux clauses et ne prouve pas la comparaison. Vérifier le contraste en juge seul, ou exiger `"Règlement"` et `"ne liste pas"`. Note : l'Annexe I du Règlement cite le justificatif concubin, ce qui nuance « concubin absent du Règlement ». |
| RC04 | OK | aucun | Aucun « rapatriement » ni « étranger » dans le corpus. Le piège de la section Assistance du Résumé C39949 est réel. Réserve : I0 `"rapatriement"` apparaît dans un refus correct, d'où le juge obligatoire. |
| RC05 | à corriger | autre | Valeurs confirmées (Résumé C39949 : 60 jours ; notice Agriculture art. 14 : 90 jours). « Le Résumé, propre au contrat, prime » n'est écrit dans aucune source. Retirer cette phrase ou la citer. |
| RC06 | OK | aucun | Taux C39949 confirmés (35/25, 45/35, 70/55). Les `formes` ne portent que le premier nombre ; le juge couvre le reste. |
| RC07 | OK | aucun | 82 % (A), 78 % (B), franchise 90 jours dans le Résumé C87656. |
| RC08 | à corriger | ambiguë | Valeurs C83792 confirmées. « Quelles sont les garanties décès » couvre aussi la rente éducation, le double effet et le décès accidentel, hors points obligatoires. Préciser « capital décès toutes causes, majoration et obsèques ». Autre risque : le « 1 900 € » déterministe casse avec une espace insécable. |
| RC09 | à corriger | critère trop lâche | Valeurs confirmées (5,5 / 8 / 11 %, 26e anniversaire). O1 `"8 %"` est une sous-chaîne de « 18 % », « 28 % » et « 78 % ». C20077 a aussi 8 % pour 12-17 ans. Utiliser une regex avec borne (`(?<!\d)8 %`) et un interdit sur 7 %. |
| RC10 | à corriger | ambiguë | Valeurs confirmées (rente de conjoint 15 %, obsèques 2 500 €). « Disponibles » peut englober les 6 options de l'art. 16 du Règlement. La réponse attendue parle de garanties « souscrites ». Reformuler : « Quelles garanties optionnelles sont souscrites ? ». |
| RC11 | à corriger | ambiguë | La notice Métallurgie confirme « continue » et « aucune dérogation ». Le Règlement art. 14 ne définit aucun régime par défaut, il décrit deux modalités. La prémisse « régime par défaut du Règlement » est donc fausse. De plus, `"continue"` est une sous-chaîne de « discontinue ». Reformuler : « modalité retenue et écart éventuel à la CCN ». Ajouter RESUME_C73736 aux sources acceptables. |
| RC12 | à corriger | critère trop lâche | 50 % confirmé (C73736, 2e catégorie, tranche B). `"50 %"` est une sous-chaîne de « 150 % » et vaut aussi pour la 1re catégorie du Règlement. Utiliser une regex avec borne. |
| RC13 | à corriger | critère trop lâche | Confirmé : Résumé C73736 (aucune désignation personnalisée) et notice Métallurgie (clause type de plein droit). La question tronque la clause (« conjoint puis enfants puis héritiers ») et ses `formes` sont triviales : `"clause bénéficiaire type"` est dans la question, `"conjoint"` est générique. Ajouter un interdit sur le tableau d'exemple 60 %/40 %/100 % de la notice et des formes `"parents"`, `"autres ascendants"`. |
| RC14 | OK | aucun | Annexe I du Règlement, ligne concubin : confirmé. |
| RC15 | OK | aucun | FAQ : 90 jours, jours calendaires, premier jour. Confirmé. |
| RC16 | à corriger | critère trop lâche | FAQ confirmée. Les `formes` ne portent pas la polarité : « Oui, le jour de carence retarde… » contient `"jour de carence"` et `"premier jour"`. Ajouter un interdit « la franchise démarre après le jour de carence ». |
| RC17 | à corriger | critère trop lâche | Pas de rente de conjoint dans le Résumé C73736, et la notice et son distracteur la citent à l'art. 16 : piège valide. La forme de O0 est une phrase exacte, trop fragile. Prendre `["ne trouve pas","aucune information","pas souscrite"]`. |
| RC18 | OK | aucun | C20077 : 120 % (A et B). |
| RC19 | à corriger | autre | 25 % et « sans limitation de rang » sont confirmés (Résumé C20077 ; notice Transport art. 13). Le Résumé seul suffit à répondre, donc le « croisement » est artificiel. Reclasser en `fait_simple` avec RESUME_C20077, ou poser une question qui exige la notice. |
| RC20 | à corriger | non discriminante | Règlement art. 15 (base 50 % en 1re catégorie) et Résumé C20077 (50 %) : confirmés. La réponse égale le taux de base, donc un système qui ne lit que le Règlement passe. `"50 %"` est aussi sous-chaîne de « 150 % ». Interroger la 2e catégorie (75 % contre 100 % de base), où la dérogation est réelle. |
| RC21 | à corriger | non discriminante | FAQ et Règlement art. 15 confirment la réponse. Les 3 catégories d'invalidité sont une connaissance générale de la Sécurité sociale, donc répondables sans corpus. Remplacer par une question liée au contrat, ou supprimer. Ajouter REGLEMENT_prevcorp aux sources acceptables. |
| RC22 | à corriger | critère trop lâche | Règlement art. 10 (2 ans) et notice Transport art. 10 (5 ans pour l'incapacité) : confirmés. La question donne les deux options (50 % de chance). I0 et O1 ont les mêmes `formes` (`"2 ans"`). Poser la question ouverte et formuler I0 : « retient 2 ans pour C20077 ». |
| RC23 | à corriger | autre | FAQ confirmée (48 heures, 8 jours) et Résumé C20077 (78 % en A, 72 % en B). La FAQ écrit « trois derniers mois », donc la forme `"3 derniers mois"` est un faux négatif. L'Annexe I de la notice Transport dit « douze derniers mois » : conflit à arbitrer. Prendre `["3 derniers mois","trois derniers mois"]` et ajouter un interdit « 12 mois ». |
| RC24 | à corriger | ambiguë | Notice santé et Résumé C87656 confirmés : 180 % pour célibataire/veuf/divorcé, +25 % par enfant. La question dit « ex. C87656 » (contrat non figé) et ne précise pas la situation de famille de l'assuré. Fixer le contrat et préciser « assuré célibataire sans enfant à charge ». |
| RC25 | OK | aucun | Notice Transport : clause type (conjoint, enfants, héritiers) et Annexe II (concubin non reconnu). Piège Règlement (parents, ascendants) valide. |

## Décompte

Par verdict :

| Verdict | Nombre |
|---|---|
| OK | 7 (RC04, RC06, RC07, RC14, RC15, RC18, RC25) |
| à corriger | 17 |
| à supprimer | 1 (RC01) |
| Total | 25 |

Par type de défaut, pour les 18 questions non OK :

| Défaut | Nombre | Questions |
|---|---|---|
| critère trop lâche | 8 | RC02, RC03, RC09, RC12, RC13, RC16, RC17, RC22 |
| ambiguë | 4 | RC08, RC10, RC11, RC24 |
| non discriminante | 3 | RC01, RC20, RC21 |
| autre | 3 | RC05, RC19, RC23 |
| réponse fausse | 0 | aucune |
