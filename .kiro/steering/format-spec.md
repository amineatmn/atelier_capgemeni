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

Pour une spec de type `bugfix` : `templates/bugfix.md` (remplace requirements.md) et `templates/design-bugfix.md`.

## Règles pour requirements.md

- Exigences numérotées `### Exigence 1`, `### Exigence 2`…, chacune avec une user story (« En tant que…, je veux…, afin de… »).
- Critères d'acceptation numérotés `1.1`, `1.2`…, rédigés en EARS français :
  - **Toujours** : `LE SYSTÈME DOIT …`
  - **Événement** : `QUAND <déclencheur>, LE SYSTÈME DOIT …`
  - **État** : `PENDANT QUE <état>, LE SYSTÈME DOIT …`
  - **Option** : `OÙ <fonction présente>, LE SYSTÈME DOIT …`
  - **Indésirable** : `SI <condition anormale>, ALORS LE SYSTÈME DOIT …`
  - Forme négative admise : `LE SYSTÈME NE DOIT PAS …`. Tout critère contient « LE SYSTÈME DOIT » ou « LE SYSTÈME NE DOIT » (contrôlé par `tools/valider_specs.py`), et tout `SI` a son `ALORS`.
- Un critère = un comportement testable. Les seuils sont chiffrés (pas de « rapide » ni de « temps réel » sans valeur).
- Chaque critère se termine par `_Source : …_` (IDs `B0x-Dn`, `CT-nn`, `Hnn` uniquement). Les chiffres (`B0x-Nn`) ne sont pas des sources : on écrit la valeur dans le critère et on cite la demande qui la porte.
- Sections finales obligatoires : `## Hors périmètre`, `## Hypothèses`, `## Questions ouvertes`.

- **Couverture** : chaque demande incluse dans le projet est citée par au moins un critère ou listée dans `Hors périmètre` avec sa raison. Une demande qui n'est pas une exigence du système (ex. « donnez-moi un planning ») va dans `Hors périmètre`.
- **Hypothèses** : le tableau liste toutes les `Hnn` citées, et seulement elles. Une valeur que les sources ne donnent pas (seuil, délai, horaire) est soit une hypothèse, soit un paramètre, jamais une évidence.
- **Conflits non arbitrés** : préférer un comportement paramétrable qui permet les deux positions, avec une valeur par défaut prudente.
- **Questions** : préciser dans la colonne `Bloquante` ce qu'elles bloquent (« oui (exigence 4) »).
- **Échéances** : si une échéance ou un gel impose un découpage, l'annoncer dans l'introduction (lots) et le refléter dans `tasks.md`.

## Règles pour bugfix.md (spec de type bugfix)

- Trois sections obligatoires : `## Comportement actuel`, `## Comportement attendu`, `## Comportement inchangé`. Leurs items numérotés deviennent les critères `1.n`, `2.n` et `3.n`, que `tasks.md` référence.
- **Actuel** : `QUAND <situation>, ALORS LE SYSTÈME <défaut observé>` (pas de « DOIT » : c'est un constat).
- **Attendu** : `QUAND <situation>, LE SYSTÈME DOIT <comportement corrigé, mesurable>`.
- **Inchangé** : `QUAND <situation voisine>, LE SYSTÈME DOIT CONTINUER À <comportement à préserver>`.
- Même traçabilité `_Source : …_` et mêmes sections finales que requirements.md.
- design.md suit `templates/design-bugfix.md` : cause, correctif, tests de reproduction, de correction et de non-régression.

## Règles pour design.md

- Commencer par un tableau des **choix structurants**, avec la raison et l'alternative écartée.
- Les technologies non imposées par les sources sont présentées comme des **propositions**.
- La volumétrie reprend les chiffres sources (`B0x-Nn`) et marque les **estimations** comme telles.
- Chaque composant et chaque cas d'erreur référence ses exigences.
- Le modèle de données indique, pour chaque entité, si elle contient des données personnelles et sa durée de conservation.

## Règles pour tasks.md

- Cases à cocher `- [ ] 1. …`, sous-tâches `- [ ] 1.1 …`.
- Chaque sous-tâche se termine par `_Exigences : 1.1, 2.3_`.
- Le premier groupe de tâches couvre les **prérequis** : avis de la DPO (CT-01), contrats d'interface, jeu de données de test synthétique (CT-04).
- Les dépendances sont écrites sur la tâche parente : `(dépend de 2.1)`. Les tâches indépendantes peuvent s'exécuter en parallèle.
- Les tâches de test et de recette font partie du plan, ce ne sont pas des options.
- Une sous-tâche correspond à un livrable vérifiable, de quelques heures à deux jours de travail.

## Exemple de référence

La spec `templates/exemple-p01/` montre le niveau attendu (détail, traçabilité, traitement des conflits).
