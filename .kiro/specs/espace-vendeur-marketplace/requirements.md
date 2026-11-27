# Exigences : Évolutions de l'espace vendeur de la marketplace

<!-- Projet P07, slug espace-vendeur-marketplace. Commanditaire : direction marketplace. Source : B09. -->

## Introduction

L'espace vendeur de la marketplace existe déjà. Les vendeurs, les chargés de compte, la finance, la DSI et la direction marketplace ont déposé entre le 02/09/2026 et le 03/11/2026 des demandes d'évolution (MKP-01 à MKP-12). Elles portent sur le suivi des ventes, les factures de commission, deux alertes de retard d'expédition, la modification de l'IBAN par le vendeur, la messagerie avec les clients, l'ouverture aux vendeurs européens, la lisibilité des reversements et l'accès mobile.

Deux conflits restent sans arbitrage : le vendeur modifie son IBAN lui-même (MKP-04) alors que la finance exige une double validation interne (MKP-05, conflit C25), et les deux alertes de retard ont des seuils et fenêtres différents (conflit C26). Ils sont traités par des hypothèses (H24, H25) et par des paramètres.

**Découpage en lots** (CT-07 : aucune mise en production du 16/11 au 11/01) :

- **Lot 1 (V1)** : ventes (MKP-01, échéance T1 2027), factures (MKP-02), alerte chargés de compte (MKP-03, fin mars), IBAN (MKP-04 et MKP-05, « ASAP »), alerte vendeur (MKP-08, 15/01/2027). Les échéances « ASAP » et du 15/01/2027 tombent juste après le gel : toute livraison avant le 16/11 suppose une mise en production avant le gel, sinon elle intervient à partir du 12/01.
- **Lot 2 (V2)** : messagerie vendeur-client (MKP-09, S1 2027), ouverture européenne (MKP-10, 2027), reversements lisibles (MKP-11), mobile (MKP-12, T2 2027).

Les correctifs d'export et de performance (projet P08) sont à livrer avant les nouvelles vues de ventes.

## Glossaire

- **Espace vendeur** : portail de la marketplace sur lequel les vendeurs partenaires consultent leur activité (B09-F15). Le système qui le porte n'est pas nommé dans les sources.
- **Vendeur** : vendeur partenaire de la marketplace sur Vitrine.
- **Chargé de compte** : collaborateur de la direction marketplace qui suit un portefeuille de vendeurs.
- **Commande expédiée en retard** : commande expédiée après la date d'expédition attendue. La définition exacte reste à fournir par la direction marketplace (Q26).
- **Taux de retard** : part de commandes expédiées en retard sur une fenêtre de calcul.
- **Comptoir** : outil du service client.
- **Hangar, Passerelle, le Lac** : systèmes d'information d'Orvanne (voir le glossaire Orvanne).

## Exigences

### Exigence 1 : Vue des ventes du vendeur

**User story :** En tant que vendeur, je veux voir en un coup d'œil mes ventes du jour, de la semaine et du mois, afin de piloter mon activité sans export.

#### Critères d'acceptation

1. QUAND un vendeur ouvre son tableau de bord, LE SYSTÈME DOIT afficher sur une seule page ses ventes du jour, de la semaine et du mois. _Source : B09-D1_
2. LE SYSTÈME DOIT limiter les ventes affichées à celles du vendeur connecté. _Source : B09-D1, CT-01_
3. SI les données de ventes sont indisponibles, ALORS LE SYSTÈME DOIT afficher un message d'indisponibilité et l'heure de la dernière actualisation connue, sans afficher de valeur à zéro. _Source : B09-D1_

### Exigence 2 : Factures de commission

**User story :** En tant que vendeur, je veux télécharger mes factures de commission, afin de ne plus les demander à la comptabilité.

#### Critères d'acceptation

1. QUAND la comptabilité produit les factures de commission en PDF pour un mois, LE SYSTÈME DOIT les rendre disponibles dans l'espace de chaque vendeur concerné. _Source : B09-D3, B09-D2_
2. QUAND un vendeur sélectionne une facture, LE SYSTÈME DOIT lui permettre de télécharger le PDF produit par la comptabilité, sans le régénérer. _Source : B09-D2, B09-D3_
3. LE SYSTÈME NE DOIT donner accès à une facture qu'au vendeur auquel elle est adressée. _Source : B09-D2, CT-01_
4. SI le PDF d'un mois n'est pas encore déposé, ALORS LE SYSTÈME DOIT indiquer que la facture de ce mois n'est pas disponible. _Source : B09-D3_

### Exigence 3 : Alerte des chargés de compte sur les retards d'expédition

**User story :** En tant que chargé de compte, je veux être alerté quand un vendeur dépasse 2 % de commandes expédiées en retard, afin d'intervenir auprès de lui.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer pour chaque vendeur le taux de commandes expédiées en retard sur 30 jours glissants. _Source : B09-D5, H25_
2. QUAND le taux d'un vendeur dépasse 2 %, LE SYSTÈME DOIT alerter les chargés de compte désignés pour ce vendeur. _Source : B09-D4, H25_
3. LE SYSTÈME DOIT proposer le seuil, la fenêtre et les destinataires de cette alerte comme paramètres, avec 2 %, 30 jours glissants et chargés de compte comme valeurs par défaut. _Source : H25_
4. LE SYSTÈME DOIT utiliser pour cette alerte la même définition de commande expédiée en retard que pour l'alerte du vendeur. _Source : H25_
5. QUAND le taux d'un vendeur reste au-dessus du seuil, LE SYSTÈME NE DOIT PAS émettre une nouvelle alerte identique tant que le taux n'est pas repassé sous le seuil. _Source : B09-D4_

### Exigence 4 : Alerte du vendeur sur son taux de retard

**User story :** En tant que vendeur, je veux être alerté dès que mon taux de retard dépasse 5 %, afin de corriger mes expéditions.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer le taux de retard de chaque vendeur sur 7 jours. _Source : B09-D13, H25_
2. QUAND le taux de retard d'un vendeur dépasse 5 %, LE SYSTÈME DOIT alerter ce vendeur dans l'espace vendeur. _Source : B09-D12, H25_
3. LE SYSTÈME DOIT proposer le seuil, la fenêtre et les destinataires de cette alerte comme paramètres, avec 5 %, 7 jours et vendeur concerné comme valeurs par défaut. _Source : H25_
4. QUAND une alerte est envoyée à un vendeur, LE SYSTÈME DOIT en informer aussi le chargé de compte du vendeur. _Source : B09-D12_
5. LE SYSTÈME DOIT être en service au plus tard le 15/01/2027. _Source : B09-D12, CT-07_

### Exigence 5 : Modification de l'IBAN avec double validation interne

**User story :** En tant que vendeur, je veux saisir moi-même mon nouvel IBAN dans l'espace vendeur, afin de ne plus passer par e-mail, et en tant que finance, je veux qu'aucun changement ne prenne effet sans double validation interne.

#### Critères d'acceptation

1. QUAND un vendeur saisit un nouvel IBAN, LE SYSTÈME DOIT enregistrer une demande de modification à l'état « en attente de validation » et conserver l'ancien IBAN actif. _Source : B09-D6, H24_
2. LE SYSTÈME NE DOIT rendre un nouvel IBAN effectif qu'après deux validations internes réalisées par deux personnes distinctes, différentes de l'auteur de la demande. _Source : B09-D7, H24_
3. PENDANT QUE la demande est en attente, LE SYSTÈME DOIT utiliser l'ancien IBAN pour les reversements et afficher au vendeur l'état de sa demande. _Source : H24_
4. SI une validation est refusée, ALORS LE SYSTÈME DOIT conserver l'ancien IBAN, clore la demande et en informer le vendeur. _Source : B09-D7, H24_
5. QUAND une demande est créée, validée ou refusée, LE SYSTÈME DOIT journaliser l'auteur, l'horodatage et la décision, sans enregistrer l'IBAN en clair dans le journal. _Source : CT-10, B09-D7_
6. LE SYSTÈME DOIT proposer les rôles des deux valideurs comme paramètre, à fixer par la finance. _Source : H24, B09-D7_
7. QUAND une demande est créée, LE SYSTÈME DOIT notifier les valideurs désignés. _Source : B09-D7, H24_

### Exigence 6 : Messagerie vendeur-client (lot 2)

**User story :** En tant que vendeur, je veux répondre aux questions des clients depuis l'espace vendeur, afin de ne pas utiliser d'autre outil.

#### Critères d'acceptation

1. QUAND un client pose une question sur un article d'un vendeur, LE SYSTÈME DOIT la rendre visible dans l'espace de ce vendeur. _Source : B09-D14_
2. QUAND un vendeur répond, LE SYSTÈME DOIT transmettre la réponse au client et la conserver dans l'historique de l'échange. _Source : B09-D14_
3. LE SYSTÈME DOIT proposer le canal (Comptoir ou messagerie dédiée) comme choix de conception à arbitrer avant le lot 2. _Source : B09-D14_
4. LE SYSTÈME DOIT soumettre le traitement des échanges à la DPO avant tout développement. _Source : CT-01, B09-D14_

### Exigence 7 : Ouverture aux vendeurs européens (lot 2)

**User story :** En tant que direction marketplace, je veux ouvrir l'espace vendeur aux vendeurs européens, en commençant par l'Allemagne et l'Espagne, afin d'étendre la marketplace.

#### Critères d'acceptation

1. QUAND un vendeur établi en Allemagne ou en Espagne est créé, LE SYSTÈME DOIT lui donner accès à l'espace vendeur. _Source : B09-D15, B09-D16_
2. LE SYSTÈME DOIT permettre de proposer les écrans et messages du vendeur dans une langue autre que le français, la liste des langues étant un paramètre. _Source : CT-11, B09-D15_
3. LE SYSTÈME DOIT permettre d'ajouter un pays d'ouverture par paramétrage, sans développement. _Source : B09-D15, B09-D16_

### Exigence 8 : Reversements compréhensibles (lot 2)

**User story :** En tant que vendeur, je veux comprendre le détail de mes reversements, afin de vérifier les sommes reçues.

#### Critères d'acceptation

1. QUAND un vendeur ouvre un reversement, LE SYSTÈME DOIT afficher le détail du calcul (ventes, commission, ajustements, montant reversé). _Source : B09-D18_
2. LE SYSTÈME DOIT valider la lisibilité de l'écran lors d'un test avec au moins 5 vendeurs, dont des vendeurs du top 20. _Source : B09-D18, B09-D6_

### Exigence 9 : Tableau de bord sur mobile (lot 2)

**User story :** En tant que vendeur, je veux consulter mon tableau de bord sur mobile, afin de suivre mon activité en déplacement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT rendre le tableau de bord vendeur utilisable sur un écran de smartphone. _Source : B09-D19_
2. LE SYSTÈME DOIT proposer la forme (application ou site adapté) comme choix de conception à arbitrer, le site adapté étant la valeur par défaut. _Source : B09-D19_
3. LE SYSTÈME DOIT respecter le RGAA pour les écrans de l'espace vendeur, sous réserve de la confirmation de Q35. _Source : CT-09_

### Exigence 10 : Contraintes transverses

**User story :** En tant que DSI et DPO, je veux que les évolutions respectent les contraintes d'Orvanne, afin de limiter les risques.

#### Critères d'acceptation

1. LE SYSTÈME NE DOIT PAS utiliser de données de production pour les démonstrations ni les tests sans anonymisation préalable. _Source : CT-04_
2. LE SYSTÈME NE DOIT PAS être mis en production entre le 16 novembre et le 11 janvier. _Source : CT-07_
3. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_
4. LE SYSTÈME DOIT journaliser les actions réalisées par un collaborateur pour le compte d'un vendeur, avec une preuve d'exécution. _Source : CT-10_
5. LE SYSTÈME NE DOIT traiter de nouvelles données personnelles qu'après l'avis de la DPO. _Source : CT-01_

## Hors périmètre

- Suivi des retours et litiges par le vendeur (`B09-D8`, MKP-06) : dépend du circuit de retours marketplace, V2 du portail de retours (H10), renvoyée vers P02.
- Export des ventes en erreur au-delà de 50 000 lignes (`B09-D9`, MKP-07) : défaut de l'existant, renvoyé vers P08.
- Index sur la table des lignes de commande (`B09-D10`) : piste de conception de la spec bugfix, renvoyée vers P08.
- Export asynchrone (`B09-D11`) : piste de conception de la spec bugfix, renvoyée vers P08.
- Lenteur de l'espace vendeur (`B09-D17`, MKP-11) : défaut à mesurer puis corriger, renvoyé vers P08. La lisibilité des reversements (`B09-D18`) reste dans ce projet (exigence 8).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H10 | La V1 exclut les articles marketplace du portail de retours ; le suivi des retours par le vendeur (MKP-06) forme la V2 de P02. | C11 | oui |
| H24 | Le vendeur saisit son nouvel IBAN ; le changement ne prend effet qu'après double validation interne, l'ancien IBAN restant utilisé entre-temps. | C25 | oui |
| H25 | Deux règles d'alerte distinctes et paramétrables (2 % sur 30 jours pour les chargés de compte, 5 % sur 7 jours pour le vendeur), sur une même définition du retard. | C26 | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q11 | Les retours marketplace entrent-ils en V1 ou en V2 du portail ? Qui fournit les étiquettes et le circuit vers les vendeurs ? | Direction de l'expérience client ; direction marketplace | non |
| Q25 | Un IBAN saisi par le vendeur puis validé par deux personnes respecte-t-il MKP-05 ? Qui sont les deux valideurs ? | Finance (DAF) ; direction marketplace | non (la validation de l'exigence 5 reste à confirmer) |
| Q26 | Qu'est-ce qu'une commande expédiée en retard ? Les deux alertes doivent-elles coexister ? | Direction marketplace | non (exigences 3 et 4) |
| Q27 | Dans quelles langues proposer l'espace vendeur, et pour quelle version ? | Grégory Thibaudeau ; direction marketplace | non (exigence 7) |
| Q34 | L'hébergement dans le cloud d'Orvanne s'applique-t-il à ce projet, ou l'UE chez un éditeur est-elle admise ? | DSI (comité d'architecture) | non (exigence 10) |
| Q35 | La conformité RGAA s'applique-t-elle à l'espace vendeur ? | DSI (comité d'architecture) | non (critère 9.3) |
| Q36 | Quand examiner les traitements de ce projet, et lesquels exigent une analyse d'impact ? | Hélène Marsac | non (exigences 5, 6 et 10) |
