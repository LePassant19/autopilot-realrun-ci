# STORY-010 — La CI teste aussi Python 3.12

> status: ready | epic: EPIC-canary | estimate: S | priority: should | depends_on: — | updated: 2026-09-17

## Récit
**En tant que** mainteneur de ce dépôt de run réel, **je veux** que la CI fasse tourner la suite sur Python 3.11 et 3.12, **afin de** voir une régression de version avant qu'elle n'atteigne `main`.

## Contexte
Story de **run réel** pour harness STORY-069 : son livrable central est un fichier que l'agent n'a pas le droit d'écrire (`.github/workflows/**` est un chemin protégé, STORY-011) et que le runner refuse de commiter. Le livrable attendu pour ce fichier est donc une **proposition** (`harness_proposals[]`), et toute la chaîne — brief, review, juge d'AC — est censée le savoir.

## Critères d'acceptation
- **AC1** — Given la CI actuelle (une seule version de Python), When la story est livrée, Then `.github/workflows/autopilot-ci.yml` est modifié pour que le job `checks` tourne en matrice sur Python `3.11` et `3.12` (`strategy.matrix.python-version`, transmis à `astral-sh/setup-uv`), sans rien retirer de l'existant (`fetch-depth: 0`, `uv sync`, la commande de test).
- **AC2** — Given `README.md`, When la story est livrée, Then une section `## CI` dit que la suite tourne sur Python 3.11 et 3.12, et un test `test_ac2_*` dans `tests/test_readme_ci.py` le vérifie.
- **AC3** — Given la suite existante (`tests/test_smoke.py`), When `pytest` tourne, Then elle reste verte.

## Définition de « Done » (DoD)
- [ ] AC1..AC3 vérifiés
- [ ] `pytest` vert

## Dépendances
Aucune.

## Notes
- `pyproject.toml` et `uv.lock` sont hors périmètre : la commande de test du runner (`uv run --with pytest pytest`) fournit déjà pytest.
- La PR de cette story n'est pas destinée à être fusionnée telle quelle : c'est la proposition sur le workflow qui est l'objet du run.
