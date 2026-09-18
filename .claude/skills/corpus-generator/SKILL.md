---
name: corpus-generator
description: Génère un document PDF synthétique du corpus documentaire PrevCorp (Règlement, Notice CCN, Résumé des garanties, ou FAQ) à partir d'une spec. Utiliser quand on doit produire ou régénérer un document du corpus RAG PrevCorp, ou ajouter un distracteur au corpus.
---

# corpus-generator

Génère un document PDF du corpus PrevCorp synthétique, conforme au plan type de son
catégorie, à partir d'une spec fournie par l'utilisateur.

## Quand utiliser ce skill

- L'utilisateur demande de générer, créer ou régénérer un document du corpus PrevCorp
  (règlement, notice CCN, résumé de garanties, FAQ).
- L'utilisateur demande d'ajouter un distracteur au corpus RAG.
- Le runner d'éval RAG (L3.4) signale un gap de couverture nécessitant un nouveau document.

Ne pas utiliser pour produire du contenu métier réel ou pour toute donnée qui ne soit pas
100% synthétique (cf. règles d'or sécurité du projet).

## Types de documents et plans type

Ce skill couvre 3 catégories de documents (cf. décision Phase 3 remaniée — les catégories
Notes techniques et Circulaires sont hors scope) :

| Type | Granularité | Référence |
|---|---|---|
| `reglement` / `notice_ccn` | Un document générique partagé par tous les contrats, ou par `segment_nom` s'il existe une CCN spécifique | [references/plan-type-notice.md](references/plan-type-notice.md) |
| `resume_garanties` | Un document par `contrat_id`, chiffres exacts | [references/plan-type-resume.md](references/plan-type-resume.md) |
| `faq` | Un document transversal, non lié à un contrat | [references/plan-type-faq.md](references/plan-type-faq.md) |

Avant de générer, lire le plan type correspondant au type demandé — il fixe la structure
obligatoire (sections, numérotation, format des tableaux) que le document généré doit suivre.

## Entrée attendue (spec)

L'utilisateur (ou un appel programmatique) fournit :

- `type` : un des 3 types ci-dessus
- `contrat_id` ou `segment_nom` : selon le type (résumé → contrat_id ; notice_ccn → segment_nom ; règlement/FAQ → aucun)
- `contenu_a_couvrir` : la ou les questions de l'eval set (`rag_questions_v0_25.yml`) que ce
  document doit permettre de résoudre — c'est ce qui pilote le contenu, pas l'inverse
  (cf. décision Phase 3 remaniée : le corpus est généré après les questions)
- `est_distracteur` : booléen — si vrai, le document doit ressembler structurellement à un
  document pertinent mais ne pas contenir l'information qui répond aux questions ciblées

## Étapes

1. Lire le plan type de référence pour le `type` demandé.
2. Vérifier que `contenu_a_couvrir` est cohérent avec le type (ex : un résumé de garanties
   ne peut pas répondre à une question de processus administratif — rediriger vers FAQ).
3. Rédiger le contenu HTML en respectant strictement la structure du plan type : mêmes
   sections dans le même ordre, même style de numérotation, mêmes conventions de tableaux.
   Contenu 100% inventé (montants, taux, noms d'assureur fictif, dates) — jamais de contenu
   copié ou reformulé depuis les documents publics ayant servi de référence structurelle.
4. Si `est_distracteur` est vrai, s'assurer explicitement que l'information recherchée par
   `contenu_a_couvrir` est absente, tout en gardant une structure et un vocabulaire crédibles.
5. Appeler `${CLAUDE_SKILL_DIR}/scripts/render.py` pour convertir le HTML en PDF via
   weasyprint et écrire le fichier dans `corpus/`.
6. Nommer le fichier selon la convention `<TYPE>_<identifiant>.pdf`
   (ex : `RESUME_CTR00296.pdf`, `NOTICE_CCN_metallurgie.pdf`, `FAQ_administrative.pdf`).

## Pièges connus

- Ne jamais produire un document qui répond à une question hors du périmètre couvert par
  son `type` (une FAQ ne contient pas de chiffres de garanties précis).
- Un distracteur mal conçu (qui répond quand même partiellement à la question) invalide
  l'éval — en cas de doute, demander confirmation avant de générer.
