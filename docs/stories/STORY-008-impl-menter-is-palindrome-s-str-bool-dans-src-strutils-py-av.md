# STORY-008 — Implémenter is_palindrome(s: str) -> bool dans src/strutils.py avec tests

> status: draft | epic: EPIC-strutils | estimate: S | priority: could | depends_on: — | origin: autopilot | updated: 2026-09-02

## Récit
En tant qu'utilisateur de la librairie strutils, je veux une fonction is_palindrome(s: str) -> bool insensible à la casse, aux espaces et à la ponctuation (accents comparés tels quels, sans normalisation Unicode), afin de détecter des palindromes de façon fiable et prévisible.

## Critères d'acceptation
- Given une chaîne vide "", When is_palindrome est appelée, Then elle retourne True.
- Given une chaîne avec casse mixte, espaces et ponctuation (ex: "Ésope reste ici et se repose"), When is_palindrome est appelée, Then la casse, les espaces et la ponctuation sont ignorés mais les accents sont comparés tels quels (pas de normalisation Unicode, donc é ≠ e).
- Given tests/test_strutils.py, When la suite pytest est lancée, Then elle couvre au minimum : chaîne vide, palindrome simple, palindrome avec ponctuation/espaces/casse, non-palindrome, cas où un accent casse la symétrie (é vs e).

## Définition de « Done » (DoD)
- src/strutils.py contient is_palindrome implémentée selon le contrat ci-dessus.
- tests/test_strutils.py existe et passe intégralement via `pytest`.
- Aucun fichier hors src/strutils.py et tests/test_strutils.py n'est modifié.

## Dépendances
Dépend de la story déclarant pytest comme dépendance de test (sinon reproduit le blocage STORY-004).

## Notes
Remplace/relance STORY-001 et STORY-004, toutes deux non abouties.
