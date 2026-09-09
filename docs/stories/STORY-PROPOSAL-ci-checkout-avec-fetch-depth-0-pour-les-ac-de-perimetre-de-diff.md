# CI : checkout avec fetch-depth 0 pour les AC de périmètre de diff

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-09

## Récit
**En tant que** Guillaume,
**je veux** Dans runner/templates/ci.yml, ajouter `with: fetch-depth: 0` à l'étape `actions/checkout@v4`. Le fichier généré .github/workflows/autopilot-ci.yml est un chemin protégé (STORY-011 AC1) : le changement doit venir du template côté runner, pas d'un agent.,
**afin de** Le template CI génère `actions/checkout@v4` sans `fetch-depth`, donc un clone superficiel sans ref `main` : tout test qui prouve un AC de périmètre (« aucun fichier hors X n'est modifié ») y échoue ou doit se neutraliser. C'est ce qui a rendu la CI rouge sur la tentative 2 de STORY-009 alors que la gate locale était verte, sans que la cause soit lisible dans les findings. Avec l'historique, la preuve d'AC3 s'exécute réellement en CI au lieu d'être skippée.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Dans runner/templates/ci.yml, ajouter `with: fetch-depth: 0` à l'étape `actions/checkout@v4`. Le fichier généré .github/workflows/autopilot-ci.yml est un chemin protégé (STORY-011 AC1) : le changement doit venir du template côté runner, pas d'un agent..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
