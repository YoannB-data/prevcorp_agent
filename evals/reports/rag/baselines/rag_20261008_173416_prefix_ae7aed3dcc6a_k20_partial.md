# Rapport d'éval RAG

- Date : 2026-10-08T17:34:16
- Hash du YAML : ae7aed3dcc6a
- Modèle : claude-sonnet-4-6
- Modèle du juge : claude-sonnet-4-6
- Temperature : 0.0
- k : 20
- Variante d'ingestion : prefix (vérifiée contre la collection)
- Contexte isolé : document entier

## Synthèse

Questions : 3 dont 0 en erreur d'I/O (exclues des scores et des dénominateurs ci-dessous).

| Type | R (retrieval) | E (end-to-end) | I (isolé) |
|---|---|---|---|
| **Tous** | 1/3 | 2/3 | 2/3 |
| fait_simple | N/A | N/A | N/A |
| chiffre_precis | N/A | N/A | N/A |
| croisement | 1/3 | 2/3 | 2/3 |
| sans_reponse | N/A | N/A | N/A |

### Répartition des diagnostics

| Diagnostic | Famille | Nb |
|---|---|---|
| sain | succès | 1 |
| échec de retrieval | échec | 1 |
| succès sans la source, isolé KO | suspect | 1 |

## Détail par question

### RC03 (croisement)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Concubin et clause bénéficiaire type — Contrat C87656
> 
> **Non**, le concubin n'est pas inclus dans la clause bénéficiaire type applicable au contrat C87656.
> 
> Le résumé de ce contrat précise qu'**aucune désignation bénéficiaire personnalisée n'a été notifiée**, et que la **clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit** [RESUME_C73736.pdf — applicable par analogie au mécanisme de renvoi au règlement].
> 
> Or, la clause bénéficiaire type du Règlement PrevCorp désigne, dans l'ordre :
> 1. Le **conjoint** non séparé de corps ou le **partenaire de PACS** ;
> 2. À défaut, les **enfants** nés ou à naître ;
> 3. À défaut, les **parents** ;
> 4. À défaut, les **autres ascendants** ;
> 5. À défaut, les **héritiers**.
> 
> Le concubin **n'y figure pas** [REGLEMENT_prevcorp.pdf].
> 
> > ⚠️ À titre de comparaison, la notice CCN Santé et action sociale prévoit une clause type incluant le concubin sous condition de résidence commune [NOTICE_CCN_sante_action_sociale.pdf], mais cette disposition **ne s'applique pas** au contrat C87656, qui relève du Règlement PrevCorp standard.
> 
> **En conclusion** : un concubin ne peut bénéficier du capital décès au titre de la clause type sur ce contrat. Une **désignation bénéficiaire personnalisée** par écrit serait nécessaire pour l'inclure [FAQ_prevcorp.pdf].

**Réponse isolée**

> Je ne dispose pas du contrat C87656 dans les documents fournis. Cependant, je peux vous indiquer ce que prévoient les deux documents disponibles sur la clause bénéficiaire type, selon le contrat applicable :
> 
> **Règlement général PrevCorp**
> Le bénéficiaire de premier rang est uniquement le **conjoint (marié) ou le partenaire de PACS**. Le concubin n'est **pas mentionné** dans la clause bénéficiaire type. [REGLEMENT_prevcorp.pdf]
> 
> **Notice CCN Santé et Action Sociale (IDCC 413)**
> La clause bénéficiaire type inclut, en premier rang : le conjoint, le partenaire de PACS, **ou le concubin sous condition de résidence commune avec l'assuré au jour du décès**. [NOTICE_CCN_sante_action_sociale.pdf]
> 
> ---
> 
> **Conclusion :** La réponse dépend du document contractuel applicable au contrat C87656 :
> - S'il relève de la **CCN Santé et Action Sociale**, le concubin est inclus (sous condition de résidence commune).
> - S'il relève du **règlement général seul**, le concubin n'est **pas inclus** dans la clause type.
> 
> Pour une réponse définitive, il convient de consulter le **résumé des garanties propre au contrat C87656**.


Chunks e2e récupérés :

1. `NOTICE_CCN_transport_routier` #11 (score 0.4262) — Arrêt de travail initial et prolongations Oui Non Décomptes d'indemnités journalières de la Sécurité sociale Oui Non Acte de décès Non Oui Livret de famille ou extrait d'acte de naissance Non Oui Relevé d'identité bancaire du bénéficiaire Oui Oui Annexe II — Adhésion au régime Le bulletin d'adhésion…
2. `NOTICE_CCN_metallurgie` #12 (score 0.4235) — Terme de la garantie. Le versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint d…
3. `RESUME_C73736` #2 (score 0.4089) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
4. `NOTICE_CCN_sante_action_sociale` #10 (score 0.3976) — en une seule fois sur présentation de la facture acquittée par la personne ayant engagé les frais. Terme de la garantie. Le versement de la rente de conjoint cesse au décès du bénéficiaire. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation parti…
5. `NOTICE_CCN_metallurgie_distracteur` #12 (score 0.3832) — versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire personnalisée Le régime applicable aux entreprises relevant de la présente convention collective repose sur un…
6. `NOTICE_CCN_agriculture` #11 (score 0.3614) — montants correspondants, figurent dans le résumé des garanties propre à chaque contrat. Modalités de versement. Les modalités de versement sont identiques à celles de la garantie de base à laquelle l'option se rattache. Terme de la garantie. Le versement cesse dans les mêmes conditions que la garant…
7. `RESUME_C87656` #1 (score 0.3595) — sociale, tranche B au-delà). Garanties de base Garantie décès toutes causes En cas de décès de l'assuré, quelle qu'en soit la cause, un capital est versé aux bénéficiaires désignés. Son montant dépend de la situation de famille du salarié constatée au jour du décès. Situation de famille Tranche A Tr…
8. `RESUME_C87656` #4 (score 0.3557) — la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du sal…
9. `FAQ_prevcorp` #4 (score 0.3545) — la vie. Qui détermine ma catégorie d'invalidité ? La catégorie est déterminée par le médecin conseil de la Sécurité sociale. Elle vous est notifiée par la caisse primaire d'assurance maladie, puis communiquée à l'assureur lors de l'ouverture de votre dossier d'invalidité. Décès Puis-je choisir libre…
10. `NOTICE_CCN_sante_action_sociale` #11 (score 0.3501) — entre eux ; à défaut, à ses parents ; à défaut, à ses autres ascendants ; à défaut, à ses héritiers. Clause bénéficiaire personnalisée Vous pouvez désigner un ou plusieurs bénéficiaires de votre choix, par écrit, en précisant leur identité, leur rang de priorité et leur quote-part. Cette désignation…
11. `RESUME_C87656` #2 (score 0.3496) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
12. `NOTICE_CCN_metallurgie` #13 (score 0.3471) — à tout moment. Nom du bénéficiaire Rang de priorité Répartition Nom Prénom 1 60 % Nom Prénom 1 40 % Nom Prénom 2 100 % À défaut de notification écrite d'une désignation particulière à l'assureur, la clause bénéficiaire type décrite ci-dessus s'applique de plein droit, sans qu'aucune répartition pers…
13. `NOTICE_CCN_agriculture` #12 (score 0.3425) — un ou plusieurs bénéficiaires de votre choix, par écrit, en précisant leur identité, leur rang de priorité et leur quote-part. Cette désignation peut être modifiée à tout moment. Nom du bénéficiaire Rang de priorité Répartition Nom Prénom 1 60 % Nom Prénom 1 40 % Nom Prénom 2 100 % Exclusions Exclus…
14. `RESUME_C87656` #0 (score 0.3371) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 180 % | 180 % Marié ou pacsé sans personne à charge | 220 % | 220 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…
15. `REGLEMENT_prevcorp` #12 (score 0.337) — ; — rente éducation ; — garantie double effet ; — garantie obsèques ; — garantie dépendance totale ; — indemnisation surcomplémentaire de l'incapacité temporaire de travail au-delà de la tranche B. Les garanties optionnelles effectivement souscrites, ainsi que leurs conditions et montants, figurent …
16. `REGLEMENT_prevcorp` #17 (score 0.3362) — Oui Non d'apprentissage Justificatif de qualité de concubin Non Non Oui Non Non (attestation de vie commune ou, à défaut, deux justificatifs de domicile commun de plus de deux ans) Relevé d'identité bancaire du Oui Oui Oui Oui Oui bénéficiaire
17. `NOTICE_CCN_transport_routier` #9 (score 0.3355) — défaut, à ses héritiers. Clause bénéficiaire personnalisée Vous pouvez désigner un ou plusieurs bénéficiaires de votre choix, par écrit, en précisant leur identité, leur rang de priorité et leur quote-part. Cette désignation peut être modifiée à tout moment. Exclusions Exclusions applicables à toute…
18. `RESUME_C87656` #3 (score 0.333) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
19. `NOTICE_CCN_metallurgie_distracteur` #1 (score 0.3289) — relevant d'un même collège tel que défini par la convention collective : ouvriers, employés, techniciens et agents de maîtrise, ingénieurs et cadres. Conjoint Personne mariée avec l'assuré et non séparée de corps par jugement définitif, ou partenaire lié à l'assuré par un pacte civil de solidarité (…
20. `NOTICE_CCN_metallurgie` #1 (score 0.3281) — relevant d'un même collège tel que défini par la convention collective : ouvriers, employés, techniciens et agents de maîtrise, ingénieurs et cadres. Conjoint Personne mariée avec l'assuré et non séparée de corps par jugement définitif, ou partenaire lié à l'assuré par un pacte civil de solidarité (…

### RC20 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp'] — points absents des chunks : ['O1']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> ## Taux d'invalidité 1re catégorie — Contrat C20077
> 
> Le contrat C20077 prévoit un taux de **50 % sur les tranches A et B** pour l'invalidité 1re catégorie. [RESUME_C20077.pdf]
> 
> ---
> 
> ### Réponse à la question
> 
> **Je ne trouve pas cette information dans les documents disponibles.**
> 
> Les documents fournis ne contiennent pas de Règlement PrevCorp détaillant un « taux de base » général, ni d'élément permettant d'identifier si ce taux de 50 % constitue le taux standard du Règlement ou une dérogation négociée dans le cadre de la Convention collective nationale du transport routier.
> 
> À titre de comparaison, les autres contrats disponibles affichent des taux différents pour la même catégorie :
> - C73736 (cadres) : 40 % / 40 % / 30 % [RESUME_C73736.pdf]
> - C87656 : 55 % / 55 % [RESUME_C87656.pdf]
> - C39949 : 35 % / 35 % / 25 % [RESUME_C39949.pdf]
> 
> Ce constat illustre une variabilité entre contrats, mais **ne permet pas de conclure sur la nature réglementaire ou dérogatoire du taux de C20077** sans accès au Règlement PrevCorp de référence.

**Réponse isolée**

> ## Taux d'invalidité 1re catégorie — Contrat C20077
> 
> **Le taux appliqué est identique au taux de base du Règlement général : il n'y a pas de dérogation.**
> 
> ### Comparaison directe
> 
> | Source | 1re catégorie | 2e catégorie | 3e catégorie |
> |--------|--------------|--------------|--------------|
> | Règlement général (taux de base) | **50 %** | 100 % | 100 % |
> | Contrat C20077 (CCN transport routier, non cadre) | **50 %** | 75 % | 100 % |
> 
> [REGLEMENT_prevcorp.pdf] — Article 15 : *"la rente est exprimée en pourcentage du salaire brut de référence, à raison de **50 % pour la 1re catégorie** et de **100 % pour les 2e et 3e catégories**"*, avec la précision que *"le résumé des garanties propre à chaque contrat précise le taux effectivement applicable, qui peut différer de ce taux de base."*
> 
> [RESUME_C20077.pdf] : confirme **50 % en tranche A et B** pour la 1re catégorie.
> 
> ### Conclusion
> 
> - Pour la **1re catégorie** : le contrat C20077 retient le taux de base (50 %) → **pas de dérogation**.
> - Pour la **2e catégorie** : en revanche, le contrat C20077 applique **75 %** au lieu des 100 % prévus par défaut → **c'est là que se situe la dérogation CCN**.

Points en échec (e2e) : ['O1']

Chunks e2e récupérés :

1. `RESUME_C20077` #3 (score 0.5579) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
2. `RESUME_C20077` #5 (score 0.5328) — cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assu…
3. `RESUME_C20077` #4 (score 0.5203) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'appr…
4. `RESUME_C20077` #1 (score 0.4889) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…
5. `RESUME_C20077` #0 (score 0.4766) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 120 % | 120 % Marié ou pacsé sans personne à charge | 150 % | 150 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…
6. `RESUME_C20077` #2 (score 0.4706) — décès Garantie Tranche A Tranche B Invalidité absolue et définitive (anticipation du capital décès) 100 % 100 % Décès accidentel (capital additionnel) 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % Obsèques (capital forfaitaire) 2 000 € 2 000 € Rente éducation Lorsq…
7. `RESUME_C73736` #6 (score 0.4608) — primaire d'assurance maladie et communiquée à l'assureur lors de l'ouverture du dossier. Catégorie Tranche A Tranche B Tranche C Invalidité 1re catégorie 40 % 40 % 30 % Invalidité 2e catégorie 50 % 50 % 40 % Invalidité 3e catégorie 75 % 75 % 60 % Assistance Une prestation d'assistance (soutien psych…
8. `RESUME_C39949` #4 (score 0.4446) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sé…
9. `FAQ_prevcorp` #5 (score 0.4416) — dans la limite de 12 mois, sans cotisation supplémentaire à votre charge. 6. Divers Je suis salarié du contrat C20077 et je me trouve en arrêt de travail : quelles démarches dois- je effectuer pour percevoir mes indemnités journalières complémentaires ? Vous devez transmettre votre avis d'arrêt de t…
10. `RESUME_C87656` #4 (score 0.4374) — la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du sal…
11. `RESUME_C87656` #3 (score 0.434) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
12. `RESUME_C73736` #3 (score 0.4321) — décès) Décès accidentel (capital additionnel) 100 % 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % 100 % Obsèques (capital forfaitaire) 2 200 € 2 200 € 2 200 € Âge de l'enfant | Taux annuel Jusqu'à 11 ans | 6 % De 12 à 17 ans | 9 % De 18 à 25 ans (études ou apprenti…
13. `RESUME_C83792` #4 (score 0.4312) — | 28 % Invalidité 2e catégorie | 48 % | 48 % | 38 % Invalidité 3e catégorie | 72 % | 72 % | 57 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5,5 % De 12 à 17 ans 8 % De 18 à 25 ans (études ou apprentissage) 11 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par l…
14. `RESUME_C73736` #5 (score 0.4302) — court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 90 jours 80 % 75 % 70 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de ma…
15. `RESUME_C73736` #2 (score 0.4229) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
16. `RESUME_C83792` #5 (score 0.4222) — la franchise de 90 jours 78 % 72 % 66 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquida…
17. `NOTICE_CCN_sante_action_sociale` #8 (score 0.4221) — dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Modalités de versement. Les indemnités sont versées mensuellement à terme échu, au souscripteur en cas de maintien de salaire, à l'assuré dans les autres cas. Terme de la garantie. Le versement cesse à la r…
18. `FAQ_prevcorp` #4 (score 0.4221) — la vie. Qui détermine ma catégorie d'invalidité ? La catégorie est déterminée par le médecin conseil de la Sécurité sociale. Elle vous est notifiée par la caisse primaire d'assurance maladie, puis communiquée à l'assureur lors de l'ouverture de votre dossier d'invalidité. Décès Puis-je choisir libre…
19. `RESUME_C87656` #2 (score 0.4219) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
20. `RESUME_C39949` #5 (score 0.4162) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidatio…

### RC22 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : OK ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : succès sans la source, isolé KO (suspect) — à corriger : audit manuel

**Réponse e2e**

> ## Délai de prescription pour l'incapacité de travail — Contrat C20077
> 
> Le contrat C20077 relève de la **Convention collective nationale du transport routier** [RESUME_C20077.pdf].
> 
> Pour cette convention, la notice prévoit une règle dérogatoire explicite :
> 
> > *« Par dérogation, et compte tenu des spécificités du secteur du transport routier, le délai de prescription applicable à une action relative à la garantie incapacité de travail est porté à **5 ans**.»*
> > [NOTICE_CCN_transport_routier.pdf]
> 
> Le délai de droit commun de 2 ans s'applique aux autres actions dérivant du contrat, mais **pour l'incapacité de travail spécifiquement, c'est bien 5 ans** qui s'applique au contrat C20077.

**Réponse isolée**

> Je ne dispose pas du contrat C20077 dans les documents fournis, donc je ne peux pas répondre spécifiquement pour ce contrat.
> 
> Cependant, voici ce que les documents disponibles indiquent sur le délai de prescription pour les actions en incapacité de travail :
> 
> - **Règlement général PrevCorp** : le délai de prescription est de **2 ans** à compter de l'événement qui lui donne naissance, sans dérogation spécifique pour l'incapacité de travail. [REGLEMENT_prevcorp.pdf]
> 
> - **Notice CCN Transport Routier (IDCC 16)** : par dérogation expresse, *« le délai de prescription applicable à une action relative à la garantie incapacité de travail est porté à **5 ans** »*. [NOTICE_CCN_transport_routier.pdf]
> 
> **En pratique**, pour déterminer le délai applicable au contrat C20077, il faut identifier la convention collective ou la notice d'information rattachée à ce contrat :
> - Si ce contrat relève de la **CCN Transport Routier** → **5 ans**
> - Si aucune dérogation spécifique n'est prévue → **2 ans** (règle générale)
> 
> Merci de vérifier le résumé des garanties ou la notice propre au contrat C20077.

Points en échec (isolé) : ['O0']

Chunks e2e récupérés :

1. `NOTICE_CCN_transport_routier` #6 (score 0.4822) — action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré. Par dérogation, et compte tenu des spécificités du secteur du transport rout…
2. `RESUME_C20077` #3 (score 0.4691) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
3. `RESUME_C20077` #4 (score 0.4647) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'appr…
4. `RESUME_C20077` #5 (score 0.4443) — cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assu…
5. `RESUME_C20077` #0 (score 0.4344) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 120 % | 120 % Marié ou pacsé sans personne à charge | 150 % | 150 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…
6. `RESUME_C20077` #2 (score 0.4322) — décès Garantie Tranche A Tranche B Invalidité absolue et définitive (anticipation du capital décès) 100 % 100 % Décès accidentel (capital additionnel) 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % Obsèques (capital forfaitaire) 2 000 € 2 000 € Rente éducation Lorsq…
7. `RESUME_C20077` #1 (score 0.4139) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…
8. `FAQ_prevcorp` #5 (score 0.4054) — dans la limite de 12 mois, sans cotisation supplémentaire à votre charge. 6. Divers Je suis salarié du contrat C20077 et je me trouve en arrêt de travail : quelles démarches dois- je effectuer pour percevoir mes indemnités journalières complémentaires ? Vous devez transmettre votre avis d'arrêt de t…
9. `NOTICE_CCN_sante_action_sociale` #6 (score 0.4035) — 10 — Prescription Toute action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré. Article 11 — Fausse déclaration Toute réticence ou f…
10. `NOTICE_CCN_metallurgie_distracteur` #6 (score 0.395) — l'évolution du point de référence défini par l'assureur, dans la limite de l'évolution des salaires de la branche. Article 9 — Litiges-réclamations 9.1 Toute réclamation doit être adressée par écrit au service réclamations de l'assureur, qui en accuse réception sous 10 jours ouvrés et apporte une ré…
11. `NOTICE_CCN_metallurgie` #6 (score 0.3944) — l'évolution du point de référence défini par l'assureur, dans la limite de l'évolution des salaires de la branche. Article 9 — Litiges-réclamations 9.1 Toute réclamation doit être adressée par écrit au service réclamations de l'assureur, qui en accuse réception sous 10 jours ouvrés et apporte une ré…
12. `RESUME_C87656` #2 (score 0.3848) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
13. `FAQ_prevcorp` #4 (score 0.3779) — la vie. Qui détermine ma catégorie d'invalidité ? La catégorie est déterminée par le médecin conseil de la Sécurité sociale. Elle vous est notifiée par la caisse primaire d'assurance maladie, puis communiquée à l'assureur lors de l'ouverture de votre dossier d'invalidité. Décès Puis-je choisir libre…
14. `NOTICE_CCN_agriculture` #6 (score 0.3776) — l'évolution des salaires de la branche. Article 9 — Litiges-réclamations 9.1 Toute réclamation doit être adressée par écrit au service réclamations de l'assureur, qui en accuse réception sous 10 jours ouvrés et apporte une réponse sous 2 mois. 9.2 À défaut de solution satisfaisante, vous pouvez sais…
15. `NOTICE_CCN_sante_action_sociale` #5 (score 0.3749) — des cotisations. Article 7 — Base des garanties Les prestations sont calculées sur le salaire brut de référence, réparti entre la tranche A (jusqu'au plafond annuel de la Sécurité sociale) et la tranche B (au-delà de ce plafond). Article 8 — Revalorisation des prestations Les prestations en cours de…
16. `RESUME_C39949` #4 (score 0.3729) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sé…
17. `RESUME_C87656` #3 (score 0.3652) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
18. `RESUME_C83792` #4 (score 0.3648) — | 28 % Invalidité 2e catégorie | 48 % | 48 % | 38 % Invalidité 3e catégorie | 72 % | 72 % | 57 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5,5 % De 12 à 17 ans 8 % De 18 à 25 ans (études ou apprentissage) 11 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par l…
19. `RESUME_C73736` #3 (score 0.3626) — décès) Décès accidentel (capital additionnel) 100 % 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % 100 % Obsèques (capital forfaitaire) 2 200 € 2 200 € 2 200 € Âge de l'enfant | Taux annuel Jusqu'à 11 ans | 6 % De 12 à 17 ans | 9 % De 18 à 25 ans (études ou apprenti…
20. `NOTICE_CCN_transport_routier` #5 (score 0.3554) — — Base des garanties Les prestations sont calculées sur le salaire brut de référence, réparti entre la tranche A (jusqu'au plafond annuel de la Sécurité sociale) et la tranche B (au-delà de ce plafond). Article 8 — Revalorisation des prestations Les prestations en cours de service sont revalorisées …
