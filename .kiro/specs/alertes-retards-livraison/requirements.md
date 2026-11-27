# Exigences : détection des retards de livraison, suivi colis dans Comptoir et information du client

<!-- Projet P01, slug alertes-retards-livraison. Commanditaire : direction des opérations logistiques.
     Parties prenantes : service client, DSI, DPO, marketing. Sources : B01, B02, B05 (B07 via CT-nn). -->

## Introduction

Orvanne découvre aujourd'hui les retards de livraison quand les clients appellent. Depuis septembre, 4 contacts sur 10 au service client portent sur l'état d'une commande (WISMO), sur environ 2 600 contacts par jour et plus de 5 000 pendant les fêtes. Orvanne expédie 35 000 colis par jour en temps normal et environ le double pendant le pic de fin d'année. Lors du pic précédent, le taux de service est resté dégradé pendant trois semaines.

Le projet couvre quatre besoins qui reposent sur les mêmes données de suivi :
1. un tableau de bord des colis en retard pour la logistique ;
2. le suivi des colis dans la fiche commande de Comptoir pour le service client ;
3. une liste quotidienne des commandes en retard pour le service client ;
4. un message proactif au client quand sa commande est en retard.

Les sources se contredisent sur le canal (SMS ou e-mail), le seuil de retard, la validation des messages Premium et la fraîcheur des données. Ces points ne sont pas arbitrés : la spec les traite par des **paramètres** dont les valeurs par défaut sont les hypothèses `H01` à `H06`.

Le gel des mises en production du 16 novembre au 11 janvier (`CT-07`) recouvre le pic. Le projet est donc livré en deux lots. La date du lot 1 dépend de la question bloquante `Q03` (dérogation au gel ou non).
- **Lot 1** (exigences 1 à 3) : outils internes, sans aucun envoi aux clients.
- **Lot 2** (exigences 4 à 8) : suivi dans Comptoir, liste quotidienne et messages aux clients, mise en service au T1 2027, après le 11 janvier.
- L'exigence 9 (non fonctionnelle) s'applique aux deux lots.

Découpage par version : la V1 envoie les messages par e-mail et sans validation Premium active ; le SMS (`B01-D5`) et la validation Premium (`B02-D8`) sont livrés comme options désactivées par défaut, activables en V2 (`H01`, `H03`).

## Glossaire

- **Colis** : unité expédiée et suivie par un transporteur ; une commande peut comporter plusieurs colis.
- **Date promise** : date de livraison affichée au client sur Vitrine.
- **Statut transporteur** : événement de suivi d'un colis reçu via Passerelle.
- **Niveau de retard** : état calculé d'un colis non livré : `à l'heure`, `à surveiller` ou `en retard` (exigence 2).
- **Retard « rouge »** : colis au niveau `en retard` (définition provisoire, `H02`, `Q02`).
- **Dossier ouvert** : demande client en cours de traitement dans Comptoir sur une commande (définition à préciser).
- **Client Premium** : catégorie de clients citée par le service client, non définie (lien avec Orvanne+ à confirmer, `Q04`).
- **Message de retard** : message de service informant un client du retard de sa commande ; il ne contient aucune offre commerciale (`CT-03`).
- **WISMO** : contact client demandant où en est sa commande.
- **E1, E2, E3** : les trois entrepôts d'Orvanne.

## Exigences

### Exigence 1 : consolidation des statuts de suivi des colis (lot 1)

**User story :** En tant que responsable transport, je veux que les statuts des trois transporteurs soient consolidés à partir de Passerelle, afin de ne plus croiser à la main les extractions de Hangar et les fichiers des transporteurs.

#### Critères d'acceptation

1. QUAND Passerelle fournit un statut transporteur pour un colis, LE SYSTÈME DOIT l'enregistrer dans l'historique de ce colis avec son horodatage d'origine. _Source : B01-D10, B02-D1_
2. LE SYSTÈME DOIT rattacher chaque colis à sa commande, à son transporteur, à son entrepôt d'expédition (E1, E2 ou E3), à sa région de livraison et à sa date promise. _Source : B01-D3, B02-D6_
3. LE SYSTÈME DOIT traiter les statuts des trois transporteurs d'Orvanne. _Source : B02-D3, B01-D10_
4. LE SYSTÈME DOIT rendre visible un statut au plus tard 15 minutes après son arrivée dans Passerelle ; cette valeur est un paramètre, à ajuster après mesure de la fraîcheur réelle des statuts. _Source : H04, B01-D2_
5. SI un même statut est reçu plusieurs fois pour un colis, ALORS LE SYSTÈME DOIT ne l'enregistrer qu'une fois. _Source : B01-D10_
6. SI aucun statut n'a été reçu d'un transporteur depuis plus de 24 heures, ALORS LE SYSTÈME DOIT signaler l'interruption du flux sur le tableau de bord et à la supervision ; ce délai est un paramètre. _Source : H04, B01-D2_

### Exigence 2 : détection des retards (lot 1)

**User story :** En tant que responsable transport, je veux que le système calcule le niveau de retard de chaque colis à partir de la date promise, afin d'agir avant que le client appelle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT évaluer le retard par colis et calculer, pour chaque colis non livré, un niveau `à l'heure`, `à surveiller` ou `en retard`. _Source : H05, H02, B01-D3_
2. QUAND la date promise affichée sur Vitrine est dépassée et que le colis n'est pas livré, LE SYSTÈME DOIT passer le colis au niveau `à surveiller` à 6 h 00 le lendemain (J+1 matin). _Source : B02-D6, H02_
3. QUAND un colis n'est pas livré 48 heures après la date promise, LE SYSTÈME DOIT passer le colis au niveau `en retard`. _Source : B01-D7, H02_
4. QUAND un colis reçoit le statut « livré », LE SYSTÈME DOIT le sortir du suivi des retards. _Source : B01-D1, B02-D1_
5. LE SYSTÈME DOIT permettre à un administrateur métier de modifier les deux seuils de passage de niveau, et le niveau qui déclenche l'alerte client (`en retard` par défaut), sans nouvelle mise en production. _Source : H02_
6. LE SYSTÈME DOIT recalculer les niveaux de tous les colis non livrés chaque jour, avant l'heure de production de la liste quotidienne. _Source : B02-D6, B02-D15_
7. QUAND la date promise d'un colis est modifiée après la commande, LE SYSTÈME DOIT utiliser la date promise la plus récente affichée sur Vitrine. _Source : B02-D6, H02_
8. SI la date promise d'un colis est absente, ALORS LE SYSTÈME DOIT exclure ce colis du calcul et le compter à part (« date promise inconnue »). _Source : B01-D7, B02-D6_

### Exigence 3 : tableau de bord des retards (lot 1)

**User story :** En tant que membre des équipes transport ou responsable d'entrepôt, je veux un tableau de bord des colis en retard, afin de repérer les dérives par transporteur, par entrepôt et par région, et d'agir dessus.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher le nombre de colis `à surveiller` et `en retard`, ventilé par transporteur, par entrepôt (E1, E2, E3) et par région. _Source : B01-D1, B01-D3_
2. QUAND un utilisateur sélectionne une ventilation, LE SYSTÈME DOIT afficher la liste des colis concernés, puis le détail d'un colis : commande, historique des statuts, date promise et nouvelle date de livraison communiquée par le transporteur, si elle existe. _Source : B01-D3, B01-D6_
3. LE SYSTÈME DOIT afficher les colis `en retard` en rouge et les colis `à surveiller` en orange, et placer les colis `en retard` en tête des listes, par ancienneté de retard décroissante. _Source : B01-D4, H02_
4. LE SYSTÈME DOIT rafraîchir le tableau de bord à chaque arrivée de statuts dans Passerelle et afficher la date et l'heure de la dernière mise à jour. _Source : B01-D2, H04_
5. LE SYSTÈME DOIT réserver l'accès au tableau de bord aux équipes transport, aux responsables d'entrepôt et au service client. _Source : B01-D1, CT-01_
6. LE SYSTÈME DOIT permettre l'export de la liste affichée au format CSV. _Source : B01-D1_

### Exigence 4 : suivi du colis dans la fiche commande de Comptoir (lot 2)

**User story :** En tant que conseiller du service client, je veux voir le suivi des colis dans la fiche commande de Comptoir, afin de répondre au client sans en sortir.

#### Critères d'acceptation

1. QUAND un conseiller ouvre une fiche commande dans Comptoir, LE SYSTÈME DOIT afficher, pour chaque colis, le dernier statut, son horodatage, le niveau de retard et l'historique des statuts, sans que le conseiller quitte Comptoir. _Source : B02-D1_
2. LE SYSTÈME DOIT afficher le suivi en moins de 2 secondes pour 95 % des ouvertures de fiche, y compris pendant le pic (environ 70 000 colis expédiés par jour). _Source : B02-D2, B01-D2_
3. LE SYSTÈME DOIT afficher le suivi pour les colis des trois transporteurs. _Source : B02-D3_
4. SI le suivi ne répond pas dans le délai, ALORS LE SYSTÈME DOIT afficher la fiche commande sans le suivi, avec un message indiquant que le suivi est momentanément indisponible. _Source : B02-D2, B02-D1_

### Exigence 5 : liste quotidienne des commandes en retard pour le service client (lot 2)

**User story :** En tant que responsable du service client, je veux recevoir chaque matin la liste des commandes en retard, afin d'anticiper les appels et de savoir quels messages vont partir.

#### Critères d'acceptation

1. LE SYSTÈME DOIT mettre à disposition du service client, chaque matin et avant le premier envoi de message de la journée, la liste des commandes ayant au moins un colis `à surveiller` ou `en retard`. L'heure de mise à disposition est un paramètre (7 h 00 par défaut). _Source : B02-D15, H03, H02_
2. LE SYSTÈME DOIT indiquer pour chaque commande de la liste : le niveau de retard, le transporteur, la présence d'un dossier ouvert, le statut Premium si la catégorie est définie, et l'état du message (programmé, en attente de validation, envoyé, non envoyé avec motif). _Source : B02-D15, B02-D14, B02-D7, H03_
3. LE SYSTÈME DOIT rendre la liste consultable dans Comptoir et exportable au format CSV, sans tableau de bord. _Source : B02-D15_
4. LE SYSTÈME DOIT inclure dans la liste les commandes ayant un dossier ouvert, en les signalant comme non concernées par un envoi. _Source : B02-D15, B02-D7, H03_

### Exigence 6 : message de retard au client (lot 2)

**User story :** En tant que client, je veux être prévenu quand ma commande est en retard et savoir quand elle arrivera, afin de ne pas avoir à contacter le service client.

#### Critères d'acceptation

1. QUAND un colis d'une commande atteint le niveau qui déclenche l'alerte, LE SYSTÈME DOIT envoyer un message de retard au client sans intervention manuelle, sauf dans les cas de l'exigence 7. _Source : B01-D5, B01-D8, B02-D4, H02, H03_
2. LE SYSTÈME DOIT envoyer le message par le canal configuré ; en V1, ce canal est l'e-mail pour tous les clients concernés. _Source : B02-D5, H01_
3. OÙ le canal SMS est activé, LE SYSTÈME DOIT envoyer le message par SMS aux clients dont le numéro de mobile est connu et par e-mail aux autres. _Source : B01-D5, H01, CT-02_
4. QUAND une nouvelle date de livraison est connue, LE SYSTÈME DOIT l'indiquer dans le message. _Source : B01-D6_
5. SI aucune nouvelle date de livraison n'est connue, ALORS LE SYSTÈME DOIT envoyer le message sans date estimée, avec le modèle prévu à cet effet. _Source : B01-D6, B02-D4_
6. LE SYSTÈME DOIT envoyer au plus un message par commande et par niveau de retard, en listant tous les colis en retard de la commande. _Source : H05, B02-D4_
7. LE SYSTÈME DOIT envoyer les messages dans une plage horaire paramétrable (8 h 00 à 20 h 00 par défaut). _Source : B02-D4, H03_
8. QUAND un message de retard est envoyé, LE SYSTÈME DOIT l'enregistrer dans l'historique de la commande consultable dans Comptoir : date, canal, modèle et contenu. _Source : B02-D14, H03, CT-10_
9. LE SYSTÈME NE DOIT PAS inclure de code promotionnel ni d'offre commerciale dans le message de retard. _Source : H06, CT-03, B02-D10_

### Exigence 7 : règles de non-envoi, information du service client et validation

**User story :** En tant que responsable du service client, je veux qu'aucun message ne contredise un échange en cours et que le service client sache ce qui part, afin que le client reçoive un discours unique.

#### Critères d'acceptation

1. SI un dossier est ouvert dans Comptoir sur la commande, ALORS LE SYSTÈME DOIT ne pas envoyer de message de retard et en indiquer le motif dans la liste quotidienne. _Source : B02-D7, H03_
2. LE SYSTÈME DOIT vérifier l'absence de dossier ouvert au moment de l'envoi, et non au moment du calcul du retard. _Source : B02-D7_
3. SI Comptoir ne répond pas lors de la vérification du dossier ouvert, ALORS LE SYSTÈME DOIT reporter l'envoi et ne jamais envoyer sans cette vérification. _Source : B02-D7, B02-D14_
4. LE SYSTÈME DOIT informer le service client de tout message avant son envoi, par la liste quotidienne (exigence 5) ; aucun message ne part sans figurer dans la liste du jour. _Source : B02-D14, B01-D8, H03_
5. OÙ la validation Premium est activée, LE SYSTÈME DOIT placer le message d'un client Premium dans une file de validation de Comptoir au lieu de l'envoyer. _Source : B02-D8, H03_
6. QUAND un conseiller valide un message de la file, LE SYSTÈME DOIT l'envoyer après avoir de nouveau appliqué le critère 7.1 ; QUAND il le rejette, LE SYSTÈME DOIT l'abandonner et enregistrer le motif. _Source : B02-D8, B02-D7_
7. SI un message de la file n'est pas traité dans le délai de validation paramétré, ALORS LE SYSTÈME DOIT le signaler au responsable du service client ; le message n'est pas envoyé par défaut, et ce comportement est paramétrable. _Source : B02-D8, H03_
8. QUAND la commande est livrée avant l'envoi d'un message programmé ou en attente de validation, LE SYSTÈME DOIT annuler ce message. _Source : B02-D4, B01-D7_
9. PENDANT QUE la catégorie Premium n'est pas définie, LE SYSTÈME DOIT laisser la validation Premium désactivée. _Source : H03, B02-D8_

### Exigence 8 : contenu et modèles de message

**User story :** En tant que membre de l'équipe du service client, je veux modifier moi-même le texte des messages, afin d'ajuster la communication sans passer par la DSI.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au service client de créer, modifier, prévisualiser et activer les modèles de message, par canal et par cas (avec ou sans nouvelle date), sans intervention de la DSI. _Source : B02-D9_
2. LE SYSTÈME DOIT limiter les variables des modèles aux informations de service : prénom, numéro de commande, transporteur, date promise, nouvelle date de livraison, lien de suivi. _Source : B02-D10, CT-03_
3. SI un modèle contient un code promotionnel, un lien vers une offre ou un contenu commercial, ALORS LE SYSTÈME DOIT refuser son activation. _Source : CT-03, H06_
4. LE SYSTÈME DOIT conserver l'historique des versions de chaque modèle avec son auteur et sa date d'activation. _Source : B02-D9, CT-10_
5. OÙ le canal SMS est activé, LE SYSTÈME DOIT limiter un SMS à 160 caractères une fois les variables remplacées. _Source : B01-D5, H01_

### Exigence 9 : exigences non fonctionnelles et conformité

**User story :** En tant que DSI, je veux une solution dimensionnée pour le pic, hébergée chez Orvanne et conforme au RGPD, afin qu'elle tienne quand elle est la plus utile.

#### Critères d'acceptation

1. LE SYSTÈME DOIT traiter les statuts de 70 000 colis expédiés par jour (pic, soit environ le double des 35 000 colis par jour en temps normal) sans dépasser le délai du critère 1.4. _Source : B01-D2, B01-D10_
2. LE SYSTÈME DOIT être hébergé dans le cloud d'Orvanne, dans l'Union européenne. _Source : B01-D9, CT-08_
3. LE SYSTÈME DOIT bloquer l'activation du canal SMS tant que l'avis favorable de la DPO sur l'usage du numéro de mobile n'est pas enregistré. _Source : CT-02, CT-01_
4. LE SYSTÈME DOIT conserver l'historique des statuts et des messages pendant une durée paramétrable fixée avec la DPO, puis les supprimer. _Source : CT-01_
5. LE SYSTÈME DOIT journaliser les accès au tableau de bord, les validations et rejets de messages, et les modifications de modèles et de paramètres, avec leur auteur et leur date. _Source : CT-10, CT-01_
6. LE SYSTÈME DOIT produire chaque jour le nombre de messages de retard envoyés, non envoyés (dossier ouvert), validés, rejetés et expirés, afin de mesurer l'évolution du taux de contacts WISMO. _Source : B02-D11_
7. LE SYSTÈME DOIT utiliser des données synthétiques ou anonymisées pour tous les tests et démonstrations. _Source : CT-04_
8. LE SYSTÈME NE DOIT PAS être mis en production entre le 16 novembre et le 11 janvier. _Source : CT-07, B02-D12_

## Hors périmètre

- Code promo dans les messages de retard (`B05-D7`) : interdit dans un message de service par `CT-03` (`B07-D12`, `B02-D10`). Une offre commerciale relève d'un message marketing distinct, soumis au consentement (`H06`). Aucun projet ne la reprend pour l'instant (`Q07`).
- Planning demandé à la DSI pour la fin de la semaine suivant l'e-mail (`B01-D11`) : livrable de gestion de projet, pas une exigence du système. Le découpage en lots de `tasks.md` sert de base à ce planning.
- Mise en service au premier trimestre (`B02-D13`) : échéance reprise dans le découpage en lots (introduction et `tasks.md`), pas comme exigence du système. Le gel (`B02-D12`) est repris par le critère 9.8.
- Mesure de la baisse de 30 % des contacts WISMO (`B02-D11`) : elle relève des outils du service client ; le projet fournit les données d'envoi (critère 9.6). La base de référence reste à définir (`Q39`).
- Tableau de bord pour le service client : le service client demande une liste (`B02-D15`), mais il a accès au tableau de bord (critère 3.5).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H01 | Le canal est un paramètre. La V1 envoie un e-mail à tous les clients concernés ; le SMS n'est activé qu'après analyse de la DPO (CT-02) et accord budgétaire, pour les clients dont le mobile est connu. | C01 | oui |
| H02 | Le seuil de retard est un paramètre calculé à partir de la date promise : `à surveiller` à J+1 matin (liste et tableau de bord), `en retard` à J+2 soit 48 h (alerte client). La signification des « rouges » reste à définir. | C02 | oui |
| H03 | L'alerte part automatiquement. Le service client reçoit chaque matin la liste des commandes concernées. Aucune alerte si un dossier est ouvert. La validation Premium est une option paramétrable, désactivée tant que la catégorie n'est pas définie. | C04 | oui |
| H04 | Le tableau de bord est rafraîchi à chaque arrivée de statuts dans Passerelle et affiche l'heure de dernière mise à jour ; la fréquence cible est fixée après mesure de la fraîcheur des statuts. | C05 | oui |
| H05 | Le retard est évalué par colis. Le client reçoit au plus un message par commande, qui liste les colis en retard. | C06 | oui |
| H06 | L'alerte de retard ne contient ni code promo ni offre commerciale ; une offre relève d'un message marketing distinct, hors P01. | C07 | oui |

Valeurs par défaut proposées pour des paramètres que les sources ne donnent pas (15 minutes, 24 heures, 6 h 00, 7 h 00, plage 8 h à 20 h) : ce sont des paramètres modifiables sans mise en production, à valider avec la logistique et le service client.

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q01 | Quel canal pour l'alerte de retard : e-mail, SMS (budget, avis DPO sur l'usage du mobile), ou les deux selon la disponibilité du mobile ? | Solène Garrigue, Yanis Mercadier ; avis d'Hélène Marsac | non |
| Q02 | À partir de quand une commande est-elle « en retard » : J+1 matin ou 48 h après la date promise ? Que signifient les « rouges » ? | Solène Garrigue, Yanis Mercadier | non |
| Q03 | Une dérogation au gel du 16/11 au 11/01 est-elle possible pour un tableau de bord interne sans envoi aux clients ? Sinon, confirmation d'une mise en service au T1 2027. | Bertrand Lacassagne (DSI) | oui (date du lot 1, exigences 1 à 3) |
| Q04 | Qu'est-ce qu'un client Premium (lien avec Orvanne+) ? Quel délai de validation, et que se passe-t-il sans validation ? | Yanis Mercadier ; Capucine Lorrain | non (exigence 7.5 à 7.7 désactivée par défaut) |
| Q05 | À quelle fréquence Passerelle reçoit-elle les statuts des 3 transporteurs ? Quel rafraîchissement du tableau de bord est acceptable ? | Solène Garrigue ; équipe Passerelle (DSI) | non |
| Q06 | Pour une commande à plusieurs colis, un message par colis ou un seul par commande ? | Solène Garrigue, Yanis Mercadier | non |
| Q07 | Confirmez-vous l'abandon du code promo dans les messages de retard ? Souhaitez-vous un message commercial distinct soumis au consentement ? | Capucine Lorrain ; Hélène Marsac | non |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non |
| Q36 | Quand la DPO peut-elle examiner le traitement (CT-01) et exige-t-il une analyse d'impact ? | Hélène Marsac | non |
| Q39 | Quelle base de référence et quelle période pour la baisse de 30 % des contacts WISMO ? | Yanis Mercadier ; direction de l'expérience client | non |
