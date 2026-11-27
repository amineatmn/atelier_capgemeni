# Orvanne : des expressions de besoin aux specs Kiro

Solution agentique pour le challenge B. Elle prend les 9 expressions de besoin de `challenge-b/` et produit des specs Kiro (`requirements.md`, `design.md`, `tasks.md`) prêtes pour le développement, avec un registre des conflits et des questions ouvertes.

> Ouvrir **ce dossier** (`atelier_capgmeni/`) comme workspace Kiro : les agents, le steering et les hooks sont dans `.kiro/` à la racine.

## Utilisation

Dans le chat Kiro, choisir l'agent **orchestrateur** puis demander :

- « Génère les specs à partir de challenge-b » : pipeline complet, avec une pause pour valider la carte des projets et les arbitrages ;
- « Analyse seulement » ou « Régénère la spec P02 » : une seule étape.

**Démo :** ouvrir `demo/index.html` dans un navigateur. La page est autonome, sans serveur. Elle montre les documents et leurs demandes, les projets et leurs conflits, les 8 specs et le rapport qualité. Chaque identifiant (`B02-D7`, `C01`, `H03`…) est cliquable et affiche sa preuve : la citation exacte, les positions en conflit, l'hypothèse retenue.

**Démo en direct :** `python3 tools/demo_live.py` (port 8766). On colle une nouvelle expression de besoin, puis les agents Extracteur, Analyste, Rédacteur et Contrôleur en débattent en temps réel (7 tours, environ 1 minute) : objections, corrections, puis verdict et conclusion commune. Chaque message est un vrai appel à un agent Kiro, en lecture seule.

**Sans l'IDE :** `bash tools/pipeline.sh` exécute tout le pipeline avec la CLI Kiro, ou une seule étape : `bash tools/pipeline.sh specs P02`, `… qualite`, `… demo`.

Contrôles manuels :

```bash
python3 tools/valider_contrats.py   # fiches et analyse
python3 tools/valider_specs.py      # specs (structure, EARS, traçabilité, couverture par les tâches)
python3 tools/rapport_qualite.py    # work/rapport-qualite.md
python3 tools/generer_demo.py       # demo/index.html
python3 tools/extracteur.py verifier  # relecture des fiches (passages non cités, chiffres oubliés)
```

## Pipeline

```
challenge-b/*  →  extracteur  →  work/fiches/B0x.json
                  analyste    →  work/analyse.json + work/analyse.md (conflits, hypothèses, questions)
                  redacteur-spec → .kiro/specs/<slug>/
                  controleur  →  work/rapport-qualite.md
```

Les formats échangés entre les étapes sont définis dans [CONTRATS.md](CONTRATS.md).

## Arborescence

| Chemin | Contenu | Responsable |
|---|---|---|
| `CONTRATS.md` | Formats d'interface entre les étapes | toute l'équipe |
| `.kiro/steering/00-pipeline.md` | Règles communes à tous les agents (toujours chargé) | D |
| `.kiro/steering/glossaire-orvanne.md` | Systèmes, organisation, termes métier | A |
| `.kiro/steering/contraintes-transverses.md` | RGPD, gel des mises en production, hébergement… | B |
| `.kiro/steering/format-spec.md` | Règles de rédaction des specs (chargé sur `.kiro/specs/**`) | C |
| `.kiro/agents/extracteur.md` | Agent de l'étape 1 | A |
| `.kiro/agents/analyste.md` | Agent de l'étape 2 | B |
| `.kiro/agents/redacteur-spec.md` | Agent de l'étape 3 | C |
| `.kiro/agents/controleur.md`, `orchestrateur.md` | Étape 4 et pilotage | D |
| `.kiro/hooks/validation-automatique.json` | Lance les validateurs dès qu'un agent écrit une fiche, l'analyse ou une spec | D |
| `templates/` | Modèles des 3 fichiers de spec | C |
| `tools/` | Validateurs Python (sans dépendance) | D |
| `work/exemples/` | Fiche B01 réelle et extrait d'analyse (P01), qui servent de référence | A, B |
| `work/` | Sorties intermédiaires générées | — |
| `.kiro/specs/` | Specs générées (le livrable) | — |

## Répartition du travail

| Qui | Mission | Fini quand |
|---|---|---|
| **A : extraction** | Mettre au point le prompt de l'extracteur sur les 9 formats (CSV, transcription, notes non relues…) ; compléter le glossaire | Les 9 fiches passent `valider_contrats.py` et aucune demande importante ne manque à la relecture |
| **B : analyse** | Mettre au point l'analyste : regroupement en projets, conflits, hypothèses, questions ; compléter les contraintes transverses | `work/analyse.json` est valide, chaque demande est incluse ou exclue, et les conflits connus sont tous détectés |
| **C : rédaction** | Mettre au point les modèles et le rédacteur ; écrire d'abord la spec P01 à la main avec l'exemple d'analyse pour caler le niveau attendu | La spec P01 générée passe `valider_specs.py` et est jugée exploitable par l'équipe |
| **D : qualité et intégration** | Contrôleur, orchestrateur, hooks, validateurs ; exécutions de bout en bout ; démo | Le pipeline complet tourne sur les 9 documents et produit le rapport qualité |

Pour travailler en parallèle, chacun part des exemples de `work/exemples/` sans attendre l'étape précédente. Toute modification de format passe par `CONTRATS.md` et doit être annoncée à l'équipe.

## Résultats

Sorties du pipeline sur les 9 documents de `challenge-b/` :

- `work/fiches/` : 9 fiches, 168 demandes extraites avec leur citation exacte ;
- `work/analyse.json` et `work/analyse.md` : 8 projets, 26 conflits, 31 hypothèses, 39 questions ;
- `.kiro/specs/` : 8 specs Kiro, toutes conformes à `tools/valider_specs.py` ;
- `work/rapport-qualite.md` : toutes les specs au verdict OK ; la référence humaine des conflits (`work/exemples/conflits-attendus.md`, 34 conflits) est couverte à 25, partiellement à 7, et 2 conflits ne sont pas détectés ;
- `demo/index.html` : présentation interactive des résultats.

| Id | Spec | Type | Sources |
|---|---|---|---|
| P01 | [Détection des retards de livraison, suivi colis dans Comptoir et information du client](.kiro/specs/alertes-retards-livraison/) | feature | B01, B02, B05 |
| P02 | [Portail de retours en libre-service, remboursement et visibilité des entrepôts](.kiro/specs/portail-retours/) | feature | B03, B04, B09 |
| P03 | [Déclaration de casse à la douchette, blocage du stock dans Hangar et litiges transporteurs](.kiro/specs/declaration-casse-entrepot/) | feature | B06, B04 |
| P04 | [Relance personnalisée des paniers abandonnés](.kiro/specs/relance-paniers-abandonnes/) | feature | B05 |
| P05 | [Registre et traitement des demandes d'exercice de droits RGPD](.kiro/specs/registre-droits-rgpd/) | feature | B07 |
| P06 | [Prise de rendez-vous de déchargement par les fournisseurs et transporteurs](.kiro/specs/rdv-livraisons-fournisseurs/) | feature | B08 |
| P07 | [Évolutions de l'espace vendeur de la marketplace](.kiro/specs/espace-vendeur-marketplace/) | feature | B09 |
| P08 | [Correctifs de l'espace vendeur : export des ventes et temps de réponse](.kiro/specs/correctifs-espace-vendeur/) | bugfix | B09 |

Les décisions de format sont dans `CONTRATS.md` §6.
