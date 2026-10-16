# Revue de faisabilité : questions hybrides RT-H01 à RT-H10 (v0)

Date : 2026-10-15. Branche : `feat/routing-eval-set`. Aucune question n'a été réécrite dans l'eval set : les reformulations ci-dessous sont des propositions.

Sources vérifiées :
- **Données** : `dev.duckdb` (dbt `prevcorp_dbt`), modèles `marts/`, ouverts en lecture seule.
- **Corpus** : `data/corpus/src/*.html`. Le dossier `corpus_src/` du brief n'existe pas, c'est ce chemin.
- **Revue de discriminance** : subagent `eval-reviewer`.

## Écarts entre le brouillon et le schéma réel

Ils concernent toutes les questions :

| Brouillon | Réel |
|---|---|
| `fct_claims` | `fct__dossiers` (colonne `risque`, valeurs : Décès, Incapacité, Invalidité, Rente éducation, Rente viagère) |
| `dim_contracts` | `dim__contrats` (`contrat_numero`, `contrat_type`, `segment_nom`, `debut_date`, `est_en_cours`) |
| `fct_premiums` | `fct__cotisations` (`cotisation_montant`, `encaissement_date`, `echeance_date`) |
| type « ITT » | `risque = 'Incapacité'` |
| segment sur les paiements | absent de `fct__paiements` : jointure sur `fct__dossiers` nécessaire |
| statut « en attente pièces » | **n'existe pas** (`etat_motif` : REPRISE TRAVAIL, SANS SUITE, DECEDE, RETRAITE, NULL si en cours) |
| assurés par contrat | **pas de `contrat_id` dans `dim__assures`** : on ne peut compter les assurés d'un contrat que via leurs dossiers |
| garanties/options souscrites | aucune colonne en base : cette information est seulement dans les Résumés |

Autres contraintes des données :
- Les données s'arrêtent au 31/12/2025. `duree_dossier_jours` est calculée jusqu'à cette date pour les dossiers en cours, et à partir de `creation_date`, pas de `fait_generateur_date`.
- Dernier contrat souscrit : 2023-12-21.
- Dernier encaissement de cotisation : 2025-10-21.
- 5 contrats seulement ont un Résumé : C20077 (Transport, non cadre), C39949 (Agriculture, non cadre), C73736 (Métallurgie, cadre), C83792 (Enseignement privé, ensemble du personnel), C87656 (Santé, cadre). Les 5 sont actifs.
- 4 segments sur 10 seulement ont une Notice : Agriculture, Métallurgie (vraie + distracteur), Santé et action sociale, Transport routier.

## Tableau de synthèse

| id | SQL faisable | Résultat SQL | Fait RAG trouvé | Dépendance | Discriminante | Reco |
|---|---|---|---|---|---|---|
| RT-H01 | oui | **0** dossier Incapacité en 2025 sur C39949 (3 au total : fait générateur 2022, 2023, 2024) | RESUME_C39949, Incapacité temporaire de travail : « À l'issue de la franchise de 60 jours » ; NOTICE_CCN_agriculture : « fixée à 90 jours » | aucune (2 parties indépendantes) | PASS (reviewer), mais SQL nul | **modifier** |
| RT-H02 | oui | 1 arrêt en cours (fait générateur 2023-10-08), au-delà de 60 j **et** de 90 j | idem RT-H01 (60 j vs 90 j) | SQL ← RAG (seuil) | À REVOIR : réponse identique avec 60 ou 90 j | **garder (routing seul)** |
| RT-H03 | partiel : « non réglés » n'a pas de colonne | 54 dossiers Incapacité en cours avec fait générateur > 2 ans (53 via `duree_dossier_jours`) ; 0 > 5 ans | NOTICE_CCN_transport_routier, Article 10 : « prescription applicable […] incapacité de travail est porté à 5 ans » | aucune pour compter ; la conclusion « dans le délai » croise les deux | À REVOIR : « non réglés » ambigu | **modifier** |
| RT-H04 | non sur 2025 | **0** cotisation encaissée en 2025 sur C73736 (dernière année : 2024, 44 505,50 €) | RESUME_C73736 : aucune section Rente de conjoint (absence vérifiée, cf. RC17). Piège : NOTICE_CCN_metallurgie art. 16, rente de conjoint « en complément des garanties de base » | aucune | À REVOIR : le SQL n'influe pas sur la réponse | **modifier** |
| RT-H05 | oui | 1 146 076,50 € brut / 1 085 616,14 € net, 12 paiements, 11 contrats | NOTICE_CCN_metallurgie, Clause bénéficiaire type : « s'applique de plein droit » à défaut de désignation ; distracteur : « clause bénéficiaire personnalisée […] se substitue à la clause type » | aucune ; la clause n'est pas en base, par dossier | À REVOIR : lien montant ↔ clause présupposé | **modifier** |
| RT-H06 | oui | Transport 16, Hôtellerie 15, Santé 13… (par fait générateur 2025). **Par `creation_date` : Hôtellerie 18, Transport 17** | NOTICE_CCN_sante_action_sociale, Clause bénéficiaire type : « ou à son concubin sous condition de résidence commune » ; NOTICE_CCN_transport_routier, Annexe II : « ne reconnaissant pas la qualité de concubin » | aucune | À REVOIR : 3 ambiguïtés | **modifier** |
| RT-H07 | oui | 47 contrats Enseignement privé actifs | RESUME_C83792 seulement (garanties décès, cf. RC08) ; pas de Notice Enseignement privé | aucune | À REVOIR : RAG ne couvre que 1 contrat sur 47 | **modifier** |
| RT-H08 | **non** | 0 contrat souscrit en 2025 (max `debut_date` = 2023-12-21) | « carence » **absent du Règlement**. Présent seulement dans RESUME_C87656 (« délai de carence de 3 mois »), la Notice Santé et la FAQ (jour de carence SS) | — | À REVOIR : prémisse fausse, question causale | **rejeter** |
| RT-H09 | **non** | aucun statut « en attente pièces » | REGLEMENT_prevcorp, Annexe I, colonne DÉCÈS-IAD (acte de décès, livret de famille, justificatif concubin, RIB, bulletins) | — | À REVOIR : seule la moitié RAG est répondable | **modifier** |
| RT-H10 | partiel | CADRE : 179 contrats en base, 2 documentés. Assurés **ayant un dossier** : C87656 = 13, C73736 = 14 | Obsèques présentes dans **les 5 Résumés**. Option souscrite seulement sur RESUME_C87656 (« Garanties optionnelles souscrites », 2 500 €) ; garantie de base ailleurs (C73736 : 2 200 €) | SQL ← RAG (liste de contrats) | À REVOIR : prémisse « option » fausse pour 4 contrats sur 5 | **modifier** |

Bilan : 1 à garder (RT-H02, pour le routing seul), 8 à modifier, 1 à rejeter (RT-H08).

## Détail par question

### RT-H01 : modifier

- **SQL** :
  ```sql
  select count(*) from fct__dossiers
  where contrat_numero = 'C39949' and risque = 'Incapacité'
    and year(fait_generateur_date) = 2025;  -- 0 (même résultat avec creation_date)
  ```
  Le résultat est nul. Le reviewer note qu'un « 0 » deviné serait juste.
- **RAG** : conforme au brouillon (60 j dans le Résumé, 90 j dans la Notice Agriculture). Autre source de 90 j non prévue comme distracteur : la FAQ, « franchise de 90 jours » pour un arrêt maladie ordinaire.
- **Reformulation** : « Combien de dossiers d'arrêt de travail ont été ouverts sur le contrat C39949 depuis 2022, et quelle franchise ITT prévoit son Résumé des garanties ? » → 3 / 60 jours.

### RT-H02 : garder (routing seul)

- **SQL** :
  ```sql
  select count(*) from fct__dossiers
  where contrat_numero = 'C39949' and risque = 'Incapacité' and est_en_cours
    and date '2025-12-31' - fait_generateur_date > 60;  -- 1 (idem avec > 90)
  ```
- **Limite** : la dépendance SQL ← RAG est réelle, mais le piège 60/90 n'est pas testable sur ces données. C39949 n'a que 3 dossiers Incapacité, tous au-delà de 90 j, et c'est le seul Résumé à 60 j. Le label `hybride` reste juste. En end-to-end, un agent qui prendrait 90 j obtiendrait la même réponse.
- **Ancrage de date** : « en cours » est implicitement au 31/12/2025, alors qu'on est le 15/10/2026. À préciser si la question sert aussi en end-to-end.

### RT-H03 : modifier

- **SQL** : 54 dossiers.
  ```sql
  select count(*) from fct__dossiers
  where segment_nom = 'Transport routier' and risque = 'Incapacité' and est_en_cours
    and date '2025-12-31' - fait_generateur_date > 730;  -- 54
  ```
- **Problèmes** :
  - « Non réglés » n'a pas de colonne. `est_en_cours` signifie « prestations en cours de versement », et les 54 dossiers ont des paiements.
  - La prescription porte sur une *action* et court « à compter de l'événement qui lui donne naissance ». Appliquée à un dossier en cours d'indemnisation, la question est juridiquement floue.
  - Aucun dossier n'a plus de 5 ans : la réponse « oui, tous » est triviale une fois les 5 ans connus.
- **Reformulation** : « Sur le Transport routier, combien de dossiers incapacité encore en cours ont un fait générateur de plus de 2 ans au 31/12/2025, et quel délai de prescription s'applique à la garantie incapacité dans cette convention ? » → 54 / 5 ans. Piège : 2 ans dans le Règlement et les autres Notices.

### RT-H04 : modifier

- **SQL** : C73736 n'a aucune cotisation encaissée en 2025 (2022 : 40 745,97 € ; 2023 : 54 542,79 € ; 2024 : 44 505,50 €). En 2025, seuls 264 contrats sur 483 ont un encaissement.
- **RAG** : absence confirmée. Le piège de la Notice Métallurgie (art. 16) est bien présent.
- **Problème** : « des cotisations couvrent une garantie » est mal posé. La réponse vient entièrement du RAG.
- **Reformulation (explicite)** : « Quel montant de cotisations a été encaissé en 2024 sur le contrat C73736, et ce contrat prévoit-il une rente de conjoint ? » → 44 505,50 € / non.
- **Variante implicite**, si tu veux garder la forme : non vérifiable sans nouvelle formulation. Je ne vois pas de lien chiffré naturel entre un total de cotisations et une garantie absente.

### RT-H05 : modifier

- **SQL** :
  ```sql
  select sum(p.brut_montant), sum(p.net_montant)
  from fct__paiements p join fct__dossiers d using (dossier_id)
  where d.segment_nom = 'Métallurgie' and p.risque = 'Décès'
    and year(p.paiement_date) = 2025;  -- 1 146 076,50 / 1 085 616,14
  ```
  À trancher : brut ou net ? `risque = 'Décès'` couvre aussi d'éventuels capitaux obsèques ; la base ne distingue pas.
- **RAG** : la clause qui s'applique à un dossier donné est **non vérifiable**, car aucune donnée de désignation par dossier. Seule la règle par défaut est connue : clause type (vraie Notice, et C73736 « la clause bénéficiaire type du Règlement PrevCorp s'applique ») ; clause personnalisée imposée (distracteur).
- **Reformulation** : « Quel montant brut de capitaux décès a été versé en Métallurgie en 2025, et quelle clause bénéficiaire s'applique à défaut de désignation selon la Notice Métallurgie ? » → 1 146 076,50 € / clause type : conjoint ou partenaire de PACS, puis enfants, puis parents, puis ascendants, puis héritiers.

### RT-H06 : modifier

- **SQL** : le classement dépend de la date retenue.
  - Avec `fait_generateur_date` (recommandée par la doc dbt) : Transport routier 16, Hôtellerie 15, Santé 13.
  - Avec `creation_date` : Hôtellerie 18, Transport 17.
- **RAG** : le fait « Santé seule à l'autoriser » est **ambigu** :
  - Seule la clause *type* de la Notice Santé cite le concubin.
  - Toutes les Notices et le Règlement autorisent une clause personnalisée « bénéficiaires de votre choix ».
  - Le Règlement, Annexe I, exige un « justificatif de qualité de concubin » pour DÉCÈS-IAD.
  - 6 segments sur 10 n'ont pas de Notice, dont Hôtellerie (n° 2 ou n° 1 selon la date).
- **Reformulation** : « Quel segment a enregistré le plus de décès survenus en 2025, et la clause bénéficiaire type de sa Notice reconnaît-elle le concubin ? » → Transport routier (16) / non (clause type : conjoint, enfants, héritiers ; Annexe II l'exclut explicitement). Le mot « survenus » ancre la date sur le fait générateur.

### RT-H07 : modifier

- **SQL** : `count(*) from dim__contrats where segment_nom = 'Enseignement privé' and est_en_cours` → 47.
- **RAG** : seul RESUME_C83792 décrit des garanties décès Enseignement privé. Pour les 46 autres contrats, **non vérifiable**.
- **Reformulation** : « Combien de contrats Enseignement privé sont actifs, et quelles garanties décès prévoit le contrat C83792 ? » → 47 / table RC08. Recoupe RC08 : la moitié RAG est déjà couverte, ce qui est acceptable pour un eval de routing.

### RT-H08 : rejeter

- **SQL** : aucun contrat souscrit en 2025. Contrats par année de `debut_date` : 2010 à 2023 seulement.
- **RAG** : le Règlement ne contient pas « carence ». Le plus proche est l'article 1.1, « ancienneté d'au moins 3 mois » (une condition d'adhésion, pas une carence). Le délai de carence n'existe que dans RESUME_C87656 (3 mois).
- **Problème** : question causale sans réponse vérifiable. Elle relève d'une catégorie « prémisse fausse », pas du routing hybride.

### RT-H09 : modifier

- **SQL** : pas de statut d'attente de pièces. Les seules traces de pièces manquantes sont `justif_ss_date` et `attest_non_activite_date` à NULL, documentées comme applicables **à l'Invalidité uniquement**.
- **RAG** : Règlement, Annexe I. Les pièces varient selon la Notice : Transport n'a que les colonnes ITT/DÉCÈS ; seul le Règlement mentionne le justificatif concubin.
- **Reformulation** (bascule sur l'Invalidité, seule moitié SQL calculable) : « Combien de dossiers invalidité en cours n'ont pas encore reçu le justificatif Sécurité sociale, et quelles pièces faut-il fournir pour un dossier invalidité ? »
  - SQL : 303 dossiers sur 823 en cours (`justif_ss_date is null`).
  - RAG : Règlement, Annexe I, colonne IPP (bulletins de salaire, décomptes ou pension SS, notification de taux d'invalidité, RIB).
  - Attention : la colonne s'appelle IPP, pas « invalidité ». Seules les Notices Agriculture et Santé ont aussi cette colonne.

### RT-H10 : modifier

- **RAG** : la garantie obsèques figure dans les 5 Résumés. Seul C87656 la classe en « Garanties optionnelles souscrites ». La liste attendue « C87656 » n'est donc juste que si la question parle d'*option*.
- **SQL** : on ne peut compter que les assurés ayant au moins un dossier sur le contrat, faute de `contrat_id` dans `dim__assures`.
  ```sql
  select count(distinct d.assure_id)
  from fct__dossiers d join dim__contrats c using (contrat_id)
  where c.contrat_numero = 'C87656';  -- 13
  ```
  Pour les 177 autres contrats CADRE sans Résumé : non vérifiable.
- **Reformulation** : « Quel contrat cadre a souscrit la garantie obsèques en option, et combien de ses assurés ont au moins un dossier ? » → C87656 / 13. La forme dépendante est conservée (RAG → SQL). Limite : « quel contrat » sous-entend tout le portefeuille, alors que le corpus n'en documente que 5.

## Question d'architecture : comment `hybride` est-il exécuté ?

**Ni en parallèle, ni en séquence : la route `hybride` n'existe pas dans le code actuel.**

- `src/router.py:21` : `route()` est typée `-> Literal["sql", "rag"]`. Le prompt (`src/router.py:9`) ne décrit que ces deux classes.
- `src/router.py:35-36` : toute autre étiquette lève `ValueError("Réponse inattendue du routeur")`. Si le LLM répondait « hybride », l'appel planterait.
- `src/orchestrator.py:18` : `OrchestratorResult.route` est aussi `Literal["sql", "rag"]`.
- `src/orchestrator.py:35-53` : un seul pipeline est exécuté.
  - Ligne 35 : appel du routeur.
  - Lignes 37-44 : branche SQL (`agent_main(question)`, ligne 38).
  - Ligne 46 : sinon, branche RAG (`generate(question)`).
- Aucun parallélisme : pas de thread, d'`asyncio` ni de `concurrent` dans `src/`.
- La sortie d'un pipeline ne peut pas alimenter l'autre : chacun reçoit seulement la question brute (lignes 38 et 46).

Conséquences pour l'eval set :
1. Avec le code actuel, toute question `hybride` sera routée `sql` ou `rag`. Le score de routing sur ces 10 questions mesurera **ce que le routeur binaire fait quand il est forcé**, pas une capacité hybride.
2. Les questions **dépendantes** (RT-H02 et RT-H10 reformulée) exigent une exécution *séquentielle* avec passage de contexte : RAG → extraction d'un paramètre (seuil, liste de contrats) → SQL. Le parallélisme ne suffira pas pour elles.
3. Les questions **explicites indépendantes** (les autres) peuvent se contenter d'un parallélisme puis d'une fusion. Les distinguer dans l'eval set (`forme: dependante` vs `forme: explicite`) permettra de mesurer les deux implémentations séparément.

## Suggestions du reviewer à reprendre

- Le scoring end-to-end doit exiger les **deux** moitiés de la réponse. Sinon un routeur binaire marque des points partiels.
- Ajouter des routeurs témoins (« toujours sql », « toujours rag ») qui doivent échouer sur tout le lot hybride : c'est un contrôle de discriminance.
