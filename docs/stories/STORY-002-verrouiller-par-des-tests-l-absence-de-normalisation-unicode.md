# STORY-002 — Verrouiller par des tests l'absence de normalisation Unicode

> status: ready | epic: EPIC-strutils | estimate: S | priority: should | depends_on: 001 | origin: autopilot | updated: 2026-09-01

## Récit

En tant que mainteneur de `src/strutils.py`,
je veux des tests de non-régression qui échouent dès qu'on introduit une normalisation Unicode dans `is_palindrome`,
afin qu'un futur contributeur ne « corrige » pas de bonne foi la règle « accents comparés tels quels » qui est le cœur du contrat.

## Critères d'acceptation

- **AC1** — Given la règle `é ≠ e`, When on appelle `is_palindrome("ée")`, Then le résultat est `False`, et When on appelle `is_palindrome("éé")` et `is_palindrome("ressasser")`, Then les résultats sont respectivement `True` et `False` — un test nommé explicitement `test_accents_non_normalises`.
- **AC2** — Given une implémentation qui normaliserait en NFC, When on appelle `is_palindrome("\u00e9" + "e\u0301")` (é précomposé suivi de é décomposé), Then le résultat est `False` ; le test porte un commentaire indiquant qu'une implémentation normalisante renverrait `True`.
- **AC3** — Given que la marque combinante U+0301 n'est pas alphanumérique et est donc retirée par le filtre, When on appelle `is_palindrome("e\u0301" + "e")`, Then le résultat est `True` ; ce comportement est documenté comme conséquence connue et non comme bug.
- **AC4** — Given une implémentation qui utiliserait `casefold()`, When on appelle `is_palindrome("ßss")`, Then le résultat est `False` (avec `casefold()` il vaudrait `True`).
- **AC5** — Given des séparateurs non-ASCII, When on appelle `is_palindrome("ka\u00a0ya\tk\n")` (espace insécable, tabulation, retour ligne), Then le résultat est `True`.
- **AC6** — Given `src/strutils.py`, When on exécute `grep -nE "unicodedata|casefold|normalize" src/strutils.py`, Then aucune ligne ne remonte.

## Définition de « Done » (DoD)

- [ ] Les cinq cas AC1 à AC5 sont des tests distincts et nommés dans `tests/test_strutils.py`.
- [ ] La docstring de `is_palindrome` énonce les quatre règles : `.lower()` (pas `casefold`), filtre `isalnum()`, aucune normalisation NFC/NFD, marques combinantes retirées par le filtre.
- [ ] La commande de l'AC6 est exécutée et sa sortie vide est reportée.
- [ ] `python -m pytest` est vert.
- [ ] Aucune dépendance ajoutée (`hypothesis` explicitement écarté, voir Notes).

## Dépendances

- Story #1 : la fonction et le fichier de tests doivent exister.

## Notes / décisions pré-identifiées

- **Pourquoi cette story existe** : la clause « sans normalisation Unicode » est la seule exigence non standard du besoin, donc la seule que le temps effacera. Sans test la fixant, un refactor bien intentionné (`unicodedata.normalize`) passerait au vert.
- **Asymétrie précomposé / décomposé** : `"é"` en U+00E9 est conservé accent compris, tandis que `"e" + U+0301` perd son accent au filtrage et se comporte comme `"e"`. Deux saisies visuellement identiques, deux résultats. Arbitrage headless : on documente et on teste plutôt que d'ajouter une normalisation contraire au goal. C'est le point à trancher en priorité si l'utilisateur amende sa demande.
- **`hypothesis` écarté** : des tests de propriété (ex. `is_palindrome(s + s[::-1])`) seraient élégants, mais le repo n'a volontairement aucune dépendance de test déclarée ; on ne change pas cette propriété du repo pour cette story.
- Les cas de la story #1 ne sont pas dupliqués ici : cette story n'ajoute que les invariants Unicode.

## Surface déclarée

- `src/strutils.py`
- `tests/test_strutils.py`
