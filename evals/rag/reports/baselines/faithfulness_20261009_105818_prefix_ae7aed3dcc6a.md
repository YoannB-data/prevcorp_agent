# Rapport faithfulness (juge maison)

- Date : 2026-10-09T10:58:18
- Hash du YAML : ae7aed3dcc6a
- Modèle : claude-sonnet-4-6
- Modèle du juge : claude-sonnet-4-6
- Temperature : 0.0
- k : 5
- Variante d'ingestion : prefix (vérifiée contre la collection)

## Synthèse

Questions : 25 dont 0 en erreur d'I/O (exclues des moyennes).

| Type | Faithfulness moyenne |
|---|---|
| **Tous** | 0.92 (24 q.) |
| fait_simple | 0.87 (5 q.) |
| chiffre_precis | 1.00 (5 q.) |
| croisement | 0.93 (13 q.) |
| sans_reponse | 0.75 (1 q.) |

## Détail par question

### RC01 (chiffre_precis)

- faithfulness : 1.00 (4 affirmations)

**Réponse e2e**

> ## Franchise ITT — Contrat C87656
> 
> Le délai de franchise de la garantie Incapacité Temporaire de Travail du contrat C87656 est de **90 jours**.
> 
> La franchise court à compter du **premier jour d'arrêt de travail continu** et s'apprécie **par sinistre**, sauf rechute constatée dans les conditions prévues au contrat.
> 
> Par ailleurs, un **délai de carence de 3 mois** s'applique avant la prise d'effet de la garantie. [RESUME_C87656.pdf]

### RC02 (croisement)

- faithfulness : 1.00 (5 affirmations)

**Réponse e2e**

> Oui, le contrat C87656 prévoit un délai de carence avant la prise d'effet de la garantie ITT.
> 
> **Délai de carence : 3 mois** avant la prise d'effet de la garantie. [RESUME_C87656.pdf]
> 
> Ce délai de carence s'applique en plus de la franchise contractuelle de 90 jours, qui court à compter du premier jour d'arrêt de travail continu et s'apprécie par sinistre (sauf rechute constatée dans les conditions prévues au contrat). [RESUME_C87656.pdf]

### RC03 (croisement)

- faithfulness : 1.00 (5 affirmations)

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les documents fournis concernent le contrat **C73736** [RESUME_C73736.pdf] et non le contrat **C87656**. Il m'est donc impossible de me prononcer sur la clause bénéficiaire type de ce contrat spécifique.
> 
> ---
> 
> **À titre informatif**, sur la question du concubin dans les clauses bénéficiaires type, les documents disponibles montrent des approches différentes selon les conventions :
> 
> - **CCN Santé/Action sociale** : le concubin est **inclus** dans la clause type, sous condition de résidence commune au jour du décès [NOTICE_CCN_sante_action_sociale.pdf]
> - **CCN Transport routier** : le concubin est **exclu**, la convention ne lui reconnaissant pas la qualité de bénéficiaire [NOTICE_CCN_transport_routier.pdf]
> - **CCN Métallurgie** : la clause type ne mentionne pas le concubin [NOTICE_CCN_metallurgie.pdf]
> 
> Pour obtenir la réponse concernant le contrat C87656, il conviendrait de consulter le résumé ou la notice contractuelle correspondante.

### RC04 (sans_reponse)

- faithfulness : N/A (aucune affirmation) (0 affirmations)

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis du contrat C39949 mentionnent uniquement une **prestation d'assistance** (soutien psychologique, aide à domicile, conseil juridique) incluse sans supplément de cotisation [RESUME_C39949.pdf], mais ne précisent pas si le rapatriement à l'étranger en fait partie. Le détail complet des garanties d'assistance est renvoyé au **"contrat d'assistance annexé"**, qui n'est pas disponible dans les documents fournis.
> 
> Pour obtenir une réponse précise, il conviendrait de consulter ce contrat d'assistance annexé.

### RC05 (croisement)

- faithfulness : 1.00 (5 affirmations)

**Réponse e2e**

> ## Analyse comparative : Garantie ITT — Contrat C39949 vs Notice CCN Agriculture
> 
> Oui, il existe un **écart significatif** sur la durée de la franchise ITT.
> 
> ---
> 
> ### 🔴 Point de divergence : Durée de la franchise
> 
> | | Franchise ITT |
> |---|---|
> | **Notice CCN Agriculture** | **90 jours** [NOTICE_CCN_agriculture.pdf] |
> | **Résumé contrat C39949** | **60 jours** [RESUME_C39949.pdf] |
> 
> La Notice CCN Agriculture précise explicitement : *"La franchise applicable à la garantie ITT est fixée à **90 jours**"* et ajoute que *"le régime de base de la convention ne prévoit aucune dérogation à cette modalité"* [NOTICE_CCN_agriculture.pdf].
> 
> Or, le Résumé C39949 mentionne des indemnités versées *"à l'issue de la **franchise de 60 jours**"* [RESUME_C39949.pdf].
> 
> ---
> 
> ### ✅ Point de convergence : Modalité de la franchise
> 
> Les deux documents s'accordent sur le fait que la franchise est **continue**, courant *"sans interruption à compter du premier jour d'arrêt de travail"* [NOTICE_CCN_agriculture.pdf] [RESUME_C39949.pdf].
> 
> ---
> 
> ### ⚠️ Point d'attention
> 
> L'écart sur la durée de franchise (90 j vs 60 j) est notable et favorable à l'assuré dans le contrat C39949. Il conviendrait de vérifier si cette dérogation est contractuellement justifiée, notamment au regard de la mention dans la Notice selon laquelle *"le régime de base ne prévoit aucune dérogation"*.

### RC06 (croisement)

- faithfulness : 0.85 (13 affirmations)
- affirmations NON appuyées :
  - La rente invalidité cesse au décès de l'assuré.
  - La rente invalidité cesse au départ à la retraite de l'assuré.

**Réponse e2e**

> ## Taux de couverture invalidité — Contrat C39949
> 
> Voici les taux applicables, calculés en **pourcentage du salaire annuel brut de référence** [RESUME_C39949.pdf] :
> 
> | Catégorie d'invalidité | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | **1re catégorie** | 35 % | 35 % | 25 % |
> | **2e catégorie** | 45 % | 45 % | 35 % |
> | **3e catégorie** | 70 % | 70 % | 55 % |
> 
> **Précisions importantes** [RESUME_C39949.pdf] :
> - La catégorie d'invalidité est **notifiée par la CPAM** et communiquée à l'assureur à l'ouverture du dossier.
> - La rente cesse notamment au **décès de l'assuré** ou à son **départ à la retraite**.

### RC07 (croisement)

- faithfulness : 1.00 (10 affirmations)

**Réponse e2e**

> ## Contrat C87656 — Incapacité Temporaire de Travail
> 
> ### Taux de couverture
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise contractuelle de 90 jours | **82 %** | **78 %** |
> 
> [RESUME_C87656.pdf]
> 
> ### Franchise
> 
> - **Durée : 90 jours**
> - La franchise court à compter du **premier jour d'arrêt de travail continu** et s'apprécie **par sinistre**, sauf rechute constatée dans les conditions prévues au contrat.
> - Un **délai de carence de 3 mois** s'applique avant la prise d'effet de la garantie.
> 
> [RESUME_C87656.pdf]
> 
> ### Modalités de versement
> 
> Les indemnités sont versées **mensuellement à terme échu**, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité ou au décès de l'assuré.
> 
> [RESUME_C87656.pdf]

### RC08 (chiffre_precis)

- faithfulness : 1.00 (15 affirmations)

**Réponse e2e**

> ## Garanties décès — Contrat C83792
> 
> *(Convention collective nationale de l'enseignement privé)*
> 
> ### Capital décès toutes causes
> Le capital versé aux bénéficiaires dépend de la situation de famille au jour du décès :
> 
> | Situation de famille | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | Célibataire, veuf, divorcé sans enfant à charge | 140 % | 140 % | 115 % |
> | Marié ou pacsé sans enfant à charge | 160 % | 160 % | 135 % |
> 
> *(Les taux sont exprimés en % du salaire annuel brut de référence)*
> [RESUME_C83792.pdf]
> 
> ### Majorations familiales
> Une majoration par enfant à charge est applicable, **cumulable sans limitation de rang** :
> 
> | | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | Majoration par enfant à charge | +28 % | +28 % | +18 % |
> 
> [RESUME_C83792.pdf]
> 
> ### Autres garanties liées au décès
> 
> | Garantie | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | Invalidité absolue et définitive *(anticipation du capital décès)* | 100 % | 100 % | 100 % |
> | Décès accidentel *(capital additionnel)* | 100 % | 100 % | 100 % |
> | Double effet *(décès simultané ou postérieur du conjoint)* | 100 % | 100 % | 100 % |
> | **Obsèques** *(capital forfaitaire)* | **1 900 €** | **1 900 €** | **1 900 €** |
> 
> [RESUME_C83792.pdf]

### RC09 (chiffre_precis)

- faithfulness : 1.00 (6 affirmations)

**Réponse e2e**

> Oui, une rente éducation est prévue sur le contrat C83792.
> 
> Selon les documents disponibles, lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée **jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire**, selon les taux annuels suivants :
> 
> | Âge de l'enfant | Taux annuel |
> |---|---|
> | Jusqu'à 11 ans | 5,5 % |
> | De 12 à 17 ans | 8 % |
> | De 18 à 25 ans (études ou apprentissage) | 11 % |
> 
> [RESUME_C83792.pdf]

### RC10 (croisement)

- faithfulness : 0.64 (11 affirmations)
- affirmations NON appuyées :
  - La garantie optionnelle 'Rente éducation' est disponible sur le contrat C87656.
  - La garantie optionnelle 'Garantie double effet' est disponible sur le contrat C87656.
  - La garantie optionnelle 'Garantie dépendance totale' est disponible sur le contrat C87656.
  - La garantie optionnelle 'Indemnisation surcomplémentaire de l'incapacité temporaire de travail au-delà de la tranche B' est disponible sur le contrat C87656.

**Réponse e2e**

> ## Garanties optionnelles du contrat C87656
> 
> Oui, plusieurs garanties optionnelles sont disponibles. Selon les documents, voici celles qui sont listées de manière générale :
> 
> **Garanties optionnelles possibles :**
> - Rente éducation
> - Garantie double effet
> - Garantie obsèques
> - Garantie dépendance totale
> - Indemnisation surcomplémentaire de l'incapacité temporaire de travail au-delà de la tranche B
> 
> [REGLEMENT_prevcorp.pdf]
> 
> **Garanties optionnelles effectivement souscrites sur le contrat C87656 :**
> 
> D'après le résumé du contrat, les garanties optionnelles souscrites sont :
> 
> - **Rente de conjoint** : en cas de décès de l'assuré, une rente viagère est versée au conjoint ou partenaire de PACS, à hauteur de **15 % du salaire annuel brut de référence** (Tranche A et Tranche B)
> - **Garantie obsèques** : capital forfaitaire de **2 500 €**
> 
> [RESUME_C87656.pdf]
> 
> > ⚠️ Le document précise que *"les garanties optionnelles effectivement souscrites, ainsi que leurs conditions et montants, figurent dans le résumé des garanties propre à chaque contrat"* [REGLEMENT_prevcorp.pdf]. Pour toute confirmation exhaustive, il convient de se référer au résumé complet du contrat C87656.

### RC11 (croisement)

- faithfulness : 1.00 (8 affirmations)

**Réponse e2e**

> ## Franchise ITT du contrat C73736 : continue ou discontinue ?
> 
> ### Nature de la franchise dans le contrat C73736
> 
> Le contrat C73736 prévoit une **franchise continue** :
> 
> > *« La franchise est une franchise continue et court sans interruption à compter du premier jour d'arrêt de travail. »*
> > [RESUME_C73736.pdf]
> 
> ### Comparaison avec les régimes de référence
> 
> Deux régimes distincts apparaissent dans les documents disponibles :
> 
> | Référentiel | Type de franchise |
> |---|---|
> | CCN Agriculture | Continue (90 jours) — régime par défaut, sans dérogation possible [NOTICE_CCN_agriculture.pdf] |
> | CCN Métallurgie | **Discontinue** — les journées se cumulent même séparées par des reprises de travail [NOTICE_CCN_metallurgie_distracteur.pdf] |
> 
> ### Conclusion
> 
> La franchise **continue** du contrat C73736 est **cohérente avec le régime par défaut de la CCN Agriculture** [NOTICE_CCN_agriculture.pdf], qui ne prévoit aucune dérogation à cette modalité.
> 
> Elle constitue en revanche une **différence notable** par rapport au régime de la CCN Métallurgie, qui retient une franchise discontinue [NOTICE_CCN_metallurgie_distracteur.pdf].
> 
> > ⚠️ Je ne dispose pas du Règlement général PrevCorp mentionné dans la notice métallurgie (article 14) pour confirmer quel régime constitue le « défaut » contractuel global. Si ce point est déterminant, il conviendrait de consulter ce document.

### RC12 (chiffre_precis)

- faithfulness : 1.00 (1 affirmations)

**Réponse e2e**

> D'après les documents disponibles, pour le contrat **C73736**, le taux de la rente invalidité **2e catégorie** sur la **Tranche B** est de :
> 
> ## **50 %** du salaire annuel brut de référence
> 
> [RESUME_C73736.pdf]

### RC13 (croisement)

- faithfulness : 1.00 (9 affirmations)

**Réponse e2e**

> ## Clause bénéficiaire applicable au contrat C73736
> 
> Le contrat C73736 applique la **clause bénéficiaire type**.
> 
> En effet, il est explicitement indiqué :
> 
> > *"Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit."* [RESUME_C73736.pdf]
> 
> ### Ordre de priorité de la clause type applicable :
> 
> Conformément au Règlement PrevCorp, le capital décès est versé dans l'ordre suivant [REGLEMENT_prevcorp.pdf] :
> 
> 1. **Conjoint** non séparé de corps ou partenaire pacsé
> 2. À défaut, **enfants** nés ou à naître, par parts égales
> 3. À défaut, **parents**
> 4. À défaut, **autres ascendants**
> 5. À défaut, **héritiers**
> 
> > ⚠️ Il n'y a donc **aucune répartition personnalisée** à mentionner pour ce contrat. Si l'assuré souhaite désigner des bénéficiaires spécifiques, il peut le faire à tout moment par écrit en précisant leur identité, rang de priorité et quote-part. [REGLEMENT_prevcorp.pdf]

### RC14 (fait_simple)

- faithfulness : 1.00 (3 affirmations)

**Réponse e2e**

> ## Justificatif de qualité de concubin en cas de décès
> 
> Selon les documents PrevCorp, pour prouver la qualité de concubin dans le cadre d'une demande de **rente conjoint suite à un décès**, il faut fournir :
> 
> > **Une attestation de vie commune** ou, à défaut, **deux justificatifs de domicile commun de plus de deux ans**.
> 
> [REGLEMENT_prevcorp.pdf — Extraits 1, 2 et 4]
> 
> ---
> 
> ⚠️ **Point d'attention important** : La convention collective du transport routier **ne reconnaît pas** la qualité de concubin comme ouvrant droit aux garanties liées à la situation de famille. Aucune rubrique n'est prévue à cet effet dans le bulletin d'adhésion individuel.
> 
> [NOTICE_CCN_transport_routier.pdf — Extrait 3]
> 
> Il convient donc de vérifier le régime applicable à l'assuré avant de constituer le dossier.

### RC15 (fait_simple)

- faithfulness : 1.00 (5 affirmations)

**Réponse e2e**

> ## Durée de la franchise en cas d'arrêt maladie ordinaire
> 
> La franchise est de **90 jours calendaires**, décomptés à partir du premier jour de l'arrêt de travail. [FAQ_prevcorp.pdf]
> 
> Cette franchise est de type **continu** : le délai court sans interruption à compter du premier jour de l'arrêt de travail, quelle que soit la durée de celui-ci. [NOTICE_CCN_metallurgie.pdf] [REGLEMENT_prevcorp.pdf]
> 
> > ⚠️ **Point important** : le jour de carence de la Sécurité sociale et la franchise contractuelle de 90 jours sont deux notions **distinctes** et indépendantes l'une de l'autre. [FAQ_prevcorp.pdf]
> 
> ---
> *Note : Un document distracteur ([NOTICE_CCN_metallurgie_distracteur.pdf]) mentionne une franchise de 60 jours en modalité discontinue, mais ce régime ne correspond pas aux conditions de base du contrat PrevCorp décrites dans les autres documents.*

### RC16 (fait_simple)

- faithfulness : 1.00 (4 affirmations)

**Réponse e2e**

> Non, la franchise de 90 jours n'est pas retardée par le jour de carence de la Sécurité sociale.
> 
> Ces deux notions sont **distinctes** : la franchise contractuelle de 90 jours démarre **au premier jour de l'arrêt de travail**, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. [FAQ_prevcorp.pdf]

### RC17 (sans_reponse)

- faithfulness : 0.75 (4 affirmations)
- affirmations NON appuyées :
  - Les taux de cotisation du contrat C73736 sont des taux globaux toutes garanties confondues.

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits du contrat **C73736** indiquent uniquement les **taux de cotisation globaux** (toutes garanties confondues) pour le personnel cadre :
> 
> | Tranche A | Tranche B | Tranche C |
> |-----------|-----------|-----------|
> | 1,60 % | 2,45 % | 2,45 % |
> 
> [RESUME_C73736.pdf]
> 
> Aucun document disponible ne ventile ces cotisations **garantie par garantie**, ni ne précise la part spécifiquement affectée à la rente de conjoint, ni la répartition employeur/salarié.

### RC18 (chiffre_precis)

- faithfulness : 1.00 (4 affirmations)

**Réponse e2e**

> ## Capital décès — Contrat C20077
> 
> Pour un salarié **célibataire, veuf ou divorcé sans personne à charge**, le capital décès toutes causes s'élève à :
> 
> | Tranche A | Tranche B |
> |-----------|-----------|
> | **120 %** | **120 %** |
> 
> Ces taux sont exprimés en pourcentage du **salaire annuel brut de référence**, la tranche A correspondant à la part de rémunération jusqu'au plafond annuel de la Sécurité sociale, la tranche B à la part au-delà.
> 
> [RESUME_C20077.pdf]

### RC19 (croisement)

- faithfulness : 1.00 (8 affirmations)

**Réponse e2e**

> ## Majoration capital décès par enfant à charge — Contrat C20077
> 
> **Oui**, le contrat C20077 prévoit bien une majoration du capital décès par enfant à charge.
> 
> **Taux : +25 % par enfant à charge**
> 
> Les conditions d'application sont les suivantes [RESUME_C20077.pdf] :
> - La majoration s'applique **par enfant à charge reconnu au jour du sinistre**
> - Elle est **cumulable sans limitation de rang**
> - Elle s'applique **quelle que soit la situation de famille** retenue
> - Elle vient **s'ajouter au capital de base sans condition d'ancienneté** de l'enfant dans le foyer
> 
> ---
> 
> > À titre de comparaison, le contrat C73736 prévoit une majoration similaire mais à des taux différents : **+30 %** en Tranches A et B, et **+20 %** en Tranche C [RESUME_C73736.pdf].

### RC20 (croisement)

- faithfulness : 1.00 (2 affirmations)

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles indiquent que le taux de couverture en **invalidité 1re catégorie** pour le contrat C20077 est de **50 % du salaire annuel brut de référence**, sur les tranches A et B. [RESUME_C20077.pdf]
> 
> Cependant, **je ne trouve pas cette information dans les documents disponibles** concernant la nature de ce taux : il m'est impossible de déterminer, sur la base des extraits fournis, s'il s'agit du **taux de base issu du Règlement de Prévoyance** de la Convention Collective Nationale du Transport Routier, ou d'une **dérogation négociée** au niveau de l'entreprise ou de la branche.
> 
> Pour répondre précisément à cette question, il faudrait consulter :
> - Le **Règlement de Prévoyance de la CCN Transport Routier** (accord de branche),
> - Et/ou les **conditions particulières du contrat C20077** qui préciseraient une éventuelle dérogation.

### RC21 (fait_simple)

- faithfulness : 1.00 (7 affirmations)

**Réponse e2e**

> ## Les 3 catégories d'invalidité
> 
> Les trois catégories d'invalidité sont définies dans les mêmes termes que ceux de la Sécurité sociale :
> 
> | Catégorie | Définition |
> |-----------|------------|
> | **1re catégorie** | Invalides **capables d'exercer une activité rémunérée** |
> | **2e catégorie** | Invalides **absolument incapables d'exercer une profession quelconque** |
> | **3e catégorie** | Invalides absolument incapables d'exercer une profession quelconque **et dans l'obligation de recourir à l'assistance d'une tierce personne** pour accomplir les actes ordinaires de la vie |
> 
> [FAQ_prevcorp.pdf] [REGLEMENT_prevcorp.pdf]
> 
> ---
> 
> ## Détermination de la catégorie
> 
> La catégorie est **déterminée par le médecin conseil de la Sécurité sociale**, puis **notifiée à l'assuré par la caisse primaire d'assurance maladie (CPAM)**, qui la communique ensuite à l'assureur lors de l'ouverture du dossier.
> 
> [FAQ_prevcorp.pdf] [RESUME_C83792.pdf] [RESUME_C73736.pdf]

### RC22 (croisement)

- faithfulness : 0.60 (5 affirmations)
- affirmations NON appuyées :
  - Le délai de prescription applicable à une action relative à la garantie incapacité de travail est de 5 ans sur le contrat C20077.
  - La dérogation portant le délai de prescription à 5 ans est applicable au contrat C20077.

**Réponse e2e**

> ## Délai de prescription — Incapacité de travail
> 
> Le délai de prescription applicable à une action relative à la **garantie incapacité de travail** est de **5 ans**.
> 
> En effet, par dérogation au délai de droit commun de 2 ans, et **compte tenu des spécificités du secteur du transport routier**, ce délai est porté à 5 ans. [NOTICE_CCN_transport_routier.pdf]
> 
> > À noter : le contrat C20077 relevant de la **Convention collective nationale du transport routier** [RESUME_C20077.pdf], cette dérogation de 5 ans lui est applicable.

### RC23 (croisement)

- faithfulness : 1.00 (14 affirmations)

**Réponse e2e**

> ## Démarches et taux des indemnités journalières — Contrat C20077
> 
> ### 📋 Démarches à effectuer
> 
> Selon [FAQ_prevcorp.pdf], le salarié doit :
> 
> 1. **Transmettre son avis d'arrêt de travail** (initial et prolongations) à son **employeur dans les 48 heures** suivant sa délivrance.
> 2. L'employeur dispose ensuite de **8 jours** pour adresser à l'assureur :
>    - Une déclaration d'arrêt de travail
>    - Une copie de l'avis médical
>    - Les bulletins de salaire des **trois derniers mois**
> 
> > Le dossier peut être transmis via le **formulaire de l'espace adhérent en ligne** ou par **courrier au service prestations** (adresse sur la carte d'adhérent).
> 
> ---
> 
> ### 💰 Taux des indemnités journalières
> 
> Selon [RESUME_C20077.pdf], les indemnités sont versées **à l'issue de la franchise contractuelle** aux taux suivants :
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise | **78 %** | **72 %** |
> 
> Ces taux s'entendent **sous déduction des prestations de la Sécurité sociale** et de tout revenu de remplacement.
> 
> ---
> 
> ### ⚠️ Points importants
> 
> - La franchise court à compter du **premier jour d'arrêt continu** et s'apprécie **par sinistre** (sauf rechute). [RESUME_C20077.pdf]
> - Les indemnités sont versées **mensuellement à terme échu**, sur présentation des décomptes de la Sécurité sociale. [RESUME_C20077.pdf]
> - Le versement cesse à la **reprise du travail**, à la **liquidation d'une pension d'invalidité**, au **décès** ou au **départ à la retraite**. [RESUME_C20077.pdf]

### RC24 (croisement)

- faithfulness : 1.00 (8 affirmations)

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles ne permettent pas de répondre précisément à cette question combinée.
> 
> Voici ce qui est documenté séparément :
> 
> **Sur la reconnaissance du concubin comme bénéficiaire :**
> La notice [NOTICE_CCN_sante_action_sociale.pdf] reconnaît le concubin comme bénéficiaire de la clause type, **sous condition de résidence commune avec l'assuré au jour du décès**. Les autres notices ([NOTICE_CCN_metallurgie.pdf], [NOTICE_CCN_agriculture.pdf]) ne mentionnent pas le concubin dans leur clause bénéficiaire type.
> 
> **Sur les montants du contrat C87656 :**
> Le résumé [RESUME_C87656.pdf] mentionne :
> - Une **rente de conjoint** (15 % en Tranche A et B) versée au **conjoint ou partenaire de PACS** survivant — le concubin n'est pas explicitement mentionné comme éligible à cette rente.
> - Un **capital obsèques forfaitaire de 2 500 €** versé à la personne ayant engagé les frais.
> 
> **Limite :** Le montant du capital décès principal du contrat C87656 n'est pas renseigné dans les extraits fournis, et l'éligibilité du concubin à la rente de conjoint sur ce contrat spécifique n'est pas confirmée.
> 
> > Je ne trouve pas cette information complète dans les documents disponibles. Il est recommandé de consulter la notice d'information complète du contrat C87656.

### RC25 (fait_simple)

- faithfulness : 0.33 (9 affirmations)
- affirmations NON appuyées :
  - La clause bénéficiaire type standard de PrevCorp prévoit en premier lieu le conjoint non séparé de corps ou le partenaire pacsé.
  - La clause bénéficiaire type standard de PrevCorp prévoit en deuxième lieu, à défaut de conjoint ou partenaire pacsé, les enfants nés ou à naître par parts égales.
  - La clause bénéficiaire type standard de PrevCorp prévoit en troisième lieu, à défaut d'enfants, les parents.
  - La clause bénéficiaire type standard de PrevCorp prévoit en quatrième lieu, à défaut de parents, les autres ascendants.
  - La clause bénéficiaire type standard de PrevCorp prévoit en cinquième lieu, à défaut d'autres ascendants, les héritiers.
  - Sur le contrat C20077, le concubin ne serait pas reconnu bénéficiaire en l'absence de désignation personnalisée.

**Réponse e2e**

> ## Bénéficiaires du capital décès sur le contrat C20077 en l'absence de désignation
> 
> Les documents disponibles ne contiennent pas la clause bénéficiaire type spécifique au contrat C20077 ni à la Convention collective nationale du transport routier.
> 
> Cependant, voici ce que les extraits permettent d'établir :
> 
> **Ce qui est confirmé pour C20077 :**
> - Aucune mention d'une clause bénéficiaire type propre à ce contrat n'apparaît dans les extraits disponibles. [RESUME_C20077.pdf]
> 
> **Ce qui est applicable par analogie (autres contrats PrevCorp) :**
> La clause bénéficiaire type standard de PrevCorp, telle que décrite dans la notice CCN Agriculture, prévoit l'ordre de priorité suivant en l'absence de désignation particulière :
> 
> 1. Le **conjoint** non séparé de corps ou le **partenaire pacsé**
> 2. À défaut, les **enfants** nés ou à naître, par parts égales
> 3. À défaut, les **parents**
> 4. À défaut, les **autres ascendants**
> 5. À défaut, les **héritiers**
> 
> [NOTICE_CCN_agriculture.pdf]
> 
> > ⚠️ **Point important :** Le concubin **n'est pas mentionné** dans cette clause type (contrairement à la notice CCN Santé/Action sociale qui l'inclut sous conditions). Pour C20077, le concubin ne serait donc **pas reconnu bénéficiaire** en l'absence de désignation personnalisée.
> 
> **Je ne trouve pas cette information de manière explicite et certaine dans les documents disponibles** pour le contrat C20077 spécifiquement. Il est recommandé de consulter les **conditions générales du contrat C20077** pour confirmation.
