# Prioriser la tentative la plus récente dans le brief condensé

> status: draft | epic: EPIC-proposals | estimate: — | depends_on: — | updated: 2026-09-06

## Récit
**En tant que** Guillaume,
**je veux** Dans la génération du brief : itérer sur les tentatives en ordre décroissant, accumuler jusqu'au budget, puis ré-ordonner pour l'affichage. Ajouter un test qui, avec 3 tentatives et un budget ne tenant que pour une, vérifie que les findings conservés sont ceux de la tentative 3.,
**afin de** Le brief condensé de reprise a tronqué les findings de la tentative 2 (« [...tronqué pour tenir dans le budget du brief condensé...] »), ne laissant visibles que ceux de la tentative 1 — déjà corrigés. J'ai dû ré-inférer le motif de rejet réel (absence de fonction test_ac3_*) depuis le rappel générique sur l'extracteur de preuves. Tronquer par la fin fait perdre en priorité les findings les plus récents, c'est-à-dire les seuls encore actionnables.

## Critères d'acceptation
- **AC1** — Given le besoin harness identifié pendant l'exécution de STORY-009, When il est instruit, Then Dans la génération du brief : itérer sur les tentatives en ordre décroissant, accumuler jusqu'au budget, puis ré-ordonner pour l'affichage. Ajouter un test qui, avec 3 tentatives et un budget ne tenant que pour une, vérifie que les findings conservés sont ceux de la tentative 3..

## Définition de « Done » (DoD)
- [ ] AC1 vérifié

## Notes / décisions pré-identifiées
Proposition générée automatiquement par le runner autopilot pendant STORY-009 — brute, non affinée (pas de challenge/clarification, cf. `/cadrer`). À trier par Guillaume : garder (cadrer normalement), fusionner dans une story existante, ou passer en `icebox`. Jamais promue en l'état (`bin/autopilot promote`) : elle doit repasser par le flux spec-first habituel avant tout `ready`.
