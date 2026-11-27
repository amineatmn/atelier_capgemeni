# Exigences : détection des retards de livraison, information du client et pilotage

<!-- Projet P01, slug alertes-retards-livraison. Commanditaire : direction des opérations logistiques.
     Parties prenantes : service client, DSI, DPO, marketing. Sources : B01, B02, B05, B07.
     Spec étalon rédigée à la main (élève C). Les IDs B02-Dn sont provisoires tant que work/fiches/B02.json n'existe pas :
     voir templates/exemple-p01/ids-provisoires.md. -->

## Introduction

Orvanne découvre aujourd'hui les retards de livraison quand les clients appellent. Lors du pic de fin d'année précédent, le taux de service est resté dégradé pendant trois semaines. Le suivi se fait à la main, à partir d'extractions de Hangar et des fichiers envoyés chaque matin par les transporteurs.

Depuis septembre, 4 contacts sur 10 au service client portent sur l'état d'une commande (WISMO), sur environ 2 600 contacts par jour, et plus de 5 000 pendant les fêtes. Orvanne expédie environ 35 000 colis par jour, et à peu près le double pendant le pic.

Le projet couvre quatre besoins qui reposent sur les mêmes données de suivi :
1. un tableau de bord des retards pour la logistique ;
2. le suivi des colis dans Comptoir pour le service client ;
3. une liste quotidienne des commandes en retard pour le service client ;
4. un message proactif au client quand sa commande est en retard.

Le projet est livré en deux lots, pour tenir compte du gel des mises en production du 16 novembre au 11 janvier (`CT-07`) :
- **Lot 1** (exigences 1 à 3) : outils internes, sans aucun envoi aux clients.
- **Lot 2** (exigences 4 à 9) : suivi dans Comptoir et information des clients, au premier trimestre 2027.

## Glossaire

- **Colis** : unité expédiée et suivie par un transporteur ; une commande peut comporter plusieurs colis.
- **Date promise** : date de livraison affichée au client sur Vitrine au moment de la commande.
- **Statut transporteur** : événement de suivi d'un colis (pris en charge, en transit, en livraison, livré, incident…) reçu via Passerelle.
- **Niveau de retard** : état calculé d'un colis non livré par rapport à sa date promise : `à l'heure`, `à surveiller` ou `en retard` (voir exigence 2).
- **Dossier ouvert** : demande client en cours de traitement dans Comptoir sur une commande.
- **Client Premium** : catégorie de client définie par le service client (définition à confirmer, `Q05`).
- **Message de retard** : message de service informant un client du retard de sa commande ; il ne contient aucune offre commerciale.
- **WISMO** : contact client demandant où en est sa commande.

## Exigences

### Exigence 1 : consolidation des statuts de suivi des colis

**User story :** En tant que responsable transport, je veux que les statuts des trois transporteurs soient consolidés automatiquement, afin de ne plus croiser à la main les extractions de Hangar et les fichiers des transporteurs.

#### Critères d'acceptation

1. QUAND Passerelle reçoit un statut transporteur pour un colis, LE SYSTÈME DOIT l'enregistrer dans l'historique de ce colis, avec son horodatage d'origine. _Source : B01-D10_
2. LE SYSTÈME DOIT rattacher chaque colis à sa commande, à son transporteur, à son entrepôt d'expédition (E1, E2 ou E3), à sa région de livraison et à sa date promise. _Source : B01-D3, B02-D5, H09_
3. LE SYSTÈME DOIT traiter les statuts des trois transporteurs d'Orvanne. _Source : B02-D10_
4. LE SYSTÈME DOIT rendre visible un statut au plus tard 15 minutes après sa réception par Passerelle. _Source : B01-D2, H05_
5. SI un même statut est reçu plusieurs fois pour un colis, ALORS LE SYSTÈME DOIT ne l'enregistrer qu'une fois. _Source : B01-D10_
6. SI aucun statut n'a été reçu d'un transporteur depuis plus de 4 heures, ALORS LE SYSTÈME DOIT signaler l'interruption du flux sur le tableau de bord. _Source : B01-D2, H05_

### Exigence 2 : détection des retards

**User story :** En tant que responsable transport, je veux que le système calcule le niveau de retard de chaque colis, afin d'agir avant que le client appelle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer, pour chaque colis non livré, un niveau de retard `à l'heure`, `à surveiller` ou `en retard`. _Source : B01-D7, B02-D5, H02_
2. QUAND la date promise d'un colis non livré est dépassée, LE SYSTÈME DOIT passer le colis au niveau `à surveiller`. _Source : B02-D5, H02_
3. QUAND un colis n'est pas livré 48 heures après la fin de sa date promise, LE SYSTÈME DOIT passer le colis au niveau `en retard`. _Source : B01-D7, H02_
4. QUAND un colis reçoit le statut « livré », LE SYSTÈME DOIT le sortir du suivi des retards. _Source : B01-D1_
5. LE SYSTÈME DOIT permettre à un administrateur métier de modifier les deux seuils de passage de niveau sans nouvelle mise en production. _Source : H02_
6. LE SYSTÈME DOIT recalculer les niveaux de tous les colis non livrés au plus tard à 6 h 00 chaque jour. _Source : B02-D5, B02-D14_

### Exigence 3 : tableau de bord des retards (lot 1)

**User story :** En tant que membre des équipes transport ou responsable d'entrepôt, je veux un tableau de bord des colis en retard, afin de repérer les dérives par transporteur, par entrepôt et par région, et d'agir dessus.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher le nombre de colis `à surveiller` et `en retard`, ventilé par transporteur, par entrepôt (E1, E2, E3) et par région. _Source : B01-D1, B01-D3_
2. QUAND un utilisateur sélectionne une ventilation, LE SYSTÈME DOIT afficher la liste des colis concernés, puis le détail d'un colis : commande, historique des statuts, date promise et nouvelle date estimée. _Source : B01-D3_
3. LE SYSTÈME DOIT afficher les colis `en retard` en rouge, les colis `à surveiller` en orange, et trier les listes en plaçant les colis `en retard` en premier, par ancienneté du retard décroissante. _Source : B01-D4, H06_
4. LE SYSTÈME DOIT afficher la date et l'heure de la dernière mise à jour des données. _Source : B01-D2, H05_
5. LE SYSTÈME DOIT réserver l'accès au tableau de bord aux équipes transport, aux responsables d'entrepôt et au service client. _Source : B01-D1, CT-01_
6. LE SYSTÈME DOIT permettre l'export de la liste affichée au format CSV. _Source : B01-D1_

### Exigence 4 : suivi du colis dans la fiche commande de Comptoir (lot 2)

**User story :** En tant que conseiller du service client, je veux voir le suivi des colis dans la fiche commande de Comptoir, afin de répondre au client sans ouvrir le site du transporteur.

#### Critères d'acceptation

1. QUAND un conseiller ouvre une fiche commande dans Comptoir, LE SYSTÈME DOIT afficher, pour chaque colis de la commande, le dernier statut, son horodatage, le niveau de retard et l'historique complet des statuts. _Source : B02-D1_
2. LE SYSTÈME DOIT afficher le suivi en moins de 2 secondes pour 95 % des ouvertures de fiche, y compris pendant le pic (environ 70 000 colis expédiés par jour). _Source : B02-D2, B01-D2_
3. LE SYSTÈME DOIT afficher le suivi pour les colis des trois transporteurs. _Source : B02-D10_
4. SI le service de suivi ne répond pas dans le délai, ALORS LE SYSTÈME DOIT afficher la fiche commande sans le suivi, avec un message indiquant que le suivi est momentanément indisponible. _Source : B02-D2_

### Exigence 5 : liste quotidienne des commandes en retard pour le service client (lot 2)

**User story :** En tant que responsable du service client, je veux chaque matin la liste des commandes concernées par un retard, afin d'anticiper les appels.

#### Critères d'acceptation

1. LE SYSTÈME DOIT mettre à disposition du service client, chaque jour à 7 h 00, la liste des commandes ayant au moins un colis `à surveiller` ou `en retard`. _Source : B02-D14, H02_
2. LE SYSTÈME DOIT indiquer pour chaque commande de la liste : le niveau de retard, le transporteur, la présence d'un dossier ouvert dans Comptoir, le statut client Premium, et si un message de retard a été envoyé, programmé ou mis en attente de validation. _Source : B02-D14, B02-D13, B01-D12, H04_
3. LE SYSTÈME DOIT rendre la liste consultable dans Comptoir et exportable au format CSV. _Source : B02-D14_

### Exigence 6 : message de retard au client (lot 2)

**User story :** En tant que client, je veux être prévenu quand ma commande est en retard et savoir quand elle arrivera, afin de ne pas avoir à contacter le service client.

#### Critères d'acceptation

1. QUAND une commande passe au niveau de retard qui déclenche l'alerte, LE SYSTÈME DOIT envoyer un message de retard au client sans intervention manuelle, sauf dans les cas de l'exigence 7. _Source : B01-D5, B01-D8, B02-D3, H02_
2. LE SYSTÈME DOIT envoyer le message par le canal configuré ; en V1, ce canal est l'e-mail. _Source : B02-D4, H01, CT-02_
3. OÙ le canal SMS est activé, LE SYSTÈME DOIT envoyer le message par SMS aux clients dont le numéro de mobile est connu, et par e-mail aux autres. _Source : B01-D5, H01, CT-02_
4. QUAND le transporteur a communiqué une nouvelle date de livraison, LE SYSTÈME DOIT l'indiquer dans le message. _Source : B01-D6, H07_
5. SI aucune nouvelle date de livraison n'est connue, ALORS LE SYSTÈME DOIT envoyer le message sans date estimée, avec le modèle prévu à cet effet. _Source : B01-D6, H07_
6. LE SYSTÈME DOIT envoyer au plus un message par commande et par niveau de retard, en regroupant tous les colis concernés de la commande. _Source : B02-D3, H08_
7. LE SYSTÈME DOIT envoyer les messages entre 8 h 00 et 20 h 00. _Source : B02-D3, H08_
8. QUAND un message de retard est envoyé, LE SYSTÈME DOIT l'enregistrer dans l'historique de la commande consultable dans Comptoir : date, canal, modèle utilisé, contenu envoyé. _Source : B02-D13, B01-D12, H04_

### Exigence 7 : règles de non-envoi et validation

**User story :** En tant que responsable du service client, je veux qu'aucun message ne contredise un échange en cours et que les messages aux clients Premium soient validés, afin que le client reçoive un discours unique.

#### Critères d'acceptation

1. SI un dossier est ouvert dans Comptoir sur la commande, ALORS LE SYSTÈME DOIT ne pas envoyer de message de retard et doit l'indiquer dans la liste quotidienne. _Source : B02-D6_
2. LE SYSTÈME DOIT vérifier l'absence de dossier ouvert au moment de l'envoi, et non au moment du calcul du retard. _Source : B02-D6_
3. SI le client est Premium, ALORS LE SYSTÈME DOIT placer le message dans une file de validation de Comptoir au lieu de l'envoyer. _Source : B02-D7, H03_
4. QUAND un conseiller valide un message de la file, LE SYSTÈME DOIT l'envoyer, après avoir de nouveau appliqué le critère 7.1 ; QUAND il le rejette, LE SYSTÈME DOIT l'abandonner et enregistrer le motif. _Source : B02-D7, B02-D6, H03_
5. SI un message de la file n'a pas été traité au bout du délai de validation paramétré, ALORS LE SYSTÈME DOIT le signaler au responsable du service client et ne pas l'envoyer. _Source : B02-D7, H03_
6. QUAND la commande est livrée avant l'envoi d'un message programmé ou en attente de validation, LE SYSTÈME DOIT annuler ce message. _Source : B02-D3_

### Exigence 8 : contenu et modèles de message

**User story :** En tant que membre de l'équipe du service client, je veux modifier moi-même le texte des messages, afin d'ajuster la communication sans passer par la DSI.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au service client de créer, modifier, prévisualiser et activer les modèles de message, par canal et par cas (avec ou sans nouvelle date), sans intervention de la DSI. _Source : B02-D8_
2. LE SYSTÈME DOIT proposer dans les modèles uniquement des variables de service : prénom, numéro de commande, transporteur, date promise, nouvelle date estimée, lien de suivi. _Source : B02-D9, CT-03_
3. SI un modèle contient un code promotionnel, un lien vers une offre ou un contenu commercial, ALORS LE SYSTÈME DOIT refuser son activation. _Source : B02-D9, CT-03_
4. LE SYSTÈME DOIT conserver l'historique des versions de chaque modèle, avec leur auteur et leur date d'activation. _Source : B02-D8, B02-D13_
5. LE SYSTÈME DOIT limiter un SMS à 160 caractères une fois les variables remplacées. _Source : B01-D5, H01_

### Exigence 9 : exigences non fonctionnelles

**User story :** En tant que DSI, je veux une solution dimensionnée pour le pic, hébergée chez Orvanne et conforme au RGPD, afin qu'elle tienne quand elle est la plus utile.

#### Critères d'acceptation

1. LE SYSTÈME DOIT traiter les statuts de 70 000 colis expédiés par jour, soit le volume du pic d'après B01 (35 000 colis par jour en temps normal, à peu près le double pendant le pic), sans dépasser le délai du critère 1.4. _Source : B01-D2, B01-D10_
2. LE SYSTÈME DOIT être hébergé dans le cloud d'Orvanne, dans l'Union européenne. _Source : B01-D9, CT-08_
3. LE SYSTÈME DOIT utiliser le numéro de mobile du client uniquement après l'avis favorable de la DPO sur cet usage, l'activation du canal SMS étant bloquée tant que cet avis n'est pas enregistré. _Source : CT-02, CT-01_
4. LE SYSTÈME DOIT conserver les historiques de statuts et de messages pendant une durée paramétrable, fixée avec la DPO, puis les supprimer. _Source : CT-01, H10_
5. LE SYSTÈME DOIT journaliser les accès au tableau de bord, les validations et rejets de messages, et les modifications de modèles et de paramètres. _Source : CT-01, B02-D13_
6. LE SYSTÈME DOIT produire chaque jour le nombre de messages de retard envoyés, non envoyés à cause d'un dossier ouvert, validés, rejetés et expirés, afin de mesurer l'effet sur le taux de contacts WISMO. _Source : B02-D11_

## Hors périmètre

- Code promotionnel dans les messages de retard (`B05-D9`) : interdit dans un message de service par `CT-03`. Aucun projet ne le reprend. Une demande de relance commerciale relève du projet P04 et d'une base légale distincte.
- Tableau de bord pour le service client (`B02-D14`) : le service client a demandé une liste, pas un tableau de bord. Il a cependant accès au tableau de bord (critère 3.5).
- Mesure du taux de contacts WISMO : elle relève des outils du service client. Le projet fournit les données d'envoi nécessaires (critère 9.6).
- Planning demandé à la DSI pour la fin de la semaine suivante (`B01-D11`) : livrable de gestion de projet, pas une exigence du système. Le découpage en lots de `tasks.md` sert de base à ce planning.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H01 | Le canal est paramétrable. La V1 envoie des e-mails ; le SMS est activable après avis de la DPO et validation du budget. | C01 | oui |
| H02 | Deux seuils paramétrables : `à surveiller` dès que la date promise est dépassée (J+1, liste du service client et tableau de bord) et `en retard` à 48 h (alerte client, rouge). Le niveau qui déclenche l'alerte client est lui aussi paramétrable, `en retard` par défaut. | C02 | oui |
| H03 | Seuls les messages aux clients Premium passent par une validation. Sans validation dans le délai paramétré, le message n'est pas envoyé. | C04 | oui |
| H04 | Le service client est informé de chaque message par la liste quotidienne et par l'historique de la commande dans Comptoir. | C05 | oui |
| H05 | « Temps réel » signifie un statut visible au plus tard 15 minutes après sa réception par Passerelle. | — | oui |
| H06 | « Rouge » désigne les colis `en retard` ; les colis `à surveiller` sont en orange. | — | oui |
| H07 | La nouvelle date de livraison est celle fournie par le transporteur ; Orvanne ne calcule pas de date. | — | oui |
| H08 | Un message par commande et par niveau, envoyé entre 8 h et 20 h. | — | oui |
| H09 | La région de livraison est le département, déduit du code postal de livraison. | — | oui |
| H10 | La durée de conservation des historiques est un paramètre ; la valeur sera fixée avec la DPO. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q01 | Quel canal pour l'alerte de retard : SMS (budget, avis DPO), e-mail, ou les deux selon la disponibilité du mobile ? | Solène Garrigue, Yanis Mercadier, Hélène Marsac | non |
| Q02 | À partir de quand une commande est-elle « en retard » pour le client : J+1 ou J+2 après la date promise ? | Solène Garrigue, Yanis Mercadier | non |
| Q03 | Le lot 1 (tableau de bord interne, sans envoi aux clients) peut-il bénéficier d'une dérogation au gel du 16/11 ? Sinon, à quelle date le pic se termine-t-il ? | Bertrand Lacassagne (DSI) | oui (planning du lot 1) |
| Q04 | Quel est le délai de validation des messages Premium, et faut-il envoyer le message ou l'abandonner à son expiration ? | Yanis Mercadier | non |
| Q05 | Comment identifie-t-on un client Premium, et dans quel système ? Est-ce la même population que les membres Orvanne+ ? | Yanis Mercadier | oui (exigence 7) |
| Q06 | Passerelle reçoit-elle les statuts des trois transporteurs en continu, ou une partie arrive-t-elle seulement par les fichiers du matin ? | Équipe Passerelle (DSI) | oui (exigence 1) |
| Q07 | Quel service d'envoi utiliser pour les e-mails transactionnels ? L'outil d'e-mailing marketing est-il adapté à des messages de service ? | DSI, Hélène Marsac | non |
| Q08 | D'où vient la date promise de chaque colis (Vitrine, système de gestion des commandes) et est-elle disponible dans Passerelle ? | DSI | oui (exigence 2) |
| Q09 | Comptoir permet-il d'intégrer un encart, une file de validation et une liste issus d'un autre système (composant, API, lien contextuel) ? | Équipe Comptoir (DSI) | oui (exigences 4, 5 et 7) |
