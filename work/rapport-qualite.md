# Rapport qualité

Généré par `tools/rapport_qualite.py`. Contrôles automatiques : `tools/valider_specs.py` (structure, EARS, sources existantes, couverture des critères par les tâches) et couverture de l'analyse (demandes, conflits, contraintes, questions bloquantes).

## Synthèse par spec

| Projet | Spec | Type | Validateur | Critères | Sous-tâches | Demandes citées | Conflits avec hypothèse citée | Verdict |
|---|---|---|---|---|---|---|---|---|
| P01 | `alertes-retards-livraison` | feature | OK | 68 | 60 | 27/27 | 7/7 | OK (question bloquante ouverte) |
| P02 | `portail-retours` | feature | OK | 84 | 74 | 49/49 | 8/8 | OK |
| P03 | `declaration-casse-entrepot` | feature | OK | 69 | 51 | 14/14 | 3/3 | OK |
| P04 | `relance-paniers-abandonnes` | feature | OK | 54 | 46 | 12/12 | 4/4 | OK |
| P05 | `registre-droits-rgpd` | feature | OK | 69 | 52 | 20/20 | 0/0 | OK |
| P06 | `rdv-livraisons-fournisseurs` | feature | OK | 63 | 59 | 30/30 | 4/4 | OK |
| P07 | `espace-vendeur-marketplace` | feature | OK | 59 | 57 | 19/19 | 3/3 | OK |
| P08 | `correctifs-espace-vendeur` | bugfix | OK | 17 | 25 | 4/4 | 0/0 | OK |

## Détail par spec

### P01 Détection des retards de livraison, suivi colis dans Comptoir et information du client

- Aucun constat.
- Question bloquante `Q03` (DSI (Bertrand Lacassagne)) : Le pic tombe pendant le gel du 16/11 au 11/01. Une dérogation est-elle envisageable pour un tableau de bord interne, sans envoi aux clients, avant le 16/11 ? Sinon, confirmez-vous une mise en service au T1 2027 ?

### P02 Portail de retours en libre-service, remboursement et visibilité des entrepôts

- Aucun constat.

### P03 Déclaration de casse à la douchette, blocage du stock dans Hangar et litiges transporteurs

- Aucun constat.

### P04 Relance personnalisée des paniers abandonnés

- Aucun constat.

### P05 Registre et traitement des demandes d'exercice de droits RGPD

- Aucun constat.

### P06 Prise de rendez-vous de déchargement par les fournisseurs et transporteurs

- Aucun constat.

### P07 Évolutions de l'espace vendeur de la marketplace

- Aucun constat.

### P08 Correctifs de l'espace vendeur : export des ventes et temps de réponse

- Aucun constat.

## Couverture de la référence humaine des conflits

Référence : `work/exemples/conflits-attendus.md` (34 conflits attendus). Couverts : 25, partiellement : 7, non couverts : 2.

| Réf. | Traité par | Couverture | Commentaire |
|---|---|---|---|
| R01 | C01 | oui |  |
| R02 | C02 | oui |  |
| R03 | C04 | oui |  |
| R04 | C04 | partiel | La propriété des messages (logistique ou service client) n'est traitée que sous l'angle du contrôle des envois. |
| R05 | C03 | oui |  |
| R06 | C07 | oui |  |
| R07 | C09 | oui |  |
| R08 | C10 | oui |  |
| R09 | C08 | oui |  |
| R10 | C11 | oui |  |
| R11 | C13 | oui |  |
| R12 | C12 | oui |  |
| R13 | CT-06 | partiel | Traité comme contrainte transverse, sans conflit explicite entre EF-09 et la DPO. |
| R14 | C15 | oui |  |
| R15 | C14 | oui |  |
| R16 | — | non | Le bon d'achat majoré de 5 % (B04) n'apparaît ni en conflit ni en hypothèse. |
| R17 | C16 | oui |  |
| R18 | H11, Q37 | partiel | La note A / B / C est traitée, pas le choix du périmètre « casse seule ou casse et retours ». |
| R19 | C17 | oui |  |
| R20 | C20 | oui |  |
| R21 | C19 | oui |  |
| R22 | C18 | oui |  |
| R23 | Q33 | partiel | Les plafonds de remise sont une question, pas un conflit. |
| R24 | C21 | oui |  |
| R25 | C22 | oui |  |
| R26 | C23 | oui |  |
| R27 | C24 | oui |  |
| R28 | C26 | oui |  |
| R29 | C25 | oui |  |
| R30 | — | non | L'hétérogénéité des priorités de B09 n'est relevée que dans la fiche (point flou). |
| R31 | C11 | partiel | Le suivi des retours par les vendeurs (MKP-06) est lié au conflit sur les retours marketplace. |
| R32 | C02, C26 | partiel | Les sens du mot « retard » sont traités projet par projet, pas comme une définition commune. |
| R33 | CT-01 | oui | Traité comme contrainte transverse sur tous les projets. |
| R34 | H08, Q04, Q09 | partiel | La relation entre Premium et Orvanne+ est posée en question. |

## Limites

- Les contrôles vérifient la présence et la cohérence des références, pas la justesse métier de chaque critère : une relecture humaine des specs reste nécessaire avant développement.
- La correspondance avec la référence humaine a été établie à la lecture ; elle est à revoir si l'analyse est régénérée.
