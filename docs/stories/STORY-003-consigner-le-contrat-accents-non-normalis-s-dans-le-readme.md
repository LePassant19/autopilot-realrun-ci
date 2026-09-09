# STORY-003 — Consigner le contrat « accents non normalisés » dans le README

> status: ready | epic: EPIC-strutils | estimate: S | priority: could | depends_on: 002 | origin: autopilot | updated: 2026-09-01

## Récit

En tant que futur contributeur découvrant le repo,
je veux lire en clair pourquoi `is_palindrome` traite `é` et `e` comme distincts,
afin de ne pas prendre ce comportement pour un bug et de ne pas le « corriger ».

## Critères d'acceptation

- **AC1** — Given `README.md`, When on l'ouvre, Then il contient une section `## Utilitaires` documentant `is_palindrome(s: str) -> bool` en cinq lignes maximum.
- **AC2** — Given cette section, When on la lit, Then elle énonce les trois règles : casse ignorée, caractères non alphanumériques ignorés, aucune normalisation Unicode (`é` ≠ `e`), et mentionne que la chaîne vide vaut `True`.
- **AC3** — Given cette section, When on la lit, Then elle signale l'exemple contre-intuitif `is_palindrome("Élu par cette crapule") is False` avec sa raison en une phrase.
- **AC4** — Given le diff de la story, When on exécute `git diff --name-only`, Then seul `README.md` apparaît ; aucun fichier de `src/` ni de `tests/` n'est modifié.

## Définition de « Done » (DoD)

- [ ] La section `## Utilitaires` est ajoutée à `README.md` sans supprimer le contenu existant.
- [ ] Les trois règles et l'exemple contre-intuitif y figurent.
- [ ] Le diff est limité à `README.md` (sortie de `git diff --name-only` reportée).
- [ ] `python -m pytest` reste vert (aucune raison de casser, vérification de forme).

## Dépendances

- Story #2 : le contrat doit être figé par des tests avant d'être écrit dans le README, sinon la doc précède la vérité.

## Notes / décisions pré-identifiées

- **Priorité `could` assumée** : la docstring de la story #2 est déjà la source de vérité ; le README ne fait que rendre la règle visible sans lecture du code. C'est du confort, pas du besoin — à sacrifier sans regret si l'utilisateur veut s'arrêter plus tôt.
- **Pas de `docs/`** : le repo n'a pas d'arborescence documentaire et n'en justifie pas une pour un seul utilitaire ; le README est le bon endroit.
- **Aucune duplication du contrat** : le README énonce les règles et renvoie à la docstring pour le détail, afin d'éviter deux textes qui divergeront.

## Surface déclarée

- `README.md`
