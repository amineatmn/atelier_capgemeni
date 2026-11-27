---
inclusion: fileMatch
fileMatchPattern: [".kiro/specs/**/*.md", "templates/**/*.md"]
---
# Format des specs Orvanne

<!-- Responsable : C. Ce fichier est chargé automatiquement dès qu'on travaille sur une spec. -->

Les modèles sont dans `templates/` :
#[[file:templates/requirements.md]]
#[[file:templates/design.md]]
#[[file:templates/tasks.md]]

## Règles pour requirements.md

- Exigences numérotées `### Exigence 1`, `### Exigence 2`…, chacune avec une user story (« En tant que…, je veux…, afin de… »).
- Critères d'acceptation numérotés `1.1`, `1.2`…, rédigés en EARS français :
  - **Toujours** : `LE SYSTÈME DOIT …`
  - **Événement** : `QUAND <déclencheur>, LE SYSTÈME DOIT …`
  - **État** : `PENDANT QUE <état>, LE SYSTÈME DOIT …`
  - **Option** : `OÙ <fonction présente>, LE SYSTÈME DOIT …`
  - **Indésirable** : `SI <condition anormale>, ALORS LE SYSTÈME DOIT …`
- Un critère = un comportement testable. Les seuils sont chiffrés (pas de « rapide » ni de « temps réel » sans valeur).
- Chaque critère se termine par `_Source : …_` (IDs `B0x-Dn`, `CT-nn`, `Hnn`).
- Sections finales obligatoires : `## Hors périmètre`, `## Hypothèses`, `## Questions ouvertes`.

## Règles pour tasks.md

- Cases à cocher `- [ ] 1. …`, sous-tâches `- [ ] 1.1 …`.
- Chaque sous-tâche se termine par `_Exigences : 1.1, 2.3_`.
- Ordonner les tâches pour que les dépendances soient explicites : les tâches indépendantes peuvent s'exécuter en parallèle.
- Les tâches de test font partie du plan, ce ne sont pas des options.
