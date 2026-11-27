# Analyse transverse des expressions de besoin d'Orvanne

Rendu lisible de `work/analyse.json`, qui fait foi. Entrée : les 9 fiches `work/fiches/B01.json` à `B09.json` (168 demandes). Sortie : 8 projets, 11 contraintes transverses, 26 conflits, 31 hypothèses, 39 questions.

## 1. Carte des projets

| Id | Slug | Type | Commanditaire | Documents | Demandes incluses | Conflits |
|---|---|---|---|---|---|---|
| P01 | `alertes-retards-livraison` | feature | Direction des opérations logistiques | B01, B02, B05 | 26 | C01 à C07 |
| P02 | `portail-retours` | feature | Direction de l'expérience client | B03, B04, B09 | 47 | C08 à C15 |
| P03 | `declaration-casse-entrepot` | feature | Exploitation entrepôt E2 | B06, B04 | 14 | C12, C16, C17 |
| P04 | `relance-paniers-abandonnes` | feature | Marketing (CRM et fidélité) | B05 | 11 | C07, C18 à C20 |
| P05 | `registre-droits-rgpd` | feature | Direction juridique et conformité (DPO) | B07 | 13 | aucun |
| P06 | `rdv-livraisons-fournisseurs` | feature | Approvisionnement et transport amont | B08 | 30 | C21 à C24 |
| P07 | `espace-vendeur-marketplace` | feature | Direction marketplace | B09 | 14 | C11, C25, C26 |
| P08 | `correctifs-espace-vendeur` | bugfix | Direction marketplace | B09 | 4 | aucun |

Total : 159 demandes incluses et 9 exclues sans renvoi vers un autre projet. Chaque demande est incluse dans un seul projet.

### Écarts par rapport à la liste provisoire (CONTRATS.md §6)

- **P08 créé (bugfix), séparé de P07.** MKP-07 (`B09-D9`, avec les pistes DSI `B09-D10` et `B09-D11`) et MKP-11 « trop lent » (`B09-D17`) décrivent des défauts de l'espace vendeur existant, pas de nouvelles capacités. Le format bugfix (comportement actuel, attendu, inchangé) leur convient, alors qu'il ne convient pas aux 12 autres lignes. Les deux défauts peuvent être livrés indépendamment des évolutions de P07, et ils doivent l'être avant MKP-01 et MKP-12, qui s'appuient sur les mêmes données de ventes. Limite : MKP-11 n'est ni chiffré ni localisé. La spec commence donc par une mesure, et le comportement attendu sera fixé ensuite (H27, Q28). Les « reversements incompréhensibles » (`B09-D18`), qui figurent sur la même ligne MKP-11, restent dans P07 : il s'agit d'un besoin d'explication, pas d'un défaut.
- **MKP-06 (`B09-D8`) est placé dans P02**, conformément à la liste provisoire, en V2 avec les retours marketplace (H10).
- **La saisie de la note A / B / C à la douchette (`B04-D13`) est placée dans P03.** Elle utilise le même écran que la déclaration de casse (`B06-D10`) et est prévue en V2.
- **Règles de B07 sorties de P05.** Les demandes `B07-D10` à `B07-D16` sont des règles applicables à tous les projets : elles sont exclues de P05 et portées par les CT. `B07-D14` (purge des historiques de prospection) est exclue sans renvoi, faute de porteur (Q31).
- **Autres exclusions** : `B05-D7` (code promo dans les messages de retard, interdit par CT-03) et `B04-D16` (taux de retour par produit, idée sans porteur, Q32).

### Découpage V1 / V2

| Projet | V2 | Motif |
|---|---|---|
| P01 | Canal SMS (`B01-D5`), validation Premium (`B02-D8`) | Avis DPO, budget, catégorie Premium non définie (H01, H03) |
| P02 | Photos (`B03-D17`, `B04-D1`), marketplace (`B04-D9`, `B04-D10`, `B09-D8`), bon d'achat (`B04-D14`) | « Souhaitable », CT-06, circuit distinct, simple idée (H10) |
| P03 | Téléphones des chefs d'équipe (`B06-D7`), retours abîmés A / B / C (`B06-D10`, `B04-D13`) | Piste « à voir », dépend de la grille de P02 (H15) |
| P04 | Modèle d'IA (`B05-D2`) | Règles d'abord (H30) |
| P05 | Orchestration automatisée (`B07-D5`) | Échéance du contrôle interne (H31) |
| P06 | Notation, pénalités, lien Hangar, application chauffeurs (`B08-D18`, `D19`, `D23`, `D24`) | Classés V2 en atelier (B08) |
| P07 | MKP-09, MKP-10, MKP-11 reversements, MKP-12 | Échéances S1, T2 et 2027 |

### Dépendances

- **P02 et P03** partagent la grille A / B / C (`B04-D11`). L'écran douchette de P03 saisit la note des retours abîmés, et le remboursement après contrôle (H07) dépend de cette saisie.
- **P02 et P07** : le suivi des retours par le vendeur (MKP-06) attend les retours marketplace (V2 de P02).
- **P01 et P02** lisent tous deux les statuts transporteurs dans Passerelle.
- **P07 et P08** : les correctifs précèdent les nouvelles vues de ventes.
- **P05 dépend de tous les projets** : chaque nouveau stockage de données clients (alertes, retours, photos, contacts fournisseurs, échanges vendeur-client) entre dans l'orchestration des droits (`B07-D5`). P04 doit appliquer les oppositions à la prospection.

## 2. Contraintes transverses

| Id | Contrainte | Sources | Projets |
|---|---|---|---|
| CT-01 | Tout nouveau traitement de données personnelles est soumis à la DPO avant développement | B07-D10 | P01 à P07 |
| CT-02 | Le mobile est collecté pour la livraison ; tout autre usage suppose une analyse préalable | B07-D11 | P01, P04 |
| CT-03 | Un message de service ne contient pas d'offre commerciale | B07-D12, B02-D10 | P01, P02, P06 |
| CT-04 | Aucune donnée de production pour des démos ou des tests sans anonymisation | B07-D16 | tous |
| CT-05 | Données de prospection conservées au plus 3 ans après le dernier contact | B07-D13 | P04 |
| CT-06 | Photos et pièces jointes = données personnelles si une étiquette ou une personne est visible | B07-D15 | P02, P03 |
| CT-07 | Gel des mises en production du 16/11 au 11/01 | B02-D12 | tous |
| CT-08 | Hébergement dans l'UE ; cloud d'Orvanne pour P01, généralisation à confirmer (Q34) | B01-D9, B03-D21 | tous |
| CT-09 | **Nouvelle.** Interfaces destinées à des personnes externes conformes au RGAA et utilisables sur mobile ; extension à P06 et P07 à confirmer (Q35) | B03-D22 | P02, P06, P07 |
| CT-10 | **Nouvelle.** Les actions faites pour le compte d'un client ou d'un tiers sont journalisées, avec une preuve d'exécution | B03-D23, B07-D1 | P01, P02, P05, P07 |
| CT-11 | **Nouvelle.** Utilisateurs externes non francophones : écrans et messages traduisibles | B08-D21, B09-D15 | P06, P07 |

`contraintes-transverses.md` (steering, responsable B) doit être complété avec CT-09 à CT-11 et les sources réelles.

## 3. Registre des conflits

### Bloquant

| Id | Sujet | Positions | Arbitre | Question |
|---|---|---|---|---|
| C03 | Échéance « pour le pic » contre gel | B01-D1 et B01-D5 : opérationnel pour le pic ; B02-D12 : gel du 16/11 au 11/01 ; B02-D13 : T1 | DSI (Bertrand Lacassagne) | Q03 |

Le pic tombe pendant le gel, et l'e-mail B01 date du 14/10 : il ne laisse qu'un mois, sans consultation de la DPO. Ce conflit ne bloque pas la rédaction des exigences fonctionnelles de P01. Il bloque le choix du contenu et de la date de la V1 (dérogation pour un tableau de bord interne, ou mise en service au T1).

### Majeurs et mineurs

| Id | Projet | Sujet | Gravité | Positions (sources) | Arbitre | Hypothèse |
|---|---|---|---|---|---|---|
| C01 | P01 | Canal de l'alerte | majeur | SMS (B01-D5) / e-mail (B02-D5) / CT-02 (B07-D11) | Logistique et service client, avis DPO | H01 |
| C02 | P01 | Définition du retard | majeur | 48 h (B01-D7) / J+1 matin (B02-D6) | Logistique et service client | H02 |
| C04 | P01 | Automatique ou contrôlé | majeur | Aucune intervention (B01-D8) / validation Premium (B02-D8) / service client informé (B02-D14) | Responsable du service client | H03 |
| C05 | P01 | Temps réel contre statuts quotidiens | majeur | B01-D2 / B01-D10 (fichiers du matin) | Logistique et DSI | H04 |
| C06 | P01 | Colis ou commande | mineur | B01-D3 / B02-D4 | Logistique et service client | H05 |
| C07 | P01, P04 | Code promo dans l'alerte | mineur | B05-D7 / B07-D12, B02-D10 | DPO | H06 |
| C08 | P02 | Moment du remboursement | majeur | Premier scan (B03-D15) / après contrôle (B04-D2) / au dépôt (B04-D3) / « reçu » avant « remboursé » (B03-D14) | DAF puis codir | H07 |
| C09 | P02 | Délai de retour | majeur | 30 j (B03-D10) / 14 j (B04-D4) / 30 j Orvanne+ (B04-D5) | Direction de l'expérience client, après relecture juridique des CGV | H08 |
| C10 | P02 | Gratuité des retours | majeur | Gratuit (B03-D29) / 4,90 retenus hors défaut (B04-D6, D7) / gratuit pour le lancement (B04-D8) | DAF et direction de l'expérience client | H09 |
| C11 | P02, P07 | Marketplace en V1 | majeur | Exclu (B03-D5) / V1 (B04-D9) / circuit distinct (B04-D10) / MKP-06 (B09-D8) | Direction de l'expérience client et direction marketplace | H10 |
| C12 | P02, P03 | Montant selon la note C | majeur | Réduction (B04-D12, E2) / illégal (B04-D12, service client) | Direction juridique | H11 |
| C13 | P02 | Sans compte ou connecté | majeur | B03-D8 / B03-D11 | Direction de l'expérience client | H12 |
| C14 | P02 | RMA imprimé | mineur | B04-D15 / B03-D13 | Inès Rouvière et Karim Benhaddou | H13 |
| C15 | P02 | Avant les soldes contre gel et DPO | majeur | B03-D30 / B02-D12 / B07-D10 | DSI et direction de l'expérience client | H14 |
| C16 | P03 | Photo contre douchettes sans appareil | majeur | B06-D2 / B06-D6 / B06-D7 | Karim Benhaddou et DSI | H15 |
| C17 | P03 | Inventaire de janvier contre gel | majeur | B06-D13 / B02-D12 | DSI et exploitation E2 | H16 |
| C18 | P04 | Base légale et canaux | majeur | B05-D9, B05-D4 / B07-D10, B07-D11 | DPO | H17 |
| C19 | P04 | Historique depuis 2014 | majeur | B05-D3 / B07-D13 | DPO | H18 |
| C20 | P04 | Démo sur vrais clients | majeur | B05-D11 / B07-D16 | DPO | H19 |
| C21 | P06 | Durée des créneaux | majeur | 30 min (B08-D3) / 1 h sur E2 (B08-D20) / 1 h sur E1 (B08-D26) | Approvisionnement avec les chefs de site | H20 |
| C22 | P06 | Quais de E1 : 6 ou 4 | mineur | B08-N2 / B08-D26 | Chef de quai E1 | H21 |
| C23 | P06 | Messageries sans commande d'achat | majeur | R1 (B08-D2) / B08-D22 | Approvisionnement, escalade à la logistique | H22 |
| C24 | P06 | Notation et pénalités | mineur | B08-D18, B08-D19 / B08-N14 | Achats et approvisionnement | H23 |
| C25 | P07 | IBAN modifié par le vendeur | majeur | MKP-04 (B09-D6) / MKP-05 (B09-D7) | Finance | H24 |
| C26 | P07 | Alertes de retard vendeur | mineur | 2 % sur 30 j (B09-D4) / 5 % sur 7 j (B09-D12) | Direction marketplace | H25 |

### Points d'attention sans conflit déclaré

- **MKP-08 (échéance 15/01/2027, P1)** : la mise en production n'est possible qu'entre le 12 et le 15 janvier. L'échéance est compatible avec le gel, mais très serrée.
- **Bon d'achat majoré de 5 % (`B04-D14`, V2)** : s'il est proposé dans les messages du portail de retours, il faut vérifier CT-03 avec la DPO.
- **« Retard » dans P01 et dans P07** : le terme ne désigne pas la même chose (livraison au client contre expédition par le vendeur). Les specs doivent employer deux termes distincts.

## 4. Hypothèses retenues

Toutes les hypothèses sont réversibles. La plupart reposent sur un paramètre, ce qui permet d'appliquer l'arbitrage sans refonte.

| Id | Conflit | Hypothèse (résumé) |
|---|---|---|
| H01 | C01 | Canal paramétrable ; V1 par e-mail ; SMS après avis DPO et accord sur le budget |
| H02 | C02 | Seuil paramétrable : « à surveiller » à J+1 matin, « en retard » à J+2 (alerte client) |
| H03 | C04 | Envoi automatique ; liste au service client chaque matin ; pas d'envoi si un dossier est ouvert ; validation Premium désactivée |
| H04 | C05 | Rafraîchissement à chaque arrivée de statuts dans Passerelle, heure de mise à jour affichée |
| H05 | C06 | Retard évalué par colis, un seul message par commande |
| H06 | C07 | Aucune offre commerciale dans l'alerte |
| H07 | C08 | Déclencheur paramétrable ; V1 : remboursement après contrôle qualité |
| H08 | C09 | 14 j pour tous, 30 j pour Orvanne+, paramétrable |
| H09 | C10 | Frais paramétrables par motif, 0 au départ ; retenue de 4,90 activable si les CGV la prévoient |
| H10 | C11 | Marketplace en V2 |
| H11 | C12 | Remboursement intégral en V1 ; une note C déclenche un traitement manuel |
| H12 | C13 | Les deux parcours, avec ou sans compte ; l'accès sans compte est limité à la commande saisie |
| H13 | C14 | RMA en PDF à glisser dans le colis |
| H14 | C15 | Pilote au plus tôt le 12/01, après avis DPO ; décalage après les soldes si nécessaire |
| H15 | C16 | Photo facultative ; autre terminal en V2 |
| H16 | C17 | E2 au plus tôt le 12/01 ; sinon inventaire avec la fiche papier |
| H17 | C18 | V1 par e-mail aux seuls clients ayant consenti ; autres canaux après la DPO |
| H18 | C19 | Commandes du Lac et navigation des clients connectés, sur 3 ans au plus |
| H19 | C20 | Démo sur données anonymisées ou synthétiques |
| H20 | C21 | Durée de créneau paramétrable par site, 30 min par défaut |
| H21 | C22 | Nombre de quais paramétrable par site |
| H22 | C23 | R1 maintenue ; quai bloqué par le chef de quai pour les messageries |
| H23 | C24 | Ponctualité enregistrée en V1 ; notation en V2 ; pénalités hors périmètre |
| H24 | C25 | IBAN saisi par le vendeur, effectif après double validation interne |
| H25 | C26 | Deux règles d'alerte paramétrables, définition du retard commune |
| H26 | — | Textes externalisés pour la traduction ; V1 en français (P06, P07) |
| H27 | — | MKP-11 : mesurer d'abord ; index et asynchrone restent des pistes (P08) |
| H28 | — | Délai de déclaration des litiges paramétrable, 7 j provisoires (P03) |
| H29 | — | Compte à rebours depuis la réception, en jours calendaires, seuils paramétrables (P05) |
| H30 | — | Relance par règles en V1, modèle d'IA en V2 (P04) |
| H31 | — | Registre en V1 avec actions tracées à la main, orchestration automatisée en V2 (P05) |

## 5. Questions par destinataire

Seule Q03 est bloquante.

**DSI (Bertrand Lacassagne, comité d'architecture, équipe Passerelle)**
- **Q03 (bloquante)** : dérogation au gel pour un tableau de bord interne avant le pic, ou mise en service au T1 ?
- Q05 : fréquence de réception des statuts des 3 transporteurs dans Passerelle (avec Solène Garrigue).
- Q15 : date des soldes d'hiver, périmètre du pilote et fenêtre après le gel (avec Inès Rouvière et la direction de l'expérience client).
- Q16 : terminaux pour la photo (avec Karim Benhaddou).
- Q28 : pages lentes et temps de réponse attendu (avec la direction marketplace).
- Q34 : le « cloud d'Orvanne » est-il exigé pour tous les projets ?
- Q35 : le RGAA s'applique-t-il au portail fournisseurs et à l'espace vendeur ?

**Solène Garrigue (direction des opérations logistiques) et Yanis Mercadier (service client)**
- Q01 : canal de l'alerte (avec l'avis d'Hélène Marsac).
- Q02 : seuil de retard et signification des « rouges ».
- Q04 : définition de Premium et validation (Yanis Mercadier, avec Capucine Lorrain).
- Q06 : un message par colis ou par commande.
- Q39 : base de mesure des baisses de 30 % (WISMO) et de 60 % (contacts liés aux retours) (Yanis Mercadier, avec la direction de l'expérience client).

**Hélène Marsac (DPO)**
- Q07 : abandon du code promo (avec Capucine Lorrain).
- Q18 : portée du consentement newsletter et canaux de la relance.
- Q19 : données et profondeur d'historique utilisables (avec l'équipe du Lac).
- Q20 : démo sur données anonymisées (avec Capucine Lorrain).
- Q30 : date du contrôle interne, départ du compte à rebours, traitement du Lac et des sauvegardes.
- Q31 : porteur de la purge des historiques de prospection (avec Capucine Lorrain).
- Q36 : calendrier d'examen des projets P01 à P04, P06 et P07.

**Direction juridique et conformité**
- Q09 : délai de retour prévu par les CGV (avec la direction de l'expérience client).
- Q12 : légalité d'un remboursement réduit selon la note.

**DAF, codir et contrôle de gestion (Odile)**
- Q08 : moment du remboursement (chiffrage d'Odile avant le codir).
- Q10 : gratuité ou retenue de 4,90 € (avec la direction de l'expérience client et Capucine Lorrain).
- Q25 : double validation de l'IBAN (finance, avec la direction marketplace).
- Q32 : suivi du taux de retour par produit (Odile, avec l'équipe du Lac).
- Q33 : plafonds de remise de la relance (finance, avec Capucine Lorrain).

**Direction de l'expérience client et Inès Rouvière (cheffe de projet digital)**
- Q11 : marketplace en V1 ou en V2 (avec la direction marketplace et Yanis Mercadier).
- Q13 : accès au portail avec ou sans compte.
- Q14 : impression du RMA (avec Karim Benhaddou).
- Q37 : saisie de la note A / B / C sur la douchette (avec Karim Benhaddou).

**Capucine Lorrain (marketing)**
- Q33 : IA ou règles en V1.
- Voir aussi Q07, Q20, Q31 et Q10.

**Karim Benhaddou (exploitation E2)**
- Q17 : date de l'inventaire de janvier.
- Q29 : délai de déclaration des litiges et identité du « transport » (service transport à identifier).
- Voir aussi Q14, Q16, Q21 et Q37.

**Approvisionnement (Grégory Thibaudeau), E1 (Rémi Vasseur) et achats (Nadège Courtois)**
- Q21 : durée de créneau par site (avec Karim Benhaddou).
- Q22 : 6 ou 4 quais sur E1 (Rémi Vasseur).
- Q23 : messageries sans commande d'achat.
- Q24 : notation et pénalités (Nadège Courtois).
- Q27 : langues du portail (avec la direction marketplace).
- Q38 : E3 dans le périmètre.

**Direction marketplace**
- Q26 : définition du retard d'expédition et coexistence des deux alertes.
- Voir aussi Q11, Q25, Q27 et Q28.
