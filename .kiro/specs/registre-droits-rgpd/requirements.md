# Exigences : registre et traitement des demandes d'exercice de droits RGPD

<!-- Projet P05, slug registre-droits-rgpd. Commanditaire : direction juridique et conformité (DPO).
     Parties prenantes : DSI (comité d'architecture), service client, comité des risques. Source : B07.
     Dépendances : P01, P02, P03, P04, P06, P07 (nouveaux stockages de données personnelles à inscrire au catalogue des systèmes). -->

## Introduction

Les clients d'Orvanne demandent à accéder à leurs données, à les faire rectifier ou effacer, ou à s'opposer à la prospection. Ces demandes arrivent par l'adresse dédiée, par courrier, par le chat et par les réseaux sociaux. L'équipe de la DPO (2 personnes) les suit aujourd'hui dans un classeur partagé.

Sur les neuf premiers mois de 2026, Orvanne a enregistré 412 demandes, dont 61 % de demandes d'effacement. Dix-sept ont été traitées au-delà du délai légal d'un mois. La dernière revue interne a relevé qu'aucune preuve d'exécution n'est conservée et que les données restent dans le Lac et dans les sauvegardes après leur effacement dans Vitrine.

Le projet remplace le classeur par un registre unique qui suit l'échéance de chaque demande, trace les actions réalisées dans chaque système, conserve la preuve de clôture, remet les exports d'accès et produit un tableau de bord trimestriel pour le comité des risques.

Le projet est livré en deux lots (`H31`) :
- **Lot 1** (exigences 1 à 11) : registre, compte à rebours, saisie par le service client, traçabilité manuelle des actions dans chaque système, effacement avec isolation des données légales, export d'accès, tableau de bord. Il est attendu avant le prochain contrôle interne, dont la date n'est pas connue (`Q30`). Le gel des mises en production du 16 novembre au 11 janvier (`CT-07`) commence une semaine après la note B07 : la mise en production du lot 1 a donc lieu au plus tôt le 12 janvier 2027.
- **Lot 2** (exigence 12) : orchestration automatisée des actions dans Vitrine, Comptoir, Hangar, le Lac, l'outil d'e-mailing et les nouveaux systèmes.

## Glossaire

- **Demande** : demande d'exercice de droits adressée par une personne à Orvanne (accès, rectification, effacement, opposition à la prospection).
- **Demandeur** : personne qui exerce ses droits ; en général un client.
- **Équipe de la DPO** : la déléguée à la protection des données et son équipe (2 personnes), qui instruisent et clôturent les demandes.
- **Échéance** : date limite de réponse, à un mois de la date de réception, ou plus tard en cas de prolongation.
- **Prolongation** : report motivé de l'échéance de deux mois.
- **Catalogue des systèmes** : liste des systèmes d'Orvanne qui stockent des données clients, avec leur responsable et leur mode de traitement (`manuel` ou `automatisé`).
- **Système concerné** : système du catalogue dans lequel une action doit être réalisée pour une demande.
- **Action** : opération réalisée dans un système concerné (extraction, rectification, suppression, anonymisation, conservation légale, opposition enregistrée, aucune donnée trouvée), avec son auteur, sa date et sa preuve.
- **Donnée isolée** : donnée conservée malgré un effacement au titre d'une obligation légale (exemple : factures, 10 ans), avec sa date de fin de conservation.
- **Preuve de clôture** : document ou référence qui atteste la réponse apportée au demandeur et l'exécution de la demande.
- **Export d'accès** : document lisible qui rassemble les données d'un demandeur, remis par un canal sécurisé.

## Exigences

### Exigence 1 : registre unique des demandes (lot 1)

**User story :** En tant que membre de l'équipe de la DPO, je veux enregistrer toutes les demandes dans un registre unique, afin de ne plus dépendre d'un classeur partagé et de savoir à tout moment où en est chaque demande.

#### Critères d'acceptation

1. LE SYSTÈME DOIT enregistrer chaque demande avec son canal, sa date de réception, son type, l'état de vérification de l'identité, les systèmes concernés, son échéance, son statut et sa preuve de clôture. _Source : B07-D1_
2. LE SYSTÈME DOIT proposer pour le canal une liste paramétrable, initialisée avec l'adresse dédiée, le courrier, le chat et les réseaux sociaux. _Source : B07-D1, B07-D18_
3. LE SYSTÈME DOIT proposer pour le type une liste paramétrable, initialisée avec l'accès, la rectification, l'effacement et l'opposition à la prospection. _Source : B07-D1_
4. LE SYSTÈME DOIT attribuer à chaque demande un identifiant unique, jamais réutilisé. _Source : B07-D1_
5. LE SYSTÈME DOIT gérer les statuts `reçue`, `en cours`, `prolongée` et `clôturée`, et enregistrer chaque changement de statut avec son auteur et son horodatage. _Source : B07-D1, CT-10_
6. LE SYSTÈME DOIT enregistrer pour la vérification d'identité son état (`non vérifiée` ou `vérifiée`), le moyen utilisé choisi dans une liste paramétrable, son auteur et sa date. _Source : B07-D1_
7. LE SYSTÈME DOIT permettre de rechercher une demande par identifiant, nom ou adresse e-mail du demandeur, type, statut, canal et période de réception. _Source : B07-D1, B07-D17_
8. LE SYSTÈME DOIT permettre d'importer les demandes non clôturées du classeur partagé actuel en conservant leur date de réception d'origine. _Source : B07-D1_
9. SI une demande est créée pour un demandeur qui a déjà une demande non clôturée du même type, ALORS LE SYSTÈME DOIT afficher un avertissement avec un lien vers la demande existante, sans bloquer la création. _Source : B07-D1_

### Exigence 2 : catalogue des systèmes concernés (lot 1)

**User story :** En tant que membre de l'équipe de la DPO, je veux une liste à jour des systèmes qui stockent des données clients, afin de n'oublier aucun système lors du traitement d'une demande.

#### Critères d'acceptation

1. LE SYSTÈME DOIT tenir un catalogue des systèmes stockant des données clients, initialisé avec Vitrine, Comptoir, Hangar, le Lac et l'outil d'e-mailing. _Source : B07-D5, B07-D1_
2. LE SYSTÈME DOIT permettre à l'équipe de la DPO d'ajouter, de modifier ou de désactiver un système du catalogue sans nouvelle mise en production, en indiquant son responsable et son mode de traitement (`manuel` ou `automatisé`). _Source : B07-D5, H31_
3. QUAND une demande est créée, LE SYSTÈME DOIT proposer comme systèmes concernés tous les systèmes actifs du catalogue, chaque retrait d'un système exigeant un motif. _Source : B07-D1, B07-D5_

### Exigence 3 : compte à rebours et alertes (lot 1)

**User story :** En tant que membre de l'équipe de la DPO, je veux être alertée avant l'échéance de chaque demande, afin qu'aucune demande ne soit plus traitée au-delà du délai légal.

#### Critères d'acceptation

1. QUAND une demande est créée, LE SYSTÈME DOIT fixer son échéance à un mois après sa date de réception, décompté en jours calendaires. _Source : B07-D4, H29_
2. LE SYSTÈME DOIT afficher pour chaque demande non clôturée le nombre de jours calendaires restant avant l'échéance. _Source : B07-D2, H29_
3. QUAND une demande non clôturée atteint J+15 après sa date de réception, LE SYSTÈME DOIT envoyer une alerte à l'équipe de la DPO. _Source : B07-D2, H29_
4. QUAND une demande non clôturée atteint J+25 après sa date de réception, LE SYSTÈME DOIT envoyer une seconde alerte à l'équipe de la DPO et marquer la demande comme urgente dans les listes. _Source : B07-D2, H29_
5. SI l'échéance d'une demande est dépassée sans clôture, ALORS LE SYSTÈME DOIT marquer la demande « hors délai », alerter l'équipe de la DPO et conserver ce marquage après la clôture. _Source : B07-D4, B07-D2_
6. LE SYSTÈME DOIT permettre à un administrateur de l'équipe de la DPO de modifier le délai de réponse et les seuils d'alerte sans nouvelle mise en production, chaque modification étant journalisée. _Source : H29, CT-10_
7. LE SYSTÈME DOIT afficher en page d'accueil les demandes non clôturées triées par échéance croissante. _Source : B07-D2, B07-D17_

### Exigence 4 : prolongation du délai (lot 1)

**User story :** En tant que membre de l'équipe de la DPO, je veux prolonger le délai d'une demande complexe en motivant ma décision, afin de rester dans le cadre légal et d'en garder la trace.

#### Critères d'acceptation

1. QUAND un membre de l'équipe de la DPO prolonge une demande, LE SYSTÈME DOIT exiger un motif écrit, passer la demande au statut `prolongée` et journaliser la décision. _Source : B07-D3, CT-10_
2. QUAND une demande est prolongée, LE SYSTÈME DOIT calculer la nouvelle échéance selon le paramètre de prolongation, fixé par défaut à deux mois ajoutés à l'échéance initiale. _Source : B07-D3, H29_
3. QUAND une demande est prolongée, LE SYSTÈME DOIT recalculer ses alertes selon les seuils paramétrés pour les demandes prolongées. _Source : H29_
4. LE SYSTÈME NE DOIT PAS permettre de prolonger une demande de plus de deux mois au total. _Source : B07-D3_
5. LE SYSTÈME DOIT réserver la prolongation aux membres de l'équipe de la DPO. _Source : B07-D3, B07-D18_

### Exigence 5 : enregistrement des demandes par le service client (lot 1)

**User story :** En tant que conseiller du service client, je veux enregistrer dans le registre une demande reçue sur mes canaux, afin qu'elle soit traitée dans le délai par l'équipe de la DPO.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à un conseiller du service client d'enregistrer une demande avec son canal, sa date de réception, son type et le message d'origine du demandeur, en texte ou en pièce jointe. _Source : B07-D18_
2. QUAND un conseiller enregistre une demande, LE SYSTÈME DOIT retenir comme date de réception la date d'envoi du message du demandeur, et non la date de saisie. _Source : B07-D18, H29_
3. QUAND un conseiller enregistre une demande, LE SYSTÈME DOIT notifier l'équipe de la DPO. _Source : B07-D18_
4. LE SYSTÈME DOIT limiter l'accès du service client à la création des demandes et à la consultation de leur statut et de leur échéance, sans accès aux pièces d'identité, aux exports ni aux preuves. _Source : B07-D18, B07-D6, CT-01_
5. OÙ l'intégration avec Comptoir est disponible, LE SYSTÈME DOIT permettre l'enregistrement d'une demande depuis Comptoir sans ressaisir l'identité ni les coordonnées du client. _Source : B07-D18, B07-D20_

### Exigence 6 : traçabilité des actions et clôture (lot 1)

**User story :** En tant que membre de l'équipe de la DPO, je veux tracer chaque action réalisée dans chaque système et conserver la preuve de clôture, afin de démontrer l'exécution effective lors d'un contrôle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT enregistrer, pour chaque système concerné d'une demande, l'action réalisée, son auteur, sa date et une preuve sous forme de pièce jointe ou de référence. _Source : B07-D1, H31, CT-10_
2. LE SYSTÈME DOIT proposer les actions selon le type de demande : extraction pour l'accès, rectification, suppression, anonymisation ou conservation légale pour l'effacement, opposition enregistrée pour l'opposition, et « aucune donnée trouvée » pour tous les types. _Source : B07-D6, B07-D7, H31_
3. SI au moins un système concerné n'a pas d'action enregistrée, ALORS LE SYSTÈME DOIT refuser la clôture de la demande et indiquer les systèmes manquants. _Source : B07-D1, CT-10_
4. QUAND un membre de l'équipe de la DPO clôture une demande, LE SYSTÈME DOIT exiger une preuve de clôture et une issue, `exécutée` ou `non exécutée` avec un motif. _Source : B07-D1_
5. SI l'identité du demandeur n'est pas vérifiée, ALORS LE SYSTÈME DOIT refuser la clôture avec l'issue `exécutée`. _Source : B07-D1_
6. QUAND une demande est clôturée, LE SYSTÈME DOIT interdire la modification de la demande, de ses actions et de ses preuves, toute correction ultérieure étant ajoutée comme un complément daté et signé par son auteur. _Source : B07-D1, CT-10_

### Exigence 7 : effacement et isolation des données à conserver (lot 1)

**User story :** En tant que membre de l'équipe de la DPO, je veux distinguer les données supprimées, anonymisées et conservées au titre d'une obligation légale, afin d'effacer tout ce qui peut l'être sans enfreindre les obligations de conservation.

#### Critères d'acceptation

1. QUAND une action est enregistrée pour une demande d'effacement, LE SYSTÈME DOIT exiger son mode : suppression, anonymisation ou conservation au titre d'une obligation légale. _Source : B07-D7_
2. SI des données sont conservées au titre d'une obligation légale, ALORS LE SYSTÈME DOIT exiger leur catégorie, l'obligation légale invoquée et leur date de fin de conservation. _Source : B07-D8_
3. LE SYSTÈME DOIT proposer une liste paramétrable des obligations légales de conservation, initialisée avec les factures et une durée de 10 ans. _Source : B07-D8_
4. QUAND la date de fin de conservation d'une donnée isolée est atteinte, LE SYSTÈME DOIT alerter l'équipe de la DPO pour achever l'effacement. _Source : B07-D7, B07-D8_
5. LE SYSTÈME NE DOIT PAS permettre de retirer le Lac des systèmes concernés d'une demande d'effacement. _Source : B07-D5, B07-D7_

### Exigence 8 : export d'accès remis par un canal sécurisé (lot 1)

**User story :** En tant que demandeur, je veux recevoir mes données dans un document lisible, par un moyen sûr, afin de savoir ce qu'Orvanne détient sur moi sans risque qu'un tiers y accède.

#### Critères d'acceptation

1. QUAND toutes les extractions d'une demande d'accès sont enregistrées, LE SYSTÈME DOIT constituer un export unique, lisible sans outil technique, qui présente les données par système avec des libellés en français. _Source : B07-D6_
2. LE SYSTÈME NE DOIT PAS remettre un export tant que l'identité du demandeur n'est pas vérifiée. _Source : B07-D6, B07-D1_
3. LE SYSTÈME DOIT remettre l'export par un lien de téléchargement personnel, valable pendant une durée paramétrable, dont l'ouverture exige un code de vérification transmis séparément du lien. _Source : B07-D6_
4. SI le lien expire sans téléchargement, ALORS LE SYSTÈME DOIT le désactiver et alerter l'équipe de la DPO. _Source : B07-D6_
5. QUAND le demandeur télécharge l'export, LE SYSTÈME DOIT enregistrer la date et l'heure du téléchargement comme preuve de remise. _Source : B07-D6, CT-10_
6. OÙ la demande a été reçue par courrier, LE SYSTÈME DOIT permettre d'enregistrer une remise par courrier, avec la référence d'envoi comme preuve. _Source : B07-D6, B07-D1_
7. LE SYSTÈME DOIT supprimer le fichier d'export à l'issue d'un délai paramétrable après sa remise ou l'expiration du lien, en conservant uniquement la preuve de remise et l'empreinte du fichier. _Source : B07-D6, CT-01_

### Exigence 9 : tableau de bord trimestriel pour le comité des risques (lot 1)

**User story :** En tant que membre du comité des risques, je veux un tableau de bord trimestriel des demandes, afin de suivre le respect des délais et la conformité du traitement.

#### Critères d'acceptation

1. LE SYSTÈME DOIT produire pour chaque trimestre civil un tableau de bord indiquant au minimum, par type et par canal : les demandes reçues, clôturées, en cours, prolongées et traitées hors délai, ainsi que le délai médian de traitement. _Source : B07-D9, B07-D4, B07-D3_
2. LE SYSTÈME DOIT indiquer dans le tableau de bord le nombre de demandes clôturées sans preuve d'exécution pour au moins un système, issues de l'import du classeur. _Source : B07-D9, B07-D1_
3. LE SYSTÈME NE DOIT PAS faire figurer de donnée personnelle dans le tableau de bord. _Source : B07-D9, CT-01_
4. LE SYSTÈME DOIT permettre l'export du tableau de bord au format PDF et donner au comité des risques un accès en lecture limité à ce seul tableau de bord. _Source : B07-D9, CT-01_

### Exigence 10 : prise en main sans formation lourde (lot 1)

**User story :** En tant que membre de l'équipe de la DPO ou conseiller du service client, je veux un outil simple, afin de l'utiliser sans formation lourde.

#### Critères d'acceptation

1. LE SYSTÈME DOIT permettre à chaque membre de l'équipe de la DPO de réaliser sans assistance, avec pour seul support l'aide intégrée aux écrans, les scénarios de recette : enregistrer, vérifier l'identité, prolonger, tracer une action, clôturer, remettre un export. _Source : B07-D17_
2. LE SYSTÈME DOIT permettre à un conseiller du service client d'enregistrer une demande sans assistance, avec pour seul support l'aide intégrée à l'écran de saisie. _Source : B07-D17, B07-D18_
3. LE SYSTÈME DOIT présenter les écrans en français, avec les termes du glossaire de cette spec pour les types, statuts et actions. _Source : B07-D17_

### Exigence 11 : sécurité, conservation et hébergement (lot 1)

**User story :** En tant que DPO, je veux que le registre protège les données qu'il contient et garde la trace de chaque opération, afin qu'il soit lui-même conforme et opposable lors d'un contrôle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT journaliser, sans possibilité de modification ni de suppression par les utilisateurs, toute consultation, création, modification, prolongation, action, clôture et remise d'export, avec l'utilisateur et l'horodatage. _Source : CT-10, B07-D1_
2. LE SYSTÈME DOIT restreindre les accès selon quatre rôles : équipe de la DPO, administrateur de l'équipe de la DPO, service client et comité des risques. _Source : CT-01, B07-D18, B07-D9_
3. LE SYSTÈME DOIT chiffrer les pièces jointes, les preuves et les exports au repos et en transit. _Source : B07-D6, CT-01_
4. LE SYSTÈME DOIT conserver chaque demande clôturée pendant une durée paramétrable fixée par la DPO, puis la supprimer avec ses pièces jointes et ses preuves. _Source : CT-01, B07-D1_
5. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_
6. LE SYSTÈME DOIT authentifier les utilisateurs internes par l'authentification interne existante d'Orvanne, sans compte propre à l'outil. _Source : B07-D20_
7. LE SYSTÈME DOIT utiliser exclusivement des données synthétiques ou anonymisées dans les environnements de développement, de test et de démonstration. _Source : CT-04_

### Exigence 12 : orchestration des actions dans les systèmes (lot 2)

**User story :** En tant que membre de l'équipe de la DPO, je veux que le registre déclenche lui-même les actions dans les systèmes concernés et en recueille la preuve, afin de réduire les manipulations et les oublis.

#### Critères d'acceptation

1. OÙ un système du catalogue est en mode `automatisé`, LE SYSTÈME DOIT lui transmettre l'action correspondant au type de demande, après vérification de l'identité et validation de la liste des systèmes concernés par un membre de l'équipe de la DPO. _Source : B07-D5, B07-D7, H31_
2. OÙ l'orchestration est active, LE SYSTÈME DOIT couvrir Vitrine, Comptoir, Hangar, le Lac et l'outil d'e-mailing. _Source : B07-D5_
3. QUAND un système automatisé renvoie le compte rendu d'une action, LE SYSTÈME DOIT l'enregistrer comme action et preuve pour ce système. _Source : B07-D5, CT-10_
4. SI un système automatisé signale une erreur ou ne renvoie pas de compte rendu dans le délai paramétré, ALORS LE SYSTÈME DOIT alerter l'équipe de la DPO et repasser l'action en traitement manuel. _Source : B07-D5, H31_
5. QUAND une demande d'effacement est orchestrée, LE SYSTÈME DOIT transmettre à chaque système les catégories de données à isoler au titre d'une obligation légale. _Source : B07-D8, B07-D5_
6. QUAND une demande d'accès est orchestrée, LE SYSTÈME DOIT intégrer à l'export d'accès les extractions renvoyées par les systèmes. _Source : B07-D5, B07-D6_
7. QUAND une demande d'opposition à la prospection est orchestrée, LE SYSTÈME DOIT transmettre l'opposition à l'outil d'e-mailing. _Source : B07-D5_
8. LE SYSTÈME DOIT publier un contrat d'interface unique, que tout nouveau système stockant des données clients implémente pour passer en mode `automatisé`. _Source : B07-D5_

## Hors périmètre

- Première version avant le prochain contrôle interne (`B07-D19`) : échéance de projet, pas une exigence du système. Elle fixe le lot 1 (introduction et `tasks.md`) ; sa date dépend de `Q30` et du gel `CT-07`.
- Soumission de tout nouveau traitement à la DPO (`B07-D10`) : règle transverse portée par `CT-01`, appliquée par chaque projet. Le registre lui-même y est soumis (tâche 1.1).
- Usage du numéro de mobile (`B07-D11`) : règle portée par `CT-02`. Le registre n'utilise pas le mobile, y compris pour transmettre le code de l'export.
- Absence d'offre commerciale dans un message de service (`B07-D12`) : règle portée par `CT-03`.
- Conservation des données de prospection 3 ans au plus (`B07-D13`) : règle portée par `CT-05`, appliquée par P04.
- Purge des historiques de prospection de plus de 3 ans (`B07-D14`) : chantier sans porteur ni échéance, distinct de l'outil de registre (`Q31`). Aucun projet ne le reprend à ce jour.
- Photos et pièces jointes comme données personnelles (`B07-D15`) : règle portée par `CT-06`, appliquée par P02 et P03. Leurs stockages entreront au catalogue des systèmes (exigence 2).
- Données de production pour les démonstrations et les tests (`B07-D16`) : règle portée par `CT-04`, appliquée au registre par le critère 11.7.
- Repérage automatique des demandes arrivant par le chat ou les réseaux sociaux : la note B07 constate le problème (`B07-F2`) sans demander de fonction. Le projet fournit la saisie par le service client (exigence 5).
- Traitement des sauvegardes lors d'un effacement : le constat le signale, mais le traitement attendu n'est pas décrit (`B07-F1`). Il reste à spécifier après la réponse à `Q30`.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H29 | Le compte à rebours d'une demande de droits part de sa date de réception, en jours calendaires ; les seuils d'alerte (J+15, J+25) et l'échéance après prolongation sont des paramètres. | — | oui |
| H31 | La V1 du registre, attendue avant le prochain contrôle interne, couvre le registre, le compte à rebours, la saisie par le service client, la preuve de clôture, l'export d'accès et le tableau de bord ; les actions dans chaque système sont tracées manuellement. L'orchestration automatisée dans Vitrine, Comptoir, Hangar, le Lac et l'outil d'e-mailing (B07-D5) vient en V2. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q30 | Quelle est la date du prochain contrôle interne ? Le compte à rebours part-il de la réception ou de la vérification d'identité ? Comment traiter le Lac et les sauvegardes lors d'un effacement ? | Hélène Marsac | non (date du lot 1 ; traitement des sauvegardes non spécifié, voir Hors périmètre) |
| Q31 | Qui porte la purge des historiques de prospection de plus de 3 ans, et pour quelle échéance ? | Hélène Marsac ; Capucine Lorrain | non |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne (B01) s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis (B03, B07-D20) ? | DSI (comité d'architecture) | non (critère 11.5) |

### Points à remonter à l'analyste (sans question dans `work/analyse.json`)

Ces points flous de la fiche B07 n'ont pas de question associée. La spec les traite par un paramètre ou une valeur prudente, à faire confirmer par la DPO :

- **Moyens de vérification de l'identité** (`B07-F3`) : liste paramétrable (critère 1.6). Les critères 6.5 et 8.2 interdisent une clôture `exécutée` et la remise d'un export sans identité vérifiée ; ce choix prudent est à confirmer.
- **Canal sécurisé et format de l'export** (`B07-F4`) : lien personnel à durée limitée et code transmis séparément (critère 8.3), document lisible (critère 8.1). Mécanisme proposé, à valider.
- **Choix entre suppression et anonymisation** (`B07-F7`) : laissé à l'appréciation de l'équipe de la DPO, action par action (critère 7.1).
- **Contenu du tableau de bord trimestriel** (`B07-F9`) : indicateurs minimaux déduits du constat de B07 (critères 9.1 et 9.2), à valider.
- **Rectification et opposition** (`B07-F15`) : traitées par le même circuit que les autres types, sans règle propre.
- **Échéance du lot 1 et gel** : si le prochain contrôle interne a lieu avant le 12 janvier 2027, `B07-D19` entre en conflit avec `CT-07`. Ce conflit n'est pas enregistré dans l'analyse.
- **Localisation des factures à isoler** (`B07-D8`) : le système qui les détient n'est pas cité.
- **Durée de conservation du registre lui-même** et délai de suppression des exports (critères 8.7 et 11.4) : paramètres à fixer par la DPO.
