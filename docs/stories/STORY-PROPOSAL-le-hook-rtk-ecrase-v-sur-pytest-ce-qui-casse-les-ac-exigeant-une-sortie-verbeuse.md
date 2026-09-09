# Le hook RTK écrase `-v` sur pytest, ce qui casse les AC exigeant une sortie verbeuse

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-02

## Récit
**En tant que** Guillaume,
**je veux** Faire préserver par le hook RTK les flags de verbosité explicites (`-v`/`-vv`/`--verbose`) au lieu de les remplacer par `-q`, ou signaler explicitement la réécriture à l'agent.,
**afin de** Le hook RTK réécrit `python -m pytest -v` en `pytest --tb=short -q` et supprime le `-v`. AC7 de cette story exige nommément la sortie verbeuse (noms de tests visibles) comme garde-fou anti-story-déclarée-à-vide. La tentative 2 a donc été pénalisée d'un finding `minor` pour un format de sortie que le harness lui avait imposé à son insu — l'agent croyait avoir exécuté la commande demandée. Le contournement (`rtk proxy`) existe mais n'est découvrable que par lecture attentive du CLAUDE.md global.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-004, When il est instruit, Then Faire préserver par le hook RTK les flags de verbosité explicites (`-v`/`-vv`/`--verbose`) au lieu de les remplacer par `-q`, ou signaler explicitement la réécriture à l'agent..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-004 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
