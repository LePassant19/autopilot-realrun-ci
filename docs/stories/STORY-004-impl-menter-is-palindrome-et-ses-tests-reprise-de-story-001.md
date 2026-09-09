# STORY-004 — Implémenter is_palindrome et ses tests (reprise de STORY-001)

> status: blocked | epic: EPIC-strutils | estimate: S | priority: must | depends_on: — | origin: autopilot | updated: 2026-09-02

## Récit

En tant que développeur du projet `realrun-ci`,
je veux une fonction `is_palindrome(s: str) -> bool` dans `src/strutils.py`, couverte par `tests/test_strutils.py`,
afin de tester si une chaîne se lit identiquement dans les deux sens en ignorant casse, espaces et ponctuation, sans jamais normaliser les accents.

Cette story reprend STORY-001, restée `blocked` après trois tentatives dont les sessions dev n'ont produit aucune action. Le besoin est inchangé ; ce qui change, c'est l'exigence de preuve d'exécution (AC7) et l'intégration du contrat accents ici plutôt qu'en Should.

## Critères d'acceptation

- **AC1** — Given le repo à sa racine, When on exécute `python -c "from src.strutils import is_palindrome"`, Then l'import réussit et la fonction est annotée `(s: str) -> bool` (le `pythonpath = ["."]` de `pyproject.toml` rend `src` importable ; n'ajouter un `src/__init__.py` vide que si l'import échoue sans lui).
- **AC2** — Given une chaîne palindrome à la casse variable, When on appelle `is_palindrome("Kayak")` et `is_palindrome("RaceCar")`, Then les deux renvoient `True`.
- **AC3** — Given une chaîne contenant espaces et ponctuation, When on appelle `is_palindrome("A man, a plan, a canal: Panama")` et `is_palindrome("elu par cette crapule")`, Then les deux renvoient `True`.
- **AC4** — Given une chaîne non palindrome, When on appelle `is_palindrome("hello")` et `is_palindrome("abca")`, Then les deux renvoient `False`.
- **AC5** — Given une chaîne vide, When on appelle `is_palindrome("")`, Then le résultat est `True` ; et Given une chaîne uniquement faite d'espaces et de ponctuation, When on appelle `is_palindrome("!!! ... ???")`, Then le résultat est `True` (elle se réduit à la chaîne vide).
- **AC6** — Given la règle « accents comparés tels quels », When on appelle `is_palindrome("ée")`, `is_palindrome("éé")` et `is_palindrome("Élu par cette crapule")`, Then les résultats sont respectivement `False`, `True` et `False`, dans un test nommé `test_accents_non_normalises` ; et When on exécute `grep -nE "unicodedata|casefold|normalize" src/strutils.py`, Then aucune ligne ne remonte.
- **AC7** — Given la suite complète, When on exécute `python -m pytest -v`, Then tous les tests passent (`tests/test_smoke.py` inclus) et la sortie intégrale de la commande est collée dans le rapport de la story. Un rapport sans sortie `pytest` réelle vaut échec de la story : les trois tentatives précédentes ont échoué sans qu'aucun fichier n'ait jamais été écrit, cet AC est le garde-fou contre une story déclarée faite à vide.
- **AC8** — Given la branche de la story, When on exécute `git diff --stat`, Then n'apparaissent que `src/strutils.py`, `tests/test_strutils.py`, et éventuellement `src/__init__.py` et le fichier de STORY-001 ; `pyproject.toml` est absent de la liste (aucune dépendance ajoutée).

## Définition de « Done » (DoD)

- [ ] `is_palindrome` est implémentée dans `src/strutils.py` en stdlib pure (aucun import tiers).
- [ ] Sa docstring énonce les quatre règles du contrat : casse ignorée via `.lower()` (jamais `casefold()`), caractères non alphanumériques ignorés via `isalnum()`, aucune normalisation Unicode (`é` ≠ `e`), chaîne vide → `True`.
- [ ] `tests/test_strutils.py` existe et couvre AC2 à AC6, un test nommé par cas.
- [ ] La sortie complète de `python -m pytest -v` est collée dans le rapport de la story.
- [ ] La sortie de `git diff --stat` est collée dans le rapport.
- [ ] `docs/stories/STORY-001-*.md` est passée en `status: superseded` dans sa ligne meta, avec une ligne renvoyant vers cette story — le repo ne doit pas conserver deux backlogs concurrents pour le même besoin.

## Dépendances

Aucune. Cette story remplace STORY-001 (`blocked`), qu'elle passe en `superseded`.

## Notes / décisions pré-identifiées

- **Implémentation retenue** : `"".join(c for c in s if c.isalnum()).lower()` puis comparaison avec son inverse. `isalnum()` est Unicode-aware : il conserve lettres accentuées précomposées et chiffres, et retire espaces, tabulations, retours ligne, NBSP et ponctuation — AC3 et AC5 sont couverts sans liste de caractères en dur.
- **`.lower()` et non `.casefold()`** : `casefold()` déplie `ß` en `ss`, une normalisation que le goal exclut explicitement.
- **Pourquoi le contrat accents est ici et non dans la story suivante** : le cadrage répond `false` à « alternative plus simple clairement inférieure », donc le runner n'exécutera que les Must. Laisser le seul test de la clause `é ≠ e` dans une Should reviendrait à ne jamais vérifier la seule exigence non standard du besoin. Les cas Unicode plus fins (formes décomposées, `ß`, séparateurs exotiques) restent, eux, dans la story suivante.
- **Conséquence assumée, à relire au veto** : `is_palindrome("Élu par cette crapule")` renvoie `False` (É → é, distinct du e final) alors que la variante sans accent renvoie `True`. C'est la règle demandée ; AC3 utilise donc délibérément la variante sans accent et AC6 verrouille la variante accentuée.
- **Aucune validation de type** : la signature annonce `str` ; conformément à « trust internal invariants », pas de garde runtime pour `None` ou un non-`str`.
- **Les chiffres sont significatifs** : `"12321"` → `True`, `"12345"` → `False`, conséquence directe de `isalnum()` ; aucun cas du goal ne s'y oppose.
- **Si la session dev se termine à nouveau sans rien écrire**, ce n'est pas un problème de story : le diagnostic appartient au repo autopilot (transcripts dev vides), pas à `realrun-ci`.

## Surface déclarée

- `src/strutils.py`
- `src/__init__.py`
- `tests/test_strutils.py`
- `docs/stories/STORY-001-*.md`
