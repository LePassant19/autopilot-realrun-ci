# STORY-009 — Canari : consigner la date du jour dans CANARY.md

> status: ready | epic: EPIC-canary | estimate: S | priority: must | depends_on: — | updated: 2026-09-05

## Récit
**En tant que** runner autopilot, **je veux** qu'une story triviale traverse dev → checks → gates → PR → CI, **afin de** prouver chaque matin que le moteur tourne avant de dépenser sur une vraie story (harness STORY-048).

## Critères d'acceptation
- **AC1** — Given le dépôt, When la story est implémentée, Then un fichier `CANARY.md` existe à la racine et contient une ligne `canary YYYY-MM-DD` avec la date du jour (UTC).
- **AC2** — Given `tests/test_canary.py`, When `pytest` tourne, Then un test vérifie que `CANARY.md` contient une ligne `canary ` suivie d'une date ISO valide (`datetime.date.fromisoformat`).
- **AC3** — Given la suite existante (`tests/test_smoke.py`), When `pytest` tourne, Then elle reste verte et aucun autre fichier du dépôt n'est modifié.

## Définition de « Done » (DoD)
- [ ] AC1..AC3 vérifiés
- [ ] `pytest` vert

## Dépendances
Aucune.

## Notes
Story canari : rejouée chaque jour depuis `main`, sa PR est fermée sans fusion — `main` ne change jamais, la story reste rejouable telle quelle. Deux fichiers au plus : `CANARY.md` et `tests/test_canary.py`.
