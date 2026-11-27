# Exigences : prise de rendez-vous des livraisons fournisseurs

<!-- Projet P06, slug rdv-livraisons-fournisseurs. Commanditaire : approvisionnement et transport amont (Grégory Thibaudeau).
     Parties prenantes : exploitation E1 (chef de quai) et E2, achats, DSI, poste de garde. Source : B08. -->

## Introduction

Les fournisseurs et leurs transporteurs prennent rendez-vous par téléphone ou par e-mail, et les créneaux sont notés dans des tableurs par site. E1 reçoit environ 70 camions par jour et E2 une quarantaine. Un camion sur quatre se présente sans rendez-vous ou hors créneau, l'attente moyenne dépasse 1 h 30 le lundi matin et le bureau de réception passe environ 3 heures par jour au téléphone.

Le projet livre un portail web de réservation de créneaux de déchargement (règles R1 à R7), une vue planning par site, le pointage au poste de garde et l'export des indicateurs. Le pilote démarre sur E1 au printemps, avec une vingtaine de fournisseurs choisis par les achats.

**Lots.** V1 : toutes les exigences ci-dessous. V2 (hors de cette spec) : notation des fournisseurs, lien avec Hangar, application mobile pour les chauffeurs. Le gel des mises en production du 16/11 au 11/01 (CT-07) tombe avant le pilote : le développement et la recette se font en préproduction pendant le gel, et la première mise en production a lieu après le 11/01. Les échéances de préparation (liste des fournisseurs pilotes et vérification de Passerelle au 27/11, paramétrage de E1 au 04/12, chiffrage de la DSI en décembre) sont reprises dans `tasks.md`.

Plusieurs points ne sont pas arbitrés (durée des créneaux, nombre de quais de E1, messageries sans commande d'achat, notation). La spec les traite par des paramètres et des hypothèses (H20 à H23).

## Glossaire

- **Créneau** : plage de déchargement sur un quai. Sa durée est un paramètre de site, 30 minutes par défaut (H20).
- **Réservation** : engagement d'un fournisseur ou d'un transporteur (le réservant) à livrer une ou plusieurs commandes d'achat sur un ou plusieurs créneaux.
- **Commande d'achat** : commande passée par Orvanne à un fournisseur, lue dans Passerelle. « Soldée » signifie entièrement livrée ou close.
- **Camion complet** : camion déclaré comme tel à la réservation ; il consomme deux créneaux (H20). Sa définition précise reste à fournir par le chef de quai.
- **Pointage** : enregistrement de l'arrivée d'un camion par le poste de garde.
- **Créneau perdu** : créneau d'une réservation dont le camion arrive plus de 20 minutes après son début.
- **Clôture** : J-1 à midi, limite de réservation, de modification et d'annulation.

## Exigences

### Exigence 1 : accès des fournisseurs et des transporteurs

**User story :** En tant que responsable de l'approvisionnement, je veux que seuls des fournisseurs et des transporteurs identifiés réservent, afin de maîtriser l'accès au portail.

#### Critères d'acceptation

1. LE SYSTÈME DOIT proposer un portail web de réservation aux fournisseurs et à leurs transporteurs. _Source : B08-D1_
2. LE SYSTÈME DOIT exiger une authentification individuelle pour tout accès au portail. _Source : B08-D1, CT-01_
3. LE SYSTÈME DOIT permettre à un fournisseur de rattacher et de détacher ses transporteurs, un transporteur ne voyant que les commandes d'achat des fournisseurs qui l'ont rattaché. _Source : B08-D1, B08-D2_
4. LE SYSTÈME DOIT permettre de choisir la langue du portail et des e-mails par compte, le français étant la langue par défaut et les autres langues s'ajoutant sans modification du code. _Source : B08-D21, CT-11_
5. LE SYSTÈME DOIT respecter le RGAA et s'afficher correctement sur mobile pour les écrans du portail destinés aux tiers. _Source : CT-09_

### Exigence 2 : paramétrage des sites

**User story :** En tant que chef de quai, je veux paramétrer mon site, afin que les créneaux proposés correspondent à mes quais et à mes horaires.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre de paramétrer, pour chaque site, les quais de réception, les horaires d'ouverture et les jours fermés. _Source : B08-D7, H21_
2. LE SYSTÈME DOIT permettre de paramétrer la durée des créneaux par site, avec 30 minutes par défaut, sans limiter la valeur à 30 minutes ni à une heure. _Source : B08-D3, B08-D20, B08-D26, H20_
3. LE SYSTÈME DOIT accepter le paramétrage cible de E1 (4 quais, créneaux d'une heure) comme le paramétrage actuel (6 quais), la valeur retenue étant celle fournie par le chef de quai. _Source : B08-D26, H20, H21_
4. QUAND un paramétrage est enregistré, LE SYSTÈME DOIT afficher la capacité qui en résulte : créneaux par jour, par quai et pour le site. _Source : B08-D7, B08-D26, H21_
5. SI une modification de paramétrage rend impossibles des réservations existantes, ALORS LE SYSTÈME DOIT les lister et refuser la modification tant qu'elles n'ont pas été déplacées ou annulées. _Source : B08-D7_

### Exigence 3 : réservation d'un créneau

**User story :** En tant que fournisseur ou transporteur, je veux réserver moi-même un créneau de déchargement, afin de ne plus téléphoner au bureau de réception.

#### Critères d'acceptation

1. QUAND un réservant choisit un site, une date et des commandes d'achat, LE SYSTÈME DOIT afficher les créneaux disponibles. _Source : B08-D1_
2. LE SYSTÈME DOIT exiger au moins un numéro de commande d'achat par réservation, et en accepter plusieurs. _Source : B08-D2, H22_
3. LE SYSTÈME DOIT demander si le camion est complet et, si c'est le cas, réserver deux créneaux consécutifs sur le même quai. _Source : B08-D4, H20_
4. LE SYSTÈME DOIT ouvrir la réservation à J-10 et ne plus l'accepter après J-1 à midi, heure de Paris, ces bornes étant paramétrables par site. _Source : B08-D5_
5. SI la date demandée est hors des bornes de réservation, ALORS LE SYSTÈME DOIT refuser la réservation en indiquant les bornes. _Source : B08-D5_
6. QUAND une réservation est validée, LE SYSTÈME DOIT lui attribuer un quai libre et un numéro de réservation. _Source : B08-D1_
7. LE SYSTÈME DOIT empêcher deux réservations sur le même créneau du même quai, y compris quand deux réservants valident au même moment. _Source : B08-D1_
8. LE SYSTÈME DOIT enregistrer dans chaque réservation l'adresse e-mail du transporteur destinataire des messages. _Source : B08-D10_

### Exigence 4 : contrôle des commandes d'achat

**User story :** En tant qu'acheteur, je veux que seules des commandes valides soient réservées, afin d'éviter les camions qu'on ne sait pas réceptionner.

#### Critères d'acceptation

1. QUAND un numéro de commande d'achat est saisi, LE SYSTÈME DOIT vérifier dans Passerelle qu'il existe, qu'il n'est pas soldé et qu'il appartient à un fournisseur rattaché au réservant. _Source : B08-D2, B08-D27_
2. SI le numéro saisi est inconnu, soldé ou étranger au réservant, ALORS LE SYSTÈME DOIT refuser la réservation en indiquant le motif. _Source : B08-D2, H22_
3. SI Passerelle ne répond pas, ALORS LE SYSTÈME DOIT contrôler la commande sur la dernière copie connue, marquer la réservation « commande à revérifier » et la contrôler de nouveau au retour du service. _Source : B08-D27, B08-D2_
4. QUAND une commande d'une réservation à venir devient soldée, LE SYSTÈME DOIT alerter le chef de quai et le réservant sans annuler la réservation. _Source : B08-D2_
5. LE SYSTÈME DOIT refuser toute réservation sans commande d'achat valide, y compris pour les messageries et les petits colis. _Source : B08-D2, H22_

### Exigence 5 : modification et annulation

**User story :** En tant que réservant, je veux modifier ou annuler ma réservation, afin de libérer le créneau si mes plans changent.

#### Critères d'acceptation

1. PENDANT QUE la clôture n'est pas atteinte, LE SYSTÈME DOIT permettre au réservant de modifier le créneau, les commandes ou la déclaration « camion complet », et d'annuler sa réservation. _Source : B08-D6_
2. SI la clôture est atteinte, ALORS LE SYSTÈME DOIT refuser la modification ou l'annulation par le réservant et l'inviter à contacter le site. _Source : B08-D6_
3. QUAND une réservation est annulée, LE SYSTÈME DOIT libérer ses créneaux immédiatement. _Source : B08-D6_

### Exigence 6 : confirmation et rappel par e-mail

**User story :** En tant que transporteur, je veux recevoir une confirmation puis un rappel, afin de ne pas oublier mon créneau.

#### Critères d'acceptation

1. QUAND une réservation est créée ou modifiée, LE SYSTÈME DOIT envoyer une confirmation par e-mail à l'adresse du transporteur enregistrée dans la réservation. _Source : B08-D10_
2. LE SYSTÈME DOIT envoyer un rappel par e-mail la veille du créneau, à une heure paramétrable par site. _Source : B08-D10_
3. QUAND la réservation est faite par un fournisseur, LE SYSTÈME DOIT envoyer la confirmation et le rappel à l'adresse de transporteur saisie, avec copie au compte réservant. _Source : B08-D10_
4. QUAND le chef de quai déplace ou annule une réservation, LE SYSTÈME DOIT en informer le transporteur par e-mail. _Source : B08-D11_
5. LE SYSTÈME DOIT limiter les e-mails aux informations de service (site, date, heure, quai, numéro de réservation, commandes) et DOIT les rédiger dans la langue du compte du destinataire. _Source : CT-03, B08-D21, CT-11_

### Exigence 7 : actions du chef de quai

**User story :** En tant que chef de quai, je veux garder la main sur le planning, afin de gérer les imprévus.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au chef de quai de déplacer une réservation sur un autre créneau ou un autre quai de son site. _Source : B08-D11_
2. LE SYSTÈME DOIT permettre au chef de quai de forcer une réservation en dérogeant aux bornes de réservation, avec un motif obligatoire. _Source : B08-D11_
3. LE SYSTÈME DOIT permettre au chef de quai de bloquer des créneaux, ponctuellement ou de façon récurrente, avec un motif. _Source : B08-D11, B08-D22, H22_
4. SI un créneau à bloquer porte une réservation, ALORS LE SYSTÈME DOIT refuser le blocage tant que la réservation n'a pas été déplacée ou annulée. _Source : B08-D11_
5. LE SYSTÈME DOIT journaliser chaque action du chef de quai avec son auteur, sa date et son motif. _Source : B08-D11, CT-01_

### Exigence 8 : vue planning par site

**User story :** En tant que chef de quai ou membre du bureau de réception, je veux voir le planning de mon site, afin de connaître la charge dès la veille.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher le planning d'un site par jour et par quai : réservations, créneaux libres, créneaux bloqués et statut de chaque réservation. _Source : B08-D16_
2. LE SYSTÈME DOIT afficher pour le lendemain le nombre de camions attendus. _Source : B08-D16_
3. LE SYSTÈME DOIT permettre de saisir le début et la fin du déchargement de chaque camion, pour calculer l'attente et l'occupation. _Source : B08-D13, B08-D14_

### Exigence 9 : pointage au poste de garde

**User story :** En tant qu'agent du poste de garde, je veux pointer chaque camion à son arrivée, afin d'appliquer le retard toléré et de mesurer les arrivées sans rendez-vous.

#### Critères d'acceptation

1. QUAND un camion arrive, LE SYSTÈME DOIT permettre au poste de garde de retrouver sa réservation et d'enregistrer l'heure d'arrivée. _Source : B08-D8, B08-D25_
2. SI le camion arrive plus de 20 minutes après le début de son créneau, ALORS LE SYSTÈME DOIT passer le créneau au statut « perdu » et libérer les créneaux de la réservation. _Source : B08-D9_
3. QUAND un camion sans réservation se présente, LE SYSTÈME DOIT enregistrer son arrivée avec le fournisseur ou le transporteur déclaré, pour l'indicateur des camions sans rendez-vous. _Source : B08-D12_
4. LE SYSTÈME DOIT afficher au chef de quai les camions arrivés après la tolérance ou sans réservation, afin qu'il décide de leur affectation. _Source : B08-D9, B08-D11_
5. LE SYSTÈME DOIT livrer les fonctions du poste de garde (critères 9.1 à 9.4) dans le lot V1. _Source : B08-D25_

### Exigence 10 : indicateurs et export

**User story :** En tant que responsable de l'approvisionnement, je veux suivre les indicateurs de réception, afin de mesurer l'effet du portail.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer, par site, la part des camions qui se présentent sans rendez-vous. _Source : B08-D12_
2. LE SYSTÈME DOIT calculer, par site, l'attente moyenne des camions. _Source : B08-D13_
3. LE SYSTÈME DOIT calculer, par site, le taux d'occupation des quais. _Source : B08-D14_
4. LE SYSTÈME DOIT calculer la ponctualité par fournisseur, à partir des heures d'arrivée prévues et réelles enregistrées. _Source : B08-D15, H23_
5. LE SYSTÈME DOIT permettre l'export des indicateurs, par site et par période choisie, au format CSV. _Source : B08-D17_
6. LE SYSTÈME NE DOIT PAS produire de notation ni de pénalité des fournisseurs en V1. _Source : H23_

### Exigence 11 : exigences non fonctionnelles

**User story :** En tant que DSI, je veux une solution conforme et extensible, afin de l'ouvrir à des tiers sans risque.

#### Critères d'acceptation

1. LE SYSTÈME DOIT absorber au moins le volume actuel de E1 (environ 70 camions par jour) et de E2 (une quarantaine) sans dégradation des temps de réponse. _Source : B08-D1, B08-D26_
2. LE SYSTÈME DOIT être hébergé dans l'Union européenne, dans le cloud d'Orvanne sous réserve de la réponse à Q34. _Source : CT-08_
3. LE SYSTÈME DOIT conserver les heures d'arrivée prévues et réelles, pour constituer l'historique nécessaire à la future notation des fournisseurs. _Source : H23_
4. LE SYSTÈME DOIT journaliser les connexions et les modifications des comptes et des paramétrages. _Source : CT-01_
5. LE SYSTÈME NE DOIT PAS utiliser de données de production pour les démonstrations et les tests sans anonymisation. _Source : CT-04_
6. LE SYSTÈME NE DOIT PAS être mis en production entre le 16/11 et le 11/01. _Source : CT-07_

## Hors périmètre

- Notation des fournisseurs par la ponctualité (`B08-D18`) : V2. Les heures prévues et réelles sont conservées pour la préparer (critère 11.3, H23).
- Pénalités des fournisseurs (`B08-D19`) : idée « à terme », non décidée ; pas de base contractuelle (H23).
- Lien avec Hangar pour préremplir la réception attendue (`B08-D23`) et application mobile pour les chauffeurs (`B08-D24`) : V2.
- Réservation par les messageries et petits colis sans commande d'achat (`B08-D22`) : reportée (H22). Le chef de quai bloque un quai sur une plage fixe (critère 7.3).
- Actions de projet : liste d'une vingtaine de fournisseurs pilotes (`B08-D28`), chiffrage et planning de la DSI (`B08-D29`), démarrage du pilote sur E1 au printemps (`B08-D30`). Ce sont des prérequis et des échéances, repris dans `tasks.md`, pas des exigences du système.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H20 | La durée de créneau est un paramètre par site, ajouté aux paramètres de R4, avec 30 minutes par défaut (R2). Chaque site fixe sa valeur lors du paramétrage ; un camion complet consomme deux créneaux. | C21 | oui |
| H21 | Le nombre de quais est saisi par site (R4) ; la valeur de E1 est celle que le chef de quai fournira pour le 04/12. | C22 | oui |
| H22 | R1 s'applique en V1 : toute réservation exige une commande d'achat. Pour les messageries et petits colis sans commande, le chef de quai bloque un quai sur une plage fixe (R7). Leur prise en charge dans le portail est reportée. | C23 | oui |
| H23 | La V1 enregistre les heures prévues et réelles d'arrivée, qui alimentent l'indicateur de ponctualité. La notation des fournisseurs est en V2 ; les pénalités restent hors périmètre tant qu'elles ne sont pas décidées. | C24 | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q21 | La durée de créneau peut-elle être fixée par site ? Quelle valeur pour E1 (30 minutes ou une heure) et pour E2 ? | Grégory Thibaudeau ; Rémi Vasseur ; Karim Benhaddou | non |
| Q22 | E1 a 6 quais de réception aujourd'hui, le paramétrage cible en indique 4 : pourquoi cet écart ? | Rémi Vasseur | non |
| Q23 | Les messageries et petits colis sans commande d'achat entrent-ils dans le périmètre ? Un quai réservé sur une plage fixe suffit-il en V1 ? | Grégory Thibaudeau ; Rémi Vasseur | non |
| Q24 | À partir de quand la ponctualité alimente-t-elle la notation des fournisseurs ? Les pénalités sont-elles envisagées, et sur quelle base contractuelle ? | Nadège Courtois ; Grégory Thibaudeau | non |
| Q27 | Dans quelles langues proposer le portail fournisseurs et l'espace vendeur (anglais, allemand, espagnol) ? Pour quelle version ? | Grégory Thibaudeau ; direction marketplace | non (critère 1.4 : langues ajoutables) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne (B01) s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis (B03, B07-D20) ? | DSI (comité d'architecture) | non (critère 11.2) |
| Q35 | La conformité RGAA s'applique-t-elle au portail fournisseurs et à l'espace vendeur ? | DSI (comité d'architecture) | non (critère 1.5) |
| Q36 | Quand pouvez-vous examiner les traitements des projets P01, P02, P03, P04, P06 et P07 (CT-01) ? Lesquels exigent une analyse d'impact ? | Hélène Marsac | non (mise en production) |
| Q38 | L'entrepôt E3 entre-t-il dans le périmètre de la prise de rendez-vous ? | Grégory Thibaudeau | non |
