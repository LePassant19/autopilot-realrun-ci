# STORY-000 — CI de base (story système, insérée par le runner)

> status: ready | epic: EPIC-system | estimate: S | depends_on: — | updated: (runner)

## Récit
**En tant que** runner autopilot, **je veux** un workflow CI minimal (tests + typecheck +
lint détectés depuis pyproject/package.json) **afin que** chaque PR de ce run ait un
oracle CI (STORY-009 AC2).

## Critères d'acceptation
- **AC1** — Given le repo sans workflow, When cette story est livrée, Then
  `.github/workflows/autopilot-ci.yml` (rendu depuis `runner/templates/ci.yml`, étape
  déterministe du runner — jamais un agent) est poussé en PR draft.
