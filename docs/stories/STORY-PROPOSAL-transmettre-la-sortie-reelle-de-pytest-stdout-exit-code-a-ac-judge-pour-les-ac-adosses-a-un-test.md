# Transmettre la sortie réelle de pytest (stdout + exit code) à ac_judge pour les AC adossés à un test

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-09

## Récit
**En tant que** Guillaume,
**je veux** Faire porter par le runner, en sortie de la gate `checks`, le stdout combiné + l'exit code de la commande de test exécutée, et les attacher tels quels comme preuve pour chaque AC dont le test associé a été collecté et exécuté par cette commande — au lieu (ou en complément) du constat AST actuel. Alternative : accorder à ac_judge un droit d'exécution en lecture seule limité à la commande de test déclarée par le runner.,
**afin de** Actuellement, pour un AC prouvé par un test nommé test_acN_*, ac_judge ne reçoit qu'un constat statique (« assertion réelle vérifiée par AST : True ») sans exit code ni sortie d'exécution. Quand ac_judge tourne dans un sandbox où Bash est refusé (constaté ici : 3 tentatives de relance de pytest toutes bloquées par la policy don't-ask-mode), il ne peut ni faire confiance à la gate `checks` (qui, elle, a bien exécuté `uv run --with pytest pytest` avec succès : 3 passed) ni re-exécuter lui-même la preuve. Tout AC formulé « When pytest tourne » devient alors structurellement not_proven, indépendamment de la justesse du code — comme observé sur STORY-009 (AC2, AC3) alors que les gates checks et review avaient toutes deux validé le même code.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Faire porter par le runner, en sortie de la gate `checks`, le stdout combiné + l'exit code de la commande de test exécutée, et les attacher tels quels comme preuve pour chaque AC dont le test associé a été collecté et exécuté par cette commande — au lieu (ou en complément) du constat AST actuel. Alternative : accorder à ac_judge un droit d'exécution en lecture seule limité à la commande de test déclarée par le runner..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
