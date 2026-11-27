# Exigences : évolutions de l'espace vendeur de la marketplace

<!-- Projet P07, slug espace-vendeur-marketplace. Commanditaire : direction marketplace.
     Parties prenantes : finance, comptabilité, chargés de compte, service client (Comptoir), DSI. Sources : B09 (MKP-01 à MKP-12).
     Les défauts MKP-07 et MKP-11 (lenteur) sont spécifiés dans P08 (correctifs-espace-vendeur). -->

## Introduction

Les vendeurs partenaires de la marketplace d'Orvanne disposent déjà d'un espace vendeur, dont le système porteur n'est pas nommé dans les sources (B09-F15). Le tableau de la direction marketplace (B09) recense 12 demandes saisies entre le 02/09/2026 et le 03/11/2026. Les vendeurs veulent suivre leurs ventes sans appeler leur chargé de compte, télécharger les factures de commission que la comptabilité produit chaque mois en PDF, et comprendre leurs reversements. Les vendeurs du top 20 demandent à modifier eux-mêmes leur IBAN (aujourd'hui par e-mail au chargé de compte), alors que la finance interdit, depuis l'incident de juin, toute modification de coordonnées bancaires sans double validation interne. Deux alertes de retard d'expédition sont demandées : au chargé de compte au-delà de 2 % sur 30 jours glissants, au vendeur au-delà de 5 % sur 7 jours.

Le projet est découpé en trois lots, pour tenir compte du gel des mises en production du 16 novembre au 11 janvier (`CT-07`), des échéances exprimées et de la dépendance à P08 :
- **Lot 1a** (exigences 3, 4, 6, 7, critères 10.1, 10.2, 10.4 et exigence 12) : taux de retard, alerte au vendeur (MKP-08, échéance 15/01/2027) et modification encadrée de l'IBAN (MKP-04, « ASAP »). Mise en production au plus tôt le 12 janvier 2027. Une mise en production avant le 16 novembre n'est pas prévue : elle supposerait l'avis de la DPO (`CT-01`) et la réponse à `Q25` en moins de deux semaines.
- **Lot 1b** (exigences 1, 2 et 5) : vue des ventes (MKP-01, T1 2027), factures de commission (MKP-02) et alerte aux chargés de compte (MKP-03, « fin mars », sans année). Ce lot est livré après les correctifs de P08, qui portent sur les mêmes données de ventes.
- **Lot 2** (exigences 8, 9, 11 et critères 10.3, 10.5 à 10.7) : détail des reversements (MKP-11), réponses aux questions des clients (MKP-09, S1 2027), ouverture aux vendeurs européens (MKP-10, 2027) et tableau de bord sur mobile (MKP-12, T2 2027).

## Glossaire

- **Vendeur** : partenaire qui vend ses articles sur Vitrine via la marketplace et dispose d'un compte dans l'espace vendeur.
- **Espace vendeur** : portail existant réservé aux vendeurs (ventes, export des ventes, reversements).
- **Chargé de compte** : collaborateur d'Orvanne qui suit un portefeuille de vendeurs.
- **Facture de commission** : facture mensuelle, au format PDF, que la comptabilité émet à chaque vendeur pour la commission prélevée par Orvanne.
- **Reversement** : versement par Orvanne au vendeur du produit de ses ventes, sur son IBAN en vigueur.
- **IBAN en vigueur** : dernier IBAN du vendeur ayant reçu la double validation interne ; c'est le seul utilisé pour les reversements.
- **Double validation interne** : approbation d'une modification de coordonnées bancaires par deux collaborateurs distincts d'Orvanne habilités par la finance.
- **Retard d'expédition** : commande que le vendeur expédie en retard, selon la définition unique fournie par la direction marketplace (`Q26`).
- **Taux de retard d'expédition** : part des commandes d'un vendeur en retard d'expédition sur une fenêtre de calcul donnée.
- **Règle d'alerte** : combinaison paramétrable d'un seuil, d'une fenêtre de calcul et d'un destinataire (vendeur ou chargé de compte).

## Exigences

### Exigence 1 : vue des ventes du vendeur (lot 1b)

**User story :** En tant que vendeur, je veux voir en un coup d'œil mes ventes du jour, de la semaine et du mois, afin de suivre mon activité sans appeler mon chargé de compte.

#### Critères d'acceptation

1. QUAND un vendeur ouvre son tableau de bord, LE SYSTÈME DOIT afficher le nombre de commandes et le montant des ventes du vendeur pour le jour en cours, la semaine en cours et le mois en cours. _Source : B09-D1_
2. LE SYSTÈME DOIT afficher les trois périodes sur le même écran, sans autre action du vendeur que l'ouverture du tableau de bord. _Source : B09-D1_
3. LE SYSTÈME DOIT afficher la date et l'heure de la dernière mise à jour des chiffres de ventes. _Source : B09-D1_
4. LE SYSTÈME DOIT calculer les chiffres du tableau de bord à partir des mêmes données que l'export des ventes, de sorte qu'une même période donne le même nombre de commandes et le même montant dans les deux. _Source : B09-D1_

### Exigence 2 : factures de commission (lot 1b)

**User story :** En tant que vendeur, je veux télécharger mes factures de commission, afin d'être autonome pour ma comptabilité.

#### Critères d'acceptation

1. QUAND la comptabilité dépose la facture mensuelle de commission d'un vendeur au format PDF, LE SYSTÈME DOIT la rendre téléchargeable dans l'espace vendeur de ce vendeur. _Source : B09-D2, B09-D3_
2. LE SYSTÈME DOIT lister les factures de commission du vendeur par mois, de la plus récente à la plus ancienne. _Source : B09-D2_
3. LE SYSTÈME DOIT restituer au téléchargement le fichier PDF déposé par la comptabilité, identique octet pour octet. _Source : B09-D3_
4. SI une facture déposée ne peut être rattachée à aucun vendeur, ALORS LE SYSTÈME DOIT la refuser, ne pas la publier et signaler le refus à la comptabilité. _Source : B09-D3_

### Exigence 3 : calcul du taux de retard d'expédition (lot 1a)

**User story :** En tant que membre de la direction marketplace, je veux un calcul unique du taux de retard d'expédition, afin que les alertes aux vendeurs et aux chargés de compte reposent sur la même mesure.

#### Critères d'acceptation

1. LE SYSTÈME DOIT calculer le taux de retard d'expédition de chaque vendeur selon une définition unique du retard d'expédition, enregistrée et versionnée dans les paramètres, et commune à toutes les règles d'alerte. _Source : B09-D5, B09-D13, H25_
2. LE SYSTÈME DOIT calculer le taux sur la fenêtre propre à chaque règle d'alerte : 30 jours glissants pour la règle des chargés de compte, 7 jours pour la règle du vendeur. _Source : B09-D5, B09-D13, H25_
3. LE SYSTÈME DOIT recalculer les taux de tous les vendeurs à la fréquence paramétrée. _Source : B09-D12, H25_
4. LE SYSTÈME DOIT permettre à un administrateur de la direction marketplace de modifier le seuil, la fenêtre et le destinataire de chaque règle d'alerte sans nouvelle mise en production. _Source : H25_
5. LE SYSTÈME DOIT conserver pour chaque calcul le vendeur, la fenêtre, le nombre de commandes en retard, le nombre de commandes prises en compte, le taux obtenu et la version de la définition appliquée. _Source : H25_
6. SI aucune définition du retard d'expédition n'est enregistrée, ALORS LE SYSTÈME DOIT refuser l'activation des règles d'alerte. _Source : H25_

### Exigence 4 : alerte au vendeur (lot 1a)

**User story :** En tant que chargé de compte, je veux que le vendeur soit alerté dès que son taux de retard dépasse 5 % sur 7 jours, afin qu'il corrige ses délais d'expédition et que la qualité de service se maintienne.

#### Critères d'acceptation

1. QUAND le taux de retard d'expédition d'un vendeur calculé sur 7 jours devient strictement supérieur à 5 %, LE SYSTÈME DOIT émettre une alerte à ce vendeur. _Source : B09-D12, B09-D13, H25_
2. LE SYSTÈME DOIT afficher l'alerte dans l'espace vendeur et l'envoyer par les autres canaux paramétrés pour la règle. _Source : B09-D12, H25_
3. LE SYSTÈME DOIT indiquer dans l'alerte le taux constaté, le seuil, la fenêtre de calcul, le nombre de commandes en retard et la liste de ces commandes. _Source : B09-D12_
4. QUAND une alerte est émise à un vendeur, LE SYSTÈME DOIT la rendre visible au chargé de compte de ce vendeur. _Source : B09-D12_

### Exigence 5 : alerte aux chargés de compte (lot 1b)

**User story :** En tant que chargé de compte, je veux être alerté quand un vendeur dépasse 2 % de commandes expédiées en retard sur 30 jours glissants, afin d'intervenir auprès de lui.

#### Critères d'acceptation

1. QUAND le taux de retard d'expédition d'un vendeur calculé sur 30 jours glissants devient strictement supérieur à 2 %, LE SYSTÈME DOIT émettre une alerte au chargé de compte de ce vendeur. _Source : B09-D4, B09-D5, H25_
2. LE SYSTÈME DOIT présenter au chargé de compte la liste de ses vendeurs en alerte, triée par taux décroissant, avec le taux, la fenêtre et la date du début du dépassement. _Source : B09-D4_
3. SI aucun chargé de compte n'est rattaché au vendeur, ALORS LE SYSTÈME DOIT adresser l'alerte au destinataire de repli paramétré par la direction marketplace. _Source : B09-D4, H25_

### Exigence 6 : demande de modification de l'IBAN par le vendeur (lot 1a)

**User story :** En tant que vendeur, je veux modifier mon IBAN moi-même dans l'espace vendeur, afin d'éviter l'échange par e-mail avec mon chargé de compte et de recevoir mes reversements plus vite.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au vendeur de saisir une demande de modification de son IBAN dans son espace vendeur. _Source : B09-D6, H24_
2. SI l'IBAN saisi n'a pas une structure et une clé de contrôle valides, ALORS LE SYSTÈME DOIT refuser la saisie et indiquer l'erreur au vendeur. _Source : B09-D6_
3. PENDANT QUE la demande est en attente de double validation, LE SYSTÈME DOIT continuer à utiliser l'IBAN en vigueur pour les reversements. _Source : B09-D7, H24_
4. LE SYSTÈME DOIT afficher au vendeur l'état de sa demande : en attente de validation, validée ou refusée. _Source : H24_
5. QUAND une demande est refusée, LE SYSTÈME DOIT informer le vendeur du refus et lui indiquer que l'IBAN en vigueur reste utilisé. _Source : H24_

### Exigence 7 : double validation interne des coordonnées bancaires (lot 1a)

**User story :** En tant que responsable de la finance, je veux qu'aucune modification de coordonnées bancaires ne prenne effet sans double validation interne, afin de lutter contre la fraude.

#### Critères d'acceptation

1. LE SYSTÈME NE DOIT PAS appliquer une modification de coordonnées bancaires avant sa validation par deux collaborateurs internes distincts. _Source : B09-D7, H24_
2. SI un collaborateur qui a déjà validé une demande tente de donner la seconde validation, ALORS LE SYSTÈME DOIT refuser cette validation. _Source : B09-D7_
3. LE SYSTÈME DOIT réserver la validation des demandes aux collaborateurs dotés du rôle de valideur, attribué selon les règles fixées par la finance. _Source : B09-D7, H24_
4. QUAND la seconde validation est donnée, LE SYSTÈME DOIT faire du nouvel IBAN l'IBAN en vigueur pour les reversements suivants et en informer le vendeur. _Source : H24_
5. QUAND un valideur refuse une demande, LE SYSTÈME DOIT clore la demande, enregistrer le motif et conserver l'IBAN en vigueur. _Source : B09-D7, H24_
6. LE SYSTÈME DOIT journaliser chaque saisie, validation et refus d'une demande de modification d'IBAN, avec l'auteur, l'horodatage et l'identifiant de la demande, sans IBAN en clair dans le journal. _Source : B09-D7, CT-10_

### Exigence 8 : détail des reversements (lot 2)

**User story :** En tant que vendeur, je veux comprendre de quoi se compose chaque reversement, afin de rapprocher les montants reçus de mes ventes sans solliciter mon chargé de compte.

#### Critères d'acceptation

1. QUAND un vendeur consulte ses reversements, LE SYSTÈME DOIT lister chaque reversement avec sa date et son montant. _Source : B09-D18_
2. QUAND un vendeur ouvre un reversement, LE SYSTÈME DOIT afficher le détail ligne à ligne des éléments qui le composent, dont la somme est égale au montant reversé. _Source : B09-D18_
3. LE SYSTÈME DOIT associer à chaque ligne de détail un libellé explicatif et, pour une ligne de commission, un lien vers la facture de commission correspondante. _Source : B09-D18, B09-D2_
4. SI la somme des lignes de détail diffère du montant reversé, ALORS LE SYSTÈME DOIT ne pas afficher ce détail au vendeur et signaler l'écart à la finance. _Source : B09-D18_

### Exigence 9 : réponses aux questions des clients (lot 2)

**User story :** En tant que vendeur, je veux répondre aux questions des clients depuis l'espace vendeur, afin d'améliorer leur satisfaction.

#### Critères d'acceptation

1. QUAND un client adresse une question à un vendeur, LE SYSTÈME DOIT la présenter à ce vendeur dans son espace vendeur. _Source : B09-D14_
2. QUAND le vendeur répond depuis l'espace vendeur, LE SYSTÈME DOIT transmettre la réponse au client par le canal retenu, Comptoir ou messagerie dédiée. _Source : B09-D14_
3. LE SYSTÈME DOIT conserver l'historique de chaque échange (messages, auteurs, horodatages) et l'afficher au vendeur. _Source : B09-D14_
4. OÙ le canal Comptoir est retenu, LE SYSTÈME DOIT rendre les échanges entre vendeurs et clients consultables par le service client dans Comptoir. _Source : B09-D14_
5. LE SYSTÈME DOIT limiter les données du client visibles par le vendeur à la liste validée par la DPO. _Source : B09-D14, CT-01_
6. SI l'avis de la DPO sur ce traitement n'est pas enregistré, ALORS LE SYSTÈME DOIT maintenir la fonction désactivée. _Source : CT-01_
7. LE SYSTÈME DOIT supprimer les échanges au terme de la durée de conservation paramétrée, fixée avec la DPO. _Source : CT-01_

### Exigence 10 : ouverture aux vendeurs européens (lots 1a et 2)

**User story :** En tant que membre de la direction marketplace, je veux ouvrir l'espace vendeur aux vendeurs européens, en commençant par l'Allemagne et l'Espagne, afin de développer la marketplace.

#### Critères d'acceptation

1. LE SYSTÈME DOIT stocker les textes des écrans, des alertes et des e-mails de l'espace vendeur hors du code, de sorte qu'une langue s'ajoute sans développement. _Source : CT-11, H26_
2. LE SYSTÈME DOIT proposer l'espace vendeur en français en V1. _Source : H26_
3. OÙ une langue supplémentaire est activée, LE SYSTÈME DOIT permettre au vendeur de la choisir et l'appliquer aux écrans, aux alertes et aux e-mails qu'il reçoit. _Source : B09-D15, CT-11, H26_
4. SI un texte n'existe pas dans la langue choisie par le vendeur, ALORS LE SYSTÈME DOIT afficher le texte français. _Source : H26_
5. LE SYSTÈME DOIT permettre d'ouvrir l'espace vendeur pays par pays, selon le pays d'établissement du vendeur, par paramétrage et sans développement. _Source : B09-D15, B09-D16_
6. LE SYSTÈME DOIT proposer l'Allemagne et l'Espagne parmi les pays activables dès la première ouverture hors de France. _Source : B09-D16_
7. LE SYSTÈME DOIT accepter les IBAN de tous les pays ouverts aux vendeurs, dont l'Allemagne et l'Espagne. _Source : B09-D6, B09-D16_

### Exigence 11 : tableau de bord vendeur sur mobile (lot 2)

**User story :** En tant que vendeur, je veux consulter mon tableau de bord sur mobile, afin de suivre mon activité en déplacement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT proposer sur smartphone le tableau de bord vendeur, avec les mêmes chiffres de ventes (exigence 1) et les mêmes alertes (exigence 4) que sur ordinateur. _Source : B09-D19, CT-09_
2. LE SYSTÈME DOIT afficher le tableau de bord vendeur sur un écran de smartphone sans défilement horizontal. _Source : B09-D19, CT-09_
3. LE SYSTÈME DOIT rendre conformes au RGAA les écrans destinés aux vendeurs créés ou modifiés par ce projet. _Source : CT-09_

### Exigence 12 : exigences non fonctionnelles

**User story :** En tant que DSI, je veux un espace vendeur cloisonné, hébergé dans l'UE et traçable, afin de protéger les données des vendeurs et des clients.

#### Critères d'acceptation

1. LE SYSTÈME DOIT limiter l'accès de chaque vendeur à ses propres ventes, factures, alertes, reversements, coordonnées bancaires et échanges avec les clients. _Source : B09-D1, B09-D2, B09-D6_
2. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_
3. LE SYSTÈME DOIT journaliser chaque action réalisée par un collaborateur d'Orvanne pour le compte d'un vendeur, avec l'auteur, l'action, l'objet et l'horodatage. _Source : CT-10_
4. LE SYSTÈME DOIT respecter, sur les écrans créés par ce projet, le seuil de temps de réponse fixé dans la spec bugfix P08. _Source : H27_
5. LE SYSTÈME NE DOIT PAS utiliser de données de production non anonymisées dans les environnements de recette et de démonstration. _Source : CT-04_
6. LE SYSTÈME DOIT journaliser chaque modification de la définition du retard d'expédition et des règles d'alerte, avec l'auteur, l'horodatage, l'ancienne et la nouvelle valeur. _Source : H25_

## Hors périmètre

- Suivi des retours et des litiges par le vendeur, MKP-06 (`B09-D8`) : il dépend du circuit des retours marketplace, prévu en V2 du portail de retours. Renvoyé vers P02.
- Export des ventes en erreur au-delà de 50 000 lignes, MKP-07 (`B09-D9`) : défaut de l'existant. Renvoyé vers P08.
- Index sur la table des lignes de commande et export asynchrone, MKP-07 (`B09-D10`, `B09-D11`) : solutions techniques proposées par la DSI, traitées comme pistes de conception dans la spec bugfix. Renvoyées vers P08.
- Lenteur de l'espace vendeur, MKP-11 (`B09-D17`) : défaut de l'existant, à mesurer puis corriger. Renvoyé vers P08. Le seuil qui en sortira s'applique aussi aux nouveaux écrans (critère 12.4). La seconde partie de MKP-11, la compréhension des reversements (`B09-D18`), est traitée ici (exigence 8).
- Échéances exprimées (`B09-D1` « T1 2027 », `B09-D4` « fin mars », `B09-D6` « ASAP », `B09-D12` « 15/01/2027 », `B09-D14` « S1 2027 », `B09-D15` « 2027 », `B09-D19` « T2 2027 ») : ce ne sont pas des exigences du système. Elles déterminent le découpage en lots de l'introduction et de `tasks.md`.
- Choix entre une application mobile et un site adapté pour MKP-12 : décision de conception, proposée dans `design.md` (site adapté) et soumise à la question Q-P07-7.
- Inscription, contrat et fiscalité des vendeurs européens : non décrits dans les sources (B09-F12). Aucun projet ne les reprend à ce stade (question Q-P07-6).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H24 | Le vendeur saisit son nouvel IBAN dans l'espace vendeur. Le changement ne prend effet qu'après une double validation interne ; d'ici là, l'ancien IBAN reste utilisé et le vendeur voit l'état de sa demande. | C25 | oui |
| H25 | Deux règles d'alerte distinctes et paramétrables (seuil, fenêtre, destinataire) : 2 % sur 30 jours glissants pour les chargés de compte, 5 % sur 7 jours pour le vendeur. Elles reposent sur une même définition du retard d'expédition, à fournir par la direction marketplace. | C26 | oui |
| H26 | Les textes de l'espace vendeur (écrans, e-mails) sont externalisés pour qu'une langue s'ajoute sans développement. La V1 est en français. | — | oui |
| H27 | Pour MKP-11, la spec bugfix P08 mesure les temps de réponse de l'espace vendeur et fixe un seuil chiffré avec la direction marketplace ; ce seuil vaut aussi pour les écrans de P07. | — | oui |

## Questions ouvertes

Les questions `Qnn` viennent de `work/analyse.json`. Les questions `Q-P07-n` sont nées de la rédaction : elles n'existent pas encore dans l'analyse et sont à y ajouter par l'analyste, qui leur attribuera un identifiant définitif.

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q25 | Un IBAN saisi par le vendeur puis validé par deux personnes en interne respecte-t-il MKP-05 ? Qui sont les deux valideurs ? | Finance (DAF) ; direction marketplace | non (rôle de valideur du critère 7.3 à paramétrer avant la recette du lot 1a) |
| Q26 | Qu'est-ce qu'une commande « expédiée en retard » pour un vendeur ? Les deux alertes (2 % sur 30 jours, 5 % sur 7 jours) doivent-elles coexister ? | Direction marketplace | non dans l'analyse ; la définition est requise avant le développement du calcul (exigence 3, tâche 1.3) |
| Q11 | Les retours marketplace entrent-ils en V1 ou en V2 du portail de retours ? Qui fournit les étiquettes et le circuit vers les vendeurs ? | Direction de l'expérience client ; direction marketplace ; Yanis Mercadier | non (MKP-06, hors périmètre) |
| Q27 | Dans quelles langues proposer l'espace vendeur (anglais, allemand, espagnol) ? Pour quelle version ? | Direction marketplace | non (critère 10.3) |
| Q34 | L'hébergement dans le cloud d'Orvanne s'applique-t-il à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non |
| Q35 | La conformité RGAA s'applique-t-elle à l'espace vendeur ? | DSI (comité d'architecture) | non (critère 11.3 appliqué par défaut) |
| Q36 | Quand la DPO peut-elle examiner les traitements de P07 (coordonnées bancaires, échanges vendeur-client) ? Lesquels exigent une analyse d'impact ? | Hélène Marsac | non (prérequis des lots 1a et 2) |
| Q-P07-1 | Par quel canal le vendeur répond-il aux clients : Comptoir ou une messagerie dédiée (B09-F10) ? Les questions portent-elles sur une commande, sur un article avant achat, ou les deux ? Le service client doit-il voir les échanges ? | Direction marketplace ; service client (Yanis Mercadier) | oui (conception de l'exigence 9, lot 2) |
| Q-P07-2 | Quel système porte l'espace vendeur aujourd'hui (B09-F15) ? D'où viennent les données de ventes, d'expédition des vendeurs et de reversements ? Combien de vendeurs actifs, et combien de commandes marketplace par jour, pic compris ? | DSI ; direction marketplace | non pour la spec ; oui pour l'architecture détaillée et le dimensionnement (tâche 1.2) |
| Q-P07-3 | Le montant des ventes s'entend-il TTC ou HT, net des annulations et des retours ? La semaine et le mois sont-ils calendaires ? | Direction marketplace | non (critère 1.1) |
| Q-P07-4 | De quoi se compose un reversement (ventes, commission, retenues, autres) et quel système le calcule ? Qu'est-ce que les vendeurs ne comprennent pas aujourd'hui ? | Finance ; direction marketplace | non (contenu du critère 8.3) |
| Q-P07-5 | Comment la comptabilité transmet-elle les factures PDF (dépôt, nommage, identifiant du vendeur) ? Sur combien de mois les factures restent-elles consultables ? | Comptabilité | non (critère 2.1) |
| Q-P07-6 | Que suppose l'ouverture aux vendeurs européens au-delà de la langue et de l'IBAN (inscription, contrat, fiscalité, factures) ? | Direction marketplace ; finance | non (hors périmètre à ce stade) |
| Q-P07-7 | Pour MKP-12, un site adapté au mobile suffit-il, ou une application est-elle attendue (B09-F11) ? | Direction marketplace | non (proposition : site adapté) |
| Q-P07-8 | Par quels canaux alerter le vendeur (espace vendeur, e-mail) ? Faut-il répéter l'alerte tant que le taux reste au-dessus du seuil ? Faut-il un nombre minimal de commandes pour calculer un taux ? Où est enregistré le rattachement d'un vendeur à son chargé de compte ? | Direction marketplace ; chargés de compte | non (critères 4.2 et 5.3 paramétrables) |
