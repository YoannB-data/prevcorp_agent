# Plan type — FAQ

Structure inspirée de la FAQ publique MASA (Harmonie Mutuelle/Mutex). Structure et
vocabulaire uniquement — contenu 100% synthétique.

Document transversal, unique dans le corpus (pas de déclinaison par `contrat_id` ou
`segment_nom`) — couvre les processus administratifs communs à tous les contrats.

## Structure obligatoire

1. **Page de garde** : titre "FOIRE AUX QUESTIONS PRÉVOYANCE", date de version, liste des
   thématiques (rendues comme des sections cliquables dans le PDF source, mais peuvent
   rester une simple table des matières en PDF statique).
2. **Une section par thématique**, dans cet ordre pour PrevCorp :
   - Présentation (qu'est-ce que la prévoyance, garanties en général)
   - Modalités d'adhésion (délais, questionnaire médical, carence)
   - Cotisations (montant, calcul, précompte, revalorisation)
   - Garanties (explications générales, pas de chiffres précis — renvoyer au Résumé)
   - Résiliation (modalités, portabilité)
   - Divers
3. **Format question/réponse** : chaque question en gras/titre, réponse en paragraphe
   direct juste en dessous. Pas de renvoi à une autre page pour la réponse elle-même.
4. Optionnel : annexe listant les textes de référence (décrets, accords) si pertinent pour
   le contexte fictif PrevCorp.

## Conventions de forme

- Ton direct, à la deuxième personne, orienté service ("Comment payer ma cotisation ?").
- Ne jamais inclure de chiffre de garantie précis (montant, taux, seuil) — ça appartient au
  Résumé des garanties. Si une question RAG nécessite un chiffre précis, elle ne doit pas
  être couverte par ce type de document ; c'est un signal pour vérifier `contenu_a_couvrir`
  en amont (étape 2 du SKILL.md).
- Les réponses restent courtes (un à trois paragraphes) — pas de sous-articles numérotés
  comme dans la Notice.
