# STORY-001 — Détecter les palindromes en ignorant casse, espaces et ponctuation

> status: blocked | epic: EPIC-strutils | estimate: S | priority: must | depends_on: — | origin: autopilot | updated: 2026-09-01

## Récit

En tant que développeur du projet `realrun-ci`,
je veux une fonction `is_palindrome(s: str) -> bool` dans `src/strutils.py`,
afin de tester si une chaîne se lit identiquement dans les deux sens en faisant abstraction de la casse, des espaces et de la ponctuation.

## Critères d'acceptation

- **AC1** — Given le repo à sa racine, When on exécute `from src.strutils import is_palindrome`, Then l'import réussit et la fonction est annotée `(s: str) -> bool` (le `pythonpath = ["."]` de `pyproject.toml` rend `src` importable ; ajouter `src/__init__.py` vide uniquement si l'import par package implicite échoue).
- **AC2** — Given une chaîne palindrome à la casse variable, When on appelle `is_palindrome("Kayak")` et `is_palindrome("RaceCar")`, Then les deux renvoient `True`.
- **AC3** — Given une chaîne contenant espaces et ponctuation, When on appelle `is_palindrome("A man, a plan, a canal: Panama")` et `is_palindrome("elu par cette crapule")`, Then les deux renvoient `True`.
- **AC4** — Given une chaîne non palindrome, When on appelle `is_palindrome("hello")` et `is_palindrome("abca")`, Then les deux renvoient `False`.
- **AC5** — Given une chaîne vide, When on appelle `is_palindrome("")`, Then le résultat est `True` ; et Given une chaîne composée uniquement d'espaces et de ponctuation, When on appelle `is_palindrome("!!! ... ???")`, Then le résultat est `True` (elle se réduit à la chaîne vide).
- **AC6** — Given la suite de tests, When on exécute `python -m pytest`, Then tous les tests passent, `tests/test_smoke.py` inclus, et `pyproject.toml` n'a acquis aucune dépendance.

## Définition de « Done » (DoD)

- [ ] `is_palindrome` est implémentée dans `src/strutils.py` en stdlib pure (aucun import tiers).
- [ ] Une docstring décrit le contrat : casse ignorée, caractères non alphanumériques ignorés, chaîne vide → `True`.
- [ ] `tests/test_strutils.py` existe et couvre AC2 à AC5, un cas par assertion nommée.
- [ ] `python -m pytest` est vert en local (sortie collée dans le rapport de la story).
- [ ] `pyproject.toml` est inchangé (`git diff --stat` ne le mentionne pas).

## Dépendances

Aucune.

## Notes / décisions pré-identifiées

- **Filtre retenu** : `"".join(c for c in s if c.isalnum()).lower()` puis comparaison avec son inverse. `isalnum()` est Unicode-aware : il conserve les lettres accentuées précomposées et les chiffres, et retire espaces, tabulations, retours ligne, NBSP et ponctuation — ce qui couvre AC3 et AC5 sans liste de caractères en dur.
- **`.lower()` et non `.casefold()`** : `casefold()` déplie `ß` en `ss`, ce qui est une forme de normalisation explicitement exclue par le goal. Verrouillé par un test dans la story suivante.
- **Aucune validation de type** : la signature annonce `str` ; conformément au principe « trust internal invariants », on n'ajoute pas de garde runtime pour `None` ou un non-str.
- **Les chiffres sont significatifs** : `"12321"` → `True`, `"12345"` → `False`. C'est la conséquence directe de `isalnum()` ; aucun cas du goal ne s'y oppose.
- **Conséquence assumée, à relire au veto** : `is_palindrome("Élu par cette crapule")` renvoie `False` (É → é, distinct du e final), alors que la variante sans accent renvoie `True`. C'est voulu par la règle « accents tels quels » ; AC3 utilise donc délibérément la variante sans accent.

## Surface déclarée

- `src/strutils.py`
- `src/__init__.py`
- `tests/test_strutils.py`
