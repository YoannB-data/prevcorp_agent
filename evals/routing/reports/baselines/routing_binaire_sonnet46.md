# Rapport d'éval du routeur

- Modèle : `claude-sonnet-4-6`
- Commit : `4197a53`
- Runs : 1
- Date : 2026-10-16 14:28:58
- Questions : 70

## Accuracy globale

Moyenne 71.4% (min 71.4% – max 71.4%) sur 1 run(s).

## Seuils (meta)

| Métrique | Valeur | Seuil | Verdict |
|---|---|---|---|
| accuracy (moyenne) | 71.4% | 90% | KO |
| rappel hybride | 0.0% | 80% | KO |

## Rappel et précision par classe (runs cumulés)

| Classe | Rappel | Précision |
|---|---|---|
| hybride | 0.0% | n/a |
| sql | 100.0% | 58.1% |
| rag | 100.0% | 92.6% |

## Matrice de confusion (runs cumulés, lignes = attendu, colonnes = prédit)

| attendu \ prédit | sql | rag | hybride |
|---|---|---|---|
| sql | 25 | 0 | 0 |
| rag | 0 | 25 | 0 |
| hybride | 18 | 2 | 0 |

## Accuracy par forme (runs cumulés)

| Forme | Accuracy |
|---|---|
| simple | 100.0% |
| explicite | 0.0% |
| implicite | 0.0% |
| dependante | 0.0% |
| piege | 100.0% |

## Questions instables (0)

Aucune.

## Réponses hors sql/rag (0)

Aucune.

## Latence et coût

- Latence par question : moyenne 1.58 s, max 3.23 s. Mesurée par le runner autour de `route()` ; elle inclut la création du client Anthropic.
- Coût et tokens : non exposés par le routeur.

## Erreurs de routage (dernier run)

- RT-H01 [explicite] attendu hybride, prédit sql
- RT-H02 [dependante] attendu hybride, prédit sql
- RT-H03 [explicite] attendu hybride, prédit sql
- RT-H04 [explicite] attendu hybride, prédit sql
- RT-H05 [explicite] attendu hybride, prédit sql
- RT-H06 [dependante] attendu hybride, prédit rag
- RT-H07 [explicite] attendu hybride, prédit sql
- RT-H09 [explicite] attendu hybride, prédit sql
- RT-H10 [dependante] attendu hybride, prédit sql
- RT-H11 [explicite] attendu hybride, prédit sql
- RT-H12 [explicite] attendu hybride, prédit sql
- RT-H13 [explicite] attendu hybride, prédit sql
- RT-H14 [explicite] attendu hybride, prédit sql
- RT-H15 [explicite] attendu hybride, prédit sql
- RT-H16 [explicite] attendu hybride, prédit sql
- RT-H17 [implicite] attendu hybride, prédit rag
- RT-H18 [implicite] attendu hybride, prédit sql
- RT-H19 [implicite] attendu hybride, prédit sql
- RT-H20 [implicite] attendu hybride, prédit sql
- RT-H21 [dependante] attendu hybride, prédit sql
