# Orvanne : des expressions de besoin aux specs Kiro

Solution agentique pour le challenge B. Elle prend les 9 expressions de besoin de `challenge-b/` et produit des specs Kiro (`requirements.md`, `design.md`, `tasks.md`) prêtes pour le développement, avec un registre des conflits et des questions ouvertes.

> Ouvrir **ce dossier** (`atelier_capgmeni/`) comme workspace Kiro : les agents, le steering et les hooks sont dans `.kiro/` à la racine.

## Utilisation

Dans le chat Kiro, choisir l'agent **orchestrateur** puis demander :

- « Génère les specs à partir de challenge-b » : pipeline complet, avec une pause pour valider la carte des projets et les arbitrages ;
- « Analyse seulement » ou « Régénère la spec P02 » : une seule étape.

Contrôles manuels :

```bash
python3 tools/valider_contrats.py   # fiches et analyse
python3 tools/valider_specs.py      # specs (structure, EARS, traçabilité, couverture par les tâches)
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

## Décisions à prendre au lancement

Voir `CONTRATS.md` §6 : la langue des mots-clés EARS et la liste provisoire des projets.
