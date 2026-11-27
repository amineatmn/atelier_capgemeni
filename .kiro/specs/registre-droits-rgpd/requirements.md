# Exigences : Registre et traitement des demandes d'exercice de droits RGPD

<!-- Projet P05, slug registre-droits-rgpd. Commanditaire : Direction juridique et conformité (DPO). Source : B07. -->

## Introduction

Les demandes d'exercice de droits (accès, rectification, effacement, opposition) sont suivies dans un classeur partagé tenu par une équipe de 2 personnes. Sur les neuf premiers mois de 2026, 412 demandes ont été enregistrées, dont 61 % d'effacement, et 17 ont été traitées au-delà du délai légal d'un mois. Les demandes reçues par le chat et les réseaux sociaux ne sont pas toujours reconnues comme telles, et aucune preuve d'exécution n'est conservée. La déléguée à la protection des données (DPO) demande un registre unique, un compte à rebours avec alertes, la preuve de clôture, un export d'accès, un traitement de l'effacement et un tableau de bord trimestriel.

**Lots.** La première version (lot V1) est attendue avant le prochain contrôle interne, dont la date est inconnue (Q30). Elle couvre le registre, le compte à rebours, la saisie par le service client, la preuve de clôture, l'export d'accès et le tableau de bord ; les actions dans chaque système y sont tracées manuellement (H31). L'orchestration automatisée dans les systèmes (lot V2) vient ensuite. Aucune mise en production n'a lieu du 16 novembre au 11 janvier (CT-07) : la note source date du 9 novembre 2026, donc une mise en service pendant ce gel est exclue.

## Glossaire

- **Demande** : demande d'exercice de droits d'un client ou d'un tiers (accès, rectification, effacement, opposition).
- **Registre** : base unique des demandes, objet de cette spec.
- **Équipe DPO** : équipe de la déléguée à la protection des données (2 personnes).
- **Échéance** : date limite de traitement d'une demande, calculée à partir de sa date de réception (H29).
- **Preuve de clôture** : trace conservée attestant que les actions demandées ont été exécutées.
- **Vitrine, Comptoir, Hangar, le Lac, outil d'e-mailing** : systèmes d'information d'Orvanne concernés par les données clients (voir glossaire Orvanne).

## Exigences

### Exigence 1 : Registre unique des demandes

**User story :** En tant que membre de l'équipe DPO, je veux un registre unique des demandes, afin de ne plus dépendre d'un classeur partagé et de pouvoir justifier chaque traitement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT enregistrer pour chaque demande : canal, date de réception, type, identité vérifiée ou non, systèmes concernés, échéance, statut et preuve de clôture. _Source : B07-D1_
2. LE SYSTÈME DOIT proposer les types de demande accès, rectification, effacement et opposition à la prospection. _Source : B07-D1_
3. QUAND un utilisateur crée, modifie ou clôture une demande, LE SYSTÈME DOIT journaliser l'action avec l'identité de l'utilisateur et l'horodatage. _Source : B07-D1, CT-10_
4. SI une demande est clôturée sans preuve de clôture, ALORS LE SYSTÈME DOIT refuser la clôture et afficher le motif. _Source : B07-D1_

### Exigence 2 : Délai légal et compte à rebours

**User story :** En tant que membre de l'équipe DPO, je veux un compte à rebours par demande avec des alertes, afin de ne plus dépasser le délai légal.

#### Critères d'acceptation

1. LE SYSTÈME DOIT fixer l'échéance d'une demande à un mois après sa date de réception, en jours calendaires. _Source : B07-D4, H29_
2. LE SYSTÈME DOIT afficher pour chaque demande ouverte le nombre de jours restants avant l'échéance. _Source : B07-D2_
3. QUAND une demande ouverte atteint J+15 après sa réception, LE SYSTÈME DOIT envoyer une alerte à l'équipe DPO. _Source : B07-D2, H29_
4. QUAND une demande ouverte atteint J+25 après sa réception, LE SYSTÈME DOIT envoyer une alerte à l'équipe DPO. _Source : B07-D2, H29_
5. LE SYSTÈME DOIT lire les seuils d'alerte J+15 et J+25 dans un paramètre modifiable sans développement. _Source : H29_
6. QUAND une demande est clôturée après son échéance, LE SYSTÈME DOIT la marquer « traitée hors délai » pour le tableau de bord. _Source : B07-D4, B07-D9_

### Exigence 3 : Prolongation du délai

**User story :** En tant que membre de l'équipe DPO, je veux prolonger le délai de deux mois en motivant ma décision, afin de traiter les demandes complexes dans le cadre légal.

#### Critères d'acceptation

1. QUAND l'équipe DPO prolonge une demande, LE SYSTÈME DOIT exiger un motif et repousser l'échéance de 2 mois. _Source : B07-D3, H29_
2. LE SYSTÈME DOIT conserver le motif, l'auteur et la date de chaque prolongation dans l'historique de la demande. _Source : B07-D3, CT-10_
3. LE SYSTÈME DOIT lire la durée de prolongation et les seuils d'alerte d'une demande prolongée dans des paramètres. _Source : H29_

### Exigence 4 : Saisie des demandes par le service client

**User story :** En tant qu'agent du service client, je veux enregistrer dans le registre les demandes reçues sur mes canaux, afin qu'aucune demande ne reste hors du suivi.

#### Critères d'acceptation

1. QUAND un agent du service client saisit une demande reçue par un canal, LE SYSTÈME DOIT l'enregistrer avec ce canal et la date de réception réelle. _Source : B07-D18, B07-D1_
2. LE SYSTÈME DOIT limiter les droits du service client à la création et à la consultation de ses propres saisies, sans accès aux données exportées ni aux motifs de prolongation. _Source : B07-D18, CT-10_
3. QUAND une demande est saisie, LE SYSTÈME DOIT avertir l'équipe DPO dans les 5 minutes. _Source : B07-D18, B07-D2_

### Exigence 5 : Demande d'accès et export lisible

**User story :** En tant que demandeur, je veux recevoir un export lisible de mes données par un canal sécurisé, afin d'exercer mon droit d'accès.

#### Critères d'acceptation

1. QUAND une demande d'accès est instruite, LE SYSTÈME DOIT produire un export lisible des données du demandeur. _Source : B07-D6_
2. LE SYSTÈME DOIT remettre l'export au demandeur par un canal sécurisé, avec un lien à durée limitée paramétrable (valeur initiale : 7 jours). _Source : B07-D6, CT-08_
3. SI l'identité du demandeur n'est pas vérifiée, ALORS LE SYSTÈME NE DOIT PAS remettre l'export. _Source : B07-D6, B07-D1_
4. QUAND un export est remis, LE SYSTÈME DOIT conserver dans la demande la date et le mode de remise comme preuve. _Source : B07-D6, B07-D1_

### Exigence 6 : Demande d'effacement et conservation légale

**User story :** En tant que membre de l'équipe DPO, je veux que l'effacement supprime ou anonymise les données sauf celles à conserver légalement, afin de respecter le droit à l'effacement sans perdre les pièces obligatoires.

#### Critères d'acceptation

1. QUAND une demande d'effacement est instruite, LE SYSTÈME DOIT enregistrer pour chaque système concerné l'action retenue : suppression, anonymisation ou conservation motivée. _Source : B07-D7_
2. LE SYSTÈME DOIT identifier les données soumises à une obligation légale de conservation, dont les factures conservées 10 ans, et les isoler du traitement courant. _Source : B07-D8, B07-D7_
3. SI une donnée à effacer figure dans une catégorie de conservation légale, ALORS LE SYSTÈME DOIT l'exclure de l'effacement et consigner la base de la conservation dans la demande. _Source : B07-D7, B07-D8_
4. LE SYSTÈME DOIT enregistrer pour le Lac et les sauvegardes l'action retenue ou leur exclusion motivée, sans règle automatique tant que la DPO n'a pas décidé. _Source : B07-D7_

### Exigence 7 : Traçabilité et orchestration dans les systèmes

**User story :** En tant que membre de l'équipe DPO, je veux suivre les actions menées dans chaque système, afin de prouver l'exécution des demandes.

#### Critères d'acceptation

1. LE SYSTÈME DOIT proposer, pour chaque demande, la liste des systèmes concernés parmi Vitrine, Comptoir, Hangar, le Lac et l'outil d'e-mailing, avec un statut d'action par système. _Source : B07-D5, H31_
2. EN V1, QUAND une action est réalisée dans un système, LE SYSTÈME DOIT permettre de la tracer manuellement avec l'auteur, la date et un commentaire. _Source : B07-D5, H31, CT-10_
3. SI une demande contient un système sans action tracée, ALORS LE SYSTÈME DOIT refuser la clôture. _Source : B07-D5, B07-D1_
4. EN V2, QUAND une demande d'effacement ou d'accès est validée, LE SYSTÈME DOIT déclencher l'action dans Vitrine, Comptoir, Hangar, le Lac et l'outil d'e-mailing et en enregistrer le résultat. _Source : B07-D5, H31_
5. EN V2, LE SYSTÈME DOIT permettre de déclarer un nouveau système stockant des données clients sans développement du cœur du registre. _Source : B07-D5, H31, CT-01_

### Exigence 8 : Tableau de bord trimestriel

**User story :** En tant que membre du comité des risques, je veux un tableau de bord trimestriel, afin de suivre le respect des délais.

#### Critères d'acceptation

1. LE SYSTÈME DOIT produire chaque trimestre un tableau de bord pour le comité des risques. _Source : B07-D9_
2. LE SYSTÈME DOIT y présenter au minimum le nombre de demandes par type et par canal, le nombre de demandes traitées hors délai et le nombre de prolongations. _Source : B07-D9, B07-D4_
3. LE SYSTÈME DOIT permettre l'export du tableau de bord pour un trimestre choisi. _Source : B07-D9_

### Exigence 9 : Utilisabilité

**User story :** En tant que membre de l'équipe DPO, je veux un outil simple, afin de l'utiliser sans formation lourde.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à un membre de l'équipe DPO sans formation préalable de saisir une demande et de la clôturer en suivant un guide de 1 page au plus, vérifié en recette par 2 utilisateurs. _Source : B07-D17_
2. LE SYSTÈME DOIT afficher dès l'ouverture la liste des demandes classées par échéance croissante. _Source : B07-D17, B07-D2_

### Exigence 10 : Livraison, hébergement et intégration

**User story :** En tant que commanditaire, je veux une première version avant le contrôle interne, intégrée à l'existant et hébergée dans l'Union européenne, afin de répondre au contrôle sans achat de produit.

#### Critères d'acceptation

1. LE SYSTÈME DOIT livrer le lot V1 avant le prochain contrôle interne, sans mise en production du 16 novembre au 11 janvier. _Source : B07-D19, CT-07_
2. LE SYSTÈME DOIT être hébergé dans l'Union européenne ; l'hébergement dans le cloud d'Orvanne est retenu par défaut. _Source : CT-08_
3. LE SYSTÈME DOIT être développé comme une solution intégrée au SI existant, sauf décision contraire du comité d'architecture. _Source : B07-D20_

### Exigence 11 : Conformité des données du registre

**User story :** En tant que DPO, je veux que le registre respecte lui-même le RGPD, afin de ne pas créer un nouveau risque.

#### Critères d'acceptation

1. LE SYSTÈME DOIT être soumis à l'avis de la DPO avant tout développement. _Source : CT-01_
2. LE SYSTÈME NE DOIT PAS utiliser de données de production dans les environnements de test et de démonstration sans anonymisation. _Source : CT-04_
3. LE SYSTÈME DOIT journaliser tout accès aux données personnelles du registre et en limiter la lecture à l'équipe DPO. _Source : CT-10, B07-D1_

## Hors périmètre

- Tout nouveau traitement soumis à la DPO avant développement (`B07-D10`) : règle portée par CT-01, applicable à tous les projets, renvoyée vers aucun projet.
- Usage du numéro de mobile (`B07-D11`) : règle portée par CT-02, applicable aux projets utilisant le mobile, renvoyée vers aucun projet.
- Message de service sans offre commerciale (`B07-D12`) : règle portée par CT-03, renvoyée vers aucun projet.
- Conservation de 3 ans des données de prospection (`B07-D13`) : règle portée par CT-05, renvoyée vers aucun projet.
- Purge des historiques de prospection (`B07-D14`) : chantier sans porteur ni échéance, distinct de l'outil de registre (Q31), renvoyé vers aucun projet.
- Photos et pièces jointes (`B07-D15`) : règle portée par CT-06, renvoyée vers aucun projet.
- Données de démonstration et de test (`B07-D16`) : règle portée par CT-04, renvoyée vers aucun projet ; elle s'applique néanmoins à ce projet (exigence 11).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H29 | Le compte à rebours part de la date de réception, en jours calendaires ; les seuils d'alerte (J+15, J+25) et l'échéance après prolongation sont des paramètres. | aucun | oui |
| H31 | La V1 couvre registre, compte à rebours, saisie par le service client, preuve de clôture, export d'accès et tableau de bord, avec actions tracées manuellement ; l'orchestration automatisée est en V2. | aucun | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q30 | Date du prochain contrôle interne ? Le compte à rebours part-il de la réception ou de la vérification d'identité ? Comment traiter le Lac et les sauvegardes lors d'un effacement ? | Hélène Marsac | non (précise les exigences 2, 6 et 10) |
| Q31 | Qui porte la purge des historiques de prospection de plus de 3 ans, et pour quelle échéance ? | Hélène Marsac ; Capucine Lorrain | non (hors périmètre) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non (précise l'exigence 10) |
