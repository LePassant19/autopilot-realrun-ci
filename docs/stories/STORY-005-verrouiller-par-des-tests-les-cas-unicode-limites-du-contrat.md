# STORY-005 — Verrouiller par des tests les cas Unicode limites du contrat accents

> status: ready | epic: EPIC-strutils | estimate: S | priority: should | depends_on: 004 | origin: autopilot | updated: 2026-09-02

## Récit

En tant que mainteneur de `src/strutils.py`,
je veux des tests de non-régression sur les cas Unicode limites,
afin qu'un futur contributeur ne « corrige » pas de bonne foi la règle « accents comparés tels quels », et que les comportements surprenants qui en découlent soient documentés comme voulus et non comme bugs.

## Critères d'acceptation

- **AC1** — Given une implémentation qui normaliserait en NFC, When on appelle `is_palindrome("\u00e9" + "e\u0301")` (é précomposé suivi de é décomposé), Then le résultat est `False` ; le test porte un commentaire indiquant qu'une implémentation normalisante renverrait `True`.
- **AC2** — Given que la marque combinante U+0301 n'est pas alphanumérique et est donc retirée par le filtre, When on appelle `is_palindrome("e\u0301" + "e")`, Then le résultat est `True` ; ce comportement est documenté en commentaire comme conséquence connue et assumée, pas comme bug.
- **AC3** — Given une implémentation qui utiliserait `casefold()`, When on appelle `is_palindrome("ßss")`, Then le résultat est `False` (avec `casefold()` il vaudrait `True`).
- **AC4** — Given des séparateurs non-ASCII, When on appelle `is_palindrome("ka\u00a0ya\tk\n")` (espace insécable, tabulation, retour ligne), Then le résultat est `True`.
- **AC5** — Given `tests/test_strutils.py`, When on le lit, Then les quatre cas AC1 à AC4 sont des tests distincts et nommés, et aucun test de la story précédente n'a été supprimé ni renommé.
- **AC6** — Given la suite complète, When on exécute `python -m pytest -v`, Then tous les tests passent et la sortie intégrale est collée dans le rapport de la story.

## Définition de « Done » (DoD)

- [ ] Les quatre cas AC1 à AC4 sont des tests distincts et nommés dans `tests/test_strutils.py`.
- [ ] La docstring de `is_palindrome` mentionne que les marques combinantes sont retirées par le filtre `isalnum()` (asymétrie précomposé / décomposé).
- [ ] La sortie complète de `python -m pytest -v` est collée dans le rapport.
- [ ] Aucune dépendance ajoutée (`hypothesis` explicitement écarté, voir Notes) : `pyproject.toml` est absent de `git diff --stat`.
- [ ] `docs/stories/STORY-002-*.md` est passée en `status: superseded` avec une ligne renvoyant vers cette story.

## Dépendances

- Story #1 : la fonction et le fichier de tests doivent exister.

## Notes / décisions pré-identifiées

- **Périmètre resserré par rapport à STORY-002** : le test principal du contrat (`"ée"` → `False`) a été remonté dans la story #1, parce que le tripwire de cadrage est armé et que seuls les Must sont garantis de tourner. Il ne reste donc ici que les cas limites, qui sont du durcissement réel — pas une duplication.
- **Asymétrie précomposé / décomposé** : `"é"` en U+00E9 conserve son accent, tandis que `"e" + U+0301` le perd au filtrage et se comporte comme `"e"`. Deux saisies visuellement identiques, deux résultats. Arbitrage headless : on documente et on teste, plutôt que d'ajouter une normalisation contraire au goal. C'est le point à trancher en priorité si l'utilisateur amende sa demande au veto.
- **`hypothesis` écarté** : des tests de propriété seraient élégants, mais le repo n'a volontairement aucune dépendance de test déclarée ; on ne change pas cette propriété du repo pour un palindrome.
- Les cas de la story #1 ne sont pas dupliqués ici : cette story n'ajoute que les invariants Unicode limites.

## Surface déclarée

- `src/strutils.py`
- `tests/test_strutils.py`
- `docs/stories/STORY-002-*.md`
