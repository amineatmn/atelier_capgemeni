# Exigences : prise de rendez-vous des livraisons fournisseurs

<!-- Projet P06, slug rdv-livraisons-fournisseurs. Commanditaire : approvisionnement et transport amont (Grégory Thibaudeau).
     Parties prenantes : achats, exploitation E1 et E2, DSI, DPO. Source : B08. IDs provisoires : templates/exemple-p06/ids-provisoires.md. -->

## Introduction

Les fournisseurs et leurs transporteurs prennent rendez-vous par téléphone ou par e-mail. Les créneaux sont notés dans un tableur propre à chaque site. E1 reçoit environ 70 camions par jour et E2 une quarantaine. Un camion sur quatre se présente sans rendez-vous ou hors créneau. L'attente moyenne dépasse 1 h 30 le lundi matin, et les transporteurs facturent des pénalités d'immobilisation. Le bureau de réception passe environ 3 heures par jour au téléphone, et personne ne connaît la veille la charge du lendemain.

Le projet livre un portail web de réservation des créneaux de déchargement, avec une vue planning par site, le pointage au poste de garde et l'export des indicateurs. Le pilote démarre sur E1 au printemps, avec une vingtaine de fournisseurs. La notation des fournisseurs, le lien avec Hangar et l'application chauffeur relèvent de la V2.

## Glossaire

- **Créneau** : plage de déchargement sur un quai, de durée paramétrable par site (30 minutes par défaut).
- **Réservation** : engagement d'un fournisseur ou d'un transporteur à livrer une ou plusieurs commandes d'achat sur un créneau.
- **Commande d'achat** : commande passée par Orvanne à un fournisseur, lue dans Passerelle ; « soldée » signifie entièrement livrée ou close.
- **Camion complet** : camion déclaré comme tel à la réservation ; il consomme deux créneaux consécutifs.
- **Pointage** : enregistrement de l'arrivée d'un camion par le poste de garde.
- **Réservation perdue** : réservation dont le camion arrive après la tolérance de retard.

## Exigences

### Exigence 1 : comptes et accès des fournisseurs et des transporteurs

**User story :** En tant que responsable de l'approvisionnement, je veux contrôler qui peut réserver, afin que seuls les fournisseurs habilités et leurs transporteurs accèdent au portail.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à l'approvisionnement de créer, suspendre et désactiver les comptes des fournisseurs. _Source : B08-D1, H14_
2. LE SYSTÈME DOIT permettre à un fournisseur de rattacher et de détacher ses transporteurs. _Source : B08-D1, H14_
3. LE SYSTÈME DOIT limiter un transporteur aux commandes d'achat des fournisseurs qui l'ont rattaché. _Source : B08-D2, H14_
4. LE SYSTÈME DOIT proposer le portail et les e-mails en français et en anglais, selon la langue choisie pour le compte. _Source : B08-D19, H09_
5. LE SYSTÈME DOIT exiger une authentification individuelle pour tout accès au portail. _Source : B08-D1, CT-01_

### Exigence 2 : paramétrage des sites

**User story :** En tant que chef de quai, je veux paramétrer mon site, afin que les créneaux proposés correspondent à mes quais et à mes horaires.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre de paramétrer, pour chaque site, les quais ouverts à la réservation, les horaires d'ouverture par jour de la semaine et les jours fermés. _Source : B08-D7, H02_
2. LE SYSTÈME DOIT permettre de paramétrer la durée des créneaux par site, avec 30 minutes par défaut. _Source : B08-D3, B08-D18, B08-D27, H01_
3. LE SYSTÈME DOIT permettre de paramétrer par site les bornes de réservation, avec J-10 pour l'ouverture et J-1 à 12 h 00, heure de Paris, pour la clôture par défaut. _Source : B08-D5, H06_
4. QUAND un paramétrage est saisi, LE SYSTÈME DOIT afficher la capacité qui en résulte : créneaux par jour, par quai et pour le site. _Source : B08-D27, H18_
5. SI une modification de paramétrage rend impossibles des réservations existantes, ALORS LE SYSTÈME DOIT les lister et refuser la modification tant qu'elles n'ont pas été déplacées ou annulées. _Source : B08-D7, H23_

### Exigence 3 : réservation d'un créneau

**User story :** En tant que fournisseur ou transporteur, je veux réserver moi-même un créneau de déchargement, afin de ne plus téléphoner au bureau de réception.

#### Critères d'acceptation

1. QUAND un réservant choisit un site, une date et des commandes d'achat, LE SYSTÈME DOIT afficher les créneaux disponibles. _Source : B08-D1_
2. LE SYSTÈME DOIT exiger au moins un numéro de commande d'achat par réservation, et en accepter plusieurs. _Source : B08-D2_
3. LE SYSTÈME DOIT demander si le camion est complet et, si c'est le cas, réserver deux créneaux consécutifs sur le même quai. _Source : B08-D4, H07_
4. SI la date demandée est hors des bornes de réservation du site, ALORS LE SYSTÈME DOIT refuser la réservation en indiquant les bornes. _Source : B08-D5, H06_
5. QUAND une réservation est validée, LE SYSTÈME DOIT lui attribuer un quai libre et un numéro de réservation. _Source : B08-D1, H15_
6. LE SYSTÈME DOIT empêcher deux réservations sur le même créneau du même quai, y compris quand deux réservants valident au même moment. _Source : B08-D1_
7. LE SYSTÈME DOIT enregistrer l'adresse e-mail du transporteur dans chaque réservation. _Source : B08-D10, H08_

### Exigence 4 : contrôle des commandes d'achat

**User story :** En tant qu'acheteur, je veux que seules des commandes valides soient livrées, afin d'éviter les camions qu'on ne sait pas réceptionner.

#### Critères d'acceptation

1. QUAND un numéro de commande d'achat est saisi, LE SYSTÈME DOIT vérifier dans Passerelle qu'il existe, qu'il n'est pas soldé et qu'il appartient à un fournisseur rattaché au réservant. _Source : B08-D2, H22_
2. OÙ Passerelle fournit le site de livraison de la commande, LE SYSTÈME DOIT refuser une réservation sur un autre site. _Source : B08-D2, H22_
3. LE SYSTÈME DOIT accepter une même commande d'achat dans plusieurs réservations (livraisons partielles). _Source : B08-D2, H22_
4. SI Passerelle ne répond pas, ALORS LE SYSTÈME DOIT contrôler la commande sur la dernière copie connue, marquer la réservation « commande à revérifier » et la contrôler de nouveau dès le retour du service. _Source : B08-D2, H16_
5. QUAND une commande d'une réservation à venir devient soldée ou annulée, LE SYSTÈME DOIT alerter le chef de quai et le réservant, sans annuler la réservation. _Source : B08-D2, H24_

### Exigence 5 : modification et annulation

**User story :** En tant que réservant, je veux modifier ou annuler ma réservation, afin de libérer le créneau si mes plans changent.

#### Critères d'acceptation

1. PENDANT QUE la clôture du site n'est pas atteinte, LE SYSTÈME DOIT permettre au réservant de modifier le créneau, les commandes ou la déclaration « camion complet », et d'annuler sa réservation. _Source : B08-D6, H06_
2. SI la clôture est atteinte, ALORS LE SYSTÈME DOIT refuser la modification ou l'annulation par le réservant et l'inviter à contacter le site. _Source : B08-D6_
3. QUAND une réservation est annulée, LE SYSTÈME DOIT libérer immédiatement ses créneaux. _Source : B08-D6_

### Exigence 6 : confirmation et rappel par e-mail

**User story :** En tant que transporteur, je veux recevoir une confirmation puis un rappel, afin de ne pas oublier mon créneau.

#### Critères d'acceptation

1. QUAND une réservation est créée ou modifiée, LE SYSTÈME DOIT envoyer une confirmation par e-mail au transporteur dans les 5 minutes, avec copie au compte réservant s'il est différent. _Source : B08-D10, H08, H21_
2. LE SYSTÈME DOIT envoyer un rappel par e-mail au transporteur la veille du créneau, à 8 h 00 par défaut (heure paramétrable). _Source : B08-D10, H08_
3. QUAND le chef de quai force, déplace ou annule une réservation, LE SYSTÈME DOIT en informer le transporteur par e-mail. _Source : B08-D11, H11_
4. LE SYSTÈME DOIT limiter le contenu des e-mails aux informations de service : site, adresse, date, heure, quai, numéro de réservation, commandes, consignes d'accès. _Source : B08-D10, CT-03_

### Exigence 7 : actions du chef de quai

**User story :** En tant que chef de quai, je veux garder la main sur le planning, afin de gérer les imprévus.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au chef de quai de déplacer une réservation sur un autre créneau ou un autre quai de son site. _Source : B08-D11_
2. LE SYSTÈME DOIT permettre au chef de quai de forcer une réservation en dérogeant aux bornes de réservation et à la tolérance de retard, avec un motif obligatoire. _Source : B08-D11, H11_
3. LE SYSTÈME DOIT permettre au chef de quai de bloquer des créneaux, ponctuellement ou de façon récurrente, avec un motif dont « messagerie ». _Source : B08-D11, B08-D20, H03_
4. SI un créneau à bloquer porte une réservation, ALORS LE SYSTÈME DOIT refuser le blocage tant que la réservation n'a pas été déplacée ou annulée. _Source : B08-D11, H11_
5. LE SYSTÈME DOIT journaliser chaque action du chef de quai avec son auteur, sa date et son motif. _Source : B08-D11, CT-01_

### Exigence 8 : vue planning par site

**User story :** En tant que chef de quai ou bureau de réception, je veux voir le planning de mon site, afin de connaître la charge dès la veille.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher le planning d'un site par jour et par quai : réservations, créneaux libres, créneaux bloqués, et statut de chaque réservation. _Source : B08-D22, B08-D32_
2. LE SYSTÈME DOIT afficher pour le lendemain le nombre de camions attendus et le taux de remplissage des créneaux. _Source : B08-D32_
3. LE SYSTÈME DOIT mettre à jour la vue planning au plus tard 60 secondes après tout enregistrement. _Source : B08-D22, H21_
4. LE SYSTÈME DOIT permettre au quai de saisir le début et la fin du déchargement de chaque camion. _Source : B08-D13, B08-D14, H13_

### Exigence 9 : pointage au poste de garde

**User story :** En tant qu'agent du poste de garde, je veux pointer chaque camion à son arrivée, afin d'appliquer la tolérance de retard et de mesurer les arrivées sans rendez-vous.

#### Critères d'acceptation

1. QUAND un camion arrive, LE SYSTÈME DOIT permettre au poste de garde de retrouver la réservation par son numéro, une commande d'achat ou le nom du fournisseur, et d'enregistrer l'heure d'arrivée. _Source : B08-D8, B08-D25, H05_
2. SI le camion arrive plus de 20 minutes après le début de son créneau, ALORS LE SYSTÈME DOIT passer la réservation au statut « perdue », libérer ses créneaux et enregistrer l'arrivée hors créneau. _Source : B08-D9, H10_
3. QUAND un camion sans réservation se présente, LE SYSTÈME DOIT enregistrer son arrivée avec le fournisseur ou le transporteur déclaré et une catégorie (sans rendez-vous, messagerie). _Source : B08-D12, B08-D20, H03, H19_
4. LE SYSTÈME DOIT afficher au chef de quai les camions arrivés hors créneau ou sans réservation, pour qu'il les affecte s'il le souhaite. _Source : B08-D9, H10_
5. LE SYSTÈME NE DOIT PAS collecter de donnée sur le chauffeur (nom, immatriculation). _Source : CT-01, H19_

### Exigence 10 : indicateurs et export

**User story :** En tant que responsable de l'approvisionnement, je veux suivre les indicateurs de réception, afin de mesurer l'effet du portail.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer chaque nuit, par site, par jour et par demi-journée : la part des camions sans rendez-vous, l'attente moyenne et le taux d'occupation des quais, selon les définitions de H12. _Source : B08-D12, B08-D13, B08-D14, H12, H20_
2. LE SYSTÈME DOIT calculer la ponctualité par fournisseur selon la définition de H12. _Source : B08-D15, H12_
3. LE SYSTÈME DOIT mettre à disposition les indicateurs de la veille à 6 h 00. _Source : B08-D23, H20_
4. LE SYSTÈME DOIT permettre l'export CSV des indicateurs pour un site ou tous les sites, sur une période choisie. _Source : B08-D23, H20_
5. LE SYSTÈME NE DOIT PAS produire de notation ni de pénalité des fournisseurs en V1. _Source : B08-D31, H04_

### Exigence 11 : exigences non fonctionnelles

**User story :** En tant que DSI, je veux une solution fiable, ouverte aux tiers en sécurité et conforme au RGPD, afin de pouvoir l'étendre à tous les sites.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher les créneaux disponibles en moins de 2 secondes pour 95 % des recherches, pour le double des volumes actuels de E1 et E2 (environ 220 camions par jour). _Source : B08-D1, H17_
2. LE SYSTÈME DOIT être disponible 7 jours sur 7, à 99,5 % par mois hors maintenance programmée. _Source : B08-D5, H21_
3. LE SYSTÈME DOIT être hébergé dans le cloud d'Orvanne, dans l'Union européenne. _Source : CT-08_
4. LE SYSTÈME DOIT conserver les réservations et les pointages au moins 13 mois, puis les supprimer selon la durée fixée avec la DPO. _Source : B08-D31, H04, CT-01_
5. LE SYSTÈME DOIT journaliser les connexions et les actions sur les comptes et les paramétrages. _Source : CT-01_

## Hors périmètre

- Notation des fournisseurs par la ponctualité (`B08-D16`) : V2. Les données sont conservées pour la préparer (critère 11.4).
- Pénalités des fournisseurs (`B08-D17`) : idée « à terme », non spécifiée.
- Lien avec Hangar pour préremplir la réception (`B08-D21`) et application mobile pour les chauffeurs (`B08-D24`) : V2.
- Réservation par les messageries et petits colis sans commande d'achat (`B08-D20`) : non retenue tant que C03 n'est pas arbitré. Les créneaux bloqués et le pointage par catégorie (critères 7.3 et 9.3) mesurent le phénomène.
- Actions de projet (`B08-D26`, `B08-D28`, `B08-D29`) : liste des fournisseurs pilotes, vérification de Passerelle, chiffrage. Ce sont des prérequis, repris dans `tasks.md`, pas des exigences du système.
- Démarrage du pilote sur E1 au printemps (`B08-D30`) : échéance, reprise dans l'introduction et dans `tasks.md`.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H01 | La durée du créneau est un paramètre de site, 30 minutes par défaut ; un camion complet consomme deux créneaux. | C01 | oui |
| H02 | Le nombre de quais ouverts à la réservation est un paramètre de site. | C02 | oui |
| H03 | Les messageries ne réservent pas ; le chef de quai bloque des créneaux « messagerie » et le poste de garde pointe leurs arrivées à part. | C03 | oui |
| H04 | Pas de notation ni de pénalité en V1 ; l'historique est conservé au moins 13 mois. | C04 | oui |
| H05 | Le pointage au poste de garde fait partie du pilote. | C05 | oui |
| H06 | J-10 et J-1 en jours calendaires, « midi » = 12 h 00 heure de Paris ; bornes paramétrables. | — | oui |
| H07 | Le réservant déclare si le camion est complet ; le chef de quai peut corriger. | — | oui |
| H08 | E-mails au transporteur de la réservation, copie au réservant ; rappel la veille à 8 h 00. | — | oui |
| H09 | Portail et e-mails en français et en anglais. | — | oui |
| H10 | Au-delà de 20 minutes, la réservation est perdue, ses créneaux sont libérés et le chef de quai peut forcer le camion sur un créneau libre. | — | oui |
| H11 | « Forcer » = déroger aux bornes et à la tolérance avec un motif ; un créneau réservé ne se bloque qu'après déplacement ou annulation ; le transporteur est prévenu de chaque action. | — | oui |
| H12 | Définitions des indicateurs : sans rendez-vous = arrivées sans réservation valide / arrivées pointées ; attente = début du déchargement − max(arrivée, début du créneau) ; occupation = créneaux consommés par des camions déchargés / créneaux ouverts ; ponctualité = réservations pointées dans la tolérance / réservations non annulées. | — | oui |
| H13 | Le quai saisit le début et la fin du déchargement dans la vue planning. | — | oui |
| H14 | L'approvisionnement crée les comptes fournisseurs ; un fournisseur rattache ses transporteurs. | — | oui |
| H15 | Le système attribue le quai ; le chef de quai peut déplacer. | — | oui |
| H16 | En cas de panne de Passerelle, contrôle sur la dernière copie et nouvelle vérification au retour du service. | — | oui |
| H17 | Dimensionnement pour le double des volumes actuels ; recherche de créneaux en moins de 2 secondes. | — | oui |
| H18 | Le paramétrage de E1 est saisi tel que fourni ; l'écran affiche la capacité qui en résulte. | C06 | oui |
| H19 | Aucune donnée sur le chauffeur n'est collectée en V1. | — | oui |
| H20 | Indicateurs calculés chaque nuit, disponibles à 6 h 00, export CSV par site et par période, ventilés par jour et demi-journée. | — | oui |
| H21 | Confirmation sous 5 minutes, planning à jour sous 60 secondes, disponibilité 7 j/7 à 99,5 % par mois. | — | oui |
| H22 | Commande acceptée si elle existe, n'est pas soldée et appartient à un fournisseur rattaché ; contrôle du site si Passerelle le fournit ; livraisons partielles admises. | — | oui |
| H23 | Une modification de paramétrage qui touche des réservations est refusée tant qu'elles ne sont pas déplacées ou annulées. | — | oui |
| H24 | Une commande devenue soldée ou annulée déclenche une alerte, pas une annulation automatique. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q01 | Quelle durée de créneau par site : 30 minutes (R2) ou 1 heure (E2, paramétrage cible de E1) ? | Grégory Thibaudeau, Rémi Vasseur, Karim Benhaddou | non |
| Q02 | E1 ouvre-t-il 6 ou 4 quais à la réservation ? | Rémi Vasseur | non |
| Q03 | Les messageries et petits colis sans commande d'achat sont-ils dans le périmètre ? | Grégory Thibaudeau | non |
| Q04 | Quelle durée d'historique conserver pour la future notation ? | Grégory Thibaudeau, Nadège Courtois | non |
| Q05 | Le pointage au poste de garde est-il ferme dans le pilote ? Le poste de garde de E1 est-il équipé ? | Grégory Thibaudeau, Inès Rouvière | oui (exigence 9) |
| Q06 | Passerelle expose-t-elle les commandes d'achat avec numéro, fournisseur, site et statut, et avec quel délai ? | Inès Rouvière, équipe Passerelle | oui (exigence 4) |
| Q07 | Que signifie « forcer » un créneau ? Que devient un camion dont le créneau est perdu ? | Rémi Vasseur | non |
| Q08 | Comment calculer l'attente moyenne ? Correspond-elle à la base des pénalités d'immobilisation ? | Grégory Thibaudeau | non |
| Q09 | Comment reconnaît-on un camion complet ? | Rémi Vasseur, Grégory Thibaudeau | non |
| Q10 | Horaires et jours fermés de E1 et E2 ; J-1 calendaire ou ouvré ; E3 est-il concerné ? | Rémi Vasseur, Karim Benhaddou, Grégory Thibaudeau | non |
| Q11 | Quand le fournisseur réserve, qui reçoit la confirmation et le rappel, et à quelle heure ? | Grégory Thibaudeau | non |
| Q12 | Quelles langues proposer en plus du français ? | Nadège Courtois | non |
| Q13 | Quelle base légale et quelles durées de conservation pour les contacts, les réservations et le journal ? | DPO | oui (mise en service) |
| Q14 | Qui crée et désactive les comptes des fournisseurs et des transporteurs ? | Grégory Thibaudeau, Nadège Courtois | non |
| Q15 | Quels objectifs chiffrés pour les indicateurs ? | Grégory Thibaudeau | non |
| Q16 | Avec 4 quais et des créneaux d'une heure, quels horaires permettent de recevoir 70 camions par jour à E1 ? | Rémi Vasseur, Grégory Thibaudeau | non |
| Q17 | Quel service d'envoi pour les e-mails vers des destinataires externes ? | Inès Rouvière | non |
