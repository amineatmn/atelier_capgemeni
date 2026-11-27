# Identifiants provisoires de l'essai P06 (B08)

<!-- Essai du rédacteur de spec sans étapes 1 et 2. Ces IDs remplacent provisoirement work/fiches/B08.json
     et la partie P06 de work/analyse.json. Numérotation dans l'ordre d'apparition dans le document.
     Les Cnn, Hnn et Qnn repartent de 01 pour l'essai : ils entreront en collision avec ceux des autres projets
     quand l'analyse globale existera.
     Reprise : citations vérifiées contre la source ; ajouts sans renumérotation : B08-D31 et D32, B08-N2 (citation),
     B08-N10 à N16, B08-F11 à F16, C06, H18 à H24, Q15 à Q17 ; renvoi de C04 vers B08-D31. -->

Document : `B08_compte-rendu-atelier_approvisionnement.md`, compte rendu d'atelier du 12 novembre 2026, rédigé par Inès Rouvière (DSI). Participants : Grégory Thibaudeau (approvisionnement et transport amont), Karim Benhaddou (exploitation E2), Nadège Courtois (achats), Rémi Vasseur (chef de quai E1).

## Demandes élémentaires

Le statut `demande` est attribué aux règles « validées » en séance (§ 2) et aux éléments de la V1 (§ 4). Les points débattus sans décision (§ 3) gardent le statut `demande` quand quelqu'un les réclame, et deviennent des conflits.

| Id | Type | Statut source | Priorité / échéance exprimée | Énoncé | Citation |
|---|---|---|---|---|---|
| B08-D1 | fonctionnelle | demande | V1 | Portail web sur lequel le fournisseur ou son transporteur réserve un créneau de déchargement | « Un portail web sur lequel le fournisseur ou son transporteur réserve un créneau de déchargement. » |
| B08-D2 | regle_metier | demande | V1 (R1) | Une réservation porte sur un ou plusieurs numéros de commande d'achat Orvanne, valides et non soldés | « R1 : une réservation porte sur un ou plusieurs numéros de commande d'achat Orvanne, valides et non soldés. » |
| B08-D3 | regle_metier | demande | V1 (R2) | Un créneau dure 30 minutes | « R2 : les créneaux durent 30 minutes » |
| B08-D4 | regle_metier | demande | V1 (R2) | Un camion complet consomme deux créneaux | « un camion complet consomme deux créneaux » |
| B08-D5 | regle_metier | demande | V1 (R3) | La réservation est possible de J-10 à J-1 midi | « R3 : la réservation est possible de J-10 à J-1 midi » |
| B08-D6 | regle_metier | demande | V1 (R3) | La modification et l'annulation sont possibles jusqu'à J-1 midi | « la modification ou l'annulation aussi, jusqu'à J-1 midi. » |
| B08-D7 | fonctionnelle | demande | V1 (R4) | Chaque site paramètre ses quais, ses horaires d'ouverture et ses jours fermés | « R4 : chaque site paramètre ses quais, ses horaires d'ouverture et ses jours fermés. » |
| B08-D8 | fonctionnelle | demande | V1 (R5) ; « à faire en V1 si possible » | Le poste de garde pointe le camion à son arrivée | « R5 : à l'arrivée, le poste de garde pointe le camion » |
| B08-D9 | regle_metier | demande | V1 (R5) | Retard toléré de 20 minutes ; au-delà, le créneau est perdu | « le retard toléré est de 20 minutes, au-delà le créneau est perdu. » |
| B08-D10 | fonctionnelle | demande | V1 (R6) | Envoi par e-mail au transporteur d'une confirmation, puis d'un rappel la veille | « R6 : une confirmation puis un rappel la veille sont envoyés par e-mail au transporteur. » |
| B08-D11 | fonctionnelle | demande | V1 (R7) | Le chef de quai peut forcer, déplacer ou bloquer un créneau | « R7 : le chef de quai peut forcer, déplacer ou bloquer un créneau. » |
| B08-D12 | indicateur | demande | — | Part des camions sans rendez-vous | « Indicateurs attendus : part des camions sans rendez-vous » |
| B08-D13 | indicateur | demande | — | Attente moyenne | « attente moyenne » |
| B08-D14 | indicateur | demande | — | Taux d'occupation des quais | « taux d'occupation des quais » |
| B08-D15 | indicateur | demande | — | Ponctualité par fournisseur | « ponctualité par fournisseur » |
| B08-D16 | fonctionnelle | v2 | V2 | La ponctualité alimente la notation des fournisseurs | « Les achats souhaitent que la ponctualité alimente la notation des fournisseurs » |
| B08-D17 | regle_metier | idee | « à terme » | La ponctualité donne lieu, à terme, à des pénalités pour les fournisseurs | « et, à terme, des pénalités. » |
| B08-D18 | regle_metier | demande | — | Créneaux d'une heure sur E2 (palettes hétérogènes à contrôler) | « Karim demande des créneaux d'une heure sur E2, où les livraisons sont surtout des palettes hétérogènes à contrôler. » |
| B08-D19 | contrainte | idee | — | Environ 15 % des livraisons viennent de fournisseurs étrangers qui n'ont pas tous un interlocuteur francophone | « Les fournisseurs étrangers (environ 15 % des livraisons) n'ont pas tous un interlocuteur francophone. » |
| B08-D20 | fonctionnelle | demande | « hors périmètre » (Grégory) / « indispensable » (Rémi) | Prise en compte des messageries et petits colis qui livrent sans commande d'achat identifiable | « Les messageries et petits colis livrent sans commande d'achat identifiable : hors périmètre pour Grégory, indispensable pour Rémi, qui les voit occuper un quai chaque matin. » |
| B08-D21 | fonctionnelle | v2 | V2 ; « bien mais pas vital » | Lien avec Hangar pour préremplir la réception attendue | « Un lien avec Hangar pour préremplir la réception attendue est jugé « bien mais pas vital ». » |
| B08-D22 | fonctionnelle | demande | V1 | Vue planning par site | « V1 : R1 à R7, vue planning par site, export des indicateurs. » |
| B08-D23 | fonctionnelle | demande | V1 | Export des indicateurs | « export des indicateurs » |
| B08-D24 | fonctionnelle | v2 | V2 | Application mobile pour les chauffeurs | « V2 : notation des fournisseurs, lien avec Hangar, application mobile pour les chauffeurs. » |
| B08-D25 | echeance | demande | « en V1 si possible » | Tout ce qui concerne le poste de garde est à faire en V1 si possible | « Tout ce qui concerne le poste de garde est à faire en V1 si possible. » |
| B08-D26 | echeance | demande | 27/11 | Les achats listent les fournisseurs pilotes (une vingtaine) | « Lister les fournisseurs pilotes (une vingtaine) » (responsable : Nadège Courtois) |
| B08-D27 | regle_metier | demande | 04/12 | Paramétrage cible de E1 : 4 quais de réception, créneaux d'une heure | « Paramétrage cible de E1 : 4 quais de réception, créneaux d'une heure » (responsable : Rémi Vasseur) |
| B08-D28 | echeance | demande | 27/11 | La DSI vérifie la disponibilité des commandes d'achat dans Passerelle | « Vérifier la disponibilité des commandes d'achat dans Passerelle » (responsable : Inès Rouvière) |
| B08-D29 | echeance | demande | décembre | La DSI produit le chiffrage et le planning | « Chiffrage et planning » (responsable : DSI) |
| B08-D30 | echeance | demande | « au printemps » | Démarrage du pilote sur E1 au printemps | « Démarrage du pilote souhaité sur E1 au printemps. » |
| B08-D31 | regle_metier | demande | — | L'approvisionnement préfère disposer d'une année d'historique avant d'utiliser la ponctualité pour noter ou pénaliser les fournisseurs (position opposée à `B08-D16` et `B08-D17`) | « L'approvisionnement préfère attendre une année d'historique. » |
| B08-D32 | fonctionnelle | demande | — | Visibilité, la veille, sur la charge de réception du lendemain (besoin implicite tiré d'un constat partagé) | « personne n'a de visibilité, la veille, sur la charge du lendemain. » |

## Chiffres

| Id | Libellé | Valeur | Citation |
|---|---|---|---|
| B08-N1 | Camions reçus par jour à E1 | ≈ 70 | « E1 reçoit environ 70 camions par jour sur 6 quais de réception » |
| B08-N2 | Quais de réception à E1 (situation actuelle) | 6 | « E1 reçoit environ 70 camions par jour sur 6 quais de réception » |
| B08-N3 | Camions reçus par jour à E2 | ≈ 40 | « E2 une quarantaine » |
| B08-N4 | Camions sans rendez-vous ou hors créneau | 1 sur 4 | « un camion sur quatre se présente sans rendez-vous ou hors créneau » |
| B08-N5 | Attente moyenne le lundi matin | > 1 h 30 | « l'attente moyenne dépasse 1 h 30 le lundi matin » |
| B08-N6 | Temps passé au téléphone par le bureau de réception | ≈ 3 h / jour | « le bureau de réception passe environ 3 heures par jour au téléphone » |
| B08-N7 | Part des livraisons de fournisseurs étrangers | ≈ 15 % | « Les fournisseurs étrangers (environ 15 % des livraisons) » |
| B08-N8 | Fournisseurs pilotes | ≈ 20 | « Lister les fournisseurs pilotes (une vingtaine) » |
| B08-N9 | Quais de réception à E1 (paramétrage cible) | 4 | « Paramétrage cible de E1 : 4 quais de réception » |
| B08-N10 | Durée d'un créneau (règle R2) | 30 minutes | « R2 : les créneaux durent 30 minutes » |
| B08-N11 | Créneaux consommés par un camion complet | 2 | « un camion complet consomme deux créneaux » |
| B08-N12 | Ouverture de la réservation avant le jour de livraison | J-10 | « R3 : la réservation est possible de J-10 à J-1 midi » |
| B08-N13 | Clôture de la réservation, de la modification et de l'annulation | J-1, 12 h | « la modification ou l'annulation aussi, jusqu'à J-1 midi. » |
| B08-N14 | Retard toléré à l'arrivée | 20 minutes | « le retard toléré est de 20 minutes » |
| B08-N15 | Durée de créneau demandée sur E2 | 1 heure | « Karim demande des créneaux d'une heure sur E2 » |
| B08-N16 | Durée de créneau du paramétrage cible de E1 | 1 heure | « Paramétrage cible de E1 : 4 quais de réception, créneaux d'une heure » |

## Points flous internes au document

| Id | Description | Citation |
|---|---|---|
| B08-F1 | R2 fixe 30 minutes et « Rémi tient aux 30 minutes », mais l'action confiée à Rémi fixe des créneaux d'une heure pour E1 | « Paramétrage cible de E1 : 4 quais de réception, créneaux d'une heure » |
| B08-F2 | E1 a 6 quais de réception aujourd'hui, le paramétrage cible en prévoit 4 ; le sort des 2 autres n'est pas dit | « sur 6 quais de réception » / « 4 quais de réception » |
| B08-F3 | R5 fait partie de la V1 (« R1 à R7 »), mais le poste de garde n'est en V1 que « si possible » | « Tout ce qui concerne le poste de garde est à faire en V1 si possible. » |
| B08-F4 | Le sort d'un camion dont le créneau est « perdu » n'est pas décrit | « au-delà le créneau est perdu » |
| B08-F5 | « J-1 midi » : veille calendaire ou jour ouvré (livraison du lundi) ? Fuseau horaire pour les fournisseurs étrangers ? | « de J-10 à J-1 midi » |
| B08-F6 | Le fournisseur ou le transporteur réserve, mais seul le transporteur reçoit les e-mails | « réserve un créneau de déchargement » / « envoyés par e-mail au transporteur » |
| B08-F7 | « Forcer » un créneau n'est pas défini | « le chef de quai peut forcer, déplacer ou bloquer un créneau » |
| B08-F8 | Les indicateurs ne sont pas définis (début et fin de l'attente, base de l'occupation, critère de ponctualité) | « Indicateurs attendus » |
| B08-F9 | Rien n'indique comment savoir qu'un camion est « complet » | « un camion complet consomme deux créneaux » |
| B08-F10 | E3 n'est pas mentionné ; seuls E1 et E2 sont décrits | « site E1 » / « E2 une quarantaine » |
| B08-F11 | Les constats sont chiffrés mais aucun objectif n'est fixé pour les indicateurs (part sans rendez-vous, attente, temps au téléphone) | « Indicateurs attendus : part des camions sans rendez-vous, attente moyenne, taux d'occupation des quais, ponctualité par fournisseur. » |
| B08-F12 | Mesurer la part des camions sans rendez-vous suppose de pointer aussi les camions sans réservation, ce que R5 ne décrit pas | « à l'arrivée, le poste de garde pointe le camion » |
| B08-F13 | La façon dont les fournisseurs et leurs transporteurs obtiennent un accès au portail n'est pas décrite | « le fournisseur ou son transporteur réserve un créneau de déchargement » |
| B08-F14 | Le format, la périodicité et les destinataires de l'export des indicateurs ne sont pas précisés | « export des indicateurs » |
| B08-F15 | Le paramétrage cible de E1 (4 quais, créneaux d'une heure) offre 4 camions par heure, soit environ 17 h 30 d'ouverture pour 70 camions par jour, sans compter les camions complets qui consomment deux créneaux | « E1 reçoit environ 70 camions par jour » / « 4 quais de réception, créneaux d'une heure » |
| B08-F16 | Les horaires d'ouverture et les jours fermés de chaque site ne sont pas donnés | « chaque site paramètre ses quais, ses horaires d'ouverture et ses jours fermés » |

## Contraintes transverses applicables

Reprises de `.kiro/steering/contraintes-transverses.md` : `CT-01` (avis de la DPO), `CT-03` (message de service sans offre commerciale, appliqué aux e-mails de confirmation et de rappel), `CT-04` (données de test anonymisées), `CT-07` (gel du 16/11 au 11/01), `CT-08` (hébergement dans le cloud d'Orvanne, UE). `CT-02`, `CT-05` et `CT-06` ne s'appliquent pas (pas de mobile client, pas de prospection, pas de photo).

Le commentaire du fichier de steering signale une future contrainte « fournisseurs non francophones (B08) ». Elle n'existe pas encore : elle est traitée ici par l'hypothèse `H09`.

## Conflits

| Id | Sujet | Positions | Gravité | Arbitre | Hypothèse | Question |
|---|---|---|---|---|---|---|
| C01 | Durée des créneaux | `B08-D3` : 30 minutes, règle validée ; Rémi Vasseur « tient aux 30 minutes » ; `B08-D18` : 1 heure sur E2 (Karim Benhaddou) ; `B08-D27` : 1 heure sur E1, dans l'action confiée à Rémi Vasseur | majeur | Grégory Thibaudeau (commanditaire), après avis de l'exploitation E1 et E2 | H01 | Q01 |
| C02 | Nombre de quais de réception de E1 | `B08-N2` : 6 quais aujourd'hui ; `B08-D27` : 4 quais dans le paramétrage cible | mineur | Rémi Vasseur (chef de quai E1) | H02 | Q02 |
| C03 | Messageries et petits colis sans commande d'achat | `B08-D2` et Grégory Thibaudeau (`B08-D20`) : hors périmètre, une réservation porte sur une commande d'achat ; Rémi Vasseur (`B08-D20`) : indispensable | majeur | Grégory Thibaudeau (commanditaire) | H03 | Q03 |
| C04 | Usage de la ponctualité pour noter et pénaliser les fournisseurs | Achats (`B08-D16`, `B08-D17`) : notation puis pénalités ; approvisionnement (`B08-D31`) : « L'approvisionnement préfère attendre une année d'historique. » ; § 4 : notation en V2 | mineur | Grégory Thibaudeau et Nadège Courtois (hiérarchie commune non identifiée dans B08) | H04 | Q04 |
| C05 | Poste de garde en V1 | `B08-D8` : R5 dans la V1 (« R1 à R7 ») ; `B08-D25` : poste de garde en V1 « si possible » | mineur | Grégory Thibaudeau, avec la DSI (Inès Rouvière) | H05 | Q05 |
| C06 | Capacité du paramétrage cible de E1 | `B08-N1` : environ 70 camions par jour à E1 ; `B08-D27` : 4 quais et des créneaux d'une heure, soit 4 camions par heure (voir `B08-F15`) | mineur | Rémi Vasseur (chef de quai E1), avec Grégory Thibaudeau | H18 | Q16 |

## Hypothèses

| Id | Hypothèse | Justification | Conflit | Réversible |
|---|---|---|---|---|
| H01 | La durée du créneau est un paramètre de site, 30 minutes par défaut (R2). Un camion complet consomme deux créneaux du site, quelle que soit leur durée. Passer E1 ou E2 à 1 heure ne demande aucun développement. | Respecte la règle validée tout en permettant les deux autres positions | C01 | oui |
| H02 | Le nombre de quais ouverts à la réservation est un paramètre de site ; un quai peut exister sans être ouvert à la réservation. E1 est initialisé avec la valeur fournie par le chef de quai le 04/12. | Aucune des deux valeurs n'est codée | C02 | oui |
| H03 | Les messageries et petits colis sans commande d'achat ne réservent pas sur le portail (R1 maintenu). Le chef de quai peut bloquer des créneaux de façon récurrente avec le motif « messagerie », et le poste de garde enregistre leurs arrivées dans une catégorie à part, pour mesurer le phénomène. | Ne contredit pas R1, répond en partie au besoin du quai, fournit des chiffres pour l'arbitrage | C03 | oui |
| H04 | Pas de notation ni de pénalité en V1. La ponctualité est calculée et exportable, et l'historique des réservations et des pointages est conservé au moins 13 mois, pour qu'une année d'historique soit disponible en V2. La durée définitive est fixée avec la DPO. | Prépare la V2 sans engager de conséquence contractuelle pour les fournisseurs | C04 | oui |
| H05 | Le pointage au poste de garde fait partie du lot pilote, car R5 et trois des quatre indicateurs en dépendent. | Sans pointage, ni la tolérance de 20 minutes ni les indicateurs ne sont calculables | C05 | oui |
| H06 | J-10 et J-1 sont comptés en jours calendaires par rapport au jour de livraison ; « midi » signifie 12 h 00, heure de Paris. Les deux bornes sont des paramètres de site. | Lecture littérale de R3, réglable si les métiers veulent des jours ouvrés | — | oui |
| H07 | Le réservant déclare si le camion est complet ou non ; le chef de quai peut corriger cette déclaration. | Les sources ne donnent aucun critère | — | oui |
| H08 | Les e-mails partent à l'adresse du transporteur saisie dans la réservation, avec copie au compte qui a réservé s'il est différent. Le rappel est envoyé la veille à 8 h 00, avant la clôture de midi, pour laisser le temps d'annuler ; l'heure est un paramètre. | R6 ne dit ni à qui écrire quand le fournisseur réserve, ni à quelle heure envoyer le rappel | — | oui |
| H09 | Le portail et les e-mails sont disponibles en français et en anglais ; la langue est choisie par compte. | Environ 15 % des livraisons viennent de fournisseurs sans interlocuteur francophone | — | oui |
| H10 | Au-delà de la tolérance, la réservation passe au statut « perdue » et ses créneaux sont libérés. Le camion est enregistré comme arrivé hors créneau ; le chef de quai peut le forcer sur un créneau libre. | B08 ne dit pas ce que devient le camion | — | oui |
| H11 | « Forcer » permet au chef de quai de créer ou d'affecter une réservation en dérogeant aux délais de R3 et à la tolérance de R5, avec un motif obligatoire. Un créneau qui porte une réservation ne peut être bloqué qu'après déplacement ou annulation de celle-ci. Chaque action du chef de quai sur une réservation déclenche un e-mail au transporteur. | Interprétation la plus restrictive de R7 | — | oui |
| H12 | Définitions des indicateurs : part sans rendez-vous = arrivées sans réservation valide (perdues comprises) / arrivées pointées ; attente = début de déchargement − la plus tardive de l'heure de pointage et de l'heure de début du créneau ; occupation = créneaux consommés par des camions déchargés / créneaux ouverts, blocages exclus ; ponctualité d'un fournisseur = réservations pointées au plus tard 20 minutes après le début du créneau / réservations non annulées. | B08 nomme les indicateurs sans les définir | — | oui |
| H13 | Le quai saisit le début et la fin de chaque déchargement dans la vue planning. | Nécessaire pour mesurer l'attente et l'occupation | — | oui |
| H14 | Les comptes fournisseurs sont créés par l'approvisionnement pour les fournisseurs habilités (la liste des achats pendant le pilote). Un fournisseur rattache ses transporteurs ; un transporteur ne voit que les commandes des fournisseurs qui l'ont rattaché. | B08 ne dit pas comment les tiers accèdent au portail | — | oui |
| H15 | Le système attribue un quai libre à chaque réservation ; le chef de quai peut la déplacer. | Le réservant n'a pas à connaître les quais | — | oui |
| H16 | Si les commandes d'achat ne peuvent pas être vérifiées auprès de Passerelle, le contrôle porte sur la dernière copie connue, la réservation est marquée « commande à revérifier » et un nouveau contrôle a lieu dès le retour du service. | Évite de bloquer toutes les réservations pendant une panne | — | oui |
| H17 | B08 ne donne pas de pic pour l'amont : la solution est dimensionnée pour le double des volumes actuels. Les créneaux disponibles s'affichent en moins de 2 secondes pour 95 % des recherches. | Prudence ; reprend le facteur du pic de fin d'année du glossaire | — | oui |
| H18 | Le paramétrage de E1 est saisi tel que le chef de quai le fournit. L'écran de paramétrage affiche la capacité qui en résulte (créneaux par jour et par quai, total du site), pour que le chef de quai la compare au volume attendu. | La capacité de 4 quais × 1 heure semble insuffisante pour 70 camions par jour, mais les horaires d'ouverture sont inconnus | C06 | oui |
| H19 | Le pointage enregistre l'heure d'arrivée et la réservation, ou, pour un camion sans réservation, le fournisseur ou le transporteur déclaré et une catégorie. Aucune donnée sur le chauffeur (nom, immatriculation) n'est collectée en V1. | Minimisation (CT-01) ; aucune source ne demande l'identité du chauffeur | — | oui |
| H20 | L'export des indicateurs est un fichier CSV, pour un site ou tous les sites et une période choisie, ventilé par jour et par demi-journée ; la ponctualité est détaillée par fournisseur. Les indicateurs de la veille sont calculés chaque nuit et disponibles à 6 h 00. | B08 demande un export sans en donner la forme ; la demi-journée rend visible l'attente du lundi matin | — | oui |
| H21 | Valeurs de service que B08 ne donne pas : confirmation envoyée dans les 5 minutes, vue planning à jour 60 secondes au plus après un enregistrement, portail disponible 7 j/7 à 99,5 % par mois hors maintenance programmée. | La clôture à J-1 midi tombe le dimanche pour une livraison du lundi ; valeurs prudentes à confirmer | — | oui |
| H22 | Une commande d'achat est acceptée si elle existe dans Passerelle, n'est pas soldée et appartient à un fournisseur auquel le réservant est rattaché ; si Passerelle fournit le site de livraison, il doit être celui de la réservation. Une même commande peut figurer dans plusieurs réservations (livraisons partielles). | R1 ne précise ni le contrôle du site ni les livraisons partielles | — | oui |
| H23 | Une modification de paramètre de site qui touche des réservations existantes (jour fermé, quai retiré, durée de créneau) n'est enregistrée qu'après déplacement ou annulation de ces réservations ; le système les liste. | Évite qu'une réservation confirmée devienne impossible sans que le transporteur soit prévenu | — | oui |
| H24 | Si une commande devient invalide après la réservation (soldée, annulée), la réservation n'est pas annulée automatiquement : le chef de quai et le réservant sont alertés et le chef de quai décide. | Une commande peut être soldée par une autre livraison ; l'annulation automatique risquerait de renvoyer un camion déjà parti | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q01 | Quelle durée de créneau par site : 30 minutes (R2), 1 heure sur E2, 1 heure sur E1 (paramétrage cible) ? Avec des créneaux d'une heure, un camion complet consomme-t-il toujours deux créneaux ? | Grégory Thibaudeau, Rémi Vasseur, Karim Benhaddou | non |
| Q02 | E1 ouvre-t-il 6 ou 4 quais à la réservation ? Les 2 autres sont-ils réservés aux messageries ou aux camions sans rendez-vous ? | Rémi Vasseur | non |
| Q03 | Les messageries et petits colis sans commande d'achat sont-ils dans le périmètre ? Si oui, comment les identifier et qui réserve pour eux ? | Grégory Thibaudeau | non |
| Q04 | Quelle durée d'historique conserver pour la future notation ? Les achats ont-ils besoin dès la V1 d'un export de la ponctualité par fournisseur ? | Grégory Thibaudeau, Nadège Courtois | non |
| Q05 | Le pointage au poste de garde est-il ferme dans le lot pilote ? Le poste de garde de E1 dispose-t-il d'un poste informatique ou d'une tablette ? | Grégory Thibaudeau, Inès Rouvière | non |
| Q06 | Passerelle expose-t-elle les commandes d'achat avec leur numéro, leur fournisseur, leur site de livraison et leur statut (soldée ou non), et avec quel délai de mise à jour ? | Inès Rouvière, équipe Passerelle (DSI) | oui (exigence 4) |
| Q07 | Que signifie « forcer » un créneau ? Que devient un camion dont le créneau est perdu ? | Rémi Vasseur | non |
| Q08 | Comment calculer l'attente moyenne (depuis l'arrivée ou depuis l'heure du créneau, jusqu'au début ou à la fin du déchargement) ? Cette définition correspond-elle à la base des pénalités d'immobilisation facturées par les transporteurs ? | Grégory Thibaudeau | non |
| Q09 | Comment reconnaît-on un camion complet (nombre de palettes, type de véhicule) ? | Rémi Vasseur, Grégory Thibaudeau | non |
| Q10 | Quels sont les horaires d'ouverture et les jours fermés de E1 et E2 ? J-1 s'entend-il en jour calendaire ou ouvré ? E3 est-il concerné ? | Rémi Vasseur, Karim Benhaddou, Grégory Thibaudeau | non |
| Q11 | Quand le fournisseur réserve, qui reçoit la confirmation et le rappel ? À quelle heure envoyer le rappel ? | Grégory Thibaudeau | non |
| Q12 | Quelles langues proposer aux fournisseurs étrangers, en plus du français ? | Nadège Courtois | non |
| Q13 | Quelle base légale et quelles durées de conservation pour les contacts des fournisseurs et transporteurs, les réservations et le journal ? | DPO | oui (mise en service, exigence 12) |
| Q14 | Qui crée et désactive les comptes des fournisseurs et des transporteurs ? | Grégory Thibaudeau, Nadège Courtois | non |
| Q15 | Quels objectifs chiffrés fixer pour la part des camions sans rendez-vous, l'attente moyenne et le temps passé au téléphone par le bureau de réception ? | Grégory Thibaudeau | non |
| Q16 | Avec 4 quais et des créneaux d'une heure, E1 offre 4 camions par heure : quels horaires d'ouverture permettent de recevoir les 70 camions par jour ? Une partie des camions (messageries, sans rendez-vous) passe-t-elle par d'autres quais ? | Rémi Vasseur, Grégory Thibaudeau | non |
| Q17 | Quel service d'envoi utiliser pour les e-mails transactionnels vers des destinataires externes (fournisseurs et transporteurs) ? | DSI (Inès Rouvière) | non |
