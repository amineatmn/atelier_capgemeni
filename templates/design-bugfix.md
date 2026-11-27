# Conception du correctif : <Titre du défaut>

## Analyse de la cause

<Cause racine établie ou supposée (alors marquée Hnn), et comment elle a été ou sera confirmée.>

## Architecture

<Zone du système concernée : composants, tables, traitements. Diagramme Mermaid si utile.>

## Correctif proposé

| Changement | Raison | Critères |
|---|---|---|
| <modification> | <pourquoi> | 2.1 |

## Gestion des erreurs

| Situation | Comportement | Critère |
|---|---|---|
| <cas> | <réaction> | 2.1 |

## Stratégie de test

- **Reproduction** : test qui échoue avant le correctif (critères 1.n).
- **Correction** : test qui passe après le correctif (critères 2.n).
- **Non-régression** : tests des comportements inchangés (critères 3.n).
