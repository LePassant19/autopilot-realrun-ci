# Sessions ac_judge sans accès Bash empêchent toute preuve exécutée citable

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-09

## Récit
**En tant que** Guillaume,
**je veux** Donner aux sessions ac_judge soit un accès Bash en lecture seule suffisant pour rejouer la commande de test déclarée par le runner, soit un mécanisme officiel pour lire un artefact d'exécution déjà produit par la session d'implémentation/checks (ex. un chemin standard comme .autopilot/runs/<run>/<story>/pytest_output.txt) sans avoir besoin d'exécuter quoi que ce soit elle-même.,
**afin de** Sur STORY-009 tentative 1, checks et review sont passés (pytest vert, exit 0) mais ac_judge a marqué AC1/AC2/AC3 not_proven uniquement parce que sa propre session sandbox refusait tout appel Bash ("don't ask mode"). C'est un faux négatif systémique : toute story, même triviale et correctement implémentée, échouerait de la même façon tant que ce mode reste actif pour les sessions ac_judge. Cela consomme des tentatives pour rien et masque les vrais échecs.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Donner aux sessions ac_judge soit un accès Bash en lecture seule suffisant pour rejouer la commande de test déclarée par le runner, soit un mécanisme officiel pour lire un artefact d'exécution déjà produit par la session d'implémentation/checks (ex. un chemin standard comme .autopilot/runs/<run>/<story>/pytest_output.txt) sans avoir besoin d'exécuter quoi que ce soit elle-même..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
