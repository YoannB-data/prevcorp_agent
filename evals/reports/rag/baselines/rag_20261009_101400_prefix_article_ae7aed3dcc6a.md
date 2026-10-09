# Rapport d'éval RAG

- Date : 2026-10-09T10:14:00
- Hash du YAML : ae7aed3dcc6a
- Modèle : claude-sonnet-4-6
- Modèle du juge : claude-sonnet-4-6
- Temperature : 0.0
- k : 5
- Variante d'ingestion : prefix_article (vérifiée contre la collection)
- Contexte isolé : document entier

## Synthèse

Questions : 25 dont 0 en erreur d'I/O (exclues des scores et des dénominateurs ci-dessous).

| Type | R (retrieval) | E (end-to-end) | I (isolé) |
|---|---|---|---|
| **Tous** | 12/23 | 17/25 | 21/25 |
| fait_simple | 4/5 | 4/5 | 5/5 |
| chiffre_precis | 5/5 | 5/5 | 5/5 |
| croisement | 3/13 | 6/13 | 9/13 |
| sans_reponse | N/A | 2/2 | 2/2 |

### Répartition des diagnostics

| Diagnostic | Famille | Nb |
|---|---|---|
| sain | succès | 14 |
| échec de retrieval | échec | 4 |
| double échec | échec | 4 |
| succès sans la source attendue | suspect | 3 |

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
> La franchise court à compter du **premier jour d'arrêt de travail continu** et s'apprécie **par sinistre**, sauf rechute constatée dans les conditions prévues au contrat.
> 
> Par ailleurs, un **délai de carence de 3 mois** s'applique avant la prise d'effet de la garantie.
> 
> [RESUME_C87656.pdf]

**Réponse isolée**

> ## Délai de franchise — Incapacité Temporaire de Travail
> 
> Le délai de franchise de la garantie Incapacité Temporaire de Travail est de **90 jours**.
> 
> Les indemnités journalières complémentaires sont versées **à l'issue de cette franchise contractuelle de 90 jours**, qui court à compter du **premier jour d'arrêt de travail continu** et s'apprécie par sinistre (sauf rechute dans les conditions prévues au contrat).
> 
> > ⚠️ Un **délai de carence de 3 mois** s'applique également avant la prise d'effet de la garantie.
> 
> [RESUME_C87656.pdf]


Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.6213) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `RESUME_C87656` #3 (score 0.5271) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
3. `RESUME_C83792` #4 (score 0.5119) — | 28 % Invalidité 2e catégorie | 48 % | 48 % | 38 % Invalidité 3e catégorie | 72 % | 72 % | 57 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5,5 % De 12 à 17 ans 8 % De 18 à 25 ans (études ou apprentissage) 11 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par l…
4. `NOTICE_CCN_metallurgie_distracteur` #16 (score 0.508) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…
5. `RESUME_C73736` #4 (score 0.5077) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …

### RC02 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : succès sans la source attendue (suspect) — à corriger : audit manuel

**Réponse e2e**

> Oui, le contrat C87656 prévoit un délai de carence avant la prise d'effet de la garantie ITT.
> 
> **Délai de carence : 3 mois**
> 
> Ce délai s'applique avant la prise d'effet de la garantie, en plus de la franchise contractuelle de 90 jours qui court à compter du premier jour d'arrêt de travail continu. [RESUME_C87656.pdf]

**Réponse isolée**

> Oui, le contrat C87656 prévoit un délai de carence pour la garantie ITT.
> 
> **Durée : 3 mois**
> 
> > *"Un délai de carence de 3 mois s'applique avant la prise d'effet de la garantie."* [RESUME_C87656.pdf]
> 
> À noter que ce délai de carence se cumule avec la franchise contractuelle de 90 jours, qui court à compter du premier jour d'arrêt de travail continu. Les indemnités journalières complémentaires ne sont donc versées qu'à l'issue de cette franchise de 90 jours, et uniquement pour les assurés ayant dépassé le délai de carence de 3 mois. [RESUME_C87656.pdf]


Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.5318) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `RESUME_C87656` #3 (score 0.422) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
3. `NOTICE_CCN_sante_action_sociale` #16 (score 0.3938) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise et, le cas échéant, du délai de carence applicables, dans l…
4. `RESUME_C73736` #4 (score 0.3908) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …
5. `NOTICE_CCN_metallurgie_distracteur` #16 (score 0.384) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…

### RC03 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> ## Désignation bénéficiaire type et concubin — Contrat C87656
> 
> Je ne trouve pas de document relatif au **contrat C87656** dans les extraits disponibles. Le seul contrat référencé est le C73736 [RESUME_C73736.pdf].
> 
> ---
> 
> **Sur la question du concubin en général**, les documents disponibles donnent des réponses **variables selon la convention collective** :
> 
> - **CCN Action sociale** [NOTICE_CCN_sante_action_sociale.pdf] : le concubin **peut être bénéficiaire type**, sous condition de résidence commune avec l'assuré au jour du décès.
> - **CCN Agriculture** [NOTICE_CCN_agriculture.pdf] : la clause type ne mentionne **pas le concubin** — seuls le conjoint/partenaire PACS, les enfants, parents et ascendants sont visés.
> - **CCN Transport routier** [NOTICE_CCN_transport_routier.pdf] : le concubin est **explicitement exclu**, la convention ne lui reconnaissant pas la qualité ouvrant droit aux garanties liées à la situation de famille.
> 
> ---
> 
> > ⚠️ Pour obtenir une réponse précise sur le contrat **C87656**, il serait nécessaire de consulter le résumé ou la notice contractuelle correspondante, qui ne figure pas dans les documents fournis.

**Réponse isolée**

> Je ne trouve pas cette information dans les documents disponibles concernant spécifiquement le contrat C87656.
> 
> Cependant, je peux vous indiquer que les deux documents disponibles prévoient des règles différentes sur ce point :
> 
> - **Règlement général** [REGLEMENT_prevcorp.pdf] : La clause bénéficiaire type ne mentionne pas le concubin. Elle désigne en priorité le conjoint ou le partenaire de PACS, puis les enfants, les parents, les autres ascendants, et enfin les héritiers.
> 
> - **Notice CCN Santé et Action Sociale** [NOTICE_CCN_sante_action_sociale.pdf] : La clause bénéficiaire type inclut explicitement **le concubin**, sous condition de résidence commune avec l'assuré au jour du décès, au même rang que le conjoint et le partenaire de PACS.
> 
> Pour savoir quelle clause s'applique au contrat C87656, il faudrait identifier la convention collective ou le résumé des garanties propre à ce contrat.

Points en échec (e2e) : ['O1']

Chunks e2e récupérés :

1. `NOTICE_CCN_sante_action_sociale` #19 (score 0.413) — Article 16 — Garanties optionnelles désignation particulière : au conjoint de l'assuré non séparé de corps, à son partenaire lié par un pacte civil de solidarité, ou à son concubin sous condition de Bénéficiaire désigné | Rang | Répartition M. ou Mme (conjoint ou partenaire désigné) | 1 | 50 % Enfan…
2. `RESUME_C73736` #2 (score 0.4089) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
3. `NOTICE_CCN_agriculture` #19 (score 0.396) — Article 16 — Garanties optionnelles Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint de l'assuré non séparé de corps ou à son partenaire lié par un pacte civil de solidarité ; à défaut, à ses enfants nés ou à naître, …
4. `NOTICE_CCN_metallurgie_distracteur` #19 (score 0.394) — Article 16 — Rente de conjoint clause type prévue par le règlement. À défaut de déclaration expresse au moment de l'adhésion, l'assuré est réputé avoir désigné son conjoint comme bénéficiaire unique. La désignation précise l'identité de chaque bénéficiaire, son rang de priorité et sa quote-part. Ell…
5. `NOTICE_CCN_transport_routier` #19 (score 0.3894) — Article 14 — Incapacité temporaire de travail (ITT) Décomptes d'indemnités journalières de la Sécurité sociale Oui Non Acte de décès Non Oui Livret de famille ou extrait d'acte de naissance Non Oui Relevé d'identité bancaire du bénéficiaire Oui Oui Annexe II — Adhésion au régime Le bulletin d'adhési…

### RC04 (sans_reponse)

- retrieval : N/A
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis pour le contrat C39949 [RESUME_C39949.pdf] mentionnent uniquement une **prestation d'assistance** (soutien psychologique, aide à domicile, conseil juridique), mais ne précisent pas si le rapatriement à l'étranger est inclus. Le détail complet des garanties d'assistance est renvoyé au **"contrat d'assistance annexé"**, qui n'est pas disponible dans les extraits fournis.
> 
> Pour une réponse définitive, il conviendrait de consulter ce contrat d'assistance annexé.

**Réponse isolée**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis mentionnent bien une **prestation d'assistance** (soutien psychologique, aide à domicile, conseil juridique) incluse sans supplément de cotisation [RESUME_C39949.pdf], mais le détail des services couverts — notamment un éventuel rapatriement à l'étranger — renvoie au **contrat d'assistance annexé**, dont le contenu n'est pas disponible dans les extraits communiqués.
> 
> Pour obtenir une réponse précise, il conviendrait de consulter ce contrat d'assistance annexé.


Chunks e2e récupérés :

1. `RESUME_C39949` #5 (score 0.3988) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assureur lors de l'ouverture du dossier. Catégorie Tranche A Tranche B Tranche C Invalidité 1re catégorie 35 % 35 % 25 % Invalidité 2e catégorie 45 % 45 % 35 % Invalidité 3e catégorie 70 %
2. `NOTICE_CCN_metallurgie` #20 (score 0.3962) — Article 16 — Rente de conjoint douze derniers mois | Oui | Oui | Oui | Oui Arrêt de travail initial et prolongations | Oui | Non | Non | Non Décomptes d'indemnités journalières de la Sécurité sociale | Oui | Non | Non | Non Acte de décès | Non | Oui | Oui | Oui Livret de famille ou extrait d'acte de naissance | Non | Oui | Oui | Non Certificat de scolarité ou contrat d'apprentissage | Non | Non | Oui | Non Relevé d'identité bancaire du bénéficiaire | Oui | Oui | Oui | Oui Exclusions Exclusions applicables à toutes les garanties Sont exclus les sinistres résultant : de la guerre civile ou étrangère ; de la participation active de l'assuré à une émeute ou à un acte de terrorisme ; des effets directs ou indirects d'une explosion nucléaire ; d'une faute intentionnelle de l'assuré ; de la pratique d'un sport
3. `RESUME_C39949` #4 (score 0.3758) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale au-delà de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise est une franchise continue et court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation
4. `RESUME_C39949` #6 (score 0.3738) — 35 % 35 % 25 % Invalidité 2e catégorie 45 % 45 % 35 % Invalidité 3e catégorie 70 % 70 % 55 % Assistance Une prestation d'assistance (soutien psychologique, aide à domicile, conseil juridique) est incluse sans supplément de cotisation, dans les conditions fixées par le contrat d'assistance annexé. Catégorie de personnel | Tranche A | Tranche B | Tranche C Non cadre | 1,20 % | 1,85 % | 1,85 % Cotisations Catégorie de personnel Tranche A Tranche B Tranche C Non cadre 1,20 % 1,85 % 1,85 %
5. `RESUME_C20077` #4 (score 0.3632) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'apprécie par sinistre, sauf rechute constatée dans les conditions prévues au contrat. Période Tranche A Tranche B À l'issue de la franchise contractuelle 78 % 72 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie

### RC05 (croisement)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Analyse comparative : Garantie ITT
> 
> Oui, il existe un **écart significatif** entre les deux documents sur la durée de franchise.
> 
> ---
> 
> ### 🔍 Point de divergence : La franchise ITT
> 
> | Paramètre | Notice CCN Agriculture | Résumé C39949 |
> |---|---|---|
> | **Durée de franchise** | **90 jours** | **60 jours** |
> | **Type de franchise** | Continue | Continue |
> 
> [NOTICE_CCN_agriculture.pdf] : *"La franchise applicable à la garantie ITT est fixée à 90 jours."*
> 
> [RESUME_C39949.pdf] : *"À l'issue de la franchise de 60 jours : 70 % / 65 % / 60 %"*
> 
> ---
> 
> ### ⚠️ Point de vigilance supplémentaire : Terme de la garantie
> 
> | Paramètre | Notice CCN Agriculture | Résumé C39949 |
> |---|---|---|
> | **Fin de versement** | Reprise du travail, décès, retraite, **ou 1 095e jour** | Reprise du travail, décès, retraite, **ou liquidation d'une pension d'invalidité** |
> 
> Les deux documents ne mentionnent pas exactement les mêmes conditions de cessation des prestations.
> 
> ---
> 
> ### Conclusion
> 
> Le contrat C39949 est **plus favorable** que le régime de base de la CCN Agriculture sur la franchise (60 jours vs 90 jours), ce qui est cohérent avec la possibilité d'options contractuelles. Il convient toutefois de **vérifier si cette franchise réduite résulte bien d'une option souscrite** et de s'assurer que le terme de garantie applicable est clairement établi pour ce contrat.

**Réponse isolée**

> ## Analyse comparative : Garantie ITT
> 
> Oui, il existe **un écart significatif** entre les deux documents sur la garantie ITT.
> 
> ---
> 
> ### 🔴 Point de divergence : la durée de la franchise
> 
> | | Résumé C39949 | Notice CCN Agriculture |
> |---|---|---|
> | **Durée de la franchise** | **60 jours** | **90 jours** |
> 
> - Le résumé indique : *"À l'issue de la franchise de 60 jours"* [RESUME_C39949.pdf]
> - La notice indique : *"La franchise applicable à la garantie ITT est fixée à **90 jours**"* [NOTICE_CCN_agriculture.pdf]
> 
> ---
> 
> ### ✅ Points de convergence
> 
> Les deux documents sont cohérents sur :
> - La nature **continue** de la franchise [RESUME_C39949.pdf] [NOTICE_CCN_agriculture.pdf]
> - Les **taux d'indemnisation** (70 % / 65 % / 60 % selon les tranches A, B, C) [RESUME_C39949.pdf]
> - Les **modalités de versement** : mensuel à terme échu, au souscripteur en cas de maintien de salaire ou directement à l'assuré [RESUME_C39949.pdf] [NOTICE_CCN_agriculture.pdf]
> 
> ---
> 
> ### ⚠️ Conclusion
> 
> Cet écart sur la franchise (60 vs 90 jours) est **matériel** : il conditionne directement le déclenchement des prestations. Il convient de **vérifier les conditions particulières du contrat** pour déterminer quelle durée s'applique effectivement, et le cas échéant de corriger le résumé des garanties.


Chunks e2e récupérés :

1. `NOTICE_CCN_agriculture` #16 (score 0.4399) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…
2. `RESUME_C39949` #5 (score 0.437) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidatio…
3. `RESUME_C39949` #4 (score 0.432) — 25 % Invalidité 2e catégorie | 45 % | 45 % | 35 % Invalidité 3e catégorie | 70 % | 70 % | 55 % Âge de l'enfant Taux annuel Jusqu'à 11 ans 5 % De 12 à 17 ans 7 % De 18 à 25 ans (études ou apprentissage) 10 % Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail indemnisé par la Sé…
4. `NOTICE_CCN_agriculture` #22 (score 0.426) — Article 16 — Garanties optionnelles Oui | Oui Annexe I — Pièces justificatives Justificatif ITT IPP DÉCÈS- RENTE IAD ÉDUCATION Bulletins de salaire des douze derniers mois Oui Oui Oui Oui Arrêt de travail initial et prolongations Oui Non Non Non Décomptes d'indemnités journalières de la Oui Oui Non …
5. `NOTICE_CCN_agriculture` #13 (score 0.4256) — Article 11 — Fausse déclaration Toute réticence ou fausse déclaration intentionnelle de votre part entraîne la nullité de la garantie, conformément aux articles L.113-8 et L.113-9 du Code des assurances.

### RC06 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : succès sans la source attendue (suspect) — à corriger : audit manuel

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

**Réponse isolée**

> ## Taux de couverture invalidité — Contrat n° C39949
> 
> Voici les taux applicables, exprimés en **pourcentage du salaire annuel brut de référence**, par tranche de rémunération :
> 
> | Catégorie d'invalidité | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | **1re catégorie** (invalide pouvant exercer une activité rémunérée) | 35 % | 35 % | 25 % |
> | **2e catégorie** (invalide absolument incapable d'exercer une profession) | 45 % | 45 % | 35 % |
> | **3e catégorie** (invalide nécessitant l'assistance d'une tierce personne) | 70 % | 70 % | 55 % |
> 
> [RESUME_C39949.pdf]
> 
> > **Rappel :** Ces rentes sont versées **mensuellement, sous déduction des prestations de la Sécurité sociale**. La catégorie d'invalidité est déterminée par le médecin conseil de la CPAM. [REGLEMENT_prevcorp.pdf]


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

> ## Incapacité Temporaire de Travail — Contrat C87656
> 
> ### Taux de couverture
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise contractuelle de 90 jours | **82 %** | **78 %** |
> 
> Ces taux sont exprimés en pourcentage du salaire annuel brut de référence, **sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement**. [RESUME_C87656.pdf]
> 
> ### Franchise
> 
> - **Durée : 90 jours**
> - **Modalité : franchise continue**, courant à compter du premier jour d'arrêt de travail continu, appréciée par sinistre (sauf rechute dans les conditions prévues au contrat). [RESUME_C87656.pdf]
> 
> ### Point d'attention
> 
> Un **délai de carence de 3 mois** s'applique avant la prise d'effet de la garantie. [RESUME_C87656.pdf]
> 
> ### Terme du versement
> 
> Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Par ailleurs, le règlement général fixe une limite absolue au **1 095e jour d'arrêt**. [RESUME_C87656.pdf] [REGLEMENT_prevcorp.pdf]


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
> *Les taux sont exprimés en % du salaire annuel brut de référence.*
> [RESUME_C83792.pdf]
> 
> ---
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
> ---
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
> Un capital est versé aux bénéficiaires désignés, dont le montant dépend de la situation de famille au jour du décès [RESUME_C83792.pdf] :
> 
> | Situation de famille | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | Célibataire, veuf, divorcé sans enfant à charge | 140 % | 140 % | 115 % |
> | Marié ou pacsé sans enfant à charge | 160 % | 160 % | 135 % |
> 
> ### Majorations familiales
> Une majoration par enfant à charge est applicable, **cumulable sans limitation de rang** [RESUME_C83792.pdf] :
> 
> | | Tranche A | Tranche B | Tranche C |
> |---|---|---|---|
> | Par enfant à charge | +28 % | +28 % | +18 % |
> 
> ### Autres garanties liées au décès
> [RESUME_C83792.pdf] :
> 
> - **Invalidité absolue et définitive** (anticipation du capital décès) : 100 % sur toutes les tranches
> - **Décès accidentel** (capital additionnel) : 100 % sur toutes les tranches
> - **Double effet** (décès simultané ou postérieur du conjoint) : 100 % sur toutes les tranches
> - **Obsèques** (capital forfaitaire) : **1 900 €** sur toutes les tranches
> 
> ### Rente éducation
> En cas de décès laissant des enfants à charge, une rente temporaire est versée jusqu'à la fin des études ou au plus tard au **26e anniversaire** [RESUME_C83792.pdf] :
> 
> | Âge de l'enfant | Taux annuel |
> |---|---|
> | Jusqu'à 11 ans | 5,5 % |
> | De 12 à 17 ans | 8 % |
> | De 18 à 25 ans (études ou apprentissage) | 11 % |
> 
> > Les taux sont exprimés en pourcentage du **salaire annuel brut de référence**.


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

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : KO
- isolated : OK
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> Oui, des garanties optionnelles sont disponibles sur le contrat C87656.
> 
> **Rente de conjoint**
> En cas de décès de l'assuré, une rente viagère est versée à son conjoint ou partenaire de PACS. Les taux applicables sont :
> - Tranche A : **15 %**
> - Tranche B : **15 %**
> 
> [RESUME_C87656.pdf]
> 
> ---
> 
> > ⚠️ Le document mentionne l'existence de garanties optionnelles souscrites, mais ne détaille que la rente de conjoint. D'autres options pourraient exister sans être listées dans les extraits disponibles. Pour une vue exhaustive, il conviendrait de consulter l'intégralité du résumé des garanties du contrat C87656.

**Réponse isolée**

> Oui, le contrat C87656 a souscrit les garanties optionnelles suivantes :
> 
> **1. Rente de conjoint**
> En cas de décès de l'assuré, une rente viagère est versée au conjoint ou partenaire de PACS survivant.
> - Taux : **15 % du salaire brut de référence**, sur tranche A et tranche B. [RESUME_C87656.pdf]
> 
> **2. Garantie obsèques**
> Un capital forfaitaire est versé à la personne ayant engagé les frais d'obsèques, sur présentation de la facture acquittée.
> - Montant : **2 500 €** (forfaitaire). [RESUME_C87656.pdf]
> 
> ---
> 
> Pour rappel, le règlement général liste d'autres garanties optionnelles qui peuvent être souscrites (rente éducation, garantie double effet, garantie dépendance totale, indemnisation surcomplémentaire ITT au-delà de la tranche B), mais celles-ci **ne figurent pas parmi les garanties effectivement souscrites** dans le résumé du contrat C87656. [REGLEMENT_prevcorp.pdf]

Points en échec (e2e) : ['O2']

Chunks e2e récupérés :

1. `RESUME_C87656` #2 (score 0.4611) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
2. `NOTICE_CCN_sante_action_sociale` #23 (score 0.4435) — Article 16 — Garanties optionnelles de famille ou extrait d'acte de Non Non Oui Oui Non naissance Certificat de scolarité ou contrat Non Non Non Oui Non d'apprentissage Relevé d'identité bancaire du Oui Oui Oui Oui Oui bénéficiaire
3. `NOTICE_CCN_agriculture` #18 (score 0.4269) — Article 16 — Garanties optionnelles Objet de la garantie. Le souscripteur peut, en complément des garanties de base, adhérir pour tout ou partie de son personnel à une ou plusieurs garanties optionnelles portant sur les risques décès, incapacité ou invalidité. Nom du bénéficiaire | Rang de priorité …
4. `RESUME_C87656` #3 (score 0.4213) — B À l'issue de la franchise contractuelle de 90 jours | 82 % | 78 % Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 55 % | 55 % Invalidité 2e catégorie | 82 % | 82 % Invalidité 3e catégorie | 110 % | 110 % Garantie | Tranche A | Tranche B Rente de conjoint | 15 % | 15 % Garantie | Monta…
5. `RESUME_C87656` #4 (score 0.4205) — la reprise du travail, à la liquidation d'une pension d'invalidité, au décès de l'assuré ou à son départ à la retraite. Invalidité En cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du sal…

### RC11 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : double échec (échec) — à corriger : vérifier question et scorer (I), puis traiter R et E séparément

**Réponse e2e**

> ## Franchise ITT — Contrat C73736
> 
> ### Nature de la franchise
> 
> Le contrat C73736 prévoit une **franchise continue**, qui « court sans interruption à compter du premier jour d'arrêt de travail » [RESUME_C73736.pdf].
> 
> ### Correspondance avec le Règlement et la CCN
> 
> Cette modalité est **conforme au régime par défaut** prévu par la convention collective nationale de la métallurgie, qui stipule que « la franchise applicable est une franchise continue : le délai court sans interruption à compter du premier jour de l'arrêt de travail » et que « le régime de base de la convention ne prévoit aucune dérogation à cette modalité » [NOTICE_CCN_metallurgie.pdf].
> 
> Il ne s'agit donc **pas d'une dérogation**, mais bien de l'application standard du régime CCN.
> 
> ---
> 
> > ⚠️ **Point de vigilance** : Un autre document présente une franchise **discontinue** avec une franchise de **60 jours** [NOTICE_CCN_metallurgie_distracteur.pdf]. Ces paramètres ne correspondent **pas** au contrat C73736 et sont à écarter pour ce dossier.

**Réponse isolée**

> ## Franchise ITT — Contrat C73736
> 
> Je ne trouve pas cette information dans les documents disponibles.
> 
> **Aucun document fourni ne fait référence au contrat C73736** ni à ses dispositions particulières concernant la franchise ITT.
> 
> ---
> 
> ### Ce que les documents permettent d'établir :
> 
> **Régime par défaut du Règlement général :**
> Le règlement prévoit deux modalités possibles — franchise continue ou discontinue — sans en imposer une par défaut. La modalité retenue est renvoyée à la notice d'information ou au résumé des garanties propre à chaque contrat. [REGLEMENT_prevcorp.pdf, Art. 14]
> 
> **Régime applicable sous la CCN Métallurgie (IDCC 3248) :**
> La notice CCN Métallurgie fixe explicitement une **franchise continue** et précise qu'**aucune dérogation n'est prévue** par le régime de base de la convention :
> > *« Le régime de base de la convention ne prévoit aucune dérogation à cette modalité. »*
> [NOTICE_CCN_metallurgie.pdf, Art. 14]
> 
> ---
> 
> ### Conclusion :
> 
> Pour connaître le régime applicable au contrat **C73736**, il convient de consulter le **résumé des garanties propre à ce contrat**, qui n'est pas inclus dans les documents fournis.

Points en échec (e2e) : ['O0']
Points en échec (isolé) : ['O0', 'O1']

Chunks e2e récupérés :

1. `RESUME_C73736` #5 (score 0.5333) — court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 90 jours 80 % 75 % 70 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de ma…
2. `RESUME_C73736` #4 (score 0.5316) — 3e catégorie | 75 % | 75 % | 60 % Rente éducation Lorsque l'assuré laisse un ou plusieurs enfants à charge au sens de la convention collective, une rente temporaire leur est versée jusqu'à la fin de leurs études ou au plus tard à leur 26e anniversaire. Âge de l'enfant Taux annuel Jusqu'à 11 ans 6 % …
3. `RESUME_C87656` #2 (score 0.5088) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
4. `NOTICE_CCN_metallurgie_distracteur` #16 (score 0.4889) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…
5. `NOTICE_CCN_metallurgie` #16 (score 0.4731) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…

### RC12 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> D'après les documents disponibles, le taux de la rente invalidité 2e catégorie sur la Tranche B pour le contrat C73736 est de **50 %** du salaire annuel brut de référence. [RESUME_C73736.pdf]

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
> > *"Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit."*
> > [RESUME_C73736.pdf]
> 
> ### Ordre de priorité applicable
> 
> Conformément à la clause type du Règlement PrevCorp, le capital décès sera versé dans l'ordre suivant :
> 
> 1. **Au conjoint** non séparé de corps ou au partenaire pacsé
> 2. **À défaut**, aux enfants nés ou à naître, par parts égales
> 3. **À défaut**, aux parents
> 4. **À défaut**, aux autres ascendants
> 5. **À défaut**, aux héritiers
> 
> [REGLEMENT_prevcorp.pdf]
> 
> ### Conclusion
> 
> **Aucune clause personnalisée n'est enregistrée** pour ce contrat. Il n'y a donc pas de répartition spécifique à appliquer : c'est l'ordre légal type qui prévaut intégralement.

**Réponse isolée**

> ## Clause bénéficiaire applicable au contrat C73736
> 
> Le contrat C73736 applique la **clause bénéficiaire type**.
> 
> En effet, le résumé des garanties indique explicitement :
> 
> > *"Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit."* [RESUME_C73736.pdf]
> 
> Conformément à cette clause type, le capital décès est versé dans l'ordre de priorité suivant [NOTICE_CCN_metallurgie.pdf] :
> 
> 1. **Le conjoint** (marié non séparé de corps) ou le **partenaire de PACS**
> 2. À défaut, les **enfants** nés ou à naître, par parts égales
> 3. À défaut, les **parents**
> 4. À défaut, les **autres ascendants**
> 5. À défaut, les **héritiers**
> 
> Il n'existe donc **aucune clause personnalisée** déclarée à l'assureur pour ce contrat, et aucune répartition particulière n'est applicable.


Chunks e2e récupérés :

1. `NOTICE_CCN_sante_action_sociale` #19 (score 0.6054) — Article 16 — Garanties optionnelles désignation particulière : au conjoint de l'assuré non séparé de corps, à son partenaire lié par un pacte civil de solidarité, ou à son concubin sous condition de Bénéficiaire désigné | Rang | Répartition M. ou Mme (conjoint ou partenaire désigné) | 1 | 50 % Enfan…
2. `NOTICE_CCN_agriculture` #19 (score 0.592) — Article 16 — Garanties optionnelles Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint de l'assuré non séparé de corps ou à son partenaire lié par un pacte civil de solidarité ; à défaut, à ses enfants nés ou à naître, …
3. `RESUME_C73736` #2 (score 0.5823) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
4. `REGLEMENT_prevcorp` #19 (score 0.5626) — Article 16 — Garanties optionnelles parts égales entre eux ; à défaut, à ses parents ; à défaut, à ses autres ascendants ; à défaut, à ses héritiers. Clause bénéficiaire personnalisée Vous pouvez désigner un ou plusieurs bénéficiaires de votre choix, par écrit, en précisant leur identité, leur rang …
5. `NOTICE_CCN_metallurgie` #19 (score 0.5532) — Article 16 — Rente de conjoint défaut, à ses enfants nés ou à naître, par parts égales entre eux ; à défaut, à ses parents ; à défaut, à ses autres ascendants ; à défaut, à ses héritiers. Clause bénéficiaire personnalisée Vous pouvez désigner un ou plusieurs bénéficiaires de votre choix, par écrit, …

### RC14 (fait_simple)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Justificatif de qualité de concubin en cas de décès
> 
> Selon les documents PrevCorp, le justificatif requis pour prouver la qualité de concubin est :
> 
> > **Une attestation de vie commune ou, à défaut, deux justificatifs de domicile commun de plus de deux ans.**
> 
> [REGLEMENT_prevcorp.pdf — Articles 16, Extraits 2 et 3]
> 
> ---
> 
> ⚠️ **Point d'attention important** : La convention collective du **transport routier** ne reconnaît pas la qualité de concubin comme ouvrant droit aux garanties liées à la situation de famille. Aucune rubrique n'est d'ailleurs prévue à cet effet dans le bulletin d'adhésion individuel.
> 
> [NOTICE_CCN_transport_routier.pdf — Article 14, Extrait 1]
> 
> Il convient donc de vérifier la convention collective applicable à votre situation avant de constituer ce dossier.

**Réponse isolée**

> D'après les documents disponibles, pour une demande au titre du **décès (DÉCÈS-IAD)**, le justificatif de qualité de concubin requis est :
> 
> > **Une attestation de vie commune ou, à défaut, deux justificatifs de domicile commun de plus de deux ans.**
> 
> [REGLEMENT_prevcorp.pdf — Extrait 23]
> 
> À noter que ce justificatif n'est pas demandé pour les autres garanties (ITT, IPP, Rente Éducation, Rente Conjoint).


Chunks e2e récupérés :

1. `NOTICE_CCN_transport_routier` #19 (score 0.524) — Article 14 — Incapacité temporaire de travail (ITT) Décomptes d'indemnités journalières de la Sécurité sociale Oui Non Acte de décès Non Oui Livret de famille ou extrait d'acte de naissance Non Oui Relevé d'identité bancaire du bénéficiaire Oui Oui Annexe II — Adhésion au régime Le bulletin d'adhési…
2. `REGLEMENT_prevcorp` #23 (score 0.522) — Article 16 — Garanties optionnelles permanente Acte de décès Non Non Oui Oui Oui Livret de famille ou extrait d'acte de Non Non Oui Oui Non naissance Certificat de scolarité ou contrat Non Non Non Oui Non d'apprentissage Justificatif de qualité de concubin Non Non Oui Non Non (attestation de vie com…
3. `REGLEMENT_prevcorp` #22 (score 0.5155) — Article 16 — Garanties optionnelles | Oui | Non Certificat de scolarité ou contrat d'apprentissage | Non | Non | Non | Oui | Non Justificatif de qualité de concubin (attestation de vie commune ou, à défaut, deux justificatifs de domicile commun de plus de deux ans) | Non | Non | Oui | Non | Non Rele…
4. `NOTICE_CCN_metallurgie_distracteur` #21 (score 0.4343) — Article 16 — Rente de conjoint bénéficiaire qui a volontairement donné la mort à l'assuré ; le capital est alors attribué aux autres bénéficiaires. Exclusions applicables aux garanties accident et incapacité Sont exclus les sinistres survenus alors que l'assuré se trouvait en état d'ivresse, avec un…
5. `NOTICE_CCN_metallurgie` #22 (score 0.4328) — Article 16 — Rente de conjoint initial et prolongations Oui Non Non Non Décomptes d'indemnités journalières de Oui Non Non Non la Sécurité sociale Acte de décès Non Oui Oui Oui Livret de famille ou extrait d'acte de Non Oui Oui Non naissance Certificat de scolarité ou contrat Non Non Oui Non d'appre…

### RC15 (fait_simple)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Durée de la franchise en cas d'arrêt maladie ordinaire
> 
> La réponse varie selon le contrat applicable :
> 
> - **Contrat standard PrevCorp (CCN Métallurgie)** : la franchise est de **90 jours**, appliquée en mode **continu** (le délai court sans interruption à compter du premier jour d'arrêt, quelle que soit la durée de celui-ci). [NOTICE_CCN_metallurgie.pdf]
> 
> - **Contrat alternatif (CCN Métallurgie - variante)** : la franchise est de **60 jours**, appliquée en mode **discontinu** (les journées d'arrêt liées au même sinistre ou à des rechutes se cumulent, même séparées par des périodes de reprise du travail). [NOTICE_CCN_metallurgie_distracteur.pdf]
> 
> La FAQ PrevCorp confirme la franchise de **90 jours calendaires** pour un arrêt maladie ordinaire, et précise que **le jour de carence de la Sécurité sociale est distinct** de cette franchise contractuelle : les deux notions ne se confondent pas. [FAQ_prevcorp.pdf]
> 
> > ⚠️ **Point d'attention** : le règlement PrevCorp rappelle que la modalité retenue (continue ou discontinue) et la durée exacte de la franchise sont précisées dans la **notice d'information ou le résumé des garanties propre à chaque contrat**. [REGLEMENT_prevcorp.pdf]

**Réponse isolée**

> ## Franchise en cas d'arrêt maladie ordinaire
> 
> La franchise est de **90 jours calendaires**, décomptés à partir du **premier jour de l'arrêt de travail**. [FAQ_prevcorp.pdf]
> 
> **Point important :** le jour de carence de la Sécurité sociale est sans incidence sur ce délai. La franchise contractuelle de 90 jours démarre au premier jour de l'arrêt, que ce jour soit ou non pris en charge par la Sécurité sociale. [FAQ_prevcorp.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #2 (score 0.5862) — dans le temps ? Les taux de cotisation sont revus chaque année à l'occasion de la revalorisation du contrat. Toute évolution vous est communiquée par votre employeur, généralement en fin d'année pour une application au 1er janvier suivant. 4. Garanties Incapacité temporaire de travail Combien de tem…
2. `NOTICE_CCN_metallurgie_distracteur` #16 (score 0.5486) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…
3. `NOTICE_CCN_metallurgie` #16 (score 0.547) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, à l'issue du délai de franchise, dans les conditions et au taux précisés dans le résumé des…
4. `REGLEMENT_prevcorp` #16 (score 0.5383) — Article 14 — Incapacité temporaire de travail (ITT) Objet de la garantie. Lorsque l'assuré est en arrêt de travail indemnisé par la Sécurité sociale, l'assureur verse une indemnité journalière complémentaire, dans les conditions et au taux précisés dans le résumé des garanties propre à chaque contra…
5. `FAQ_prevcorp` #5 (score 0.5343) — dans la limite de 12 mois, sans cotisation supplémentaire à votre charge. 6. Divers Je suis salarié du contrat C20077 et je me trouve en arrêt de travail : quelles démarches dois- je effectuer pour percevoir mes indemnités journalières complémentaires ? Vous devez transmettre votre avis d'arrêt de t…

### RC16 (fait_simple)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> Non, la franchise de 90 jours n'est pas retardée par le jour de carence de la Sécurité sociale.
> 
> Ces deux notions sont distinctes : la franchise contractuelle démarre **au premier jour de l'arrêt de travail**, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. [FAQ_prevcorp.pdf]

**Réponse isolée**

> Non, la franchise de 90 jours n'est pas retardée par le jour de carence de la Sécurité sociale.
> 
> Ces deux notions sont distinctes : la franchise contractuelle de 90 jours démarre **dès le premier jour de l'arrêt de travail**, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. [FAQ_prevcorp.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #2 (score 0.5926) — dans le temps ? Les taux de cotisation sont revus chaque année à l'occasion de la revalorisation du contrat. Toute évolution vous est communiquée par votre employeur, généralement en fin d'année pour une application au 1er janvier suivant. 4. Garanties Incapacité temporaire de travail Combien de tem…
2. `FAQ_prevcorp` #3 (score 0.5644) — de la Sécurité sociale et la franchise contractuelle de 90 jours sont deux notions distinctes. La franchise contractuelle démarre au premier jour de l'arrêt de travail, que ce premier jour soit ou non pris en charge par la Sécurité sociale au titre de la carence. Invalidité Quelles sont les catégori…
3. `FAQ_prevcorp` #6 (score 0.4716) — Le versement des indemnités journalières complémentaires débute à l'issue de la franchise applicable à votre contrat, sur présentation des décomptes d'indemnités journalières de la Sécurité sociale ; le taux de versement applicable figure dans le résumé des garanties qui vous a été remis. Comment me…
4. `RESUME_C87656` #2 (score 0.4653) — de rang. Cette majoration s'applique de la même manière quelle que soit la situation de famille retenue dans le tableau ci-dessus, et vient s'ajouter au capital de base sans condition d'ancienneté de l'enfant dans le foyer. Incapacité temporaire de travail Lorsque l'assuré est en arrêt de travail in…
5. `REGLEMENT_prevcorp` #2 (score 0.4561) — qui sont fiscalement à charge de l'assuré. Franchise Période, exprimée en jours calendaires, pendant laquelle aucune prestation n'est due au titre de la garantie incapacité temporaire de travail malgré la survenance du sinistre. Sa durée et sa modalité d'application (continue ou discontinue) sont pr…

### RC17 (sans_reponse)

- retrieval : N/A
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits du contrat C73736 [RESUME_C73736.pdf] présentent les garanties et leurs taux de prestations, mais ne mentionnent pas de ventilation des cotisations (ni taux salarié, ni taux patronal) pour ce contrat spécifique.
> 
> Les seules cotisations mentionnées dans les documents concernent le contrat C87656 [RESUME_C87656.pdf], qui indique des taux pour le personnel cadre (Tranche A : 1,55 %, Tranche B : 2,40 %), mais sans préciser s'il s'agit de la part salariale et sans lien avec le contrat C73736.

**Réponse isolée**

> Je ne trouve pas cette information dans les documents disponibles.
> 
> Les extraits fournis du contrat C73736 mentionnent uniquement les taux de cotisation globaux par tranche pour la catégorie cadre (1,60 % en Tranche A, 2,45 % en Tranche B et C) [RESUME_C73736.pdf], mais sans ventilation par garantie ni distinction entre part salariale et part patronale. Par ailleurs, **aucune garantie "rente de conjoint" n'est mentionnée** dans ces extraits.
> 
> Pour obtenir cette information, il conviendrait de consulter le contrat complet ou le tableau de répartition des cotisations associé.


Chunks e2e récupérés :

1. `RESUME_C87656` #5 (score 0.5491) — de conjoint En cas de décès de l'assuré, une rente viagère est versée à son conjoint ou partenaire de pacs survivant, sous réserve des conditions d'éligibilité définies par la notice d'information applicable au contrat. Garantie Tranche A Tranche B Rente de conjoint 15 % 15 % Garantie obsèques Un capital forfaitaire est versé à la personne ayant engagé les frais d'obsèques de l'assuré, sur présentation de la facture acquittée. Garantie Montant Obsèques (capital forfaitaire) 2 500 € Catégorie de personnel | Tranche A | Tranche B Cadre | 1,55 % | 2,40 % Cotisations Catégorie de personnel Tranche A Tranche B Cadre 1,55 % 2,40 %
2. `NOTICE_CCN_metallurgie_distracteur` #18 (score 0.5277) — Article 16 — Rente de conjoint Objet de la garantie. Le souscripteur peut, en complément des garanties de base, adhérir pour tout ou partie de son personnel à une garantie de rente de conjoint, versée au conjoint survivant en cas de décès de l'assuré. Montant des prestations. Les montants applicables figurent dans le résumé des garanties propre à chaque contrat. Modalités de versement. La rente est versée trimestriellement d'avance. Terme de la garantie. Le versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire personnalisée Le régime applicable aux entreprises relevant de la présente convention collective repose sur une clause bénéficiaire personnalisée, déclarée par l'assuré lors de son adhésion auprès de l'assureur, qui se substitue à la clause type prévue par le règlement. À défaut de déclaration expresse au moment de l'adhésion, l'assuré est réputé avoir désigné
3. `NOTICE_CCN_metallurgie` #18 (score 0.5255) — Article 16 — Rente de conjoint Objet de la garantie. Le souscripteur peut, en complément des garanties de base, adhérir pour tout ou partie de son personnel à une garantie de rente de conjoint, versée au conjoint survivant en cas de décès de l'assuré. Montant des prestations. Les montants applicables figurent dans le résumé des garanties propre à chaque contrat. Modalités de versement. La rente est versée trimestriellement d'avance. Terme de la garantie. Le versement cesse au remariage, à la conclusion d'un nouveau PACS ou au décès du bénéficiaire, et au plus tard au 65e anniversaire de l'assuré. Bénéficiaires des garanties Clause bénéficiaire type Le capital décès est versé, à défaut de désignation particulière : au conjoint de l'assuré non séparé de corps ou à son partenaire lié par un pacte civil de solidarité ; à défaut, à ses enfants nés ou à naître, par parts égales entre eux ; à défaut, à ses parents ;
4. `RESUME_C73736` #1 (score 0.5119) — % Obsèques (capital forfaitaire) | 2 200 € | 2 200 € | 2 200 € PREVCORP PRÉVOYANCE Résumé des garanties — Contrat n° C73736 Convention collective nationale de la métallurgie — Personnel cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence, par tranche de rémunération (tranche A jusqu'au plafond annuel de la Sécurité sociale, tranche B de 1 à 4 plafonds, tranche C de 4 à 8 plafonds). Garantie décès toutes causes En cas de décès de l'assuré, quelle qu'en soit la cause, un capital est versé aux bénéficiaires désignés. Son montant dépend de la situation de famille du salarié constatée au jour du décès. Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120
5. `RESUME_C73736` #2 (score 0.5042) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'applique de plein droit. Majorations familiales Le capital décès toutes causes fait l'objet d'une majoration par enfant à charge reconnu au jour du sinistre, cumulable sans limitation de rang. Majoration par enfant à charge Tranche A Tranche B Tranche C Capital décès toutes causes + 30 % + 30 % + 20 % Autres garanties liées au décès Garantie Tranche Tranche Tranche A B C Invalidité absolue et définitive (anticipation du capital 100 % 100 % 100 % décès) Décès accidentel (capital additionnel) 100 % 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100

### RC18 (chiffre_precis)

- retrieval : OK
- end_to_end : OK
- isolated : OK
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Capital décès — Contrat C20077
> 
> Pour un salarié **célibataire, veuf ou divorcé sans personne à charge**, le capital décès toutes causes s'élève à :
> 
> | Tranche A | Tranche B |
> |-----------|-----------|
> | **120 %** | **120 %** |
> 
> Ces taux sont exprimés en pourcentage du **salaire annuel brut de référence**.
> 
> [RESUME_C20077.pdf]

**Réponse isolée**

> ## Capital décès toutes causes — Salarié célibataire sans personne à charge
> 
> Pour un salarié célibataire, veuf ou divorcé sans personne à charge, le capital décès toutes causes s'élève à :
> 
> | Tranche A | Tranche B |
> |-----------|-----------|
> | **120 %** | **120 %** |
> 
> Ces taux sont exprimés en **pourcentage du salaire annuel brut de référence**, par tranche de rémunération (Tranche A = jusqu'au plafond annuel de la Sécurité sociale ; Tranche B = au-delà). [RESUME_C20077.pdf]
> 
> > ⚠️ **À noter :** Si le salarié a des enfants à charge au jour du sinistre, une **majoration de 25 % par enfant** s'ajoute au capital de base, cumulable sans limitation de rang. [RESUME_C20077.pdf]


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

> ## Majoration du capital décès par enfant à charge — Contrat C20077
> 
> **Oui**, le contrat C20077 prévoit bien une majoration du capital décès par enfant à charge.
> 
> **Taux : +25 % par enfant à charge**, applicable sur le capital décès toutes causes. [RESUME_C20077.pdf]
> 
> ### Modalités d'application :
> - **Cumulable sans limitation de rang** (chaque enfant à charge ouvre droit à la majoration)
> - S'applique **quelle que soit la situation de famille** retenue
> - Vient **s'ajouter au capital de base**
> - **Sans condition d'ancienneté** de l'enfant dans le foyer
> - L'enfant doit être **reconnu à charge au jour du sinistre**
> 
> [RESUME_C20077.pdf]
> 
> ---
> > 💡 **À noter** : ce taux de 25 % diffère du contrat C73736, qui prévoit une majoration de **+30 % en Tranches A et B** et **+20 % en Tranche C** [RESUME_C73736.pdf].

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
> À noter : la définition des enfants à charge retenue est celle de la convention collective, soit les enfants de moins de 18 ans, ou de moins de 26 ans s'ils poursuivent des études ou sont en apprentissage, et fiscalement à charge de l'assuré. [NOTICE_CCN_transport_routier.pdf]

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
> Les documents disponibles indiquent que le taux de couverture en **invalidité 1re catégorie** pour le contrat C20077 est de **50 % du salaire annuel brut de référence**, sur les tranches A et B. [RESUME_C20077.pdf]
> 
> Cependant, **je ne trouve pas cette information dans les documents disponibles** concernant la nature de ce taux : il m'est impossible de déterminer, sur la base des extraits fournis, s'il s'agit :
> 
> - du **taux de base issu du Règlement** de prévoyance de la Convention collective nationale du transport routier, ou
> - d'une **dérogation négociée** spécifique à ce contrat.
> 
> Les extraits ne contiennent aucune référence au texte du Règlement de la CCN transport routier ni à une comparaison entre les taux contractuels et les minima conventionnels.
> 
> > ⚠️ Pour trancher cette question, il conviendrait de consulter directement le **Règlement de prévoyance de la CCN Transport Routier** (accord du 26 janvier 2011 et ses avenants) et de le comparer aux taux du contrat C20077.

**Réponse isolée**

> ## Analyse : Taux d'invalidité 1re catégorie — Contrat C20077
> 
> ### Taux de base du Règlement général
> 
> Le Règlement général fixe le taux de base suivant :
> 
> > « 50 % pour la 1re catégorie » [REGLEMENT_prevcorp.pdf, Article 15]
> 
> Il précise également que :
> 
> > « Le résumé des garanties propre à chaque contrat précise le taux effectivement applicable, **qui peut différer de ce taux de base**. » [REGLEMENT_prevcorp.pdf, Article 15]
> 
> ### Taux appliqué dans le contrat C20077
> 
> Le résumé des garanties du contrat C20077 retient :
> 
> > Invalidité 1re catégorie : **50 % (Tranche A) / 50 % (Tranche B)** [RESUME_C20077.pdf]
> 
> ### Conclusion
> 
> Le taux de 50 % appliqué au contrat C20077 pour l'invalidité 1re catégorie est **identique au taux de base** du Règlement général. Il ne s'agit donc **pas d'une dérogation**, mais d'une simple confirmation du taux standard, sans adaptation spécifique à la convention collective nationale du transport routier.

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
> | **1re catégorie** | Invalides **capables d'exercer** une activité rémunérée |
> | **2e catégorie** | Invalides **absolument incapables** d'exercer une profession quelconque |
> | **3e catégorie** | Invalides absolument incapables d'exercer une profession quelconque **et dans l'obligation de recourir à l'assistance d'une tierce personne** pour accomplir les actes ordinaires de la vie |
> 
> [FAQ_prevcorp.pdf] [REGLEMENT_prevcorp.pdf]
> 
> ---
> 
> ## Qui détermine la catégorie ?
> 
> La catégorie est déterminée par le **médecin conseil de la Sécurité sociale**. Elle est ensuite **notifiée à l'assuré par la caisse primaire d'assurance maladie (CPAM)** et communiquée à l'assureur lors de l'ouverture du dossier.
> 
> [FAQ_prevcorp.pdf] [RESUME_C83792.pdf] [RESUME_C39949.pdf]

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
2. `REGLEMENT_prevcorp` #17 (score 0.5175) — Article 15 — Invalidité Objet de la garantie. Lorsque l'assuré est reconnu invalide par la Sécurité sociale, l'assureur verse une rente complémentaire dont le montant dépend de la catégorie d'invalidité retenue. Catégories. La catégorie d'invalidité est déterminée par le médecin conseil de la Sécuri…
3. `RESUME_C83792` #5 (score 0.5007) — la franchise de 90 jours 78 % 72 % 66 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquida…
4. `RESUME_C73736` #5 (score 0.4982) — court sans interruption à compter du premier jour d'arrêt de travail. Période Tranche A Tranche B Tranche C À l'issue de la franchise de 90 jours 80 % 75 % 70 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de ma…
5. `RESUME_C39949` #5 (score 0.497) — franchise de 60 jours 70 % 65 % 60 % Les indemnités sont versées mensuellement à terme échu, sur présentation des décomptes de la Sécurité sociale, au souscripteur en cas de maintien de salaire ou directement à l'assuré dans les autres cas. Le versement cesse à la reprise du travail, à la liquidatio…

### RC22 (croisement)

- retrieval : KO — documents manquants : ['REGLEMENT_prevcorp']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : double échec (échec) — à corriger : vérifier question et scorer (I), puis traiter R et E séparément

**Réponse e2e**

> ## Délai de prescription — Garantie incapacité de travail
> 
> Je ne dispose pas d'information sur le délai de prescription spécifique au contrat C20077. Le document **RESUME_C20077.pdf** ne mentionne pas les délais de prescription.
> 
> En revanche, voici ce que les documents disponibles indiquent :
> 
> - **Règle générale** (CCN métallurgie, CCN santé/action sociale) : le délai de prescription est de **2 ans** à compter de l'événement, sans dérogation pour l'incapacité de travail. [NOTICE_CCN_metallurgie.pdf] [NOTICE_CCN_sante_action_sociale.pdf]
> 
> - **Exception sectorielle** : pour le secteur du **transport routier uniquement**, le délai est porté à **5 ans** pour la garantie incapacité de travail. [NOTICE_CCN_transport_routier.pdf]
> 
> > ⚠️ Sans connaître la CCN applicable au contrat C20077, il m'est impossible de trancher entre 2 ans et 5 ans. Je vous recommande de vérifier la convention collective rattachée à ce contrat pour appliquer le bon délai.

**Réponse isolée**

> Je ne dispose pas du contrat C20077 dans les documents fournis, et ne peux donc pas répondre spécifiquement à cette référence contractuelle.
> 
> Cependant, voici ce que les documents disponibles indiquent sur le délai de prescription pour l'incapacité de travail :
> 
> - **Règlement général PrevCorp** : le délai de prescription est de **2 ans** à compter de l'événement qui lui donne naissance. [REGLEMENT_prevcorp.pdf]
> 
> - **Notice CCN Transport Routier (IDCC 16)** : par dérogation expresse, *« le délai de prescription applicable à une action relative à la garantie incapacité de travail est porté à **5 ans** »*. [NOTICE_CCN_transport_routier.pdf]
> 
> > ⚠️ Le règlement général précise lui-même que *« des délais différents peuvent être fixés par la notice d'information propre à une convention collective, auquel cas ils se substituent au présent article »*. [REGLEMENT_prevcorp.pdf]
> 
> **En pratique** : si le contrat C20077 relève de la **CCN Transport Routier**, le délai applicable serait de **5 ans**. Pour tout autre convention collective, le délai de droit commun de **2 ans** s'appliquerait.
> 
> Pour une réponse certaine, il convient de consulter la notice d'information ou le résumé des garanties propre au contrat C20077.

Points en échec (e2e) : ['O0', 'O1']
Points en échec (isolé) : ['O0']

Chunks e2e récupérés :

1. `NOTICE_CCN_transport_routier` #12 (score 0.5295) — Article 10 — Prescription Toute action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré. Par dérogation, et compte tenu des spécifici…
2. `RESUME_C20077` #3 (score 0.4691) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
3. `NOTICE_CCN_metallurgie_distracteur` #12 (score 0.4689) — Article 10 — Prescription Toute action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré.
4. `NOTICE_CCN_metallurgie` #12 (score 0.4689) — Article 10 — Prescription Toute action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré.
5. `NOTICE_CCN_sante_action_sociale` #12 (score 0.4657) — Article 10 — Prescription Toute action dérivant du présent contrat est prescrite par 2 ans à compter de l'événement qui lui donne naissance. Ce délai est porté à 10 ans pour la garantie décès lorsque le bénéficiaire est une personne distincte de l'assuré.

### RC23 (croisement)

- retrieval : OK
- end_to_end : OK ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : sain (succès) — à corriger : rien

**Réponse e2e**

> ## Démarches et taux des indemnités journalières — Contrat C20077
> 
> ### 📋 Démarches à effectuer
> 
> Le salarié doit suivre les étapes suivantes [FAQ_prevcorp.pdf] :
> 
> 1. **Transmettre l'avis d'arrêt de travail** (initial et prolongations) à son **employeur dans les 48 heures** suivant sa délivrance
> 2. L'**employeur adresse ensuite à l'assureur**, dans un délai de **8 jours**, une déclaration d'arrêt de travail comprenant :
>    - Une copie de l'avis médical
>    - Les bulletins de salaire des trois derniers mois
> 3. Ce dossier peut être transmis **via l'espace adhérent en ligne** ou **par courrier** au service prestations (adresse sur la carte d'adhérent)
> 
> ---
> 
> ### 💰 Taux de versement des indemnités
> 
> Les indemnités journalières complémentaires sont versées **à l'issue de la franchise contractuelle** aux taux suivants [RESUME_C20077.pdf] :
> 
> | Tranche | Taux |
> |--------|------|
> | **Tranche A** | **78 %** du salaire brut de référence |
> | **Tranche B** | **72 %** du salaire brut de référence |
> 
> Ces montants sont versés **sous déduction** des prestations Sécurité sociale et de tout revenu de remplacement, **mensuellement à terme échu** [RESUME_C20077.pdf].
> 
> ### ⚠️ Fin du versement
> Les indemnités cessent en cas de : reprise du travail, liquidation d'une pension d'invalidité, décès ou départ à la retraite [RESUME_C20077.pdf].

**Réponse isolée**

> ## Démarches pour percevoir les indemnités journalières (contrat C20077)
> 
> ### 1. Démarches à effectuer
> 
> Le salarié doit **transmettre son avis d'arrêt de travail** (initial et prolongations) à son employeur **dans les 48 heures** suivant sa délivrance. [FAQ_prevcorp.pdf]
> 
> L'employeur adresse ensuite à l'assureur, **dans un délai de 8 jours** :
> - une déclaration d'arrêt de travail,
> - une copie de l'avis médical,
> - les bulletins de salaire des trois derniers mois.
> 
> Ce dossier peut être transmis via **l'espace adhérent en ligne** ou par **courrier au service prestations** (adresse sur la carte d'adhérent). [FAQ_prevcorp.pdf]
> 
> Le versement débute à l'issue de la **franchise contractuelle de 90 jours** (décomptés en jours calendaires dès le premier jour d'arrêt), sur présentation des **décomptes d'indemnités journalières de la Sécurité sociale**. [FAQ_prevcorp.pdf]
> 
> ---
> 
> ### 2. Taux de versement
> 
> | Période | Tranche A | Tranche B |
> |---|---|---|
> | À l'issue de la franchise contractuelle | **78 %** du salaire brut de référence | **72 %** du salaire brut de référence |
> 
> Ces indemnités sont versées **sous déduction des prestations Sécurité sociale** et de tout revenu de remplacement, mensuellement à terme échu. [RESUME_C20077.pdf]
> 
> > ⚠️ Le versement cesse à la reprise du travail, à la liquidation d'une pension d'invalidité, au décès ou au départ à la retraite. [RESUME_C20077.pdf]


Chunks e2e récupérés :

1. `FAQ_prevcorp` #5 (score 0.5733) — dans la limite de 12 mois, sans cotisation supplémentaire à votre charge. 6. Divers Je suis salarié du contrat C20077 et je me trouve en arrêt de travail : quelles démarches dois- je effectuer pour percevoir mes indemnités journalières complémentaires ? Vous devez transmettre votre avis d'arrêt de t…
2. `RESUME_C20077` #4 (score 0.5518) — de la période de franchise contractuelle, une indemnité journalière complémentaire lui est versée par l'assureur, sous déduction des prestations perçues au titre du régime obligatoire et de tout revenu de remplacement. La franchise court à compter du premier jour d'arrêt de travail continu et s'appr…
3. `RESUME_C20077` #3 (score 0.4834) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
4. `RESUME_C20077` #5 (score 0.4462) — cas d'invalidité reconnue par le médecin conseil de la Sécurité sociale, une rente est versée à l'assuré selon la catégorie déterminée, calculée en pourcentage du salaire annuel brut de référence. La catégorie est notifiée à l'assuré par la caisse primaire d'assurance maladie et communiquée à l'assu…
5. `RESUME_C20077` #1 (score 0.429) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…

### RC24 (croisement)

- retrieval : KO — points absents des chunks : ['O0', 'O1', 'O2']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : KO ⚠ à vérifier à la main
- diagnostic : double échec (échec) — à corriger : vérifier question et scorer (I), puis traiter R et E séparément

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles ne permettent pas de répondre précisément à cette question pour les raisons suivantes :
> 
> **Ce que les documents indiquent sur le contrat C87656 :**
> 
> Le résumé [RESUME_C87656.pdf] mentionne une **rente de conjoint de 15 % sur les tranches A et B**, versée au « conjoint ou partenaire de PACS survivant », ainsi qu'un **capital obsèques forfaitaire de 2 500 €**.
> 
> **Concernant le concubin spécifiquement :**
> 
> Aucun des extraits disponibles ne reconnaît explicitement le **concubin** (union libre) comme bénéficiaire de la rente de conjoint sur ce contrat. Les clauses bénéficiaires citées visent :
> - Le conjoint non séparé de corps [NOTICE_CCN_metallurgie.pdf]
> - Le partenaire lié par un PACS [NOTICE_CCN_metallurgie.pdf]
> 
> > ⚠️ Je ne trouve pas dans les documents disponibles de disposition reconnaissant le concubin comme bénéficiaire éligible à la rente de conjoint sur le contrat C87656, ni le montant qui lui serait applicable dans ce cas.
> 
> **Recommandation :** Il convient de vérifier les **conditions particulières du contrat C87656** et la notice d'information applicable, qui peuvent prévoir des dispositions spécifiques non couvertes par les extraits fournis.

**Réponse isolée**

> ## Bénéficiaire concubin et capital décès — Contrat C87656
> 
> ### Conditions de reconnaissance du concubin comme bénéficiaire
> 
> Le concubin n'est reconnu bénéficiaire qu'**à défaut de conjoint ou partenaire de PACS**, et sous condition de **résidence commune avec l'assuré au jour du décès**. [NOTICE_CCN_sante_action_sociale.pdf]
> 
> ---
> 
> ### Montant du capital décès
> 
> Le montant dépend de la **situation de famille** constatée au jour du décès. Or, la notice ne prévoit pas de ligne tarifaire spécifique pour le concubin dans le tableau des situations de famille. Les situations listées sont :
> 
> | Situation de famille | Tranche A | Tranche B |
> |---|---|---|
> | Célibataire, veuf ou divorcé sans personne à charge | 180 % | 180 % |
> | Marié ou pacsé sans personne à charge | 220 % | 220 % |
> 
> [RESUME_C87656.pdf]
> 
> > ⚠️ **Le concubin n'est pas assimilé au conjoint marié ou pacsé** dans ce tableau. En l'absence de précision contractuelle sur ce point, le taux applicable au concubin **ne peut pas être déterminé avec certitude sur la base des documents disponibles.**
> 
> ---
> 
> ### Majorations éventuelles
> 
> Si des **enfants à charge** sont reconnus au jour du sinistre, une **majoration de 25 % par enfant** s'applique sur le capital de base, sans limitation de rang. [RESUME_C87656.pdf]
> 
> ---
> 
> **En synthèse :** Je ne trouve pas dans les documents disponibles de taux explicitement attribué au concubin en tant que tel. Il conviendrait de consulter le résumé des garanties complet ou de contacter PrevCorp pour clarifier ce point.

Points en échec (e2e) : ['O0', 'O1', 'O2']
Points en échec (isolé) : ['O1']

Chunks e2e récupérés :

1. `NOTICE_CCN_metallurgie` #18 (score 0.4926) — Article 16 — Rente de conjoint Objet de la garantie. Le souscripteur peut, en complément des garanties de base, adhérir pour tout ou partie de son personnel à une garantie de rente de conjoint, versée au conjoint survivant en cas de décès de l'assuré. Montant des prestations. Les montants applicable…
2. `NOTICE_CCN_metallurgie_distracteur` #15 (score 0.4877) — Article 13 — Capital décès Objet de la garantie. En cas de décès de l'assuré, l'assureur verse au bénéficiaire désigné un capital. Montant des prestations. Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 140 % 140 % 110 % Marié ou pacsé sans enfant …
3. `NOTICE_CCN_metallurgie` #15 (score 0.4872) — Article 13 — Capital décès Objet de la garantie. En cas de décès de l'assuré, l'assureur verse au bénéficiaire désigné un capital. Montant des prestations. Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant …
4. `NOTICE_CCN_sante_action_sociale` #18 (score 0.4833) — Article 16 — Garanties optionnelles Objet de la garantie. Le souscripteur peut, en complément des garanties de base, adhérir pour tout ou partie de son personnel à une ou plusieurs garanties optionnelles, parmi lesquelles la rente de conjoint et la garantie obsèques. Montant des prestations. Les gar…
5. `RESUME_C87656` #5 (score 0.4819) — de conjoint En cas de décès de l'assuré, une rente viagère est versée à son conjoint ou partenaire de pacs survivant, sous réserve des conditions d'éligibilité définies par la notice d'information applicable au contrat. Garantie Tranche A Tranche B Rente de conjoint 15 % 15 % Garantie obsèques Un ca…

### RC25 (fait_simple)

- retrieval : KO — documents manquants : ['NOTICE_CCN_transport_routier'] — points absents des chunks : ['O0', 'O1']
- end_to_end : KO ⚠ à vérifier à la main
- isolated : OK ⚠ à vérifier à la main
- diagnostic : échec de retrieval (échec) — à corriger : chunking, ingestion, requête

**Réponse e2e**

> ## Application de la clause bénéficiaire type sur le contrat C20077
> 
> Les documents disponibles relatifs au contrat C20077 **ne précisent pas explicitement** la clause bénéficiaire type applicable en l'absence de désignation personnalisée, ni le traitement spécifique du concubin.
> 
> ---
> 
> **Ce que les documents indiquent sur un contrat comparable :**
> 
> Le contrat C73736 précise que :
> 
> > *"Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la **clause bénéficiaire type du Règlement PrevCorp** s'applique de plein droit."* [RESUME_C73736.pdf]
> 
> Cette mention renvoie au **Règlement PrevCorp**, document qui n'est pas fourni dans les extraits disponibles.
> 
> ---
> 
> ## Conclusion
> 
> Je ne trouve pas cette information dans les documents disponibles pour le contrat C20077 spécifiquement. Pour déterminer à qui serait versé le capital décès en l'absence de désignation (et en l'absence de reconnaissance du concubin), il conviendrait de **consulter le Règlement PrevCorp**, qui définit la clause bénéficiaire type applicable par défaut.
> 
> > 💡 **Recommandation** : Se référer directement au Règlement PrevCorp ou contacter le gestionnaire du contrat C20077.

**Réponse isolée**

> ## Versement du capital décès en l'absence de désignation
> 
> La notice est explicite sur ce point. En l'absence de désignation particulière de bénéficiaire, la clause bénéficiaire type s'applique dans l'ordre suivant :
> 
> 1. **Au conjoint de l'assuré** (époux/épouse ou partenaire de PACS)
> 2. **À défaut, à ses enfants**, par parts égales
> 3. **À défaut, à ses héritiers**
> 
> [NOTICE_CCN_transport_routier.pdf — Article 14, Clause bénéficiaire type]
> 
> ---
> 
> **Point important à noter :** Le concubin n'est **pas reconnu** comme bénéficiaire dans le cadre de cette convention. Le bulletin d'adhésion individuel ne prévoit d'ailleurs aucune rubrique pour la déclaration d'un concubin, la convention ne lui reconnaissant pas la qualité ouvrant droit aux garanties liées à la situation de famille.
> 
> [NOTICE_CCN_transport_routier.pdf — Annexe II]
> 
> > ⚠️ Si le salarié souhaite que son concubin perçoive le capital décès, **la seule solution est d'effectuer une désignation bénéficiaire personnalisée**, par écrit, en précisant l'identité du bénéficiaire, son rang de priorité et sa quote-part. Cette désignation peut être modifiée à tout moment. [NOTICE_CCN_transport_routier.pdf — Article 14, Clause bénéficiaire personnalisée]

Points en échec (e2e) : ['O0', 'O1']

Chunks e2e récupérés :

1. `RESUME_C20077` #1 (score 0.5232) — n° C20077 Convention collective nationale du transport routier — Personnel non cadre Ce document présente de façon synthétique les garanties de prévoyance collective souscrites au titre du contrat référencé ci-dessus. Les taux indiqués sont exprimés en pourcentage du salaire annuel brut de référence…
2. `RESUME_C73736` #2 (score 0.4688) — de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 150 % 150 % 120 % Marié ou pacsé sans enfant à charge 180 % 180 % 140 % Aucune désignation bénéficiaire personnalisée n'a été notifiée pour ce contrat ; la clause bénéficiaire type du Règlement PrevCorp s'appliq…
3. `RESUME_C20077` #3 (score 0.4514) — Catégorie | Tranche A | Tranche B Invalidité 1re catégorie | 50 % | 50 % Invalidité 2e catégorie | 75 % | 75 % Invalidité 3e catégorie | 100 % | 100 % Catégorie de personnel | Tranche A | Tranche B Non cadre | 1,20 % | 1,85 % Majorations familiales Le capital décès toutes causes fait l'objet d'une m…
4. `NOTICE_CCN_metallurgie_distracteur` #15 (score 0.4451) — Article 13 — Capital décès Objet de la garantie. En cas de décès de l'assuré, l'assureur verse au bénéficiaire désigné un capital. Montant des prestations. Situation de famille Tranche A Tranche B Tranche C Célibataire, veuf, divorcé sans enfant à charge 140 % 140 % 110 % Marié ou pacsé sans enfant …
5. `RESUME_C20077` #2 (score 0.4394) — décès Garantie Tranche A Tranche B Invalidité absolue et définitive (anticipation du capital décès) 100 % 100 % Décès accidentel (capital additionnel) 100 % 100 % Double effet (décès simultané ou postérieur du conjoint) 100 % 100 % Obsèques (capital forfaitaire) 2 000 € 2 000 € Rente éducation Lorsq…
