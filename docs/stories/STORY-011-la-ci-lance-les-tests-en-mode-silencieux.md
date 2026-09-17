# STORY-011 — La CI lance les tests en mode silencieux

> status: ready | epic: EPIC-canary | estimate: S | priority: should | depends_on: — | updated: 2026-09-17

## Récit
**En tant que** mainteneur de ce dépôt de run réel, **je veux** que la CI lance pytest en mode silencieux (`-q`), **afin de** lire un journal de CI qui tient sur un écran.

## Contexte
Story de **run réel** pour harness STORY-074. La commande de test de la CI a une source unique, `src/ci_contract.py::TEST_COMMAND`, et un test de couplage PRÉEXISTANT (`tests/test_ci_contract.py`) exige que `.github/workflows/autopilot-ci.yml` lance exactement cette commande. Or ce workflow est un chemin protégé (STORY-011 de harness) : l'agent ne peut pas l'écrire, le runner ne le commite jamais — son changement se livre en **proposition**. Conséquence : dès que `TEST_COMMAND` change, le test de couplage est rouge sur l'arbre commité, et vert une fois la proposition appliquée.

## Critères d'acceptation
- **AC1** — Given `src/ci_contract.py`, When la story est livrée, Then `TEST_COMMAND` vaut `uv run --with pytest pytest -q`, et un test `test_ac1_*` dans `tests/test_ci_contract.py` le vérifie.
- **AC2** — Given le test de couplage existant, When la story est livrée, Then `.github/workflows/autopilot-ci.yml` est modifié pour lancer cette même commande (`- run: uv run --with pytest pytest -q`), sans rien retirer d'autre (`fetch-depth: 0`, `uv sync`).
- **AC3** — Given la suite, When `pytest` tourne AVEC le workflow à jour, Then elle est verte — le test de couplage n'est ni supprimé, ni affaibli, ni sauté.

## Définition de « Done » (DoD)
- [ ] AC1..AC3 vérifiés
- [ ] `pytest` vert une fois la proposition appliquée

## Dépendances
Aucune.

## Notes
- `pyproject.toml` et `uv.lock` sont hors périmètre.
- Ne touche pas au test de couplage pour le faire passer : c'est lui, l'objet du run.
