# Rapport d'éval RAG

- Date : 2026-10-08T17:20:51
- Hash du YAML : ae7aed3dcc6a
- Modèle : claude-sonnet-4-6
- Modèle du juge : claude-sonnet-4-6
- Temperature : 0.0
- k : 5
- Variante d'ingestion : prefix (vérifiée contre la collection)
- Contexte isolé : document entier

## Synthèse

Questions : 25 dont 0 en erreur d'I/O (exclues des scores et des dénominateurs ci-dessous).

| Type | R (retrieval) | E (end-to-end) | I (isolé) |
|---|---|---|---|
| **Tous** | 13/23 | 18/25 | 22/25 |
| fait_simple | 4/5 | 4/5 | 5/5 |
| chiffre_precis | 5/5 | 5/5 | 5/5 |
| croisement | 4/13 | 7/13 | 10/13 |
| sans_reponse | N/A | 2/2 | 2/2 |

### Répartition des diagnostics

| Diagnostic | Famille | Nb |
|---|---|---|
| sain | succès | 15 |
| échec de retrieval | échec | 4 |
| succès sans la source attendue | suspect | 3 |
| double échec | échec | 3 |

## Détail par question

### RC01 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Franchise ITT — Contrat C87656
> 
> Le délai de franchise de la garantie Incapacité Temporaire de Travail du contrat C87656 est de **90 jours**.
> 
> La franchise court à compter du **premier jour d'arrêt de travail continu** et s'apprécie **par sinistre**, sauf rechute constatée dans les conditions prévues au contrat. [RESUME_C87656.pdf]
> 
> > ⚠️ À noter : un **délai de carence de 3 mois** s'applique également avant la prise d'effet de la garantie. [RESUME_C87656.pdf]

**Réponse isolée**

> ## Délai de franchise — Incapacité Temporaire de Travail
> 
> La franchise contractuelle de la garantie Incapacité Temporaire de Travail est de **90 jours**.
> 
> Elle court à compter du **premier jour d'arrêt de travail continu** et s'apprécie **par sinistre**, sauf rechute constatée dans les conditions prévues au contrat.
> 
> > ⚠️ Un **délai de carence de 3 mois** s'applique également avant la prise d'effet de la garantie.
> 
> [RESUME_C87656.pdf]


Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.6213) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `RESUME_C87656` #3 (score 0.5271) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
3. `NOTICE_CCN_metallurgie_distracteur` #9 (score 0.5227) — travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Mo…
4. `RESUME_C83792` #4 (score 0.5119) — | 28 % Invalidité 2e catégorie | 48 % | 48 % | 38 % Invalidité 3e catégorie | 72 % | 72 % | 57 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5,5 % De 12 à 17 ans 8 % De 18 à 25 ans (études ou apprentissage) 11 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par l…
5. `RESUME_C73736` #4 (score 0.5077) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …

### RC02 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : succès sans la source attendue (suspect) — à corriger : audit manuel

**Réponse e2e**

> Oui, le contrat C87656 prévoit un délai de carence avant la prise d'effet de la garantie ITT.
> 
> **Délai de carence : 3 mois** avant la prise d'effet de la garantie. [RESUME_C87656.pdf]
> 
> Par ailleurs, ce même contrat prévoit également une **franchise contractuelle de 90 jours** à l'issue de laquelle les indemnités journalières complémentaires sont versées. [RESUME_C87656.pdf]
> 
> Ces deux mécanismes sont distincts : le délai de carence conditionne l'ouverture du droit à la garantie, tandis que la franchise détermine le point de départ du versement des indemnités une fois la garantie acquise.

**Réponse isolée**

> Oui, le contrat C87656 prévoit un délai de carence pour la garantie ITT.
> 
> **Durée : 3 mois**
> 
> > *"Un délai de carence de 3 mois s'applique avant la prise d'effet de la garantie."* [RESUME_C87656.pdf]
> 
> À noter que ce délai de carence se distingue de la **franchise contractuelle de 90 jours**, qui, elle, s'applique par sinistre à compter du premier jour d'arrêt de travail continu. Les deux mécanismes coexistent dans le contrat. [RESUME_C87656.pdf]


Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.5318) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `NOTICE_CCN_sante_action_sociale` #7 (score 0.4225) — un capital, dont le montant varie selon la situation de famille du salarié. Montant des prestations. Le montant du capital, exprimé en pourcentage du salaire de référence par tranche, ainsi que les éventuelles majorations familiales, figurent dans le résumé des garanties propre à chaque contrat. Mod…
3. `RESUME_C87656` #3 (score 0.422) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
4. `NOTICE_CCN_agriculture` #8 (score 0.4171) — des garanties prévue à l'article 3.3. Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions …
5. `NOTICE_CCN_metallurgie_distracteur` #9 (score 0.4107) — travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Mo…

### RC03 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les documents fournis concernent le contrat **C73736** [RESUME_C73736.pdf] et non le contrat **C87656**. Il m'est donc impossible de me prononcer sur la clause bénéficiaire type de ce contrat spécifique.
> 
> ---
> 
> **À titre informatif**, les règles varient selon la convention collective applicable :
> 
> - **CCN Métallurgie** : la clause bénéficiaire type ne mentionne pas le concubin — seuls le conjoint ou partenaire de PACS sont visés en priorité. [NOTICE_CCN_metallurgie.pdf]
> - **CCN Santé/Action sociale** : le concubin est inclus dans la clause type, **sous condition de résidence commune** avec l'assuré au jour du décès. [NOTICE_CCN_sante_action_sociale.pdf]
> - **CCN Transport routier** : le concubin n'est pas reconnu comme bénéficiaire dans le cadre de la convention. [NOTICE_CCN_transport_routier.pdf]
> 
> Pour obtenir une réponse précise sur le contrat C87656, il convient de consulter le résumé ou la notice contractuelle correspondante.

**Réponse isolée**

> Je ne dispose pas du contrat C87656 dans les documents fournis. Cependant, je peux vous indiquer ce que prévoient les documents disponibles sur ce point, selon le type de contrat applicable :
> 
> **Règlement général PrevCorp :**
> La clause bénéficiaire type ne mentionne **pas le concubin**. Elle prévoit uniquement : le conjoint marié non séparé de corps ou le partenaire de PACS, puis les enfants, les parents, les autres ascendants, et enfin les héritiers. [REGLEMENT_prevcorp.pdf]
> 
> **Notice CCN Santé et Action Sociale (IDCC 413) :**
> La clause bénéficiaire type **inclut explicitement le concubin**, sous condition de résidence commune avec l'assuré au jour du décès, au même rang que le conjoint et le partenaire de PACS. [NOTICE_CCN_sante_action_sociale.pdf]
> 
> ---
> 
> **Conclusion :** La réponse dépend du contrat applicable à l'entreprise souscriptrice du contrat C87656. Si cet établissement relève de la CCN Santé et Action Sociale, le concubin est inclus (sous condition de résidence commune). Dans le cadre du règlement général, il ne l'est pas.
> 
> Pour une réponse certaine, il faudrait consulter le **résumé des garanties propre au contrat C87656**.

Points en échec (e2e) : ['O1']

Chunks e2e récupérés :

1. `NOTICE_CCN_transport_routier` #11 (score 0.4262) — Arrêt de travail initial et prolongations Oui Non Décomptes d'indemnités journalières de la Sécurité sociale Oui Non Acte de décès Non Oui Livret de famille ou extrait d'acte de naissance Non Oui Relevé d'identité bancaire du bénéficiaire Oui Oui Annexe II — Adhésion au régime Le bulletin d'adhésion…
2. `NOTICE_CCN_metallurgie` #12 (score 0.4235) — Terme de la garantie. Le versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint d…
3. `RESUME_C73736` #2 (score 0.4089) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
4. `NOTICE_CCN_sante_action_sociale` #10 (score 0.3976) — en une seule fois sur présentation de la facture acquittée par la personne ayant engagé les frais. Terme de la garantie. Le versement de la rente de conjoint cesse au décès du bénéficiaire. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation parti…
5. `NOTICE_CCN_metallurgie_distracteur` #12 (score 0.3832) — versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire personnalisée Le régime applicable aux entreprises relevant de la présente convention collective repose sur un…

### RC04 (sans_reponse)

- retrieval : N/A
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis du contrat C39949 mentionnent uniquement une **prestation d'assistance** (soutien psychologique, aide à domicile, conseil juridique) incluse sans supplément de cotisation [RESUME_C39949.pdf], mais ne précisent pas si le rapatriement à l'étranger en fait partie. Les détails complets seraient dans le **contrat d'assistance annexé**, qui n'est pas disponible dans les extraits fournis.

**Réponse isolée**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis mentionnent bien une **prestation d'assistance** (soutien psychologique, aide à domicile, conseil juridique) incluse sans supplément de cotisation [RESUME_C39949.pdf], mais le détail des services couverts — notamment un éventuel rapatriement à l'étranger — n'est pas précisé dans ces extraits. Il est indiqué que les conditions complètes figurent dans le **contrat d'assistance annexé**, auquel il conviendrait de se référer.


Chunks e2e récupérés :

1. `RESUME_C39949` #5 (score 0.3988) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assureur lors de l'ouverture du dossier. Catégorie Tranche A Tranche B Tranche C Invalidité 1re catégorie 35 % 35 % 25 % Invalidité 2e catégorie 45 % 45 % 35 % Invalidité 3e catégorie 70 %
2. `NOTICE_CCN_metallurgie_distracteur` #13 (score 0.3955) — | DÉCÈS | RENTE ÉDUCATION | RENTE CONJOINT Bulletins de salaire des douze derniers mois | Oui | Oui | Oui | Oui Arrêt de travail initial et prolongations | Oui | Non | Non | Non Décomptes d'indemnités journalières de la Sécurité sociale | Oui | Non | Non | Non Acte de décès | Non | Oui | Oui | Oui Livret de famille ou extrait d'acte de naissance | Non | Oui | Oui | Non Certificat de scolarité ou contrat d'apprentissage | Non | Non | Oui | Non Relevé d'identité bancaire du bénéficiaire | Oui | Oui | Oui | Oui Exclusions Exclusions applicables à toutes les garanties Sont exclus les sinistres résultant : de la guerre civile ou étrangère ; de la participation active de l'assuré à une émeute ou à un acte de terrorisme ; des effets directs ou indirects d'une explosion nucléaire
3. `NOTICE_CCN_metallurgie` #14 (score 0.3919) — | Oui | Non Certificat de scolarité ou contrat d'apprentissage | Non | Non | Oui | Non Relevé d'identité bancaire du bénéficiaire | Oui | Oui | Oui | Oui Exclusions Exclusions applicables à toutes les garanties Sont exclus les sinistres résultant : de la guerre civile ou étrangère ; de la participation active de l'assuré à une émeute ou à un acte de terrorisme ; des effets directs ou indirects d'une explosion nucléaire ; d'une faute intentionnelle de l'assuré ; de la pratique d'un sport à titre professionnel. Exclusions applicables au risque décès Est exclu le décès résultant du suicide de l'assuré au cours de la première année suivant son adhésion. Est également exclu le bénéficiaire qui a volontairement donné la mort à l'assuré ; le capital est alors attribué aux autres bénéficiaires. Exclusions applicables aux garanties accident et incapacité Sont exclus les sinistres survenus alors que l'assuré
4. `RESUME_C39949` #4 (score 0.3758) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale au-delà de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise est une franchise continue et court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation
5. `RESUME_C39949` #6 (score 0.3738) — 35 % 35 % 25 % Invalidité 2e catégorie 45 % 45 % 35 % Invalidité 3e catégorie 70 % 70 % 55 % Assistance Une prestation d'assistance (soutien psychologique, aide à domicile, conseil juridique) est incluse sans supplément de cotisation, dans les conditions fixées par le contrat d'assistance annexé. Catégorie de personnel | Tranche A | Tranche B | Tranche C Non cadre | 1,20 % | 1,85 % | 1,85 % Cotisations Catégorie de personnel Tranche A Tranche B Tranche C Non cadre 1,20 % 1,85 % 1,85 %

### RC05 (croisement)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Analyse comparative : Garantie ITT — Contrat C39949 vs Notice CCN Agriculture
> 
> ### Point de divergence identifié : la durée de franchise
> 
> | | Notice CCN Agriculture | Résumé C39949 |
> |---|---|---|
> | **Durée de franchise** | **90 jours** | **60 jours** |
> | **Type de franchise** | Continue | Continue |
> | **Point de départ** | 1er jour d'arrêt | 1er jour d'arrêt |
> 
> **Il existe bien un écart significatif** entre les deux documents :
> 
> - La Notice CCN Agriculture fixe la franchise ITT à **90 jours** : *"La franchise applicable à la garantie ITT est fixée à 90 jours"* [NOTICE_CCN_agriculture.pdf]
> 
> - Le Résumé des garanties du contrat C39949 prévoit une franchise de **60 jours** : *"À l'issue de la franchise de 60 jours"* [RESUME_C39949.pdf]
> 
> ### Interprétation
> 
> Cet écart est vraisemblablement **intentionnel** : la Notice CCN Agriculture précise elle-même que *"le taux de l'indemnité journalière complémentaire, par tranche, figure dans le résumé des garanties propre à chaque contrat"* [NOTICE_CCN_agriculture.pdf], laissant ainsi une marge de personnalisation contractuelle.
> 
> Le contrat C39949 offre donc une **franchise plus courte (60 jours vs 90 jours)**, ce qui constitue une condition **plus favorable** pour l'assuré par rapport au régime de base de la convention.
> 
> > ⚠️ Il est recommandé de vérifier si cette dérogation à la franchise de base est bien conforme aux conditions de souscription du contrat.

**Réponse isolée**

> ## Analyse comparative : Garantie ITT
> 
> Oui, il existe **un écart significatif** entre les deux documents sur la durée de la franchise ITT.
> 
> ---
> 
> ### 🔴 Point de divergence : la franchise
> 
> | | Résumé C39949 | Notice CCN Agriculture |
> |---|---|---|
> | **Durée de la franchise** | **60 jours** | **90 jours** |
> | **Modalité** | Continue | Continue |
> 
> - [RESUME_C39949.pdf] : *"À l'issue de la franchise de 60 jours"*
> - [NOTICE_CCN_agriculture.pdf] : *"La franchise applicable à la garantie ITT est fixée à 90 jours"* (Article 14)
> 
> ---
> 
> ### ✅ Points concordants
> 
> - Les deux documents confirment que la franchise est **continue** (court sans interruption dès le 1er jour d'arrêt). [RESUME_C39949.pdf] [NOTICE_CCN_agriculture.pdf]
> - Les taux d'indemnisation sont cohérents : **70 % / 65 % / 60 %** selon les tranches A, B, C. [RESUME_C39949.pdf]
> - Les modalités de versement (mensuel à terme échu) sont identiques. [RESUME_C39949.pdf] [NOTICE_CCN_agriculture.pdf]
> 
> ---
> 
> ### ⚠️ Conclusion
> 
> Cet écart sur la franchise (60 vs 90 jours) est un point de vigilance important. En cas de litige, la Notice précise à l'Article 14 que *"le régime de base de la convention ne prévoit aucune dérogation à cette modalité"*, ce qui suggère que la franchise de **90 jours prévue par la Notice ferait foi**. Une vérification auprès de PrevCorp est recommandée pour clarifier quelle version s'applique contractuellement.


Chunks e2e récupérés :

1. `NOTICE_CCN_agriculture` #8 (score 0.5064) — des garanties prévue à l'article 3.3. Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions …
2. `RESUME_C39949` #5 (score 0.437) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidatio…
3. `RESUME_C39949` #4 (score 0.432) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sé…
4. `NOTICE_CCN_agriculture` #11 (score 0.4308) — montants correspondants, figurent dans le résumé des garanties propre à chaque contrat. Modalités de versement. Les modalités de versement sont identiques à celles de la garantie de base à laquelle l'option se rattache. Terme de la garantie. Le versement cesse dans les mêmes conditions que la garant…
5. `NOTICE_CCN_sante_action_sociale` #7 (score 0.426) — un capital, dont le montant varie selon la situation de famille du salarié. Montant des prestations. Le montant du capital, exprimé en pourcentage du salaire de référence par tranche, ainsi que les éventuelles majorations familiales, figurent dans le résumé des garanties propre à chaque contrat. Mod…

### RC06 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : succès sans la source attendue (suspect) — à corriger : audit manuel

**Réponse e2e**

> ## Taux de couverture invalidité — Contrat C39949
> 
> Voici les taux de rente versés en pourcentage du **salaire annuel brut de référence**, selon la catégorie d'invalidité et la tranche de salaire :
> 
> | Catégorie d'invalidité | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | **1re catégorie** | 35 % | 35 % | 25 % |
> | **2e catégorie** | 45 % | 45 % | 35 % |
> | **3e catégorie** | 70 % | 70 % | 55 % |
> 
> [RESUME_C39949.pdf]
> 
> > 💡 **Rappel de fonctionnement** : La catégorie d'invalidité est déterminée par le médecin conseil de la Sécurité sociale, notifiée à l'assuré par la CPAM, puis communiquée à l'assureur lors de l'ouverture du dossier.

**Réponse isolée**

> ## Taux de couverture invalidité — Contrat C39949
> 
> Voici les taux de rente complémentaire versée par l'assureur, exprimés en **pourcentage du salaire annuel brut de référence**, selon la catégorie d'invalidité et la tranche de rémunération :
> 
> | Catégorie d'invalidité | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | **1re catégorie** (peut exercer une activité rémunérée) | 35 % | 35 % | 25 % |
> | **2e catégorie** (incapable d'exercer toute profession) | 45 % | 45 % | 35 % |
> | **3e catégorie** (incapable d'exercer + besoin d'assistance tierce personne) | 70 % | 70 % | 55 % |
> 
> [RESUME_C39949.pdf]
> 
> > **Rappel important** : ces rentes sont versées **sous déduction des prestations de la Sécurité sociale**. La catégorie d'invalidité est déterminée par le médecin conseil de la CPAM et communiquée à l'assureur lors de l'ouverture du dossier. [RESUME_C39949.pdf] [REGLEMENT_prevcorp.pdf]


Chunks e2e récupérés :

1. `RESUME_C39949` #5 (score 0.5729) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidatio…
2. `RESUME_C39949` #6 (score 0.57) — 35 % 35 % 25 % Invalidité 2e catégorie 45 % 45 % 35 % Invalidité 3e catégorie 70 % 70 % 55 % Assistance Une prestation d'assistance (soutien psychologique, aide à domicile, conseil juridique) est incluse sans supplément de cotisation, dans les conditions fixées par le contrat d'assistance annexé. Ca…
3. `RESUME_C39949` #4 (score 0.562) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sé…
4. `RESUME_C83792` #5 (score 0.5189) — la franchise de 90 jours 78 % 72 % 66 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquida…
5. `RESUME_C73736` #6 (score 0.5187) — primaire d'assurance maladie et communiquée à l'assureur lors de l'ouverture du dossier. Catégorie Tranche A Tranche B Tranche C Invalidité 1re catégorie 40 % 40 % 30 % Invalidité 2e catégorie 50 % 50 % 40 % Invalidité 3e catégorie 75 % 75 % 60 % Assistance Une prestation d'assistance (soutien psych…

### RC07 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : succès sans la source attendue (suspect) — à corriger : audit manuel

**Réponse e2e**

> ## Contrat C87656 — Incapacité Temporaire de Travail
> 
> ### Taux de couverture
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise contractuelle de 90 jours | **82 %** | **78 %** |
> 
> ### Franchise
> 
> - **Durée : 90 jours** (franchise contractuelle)
> - La franchise court à compter du **premier jour d'arrêt de travail continu** et s'apprécie **par sinistre**, sauf rechute constatée dans les conditions prévues au contrat.
> - Un **délai de carence de 3 mois** s'applique avant la prise d'effet de la garantie.
> 
> ### Modalités de versement
> 
> Les indemnités sont versées **mensuellement à terme échu**, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité ou au décès de l'assuré.
> 
> [RESUME_C87656.pdf]

**Réponse isolée**

> ## Incapacité Temporaire de Travail — Contrat n° C87656
> 
> ### Taux de couverture
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise contractuelle de 90 jours | **82 %** | **78 %** |
> 
> Les taux sont exprimés en pourcentage du salaire annuel brut de référence, **sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement**. [RESUME_C87656.pdf]
> 
> ---
> 
> ### Franchise
> 
> - **Durée : 90 jours** de franchise contractuelle [RESUME_C87656.pdf]
> - **Modalité : franchise continue**, courant à compter du **premier jour d'arrêt de travail continu**, appréciée par sinistre (sauf rechute dans les conditions prévues au contrat) [RESUME_C87656.pdf]
> 
> > ⚠️ Un **délai de carence de 3 mois** s'applique avant la prise d'effet de la garantie. [RESUME_C87656.pdf]
> 
> ---
> 
> ### Terme du versement
> 
> Les indemnités cessent à la **reprise du travail**, à la **liquidation d'une pension d'invalidité**, au **décès** de l'assuré ou à son **départ à la retraite** — et en tout état de cause au **1 095e jour d'arrêt** selon le règlement général. [RESUME_C87656.pdf] [REGLEMENT_prevcorp.pdf]


Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.59) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `RESUME_C83792` #4 (score 0.5213) — | 28 % Invalidité 2e catégorie | 48 % | 48 % | 38 % Invalidité 3e catégorie | 72 % | 72 % | 57 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5,5 % De 12 à 17 ans 8 % De 18 à 25 ans (études ou apprentissage) 11 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par l…
3. `RESUME_C87656` #3 (score 0.5195) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
4. `RESUME_C73736` #4 (score 0.5164) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …
5. `RESUME_C39949` #4 (score 0.4924) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sé…

### RC08 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

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

**Réponse isolée**

> ## Garanties décès — Contrat n° C83792
> 
> ### Capital décès toutes causes
> 
> Le capital versé aux bénéficiaires dépend de la situation de famille au jour du décès [RESUME_C83792.pdf] :
> 
> | Situation de famille | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | Célibataire, veuf, divorcé sans enfant à charge | 140 % | 140 % | 115 % |
> | Marié ou pacsé sans enfant à charge | 160 % | 160 % | 135 % |
> 
> ### Majorations par enfant à charge
> 
> Cumulable sans limitation de rang [RESUME_C83792.pdf] :
> 
> | Tranche A | Tranche B | Tranche C |
> |---|---|---|
> | + 28 % | + 28 % | + 18 % |
> 
> ### Autres garanties liées au décès
> 
> [RESUME_C83792.pdf] :
> 
> - **Invalidité absolue et définitive** (anticipation du capital décès) : 100 % sur toutes les tranches
> - **Décès accidentel** (capital additionnel) : 100 % sur toutes les tranches
> - **Double effet** (décès simultané ou postérieur du conjoint) : 100 % sur toutes les tranches
> - **Obsèques** (capital forfaitaire) : **1 900 €** sur toutes les tranches
> 
> ### Rente éducation
> 
> En cas de décès laissant des enfants à charge, une rente temporaire est versée jusqu'à la fin des études ou au plus tard au 26e anniversaire [RESUME_C83792.pdf] :
> 
> | Âge de l'enfant | Taux annuel |
> |---|---|
> | Jusqu'à 11 ans | 5,5 % |
> | De 12 à 17 ans | 8 % |
> | De 18 à 25 ans (études ou apprentissage) | 11 % |


Chunks e2e récupérés :

1. `RESUME_C83792` #0 (score 0.5068) — Situation de famille | Tranche A | Tranche B | Tranche C Célibataire, veuf, divorcé sans enfant à charge | 140 % | 140 % | 115 % Marié ou pacsé sans enfant à charge | 160 % | 160 % | 135 % Majoration par enfant à charge | Tranche A | Tranche B | Tranche C Capital décès toutes causes | + 28 % | + 28 …
2. `RESUME_C87656` #3 (score 0.5009) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
3. `RESUME_C83792` #1 (score 0.496) — % Obsèques (capital forfaitaire) | 1 900 € | 1 900 € | 1 900 € PREVCORP PRÉVOYANCE Résumé des garanties — Contrat n° C83792 Convention collective nationale de l'enseignement privé — Ensemble du personnel Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au t…
4. `RESUME_C83792` #2 (score 0.4937) — Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 140 % 140 % 115 % Marié ou pacsé sans enfant à charge 160 % 160 % 135 % Majorations familiales Le capital décès toutes causes fait l'objet d'une majoration par enfant à charge reconnu au jour du sinist…
5. `RESUME_C39949` #2 (score 0.4794) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 130 % 130 % 100 % Marié ou pacsé sans enfant à charge 150 % 150 % 110 % Majorations familiales Le capital décès toutes causes fait l'objet d'une majoration par enfant à charge reconnu au jour du sinistre, cumula…

### RC09 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

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

**Réponse isolée**

> **Oui**, une rente éducation est prévue sur le contrat C83792.
> 
> En cas de décès de l'assuré laissant un ou plusieurs enfants à charge (au sens de la convention collective), une **rente temporaire** leur est versée jusqu'à la fin de leurs études ou au plus tard à leur **26e anniversaire**, selon le barème suivant :
> 
> | Âge de l'enfant | Taux annuel |
> |---|---|
> | Jusqu'à 11 ans | 5,5 % |
> | De 12 à 17 ans | 8 % |
> | De 18 à 25 ans (études ou apprentissage) | 11 % |
> 
> Ces taux sont exprimés en pourcentage du salaire annuel brut de référence.
> 
> [RESUME_C83792.pdf]


Chunks e2e récupérés :

1. `RESUME_C83792` #3 (score 0.553) — 100 % 100 % Obsèques (capital forfaitaire) 1 900 € 1 900 € 1 900 € Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfan…
2. `RESUME_C83792` #5 (score 0.502) — la franchise de 90 jours 78 % 72 % 66 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquida…
3. `RESUME_C83792` #2 (score 0.4976) — Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 140 % 140 % 115 % Marié ou pacsé sans enfant à charge 160 % 160 % 135 % Majorations familiales Le capital décès toutes causes fait l'objet d'une majoration par enfant à charge reconnu au jour du sinist…
4. `RESUME_C39949` #3 (score 0.4929) — % 100 % Obsèques (capital forfaitaire) 1 800 € 1 800 € 1 800 € Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant | …
5. `RESUME_C73736` #4 (score 0.4921) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …

### RC10 (croisement)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Garanties optionnelles du contrat C87656
> 
> Oui, plusieurs garanties optionnelles sont disponibles. Selon le règlement général, les options possibles incluent notamment :
> 
> - Rente éducation
> - Garantie double effet
> - Garantie obsèques
> - Garantie dépendance totale
> - Indemnisation surcomplémentaire de l'incapacité temporaire de travail au-delà de la tranche B
> 
> [REGLEMENT_prevcorp.pdf]
> 
> ---
> 
> Sur le contrat C87656 spécifiquement, les garanties optionnelles **effectivement souscrites** sont :
> 
> - **Rente de conjoint** : en cas de décès de l'assuré, une rente viagère est versée à son conjoint ou partenaire de PACS, à hauteur de **15 % du salaire annuel brut de référence** (Tranche A et Tranche B)
> - **Garantie obsèques** : capital forfaitaire de **2 500 €**
> 
> [RESUME_C87656.pdf]
> 
> > ⚠️ Les conditions détaillées de chaque garantie optionnelle souscrite figurent dans le résumé des garanties propre au contrat. [REGLEMENT_prevcorp.pdf]

**Réponse isolée**

> ## Garanties optionnelles souscrites sur le contrat C87656
> 
> Oui, deux garanties optionnelles ont été souscrites sur ce contrat :
> 
> ### 1. Rente de conjoint
> Une rente viagère versée au conjoint ou partenaire de PACS survivant en cas de décès de l'assuré.
> 
> | Tranche A | Tranche B |
> |-----------|-----------|
> | 15 % | 15 % |
> 
> *(exprimée en pourcentage du salaire annuel brut de référence)*
> 
> [RESUME_C87656.pdf]
> 
> ### 2. Garantie obsèques
> Un capital forfaitaire versé à la personne ayant engagé les frais d'obsèques, sur présentation de la facture acquittée.
> 
> | Montant |
> |---------|
> | 2 500 € |
> 
> [RESUME_C87656.pdf]
> 
> ---
> 
> **À noter :** Le règlement général prévoit d'autres garanties optionnelles disponibles (rente éducation, garantie double effet, garantie dépendance totale, indemnisation surcomplémentaire ITT au-delà de la tranche B), mais celles-ci **ne figurent pas parmi les garanties souscrites** dans le résumé du contrat C87656. [REGLEMENT_prevcorp.pdf]


Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.4611) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `REGLEMENT_prevcorp` #12 (score 0.4379) — ; — rente éducation ; — garantie double effet ; — garantie obsèques ; — garantie dépendance totale ; — indemnisation surcomplémentaire de l'incapacité temporaire de travail au-delà de la tranche B. Les garanties optionnelles effectivement souscrites, ainsi que leurs conditions et montants, figurent …
3. `RESUME_C87656` #3 (score 0.4213) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
4. `RESUME_C87656` #4 (score 0.4205) — la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du sal…
5. `RESUME_C87656` #0 (score 0.406) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 180 % | 180 % Marié ou pacsé sans personne à charge | 220 % | 220 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…

### RC11 (croisement)

- retrieval : KO — documents manquants : ['NOTICE_CCN_metallurgie', 'REGLEMENT_prevcorp'] — points absents des chunks : ['O0', 'O1']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : double échec (échec) — à corriger : vérifier question et scorer (I), puis traiter R et E séparément

**Réponse e2e**

> ## Franchise ITT du contrat C73736 : continue ou discontinue ?
> 
> ### Ce que dit le contrat C73736
> 
> Le contrat C73736 prévoit une **franchise continue** :
> 
> > *"La franchise est une franchise continue et court sans interruption à compter du premier jour d'arrêt de travail."*
> > [RESUME_C73736.pdf]
> 
> La durée de cette franchise est de **90 jours**.
> 
> ---
> 
> ### Comparaison avec les régimes de référence
> 
> | Document | Type de franchise | Durée |
> |---|---|---|
> | RESUME_C73736.pdf | **Continue** | 90 jours |
> | NOTICE_CCN_agriculture.pdf | **Continue** (régime de base, sans dérogation) | 90 jours |
> | NOTICE_CCN_metallurgie_distracteur.pdf | **Discontinue** | 60 jours |
> 
> ---
> 
> ### Conclusion
> 
> La franchise **continue à 90 jours** du contrat C73736 **correspond au régime par défaut** tel que défini dans la CCN Agriculture [NOTICE_CCN_agriculture.pdf], qui précise explicitement qu'*"aucune dérogation"* n'est prévue à cette modalité.
> 
> À l'inverse, la notice métallurgie prévoit une franchise **discontinue** [NOTICE_CCN_metallurgie_distracteur.pdf], ce qui constituerait une dérogation par rapport au principe de franchise continue.
> 
> ⚠️ **Il ne s'agit donc pas d'une dérogation pour C73736**, mais bien d'une application conforme au régime standard de la CCN Agriculture.

**Réponse isolée**

> ## Franchise ITT – Contrat C73736
> 
> Je ne trouve pas cette information dans les documents disponibles.
> 
> **Le contrat C73736 n'est pas mentionné** dans les extraits fournis. Les documents disponibles sont :
> - Le **Règlement général PrevCorp** (`REGLEMENT_prevcorp.pdf`)
> - La **Notice CCN Métallurgie** (`NOTICE_CCN_metallurgie.pdf`)
> 
> ---
> 
> ## Ce que les documents indiquent en revanche :
> 
> **Sur le régime de franchise applicable à la CCN Métallurgie :**
> 
> La notice CCN Métallurgie précise explicitement que la franchise retenue est **continue** :
> > *« La franchise applicable à la présente garantie est une franchise continue au sens de l'article 14 du Règlement : le délai court sans interruption à compter du premier jour de l'arrêt de travail, quelle que soit la durée de celui-ci. Le régime de base de la convention ne prévoit aucune dérogation à cette modalité. »* [NOTICE_CCN_metallurgie.pdf]
> 
> **Sur le régime par défaut du Règlement général :**
> 
> Le Règlement général **ne fixe pas de modalité par défaut** : il décrit les deux modalités possibles (continue et discontinue) et renvoie à la notice ou au résumé des garanties propre à chaque contrat pour la modalité retenue. [REGLEMENT_prevcorp.pdf]
> 
> ---
> 
> **Pour connaître le régime applicable au contrat C73736**, il convient de consulter le **résumé des garanties propre à ce contrat**.

Points en échec (e2e) : ['O1']
Points en échec (isolé) : ['O0', 'O1']

Chunks e2e récupérés :

1. `RESUME_C73736` #5 (score 0.5333) — court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 90 jours 80 % 75 % 70 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de ma…
2. `RESUME_C73736` #4 (score 0.5316) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …
3. `NOTICE_CCN_metallurgie_distracteur` #9 (score 0.5133) — travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Mo…
4. `RESUME_C87656` #2 (score 0.5088) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
5. `NOTICE_CCN_agriculture` #8 (score 0.505) — des garanties prévue à l'article 3.3. Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions …

### RC12 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> D'après les documents disponibles, pour le contrat **C73736**, le taux de la rente invalidité **2e catégorie** sur la **Tranche B** est de :
> 
> ## **50 %** du salaire annuel brut de référence
> 
> [RESUME_C73736.pdf]

**Réponse isolée**

> Le taux de la rente invalidité 2e catégorie sur la tranche B est de **50 %** du salaire annuel brut de référence.
> 
> [RESUME_C73736.pdf]


Chunks e2e récupérés :

1. `RESUME_C73736` #5 (score 0.5783) — court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 90 jours 80 % 75 % 70 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de ma…
2. `RESUME_C73736` #4 (score 0.561) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …
3. `RESUME_C73736` #3 (score 0.5522) — décès) Décès accidentel (capital additionnel) 100 % 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % 100 % Obsèques (capital forfaitaire) 2 200 € 2 200 € 2 200 € Âge de l'enfant | Taux annuel Jusqu'à 11 ans | 6 % De 12 à 17 ans | 9 % De 18 à 25 ans (études ou apprenti…
4. `RESUME_C73736` #6 (score 0.5516) — primaire d'assurance maladie et communiquée à l'assureur lors de l'ouverture du dossier. Catégorie Tranche A Tranche B Tranche C Invalidité 1re catégorie 40 % 40 % 30 % Invalidité 2e catégorie 50 % 50 % 40 % Invalidité 3e catégorie 75 % 75 % 60 % Assistance Une prestation d'assistance (soutien psych…
5. `RESUME_C87656` #4 (score 0.5354) — la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du sal…

### RC13 (croisement)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Clause bénéficiaire applicable au contrat C73736
> 
> Le contrat C73736 applique la **clause bénéficiaire type**.
> 
> En effet, il est explicitement indiqué :
> 
> > *"Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit."* [RESUME_C73736.pdf]
> 
> ### Ordre de priorité de la clause type applicable
> 
> Conformément au Règlement PrevCorp, le capital décès est versé dans l'ordre suivant [REGLEMENT_prevcorp.pdf] :
> 
> 1. **Conjoint** non séparé de corps ou partenaire de PACS
> 2. À défaut, **enfants** nés ou à naître, par parts égales
> 3. À défaut, **parents**
> 4. À défaut, **autres ascendants**
> 5. À défaut, **héritiers**
> 
> > ⚠️ Il n'existe donc **aucune répartition personnalisée** à mentionner pour ce contrat. Si l'assuré souhaite désigner des bénéficiaires spécifiques avec une répartition sur mesure, il peut le faire à tout moment par écrit auprès de PrevCorp. [REGLEMENT_prevcorp.pdf]

**Réponse isolée**

> ## Clause bénéficiaire applicable au contrat C73736
> 
> Le contrat C73736 applique la **clause bénéficiaire type**.
> 
> En effet, le résumé des garanties indique explicitement :
> 
> > *"Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit."* [RESUME_C73736.pdf]
> 
> Conformément à la notice, cette clause type prévoit le versement du capital décès dans l'ordre de priorité suivant :
> 
> 1. Le conjoint (marié) ou partenaire de PACS, non séparé de corps
> 2. À défaut, les enfants nés ou à naître, par parts égales
> 3. À défaut, les parents
> 4. À défaut, les autres ascendants
> 5. À défaut, les héritiers
> 
> [NOTICE_CCN_metallurgie.pdf]
> 
> **Il n'existe donc aucune clause personnalisée déclarée** pour ce contrat, et aucune répartition individualisée n'est applicable.


Chunks e2e récupérés :

1. `RESUME_C73736` #2 (score 0.5823) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
2. `NOTICE_CCN_metallurgie` #12 (score 0.57) — Terme de la garantie. Le versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint d…
3. `NOTICE_CCN_sante_action_sociale` #11 (score 0.5608) — entre eux ; à défaut, à ses parents ; à défaut, à ses autres ascendants ; à défaut, à ses héritiers. Clause bénéficiaire personnalisée Vous pouvez désigner un ou plusieurs bénéficiaires de votre choix, par écrit, en précisant leur identité, leur rang de priorité et leur quote-part. Cette désignation…
4. `REGLEMENT_prevcorp` #12 (score 0.5559) — ; — rente éducation ; — garantie double effet ; — garantie obsèques ; — garantie dépendance totale ; — indemnisation surcomplémentaire de l'incapacité temporaire de travail au-delà de la tranche B. Les garanties optionnelles effectivement souscrites, ainsi que leurs conditions et montants, figurent …
5. `NOTICE_CCN_metallurgie_distracteur` #12 (score 0.5554) — versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire personnalisée Le régime applicable aux entreprises relevant de la présente convention collective repose sur un…

### RC14 (fait_simple)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Justificatif de qualité de concubin en cas de décès
> 
> Selon les documents PrevCorp, pour prouver la qualité de concubin dans le cadre d'une demande de prestation **décès-rente conjoint**, il faut fournir :
> 
> > **Une attestation de vie commune** ou, à défaut, **deux justificatifs de domicile commun de plus de deux ans**.
> 
> [REGLEMENT_prevcorp.pdf]
> 
> ---
> 
> ⚠️ **Point d'attention** : Cette exigence documentaire s'applique dans le cadre du règlement PrevCorp. En revanche, la convention collective nationale du transport routier **ne reconnaît pas la qualité de concubin** comme ouvrant droit aux garanties liées à la situation de famille — aucune rubrique n'est d'ailleurs prévue à cet effet dans le bulletin d'adhésion individuel.
> 
> [NOTICE_CCN_transport_routier.pdf]

**Réponse isolée**

> ## Justificatif de qualité de concubin en cas de décès
> 
> Pour prouver la qualité de concubin dans le cadre d'une demande de prestation décès, il faut fournir :
> 
> **Une attestation de vie commune**, ou à défaut, **deux justificatifs de domicile commun de plus de deux ans**.
> 
> [REGLEMENT_prevcorp.pdf - Extraits 16, 17 et 18]
> 
> > À noter : ce justificatif est requis uniquement pour la garantie **Décès/IAD**. Il n'est pas demandé pour les garanties Rente Éducation ou Rente Conjoint.


Chunks e2e récupérés :

1. `REGLEMENT_prevcorp` #15 (score 0.5613) — | RENTE CONJOINT Bulletins de salaire des douze derniers mois | Oui | Oui | Oui | Non | Non Arrêt de travail initial et prolongations | Oui | Non | Non | Non | Non Décomptes d'indemnités journalières ou de pension de la Sécurité sociale | Oui | Oui | Non | Non | Non Notification de taux d'invalidité…
2. `REGLEMENT_prevcorp` #16 (score 0.5326) — à défaut, deux justificatifs de domicile commun de plus de deux ans) | Non | Non | Oui | Non | Non Relevé d'identité bancaire du bénéficiaire | Oui | Oui | Oui | Oui | Oui Annexe I — Pièces justificatives Justificatif ITT IPP DÉCÈS- RENTE RENTE IAD ÉDUCATION CONJOINT Bulletins de salaire des douze d…
3. `NOTICE_CCN_transport_routier` #11 (score 0.5275) — Arrêt de travail initial et prolongations Oui Non Décomptes d'indemnités journalières de la Sécurité sociale Oui Non Acte de décès Non Oui Livret de famille ou extrait d'acte de naissance Non Oui Relevé d'identité bancaire du bénéficiaire Oui Oui Annexe II — Adhésion au régime Le bulletin d'adhésion…
4. `REGLEMENT_prevcorp` #17 (score 0.5254) — Oui Non d'apprentissage Justificatif de qualité de concubin Non Non Oui Non Non (attestation de vie commune ou, à défaut, deux justificatifs de domicile commun de plus de deux ans) Relevé d'identité bancaire du Oui Oui Oui Oui Oui bénéficiaire
5. `NOTICE_CCN_sante_action_sociale` #10 (score 0.433) — en une seule fois sur présentation de la facture acquittée par la personne ayant engagé les frais. Terme de la garantie. Le versement de la rente de conjoint cesse au décès du bénéficiaire. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation parti…

### RC15 (fait_simple)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Durée de la franchise en cas d'arrêt maladie ordinaire
> 
> La durée de la franchise est de **90 jours calendaires**, décomptés à partir du premier jour de l'arrêt de travail. [FAQ_prevcorp.pdf]
> 
> Cette franchise est de type **continu** : le délai court sans interruption à compter du premier jour de l'arrêt de travail, quelle que soit la durée de celui-ci. [NOTICE_CCN_metallurgie.pdf]
> 
> > ⚠️ **Point important** : Le jour de carence de la Sécurité sociale et la franchise contractuelle de 90 jours sont deux notions **distinctes** et indépendantes l'une de l'autre. [FAQ_prevcorp.pdf]
> 
> ---
> *À noter : un document distinct mentionne une franchise de 60 jours avec une modalité discontinue [NOTICE_CCN_metallurgie_distracteur.pdf], mais ce document semble correspondre à un contrat différent. La durée applicable à votre contrat est précisée dans votre notice d'information ou résumé des garanties.* [REGLEMENT_prevcorp.pdf]

**Réponse isolée**

> ## Franchise en cas d'arrêt maladie ordinaire
> 
> La franchise est de **90 jours calendaires**, décomptés à partir du **premier jour de l'arrêt de travail**. [FAQ_prevcorp.pdf]
> 
> > **Point important :** Le jour de carence de la Sécurité sociale est sans incidence sur ce délai. La franchise contractuelle de 90 jours démarre au premier jour de l'arrêt, que ce jour soit ou non pris en charge par la Sécurité sociale. [FAQ_prevcorp.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #2 (score 0.5862) — dans le temps ? Les taux de cotisation sont revus chaque année à l'occasion de la revalorisation du contrat. Toute évolution vous est communiquée par votre employeur, généralement en fin d'année pour une application au 1er janvier suivant. 4. Garanties Incapacité temporaire de travail Combien de tem…
2. `NOTICE_CCN_metallurgie_distracteur` #9 (score 0.5503) — travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Mo…
3. `NOTICE_CCN_metallurgie` #9 (score 0.5441) — travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Mo…
4. `REGLEMENT_prevcorp` #9 (score 0.5378) — franchise. Le délai de franchise peut être appliqué selon deux modalités : — franchise continue : le délai court sans interruption à compter du premier jour de l'arrêt de travail, quelle que soit la durée de celui-ci ; — franchise discontinue : les journées d'arrêt de travail liées au même sinistre …
5. `FAQ_prevcorp` #5 (score 0.5343) — dans la limite de 12 mois, sans cotisation supplémentaire à votre charge. 6. Divers Je suis salarié du contrat C20077 et je me trouve en arrêt de travail : quelles démarches dois- je effectuer pour percevoir mes indemnités journalières complémentaires ? Vous devez transmettre votre avis d'arrêt de t…

### RC16 (fait_simple)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> Non, la franchise de 90 jours n'est pas retardée par le jour de carence de la Sécurité sociale.
> 
> Ces deux notions sont **distinctes** : la franchise contractuelle de 90 jours démarre **au premier jour de l'arrêt de travail**, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. [FAQ_prevcorp.pdf]

**Réponse isolée**

> Non, la franchise de 90 jours n'est pas retardée par le jour de carence de la Sécurité sociale.
> 
> Ces deux notions sont distinctes : la franchise contractuelle de 90 jours démarre **dès le premier jour de l'arrêt de travail**, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. [FAQ_prevcorp.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #2 (score 0.5926) — dans le temps ? Les taux de cotisation sont revus chaque année à l'occasion de la revalorisation du contrat. Toute évolution vous est communiquée par votre employeur, généralement en fin d'année pour une application au 1er janvier suivant. 4. Garanties Incapacité temporaire de travail Combien de tem…
2. `FAQ_prevcorp` #3 (score 0.5644) — de la Sécurité sociale et la franchise contractuelle de 90 jours sont deux notions distinctes. La franchise contractuelle démarre au premier jour de l'arrêt de travail, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. Invalidité Quelles sont les catégori…
3. `REGLEMENT_prevcorp` #9 (score 0.4962) — franchise. Le délai de franchise peut être appliqué selon deux modalités : — franchise continue : le délai court sans interruption à compter du premier jour de l'arrêt de travail, quelle que soit la durée de celui-ci ; — franchise discontinue : les journées d'arrêt de travail liées au même sinistre …
4. `FAQ_prevcorp` #6 (score 0.4716) — Le versement des indemnités journalières complémentaires débute à l'issue de la franchise applicable à votre contrat, sur présentation des décomptes d'indemnités journalières de la Sécurité sociale ; le taux de versement applicable figure dans le résumé des garanties qui vous a été remis. Comment me…
5. `RESUME_C87656` #2 (score 0.4653) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…

### RC17 (sans_reponse)

- retrieval : N/A
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits du contrat **C73736** indiquent uniquement les taux de cotisation globaux par tranche :
> 
> | Catégorie | Tranche A | Tranche B | Tranche C |
> |-----------|-----------|-----------|-----------|
> | Cadre | 1,60 % | 2,45 % | 2,45 % |
> 
> [RESUME_C73736.pdf]
> 
> Cependant, **la ventilation de ces cotisations par garantie** (notamment la part spécifique à la rente de conjoint, ni la répartition salarié/employeur) **n'est pas détaillée dans les extraits disponibles**. Pour obtenir cette information précise, il conviendrait de consulter la notice d'information complète ou le tableau de répartition des cotisations du contrat C73736.

**Réponse isolée**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis du contrat C73736 mentionnent uniquement les taux de cotisation globaux par tranche pour la catégorie cadre [RESUME_C73736.pdf] :
> 
> | Catégorie | Tranche A | Tranche B | Tranche C |
> |-----------|-----------|-----------|-----------|
> | Cadre | 1,60 % | 2,45 % | 2,45 % |
> 
> Cependant, **aucune ventilation de ces cotisations** par garantie (notamment pour une éventuelle rente de conjoint) n'est présente dans les documents disponibles, et la garantie « rente de conjoint » n'est par ailleurs pas mentionnée parmi les garanties listées dans ces extraits.
> 
> Pour obtenir cette information, il conviendrait de consulter les **conditions particulières ou le tableau de cotisations détaillé** du contrat C73736.


Chunks e2e récupérés :

1. `RESUME_C87656` #5 (score 0.5491) — de conjoint En cas de décès de l'assuré, une rente viagère est versée à son conjoint ou partenaire de pacs survivant, sous réserve des conditions d'éligibilité définies par la notice d'information applicable au contrat. Garantie Tranche A Tranche B Rente de conjoint 15 % 15 % Garantie obsèques Un capital forfaitaire est versé à la personne ayant engagé les frais d'obsèques de l'assuré, sur présentation de la facture acquittée. Garantie Montant Obsèques (capital forfaitaire) 2 500 € Catégorie de personnel | Tranche A | Tranche B Cadre | 1,55 % | 2,40 % Cotisations Catégorie de personnel Tranche A Tranche B Cadre 1,55 % 2,40 %
2. `RESUME_C73736` #1 (score 0.5119) — % Obsèques (capital forfaitaire) | 2 200 € | 2 200 € | 2 200 € PREVCORP PRÉVOYANCE Résumé des garanties — Contrat n° C73736 Convention collective nationale de la métallurgie — Personnel cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence, par tranche de rémunération (tranche A jusqu'au plafond annuel de la Sécurité sociale, tranche B de 1 à 4 plafonds, tranche C de 4 à 8 plafonds). Garantie décès toutes causes En cas de décès de l'assuré, quelle qu'en soit la cause, un capital est versé aux bénéficiaires désignés. Son montant dépend de la situation de famille du salarié constatée au jour du décès. Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120
3. `RESUME_C73736` #2 (score 0.5042) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit. Majorations familiales Le capital décès toutes causes fait l'objet d'une majoration par enfant à charge reconnu au jour du sinistre, cumulable sans limitation de rang. Majoration par enfant à charge Tranche A Tranche B Tranche C Capital décès toutes causes + 30 % + 30 % + 20 % Autres garanties liées au décès Garantie Tranche Tranche Tranche A B C Invalidité absolue et définitive (anticipation du capital 100 % 100 % 100 % décès) Décès accidentel (capital additionnel) 100 % 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100
4. `RESUME_C73736` #4 (score 0.5035) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % De 12 à 17 ans 9 % De 18 à 25 ans (études ou apprentissage) 12 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale au-delà de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise est une franchise continue et court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue
5. `RESUME_C73736` #6 (score 0.4958) — primaire d'assurance maladie et communiquée à l'assureur lors de l'ouverture du dossier. Catégorie Tranche A Tranche B Tranche C Invalidité 1re catégorie 40 % 40 % 30 % Invalidité 2e catégorie 50 % 50 % 40 % Invalidité 3e catégorie 75 % 75 % 60 % Assistance Une prestation d'assistance (soutien psychologique, aide à domicile, conseil juridique) est incluse sans supplément de cotisation, dans les conditions fixées par le contrat d'assistance annexé. Catégorie de personnel | Tranche A | Tranche B | Tranche C Cadre | 1,60 % | 2,45 % | 2,45 % Cotisations Catégorie de personnel Tranche A Tranche B Tranche C Cadre 1,60 % 2,45 % 2,45 %

### RC18 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Capital décès — Salarié célibataire sans personne à charge | Contrat C20077
> 
> Pour un salarié célibataire, veuf ou divorcé sans personne à charge, le capital décès toutes causes s'élève à :
> 
> | Tranche A | Tranche B |
> |-----------|-----------|
> | **120 %** | **120 %** |
> 
> Ces taux sont exprimés en pourcentage du salaire annuel brut de référence. [RESUME_C20077.pdf]

**Réponse isolée**

> ## Capital décès toutes causes — Salarié célibataire sans personne à charge
> 
> Pour un salarié célibataire, veuf ou divorcé sans personne à charge, le capital décès toutes causes s'élève à :
> 
> | Tranche A | Tranche B |
> |-----------|-----------|
> | **120 %** du salaire annuel brut de référence | **120 %** du salaire annuel brut de référence |
> 
> > ⚠️ **À noter :** Si le salarié a des enfants à charge reconnus au jour du sinistre, une **majoration de 25 % par enfant** s'ajoute au capital de base, cumulable sans limitation de rang.
> 
> [RESUME_C20077.pdf]


Chunks e2e récupérés :

1. `RESUME_C20077` #1 (score 0.5873) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…
2. `RESUME_C73736` #1 (score 0.5587) — % Obsèques (capital forfaitaire) | 2 200 € | 2 200 € | 2 200 € PREVCORP PRÉVOYANCE Résumé des garanties — Contrat n° C73736 Convention collective nationale de la métallurgie — Personnel cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du cont…
3. `RESUME_C73736` #0 (score 0.537) — Situation de famille | Tranche A | Tranche B | Tranche C Célibataire, veuf, divorcé sans enfant à charge | 150 % | 150 % | 120 % Marié ou pacsé sans enfant à charge | 180 % | 180 % | 140 % Majoration par enfant à charge | Tranche A | Tranche B | Tranche C Capital décès toutes causes | + 30 % | + 30 …
4. `RESUME_C20077` #0 (score 0.5302) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 120 % | 120 % Marié ou pacsé sans personne à charge | 150 % | 150 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…
5. `RESUME_C87656` #1 (score 0.5255) — sociale, tranche B au-delà). Garanties de base Garantie décès toutes causes En cas de décès de l'assuré, quelle qu'en soit la cause, un capital est versé aux bénéficiaires désignés. Son montant dépend de la situation de famille du salarié constatée au jour du décès. Situation de famille Tranche A Tr…

### RC19 (croisement)

- retrieval : KO — documents manquants : ['NOTICE_CCN_transport_routier']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : double échec (échec) — à corriger : vérifier question et scorer (I), puis traiter R et E séparément

**Réponse e2e**

> ## Majoration de capital décès par enfant à charge — Contrat C20077
> 
> **Oui**, le contrat C20077 prévoit bien une majoration du capital décès par enfant à charge.
> 
> Le taux applicable est de **+25 % par enfant à charge**, avec les caractéristiques suivantes :
> 
> - **Cumulable sans limitation de rang** (applicable quel que soit le nombre d'enfants)
> - S'applique **quelle que soit la situation de famille** retenue
> - **Aucune condition d'ancienneté** de l'enfant dans le foyer n'est requise
> - La majoration s'ajoute au **capital de base**
> - L'enfant doit être **reconnu à charge au jour du sinistre**
> 
> [RESUME_C20077.pdf]
> 
> ---
> 
> > 💡 **À noter** : ce taux de 25 % diffère de celui du contrat C73736, qui prévoit une majoration de **+30 % en Tranches A et B** et **+20 % en Tranche C** [RESUME_C73736.pdf].

**Réponse isolée**

> Oui, le contrat C20077 prévoit une majoration du capital décès par enfant à charge.
> 
> **Taux : 25 % par enfant à charge**, reconnu au jour du sinistre. [RESUME_C20077.pdf]
> 
> Caractéristiques de cette majoration :
> - **Cumulable sans limitation de rang** (s'applique pour chaque enfant, quel que soit leur nombre)
> - S'applique **quelle que soit la situation de famille** retenue dans le tableau de base
> - Vient **s'ajouter au capital de base** sans condition d'ancienneté de l'enfant dans le foyer [RESUME_C20077.pdf]
> 
> À noter : la notice précise que la définition d'« enfant à charge » couvre les enfants de moins de 18 ans, ou de moins de 26 ans en cas de poursuite d'études ou d'apprentissage, fiscalement à charge de l'assuré. [NOTICE_CCN_transport_routier.pdf]

Points en échec (e2e) : ['O1', 'O2']
Points en échec (isolé) : ['O2']

Chunks e2e récupérés :

1. `RESUME_C20077` #3 (score 0.5808) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
2. `RESUME_C73736` #2 (score 0.5574) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
3. `RESUME_C20077` #2 (score 0.5405) — décès Garantie Tranche A Tranche B Invalidité absolue et définitive (anticipation du capital décès) 100 % 100 % Décès accidentel (capital additionnel) 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % Obsèques (capital forfaitaire) 2 000 € 2 000 € Rente éducation Lorsq…
4. `RESUME_C20077` #0 (score 0.5375) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 120 % | 120 % Marié ou pacsé sans personne à charge | 150 % | 150 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…
5. `RESUME_C73736` #0 (score 0.5113) — Situation de famille | Tranche A | Tranche B | Tranche C Célibataire, veuf, divorcé sans enfant à charge | 150 % | 150 % | 120 % Marié ou pacsé sans enfant à charge | 180 % | 180 % | 140 % Majoration par enfant à charge | Tranche A | Tranche B | Tranche C Capital décès toutes causes | + 30 % | + 30 …

### RC20 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp'] — points absents des chunks : ['O1']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles **ne permettent pas de répondre à cette question**.
> 
> Les extraits fournis indiquent uniquement le taux applicable :
> 
> > *« Invalidité 1re catégorie | 50 % | 50 % »* [RESUME_C20077.pdf]
> 
> pour les tranches A et B, sans préciser si ce taux de **50 %** constitue le taux de base du Règlement de prévoyance de la Convention collective nationale du transport routier ou s'il résulte d'une **dérogation** négociée.
> 
> Pour répondre à cette question, il faudrait disposer :
> - du **Règlement de prévoyance de la CCN Transport routier** (texte de référence),
> - et/ou des **conditions particulières** du contrat C20077 mentionnant explicitement une éventuelle dérogation.
> 
> Je ne trouve pas cette information dans les documents disponibles.

**Réponse isolée**

> ## Taux d'invalidité 1re catégorie — Contrat C20077
> 
> Le taux applicable au contrat C20077 pour l'invalidité 1re catégorie est de **50 % sur les tranches A et B**. [RESUME_C20077.pdf]
> 
> Ce taux correspond exactement au **taux de base** prévu par le Règlement général, qui stipule :
> 
> > *"la rente est exprimée en pourcentage du salaire brut de référence, à raison de **50 % pour la 1re catégorie**"* [REGLEMENT_prevcorp.pdf]
> 
> Il s'agit donc du **taux de base du Règlement**, sans dérogation. Le Règlement précise certes que *"le résumé des garanties propre à chaque contrat précise le taux effectivement applicable, qui peut différer de ce taux de base"* [REGLEMENT_prevcorp.pdf], mais en l'occurrence, le contrat C20077 n'a pas retenu de taux dérogatoire pour la 1re catégorie.
> 
> **En résumé :** pas de dérogation CCN sur ce point — le contrat C20077 applique strictement le taux de base réglementaire de 50 %.

Points en échec (e2e) : ['O1']

Chunks e2e récupérés :

1. `RESUME_C20077` #3 (score 0.5579) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
2. `RESUME_C20077` #5 (score 0.5328) — cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assu…
3. `RESUME_C20077` #4 (score 0.5203) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'appr…
4. `RESUME_C20077` #1 (score 0.4889) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…
5. `RESUME_C20077` #0 (score 0.4766) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 120 % | 120 % Marié ou pacsé sans personne à charge | 150 % | 150 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…

### RC21 (fait_simple)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

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
> La catégorie est **déterminée par le médecin conseil de la Sécurité sociale** et notifiée à l'assuré par la **caisse primaire d'assurance maladie (CPAM)**, qui la communique ensuite à l'assureur lors de l'ouverture du dossier.
> 
> [FAQ_prevcorp.pdf] [RESUME_C83792.pdf] [RESUME_C73736.pdf]

**Réponse isolée**

> ## Les 3 catégories d'invalidité chez PrevCorp
> 
> Les trois catégories d'invalidité retenues par le régime de prévoyance sont définies dans les mêmes termes que ceux de la Sécurité sociale [FAQ_prevcorp.pdf] :
> 
> | Catégorie | Définition |
> |-----------|------------|
> | **1re catégorie** | Invalides **capables d'exercer une activité rémunérée** |
> | **2e catégorie** | Invalides **absolument incapables d'exercer une profession quelconque** |
> | **3e catégorie** | Invalides absolument incapables d'exercer une profession quelconque **et dans l'obligation de recourir à l'assistance d'une tierce personne** pour accomplir les actes ordinaires de la vie |
> 
> ## Détermination de la catégorie
> 
> La catégorie est déterminée par le **médecin conseil de la Sécurité sociale**. Elle est ensuite **notifiée par la caisse primaire d'assurance maladie (CPAM)**, puis communiquée à l'assureur lors de l'ouverture du dossier d'invalidité. [FAQ_prevcorp.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #3 (score 0.5904) — de la Sécurité sociale et la franchise contractuelle de 90 jours sont deux notions distinctes. La franchise contractuelle démarre au premier jour de l'arrêt de travail, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. Invalidité Quelles sont les catégori…
2. `REGLEMENT_prevcorp` #10 (score 0.5143) — la garantie. Le versement cesse à la reprise du travail, au décès de l'assuré, à son départ en retraite ou au 1 095e jour d'arrêt. Article 15 — Invalidité Objet de la garantie. Lorsque l'assuré est reconnu invalide par la Sécurité sociale, l'assureur verse une rente complémentaire dont le montant dé…
3. `RESUME_C83792` #5 (score 0.5007) — la franchise de 90 jours 78 % 72 % 66 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquida…
4. `RESUME_C73736` #5 (score 0.4982) — court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 90 jours 80 % 75 % 70 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de ma…
5. `RESUME_C39949` #5 (score 0.497) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidatio…

### RC22 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : double échec (échec) — à corriger : vérifier question et scorer (I), puis traiter R et E séparément

**Réponse e2e**

> ## Délai de prescription — Incapacité de travail
> 
> Le délai de prescription applicable à une action relative à la **garantie incapacité de travail est de **5 ans****.
> 
> En effet, par dérogation au délai de droit commun de 2 ans, et **compte tenu des spécificités du secteur du transport routier**, ce délai est expressément porté à 5 ans. [NOTICE_CCN_transport_routier.pdf]
> 
> > À noter : le contrat C20077 relevant de la **Convention collective nationale du transport routier** [RESUME_C20077.pdf], cette dérogation de 5 ans lui est applicable.

**Réponse isolée**

> Je ne dispose pas du contrat C20077 dans les documents fournis, donc je ne peux pas répondre spécifiquement à cette référence contractuelle.
> 
> Cependant, je peux indiquer ce que prévoient les documents disponibles sur le délai de prescription en matière d'incapacité de travail :
> 
> - **Règlement général PrevCorp** : le délai de prescription est de **2 ans** à compter de l'événement qui lui donne naissance, sans dérogation spécifique pour l'incapacité de travail. [REGLEMENT_prevcorp.pdf]
> 
> - **Notice CCN Transport Routier (IDCC 16)** : par dérogation expresse, *« le délai de prescription applicable à une action relative à la garantie incapacité de travail est porté à **5 ans** »*. [NOTICE_CCN_transport_routier.pdf]
> 
> **En pratique**, le délai applicable dépend donc de la convention collective rattachée au contrat C20077 :
> - Si ce contrat relève de la **CCN Transport Routier**, le délai est de **5 ans**.
> - S'il relève du **régime général** sans notice spécifique dérogatoire, le délai est de **2 ans**.
> 
> Pour une réponse certaine, il convient de consulter la notice d'information ou le résumé des garanties propre au contrat C20077.

Points en échec (e2e) : ['O1']
Points en échec (isolé) : ['O0']

Chunks e2e récupérés :

1. `NOTICE_CCN_transport_routier` #6 (score 0.4822) — action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré. Par dérogation, et compte tenu des spécificités du secteur du transport rout…
2. `RESUME_C20077` #3 (score 0.4691) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
3. `RESUME_C20077` #4 (score 0.4647) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'appr…
4. `RESUME_C20077` #5 (score 0.4443) — cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assu…
5. `RESUME_C20077` #0 (score 0.4344) — Situation de famille | Tranche A | Tranche B Célibataire, veuf ou divorcé sans personne à charge | 120 % | 120 % Marié ou pacsé sans personne à charge | 150 % | 150 % Garantie | Tranche A | Tranche B Invalidité absolue et définitive (anticipation du capital décès) | 100 % | 100 % Décès accidentel (c…

### RC23 (croisement)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Démarches et taux des indemnités journalières — Contrat C20077
> 
> ### Démarches à effectuer
> 
> Le salarié doit suivre les étapes suivantes [FAQ_prevcorp.pdf] :
> 
> 1. **Transmettre l'avis d'arrêt de travail** (initial et prolongations) à son employeur **dans les 48 heures** suivant sa délivrance.
> 2. L'employeur adresse ensuite à l'assureur, **dans un délai de 8 jours**, une déclaration d'arrêt de travail accompagnée :
>    - d'une copie de l'avis médical,
>    - des bulletins de salaire des trois derniers mois.
> 3. Ce dossier peut être transmis **via le formulaire de l'espace adhérent en ligne** ou **par courrier** au service prestations (adresse sur la carte d'adhérent).
> 
> ---
> 
> ### Taux des indemnités journalières
> 
> Les indemnités sont versées **à l'issue de la franchise contractuelle**, déduction faite des prestations de la Sécurité sociale et de tout revenu de remplacement [RESUME_C20077.pdf] :
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise | **78 %** | **72 %** |
> 
> > ⚠️ Ces taux sont propres au contrat C20077 et diffèrent de ceux de la CCN Métallurgie (80 %/75 %/70 %) [NOTICE_CCN_metallurgie.pdf].
> 
> Les indemnités sont versées **mensuellement à terme échu**, au souscripteur (en cas de maintien de salaire) ou directement à l'assuré. Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès ou au départ à la retraite [RESUME_C20077.pdf].

**Réponse isolée**

> ## Démarches pour percevoir les indemnités journalières — Contrat C20077
> 
> ### 1. Démarches à effectuer
> 
> Le salarié doit :
> 
> 1. **Transmettre son avis d'arrêt de travail** (initial et prolongations) à son employeur **dans les 48 heures** suivant sa délivrance. [FAQ_prevcorp.pdf]
> 
> 2. L'employeur adresse ensuite à l'assureur, **dans un délai de 8 jours**, une déclaration d'arrêt de travail accompagnée :
>    - d'une copie de l'avis médical,
>    - des bulletins de salaire des trois derniers mois. [FAQ_prevcorp.pdf]
> 
> > La transmission peut se faire via **l'espace adhérent en ligne** (formulaire dédié) ou par **courrier au service prestations** (adresse sur la carte d'adhérent). [FAQ_prevcorp.pdf]
> 
> ---
> 
> ### 2. Conditions de versement
> 
> - Le versement débute **à l'issue de la franchise contractuelle de 90 jours** (jours calendaires à compter du 1er jour d'arrêt), sur présentation des **décomptes d'indemnités journalières de la Sécurité sociale**. [FAQ_prevcorp.pdf]
> - Les indemnités sont versées **mensuellement à terme échu**, au souscripteur (en cas de maintien de salaire) ou directement à l'assuré. [RESUME_C20077.pdf]
> 
> ---
> 
> ### 3. Taux applicable
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise contractuelle | **78 %** | **72 %** |
> 
> Ces taux sont exprimés en pourcentage du salaire annuel brut de référence, **sous déduction des prestations Sécurité sociale et de tout revenu de remplacement**. [RESUME_C20077.pdf]
> 
> ---
> 
> > ⚠️ Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès ou au départ à la retraite. [RESUME_C20077.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #5 (score 0.5733) — dans la limite de 12 mois, sans cotisation supplémentaire à votre charge. 6. Divers Je suis salarié du contrat C20077 et je me trouve en arrêt de travail : quelles démarches dois- je effectuer pour percevoir mes indemnités journalières complémentaires ? Vous devez transmettre votre avis d'arrêt de t…
2. `RESUME_C20077` #4 (score 0.5518) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'appr…
3. `RESUME_C20077` #3 (score 0.4834) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
4. `RESUME_C20077` #5 (score 0.4462) — cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assu…
5. `NOTICE_CCN_metallurgie` #9 (score 0.4335) — travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contrat. Mo…

### RC24 (croisement)

- retrieval : KO — points absents des chunks : ['O1']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles ne permettent pas de répondre précisément à cette question combinée.
> 
> Voici ce qui est documenté séparément :
> 
> **Sur la reconnaissance du concubin comme bénéficiaire :**
> La notice CCN action sociale précise que le concubin peut bénéficier du capital décès **sous condition de résidence commune avec l'assuré au jour du décès**. [NOTICE_CCN_sante_action_sociale.pdf]
> 
> **Sur les montants du contrat C87656 :**
> Le résumé mentionne uniquement :
> - Une **rente de conjoint** de **15 %** (Tranche A et B) versée au conjoint ou partenaire de PACS survivant [RESUME_C87656.pdf]
> - Un **capital obsèques forfaitaire de 2 500 €** [RESUME_C87656.pdf]
> 
> ⚠️ **Deux limites importantes :**
> 
> 1. Le résumé C87656 ne mentionne **pas explicitement le concubin** parmi les bénéficiaires de la rente de conjoint (uniquement conjoint ou partenaire de PACS).
> 2. Le **montant du capital décès** pour le contrat C87656 n'est **pas renseigné** dans les extraits fournis.
> 
> Je ne trouve pas cette information complète dans les documents disponibles. Il conviendrait de consulter la notice d'information complète rattachée au contrat C87656 pour connaître les conditions exactes d'éligibilité du concubin et le montant du capital décès associé.

**Réponse isolée**

> ## Bénéficiaire concubin et capital décès — Contrat C87656
> 
> ### Éligibilité du concubin
> 
> Le concubin peut être reconnu bénéficiaire **uniquement sous condition de résidence commune avec l'assuré au jour du décès**, à défaut de désignation particulière ou de conjoint/partenaire PACS. [NOTICE_CCN_sante_action_sociale.pdf]
> 
> ---
> 
> ### Montant du capital décès
> 
> Le montant dépend de la **situation de famille** et du **salaire brut de référence** (par tranche) :
> 
> | Situation de famille | Tranche A | Tranche B |
> |---|---|---|
> | Célibataire, veuf ou divorcé sans personne à charge | 180 % | 180 % |
> | Marié ou pacsé sans personne à charge | 220 % | 220 % |
> 
> [RESUME_C87656.pdf]
> 
> > ⚠️ **Point d'attention** : Le concubin n'étant ni conjoint marié ni partenaire PACS, la situation de famille retenue sera celle de **célibataire/veuf/divorcé**, soit **180 % du salaire brut de référence** (tranches A et B), sauf enfants à charge.
> 
> ---
> 
> ### Majorations applicables
> 
> - **+25 % par enfant à charge** reconnu au jour du sinistre, cumulable sans limitation de rang. [RESUME_C87656.pdf]
> - **Capital additionnel décès accidentel** : +100 % (tranches A et B) si le décès est accidentel. [RESUME_C87656.pdf]
> 
> ---
> 
> ### Garanties optionnelles souscrites
> 
> Le contrat C87656 prévoit une **rente de conjoint viagère à 15 %** du salaire de référence (tranches A et B), mais celle-ci est réservée au **conjoint ou partenaire PACS** — le concubin n'y est **pas éligible**. [RESUME_C87656.pdf]

Points en échec (e2e) : ['O1', 'O2']

Chunks e2e récupérés :

1. `NOTICE_CCN_sante_action_sociale` #10 (score 0.5047) — en une seule fois sur présentation de la facture acquittée par la personne ayant engagé les frais. Terme de la garantie. Le versement de la rente de conjoint cesse au décès du bénéficiaire. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation parti…
2. `NOTICE_CCN_metallurgie` #12 (score 0.4968) — Terme de la garantie. Le versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint d…
3. `RESUME_C87656` #5 (score 0.4819) — de conjoint En cas de décès de l'assuré, une rente viagère est versée à son conjoint ou partenaire de pacs survivant, sous réserve des conditions d'éligibilité définies par la notice d'information applicable au contrat. Garantie Tranche A Tranche B Rente de conjoint 15 % 15 % Garantie obsèques Un ca…
4. `NOTICE_CCN_agriculture` #11 (score 0.4635) — montants correspondants, figurent dans le résumé des garanties propre à chaque contrat. Modalités de versement. Les modalités de versement sont identiques à celles de la garantie de base à laquelle l'option se rattache. Terme de la garantie. Le versement cesse dans les mêmes conditions que la garant…
5. `NOTICE_CCN_metallurgie_distracteur` #8 (score 0.4561) — 70 % III — Dispositions relatives à chacune des garanties Article 13 — Capital décès Objet de la garantie. En cas de décès de l'assuré, l'assureur verse au bénéficiaire désigné un capital. Montant des prestations. Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enf…

### RC25 (fait_simple)

- retrieval : KO — documents manquants : ['NOTICE_CCN_transport_routier'] — points absents des chunks : ['O0', 'O1']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> ## Capital décès sans désignation bénéficiaire — Contrat C20077
> 
> Le contrat C20077 relève de la **Convention collective nationale du transport routier — Personnel non cadre**. Les documents disponibles sur ce contrat ne précisent pas explicitement la clause bénéficiaire type applicable.
> 
> Cependant, la notice de référence applicable à ce type de contrat PrevCorp ([NOTICE_CCN_agriculture.pdf]) définit la clause bénéficiaire type suivante, en l'absence de désignation particulière :
> 
> 1. **Le conjoint** non séparé de corps ou le **partenaire pacsé**
> 2. À défaut, les **enfants** nés ou à naître, par parts égales
> 3. À défaut, les **parents**
> 4. À défaut, les **autres ascendants**
> 5. À défaut, les **héritiers**
> 
> > ⚠️ **Point clé** : Le **concubin n'est pas inclus** dans cette clause bénéficiaire type [NOTICE_CCN_agriculture.pdf], contrairement à ce que prévoit par exemple la notice santé/action sociale [NOTICE_CCN_sante_action_sociale.pdf] qui l'intègre sous condition de résidence commune.
> 
> **En pratique**, si l'assuré souhaite désigner son concubin, il doit impérativement effectuer une **désignation bénéficiaire personnalisée** par écrit auprès de PrevCorp [NOTICE_CCN_agriculture.pdf].

**Réponse isolée**

> ## Versement du capital décès en l'absence de désignation — Contrat C20077
> 
> En l'absence de désignation particulière de bénéficiaire, la clause bénéficiaire type s'applique dans l'ordre suivant :
> 
> 1. **Au conjoint de l'assuré** (époux/épouse ou partenaire de PACS)
> 2. **À défaut, à ses enfants**, par parts égales
> 3. **À défaut, à ses héritiers**
> 
> [NOTICE_CCN_transport_routier.pdf — Extrait 9]
> 
> > **Point important concernant le concubin :** La notice confirme explicitement que **la qualité de concubin n'est pas reconnue** comme ouvrant droit aux garanties liées à la situation de famille. Aucune rubrique n'est d'ailleurs prévue à cet effet dans le bulletin d'adhésion individuel.
> [NOTICE_CCN_transport_routier.pdf — Extrait 12]
> 
> ---
> 
> **Recommandation pratique :** Si l'assuré souhaite que son concubin perçoive le capital décès, il doit impérativement effectuer une **désignation bénéficiaire personnalisée** par écrit, en précisant l'identité du concubin, son rang de priorité et sa quote-part. Cette désignation peut être modifiée à tout moment. [NOTICE_CCN_transport_routier.pdf — Extrait 10]

Points en échec (e2e) : ['O0', 'I0']

Chunks e2e récupérés :

1. `RESUME_C20077` #1 (score 0.5232) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…
2. `RESUME_C73736` #2 (score 0.4688) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
3. `NOTICE_CCN_agriculture` #11 (score 0.4617) — montants correspondants, figurent dans le résumé des garanties propre à chaque contrat. Modalités de versement. Les modalités de versement sont identiques à celles de la garantie de base à laquelle l'option se rattache. Terme de la garantie. Le versement cesse dans les mêmes conditions que la garant…
4. `NOTICE_CCN_sante_action_sociale` #10 (score 0.453) — en une seule fois sur présentation de la facture acquittée par la personne ayant engagé les frais. Terme de la garantie. Le versement de la rente de conjoint cesse au décès du bénéficiaire. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation parti…
5. `RESUME_C20077` #3 (score 0.4514) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
