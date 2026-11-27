# Exigences : portail de retours en libre-service, remboursement et visibilité des entrepôts

<!-- Projet P02, slug portail-retours. Commanditaire : direction de l'expérience client.
     Parties prenantes : DSI, service client, contrôle de gestion et DAF, marketing, exploitation entrepôt E2,
     direction marketplace, direction juridique et conformité (DPO). Sources : B03, B04, B09 (MKP-06). -->

## Introduction

Aujourd'hui, un client qui veut retourner un article doit contacter le service client, qui crée la demande dans Comptoir et envoie l'étiquette par e-mail. Ce parcours représente environ 900 demandes par jour ouvré, avec un délai moyen de 2,5 jours entre la demande et la réception de l'étiquette (B03). L'entrepôt E2 reçoit environ 1 100 colis retour par jour, dont 1 sur 5 n'est pas conforme à l'ouverture ; le contrôle a lieu 3 à 6 jours après la réception, 10 jours en janvier (B04).

Le portail doit permettre au client de déclarer un retour et d'obtenir son étiquette en moins de 3 minutes sans contacter un conseiller, réduire de 60 % les contacts liés aux retours en 6 mois, et donner aux entrepôts la liste des retours attendus (B03, objectifs O1 à O3).

Plusieurs règles ne sont pas arbitrées : moment du remboursement (C08), délai de retour (C09), gratuité (C10), retours marketplace (C11), montant selon la note A / B / C (C12), accès sans compte (C13), RMA imprimé (C14). La spec les traite par des **paramètres** modifiables sans mise en production, avec une valeur par défaut prudente (hypothèses H07 à H13).

Le projet est livré en deux lots :
- **Lot 1** (exigences 1 à 11) : portail pour les articles vendus et expédiés par Orvanne, remboursement, liste prévisionnelle pour les entrepôts, création et correction par le service client. Mise en service d'un pilote au plus tôt le 12 janvier 2027, après le gel des mises en production du 16 novembre au 11 janvier (`CT-07`) et après l'avis de la DPO (`CT-01`), selon `H14`.
- **Lot 2** (exigences 12 à 14) : photos jointes par le client, retours des articles marketplace et suivi par le vendeur (MKP-06), option de bon d'achat. Date à fixer après le pilote.

Le remboursement des retours marketplace n'est pas spécifié : il dépend du circuit vendeur, non décrit (`Q11`).

## Glossaire

- **Retour** : demande d'un client portant sur un ou plusieurs articles d'une même commande, identifiée par un numéro de retour.
- **Étiquette** : étiquette transporteur prépayée (PDF et QR code) obtenue par l'API du transporteur.
- **RMA** : autorisation de retour, document PDF à imprimer et à placer dans le colis pour que l'entrepôt retrouve la commande.
- **Statut du retour** : étape visible du client : `déclaré`, `déposé`, `reçu`, `remboursé`.
- **Premier scan** : premier événement de suivi du colis retour émis par le transporteur et reçu via Passerelle.
- **Note de contrôle** : note de la grille A / B / C attribuée au contrôle qualité en entrepôt (A remis en stock, B déstockage, C rebut).
- **Déclencheur du remboursement** : événement qui lance le remboursement : premier scan, réception en entrepôt ou contrôle qualité.
- **Frais de retour** : montant éventuellement retenu sur le remboursement, paramétré par motif.
- **Catégorie de client** : population à laquelle s'applique un paramètre ; en V1, « tous les clients » et « membres Orvanne+ ».
- **Liste prévisionnelle** : fichier quotidien des retours attendus par entrepôt, transmis à Hangar.
- **Signalement** : demande de traitement manuel créée dans Comptoir pour un retour noté C.
- **Administrateur métier** : personne de la direction de l'expérience client habilitée à modifier les paramètres.

## Exigences

### Exigence 1 : accès au portail et identification de la commande

**User story :** En tant que client, je veux retrouver ma commande avec ou sans compte, afin de déclarer un retour sans contacter le service client.

#### Critères d'acceptation

1. QUAND un client saisit un numéro de commande et l'adresse e-mail utilisée lors de l'achat qui correspondent, LE SYSTÈME DOIT afficher cette commande sans exiger de création de compte. _Source : B03-D8, H12_
2. QUAND un client connecté à son compte Vitrine ouvre le portail depuis une de ses commandes, LE SYSTÈME DOIT afficher cette commande sans nouvelle saisie d'identification. _Source : B03-D11, H12_
3. PENDANT QUE le client accède au portail sans compte, LE SYSTÈME DOIT limiter l'accès à la seule commande saisie et à ses retours. _Source : H12, CT-01_
4. SI le numéro de commande et l'adresse e-mail ne correspondent pas, ALORS LE SYSTÈME DOIT afficher un message unique qui n'indique pas laquelle des deux valeurs est erronée. _Source : H12, CT-01_
5. SI le nombre de tentatives échouées pour un même numéro de commande dépasse le seuil paramétré sur la fenêtre de temps paramétrée, ALORS LE SYSTÈME DOIT refuser toute nouvelle tentative pour ce numéro pendant la durée de blocage paramétrée. _Source : H12, CT-01_
6. LE SYSTÈME DOIT lire les commandes et les livraisons dans le système de gestion des commandes, via Passerelle. _Source : B03-D24_

### Exigence 2 : éligibilité des articles au retour

**User story :** En tant que client, je veux savoir pour chaque article s'il peut être retourné et jusqu'à quand, afin de ne pas déclarer un retour qui sera refusé.

#### Critères d'acceptation

1. QUAND une commande est affichée, LE SYSTÈME DOIT indiquer pour chaque article s'il est éligible au retour et, s'il ne l'est pas, la raison. _Source : B03-D9_
2. LE SYSTÈME DOIT considérer comme éligibles uniquement les articles vendus et expédiés par Orvanne, livrés en France métropolitaine et commandés sur Vitrine (site web ou application mobile). _Source : B03-D4_
3. LE SYSTÈME DOIT calculer la date limite de retour à partir de la date de livraison, avec un délai paramétré par catégorie de client, fixé à 14 jours pour tous les clients et à 30 jours pour les membres Orvanne+ à la mise en service. _Source : B03-D10, B04-D4, B04-D5, H08_
4. LE SYSTÈME DOIT afficher la date limite de retour de chaque article éligible. _Source : B03-D9, H08_
5. LE SYSTÈME DOIT rendre non éligibles les articles des catégories exclues, dont la liste est paramétrable et contient au moins l'hygiène, les produits personnalisés et les denrées. _Source : B03-D10_
6. QUAND un article est vendu par un vendeur partenaire de la marketplace, LE SYSTÈME DOIT l'afficher comme non éligible au portail, avec un renvoi vers le circuit de retour actuel. _Source : B03-D5, H10_
7. QUAND un article est un article volumineux livré sur rendez-vous, LE SYSTÈME DOIT l'afficher comme non éligible au portail, avec un renvoi vers le service client. _Source : B03-D6_
8. LE SYSTÈME NE DOIT PAS proposer d'échange et doit indiquer au client qu'un échange se fait par un retour suivi d'une nouvelle commande. _Source : B03-D7_
9. SI la date de livraison d'un article n'est pas connue, ALORS LE SYSTÈME DOIT afficher l'article comme non éligible en ligne, avec un renvoi vers le service client. _Source : B03-D9, B03-D24_
10. LE SYSTÈME DOIT limiter la quantité retournable d'un article à la quantité livrée, diminuée des quantités déjà déclarées dans d'autres retours de la commande. _Source : B03-D11_

### Exigence 3 : déclaration du retour

**User story :** En tant que client, je veux sélectionner les articles, la quantité, le motif et le mode de retour, afin d'obtenir mon étiquette en quelques minutes.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre au client de sélectionner un ou plusieurs articles éligibles, une quantité par article et un motif par article choisi dans une liste fermée. _Source : B03-D11_
2. LE SYSTÈME DOIT permettre à un administrateur métier de gérer la liste fermée des motifs, chaque motif indiquant s'il relève d'un article défectueux ou d'une erreur de préparation, la liste contenant au moins « article endommagé ». _Source : B03-D11, B03-D17, B04-D6, H09_
3. LE SYSTÈME DOIT proposer au client deux modes de retour : dépôt en point relais ou enlèvement à domicile. _Source : B03-D12_
4. QUAND le client a sélectionné ses articles et son mode de retour, LE SYSTÈME DOIT afficher avant confirmation un récapitulatif comprenant le montant prévisionnel du remboursement, les frais de retour éventuels et le moyen de paiement d'origine. _Source : B03-D27, H09_
5. LE SYSTÈME DOIT permettre à un client de déclarer un retour standard et d'obtenir son étiquette en moins de 3 minutes, de l'accès au portail à l'affichage de l'étiquette, sans contact avec un conseiller. _Source : B03-D1_
6. LE SYSTÈME DOIT mesurer, pour chaque retour déclaré sur le portail, la durée entre l'accès à la commande et l'affichage de l'étiquette. _Source : B03-D1_

### Exigence 4 : étiquette prépayée et RMA

**User story :** En tant que client, je veux recevoir une étiquette prépayée et le document à glisser dans le colis, afin d'expédier mon retour sans autre démarche ; en tant qu'opérateur d'entrepôt, je veux retrouver la commande à l'ouverture du colis.

#### Critères d'acceptation

1. QUAND le client confirme sa déclaration, LE SYSTÈME DOIT obtenir une étiquette prépayée auprès de l'API du transporteur et la fournir au format PDF et sous forme de QR code. _Source : B03-D13, B03-D25_
2. QUAND l'étiquette est obtenue, LE SYSTÈME DOIT l'afficher au client et l'envoyer par e-mail à l'adresse utilisée lors de l'achat. _Source : B03-D13_
3. QUAND l'étiquette est obtenue, LE SYSTÈME DOIT générer un RMA en PDF, à imprimer et à placer dans le colis, qui porte le numéro de retour, le numéro de commande, les articles et quantités retournés et un code-barres lisible à la douchette. _Source : B04-D15, H13_
4. LE SYSTÈME DOIT rattacher l'étiquette et le RMA au même numéro de retour, de sorte que la commande soit retrouvée à partir de l'un ou de l'autre. _Source : B04-D15, H13_
5. SI l'API du transporteur ne fournit pas l'étiquette, ALORS LE SYSTÈME DOIT enregistrer la déclaration, informer le client que l'étiquette lui sera envoyée par e-mail, et relancer la demande d'étiquette selon la politique de reprise paramétrée. _Source : B03-D13, B03-D25_
6. LE SYSTÈME NE DOIT PAS inclure d'offre commerciale dans les e-mails du portail (étiquette, RMA, suivi). _Source : CT-03_

### Exigence 5 : suivi de l'avancement du retour

**User story :** En tant que client, je veux suivre l'avancement de mon retour, afin de savoir quand je serai remboursé sans appeler le service client.

#### Critères d'acceptation

1. LE SYSTÈME DOIT afficher au client le statut de son retour parmi `déclaré`, `déposé`, `reçu` et `remboursé`, avec la date de chaque étape franchie. _Source : B03-D14_
2. QUAND Passerelle reçoit le premier scan du colis retour par le transporteur, LE SYSTÈME DOIT passer le retour au statut `déposé`. _Source : B03-D14, B03-D15_
3. QUAND l'entrepôt enregistre la réception du colis retour, LE SYSTÈME DOIT passer le retour au statut `reçu`. _Source : B03-D14, H07_
4. PENDANT QUE le déclencheur du remboursement est la réception en entrepôt ou le contrôle qualité, LE SYSTÈME DOIT n'afficher le statut `remboursé` qu'après le statut `reçu`. _Source : B03-D14, H07_
5. LE SYSTÈME DOIT donner accès au suivi par les mêmes moyens que l'accès à la commande (exigence 1) et par un lien présent dans l'e-mail de l'étiquette. _Source : B03-D14, H12_

### Exigence 6 : résultat du contrôle qualité

**User story :** En tant que responsable d'entrepôt, je veux que la note de contrôle de chaque retour soit enregistrée, afin que le remboursement et le traitement des articles non conformes en dépendent.

#### Critères d'acceptation

1. QUAND l'entrepôt transmet le résultat du contrôle d'un retour, LE SYSTÈME DOIT enregistrer la note A, B ou C, la date du contrôle, l'entrepôt et la destination associée (A remis en stock, B déstockage, C rebut). _Source : B04-D11_
2. SI le résultat transmis ne porte pas une note A, B ou C ou ne correspond à aucun retour reçu, ALORS LE SYSTÈME DOIT le rejeter et le signaler à la supervision. _Source : B04-D11_
3. LE SYSTÈME NE DOIT PAS faire varier le montant remboursé selon la note A, B ou C. _Source : B04-D12, H11_
4. SI la note d'un retour est C, ALORS LE SYSTÈME DOIT créer un signalement dans Comptoir et, si le remboursement n'est pas encore déclenché, le suspendre jusqu'à la décision d'un conseiller. _Source : H11_
5. QUAND un conseiller traite un signalement, LE SYSTÈME DOIT enregistrer sa décision (remboursement du montant prévu ou blocage) avec un motif obligatoire et l'identité du conseiller. _Source : H11, CT-10_

### Exigence 7 : remboursement

**User story :** En tant que client, je veux être remboursé automatiquement sur mon moyen de paiement ; en tant que DAF, je veux que le moment du remboursement soit un réglage, afin d'appliquer la décision du codir sans redévelopper.

#### Critères d'acceptation

1. LE SYSTÈME DOIT déclencher automatiquement le remboursement à l'événement paramétré : premier scan, réception en entrepôt ou contrôle qualité. _Source : B03-D15, B04-D2, H07_
2. LE SYSTÈME DOIT utiliser le contrôle qualité comme déclencheur pour tous les clients à la mise en service. _Source : B04-D2, H07_
3. LE SYSTÈME DOIT permettre de fixer un déclencheur différent par catégorie de client, notamment pour les membres Orvanne+. _Source : B04-D3, H07_
4. QUAND le remboursement est déclenché, LE SYSTÈME DOIT demander au prestataire de paiement de rembourser le client sur le moyen de paiement d'origine. _Source : B03-D26, B03-D27_
5. LE SYSTÈME DOIT calculer le montant remboursé comme le montant payé pour les articles retournés, diminué des frais de retour applicables à leur motif. _Source : B03-D27, H09_
6. LE SYSTÈME DOIT appliquer des frais de retour paramétrés par motif, égaux à 0 pour tous les motifs à la mise en service. _Source : B03-D29, B04-D8, H09_
7. OÙ une retenue est activée pour les motifs qui ne relèvent ni d'un article défectueux ni d'une erreur de préparation, LE SYSTÈME DOIT déduire le montant paramétré (4,90 € envisagés) du remboursement. _Source : B04-D6, B04-D7, H09_
8. LE SYSTÈME DOIT émettre au plus une demande de remboursement aboutie par article retourné, y compris en cas de nouvelle tentative. _Source : B03-D26_
9. QUAND le prestataire de paiement confirme le remboursement, LE SYSTÈME DOIT passer le retour au statut `remboursé` et enregistrer la référence de l'opération. _Source : B03-D14, B03-D26_
10. SI le prestataire de paiement refuse le remboursement ou ne répond pas après les reprises paramétrées, ALORS LE SYSTÈME DOIT créer un signalement dans Comptoir et ne pas afficher le statut `remboursé`. _Source : B03-D26_

### Exigence 8 : visibilité des entrepôts sur les retours attendus

**User story :** En tant que responsable d'entrepôt, je veux connaître chaque jour les retours attendus, afin de préparer la réception et le contrôle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT déterminer l'entrepôt de destination de chaque retour selon une règle de routage paramétrable. _Source : B03-D16_
2. LE SYSTÈME DOIT transmettre chaque jour à Hangar, par fichier et à l'heure paramétrée, la liste prévisionnelle des retours attendus pour chaque entrepôt. _Source : B03-D3, B03-D16, B03-D28_
3. LE SYSTÈME DOIT inclure dans la liste prévisionnelle, pour chaque retour déclaré et non encore reçu : numéro de retour, numéro de RMA, numéro de commande, articles, quantités, motifs, transporteur, numéro de suivi et date de premier scan si elle est connue. _Source : B03-D16, B04-D15_
4. SI Hangar n'a pas acquitté le fichier du jour dans le délai paramétré, ALORS LE SYSTÈME DOIT alerter la supervision et permettre de renvoyer le fichier. _Source : B03-D28_
5. LE SYSTÈME DOIT permettre aux entrepôts de retrouver un retour et sa commande à partir du numéro de RMA, du numéro de suivi de l'étiquette ou du numéro de commande. _Source : B03-D3, B04-D15_

### Exigence 9 : création et correction par le service client

**User story :** En tant que conseiller du service client, je veux créer ou corriger un retour pour le compte d'un client depuis Comptoir, afin de traiter les cas que le client ne peut pas faire seul.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à un conseiller de créer depuis Comptoir un retour pour le compte d'un client, avec les règles d'éligibilité de l'exigence 2. _Source : B03-D18_
2. LE SYSTÈME DOIT permettre à un conseiller de corriger les articles, les quantités, les motifs et le mode de retour d'un retour existant. _Source : B03-D18_
3. QUAND une correction modifie les articles, les quantités ou le mode d'un retour au statut `déclaré`, LE SYSTÈME DOIT générer une nouvelle étiquette et un nouveau RMA, invalider les précédents et les envoyer au client par e-mail. _Source : B03-D18, H13_
4. LE SYSTÈME DOIT afficher dans Comptoir, pour une commande, ses retours avec leur statut, leur historique et leurs signalements. _Source : B03-D18_
5. QUAND un conseiller crée, corrige un retour ou traite un signalement, LE SYSTÈME DOIT journaliser l'identifiant du conseiller, l'horodatage, l'action, le retour concerné et les valeurs avant et après, comme preuve d'exécution. _Source : B03-D23, CT-10_

### Exigence 10 : indicateurs

**User story :** En tant que commanditaire, je veux mesurer l'usage du portail et les délais de traitement, afin de suivre les objectifs O1 et O2 et d'éclairer la décision sur le moment du remboursement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT produire chaque jour le nombre de retours déclarés sur le portail, de retours créés et de retours corrigés par le service client, ainsi que la durée médiane et le 90e centile de la durée mesurée au critère 3.6. _Source : B03-D1, B03-D2_
2. LE SYSTÈME DOIT produire chaque jour, par entrepôt, les délais médians entre réception et contrôle et entre déclencheur et remboursement, ainsi que la répartition des notes A, B et C. _Source : B04-D11, H07_

### Exigence 11 : exigences non fonctionnelles, conformité et paramétrage

**User story :** En tant que DSI, je veux un portail disponible, rapide, accessible, hébergé dans l'UE et conforme au RGPD, dont les règles métier se règlent sans mise en production, afin de l'ouvrir au public en sécurité.

#### Critères d'acceptation

1. LE SYSTÈME DOIT offrir une disponibilité d'au moins 99,5 %, mesurée chaque mois. _Source : B03-D19_
2. LE SYSTÈME DOIT afficher les pages du portail en moins de 2 secondes pour 95 % des requêtes, jusqu'à 300 utilisateurs simultanés. _Source : B03-D20_
3. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : B03-D21, CT-08_
4. LE SYSTÈME DOIT proposer une interface conforme au RGAA et utilisable sur mobile. _Source : B03-D22, CT-09_
5. LE SYSTÈME DOIT permettre à un client non accompagné de réaliser un retour standard de bout en bout sur mobile lors des tests utilisateurs. _Source : B03-D31, CT-09_
6. LE SYSTÈME DOIT rester fermé aux clients tant que l'avis de la DPO sur le traitement n'est pas enregistré. _Source : CT-01, B03-D21_
7. LE SYSTÈME DOIT conserver les retours, étiquettes, remboursements et journaux pendant des durées paramétrables fixées avec la DPO, puis les supprimer automatiquement. _Source : CT-01, B03-D21_
8. LE SYSTÈME DOIT permettre à un administrateur métier de modifier sans mise en production les délais de retour, les catégories exclues, les motifs, les frais et le déclencheur du remboursement, en conservant l'auteur, la date et l'ancienne valeur de chaque modification. _Source : CT-07, H07, H08, H09_
9. OÙ le mode pilote est activé, LE SYSTÈME DOIT limiter l'accès au portail aux commandes du périmètre pilote paramétré et renvoyer les autres vers le circuit actuel. _Source : B03-D30, H14_
10. LE SYSTÈME DOIT réserver les écrans internes aux rôles habilités (service client, entrepôt, administrateur métier, DSI), authentifiés par le SSO interne. _Source : CT-01, CT-10_
11. LE SYSTÈME DOIT utiliser exclusivement des données synthétiques ou anonymisées dans ses environnements de test et de démonstration. _Source : CT-04_

### Exigence 12 : photos jointes par le client (lot 2)

**User story :** En tant que client, je veux joindre des photos d'un article endommagé ; en tant qu'exploitation entrepôt, je veux les voir avant la réception, afin d'anticiper le contrôle.

#### Critères d'acceptation

1. OÙ la fonction photos est activée, LE SYSTÈME DOIT permettre au client de joindre jusqu'à 3 photos à un article dont le motif est « article endommagé ». _Source : B03-D17_
2. SI une photo dépasse la taille maximale paramétrée ou n'est pas dans un format d'image accepté, ALORS LE SYSTÈME DOIT la refuser en indiquant la raison au client. _Source : B03-D17_
3. QUAND un retour accompagné de photos figure dans la liste prévisionnelle, LE SYSTÈME DOIT permettre à l'exploitation de l'entrepôt de destination de consulter ces photos avant la réception du colis. _Source : B04-D1_
4. LE SYSTÈME DOIT traiter les photos comme des données personnelles : accès réservé aux rôles service client et entrepôt de destination, durée de conservation paramétrée, suppression avec le retour. _Source : CT-06, CT-01_
5. LE SYSTÈME DOIT bloquer l'activation de la fonction photos tant que l'avis de la DPO sur ce traitement n'est pas enregistré. _Source : CT-06, CT-01_

### Exigence 13 : retours des articles marketplace (lot 2)

**User story :** En tant que conseiller du service client, je veux que les retours d'articles marketplace passent aussi par le portail ; en tant que vendeur, je veux suivre les retours déclarés sur mes articles.

#### Critères d'acceptation

1. OÙ les retours marketplace sont activés, LE SYSTÈME DOIT rendre éligibles les articles des vendeurs partenaires selon des règles d'éligibilité paramétrées pour la marketplace. _Source : B04-D9, H10_
2. OÙ les retours marketplace sont activés, LE SYSTÈME DOIT obtenir pour ces articles une étiquette à destination du vendeur, distincte des étiquettes vers les entrepôts d'Orvanne. _Source : B04-D10, H10_
3. LE SYSTÈME NE DOIT PAS inclure les retours d'articles marketplace dans la liste prévisionnelle transmise à Hangar. _Source : B04-D10_
4. QUAND une commande contient des articles d'Orvanne et d'un ou plusieurs vendeurs, LE SYSTÈME DOIT créer un retour et une étiquette par destinataire. _Source : B04-D10, H10_
5. LE SYSTÈME DOIT mettre à disposition de l'espace vendeur (P07) les retours déclarés sur les articles du vendeur : numéro de retour, articles, quantités, motifs, statut et dates. _Source : B09-D8, H10_

### Exigence 14 : bon d'achat à la place du remboursement (lot 2)

**User story :** En tant que client, je veux pouvoir choisir un bon d'achat majoré au lieu d'un remboursement, afin de bénéficier d'un montant supérieur.

#### Critères d'acceptation

1. OÙ l'option bon d'achat est activée (elle est désactivée à la livraison), LE SYSTÈME DOIT proposer au client, dans le récapitulatif, le choix entre le remboursement sur le moyen de paiement d'origine et un bon d'achat majoré du taux paramétré (5 % envisagés). _Source : B04-D14_
2. QUAND le client a choisi le bon d'achat, LE SYSTÈME DOIT émettre le bon d'achat au déclencheur du remboursement, au lieu de solliciter le prestataire de paiement. _Source : B04-D14, H07_
3. LE SYSTÈME NE DOIT PAS promouvoir le bon d'achat dans les e-mails de service du portail. _Source : CT-03, B04-D14_

## Hors périmètre

- Application douchette de saisie de la note et de la photo au contrôle qualité (`B04-D13`) : même écran que la déclaration de casse, renvoyée vers P03. Le portail reçoit la note par l'interface du critère 6.1.
- Suivi du taux de retour par produit (`B04-D16`) : indicateur analytique du Lac, à l'état d'idée, sans porteur (`Q32`) ; aucun projet.
- Chiffrage du coût du remboursement anticipé avant le codir (`B04-D17`) : action du contrôle de gestion, pas une exigence du système. Le résultat alimente la décision sur le déclencheur (critère 7.1) ; les indicateurs du critère 10.2 serviront à le réviser après le pilote.
- Réduction du montant remboursé selon la note (`B04-D12`) : écartée en V1 par `H11` en attendant l'avis juridique (`Q12`). Le critère 6.3 l'interdit explicitement.
- Remboursement des retours marketplace (`B04-D9`, `B04-D10`) : non spécifié, le circuit vendeur et le payeur du remboursement n'étant pas décrits (`Q11`).
- Mouvements de stock consécutifs à la note (remise en stock, déstockage, rebut) : réalisés dans Hangar, hors du portail.
- Mesure du taux de contacts liés aux retours (objectif O2, `B03-D2`) : elle relève des outils du service client ; le portail fournit ses propres données (critère 10.1). La base de référence est à fixer (`Q39`).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H07 | Le déclencheur du remboursement est un paramètre (premier scan, réception en entrepôt, contrôle qualité). La V1 rembourse après le contrôle qualité ; le statut « reçu » précède « remboursé ». | C08 | oui |
| H08 | Le délai d'éligibilité est un paramètre par catégorie de client : 14 jours après livraison pour tous, 30 jours pour les membres Orvanne+. | C09 | oui |
| H09 | Les frais de retour sont un paramètre par motif, à 0 pour tous les motifs au départ. La retenue de 4,90 (euros supposés) hors défaut ou erreur de préparation s'active sans développement si elle est décidée et inscrite dans les CGV. | C10 | oui |
| H10 | La V1 exclut les articles marketplace, affichés comme non éligibles avec un renvoi vers le circuit actuel. Les retours marketplace et leur suivi par le vendeur (MKP-06) forment la V2. | C11 | oui |
| H11 | En V1, le montant remboursé ne dépend pas de la note A / B / C. Une note C déclenche un signalement pour traitement manuel par le service client, sans réduction automatique. | C12 | oui |
| H12 | Le portail est accessible sans compte (numéro de commande et e-mail d'achat) et depuis le compte du client connecté. EF-03 s'applique aux deux parcours ; l'accès sans compte ne donne accès qu'à la commande saisie. | C13 | oui |
| H13 | Le portail produit, avec l'étiquette, un RMA en PDF à imprimer et placer dans le colis. Le cas du client sans imprimante reste ouvert. | C14 | oui |
| H14 | Le pilote est mis en service au plus tôt le 12 janvier, après le gel et après consultation de la DPO. Si la fenêtre avant les soldes d'hiver est trop courte, le pilote est décalé après les soldes. | C15 | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q08 | À quel moment rembourser un retour : premier scan, réception ou contrôle en entrepôt ? Un remboursement anticipé est-il prévu pour certains clients, lesquels ? | DAF, puis codir ; chiffrage par Odile (contrôle de gestion) | non (valeur du paramètre des critères 7.1 à 7.3) |
| Q09 | Quel délai de retour : 14 jours pour tous et 30 jours pour Orvanne+, ou 30 jours pour tous ? Que disent les CGV ? | Direction de l'expérience client ; direction juridique et conformité | non (valeur du paramètre du critère 2.3) |
| Q10 | Les retours sont-ils gratuits pour tous, ou 4,90 € sont-ils retenus hors défaut et erreur de préparation ? Jusqu'à quand dure la gratuité « pour le lancement » ? | DAF ; direction de l'expérience client ; Capucine Lorrain | non (valeurs des critères 7.6 et 7.7) |
| Q11 | Les retours marketplace entrent-ils en V1 ou en V2 ? Qui fournit les étiquettes et le circuit vers les vendeurs, et qui rembourse le client ? | Direction de l'expérience client ; direction marketplace ; Yanis Mercadier | non pour le lot 1 ; conditionne l'exigence 13 et le remboursement marketplace |
| Q12 | Est-il légal de réduire le montant remboursé selon la note C (voire B) ? Si oui, quels montants ? | Direction juridique et conformité | non (critère 6.3 maintenu tant qu'il n'y a pas de réponse) |
| Q13 | Le portail doit-il fonctionner sans compte, pour un client connecté, ou les deux ? Quelle vérification pour l'accès sans compte ? | Inès Rouvière ; direction de l'expérience client | non (exigence 1) |
| Q14 | Le RMA doit-il être imprimé par le client ? Que faire pour un client sans imprimante qui dépose avec un QR code ? | Karim Benhaddou ; Inès Rouvière | non (critère 4.3) |
| Q15 | Quelle est la date des soldes d'hiver visée et quel est le périmètre du pilote ? Une mise en service entre le 12 janvier et les soldes est-elle réaliste ? | Inès Rouvière ; direction de l'expérience client ; DSI | non (date du lot 1 et critère 11.9) |
| Q34 | L'hébergement doit-il être dans le cloud d'Orvanne, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non (critère 11.3) |
| Q36 | Quand la DPO peut-elle examiner le traitement du portail ? Exige-t-il une analyse d'impact ? | Hélène Marsac | non, mais conditionne l'ouverture aux clients (critère 11.6) |
| Q37 | La note A / B / C des retours est-elle saisie sur l'application douchette de P03 ? En V1 du portail ou plus tard ? | Karim Benhaddou ; Inès Rouvière | non (source de la note du critère 6.1 ; interface provisoire en lot 1) |
| Q39 | Quelle base de référence et quelle période de mesure pour la baisse de 60 % des contacts liés aux retours ? | Yanis Mercadier ; direction de l'expérience client | non (critère 10.1) |

Points relevés pendant la rédaction, sans question dans `work/analyse.json` (à ajouter au registre par l'analyste) :
- liste fermée des motifs de retour, non fournie (`B03-F6`) : critère 3.2 ;
- règle de choix de l'entrepôt de destination et horaire du fichier quotidien (`B03-F7`) : critères 8.1 et 8.2 ;
- périmètre de la correction par le service client (`B03-F9`) : critères 9.2 et 9.3 ;
- source de la date de livraison qui fait courir le délai (`B03-F5`) : critère 2.3 ;
- remontée de la réception des colis retour par Hangar (interface non décrite) : critère 5.3 ;
- conditions de l'accord de la finance sur le bon d'achat majoré et système d'émission du bon (`B04-F12`) : exigence 14.
