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
- `contrat_id` ou `segment_nom` : selon le type (résumé → contrat_id ; notice_ccn → segment_nom ; règlement → aucun ; **FAQ → toujours `prevcorp`, identifiant fixe** — un seul fichier FAQ existe dans tout le corpus, cf. plan type FAQ)
- `contenu_a_couvrir` : la ou les questions de l'eval set (`rag_questions_v0_25.yml`) que ce
  document doit permettre de résoudre — c'est ce qui pilote le contenu, pas l'inverse
  (cf. décision Phase 3 remaniée : le corpus est généré après les questions)
- `est_distracteur` : booléen — si vrai, le document doit ressembler structurellement à un
  document pertinent mais ne pas contenir l'information qui répond aux questions ciblées

## Étapes

1. Lire le plan type de référence pour le `type` demandé.
2. Vérifier que `contenu_a_couvrir` est cohérent avec le type (ex : un résumé de garanties
   ne peut pas répondre à une question de processus administratif — rediriger vers FAQ).
   **Si aucune question de `rag_questions_v0_25.yml` ne correspond au sujet demandé,
   s'arrêter et le signaler avant de générer** — ne jamais rédiger un document "à partir
   du plan type, sans question cible". Un corpus généré sans ancrage éval reproduit le
   blocage diagnostiqué en Phase 3 remaniée (prose générique, rien à mesurer). Demander à
   l'utilisateur soit de préciser une question cible, soit de confirmer explicitement qu'il
   veut un document hors-éval (cas rare, ex : contenu de contexte non testé).
3. **Cas particulier FAQ** : avant de rédiger, vérifier si `corpus/FAQ_prevcorp.pdf` (ou le
   HTML source correspondant) existe déjà. S'il existe, lire son contenu et ajouter la
   nouvelle thématique à la structure existante, sans dupliquer une thématique déjà
   couverte ni écraser silencieusement les thèmes déjà présents. Un seul fichier FAQ doit
   exister dans le corpus à tout moment. **Toujours conserver le HTML source** (ex :
   `corpus_src/FAQ_prevcorp.html`, hors du dossier temporaire de session) — sans lui, une
   extension future doit reparser le PDF, ce qui n'est pas fiable.
4. Rédiger le contenu HTML en respectant strictement la structure du plan type : mêmes
   sections dans le même ordre, même style de numérotation, mêmes conventions de tableaux.
   Contenu 100% inventé (montants, taux, noms d'assureur fictif, dates) — jamais de contenu
   copié ou reformulé depuis les documents publics ayant servi de référence structurelle.
5. Si `est_distracteur` est vrai, s'assurer que l'information recherchée par
   `contenu_a_couvrir` est absente, tout en gardant une structure et un vocabulaire crédibles.
6. **Ne jamais commenter, justifier ou signaler une information comme remarquable.**
   Le document doit se comporter comme un vrai document métier qui ignore totalement
   qu'il sert de matériel d'évaluation :
   - Un fait ne doit apparaître **qu'une seule fois** dans le document, à l'endroit où il
     appartient naturellement (table, article, paragraphe) — jamais répété ou reformulé
     ailleurs "pour clarifier", même en note de bas de page ou en astérisque.
   - Une absence délibérée (garantie non souscrite, information hors périmètre du type de
     document) doit rester **silencieuse** : ne jamais écrire une phrase qui explique ou
     justifie pourquoi une information n'est pas là. Un vrai document ne parle pas de ce
     qu'il ne contient pas.
   - Aucune formulation de type "il est à noter que", "important : ", "pour rappel" autour
     d'un chiffre ou d'une clause — ça revient à surligner la réponse pour le retriever.
   - Ne jamais ajouter de pied de page identifiant l'assureur (nom de société fictif,
     forme juridique, capital social, numéro RCS, siège social) : ça n'apporte rien à
     l'éval et ajoute du bruit générationnel pour rien, quel que soit le type de document.
7. Appeler `${CLAUDE_SKILL_DIR}/scripts/render.py` pour convertir le HTML en PDF via
   weasyprint et écrire le fichier dans `corpus/`. **Conserver systématiquement le HTML
   source** dans `corpus_src/<même_nom>.html` (créer le dossier s'il n'existe pas), pour
   tout type de document — pas seulement la FAQ. Une régénération ou une correction
   ultérieure doit pouvoir repartir du HTML, jamais reparser un PDF.
8. Nommer le fichier selon la convention `<TYPE>_<identifiant>.pdf`
   (ex : `RESUME_CTR00296.pdf`, `NOTICE_CCN_metallurgie.pdf`, `FAQ_prevcorp.pdf`).

## Pièges connus

- Ne jamais produire un document qui répond à une question hors du périmètre couvert par
  son `type` (une FAQ ne contient pas de chiffres de garanties précis).
- Un distracteur mal conçu (qui répond quand même partiellement à la question) invalide
  l'éval — en cas de doute, demander confirmation avant de générer. **Avant de finaliser un
  distracteur, rechercher explicitement dans le contenu généré les termes liés à la famille
  de la question ciblée** (ex : "invalid", "IPP", "IAD", "IPT" pour une question invalidité)
  et confirmer leur absence, en écartant les faux positifs lexicaux (ex : "souscriptrice").
- **Le document ne doit jamais trahir qu'il a été conçu pour une question d'éval précise.**
  Une note qui répète un chiffre déjà présent, ou une phrase qui justifie une absence,
  est un signal artificiel qui rend le retrieval trivialement réussissable — ça invalide
  le test autant qu'un distracteur qui répond à la question. Relire le document généré en
  se demandant : "un vrai document métier écrirait-il cette phrase ?" Si la réponse est non,
  la supprimer.