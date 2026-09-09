# STORY-006 — Consigner le contrat accents non normalisés dans le README

> status: ready | epic: EPIC-strutils | estimate: S | priority: could | depends_on: 005 | origin: autopilot | updated: 2026-09-02

## Récit

En tant que futur contributeur découvrant le repo,
je veux lire en clair pourquoi `is_palindrome` traite `é` et `e` comme distincts,
afin de ne pas prendre ce comportement pour un bug et de ne pas le « corriger ».

## Critères d'acceptation

- **AC1** — Given `README.md`, When on l'ouvre, Then il contient une section `## Utilitaires` documentant `is_palindrome(s: str) -> bool` en cinq lignes maximum, sans supprimer le contenu existant du fichier.
- **AC2** — Given cette section, When on la lit, Then elle énonce les trois règles — casse ignorée, caractères non alphanumériques ignorés, aucune normalisation Unicode (`é` ≠ `e`) — et mentionne que la chaîne vide vaut `True`.
- **AC3** — Given cette section, When on la lit, Then elle signale l'exemple contre-intuitif `is_palindrome("Élu par cette crapule") is False` avec sa raison en une phrase, et renvoie à la docstring pour le détail plutôt que de le recopier.
- **AC4** — Given le diff de la story, When on exécute `git diff --name-only`, Then seuls `README.md` et le fichier de STORY-003 apparaissent ; aucun fichier de `src/` ni de `tests/` n'est modifié.
- **AC5** — Given la suite de tests, When on exécute `python -m pytest`, Then elle reste verte et la sortie est collée dans le rapport (vérification de forme : cette story ne touche pas au code).

## Définition de « Done » (DoD)

- [ ] La section `## Utilitaires` est ajoutée à `README.md` sans supprimer le contenu existant.
- [ ] Les trois règles et l'exemple contre-intuitif y figurent.
- [ ] La sortie de `git diff --name-only` est collée et se limite aux fichiers autorisés.
- [ ] La sortie de `python -m pytest` est collée et verte.
- [ ] `docs/stories/STORY-003-*.md` est passée en `status: superseded` avec une ligne renvoyant vers cette story.

## Dépendances

- Story #2 : le contrat doit être figé par des tests avant d'être écrit dans le README, sinon la doc précède la vérité.

## Notes / décisions pré-identifiées

- **Priorité `could` assumée** : la docstring est déjà la source de vérité ; le README ne fait que rendre la règle visible sans lecture du code. C'est du confort, pas du besoin — à sacrifier sans regret. Avec le tripwire armé, cette story ne tournera de toute façon pas dans le premier lot.
- **Pas de page `docs/` dédiée** : `docs/` n'accueille ici que les stories ; un seul utilitaire ne justifie pas une arborescence documentaire. Le README est le bon endroit.
- **Aucune duplication du contrat** : le README énonce les règles et renvoie à la docstring pour le détail, afin d'éviter deux textes qui divergeront.

## Surface déclarée

- `README.md`
- `docs/stories/STORY-003-*.md`
