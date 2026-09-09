# docs/ inatteignable depuis le worktree dev alors qu'un DoD exige de l'éditer

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-02

## Récit
**En tant que** Guillaume,
**je veux** Rendre docs/ accessible en écriture à la session dev (le versionner, ou le monter rw), ou bien interdire au cadrage de mettre dans un DoD un chemin que la session dev ne peut pas écrire.,
**afin de** Le DoD de STORY-004 exige de modifier docs/stories/STORY-001-*.md, fichier que la story liste explicitement dans sa « Surface déclarée » et qu'AC8 autorise dans le diff. Or le sandbox de la session dev monte tout ce qui est hors du worktree en lecture seule (EROFS), et `docs/` n'est suivi par git nulle part — il n'existe donc pas dans le worktree. Aucune tentative ne peut satisfaire ce DoD, et la review le compte en `major` à chaque fois : trois tentatives brûlées sur un item structurellement inatteignable.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-004, When il est instruit, Then Rendre docs/ accessible en écriture à la session dev (le versionner, ou le monter rw), ou bien interdire au cadrage de mettre dans un DoD un chemin que la session dev ne peut pas écrire..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-004 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
