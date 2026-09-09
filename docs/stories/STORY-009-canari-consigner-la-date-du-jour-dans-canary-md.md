# STORY-009 — Canari : consigner la date du jour dans CANARY.md

> status: ready | epic: EPIC-canary | estimate: S | priority: must | depends_on: — | updated: 2026-09-09

## Récit
**En tant que** runner autopilot, **je veux** qu'une story triviale traverse dev → checks → gates → PR → CI, **afin de** prouver chaque matin que le moteur tourne avant de dépenser sur une vraie story (harness STORY-048).

## Critères d'acceptation
- **AC1** — Given le dépôt, When la story est implémentée, Then un fichier `CANARY.md` existe à la racine et contient une ligne `canary YYYY-MM-DD` avec la date du jour (UTC).
- **AC2** — Given `tests/test_canary.py`, When `pytest` tourne, Then un test lit `CANARY.md`, trouve la ligne `canary <date>`, la parse avec `datetime.date.fromisoformat` et vérifie qu'elle vaut **la date UTC du jour** (`datetime.datetime.now(datetime.timezone.utc).date()`) — c'est la preuve exécutable d'AC1. Ce test **s'exécute réellement en CI** : aucun `@pytest.mark.skip`, `skipif` ou `xfail`, même conditionné à l'environnement. Un test qui ne tourne pas ne prouve rien, et la preuve d'AC1 est le seul objet de cette story. *(Canari rouge du 2026-09-09 : un `skipif(BASE_COMMIT is None)` neutralisait AC2 dans CI. La cause n'était pas l'agent — le workflow faisait un clone SUPERFICIEL, donc `git merge-base HEAD main` était vide et l'AC de périmètre inprouvable. Corrigé le même jour par `fetch-depth: 0`, ici et dans le template du harnais : **l'historique complet est désormais disponible en CI**, il n'y a plus aucune raison de sauter un test.)*
- **AC3** — Given la suite existante (`tests/test_smoke.py`), When `pytest` tourne, Then elle reste verte et **aucun autre fichier** que `CANARY.md` et `tests/test_canary.py` n'est modifié — ni `pyproject.toml`, ni `uv.lock` : la commande de test du runner (`uv run --with pytest pytest`) fournit déjà pytest, ne le déclare pas.

## Définition de « Done » (DoD)
- [ ] AC1..AC3 vérifiés
- [ ] `pytest` vert

## Dépendances
Aucune.

## Notes
Story canari : rejouée chaque jour depuis `main`, sa PR est fermée sans fusion — `main` ne change jamais, la story reste rejouable telle quelle. Deux fichiers au plus : `CANARY.md` et `tests/test_canary.py`.
