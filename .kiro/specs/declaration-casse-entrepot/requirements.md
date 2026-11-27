# Exigences : déclaration de casse à la douchette, blocage du stock dans Hangar et litiges transporteurs

<!-- Projet P03, slug declaration-casse-entrepot. Commanditaire : exploitation de l'entrepôt E2 (rattachement de direction à confirmer).
     Parties prenantes : DSI, transport, chefs d'équipe E2, entrepôts E1 et E3, direction juridique et conformité (DPO).
     Sources : B06 (toutes les demandes), B04 (B04-D13). Conflits : C12, C16, C17. -->

## Introduction

Sur l'entrepôt E2, un préparateur ou un cariste qui trouve un colis abîmé le pose sur la palette rouge et remplit une fiche papier. Cette fiche arrive au bureau le soir, le lendemain ou jamais. Les litiges transporteurs sont donc déclarés hors délai une fois sur deux, alors que le délai de déclaration serait de 7 jours (valeur non confirmée). Le stock abîmé n'est pas bloqué à temps dans Hangar, avec le risque de revendre un article cassé.

E2 déclare environ 40 cas de casse par jour, et l'exploitation estime le nombre réel au double. Le site compte une soixantaine de douchettes, dont deux tiers d'anciennes sans appareil photo. Le réseau ne passe pas dans certaines allées du fond.

Le projet remplace la fiche papier par une déclaration à la douchette. Cette déclaration fonctionne sans réseau, crée le dossier de casse, prévient le chef d'équipe et le transport, demande le blocage du stock dans Hangar et suit le délai de déclaration du litige.

Le projet est livré en deux lots :
- **Lot 1** (exigences 1 à 7 et 10) : déclaration de casse sur E2. Mise en service au plus tôt le 12 janvier 2027, après le gel des mises en production (`CT-07`) et après l'avis de la DPO sur les photos (`H16`). Si l'inventaire de janvier a lieu avant cette date, qui n'est pas connue (`Q17`), il se fait avec la fiche papier actuelle.
- **Lot 2** (exigences 8 et 9) : ajout de photos depuis le téléphone d'un chef d'équipe, et saisie de la note A / B / C des retours abîmés sur le même écran. Le lot 2 dépend de la grille A / B / C définie par le portail de retours (P02) et des réponses à `Q16` et `Q37`.

## Glossaire

- **Douchette** : terminal de scan de l'entrepôt. E2 utilise deux générations : les nouvelles ont un appareil photo, les anciennes non.
- **Terminal** : douchette, ou téléphone d'un chef d'équipe en lot 2.
- **Identifiant scanné** : code lu sur le colis par le terminal. Sa nature exacte (étiquette transporteur, étiquette Hangar) est à confirmer.
- **Déclaration de casse** : saisie faite sur le terminal (identifiant scanné, type de dégât, photos facultatives), puis transmise au serveur.
- **Dossier de casse** : dossier créé automatiquement à la réception d'une déclaration. Il regroupe les déclarations d'un même colis, la demande de blocage, les notifications et le suivi du litige.
- **Type de dégât** : valeur choisie dans une liste paramétrable par site. La liste initiale doit être fournie par l'exploitation E2.
- **Blocage du stock** : statut posé dans Hangar qui empêche de vendre ou de préparer le stock concerné.
- **Synchronisation** : transmission au serveur des déclarations saisies sur le terminal sans réseau.
- **Litige transporteur** : réclamation adressée à un transporteur pour un colis abîmé, à déclarer dans un délai.
- **Date limite de déclaration** : date avant laquelle le litige doit être déclaré au transporteur (date de départ plus délai paramétré).
- **Le transport** : destinataire désigné par « le transport » dans B06 ; son identité (service interne ou transporteur) est à confirmer (`Q29`).
- **Grille A / B / C** : note de contrôle qualité d'un retour, définie par le portail de retours (P02) : A remis en stock, B déstockage, C rebut.
- **Administrateur métier** : membre de l'exploitation habilité à modifier le paramétrage du site.

## Exigences

### Exigence 1 : saisie de la déclaration de casse

**User story :** En tant que préparateur ou cariste de E2, je veux déclarer un colis abîmé avec ma douchette, afin de ne plus remplir de fiche papier.

#### Critères d'acceptation

1. QUAND un préparateur ou un cariste scanne un colis dans l'écran de déclaration de casse, LE SYSTÈME DOIT ouvrir une déclaration pré-remplie avec l'identifiant scanné, le site, le terminal, l'utilisateur connecté et l'horodatage du terminal. _Source : B06-D1_
2. SI le code du colis ne peut pas être lu, ALORS LE SYSTÈME DOIT permettre de saisir l'identifiant au clavier et doit marquer la déclaration comme « saisie manuelle ». _Source : B06-D1_
3. LE SYSTÈME DOIT imposer le choix d'un type de dégât dans la liste active du site avant de permettre la validation de la déclaration. _Source : B06-D3_
4. LE SYSTÈME DOIT permettre à un administrateur métier de créer, renommer, désactiver et ordonner les types de dégât, sans nouvelle mise en production. _Source : B06-D3_
5. OÙ le terminal dispose d'un appareil photo, LE SYSTÈME DOIT permettre d'ajouter de 0 à 2 photos à la déclaration, sous réserve du critère 1.8. _Source : B06-D2, H15_
6. LE SYSTÈME DOIT accepter la validation d'une déclaration sans photo, quel que soit le terminal. _Source : B06-D6, H15_
7. LE SYSTÈME DOIT fonctionner sur les deux générations de douchettes en service à E2, la prise de photo étant masquée sur les douchettes sans appareil photo. _Source : B06-D6_
8. PENDANT QUE l'avis de la DPO sur le traitement des photos n'est pas enregistré dans le paramétrage, LE SYSTÈME NE DOIT PAS proposer la prise de photo. _Source : CT-01, CT-06, H16_
9. QUAND l'utilisateur valide une déclaration, LE SYSTÈME DOIT afficher un accusé indiquant si la déclaration est transmise au serveur ou en attente de synchronisation. _Source : B06-D4, B06-D8_

### Exigence 2 : fonctionnement sans réseau et synchronisation

**User story :** En tant que préparateur ou cariste travaillant dans une allée sans réseau, je veux déclarer la casse sur place, afin de ne pas avoir à revenir dans une zone couverte ni à noter l'information ailleurs.

#### Critères d'acceptation

1. PENDANT QUE le terminal n'a pas de réseau, LE SYSTÈME DOIT permettre de saisir et de valider une déclaration complète, photos comprises. _Source : B06-D8_
2. LE SYSTÈME DOIT conserver sur le terminal la dernière liste des types de dégât reçue du serveur, afin de la proposer hors réseau. _Source : B06-D8, B06-D3_
3. LE SYSTÈME DOIT conserver sur le terminal au moins 80 déclarations non synchronisées avec 2 photos chacune, sans perte en cas d'arrêt, de batterie vide ou de redémarrage du terminal. _Source : B06-D8, B06-D2_
4. QUAND le réseau redevient disponible, LE SYSTÈME DOIT transmettre les déclarations en attente sans action de l'utilisateur, dans l'ordre de leur saisie. _Source : B06-D8_
5. LE SYSTÈME DOIT retenir l'horodatage de saisie sur le terminal comme date de la déclaration, quelle que soit la date de synchronisation. _Source : B06-D8, B06-D11_
6. SI une même déclaration est transmise plusieurs fois, par exemple lors d'une reprise après coupure, ALORS LE SYSTÈME DOIT ne l'enregistrer qu'une fois côté serveur. _Source : B06-D8, B06-D4_
7. LE SYSTÈME DOIT afficher en permanence sur le terminal le nombre de déclarations en attente de synchronisation. _Source : B06-D8_
8. QUAND le serveur a accusé réception d'une déclaration, LE SYSTÈME DOIT effacer du terminal cette déclaration et ses photos. _Source : B06-D8, CT-06_
9. LE SYSTÈME NE DOIT PAS enregistrer les photos dans la galerie du terminal ni dans un espace accessible à d'autres applications. _Source : CT-06_

### Exigence 3 : création automatique du dossier de casse

**User story :** En tant que chef d'équipe, je veux qu'un dossier de casse soit créé dès la déclaration, afin de disposer immédiatement de l'information au lieu d'attendre la fiche papier.

#### Critères d'acceptation

1. QUAND le serveur reçoit une déclaration, LE SYSTÈME DOIT créer automatiquement un dossier de casse contenant l'identifiant scanné, le site, le type de dégât, les photos, le déclarant, la date de la déclaration et la date de réception par le serveur. _Source : B06-D4_
2. SI un dossier de casse non clos existe déjà pour le même identifiant sur le même site, ALORS LE SYSTÈME DOIT rattacher la nouvelle déclaration à ce dossier au lieu d'en créer un autre. _Source : B06-D4_
3. QUAND un dossier est créé, LE SYSTÈME DOIT compléter le dossier avec les articles, les quantités, l'emplacement, le transporteur et la date de réception que Hangar associe à l'identifiant scanné, quand Hangar les connaît. _Source : B06-D4, B06-D9_
4. SI Hangar ne connaît pas l'identifiant scanné, ALORS LE SYSTÈME DOIT passer le dossier au statut « à vérifier » et le signaler aux chefs d'équipe du site. _Source : B06-D4, B06-D5_
5. LE SYSTÈME DOIT gérer pour chaque dossier les statuts « à vérifier », « ouvert », « litige déclaré », « sans litige » et « clos », la clôture étant faite par le transport ou par un chef d'équipe. _Source : B06-D4, B06-D11_
6. LE SYSTÈME DOIT permettre aux chefs d'équipe et au transport de consulter la liste des dossiers du site et le détail d'un dossier, photos comprises, depuis un écran web. _Source : B06-D4, B06-D5_
7. LE SYSTÈME DOIT permettre à un chef d'équipe de corriger l'identifiant d'un dossier « à vérifier », en conservant la valeur d'origine dans l'historique du dossier. _Source : B06-D4_

### Exigence 4 : notification du chef d'équipe et du transport

**User story :** En tant que chef d'équipe ou membre du transport, je veux être prévenu de chaque casse déclarée, afin d'agir le jour même.

#### Critères d'acceptation

1. QUAND un dossier de casse est créé, LE SYSTÈME DOIT notifier les chefs d'équipe et les destinataires « transport » paramétrés pour le site. _Source : B06-D5_
2. LE SYSTÈME DOIT inclure dans la notification l'identifiant scanné, le type de dégât, la date de la déclaration, le nombre de photos, la date limite de déclaration du litige et un lien vers le dossier. _Source : B06-D5, H28_
3. LE SYSTÈME DOIT permettre à un administrateur métier de modifier les destinataires des notifications de son site, sans nouvelle mise en production. _Source : B06-D5_
4. LE SYSTÈME NE DOIT PAS joindre les photos à la notification, les photos restant consultables uniquement dans le dossier. _Source : CT-06_
5. SI l'envoi d'une notification échoue, ALORS LE SYSTÈME DOIT réessayer, puis afficher le dossier comme « non notifié » dans l'écran de suivi. _Source : B06-D5_

### Exigence 5 : blocage du stock dans Hangar

**User story :** En tant que responsable de l'exploitation E2, je veux que le stock abîmé soit bloqué dans Hangar dès la déclaration, afin de ne pas revendre un article cassé.

#### Critères d'acceptation

1. QUAND un dossier de casse est créé, LE SYSTÈME DOIT demander à Hangar le blocage du stock rattaché à l'identifiant scanné. _Source : B06-D9_
2. LE SYSTÈME DOIT bloquer par défaut la totalité du stock que Hangar rattache à l'identifiant scanné, la granularité du blocage (colis, article, quantité) étant un paramètre du site. _Source : B06-D9_
3. QUAND Hangar confirme le blocage, LE SYSTÈME DOIT enregistrer la confirmation et son horodatage dans le dossier. _Source : B06-D9_
4. SI Hangar est indisponible ou refuse le blocage, ALORS LE SYSTÈME DOIT réessayer automatiquement, afficher le dossier comme « blocage en attente » et alerter les chefs d'équipe du site si le blocage n'est pas confirmé à l'issue du délai paramétré. _Source : B06-D9_
5. LE SYSTÈME DOIT afficher dans l'écran de suivi la liste des dossiers dont le blocage n'est pas confirmé. _Source : B06-D9_
6. QUAND une déclaration est validée sans réseau, LE SYSTÈME DOIT indiquer sur le terminal que le stock ne sera bloqué dans Hangar qu'après la synchronisation. _Source : B06-D9, B06-D8_

### Exigence 6 : suivi des litiges transporteurs

**User story :** En tant que membre du transport, je veux connaître pour chaque casse la date limite de déclaration du litige, afin de ne plus déclarer hors délai.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer pour chaque dossier une date limite de déclaration du litige, égale à la date de départ augmentée du délai paramétré, de 7 jours par défaut. _Source : B06-D11, H28_
2. LE SYSTÈME DOIT prendre comme date de départ la date de réception du colis dans Hangar quand elle est connue, et la date de la déclaration sinon, ce choix étant un paramètre. _Source : B06-D11, H28_
3. LE SYSTÈME DOIT permettre de paramétrer le délai de déclaration par transporteur, sans nouvelle mise en production. _Source : B06-D11, H28_
4. LE SYSTÈME DOIT afficher la date limite et le nombre de jours restants dans le dossier, dans la notification et dans l'écran de suivi. _Source : H28_
5. LE SYSTÈME DOIT renseigner le transporteur à partir de Hangar quand il est connu, et permettre au transport de le saisir sinon. _Source : B06-D11_
6. QUAND le transport qualifie un dossier, LE SYSTÈME DOIT enregistrer soit le statut « litige déclaré » avec la date et la référence de la déclaration chez le transporteur, soit le statut « sans litige » avec un motif. _Source : B06-D11_
7. SI un dossier est encore « ouvert » à moins du nombre de jours paramétré avant sa date limite, ALORS LE SYSTÈME DOIT alerter les destinataires « transport » du site. _Source : B06-D11, H28_
8. LE SYSTÈME DOIT trier la liste des dossiers « ouverts » par date limite croissante. _Source : B06-D11_
9. LE SYSTÈME DOIT produire chaque jour, par site et par transporteur, le nombre de dossiers créés, de litiges déclarés dans le délai, de litiges déclarés hors délai et de dossiers dont la date limite est dépassée sans qualification. _Source : B06-D11, B06-D4_

### Exigence 7 : déploiement site par site

**User story :** En tant que DSI, je veux activer la déclaration de casse site par site, afin de commencer par E2 et d'étendre ensuite aux autres entrepôts sans redéveloppement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre d'activer ou de désactiver la déclaration de casse pour chaque site (E1, E2, E3), sans nouvelle mise en production. _Source : B06-D12_
2. LE SYSTÈME DOIT être activé pour le seul site E2 lors de la première mise en service. _Source : B06-D12, H16_
3. LE SYSTÈME DOIT permettre de paramétrer séparément pour chaque site les types de dégât, les destinataires des notifications, la granularité du blocage et les délais. _Source : B06-D12, B06-D3, B06-D5_
4. PENDANT QUE la déclaration de casse n'est pas activée pour un site, LE SYSTÈME NE DOIT PAS accepter de déclaration provenant d'un terminal de ce site. _Source : B06-D12_

### Exigence 8 : photos depuis le téléphone d'un chef d'équipe (lot 2)

**User story :** En tant que chef d'équipe, je veux ajouter des photos depuis mon téléphone, afin de documenter les casses déclarées sur une douchette sans appareil photo.

#### Critères d'acceptation

1. OÙ l'usage du téléphone des chefs d'équipe est activé, LE SYSTÈME DOIT permettre à un chef d'équipe de retrouver un dossier par scan ou saisie de l'identifiant et d'y ajouter jusqu'à 2 photos. _Source : B06-D7, H15_
2. OÙ l'usage du téléphone des chefs d'équipe est activé, LE SYSTÈME DOIT permettre à un chef d'équipe de faire une déclaration de casse complète depuis son téléphone, selon les règles des exigences 1 et 3. _Source : B06-D7_
3. LE SYSTÈME DOIT réserver l'usage du téléphone aux utilisateurs authentifiés ayant le rôle de chef d'équipe. _Source : B06-D7, CT-06_
4. LE SYSTÈME DOIT appliquer sur le téléphone le fonctionnement sans réseau de l'exigence 2 et les critères 1.8, 2.8 et 2.9 sur les photos. _Source : B06-D7, B06-D8, CT-06_

### Exigence 9 : retours abîmés et note A / B / C (lot 2)

**User story :** En tant que contrôleur qualité des retours à E2, je veux saisir la note A / B / C et une photo sur le même écran que la casse, afin de ne pas utiliser un autre outil au contrôle.

#### Critères d'acceptation

1. OÙ la saisie des retours est activée pour le site, LE SYSTÈME DOIT proposer, sur le même écran que la déclaration de casse, un mode « retour » qui identifie le retour par scan. _Source : B06-D10, B04-D13_
2. LE SYSTÈME DOIT imposer en mode « retour » le choix d'une note A, B ou C, selon la grille définie par le portail de retours. _Source : B06-D10, B04-D13, B04-D11_
3. LE SYSTÈME DOIT permettre d'ajouter de 0 à 2 photos à la note, selon les règles des critères 1.5 à 1.8. _Source : B04-D13, H15_
4. QUAND une note est reçue par le serveur, LE SYSTÈME DOIT la transmettre au portail de retours avec l'identifiant du retour, la date du contrôle, le contrôleur et les photos, afin que le portail déclenche le remboursement. _Source : B04-D13, H07_
5. LE SYSTÈME NE DOIT PAS calculer ni transmettre de montant de remboursement, une note C étant transmise sans réduction. _Source : H11_
6. LE SYSTÈME DOIT appliquer au mode « retour » le fonctionnement sans réseau de l'exigence 2. _Source : B06-D8, B06-D10_
7. SI le portail de retours ne reconnaît pas l'identifiant du retour, ALORS LE SYSTÈME DOIT placer la note en anomalie et la signaler aux chefs d'équipe du site. _Source : B04-D13_
8. LE SYSTÈME DOIT accepter la note d'au moins 2 200 retours par jour sur E2, soit deux fois le volume actuel approximatif. _Source : B04-D13_

### Exigence 10 : sécurité, RGPD et exploitation

**User story :** En tant que DPO et DSI, je veux que les photos et les dossiers soient protégés, conservés une durée limitée et hébergés dans l'UE, afin que le traitement soit conforme et tienne la charge.

#### Critères d'acceptation

1. LE SYSTÈME DOIT traiter toutes les photos comme des données personnelles, qu'une étiquette ou une personne y soit visible ou non. _Source : CT-06_
2. LE SYSTÈME DOIT réserver l'accès aux dossiers et aux photos aux rôles chef d'équipe, transport, exploitation du site et administrateur métier, via l'authentification interne d'Orvanne. _Source : CT-06, CT-01_
3. LE SYSTÈME DOIT journaliser la création, la modification et la qualification des dossiers, chaque consultation de photo et chaque modification de paramètre, avec l'utilisateur et l'horodatage. _Source : CT-06, CT-01_
4. LE SYSTÈME DOIT supprimer automatiquement les photos, puis les dossiers, à l'issue de durées de conservation paramétrables fixées avec la DPO. _Source : CT-01, CT-06_
5. LE SYSTÈME DOIT chiffrer les déclarations et les photos stockées sur le terminal et sur le serveur, ainsi que leurs échanges. _Source : CT-06_
6. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_
7. LE SYSTÈME DOIT utiliser, hors production, uniquement des données synthétiques ou anonymisées, photos comprises. _Source : CT-04_
8. LE SYSTÈME DOIT accepter au moins 160 déclarations par jour sur E2, soit deux fois le volume réel estimé, et la synchronisation simultanée des 60 douchettes du site. _Source : B06-D4, B06-D8_

## Hors périmètre

- Échéance « pour l'inventaire de janvier » (`B06-D13`) : c'est une échéance, pas une exigence du système. Le gel des mises en production (`CT-07`) interdit une mise en service avant le 12 janvier 2027. Le lot 1 est mis en service au plus tôt à cette date (`H16`) ; un inventaire antérieur se fait avec la fiche papier. Aucun autre projet ne la reprend.
- Déblocage du stock dans Hangar : les sources ne décrivent ni qui débloque ni comment (B06-F11). Le déblocage reste fait dans Hangar selon les procédures actuelles, à confirmer avec l'exploitation E2.
- Envoi de la réclamation au transporteur : le transport déclare le litige avec ses outils actuels. Le système trace la date et la référence de la déclaration (critère 6.6).
- Définition de la grille A / B / C (`B04-D11`) et montant remboursé selon la note (`B04-D12`, conflit C12) : traités par le portail de retours, projet P02. P03 saisit et transmet la note (exigence 9), sans montant (`H11`).
- Mouvements de stock dans Hangar consécutifs à la note A / B / C (remise en stock, déstockage, rebut) : non décrits dans les sources, renvoyés vers P02 et la question `Q37`.
- Cadrage de E1 et E3 : l'activation est possible par paramétrage (exigence 7), mais E1 suit un autre processus avec son propre tableur (B06-F14). L'extension fera l'objet d'un cadrage distinct après le lot 1.
- Achat de téléphones pour les chefs d'équipe ou renouvellement des douchettes : décision d'équipement (`Q16`), pas une exigence du système.
- Photos des colis retour avant leur réception (`B04-D1`) : traitées dans P02.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H07 | Le déclencheur du remboursement est un paramètre (premier scan transporteur, réception en entrepôt, contrôle qualité). La V1 rembourse après le contrôle qualité en entrepôt ; le statut « reçu » précède « remboursé ». Pour P03, la note saisie au contrôle est l'événement qui permet ce remboursement. | C08 | oui |
| H11 | En V1, le montant remboursé ne dépend pas de la note A / B / C. Une note C déclenche un signalement pour traitement manuel par le service client, sans réduction automatique. | C12 | oui |
| H15 | La photo est facultative : une déclaration est valide sans photo. Les douchettes équipées proposent la photo ; l'ajout d'une photo depuis un autre terminal (téléphone de chef d'équipe) est prévu en V2. | C16 | oui |
| H16 | Le déploiement sur E2 a lieu au plus tôt le 12 janvier, après le gel et l'avis de la DPO sur les photos (CT-06). Si l'inventaire de janvier a lieu avant, il se fait avec la fiche papier actuelle. | C17 | oui |
| H28 | Le délai de déclaration des litiges transporteurs est un paramètre, avec 7 jours comme valeur provisoire ; le dossier de casse affiche la date limite de déclaration. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q12 | Est-il légal de réduire le montant remboursé selon la note de contrôle qualité (C, voire B) ? Si oui, quels montants pour A, B et C ? | Direction juridique et conformité | non (P03 transmet la note sans montant, critère 9.5) |
| Q16 | La photo est-elle obligatoire pour une déclaration de casse ? Faut-il équiper les chefs d'équipe de téléphones ou renouveler des douchettes ? | Karim Benhaddou ; DSI | non (exigence 8, lot 2) |
| Q17 | À quelle date a lieu l'inventaire de janvier sur E2 ? | Karim Benhaddou | non (date de mise en service du lot 1) |
| Q29 | Quel est le délai contractuel de déclaration d'un litige à chaque transporteur (7 jours ?) ? Qui est « le transport » à prévenir ? Le point de départ du délai (réception du colis ou constat de la casse) est à préciser avec cette réponse. | Service transport (à identifier via Karim Benhaddou) | non (valeurs par défaut des critères 4.1, 6.1 à 6.3) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne (B01) s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non (critère 10.6) |
| Q36 | Quand pouvez-vous examiner les traitements des projets P01, P02, P03, P04, P06 et P07 (CT-01) ? Lesquels exigent une analyse d'impact ? | Hélène Marsac | non pour la spécification ; oui pour l'activation des photos (critère 1.8) et la mise en service du lot 1 |
| Q37 | La saisie de la note A / B / C des retours se fait-elle sur la même application douchette que la casse ? En V1 du portail de retours ou plus tard ? | Karim Benhaddou ; Inès Rouvière | non (exigence 9, lot 2) |

### Points non couverts par l'analyse, à remonter à l'analyste

Ces manques ne bloquent pas la spécification. Ils sont traités par un paramètre ou une valeur par défaut prudente, qui reste à confirmer. Ils n'ont pas encore d'identifiant `Hnn` ou `Qnn`.

| Point | Traitement dans la spec | Critères | Interlocuteur proposé |
|---|---|---|---|
| Liste initiale des types de dégât (B06-F9) | Liste paramétrable par site | 1.3, 1.4 | Karim Benhaddou |
| Granularité du blocage et procédure de déblocage (B06-F11) | Totalité du stock rattaché par défaut ; déblocage hors périmètre | 5.2 | Karim Benhaddou ; équipe Hangar |
| Nature du code scanné (étiquette transporteur ou Hangar, colis entrant ou sortant) | Identifiant résolu par Hangar ; statut « à vérifier » sinon | 1.1, 3.3, 3.4 | Karim Benhaddou ; équipe Hangar |
| Point de départ du délai de litige | Paramètre, réception dans Hangar par défaut | 6.2 | Service transport (avec Q29) |
| Interfaces de Hangar (consultation, blocage, accusé) | Qualifiées en tâche 1.3 | 3.3, 5.1 à 5.4 | DSI (équipe Hangar) |
| Parc des douchettes (modèles, système, capacité de stockage) et couverture réseau, dont la zone C (B06-F1) | Inventaire en tâche 1.2 | 1.7, 2.1, 2.3 | DSI ; Karim Benhaddou |
| Délai cible entre la réception d'une déclaration et la notification ou la demande de blocage | Proposition de 5 minutes dans design.md, non reprise en exigence | 4.1, 5.1 | Karim Benhaddou |
| Direction de rattachement du commanditaire | — | — | Karim Benhaddou |
