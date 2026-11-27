# Exigences : Portail de retours en libre-service, remboursement et visibilité des entrepôts

<!-- Projet P02, slug portail-retours. Commanditaire : Direction de l'expérience client. Sources : B03, B04, B09. -->

## Introduction

Le service client traite environ 900 demandes de retour par jour ouvré et met en moyenne 2,5 jours à envoyer l'étiquette. L'entrepôt E2 reçoit environ 1 100 colis retour par jour, sans visibilité préalable, avec 1 retour sur 5 non conforme à l'ouverture et un contrôle qui prend 3 à 6 jours (10 jours en janvier). Le portail de retours permet au client de déclarer un retour sur Vitrine (site et application mobile) et d'obtenir son étiquette en moins de 3 minutes, de suivre son remboursement, et donne aux entrepôts la liste des retours attendus. L'objectif est de réduire de 60 % les contacts liés aux retours en 6 mois.

Les sources se contredisent sur plusieurs règles (moment du remboursement, délai, frais, marketplace, montant selon la note, accès sans compte, RMA, date de mise en service). Chaque règle non arbitrée est donc un **paramètre** avec une valeur initiale prudente, rattachée à une hypothèse (H07 à H14) et à une question ouverte.

**Découpage en lots.**
- **V1 (pilote)** : retours des articles vendus par Orvanne, parcours client, étiquette, suivi, remboursement après contrôle, liste prévisionnelle des entrepôts, outil du service client. Mise en service au plus tôt le 12 janvier, après le gel (CT-07) et la consultation de la DPO (CT-01).
- **V2** : photos jointes par le client, retours marketplace et suivi par le vendeur. L'idée du bon d'achat majoré n'est pas retenue (voir Hors périmètre).

## Glossaire

- **Vitrine** : site marchand et application mobile d'Orvanne.
- **Comptoir** : outil du service client.
- **Hangar** : système de gestion des entrepôts E1, E2, E3.
- **Passerelle** : plateforme d'échange de flux (commandes, statuts transporteurs).
- **RMA** : autorisation de retour, imprimée et placée dans le colis.
- **Grille A / B / C** : note de contrôle qualité d'un retour. A : remis en stock. B : déstockage. C : rebut.
- **Orvanne+** : programme de fidélité (délai de retour de 30 jours).
- **Déclencheur de remboursement** : événement qui provoque le remboursement (premier scan transporteur, réception en entrepôt ou contrôle qualité).
- **Catégories exclues** : hygiène, produits personnalisés, denrées.

## Exigences

### Exigence 1 : Accès au portail

**User story :** En tant que client, je veux accéder au portail avec ou sans compte, afin de déclarer un retour sans démarche préalable.

#### Critères d'acceptation

1. QUAND un client saisit un numéro de commande et l'adresse e-mail de l'achat, LE SYSTÈME DOIT ouvrir le portail sur cette commande sans création de compte. _Source : B03-D8, H12_
2. QUAND un client connecté à son compte ouvre le portail, LE SYSTÈME DOIT lui présenter ses commandes éligibles et lui permettre de sélectionner les articles à retourner. _Source : B03-D11, H12_
3. PENDANT QU'un client accède au portail sans compte, LE SYSTÈME NE DOIT PAS donner accès à une autre commande que celle saisie. _Source : H12_
4. SI le couple numéro de commande et e-mail ne correspond à aucune commande, ALORS LE SYSTÈME DOIT afficher un message identique quel que soit le motif de l'échec et bloquer les essais après un nombre d'échecs paramétrable (valeur initiale : 5 en 15 minutes). _Source : B03-D8, H12_

### Exigence 2 : Éligibilité des articles

**User story :** En tant que client, je veux savoir quels articles de ma commande je peux retourner, afin de ne pas faire de demande refusée.

#### Critères d'acceptation

1. QUAND le client ouvre une commande, LE SYSTÈME DOIT afficher pour chaque article s'il est éligible au retour et, sinon, le motif d'inéligibilité. _Source : B03-D9_
2. LE SYSTÈME DOIT calculer la date limite de retour à partir de la date de livraison avec un délai paramétrable par catégorie de client, de valeur initiale 14 jours pour tous et 30 jours pour les membres Orvanne+. _Source : B03-D10, B04-D4, B04-D5, H08_
3. LE SYSTÈME DOIT déclarer inéligibles les articles des catégories exclues (hygiène, produits personnalisés, denrées). _Source : B03-D10_
4. LE SYSTÈME DOIT limiter le périmètre aux articles vendus et expédiés par Orvanne, livrés en France métropolitaine et commandés sur Vitrine (site web et application mobile). _Source : B03-D4_
5. LE SYSTÈME DOIT déclarer inéligibles les articles volumineux livrés sur rendez-vous. _Source : B03-D6_
6. LE SYSTÈME NE DOIT PAS proposer d'échange : un échange est traité comme un retour suivi d'une nouvelle commande. _Source : B03-D7_

### Exigence 3 : Déclaration du retour

**User story :** En tant que client, je veux déclarer mon retour en choisissant articles, quantité, motif et mode de retour, afin d'obtenir mon étiquette.

#### Critères d'acceptation

1. QUAND le client sélectionne un article éligible, LE SYSTÈME DOIT lui demander la quantité et un motif choisi dans une liste fermée. _Source : B03-D11_
2. SI la quantité saisie dépasse la quantité commandée et non encore retournée, ALORS LE SYSTÈME DOIT refuser la saisie et indiquer la quantité maximale. _Source : B03-D11_
3. QUAND le client valide la sélection, LE SYSTÈME DOIT lui proposer le dépôt en point relais ou l'enlèvement à domicile. _Source : B03-D12_
4. LE SYSTÈME DOIT lire les commandes et les livraisons dans le système de gestion des commandes via Passerelle. _Source : B03-D24_
5. SI Passerelle ne répond pas dans un délai paramétrable (valeur initiale : 5 secondes), ALORS LE SYSTÈME DOIT afficher un message invitant à réessayer et ne créer aucun retour partiel. _Source : B03-D24_

### Exigence 4 : Étiquette et RMA

**User story :** En tant que client, je veux recevoir une étiquette prépayée immédiatement, afin de déposer ou faire enlever mon colis.

#### Critères d'acceptation

1. QUAND le client valide sa déclaration, LE SYSTÈME DOIT obtenir une étiquette prépayée auprès de l'API du transporteur et la générer en PDF avec un QR code. _Source : B03-D13, B03-D25_
2. QUAND l'étiquette est générée, LE SYSTÈME DOIT l'envoyer par e-mail à l'adresse de l'achat et l'afficher sur le portail. _Source : B03-D13_
3. QUAND l'étiquette est générée, LE SYSTÈME DOIT produire un RMA en PDF, à imprimer et placer dans le colis, qui permet à l'entrepôt de retrouver la commande. _Source : B04-D15, H13_
4. SI l'API du transporteur est indisponible, ALORS LE SYSTÈME DOIT enregistrer le retour au statut « en attente d'étiquette », relancer l'appel automatiquement et envoyer l'étiquette dès qu'elle est obtenue. _Source : B03-D25_
5. LE SYSTÈME NE DOIT PAS inclure d'offre commerciale dans les e-mails d'étiquette et de suivi. _Source : CT-03_

### Exigence 5 : Suivi du retour par le client

**User story :** En tant que client, je veux suivre l'avancement de mon retour, afin de ne pas contacter le service client.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher pour chaque retour l'un des statuts « déclaré », « déposé », « reçu » ou « remboursé ». _Source : B03-D14_
2. QUAND Passerelle remonte le premier scan du colis par le transporteur, LE SYSTÈME DOIT passer le retour au statut « déposé ». _Source : B03-D15, B03-D14_
3. LE SYSTÈME DOIT faire passer le statut « reçu » avant le statut « remboursé » pour tout retour, quel que soit le déclencheur de remboursement paramétré. _Source : B03-D14, H07_

### Exigence 6 : Remboursement

**User story :** En tant que client, je veux être remboursé sur mon moyen de paiement d'origine, afin de récupérer mon argent.

#### Critères d'acceptation

1. LE SYSTÈME DOIT disposer d'un paramètre « déclencheur de remboursement » à trois valeurs (premier scan transporteur, réception en entrepôt, contrôle qualité), de valeur initiale « contrôle qualité ». _Source : B03-D15, B04-D2, B04-D3, H07_
2. QUAND l'événement correspondant au déclencheur paramétré survient, LE SYSTÈME DOIT demander le remboursement au prestataire de paiement. _Source : B03-D26, H07_
3. LE SYSTÈME DOIT effectuer le remboursement sur le moyen de paiement d'origine. _Source : B03-D27_
4. LE SYSTÈME NE DOIT PAS déclencher plus d'un remboursement par ligne de retour, y compris en cas de nouvel appel ou de scan en double. _Source : B03-D26, H07_
5. SI le prestataire de paiement refuse ou ne répond pas, ALORS LE SYSTÈME DOIT conserver le retour au statut « remboursement en échec », le représenter automatiquement selon un calendrier paramétrable et alerter le service client après 3 échecs (valeur initiale). _Source : B03-D26_
6. LE SYSTÈME DOIT enregistrer pour chaque retour contrôlé la note de la grille A / B / C (A remis en stock, B déstockage, C rebut). _Source : B04-D11_
7. LE SYSTÈME DOIT calculer le montant remboursé sans tenir compte de la note A / B / C. _Source : B04-D12, H11_
8. QUAND la note est C, LE SYSTÈME DOIT créer un signalement dans Comptoir pour traitement manuel par le service client, sans réduire automatiquement le remboursement. _Source : B04-D12, H11_

### Exigence 7 : Frais de retour

**User story :** En tant que responsable de l'expérience client, je veux piloter les frais de retour par paramètre, afin d'appliquer la règle arbitrée sans développement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT appliquer des frais de retour paramétrables par motif, de valeur initiale 0 pour tous les motifs (retours gratuits). _Source : B03-D29, B04-D8, H09_
2. OÙ des frais non nuls sont paramétrés pour un motif, LE SYSTÈME DOIT les retenir sur le remboursement, la valeur candidate étant 4,90 (euros) hors article défectueux ou erreur de préparation. _Source : B04-D6, B04-D7, H09_
3. OÙ des frais non nuls sont paramétrés, LE SYSTÈME DOIT les afficher au client avant la validation de la déclaration. _Source : B04-D7, H09_

### Exigence 8 : Visibilité des retours pour les entrepôts

**User story :** En tant que responsable d'entrepôt, je veux connaître les retours attendus, afin d'organiser la réception et le contrôle.

#### Critères d'acceptation

1. QUAND un retour est déclaré, LE SYSTÈME DOIT l'inclure dans la liste prévisionnelle de l'entrepôt de destination avec la référence RMA, les articles et les quantités. _Source : B03-D16, B03-D3_
2. LE SYSTÈME DOIT transmettre à Hangar un fichier quotidien des retours attendus par entrepôt, selon un horaire paramétrable. _Source : B03-D28_
3. SI la génération ou le dépôt du fichier échoue, ALORS LE SYSTÈME DOIT alerter l'exploitation et rejouer l'envoi sans doublon de retours. _Source : B03-D28_

### Exigence 9 : Outil du service client

**User story :** En tant que conseiller du service client, je veux créer ou corriger un retour pour un client, afin de traiter les cas hors libre-service.

#### Critères d'acceptation

1. QUAND un conseiller le demande depuis Comptoir, LE SYSTÈME DOIT permettre de créer ou de corriger un retour pour le compte d'un client. _Source : B03-D18_
2. LE SYSTÈME DOIT journaliser chaque action d'un conseiller (auteur, date, retour, valeurs avant et après) de façon non modifiable. _Source : B03-D23, CT-10_
3. LE SYSTÈME DOIT conserver une preuve d'exécution de chaque action d'un conseiller. _Source : CT-10_

### Exigence 10 : Retours marketplace (V1 exclus, V2 prévus)

**User story :** En tant que client ayant acheté chez un vendeur partenaire, je veux savoir comment retourner mon article, afin de ne pas être bloqué.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher les articles des vendeurs partenaires comme non éligibles au portail en V1, avec un renvoi vers le circuit de retour actuel. _Source : B03-D5, B04-D9, H10_
2. OÙ les retours marketplace sont activés (V2), LE SYSTÈME NE DOIT PAS adresser ces retours aux entrepôts Orvanne mais au vendeur, avec un circuit et des étiquettes distincts. _Source : B04-D10, H10_
3. OÙ les retours marketplace sont activés (V2), LE SYSTÈME DOIT permettre au vendeur de suivre ses retours et litiges, y compris les retours déclarés par les clients sur ses articles. _Source : B09-D8, H10_

### Exigence 11 : Photos jointes au retour (V2)

**User story :** En tant que client, je veux joindre des photos d'un article endommagé, afin d'étayer ma demande.

#### Critères d'acceptation

1. OÙ la fonction photos est activée (V2), QUAND le motif est « article endommagé », LE SYSTÈME DOIT permettre de joindre jusqu'à 3 photos. _Source : B03-D17_
2. OÙ la fonction photos est activée (V2), LE SYSTÈME DOIT rendre les photos consultables par l'exploitation E2 avant la réception du colis. _Source : B04-D1_
3. OÙ la fonction photos est activée (V2), LE SYSTÈME DOIT traiter les photos comme des données personnelles : accès restreint, suppression à une durée de conservation paramétrable et information du client. _Source : CT-06_

### Exigence 12 : Disponibilité et performance

**User story :** En tant que client, je veux un portail disponible et rapide, afin de déclarer mon retour sans attente.

#### Critères d'acceptation

1. LE SYSTÈME DOIT atteindre une disponibilité de 99,5 %, mesurée mensuellement. _Source : B03-D19_
2. LE SYSTÈME DOIT afficher ses pages en moins de 2 secondes pour 95 % des requêtes, jusqu'à 300 utilisateurs simultanés. _Source : B03-D20_

### Exigence 13 : Objectifs et recette

**User story :** En tant que commanditaire, je veux mesurer les objectifs du portail, afin de valider sa mise en service.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à un client de déclarer un retour et d'obtenir son étiquette en moins de 3 minutes, sans contact avec un conseiller. _Source : B03-D1_
2. LE SYSTÈME DOIT fournir un indicateur mensuel des contacts liés aux retours, afin de vérifier une baisse de 60 % en 6 mois par rapport à une base de référence à fixer. _Source : B03-D2_
3. QUAND la recette est menée, LE SYSTÈME DOIT permettre à un client non accompagné de réaliser un retour standard de bout en bout sur mobile. _Source : B03-D31_

### Exigence 14 : Conformité, sécurité et hébergement

**User story :** En tant que DPO et responsable de la DSI, je veux que le portail respecte les règles de conformité, afin de limiter les risques juridiques.

#### Critères d'acceptation

1. LE SYSTÈME DOIT être conforme au RGAA et utilisable sur mobile. _Source : B03-D22, CT-09_
2. LE SYSTÈME DOIT être hébergé dans l'Union européenne et conforme au RGPD. _Source : B03-D21, CT-08_
3. LE SYSTÈME NE DOIT PAS entrer en développement avant la consultation de la DPO sur le traitement des données personnelles des retours. _Source : CT-01_
4. LE SYSTÈME NE DOIT PAS utiliser de données de production dans les tests et démonstrations sans anonymisation. _Source : CT-04_

### Exigence 15 : Mise en service

**User story :** En tant que chef de projet, je veux planifier le pilote hors gel, afin d'éviter une mise en production interdite.

#### Critères d'acceptation

1. LE SYSTÈME NE DOIT PAS être mis en production entre le 16 novembre et le 11 janvier. _Source : CT-07_
2. LE SYSTÈME DOIT être mis en service sur un périmètre pilote au plus tôt le 12 janvier, après la consultation de la DPO. _Source : B03-D30, H14, CT-01_
3. SI la date des soldes d'hiver ne laisse pas de fenêtre suffisante après le gel, ALORS LE SYSTÈME DOIT décaler la mise en service du pilote après les soldes plutôt que de la placer pendant le gel. _Source : B03-D30, H14, CT-07_

## Hors périmètre

- Application douchette de saisie de la note et de la photo au contrôle qualité (`B04-D13`) : même écran que la déclaration de casse, traitée dans P03. Renvoyée vers P03. Le portail consomme la note saisie (exigence 6).
- Suivi du taux de retour par produit (`B04-D16`) : indicateur analytique du Lac, à l'état d'idée, sans porteur identifié. Renvoyé vers aucun projet.
- Bon d'achat majoré de 5 % à la place du remboursement (`B04-D14`) : idée, non arbitrée, non retenue en V1 ni en V2. Renvoyée vers aucun projet.
- Chiffrage du coût du remboursement anticipé avant le codir (`B04-D17`) : travail du contrôle de gestion, pas une exigence du système. Il éclaire le choix du déclencheur (exigence 6).
- Réduction du montant remboursé selon la note C : écartée en V1 (H11), en attente de l'avis juridique (`B04-D12`).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H07 | Le déclencheur du remboursement est un paramètre ; la V1 rembourse après le contrôle qualité, le statut « reçu » précède « remboursé ». | C08 | oui |
| H08 | Le délai d'éligibilité est un paramètre par catégorie de client : 14 jours pour tous, 30 jours pour Orvanne+. | C09 | oui |
| H09 | Les frais de retour sont un paramètre par motif, initialement 0 ; la retenue de 4,90 s'active sans développement. | C10 | oui |
| H10 | La V1 exclut les articles marketplace ; retours marketplace et suivi vendeur en V2. | C11 | oui |
| H11 | En V1, le montant remboursé ne dépend pas de la note ; une note C déclenche un signalement manuel. | C12 | oui |
| H12 | Accès sans compte par numéro de commande et e-mail, et accès connecté ; l'accès sans compte est limité à la commande saisie. | C13 | oui |
| H13 | Le portail produit un RMA en PDF à imprimer et placer dans le colis ; le cas sans imprimante reste ouvert. | C14 | oui |
| H14 | Le pilote est mis en service au plus tôt le 12 janvier, après le gel et la consultation de la DPO ; sinon décalé après les soldes. | C15 | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q08 | Moment du remboursement : premier scan, réception ou contrôle ? Remboursement anticipé pour certains clients ? | DAF, puis codir | non (valeur du paramètre, exigence 6) |
| Q09 | Délai de retour : 14 jours / 30 jours Orvanne+, ou 30 jours pour tous ? | Direction de l'expérience client ; direction juridique | non (exigence 2) |
| Q10 | Retours gratuits pour tous ou 4,90 € retenus hors défaut ? Jusqu'à quand la gratuité de lancement ? | DAF ; direction de l'expérience client | non (exigence 7) |
| Q11 | Retours marketplace en V1 ou V2 ? Qui fournit les étiquettes et le circuit ? | Direction de l'expérience client ; direction marketplace | non (exigence 10) |
| Q12 | Une réduction du remboursement selon la note C est-elle légale ? | Direction juridique et conformité | non (exigence 6) |
| Q13 | Portail sans compte, connecté ou les deux ? Quelle vérification sans compte ? | Inès Rouvière | non (exigence 1) |
| Q14 | RMA imprimé obligatoire ? Que faire sans imprimante ? | Karim Benhaddou ; Inès Rouvière | non (exigence 4) |
| Q15 | Date des soldes d'hiver et périmètre du pilote ? | Inès Rouvière ; DSI | non (exigence 15) |
| Q32 | Qui suit le taux de retour par produit ? | Contrôle de gestion ; équipe du Lac | non (hors périmètre) |
| Q34 | L'hébergement « cloud d'Orvanne » s'applique-t-il à tous les projets ? | DSI | non (exigence 14) |
| Q35 | Le RGAA s'applique-t-il aux autres interfaces externes ? | DSI | non (exigence 14) |
| Q36 | Quand la DPO examine-t-elle le traitement ? Analyse d'impact requise ? | Hélène Marsac | non (exigences 14 et 15) |
| Q37 | La note A / B / C est-elle saisie sur l'application douchette de la casse, en V1 ? | Karim Benhaddou ; Inès Rouvière | non (exigence 6) |
| Q39 | Base de référence et période de mesure de la baisse de 60 % des contacts ? | Yanis Mercadier | non (exigence 13) |
