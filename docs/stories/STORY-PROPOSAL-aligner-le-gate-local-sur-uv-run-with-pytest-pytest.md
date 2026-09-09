# Aligner le gate local sur `uv run --with pytest pytest`

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-06

## Récit
**En tant que** Guillaume,
**je veux** Si le gate de check pytest du runner peut être ajusté pour utiliser `uv run --with pytest pytest` (comme le workflow CI qu'il génère lui-même), les stories n'auraient plus besoin de déclarer pytest comme dépendance de projet juste pour satisfaire le gate — cohérent avec l'intention initiale 'projet python sans dépendance de test déclarée'.,
**afin de** Le gate local du runner invoque `uv run pytest` (sans --with), incohérent avec le template CI généré (.github/workflows/autopilot-ci.yml) qui utilise `uv run --with pytest pytest` précisément pour ne pas exiger de dépendance de test déclarée. Ça a fait échouer 3 tentatives consécutives sur ce canari avant que la dépendance ne soit ajoutée en dur.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Si le gate de check pytest du runner peut être ajusté pour utiliser `uv run --with pytest pytest` (comme le workflow CI qu'il génère lui-même), les stories n'auraient plus besoin de déclarer pytest comme dépendance de projet juste pour satisfaire le gate — cohérent avec l'intention initiale 'projet python sans dépendance de test déclarée'..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
