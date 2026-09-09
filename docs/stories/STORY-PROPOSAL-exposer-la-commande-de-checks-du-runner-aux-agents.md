# Exposer la commande de checks du runner aux agents

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-06

## Récit
**En tant que** Guillaume,
**je veux** Ajouter docs/method/checks.md et l'inclure dans le contexte de brief. Alternative plus robuste : faire échouer le runner avec un message explicite (« pytest introuvable : utilisez `uv run --with pytest pytest`, ne déclarez pas pytest dans pyproject.toml ») plutôt qu'un `Failed to spawn: pytest` brut.,
**afin de** Le dépôt est volontairement « sans dépendance de test déclarée » (commit d'init cc352a0), et la CI générée invoque `uv run --with pytest pytest`. Mais rien n'indique à l'agent quelle commande le runner exécute pour ses checks locaux. Trois tentatives se sont perdues sur ce point : la tentative 1 a déclaré pytest dans pyproject.toml pour débloquer `uv run pytest` et s'est fait recaler sur AC3.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Ajouter docs/method/checks.md et l'inclure dans le contexte de brief. Alternative plus robuste : faire échouer le runner avec un message explicite (« pytest introuvable : utilisez `uv run --with pytest pytest`, ne déclarez pas pytest dans pyproject.toml ») plutôt qu'un `Failed to spawn: pytest` brut..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
