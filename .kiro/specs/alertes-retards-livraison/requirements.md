# Exigences : détection des retards de livraison, suivi colis dans Comptoir et information du client

<!-- Projet P01, slug alertes-retards-livraison. Commanditaire : direction des opérations logistiques.
     Parties prenantes : service client, DSI, direction juridique et conformité (DPO), marketing.
     Sources : B01, B02, B05 (demande exclue), B07 (contraintes CT-01 à CT-04). Identifiants : work/fiches/ et work/analyse.json. -->

## Introduction

Orvanne découvre aujourd'hui les retards de livraison quand les clients appellent. Lors du pic de l'an dernier, le taux de service est resté dégradé pendant trois semaines. Le suivi se fait à la main, à partir d'extractions de Hangar et des fichiers que les transporteurs envoient chaque matin. Orvanne expédie environ 35 000 colis par jour en temps normal, et à peu près le double pendant le pic (B01).

Le service client reçoit environ 2 600 contacts par jour, et plus de 5 000 pendant les fêtes. Depuis septembre, 4 contacts sur 10 portent sur l'état d'une commande (WISMO). L'objectif est de baisser ce taux de 30 % (B02).

Le projet couvre quatre besoins qui reposent sur les mêmes données de suivi :
1. un tableau de bord des retards pour les équipes transport et les responsables d'entrepôt ;
2. le suivi des colis dans la fiche commande de Comptoir ;
3. une liste quotidienne des commandes en retard pour le service client ;
4. un message de retard envoyé automatiquement au client.

Le découpage suit le gel des mises en production du 16 novembre au 11 janvier (`CT-07`) et le découpage V1 / V2 de l'analyse :
- **Lot 1** (exigences 1 à 3, critères 11.1, 11.2, 11.4, 11.7, 11.8) : outils internes, sans aucun envoi aux clients. **Sa date de mise en service dépend de la question bloquante Q03** (dérogation au gel avant le 16 novembre, ou mise en service après le 11 janvier). La spec ne la fixe pas.
- **Lot 2** (exigences 4 à 7 et 9, critères 11.3, 11.5, 11.6) : Comptoir et message de retard par e-mail, au premier trimestre 2027.
- **Lot 3 = V2** (exigences 8 et 10) : validation des messages Premium et canal SMS. Ces options restent désactivées tant que la catégorie Premium n'est pas définie (Q04) et que la DPO n'a pas rendu son avis sur l'usage du mobile (`CT-02`).

## Glossaire

- **Colis** : unité expédiée et suivie par un transporteur ; une commande peut comporter plusieurs colis.
- **Date promise (J)** : date de livraison affichée au client sur Vitrine au moment de la commande.
- **J+1, J+2** : premier et deuxième jour suivant la date promise. Selon `H02`, J+2 correspond aux 48 heures après la date promise demandées par la logistique.
- **Statut transporteur** : événement de suivi d'un colis (pris en charge, en transit, livré, incident…) reçu par Passerelle.
- **Niveau de retard** : état calculé d'un colis non livré : `à l'heure`, `à surveiller` (J+1) ou `en retard` (J+2). Les seuils sont des paramètres (`H02`).
- **Niveau d'alerte client** : niveau de retard qui déclenche le message au client ; paramètre, `en retard` par défaut (`H02`).
- **Délai de rafraîchissement** : délai maximal entre la réception d'un statut par Passerelle et son affichage sur le tableau de bord ; paramètre dont la valeur cible sera fixée après mesure (`H04`).
- **Dossier ouvert** : demande client en cours de traitement dans Comptoir sur une commande (définition exacte à confirmer, voir « Points à ajouter à l'analyse »).
- **Client Premium** : catégorie de client citée par le service client ; définition et lien avec Orvanne+ à confirmer (Q04).
- **Message de retard** : message de service informant un client du retard de sa commande ; il ne contient aucune offre commerciale (`CT-03`).
- **Liste quotidienne** : liste des commandes concernées par un retard, publiée chaque matin pour le service client.
- **Administrateur métier** : utilisateur habilité à modifier les seuils, canaux, horaires et options de l'application.
- **WISMO** : contact client demandant où en est sa commande.

## Exigences

### Exigence 1 : consolidation des statuts de suivi des colis (lot 1)

**User story :** En tant que membre des équipes transport, je veux que les statuts des trois transporteurs soient consolidés automatiquement à partir de Passerelle, afin de ne plus croiser à la main les extractions de Hangar et les fichiers des transporteurs.

#### Critères d'acceptation

1. QUAND Passerelle reçoit un statut transporteur pour un colis, LE SYSTÈME DOIT l'enregistrer dans l'historique de ce colis avec son horodatage d'origine et son horodatage de réception. _Source : B01-D10_
2. LE SYSTÈME DOIT rattacher chaque colis à sa commande, à son transporteur, à son entrepôt d'expédition (E1, E2 ou E3), à sa région de livraison et à la date promise affichée sur Vitrine. _Source : B01-D3, B02-D6_
3. LE SYSTÈME DOIT traiter les statuts des trois transporteurs d'Orvanne. _Source : B02-D3_
4. SI un statut déjà enregistré pour un colis est reçu de nouveau, ALORS LE SYSTÈME DOIT l'ignorer sans créer de doublon dans l'historique. _Source : B01-D10_
5. SI un code de statut transporteur n'est pas reconnu, ALORS LE SYSTÈME DOIT conserver l'événement avec son code d'origine, ne pas modifier le niveau de retard du colis et signaler le code à la supervision. _Source : B01-D10, B02-D3_
6. QUAND Passerelle reçoit un lot de statuts, LE SYSTÈME DOIT les rendre visibles sur le tableau de bord dans le délai de rafraîchissement paramétré, sans attendre de traitement quotidien. _Source : B01-D2, H04_
7. LE SYSTÈME DOIT calculer chaque jour, par transporteur, la médiane et le 95e centile du délai entre l'horodatage d'origine des statuts et leur réception par Passerelle. _Source : B01-D2, H04_
8. SI aucun statut n'a été reçu d'un transporteur depuis une durée supérieure au seuil paramétré, ALORS LE SYSTÈME DOIT afficher sur le tableau de bord un bandeau signalant l'interruption du flux de ce transporteur. _Source : B01-D10, H04_

### Exigence 2 : détection des retards (lot 1)

**User story :** En tant que responsable transport, je veux que le système calcule le niveau de retard de chaque colis, afin d'agir avant que le client appelle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT attribuer à chaque colis non livré un niveau de retard `à l'heure`, `à surveiller` ou `en retard`, calculé à partir de la date promise affichée sur Vitrine. _Source : B02-D6, B01-D7, H02_
2. QUAND le calcul du matin de J+1 constate qu'un colis n'est pas livré, LE SYSTÈME DOIT le passer au niveau `à surveiller`. _Source : B02-D6, H02_
3. QUAND le calcul du matin de J+2 constate qu'un colis n'est toujours pas livré, LE SYSTÈME DOIT le passer au niveau `en retard`. _Source : B01-D7, H02_
4. QUAND un colis reçoit le statut « livré », LE SYSTÈME DOIT le retirer du suivi des retards et de la liste quotidienne. _Source : B01-D1, B02-D15_
5. LE SYSTÈME DOIT permettre à un administrateur métier de modifier, sans nouvelle mise en production, le nombre de jours après la date promise qui déclenche chacun des deux niveaux. _Source : H02_
6. LE SYSTÈME DOIT recalculer chaque matin le niveau de tous les colis non livrés avant l'heure de publication de la liste quotidienne. _Source : B02-D6, B02-D15, H02_
7. SI la date promise d'un colis est inconnue, ALORS LE SYSTÈME DOIT l'exclure du calcul des niveaux et le compter à part sur le tableau de bord. _Source : B02-D6_

### Exigence 3 : tableau de bord des retards (lot 1)

**User story :** En tant que membre des équipes transport ou responsable d'entrepôt, je veux un tableau de bord des colis en retard, afin de repérer les dérives par transporteur, par entrepôt et par région, et d'agir dessus.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher le nombre de colis `à surveiller` et `en retard`, ventilé par transporteur, par entrepôt (E1, E2, E3) et par région de livraison. _Source : B01-D1, B01-D3_
2. QUAND un utilisateur sélectionne une ventilation, LE SYSTÈME DOIT afficher la liste des colis concernés puis, à la sélection d'un colis, sa commande, l'historique de ses statuts, sa date promise et la nouvelle date de livraison si elle est connue. _Source : B01-D3, B01-D6_
3. LE SYSTÈME DOIT afficher en rouge les colis du niveau paramétré comme prioritaire, `en retard` par défaut, et les placer en tête des listes par ancienneté du retard décroissante. _Source : B01-D4, H02_
4. LE SYSTÈME DOIT afficher, pour chaque transporteur, la date et l'heure de la dernière mise à jour des données. _Source : B01-D2, H04_
5. LE SYSTÈME DOIT réserver l'accès au tableau de bord aux équipes transport, aux responsables d'entrepôt et aux administrateurs métier. _Source : B01-D1, CT-01_

### Exigence 4 : suivi des colis dans la fiche commande de Comptoir (lot 2)

**User story :** En tant que conseiller du service client, je veux voir le suivi des colis dans la fiche commande de Comptoir, afin de répondre au client sans ouvrir le site du transporteur.

#### Critères d'acceptation

1. QUAND un conseiller ouvre une fiche commande dans Comptoir, LE SYSTÈME DOIT afficher pour chaque colis de la commande le dernier statut, son horodatage, le niveau de retard et l'historique complet des statuts, sans quitter Comptoir. _Source : B02-D1_
2. LE SYSTÈME DOIT afficher le suivi des colis dans la fiche commande en moins de 2 secondes, y compris au volume du pic (70 000 colis expédiés par jour). _Source : B02-D2, B01-D1_
3. LE SYSTÈME DOIT afficher ce suivi pour les colis des trois transporteurs. _Source : B02-D3_
4. SI le suivi n'est pas disponible dans le délai de 2 secondes, ALORS LE SYSTÈME DOIT afficher la fiche commande sans le suivi, avec un message indiquant que le suivi est momentanément indisponible. _Source : B02-D2_

### Exigence 5 : liste quotidienne des commandes en retard (lot 2)

**User story :** En tant que responsable du service client, je veux chaque matin la liste des commandes concernées par un retard, avant tout envoi aux clients, afin d'anticiper les appels et de savoir quels messages partent.

#### Critères d'acceptation

1. QUAND l'heure de publication paramétrée est atteinte, LE SYSTÈME DOIT mettre à disposition du service client la liste des commandes ayant au moins un colis `à surveiller` ou `en retard`. _Source : B02-D15, H02_
2. LE SYSTÈME DOIT publier la liste du jour avant le premier envoi de message de retard de la journée et ne déclencher aucun envoi avant cette publication. _Source : B02-D14, H03_
3. LE SYSTÈME DOIT indiquer pour chaque commande de la liste les colis concernés et leur niveau, le transporteur, la présence d'un dossier ouvert dans Comptoir et l'état du message de retard (prévu dans la journée, envoyé, annulé, non envoyé avec son motif). _Source : B02-D15, B02-D14, B02-D7, H03_
4. LE SYSTÈME DOIT rendre la liste consultable par les membres du service client dans Comptoir. _Source : B02-D15_

### Exigence 6 : message de retard au client (lot 2)

**User story :** En tant que client, je veux être prévenu quand ma commande est en retard et savoir quand elle arrivera, afin de ne pas avoir à contacter le service client.

#### Critères d'acceptation

1. QUAND au moins un colis d'une commande atteint le niveau d'alerte client, LE SYSTÈME DOIT programmer un message de retard pour cette commande sans intervention manuelle, sous réserve des règles des exigences 7 et 8. _Source : B01-D5, B02-D4, B01-D8, H02, H03_
2. LE SYSTÈME DOIT permettre à un administrateur métier de choisir le niveau d'alerte client, `en retard` par défaut, sans nouvelle mise en production. _Source : H02_
3. LE SYSTÈME DOIT envoyer le message de retard par e-mail en V1. _Source : B02-D5, H01_
4. LE SYSTÈME DOIT envoyer au plus un message de retard par commande, listant tous les colis de la commande qui ont atteint le niveau d'alerte client au moment de l'envoi. _Source : B02-D4, H05_
5. QUAND une nouvelle date de livraison est connue pour un colis, LE SYSTÈME DOIT l'indiquer dans le message. _Source : B01-D6_
6. SI aucune nouvelle date de livraison n'est connue pour un colis, ALORS LE SYSTÈME DOIT utiliser le modèle de message sans date estimée. _Source : B01-D6_
7. QUAND un message de retard est envoyé, LE SYSTÈME DOIT l'enregistrer dans l'historique de la commande consultable dans Comptoir, avec sa date, son canal, la version du modèle et le contenu envoyé. _Source : B02-D14, H03_
8. SI le service d'envoi renvoie une erreur, ALORS LE SYSTÈME DOIT retenter l'envoi le nombre de fois paramétré puis marquer le message « non envoyé : erreur technique » dans la liste quotidienne. _Source : B02-D14_
9. SI l'adresse e-mail du client est absente ou invalide, ALORS LE SYSTÈME DOIT ne pas envoyer le message et le marquer « non envoyé : coordonnées » dans la liste quotidienne. _Source : B02-D14, B02-D5_
10. QUAND la commande est livrée avant l'envoi d'un message programmé ou en attente de validation, LE SYSTÈME DOIT annuler ce message. _Source : B02-D4_

### Exigence 7 : non-envoi en cas de dossier ouvert (lot 2)

**User story :** En tant que responsable du service client, je veux qu'aucun message automatique ne contredise un échange en cours, afin que le client ne reçoive pas deux discours différents.

#### Critères d'acceptation

1. SI un dossier est ouvert dans Comptoir sur la commande, ALORS LE SYSTÈME DOIT ne pas envoyer le message de retard et indiquer le motif « dossier ouvert » dans la liste quotidienne. _Source : B02-D7, H03_
2. LE SYSTÈME DOIT vérifier l'absence de dossier ouvert au moment de l'envoi, et non au moment du calcul du retard. _Source : B02-D7_
3. SI Comptoir ne répond pas lors de cette vérification, ALORS LE SYSTÈME DOIT reporter l'envoi et ne jamais envoyer de message sans vérification. _Source : B02-D7_

### Exigence 8 : validation des messages Premium (lot 3, V2, option)

**User story :** En tant que responsable du service client, je veux pouvoir faire valider par un conseiller les messages destinés aux clients Premium, afin de garder la main sur la relation avec ces clients.

#### Critères d'acceptation

1. OÙ la validation des messages Premium est activée, LE SYSTÈME DOIT placer les messages destinés aux clients Premium dans une file de validation de Comptoir au lieu de les envoyer. _Source : B02-D8, H03_
2. LE SYSTÈME NE DOIT PAS permettre l'activation de la validation Premium tant que la règle d'identification des clients Premium n'est pas paramétrée. _Source : H03_
3. QUAND un conseiller valide un message de la file, LE SYSTÈME DOIT appliquer de nouveau la règle du critère 7.1 puis envoyer le message. _Source : B02-D8, B02-D7_
4. QUAND un conseiller rejette un message de la file, LE SYSTÈME DOIT l'abandonner et enregistrer le motif saisi. _Source : B02-D8, CT-10_
5. SI un message de la file n'est pas traité dans le délai de validation paramétré, ALORS LE SYSTÈME DOIT appliquer l'action d'expiration paramétrée (envoyer ou abandonner) et le signaler au responsable du service client. _Source : B02-D8, H03_
6. QUAND un conseiller valide ou rejette un message, LE SYSTÈME DOIT journaliser son identifiant, l'action et l'horodatage. _Source : CT-10_

### Exigence 9 : modèles de message (lot 2)

**User story :** En tant que membre de l'équipe du service client, je veux modifier moi-même le texte des messages, afin d'ajuster la communication sans passer par la DSI.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au service client de créer, modifier, prévisualiser et activer les modèles de message, par canal et par cas (avec ou sans nouvelle date), sans intervention de la DSI. _Source : B02-D9_
2. LE SYSTÈME DOIT n'accepter dans les modèles que les variables d'une liste fermée de variables de service validée par la DPO. _Source : B02-D10, CT-03, CT-01_
3. SI un modèle contient un code promotionnel, un lien vers une offre ou un terme de la liste des termes commerciaux interdits, ALORS LE SYSTÈME DOIT refuser son activation. _Source : B02-D10, CT-03, H06_
4. LE SYSTÈME DOIT conserver l'historique des versions de chaque modèle, avec leur auteur et leur date d'activation. _Source : B02-D9, CT-10_
5. QUAND un utilisateur prévisualise un modèle, LE SYSTÈME DOIT afficher le message rempli avec des données synthétiques. _Source : B02-D9, CT-04_

### Exigence 10 : canal SMS (lot 3, V2, option)

**User story :** En tant que directrice des opérations logistiques, je veux pouvoir envoyer l'alerte par SMS une fois ce canal autorisé, afin de toucher les clients qui ne lisent pas leurs e-mails.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à un administrateur métier de choisir le canal d'envoi (e-mail seul, ou SMS avec repli sur l'e-mail) sans nouvelle mise en production. _Source : H01_
2. OÙ le canal SMS est activé, LE SYSTÈME DOIT envoyer le message par SMS aux clients dont le numéro de mobile est connu, et par e-mail aux autres. _Source : B01-D5, H01_
3. LE SYSTÈME NE DOIT PAS permettre l'activation du canal SMS tant que l'avis favorable de la DPO sur l'usage du numéro de mobile n'est pas enregistré dans l'application. _Source : CT-02, H01_
4. OÙ le canal SMS est activé, LE SYSTÈME DOIT refuser l'activation d'un modèle SMS dont la longueur, variables remplacées par leur longueur maximale, dépasse la longueur maximale paramétrée. _Source : B01-D5, H01_

### Exigence 11 : exigences non fonctionnelles

**User story :** En tant que DSI, je veux une solution dimensionnée pour le pic, hébergée chez Orvanne et conforme au RGPD, afin qu'elle tienne quand elle est la plus utile.

#### Critères d'acceptation

1. LE SYSTÈME DOIT intégrer les statuts de 70 000 colis expédiés par jour, volume du pic, en respectant le délai de rafraîchissement paramétré du critère 1.6. _Source : B01-D1, B01-D2_
2. LE SYSTÈME DOIT être hébergé dans le cloud d'Orvanne, dans l'Union européenne. _Source : B01-D9, CT-08_
3. LE SYSTÈME DOIT supprimer les historiques de statuts et de messages à l'issue d'une durée de conservation paramétrable, fixée avec la DPO. _Source : CT-01_
4. LE SYSTÈME DOIT journaliser les accès au tableau de bord, les modifications de modèles et de paramètres, et les actions des conseillers sur les messages. _Source : CT-10, CT-01_
5. LE SYSTÈME DOIT produire chaque jour, avec un export, le nombre de messages de retard programmés, envoyés, annulés, non envoyés par motif, validés, rejetés et expirés, pour le suivi du taux de contacts WISMO. _Source : B02-D11_
6. QUAND la DPO transmet une demande d'accès ou d'effacement concernant un client, LE SYSTÈME DOIT permettre d'extraire ou de supprimer les messages de retard de ce client. _Source : CT-01_
7. LE SYSTÈME DOIT pouvoir être mis en service avec l'envoi de messages aux clients désactivé, l'activation se faisant par paramètre sans nouvelle mise en production. _Source : B01-D1, B02-D12, CT-07_
8. LE SYSTÈME DOIT être testé et démontré uniquement avec des données synthétiques ou anonymisées. _Source : CT-04_

## Hors périmètre

- Code promo dans les messages de retard (`B05-D7`) : interdit dans un message de service par `CT-03` (`H06`). Une offre commerciale relèverait d'un message marketing distinct, soumis au consentement ; renvoyée vers aucun projet (conflit C07, Q07).
- Planning demandé à la DSI pour la fin de la semaine suivante (`B01-D11`) : livrable de gestion de projet, pas une exigence du système. Le découpage en lots de `tasks.md` sert de base à ce planning, sous réserve de Q03 ; renvoyé vers aucun projet.
- Mise en service au premier trimestre 2027 (`B02-D13`) : échéance de planning, pas un comportement du système. Elle fixe la date du lot 2 dans `tasks.md`.
- Mesure du taux de contacts WISMO et de sa baisse de 30 % (`B02-D11`, partie mesure) : les contacts sont comptés par les outils du service client, et la base de référence reste à définir (Q39). Le projet fournit les données d'envoi (critère 11.5).
- Tableau de bord pour le service client (`B02-D15`) : le service client demande une liste, pas un tableau de bord ; il reçoit la liste quotidienne (exigence 5) et le suivi dans Comptoir (exigence 4).
- Validation manuelle de chaque message par un conseiller (`B01-D8`) : écartée ; seule la validation optionnelle des messages Premium est prévue (exigence 8, `H03`).
- Accès partagé aux statuts transporteurs avec le portail de retours (P02) : le référentiel de suivi peut servir P02, mais les besoins de P02 sont spécifiés dans P02.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H01 | Le canal de l'alerte est un paramètre. La V1 envoie un e-mail à tous les clients concernés. Le SMS n'est activé qu'après analyse de la DPO (CT-02) et accord budgétaire, pour les seuls clients dont le mobile est connu. | C01 | oui |
| H02 | Le seuil de retard est un paramètre calculé à partir de la date promise affichée sur Vitrine, avec deux niveaux : « à surveiller » à J+1 matin (liste du service client, tableau de bord) et « en retard » à J+2, soit 48 h (alerte au client). La signification des « rouges » (B01-D4) reste à définir. | C02 | oui |
| H03 | L'alerte part automatiquement (B01-D8). Le service client reçoit chaque matin, avant les envois du jour, la liste des commandes concernées (B02-D15), ce qui répond à B02-D14. Aucune alerte si un dossier est ouvert dans Comptoir (B02-D7). La validation préalable pour les clients Premium (B02-D8) est une option paramétrable, désactivée tant que la catégorie Premium n'est pas définie. | C04 | oui |
| H04 | Le tableau de bord est rafraîchi à chaque arrivée de statuts dans Passerelle et affiche l'heure de la dernière mise à jour. La fréquence cible est fixée après mesure de la fraîcheur des statuts des 3 transporteurs. | C05 | oui |
| H05 | Le retard est évalué par colis. Le client reçoit au plus un message par commande, qui liste les colis en retard. | C06 | oui |
| H06 | L'alerte de retard ne contient ni code promo ni offre commerciale. Une éventuelle offre relève d'un message marketing distinct, hors P01, soumis aux règles de consentement. | C07 | oui |

Le conflit C03 (échéance « pour le pic » contre gel des mises en production) est **bloquant** et n'a pas d'hypothèse : la date du lot 1 n'est pas spécifiée (Q03).

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q01 | Quel canal pour l'alerte de retard : e-mail, SMS (budget, avis DPO sur l'usage du mobile), ou les deux selon la disponibilité du mobile ? | Solène Garrigue, Yanis Mercadier ; avis d'Hélène Marsac | non (activation de l'exigence 10) |
| Q02 | À partir de quand une commande est-elle « en retard » : J+1 matin ou 48 h après la date promise ? Le seuil peut-il différer entre la liste du service client, le tableau de bord et l'alerte client ? Que signifient les « rouges » du tableau de bord ? | Solène Garrigue, Yanis Mercadier | non (valeurs des critères 2.5, 3.3, 6.2) |
| Q03 | Le pic tombe pendant le gel du 16/11 au 11/01. Une dérogation est-elle envisageable pour un tableau de bord interne, sans envoi aux clients, avant le 16/11 ? Sinon, confirmez-vous une mise en service au T1 2027 ? | DSI (Bertrand Lacassagne) | oui (date de mise en service du lot 1, tâche 5) |
| Q04 | Qu'est-ce qu'un client Premium (lien avec Orvanne+) ? La liste du matin suffit-elle à « savoir » qu'un message part, ou faut-il une validation ? Quel délai de validation pour les Premium, et que se passe-t-il sans validation ? | Yanis Mercadier ; Capucine Lorrain pour le lien avec Orvanne+ | non (activation de l'exigence 8) |
| Q05 | À quelle fréquence Passerelle reçoit-elle les statuts des 3 transporteurs ? Quel délai de rafraîchissement du tableau de bord est acceptable pour la logistique ? | Solène Garrigue ; DSI (équipe Passerelle) | non (valeur des critères 1.6 et 1.8) |
| Q06 | Pour une commande à plusieurs colis, le client reçoit-il un message par colis en retard ou un seul message par commande ? | Solène Garrigue, Yanis Mercadier | non (critère 6.4) |
| Q07 | Confirmez-vous l'abandon du code promo dans les messages de retard (CT-03) ? Souhaitez-vous à la place un message commercial distinct, soumis au consentement ? | Capucine Lorrain ; Hélène Marsac | non |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne (B01) s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis (B03, B07-D20) ? | DSI (comité d'architecture) | non (P01 reste dans le cloud d'Orvanne, critère 11.2) |
| Q36 | Quand pouvez-vous examiner les traitements des projets P01, P02, P03, P04, P06 et P07 (CT-01) ? Lesquels exigent une analyse d'impact ? | Hélène Marsac | non (prérequis du développement, tâche 1.1) |
| Q39 | Quelle base de référence et quelle période de mesure pour la baisse de 30 % des contacts WISMO et la baisse de 60 % des contacts liés aux retours ? | Yanis Mercadier ; direction de l'expérience client | non |

### Points à ajouter à l'analyse

Ces manques des sources n'ont ni question ni hypothèse dans `work/analyse.json`. La spec les traite comme des paramètres ou des vérifications préalables (tâches 1.3, 1.4 et 1.6), sans fixer de valeur :

- origine de la nouvelle date de livraison : transporteur ou calcul interne (B01-F3) ;
- origine de la date promise de chaque colis et sa disponibilité dans Passerelle (B02-D6) ;
- découpage des « régions » du tableau de bord (B01-D3) ;
- définition d'un dossier ouvert dans Comptoir, et comportement si le dossier est clôturé ensuite (B02-F4) ;
- heure exacte de « J+1 matin » et cas d'une date promise modifiée après la commande (B02-F3) ;
- format de la liste quotidienne (B02-F9) ;
- capacités d'extension de Comptoir (encart, liste, file de validation) et service d'envoi des e-mails transactionnels.
