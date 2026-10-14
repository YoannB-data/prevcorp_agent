# Revue eval-reviewer : evals/rag/eval_set.yml (v3, HEAD)

Les 25 questions ont été relues contre `data/corpus/src/`, avec les règles de matching de `forme_presente` (valeur + unité pour les formes chiffrées, mot entier pour les formes textuelles). Les `formes` des points `verif: juge` ne sont pas comparées par `scorers.py` : « critère trop lâche » n'est donc retenu que pour les points déterministes.

| id | verdict | défaut | correction proposée |
|---|---|---|---|
| RC01 | à supprimer | non discriminante | 90 jours est la valeur dominante du corpus (FAQ, C83792, C73736, notice Agriculture). Un mauvais retrieval ou une réponse devinée passe. La question double RC07/O2. La supprimer. |
| RC02 | à corriger | critère trop lâche | Valeurs confirmées (Résumé C87656 : carence de 3 mois, franchise de 90 jours). O0 est déterministe (`"3 mois"`, valeur + unité). Il matche aussi l'ancienneté de 3 mois (Règlement art. 1.1, notices art. 1.1), donc une mauvaise réponse passe. Passer O0 en `verif: juge`, ou exiger un contexte textuel (`"carence de 3 mois"`). |
| RC03 | OK | aucun | Notice Santé : concubin sous condition de résidence commune. Clause du Règlement sans concubin. Le concubin n'apparaît que dans l'Annexe I, comme le dit `corpus_a_contenir`. Points en juge, donc les `formes` sont sans effet. |
| RC04 | OK | aucun | Aucune occurrence de « rapatri » ni de « à l'étranger » dans le corpus. Le piège de la section Assistance du Résumé C39949 est réel. |
| RC05 | à corriger | autre | Valeurs confirmées (Résumé C39949 : 60 jours ; notice Agriculture art. 14 : 90 jours). « Le Résumé, propre au contrat, prime » n'est écrit nulle part. Le préambule du Règlement dit seulement que les dispositions particulières figurent dans la notice ou le résumé. Retirer cette phrase de `reponse_attendue` ou la reformuler en « le Résumé précise le contrat ». |
| RC06 | OK | aucun | C39949 : 35/35/25, 45/45/35, 70/70/55 confirmés. Points en juge. |
| RC07 | OK | aucun | C87656 : 82 % (A), 78 % (B), franchise de 90 jours confirmés. |
| RC08 | OK | aucun | Valeurs confirmées pour C83792 : 140/115, 160/135, +28/+18, obsèques 1 900 €. Les `formes` numériques sont comparées par valeur + unité et « 1 900 € » se parse correctement. Pas de collision (« 28 % » ne matche pas « 128 % »). |
| RC09 | à corriger | ambiguë | Valeurs confirmées (5,5 / 8 / 11 %, 26e anniversaire). La question est un oui/non (« est-elle prévue ? ») alors que les points exigent les taux. Reformuler : « Quels sont les taux de la rente éducation du contrat C83792 ? ». « 8 % » est comparé par valeur, donc sans collision avec 18 % ou 78 %. |
| RC10 | à corriger | ambiguë | Valeurs confirmées (rente de conjoint 15 %, obsèques 2 500 €). « Disponibles » peut englober les 6 options de l'art. 16 du Règlement, alors que `reponse_attendue` parle de garanties souscrites. Reformuler : « Quelles garanties optionnelles sont souscrites sur C87656 ? ». |
| RC11 | à corriger | ambiguë | Notice Métallurgie : franchise continue, « aucune dérogation » confirmés. La prémisse « régime par défaut du Règlement » est fausse : l'art. 14 du Règlement décrit deux modalités sans défaut. Reformuler : « Quelle modalité de franchise s'applique et la CCN y déroge-t-elle ? ». Ajouter RESUME_C73736 (franchise continue) aux sources acceptables. Le piège du distracteur « discontinue » est bien couvert par I0. |
| RC12 | OK | aucun | C73736, 2e catégorie, tranche B : 50 %. |
| RC13 | à corriger | ambiguë | Résumé C73736 (aucune désignation notifiée) et notice Métallurgie (clause type de plein droit) confirmés. La parenthèse de la question « (conjoint puis enfants puis héritiers) » est celle de la notice Transport, tronquée. La réponse attendue inclut parents et autres ascendants. Corriger la parenthèse en « conjoint ou partenaire de PACS, enfants, parents, autres ascendants, héritiers », ou la retirer. |
| RC14 | OK | aucun | Annexe I du Règlement, ligne concubin : « attestation de vie commune ou, à défaut, deux justificatifs de domicile commun de plus de deux ans ». |
| RC15 | OK | aucun | FAQ : 90 jours, jours calendaires, premier jour. |
| RC16 | OK | aucun | FAQ confirmée : la franchise démarre au premier jour malgré le jour de carence. Points en juge. |
| RC17 | OK | aucun | Pas de rente de conjoint dans le Résumé C73736 (le résumé ne donne qu'une cotisation globale). La notice et son distracteur la citent à l'art. 16 : piège valide. |
| RC18 | OK | aucun | C20077 : 120 % (A et B) confirmé. |
| RC19 | à corriger | autre | Valeurs confirmées (25 %, sans limitation de rang). Le Résumé C20077 contient à lui seul le principe et le taux. La notice Transport art. 13 renvoie au résumé pour le taux. Le type « croisement » n'est donc pas justifié. Reclasser en `fait_simple` avec RESUME_C20077, ou poser une question qui exige vraiment la notice. |
| RC20 | à corriger | non discriminante | Règlement art. 15 (base 50 % en 1re catégorie) et Résumé C20077 (50 %) confirmés. La réponse égale le taux de base, et la question propose deux options. La notice Transport ne traite pas l'invalidité, donc la « dérogation CCN » n'existe pas. Interroger la 2e catégorie (75 % sur C20077 contre 100 % de base), où l'écart est réel. |
| RC21 | à corriger | non discriminante | FAQ et Règlement art. 15 confirment la réponse. Les 3 catégories d'invalidité sont une connaissance générale de la Sécurité sociale, donc répondables sans corpus. Remplacer par une question propre au contrat, ou supprimer. Si conservée, ajouter REGLEMENT_prevcorp aux sources acceptables. |
| RC22 | à corriger | non discriminante | Valeurs confirmées (Règlement art. 10 : 2 ans ; notice Transport art. 10 : 5 ans pour l'incapacité). La question donne les deux options, soit 50 % de chance. O1 et I0 ont les mêmes `formes` (`"2 ans"`), mais ils sont en juge, donc sans effet. Poser la question ouverte (« Quel est le délai de prescription pour une action en incapacité sur C20077 ? »). |
| RC23 | à corriger | ambiguë | FAQ (48 heures, 8 jours, trois derniers mois) et Résumé C20077 (78 % en A, 72 % en B) confirmés. « Trois » est converti en 3 par la normalisation, donc `"3 derniers mois"` matche. Mais l'Annexe I de la notice Transport et celle du Règlement disent « douze derniers mois » pour l'ITT. Un système qui suit la notice échoue. Ajouter NOTICE_CCN_transport_routier aux sources. Préciser « selon la FAQ », ou ajouter un point jugé sur le conflit. |
| RC24 | à corriger | ambiguë | Notice Santé (concubin) et Résumé C87656 (180 % pour célibataire/veuf/divorcé, +25 % par enfant) confirmés. La formulation « (ex. C87656) » ne fige pas le contrat. La situation de famille de l'assuré n'est pas précisée. Reformuler : « Sur le contrat C87656, quel capital perçoit le concubin d'un assuré célibataire sans enfant à charge ? ». |
| RC25 | OK | aucun | Notice Transport : clause type (conjoint, enfants, héritiers) et Annexe II (concubin non reconnu) confirmées. Le piège du Règlement (parents, ascendants) est valide et couvert par I0. |

## Décompte

Par verdict :

| Verdict | Nombre | Questions |
|---|---|---|
| OK | 12 | RC03, RC04, RC06, RC07, RC08, RC12, RC14, RC15, RC16, RC17, RC18, RC25 |
| à corriger | 12 | RC02, RC05, RC09, RC10, RC11, RC13, RC19, RC20, RC21, RC22, RC23, RC24 |
| à supprimer | 1 | RC01 |
| Total | 25 | |

Par type de défaut, pour les 13 questions non OK :

| Défaut | Nombre | Questions |
|---|---|---|
| critère trop lâche | 1 | RC02 |
| ambiguë | 6 | RC09, RC10, RC11, RC13, RC23, RC24 |
| non discriminante | 4 | RC01, RC20, RC21, RC22 |
| autre | 2 | RC05, RC19 |
| réponse fausse | 0 | aucune |
