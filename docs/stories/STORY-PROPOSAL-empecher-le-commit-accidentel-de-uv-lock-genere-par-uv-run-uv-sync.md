# Empêcher le commit accidentel de uv.lock généré par uv run/uv sync

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-06

## Récit
**En tant que** Guillaume,
**je veux** Soit ajouter 'uv.lock' au .gitignore racine (mais hors périmètre de cette story, AC3 interdit d'y toucher), soit — plus robuste — faire en sorte que le pas de commit du runner ne stage que les chemins listés dans files_touched[] plutôt qu'un git add -A, pour ne jamais capturer d'artefacts d'outillage générés pendant les checks.,
**afin de** uv run/uv sync recrée systématiquement un uv.lock local des qu'il tourne dans un projet uv, même sans dépendances. Si le pas de commit du runner fait un git add large (ex: git add -A) après l'exécution des checks, ce fichier repasse suivi à chaque tentative et recasse AC3 en boucle (observé sur au moins 2 tentatives de cette story). Un gitignore d'entrée de dépôt pour uv.lock (ou un git add ciblé aux seuls fichiers listés dans files_touched) éviterait la régression systématique.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Soit ajouter 'uv.lock' au .gitignore racine (mais hors périmètre de cette story, AC3 interdit d'y toucher), soit — plus robuste — faire en sorte que le pas de commit du runner ne stage que les chemins listés dans files_touched[] plutôt qu'un git add -A, pour ne jamais capturer d'artefacts d'outillage générés pendant les checks..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
