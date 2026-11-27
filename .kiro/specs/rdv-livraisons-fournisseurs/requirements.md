# Exigences : prise de rendez-vous de déchargement par les fournisseurs et transporteurs

<!-- Projet P06, slug rdv-livraisons-fournisseurs. Commanditaire : approvisionnement et transport amont.
     Parties prenantes : exploitation E1 (chef de quai), exploitation E2, achats, DSI, poste de garde, DPO.
     Source unique : B08 (compte rendu d'atelier du 12/11/2026). Conflits : C21, C22, C23, C24. -->

## Introduction

Les fournisseurs d'Orvanne et leurs transporteurs prennent aujourd'hui rendez-vous par téléphone ou par e-mail auprès du bureau de réception de chaque site, qui note les créneaux dans un tableur propre au site. E1 reçoit environ 70 camions par jour sur 6 quais de réception, E2 une quarantaine. Un camion sur quatre se présente sans rendez-vous ou hors créneau. L'attente moyenne dépasse 1 h 30 le lundi matin, avec des pénalités d'immobilisation facturées par les transporteurs. Le bureau de réception passe environ 3 heures par jour au téléphone, et personne ne voit la veille la charge du lendemain.

L'atelier a retenu un portail web de réservation des créneaux de déchargement, régi par sept règles (R1 à R7), avec une vue planning par site, le pointage des camions au poste de garde et un export des indicateurs.

Le projet est découpé en deux versions :
- **V1** (exigences 1 à 11) : règles R1 à R7, vue planning, poste de garde, indicateurs et export. Pilote sur E1 au printemps, avec une vingtaine de fournisseurs pilotes. L'année n'est pas écrite dans B08 ; l'atelier datant du 12/11/2026, le pilote est compris comme celui du printemps 2027.
- **V2** (hors de cette spec, voir « Hors périmètre ») : notation des fournisseurs, lien avec Hangar, application mobile pour les chauffeurs.

Jalons connus : liste des fournisseurs pilotes et vérification des commandes d'achat dans Passerelle pour le 27/11, paramétrage cible de E1 pour le 04/12, chiffrage et planning de la DSI en décembre. Le gel des mises en production du 16 novembre au 11 janvier (`CT-07`) ne touche pas le pilote du printemps ; il interdit en revanche toute mise en production anticipée pendant cette période.

## Glossaire

- **Site** : entrepôt de réception (E1, E2 ; E3 non évoqué dans B08, voir `Q38`).
- **Quai** : quai de réception d'un site, sur lequel un camion décharge.
- **Créneau** : plage horaire de déchargement sur un quai, de durée fixée par site (30 minutes par défaut).
- **Réservation** : rendez-vous de déchargement pris sur un ou plusieurs créneaux consécutifs d'un même quai, pour une ou plusieurs commandes d'achat.
- **Commande d'achat** : commande passée par Orvanne à un fournisseur, identifiée par un numéro ; elle est « soldée » quand il ne reste rien à livrer.
- **Camion complet** : livraison déclarée comme telle par l'auteur de la réservation ; elle consomme deux créneaux (R2).
- **Jour J** : jour du créneau réservé. « J-1 midi » désigne 12 h 00, heure de Paris, la veille du jour J.
- **Pointage** : enregistrement de l'arrivée d'un camion par le poste de garde.
- **Créneau perdu** : réservation dont le camion n'a pas été pointé dans les 20 minutes suivant le début du créneau (R5).
- **Forçage** : action du chef de quai qui crée ou maintient une réservation en dehors des règles de capacité ou de délai (R7).
- **Blocage** : action du chef de quai qui rend un créneau ou un quai non réservable (R7).
- **Utilisateur externe** : contact d'un fournisseur ou d'un transporteur disposant d'un compte sur le portail.

## Exigences

### Exigence 1 : accès au portail fournisseurs

**User story :** En tant que fournisseur ou transporteur, je veux réserver moi-même un créneau de déchargement sur un portail web, afin de ne plus appeler le bureau de réception.

#### Critères d'acceptation

1. LE SYSTÈME DOIT proposer un portail web sur lequel un fournisseur ou son transporteur réserve un créneau de déchargement sur un site d'Orvanne. _Source : B08-D1_
2. LE SYSTÈME DOIT réserver l'accès au portail aux comptes nominatifs ouverts par Orvanne pour des contacts de fournisseurs et de transporteurs. _Source : B08-D1, CT-01_
3. PENDANT QUE le pilote est en cours, LE SYSTÈME DOIT n'ouvrir de compte qu'aux fournisseurs de la liste pilote établie par les achats (une vingtaine) et à leurs transporteurs. _Source : B08-D28, B08-D30_
4. LE SYSTÈME DOIT limiter chaque compte externe aux commandes d'achat et aux réservations des fournisseurs auxquels il est rattaché. _Source : B08-D2, CT-01_
5. LE SYSTÈME DOIT présenter les écrans du portail de façon utilisable sur un smartphone et conforme au RGAA. _Source : CT-09_

### Exigence 2 : paramétrage des sites

**User story :** En tant que responsable de site, je veux paramétrer mes quais, mes horaires, mes jours fermés et la durée de mes créneaux, afin que les réservations correspondent à la capacité réelle de mon site.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à chaque site de paramétrer ses quais de réception, ses horaires d'ouverture et ses jours fermés. _Source : B08-D7_
2. LE SYSTÈME DOIT permettre à chaque site de paramétrer la durée de ses créneaux, avec une valeur par défaut de 30 minutes. _Source : B08-D3, B08-D20, H20_
3. LE SYSTÈME DOIT générer les créneaux réservables de chaque jour ouvert d'un site à partir de ses horaires d'ouverture et de sa durée de créneau, avec une capacité égale au nombre de quais actifs. _Source : B08-D3, B08-D7_
4. SI une modification du paramétrage d'un site (quais, horaires, jours fermés, durée de créneau) rend incompatibles des réservations existantes, ALORS LE SYSTÈME DOIT refuser la modification et lister les réservations à déplacer ou à annuler au préalable. _Source : B08-D7, B08-D11_
5. LE SYSTÈME DOIT accepter, sans développement, le paramétrage cible de E1 fourni par le chef de quai E1, soit 4 quais de réception et des créneaux d'une heure selon le compte rendu du 12/11, valeurs à confirmer. _Source : B08-D26, H20, H21_
6. LE SYSTÈME DOIT permettre d'ouvrir la réservation site par site, E1 étant le premier site ouvert pour le pilote. _Source : B08-D30, B08-D7_

### Exigence 3 : réservation d'un créneau

**User story :** En tant que fournisseur ou transporteur, je veux réserver un créneau pour les commandes d'achat que je livre, afin d'être déchargé à l'heure prévue.

#### Critères d'acceptation

1. QUAND un utilisateur externe crée une réservation, LE SYSTÈME DOIT exiger au moins un numéro de commande d'achat Orvanne et permettre d'en saisir plusieurs. _Source : B08-D2_
2. LE SYSTÈME DOIT vérifier que chaque commande d'achat saisie est valide et non soldée, à partir des commandes d'achat transmises par Passerelle. _Source : B08-D2, B08-D27_
3. SI une commande d'achat saisie est inconnue, non rattachée au compte ou soldée, ALORS LE SYSTÈME DOIT refuser la réservation en indiquant la commande en cause et l'un des deux motifs « inconnue ou non rattachée à votre compte » ou « soldée ». _Source : B08-D2, CT-01_
4. LE SYSTÈME DOIT demander à l'auteur de la réservation s'il s'agit d'un camion complet, puis réserver deux créneaux consécutifs sur le même quai pour un camion complet et un seul créneau dans les autres cas. _Source : B08-D4_
5. LE SYSTÈME DOIT n'accepter une réservation d'un utilisateur externe que si elle est faite entre J-10 et J-1 à 12 h 00, heure de Paris. _Source : B08-D5_
6. LE SYSTÈME DOIT proposer uniquement les créneaux d'un jour ouvert du site sur lesquels un quai est libre pendant toute la durée demandée. _Source : B08-D3, B08-D7_
7. SI deux réservations visent en même temps le dernier quai libre d'un créneau, ALORS LE SYSTÈME DOIT n'en enregistrer qu'une et proposer d'autres créneaux à l'autre utilisateur. _Source : B08-D7, B08-D3_
8. QUAND une réservation est enregistrée, LE SYSTÈME DOIT lui attribuer un numéro de réservation unique et un quai. _Source : B08-D1, B08-D16_
9. LE SYSTÈME DOIT exiger dans chaque réservation l'adresse e-mail du transporteur qui effectue la livraison. _Source : B08-D10_

### Exigence 4 : modification et annulation par l'utilisateur externe

**User story :** En tant que fournisseur ou transporteur, je veux modifier ou annuler ma réservation, afin de libérer le créneau si mon planning change.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à un utilisateur externe de modifier ou d'annuler une réservation de son périmètre jusqu'à J-1 à 12 h 00, heure de Paris. _Source : B08-D6_
2. SI un utilisateur externe demande une modification ou une annulation après J-1 à 12 h 00, ALORS LE SYSTÈME DOIT la refuser et afficher les coordonnées du site à contacter. _Source : B08-D6, B08-D11_
3. QUAND une réservation est modifiée, LE SYSTÈME DOIT appliquer de nouveau les contrôles des critères 3.2 à 3.7. _Source : B08-D6, B08-D2_
4. QUAND une réservation est annulée, LE SYSTÈME DOIT rendre ses créneaux de nouveau réservables. _Source : B08-D6_

### Exigence 5 : confirmation et rappel par e-mail

**User story :** En tant que transporteur, je veux recevoir une confirmation puis un rappel la veille, afin de me présenter au bon site, au bon quai et à la bonne heure.

#### Critères d'acceptation

1. QUAND une réservation est enregistrée, LE SYSTÈME DOIT envoyer au transporteur un e-mail de confirmation indiquant le numéro de réservation, le site, le quai, la date, l'heure, les commandes d'achat et la tolérance de retard de 20 minutes. _Source : B08-D10, B08-D9_
2. LE SYSTÈME DOIT envoyer au transporteur un e-mail de rappel la veille du créneau, à une heure paramétrable postérieure à 12 h 00. _Source : B08-D10, B08-D6_
3. QUAND une réservation est modifiée, déplacée ou annulée, LE SYSTÈME DOIT en informer le transporteur par e-mail avec les nouvelles informations. _Source : B08-D10, B08-D11_
4. QUAND l'auteur de la réservation n'est pas le transporteur, LE SYSTÈME DOIT lui adresser une copie des e-mails de confirmation, de modification et d'annulation. _Source : B08-D10, B08-D1_
5. LE SYSTÈME NE DOIT PAS insérer d'offre ni de contenu commercial dans les e-mails de confirmation, de rappel, de modification ou d'annulation. _Source : CT-03_
6. SI l'envoi d'un e-mail échoue après 3 tentatives, ALORS LE SYSTÈME DOIT signaler l'échec sur la réservation dans la vue planning du site. _Source : B08-D10, B08-D16_

### Exigence 6 : actions du chef de quai

**User story :** En tant que chef de quai, je veux forcer, déplacer ou bloquer un créneau, afin d'adapter le planning aux aléas du site.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au chef de quai de déplacer une réservation vers un autre créneau ou un autre quai de son site, y compris après J-1 à 12 h 00. _Source : B08-D11_
2. LE SYSTÈME DOIT permettre au chef de quai de forcer une réservation pour le compte d'un fournisseur, c'est-à-dire de la créer ou de la maintenir sur un créneau sans quai libre ou en dehors du délai de J-10 à J-1 à 12 h 00. _Source : B08-D11, CT-10_
3. SI le chef de quai force une réservation, ALORS LE SYSTÈME DOIT continuer d'exiger au moins une commande d'achat valide et non soldée. _Source : B08-D2, H22_
4. LE SYSTÈME DOIT permettre au chef de quai de bloquer un créneau ou un quai, ponctuellement ou sur une plage horaire récurrente, avec un motif obligatoire. _Source : B08-D11, B08-D22, H22_
5. SI le chef de quai bloque un créneau qui porte une réservation, ALORS LE SYSTÈME DOIT refuser le blocage tant que la réservation n'a pas été déplacée ou annulée. _Source : B08-D11_
6. LE SYSTÈME DOIT journaliser chaque forçage, déplacement, blocage et annulation fait par un utilisateur interne, avec son auteur, son horodatage, les valeurs avant et après, et le motif. _Source : B08-D11, CT-10_
7. LE SYSTÈME DOIT réserver les actions de forçage, de déplacement et de blocage aux utilisateurs ayant le rôle de chef de quai du site concerné. _Source : B08-D11_

### Exigence 7 : poste de garde

**User story :** En tant qu'agent du poste de garde, je veux pointer chaque camion à son arrivée, afin d'appliquer la tolérance de retard et de mesurer les arrivées sans rendez-vous.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher au poste de garde la liste des réservations du jour pour son site, triée par heure de créneau, avec une recherche par numéro de réservation ou par numéro de commande d'achat. _Source : B08-D8, B08-D25_
2. QUAND le poste de garde pointe un camion, LE SYSTÈME DOIT enregistrer l'heure d'arrivée et la rattacher à la réservation. _Source : B08-D8_
3. QUAND un camion est pointé au plus tard 20 minutes après le début de son créneau, LE SYSTÈME DOIT passer la réservation au statut « arrivé ». _Source : B08-D9_
4. QUAND 20 minutes se sont écoulées depuis le début d'un créneau réservé sans pointage du camion, LE SYSTÈME DOIT passer la réservation au statut « perdu » et rendre le quai disponible pour le chef de quai. _Source : B08-D9_
5. SI un camion est pointé sur une réservation au statut « perdu », ALORS LE SYSTÈME DOIT enregistrer son heure d'arrivée et le signaler au chef de quai, qui décide de la suite. _Source : B08-D9, B08-D11_
6. QUAND un camion se présente sans réservation, LE SYSTÈME DOIT permettre au poste de garde de l'enregistrer comme « sans rendez-vous », avec son heure d'arrivée et, s'il est connu, son fournisseur ou son transporteur. _Source : B08-D8, B08-D12_

### Exigence 8 : vue planning par site

**User story :** En tant que chef de quai ou membre de l'approvisionnement, je veux voir le planning de chaque site par quai et par créneau, afin de connaître la charge du lendemain et de suivre la journée en cours.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher, pour un site et un jour choisis, le planning par quai et par créneau avec le statut de chaque créneau : libre, réservé, bloqué, arrivé, à quai, déchargé ou perdu. _Source : B08-D16_
2. LE SYSTÈME DOIT afficher, pour chaque réservation du planning, le fournisseur, le transporteur, les commandes d'achat et l'indication de camion complet. _Source : B08-D16, B08-D2, B08-D4_
3. LE SYSTÈME DOIT permettre de consulter le planning de chacun des 10 jours à venir, avec le nombre de réservations et le taux de remplissage des créneaux du jour affiché. _Source : B08-D16, B08-D5_
4. QUAND un utilisateur ouvre ou actualise la vue planning, LE SYSTÈME DOIT afficher l'état enregistré à cet instant, pointages et actions du chef de quai compris. _Source : B08-D16_
5. QUAND le chef de quai enregistre la mise à quai puis la fin du déchargement d'un camion, LE SYSTÈME DOIT horodater chacune de ces deux étapes. _Source : B08-D13, B08-D14_
6. LE SYSTÈME DOIT réserver la vue planning aux utilisateurs internes du site (chef de quai, poste de garde, bureau de réception) et à l'approvisionnement. _Source : B08-D16, CT-01_

### Exigence 9 : indicateurs et export

**User story :** En tant que responsable de l'approvisionnement, je veux suivre les arrivées sans rendez-vous, l'attente, l'occupation des quais et la ponctualité des fournisseurs, afin de mesurer l'effet du portail et de constituer un historique.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer, par site et par jour, la part des camions sans rendez-vous, égale au nombre de camions enregistrés « sans rendez-vous » divisé par le nombre total de camions pointés. _Source : B08-D12_
2. LE SYSTÈME DOIT calculer, par site, par jour et par demi-journée, l'attente moyenne des camions, égale à la moyenne des durées entre le pointage et la mise à quai. _Source : B08-D13_
3. LE SYSTÈME DOIT calculer, par site et par jour, le taux d'occupation des quais, égal au nombre de créneaux-quais réservés divisé par le nombre de créneaux-quais ouverts, les créneaux bloqués étant comptés à part. _Source : B08-D14_
4. LE SYSTÈME DOIT calculer, par fournisseur et sur une période choisie, la ponctualité, égale à la part des réservations pointées au plus tard 20 minutes après le début du créneau, les réservations perdues comptant comme non ponctuelles. _Source : B08-D15, B08-D9_
5. LE SYSTÈME DOIT permettre d'exporter au format CSV les indicateurs des critères 9.1 à 9.4 pour un site et une période choisis. _Source : B08-D17_
6. LE SYSTÈME DOIT conserver pendant au moins 12 mois, pour chaque réservation, l'heure prévue, l'heure de pointage, l'heure de mise à quai et le fournisseur. _Source : B08-D15, B08-D18, H23_
7. LE SYSTÈME NE DOIT PAS calculer de note ni de pénalité des fournisseurs en V1. _Source : B08-D19, H23_

### Exigence 10 : langues

**User story :** En tant que fournisseur étranger sans interlocuteur francophone, je veux pouvoir utiliser le portail dans ma langue quand elle sera proposée, afin de réserver sans erreur.

#### Critères d'acceptation

1. LE SYSTÈME DOIT proposer en V1 les écrans du portail et les e-mails en français. _Source : H26_
2. LE SYSTÈME DOIT stocker tous les textes des écrans externes et des e-mails hors du code, de sorte qu'une langue s'ajoute sans développement. _Source : B08-D21, CT-11, H26_
3. OÙ plusieurs langues sont activées, LE SYSTÈME DOIT afficher le portail et envoyer les e-mails dans la langue choisie dans le compte de l'utilisateur externe. _Source : B08-D21, CT-11_

### Exigence 11 : hébergement, données personnelles et données de test

**User story :** En tant que DSI et DPO, je veux une solution hébergée dans l'Union européenne, qui collecte le minimum de données sur les contacts externes, afin de respecter les règles d'Orvanne.

#### Critères d'acceptation

1. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_
2. LE SYSTÈME DOIT limiter les données collectées sur un contact externe à son nom, son prénom, son adresse e-mail professionnelle, sa langue et son rattachement à un fournisseur ou à un transporteur. _Source : CT-01_
3. LE SYSTÈME DOIT supprimer les comptes externes inactifs et leurs données de contact au terme d'une durée paramétrable, fixée avec la DPO. _Source : CT-01_
4. LE SYSTÈME DOIT utiliser exclusivement des données synthétiques ou anonymisées dans les environnements de test et de démonstration. _Source : CT-04_

## Hors périmètre

- Notation des fournisseurs à partir de la ponctualité (`B08-D18`) : classée en V2 par l'atelier ; la V1 constitue l'historique nécessaire (critère 9.6, `H23`). Renvoyée vers la V2 de P06.
- Pénalités des fournisseurs (`B08-D19`) : idée « à terme », non décidée, sans base contractuelle connue (`H23`, `Q24`). Aucun projet ne la reprend ; le critère 9.7 l'exclut explicitement de la V1.
- Lien avec Hangar pour préremplir la réception attendue (`B08-D23`) : jugé « bien mais pas vital » et classé en V2. Renvoyé vers la V2 de P06.
- Application mobile pour les chauffeurs (`B08-D24`) : classée en V2. Renvoyée vers la V2 de P06.
- Prise de rendez-vous dans le portail pour les messageries et petits colis sans commande d'achat (`B08-D22`) : non arbitrée (conflit C23). En V1, R1 s'applique et le chef de quai bloque un quai sur une plage fixe (critère 6.4, `H22`). Leur prise en charge dans le portail reste à décider (`Q23`).
- Chiffrage et planning (`B08-D29`) : livrable de la DSI attendu en décembre, pas une exigence du système. Le découpage de `tasks.md` sert de base à ce chiffrage.
- Entrepôt E3 : non évoqué dans B08. Le paramétrage par site (exigence 2) permet de l'ajouter sans développement si la réponse à `Q38` l'inclut.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H20 | La durée de créneau est un paramètre par site, ajouté aux paramètres de R4, avec 30 minutes par défaut (R2). Chaque site fixe sa valeur lors du paramétrage ; un camion complet consomme deux créneaux. | C21 | oui |
| H21 | Le nombre de quais est saisi par site (R4) ; la valeur de E1 est celle que le chef de quai fournira pour le 04/12. | C22 | oui |
| H22 | R1 s'applique en V1 : toute réservation exige une commande d'achat. Pour les messageries et petits colis sans commande, le chef de quai bloque un quai sur une plage fixe (R7). Leur prise en charge dans le portail est reportée. | C23 | oui |
| H23 | La V1 enregistre les heures prévues et réelles d'arrivée, qui alimentent l'indicateur de ponctualité. La notation des fournisseurs est en V2 ; les pénalités restent hors périmètre tant qu'elles ne sont pas décidées. | C24 | oui |
| H26 | Les textes du portail fournisseurs (écrans, e-mails) sont externalisés pour qu'une langue s'ajoute sans développement. La V1 est en français. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q21 | La durée de créneau peut-elle être fixée par site ? Quelle valeur pour E1 (30 minutes ou une heure) et pour E2 ? | Grégory Thibaudeau ; Rémi Vasseur ; Karim Benhaddou | non (valeur du paramètre 2.2 ; défaut 30 min) |
| Q22 | E1 a 6 quais de réception aujourd'hui, le paramétrage cible en indique 4 : pourquoi cet écart ? | Rémi Vasseur | non (valeur saisie au critère 2.5) |
| Q23 | Les messageries et petits colis sans commande d'achat entrent-ils dans le périmètre ? Un quai réservé sur une plage fixe suffit-il en V1 ? | Grégory Thibaudeau ; Rémi Vasseur | non (critères 6.3 et 6.4) |
| Q24 | À partir de quand la ponctualité alimente-t-elle la notation des fournisseurs ? Les pénalités sont-elles envisagées, et sur quelle base contractuelle ? | Nadège Courtois ; Grégory Thibaudeau | non (V2 ; critère 9.7) |
| Q27 | Dans quelles langues proposer le portail fournisseurs (anglais, allemand, espagnol) ? Pour quelle version ? | Grégory Thibaudeau | non (critère 10.3) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non (critère 11.1) |
| Q35 | La conformité RGAA s'applique-t-elle au portail fournisseurs ? | DSI (comité d'architecture) | non (critère 1.5, appliqué par prudence) |
| Q36 | Quand la DPO peut-elle examiner le traitement des contacts fournisseurs et transporteurs (CT-01) ? Une analyse d'impact est-elle nécessaire ? | Hélène Marsac | non (critères 11.2 et 11.3 ; préalable au développement) |
| Q38 | L'entrepôt E3 entre-t-il dans le périmètre de la prise de rendez-vous ? | Grégory Thibaudeau | non (paramétrage, exigence 2) |

### Points sans hypothèse dans l'analyse, à remonter à l'analyste (étape 2)

Les sources ne tranchent pas les points suivants et `work/analyse.json` ne leur associe ni hypothèse ni question. La spec retient le comportement le plus simple compatible avec B08 ; ces choix sont à valider avec l'approvisionnement.

- Définition de « camion complet » (`B08-F6`) : déclarée par l'auteur de la réservation (critère 3.4).
- Destinataire des e-mails quand le fournisseur réserve lui-même (`B08-F9`) : e-mail du transporteur obligatoire, copie à l'auteur (critères 3.9 et 5.4).
- Suite d'un créneau perdu (`B08-F11`) : décision du chef de quai, qui peut forcer un nouveau créneau (critères 7.5 et 6.2).
- Accès des fournisseurs et transporteurs au portail (`B08-F12`) : comptes nominatifs ouverts par Orvanne (critère 1.2).
- Définitions des indicateurs (critères 9.1 à 9.4), en particulier le point de départ de l'attente (pointage) et le traitement des créneaux bloqués.
- `CT-10` n'est pas rattachée à P06 dans l'analyse, alors que le forçage d'une réservation pour le compte d'un fournisseur en relève (critères 6.2 et 6.6).
- Durée de conservation des données de contact externes : aucune valeur dans les sources (critère 11.3, à fixer avec la DPO via `Q36`).
