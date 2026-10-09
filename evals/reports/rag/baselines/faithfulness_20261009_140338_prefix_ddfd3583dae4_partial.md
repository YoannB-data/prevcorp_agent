# Rapport faithfulness (juge maison)

- Date : 2026-10-09T14:03:38
- Hash du YAML : ddfd3583dae4
- Modèle : claude-sonnet-4-6
- Modèle du juge : claude-sonnet-4-6
- Temperature : 0.0
- k : 5
- Variante d'ingestion : prefix (vérifiée contre la collection)

## Synthèse

Questions : 4 dont 0 en erreur d'I/O (exclues des moyennes).

Rapport PARTIEL (--ids) : aucune moyenne calculée.

## Détail par question

### RC17 (sans_reponse)

- faithfulness : 1.00 (3 affirmations)
- affirmations :
  - A1 [appuyée] Sur le contrat C73736, le taux de cotisation global pour le personnel cadre en Tranche A est de 1,60 %.
  - A2 [appuyée] Sur le contrat C73736, le taux de cotisation global pour le personnel cadre en Tranche B est de 2,45 %.
  - A3 [appuyée] Sur le contrat C73736, le taux de cotisation global pour le personnel cadre en Tranche C est de 2,45 %.

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
> Aucune ventilation de ces cotisations par garantie (notamment pour la rente de conjoint spécifiquement) n'est présente dans les extraits fournis. Pour obtenir cette décomposition, il conviendrait de consulter la **notice d'information complète** ou les **conditions particulières** du contrat C73736.

### RC20 (croisement)

- faithfulness : N/A (aucune affirmation) (0 affirmations)

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles **ne permettent pas de répondre à cette question**.
> 
> Les extraits fournis indiquent uniquement le taux applicable :
> 
> > *« Invalidité 1re catégorie | 50 % | 50 % »* (Tranche A et Tranche B) [RESUME_C20077.pdf]
> 
> Cependant, **aucun élément dans ces extraits ne précise** si ce taux de 50 % constitue :
> - le taux de base du Règlement de prévoyance de la CCN du transport routier, ou
> - une dérogation (en hausse ou en baisse) par rapport à ce Règlement.
> 
> Pour répondre à cette question, il faudrait disposer du **Règlement de prévoyance de la CCN du transport routier** (ou de l'accord de branche applicable) afin de comparer le taux conventionnel de référence avec celui retenu dans le contrat C20077.
> 
> Je ne trouve pas cette information dans les documents disponibles.

### RC24 (croisement)

- faithfulness : 1.00 (3 affirmations)
- affirmations :
  - A1 [appuyée] Le concubin peut être bénéficiaire du capital décès sous condition de résidence commune avec l'assuré au jour du décès, selon la CCN Action Sociale.
  - A2 [appuyée] Le contrat C87656 prévoit une rente de conjoint de 15 % sur la Tranche A et la Tranche B.
  - A3 [appuyée] Le contrat C87656 prévoit un capital obsèques forfaitaire de 2 500 €.

**Réponse e2e**

> ## Réponse
> 
> Les documents disponibles ne permettent pas de répondre précisément à cette question combinée.
> 
> Voici ce qui est documenté séparément :
> 
> **Sur la reconnaissance du concubin comme bénéficiaire :**
> La notice CCN Action Sociale précise que le concubin peut être bénéficiaire du capital décès **sous condition de résidence commune avec l'assuré au jour du décès**. [NOTICE_CCN_sante_action_sociale.pdf]
> 
> **Sur les montants du contrat C87656 :**
> Le résumé du contrat C87656 mentionne uniquement la **rente de conjoint** (15 % sur Tranche A et B) et le **capital obsèques forfaitaire de 2 500 €**, mais **ne précise pas le montant du capital décès** versé au bénéficiaire (conjoint, partenaire ou concubin). [RESUME_C87656.pdf]
> 
> ---
> 
> > **Je ne trouve pas dans les documents disponibles le montant du capital décès spécifiquement applicable au concubin sur le contrat C87656.**
> 
> Pour obtenir cette information, il conviendrait de consulter la **notice d'information complète** rattachée au contrat C87656, qui devrait détailler les montants du capital décès selon la situation familiale.

### RC25 (fait_simple)

- faithfulness : 1.00 (9 affirmations)
- affirmations :
  - A1 [appuyée] Le contrat C20077 relève de la Convention collective nationale du transport routier — Personnel non cadre.
  - A2 [appuyée] La notice CCN Agriculture prévoit, à défaut de désignation particulière, que le capital décès est versé en premier lieu au conjoint non séparé de corps ou au partenaire pacsé.
  - A3 [appuyée] La notice CCN Agriculture prévoit, à défaut de conjoint ou partenaire pacsé, que le capital décès est versé aux enfants nés ou à naître, par parts égales.
  - A4 [appuyée] La notice CCN Agriculture prévoit, à défaut d'enfants, que le capital décès est versé aux parents.
  - A5 [appuyée] La notice CCN Agriculture prévoit, à défaut de parents, que le capital décès est versé aux autres ascendants.
  - A6 [appuyée] La notice CCN Agriculture prévoit, à défaut d'autres ascendants, que le capital décès est versé aux héritiers.
  - A7 [appuyée] Le concubin n'apparaît pas dans la clause bénéficiaire type de la notice CCN Agriculture.
  - A8 [appuyée] La notice CCN Santé/Action sociale intègre le concubin comme bénéficiaire sous condition de résidence commune.
  - A9 [appuyée] Sur le contrat C20077, le concubin n'est pas reconnu bénéficiaire en l'absence de désignation personnalisée.

**Réponse e2e**

> ## Capital décès sans désignation bénéficiaire — Contrat C20077
> 
> Le contrat C20077 relève de la **Convention collective nationale du transport routier — Personnel non cadre**.
> 
> Les documents disponibles pour ce contrat [RESUME_C20077.pdf] ne précisent pas la clause bénéficiaire type applicable.
> 
> En revanche, la notice de référence la plus proche en matière de clause bénéficiaire type est celle de la CCN Agriculture [NOTICE_CCN_agriculture.pdf], qui prévoit l'ordre suivant à défaut de désignation particulière :
> 
> 1. **Le conjoint** non séparé de corps ou le **partenaire pacsé**
> 2. À défaut, les **enfants** nés ou à naître, par parts égales
> 3. À défaut, les **parents**
> 4. À défaut, les **autres ascendants**
> 5. À défaut, les **héritiers**
> 
> > ⚠️ **Point important** : Le concubin **n'apparaît pas** dans cette clause bénéficiaire type (contrairement à la notice CCN Santé/Action sociale [NOTICE_CCN_sante_action_sociale.pdf] qui l'intègre sous condition de résidence commune). Pour le contrat C20077, le concubin ne serait donc **pas bénéficiaire** en l'absence de désignation personnalisée.
> 
> **Je ne trouve pas dans les documents disponibles** la clause bénéficiaire type propre au contrat C20077 de manière explicite. Il est recommandé de se référer aux **conditions générales ou à la notice spécifique** de ce contrat pour confirmation.
