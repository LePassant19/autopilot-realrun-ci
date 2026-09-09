# STORY-007 — Déclarer pytest comme dépendance de test dans pyproject.toml

> status: draft | epic: EPIC-strutils | estimate: S | priority: could | depends_on: — | origin: autopilot | updated: 2026-09-02

## Récit
En tant que mainteneur du projet, je veux que pytest soit déclaré explicitement comme dépendance de développement/test dans pyproject.toml, afin que les agents (et humains) puissent exécuter la suite de tests sans devoir contourner ou modifier le harnais de vérification.

## Critères d'acceptation
- Given pyproject.toml sans pytest déclaré, When on ajoute pytest en dépendance de test (groupe dev/test), Then `uv sync` (ou équivalent) installe pytest sans action manuelle supplémentaire.
- Given uv.lock à jour après ajout, When on lance `pytest`, Then la commande s'exécute sans erreur "module not found".
- Given le harnais de vérification (verify/ac8.sh ou équivalent), When il est invoqué, Then il n'a pas besoin d'être modifié ou supprimé pour fonctionner.

## Définition de « Done » (DoD)
- pyproject.toml et uv.lock committés avec pytest en dépendance de test.
- `pytest` s'exécute localement avec succès (même sur une suite vide ou minimale).
- Aucun fichier du harnais (verify/*, uv.lock) n'a été supprimé ou altéré hors de cet ajout.

## Dépendances
Aucune — bloquant pour toute story impliquant des tests (is_palindrome et suivantes).

## Notes
Révélé par STORY-004 : l'agent a supprimé uv.lock et verify/ac8.sh en réaction probable à l'absence de pytest, au lieu de déclarer la dépendance manquante.
