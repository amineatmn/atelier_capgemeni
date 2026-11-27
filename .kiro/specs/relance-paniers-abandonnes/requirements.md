# Exigences : relance personnalisée des paniers abandonnés

<!-- Projet P04, slug relance-paniers-abandonnes. Commanditaire : marketing (CRM et fidélité).
     Parties prenantes : DSI, équipe du Lac, direction juridique et conformité (DPO), finance, comité commerce.
     Sources : B05 (demandes), B07 (règles de conformité, via CT-01, CT-02, CT-04, CT-05), B02 (gel, via CT-07). -->

## Introduction

Aujourd'hui, Orvanne envoie le même e-mail de relance à tous les clients 24 heures après l'abandon de leur panier, et cette relance convertit « à 2 et quelques % » (B05-N1, B05-N2). Le marketing veut une relance qui choisit, pour chaque client, le message, le moment, le canal et, si le client hésite, une remise plafonnée à 10 % (15 % pour les membres Orvanne+). Il demande aussi un tableau du chiffre d'affaires incrémental et une démonstration pour le comité commerce du 8 décembre 2026.

Plusieurs points de la demande sont contestés ou encadrés par des règles de conformité :
- la DPO n'a pas été consultée et le consentement newsletter n'est pas réputé couvrir ce traitement (`C18`, `CT-01`, `CT-02`) ;
- l'historique d'achats depuis 2014 dépasse la limite de 3 ans des données de prospection (`C19`, `CT-05`) ;
- la démonstration sur les données des vrais clients est interdite sans anonymisation (`C20`, `CT-04`) ;
- la nature de « l'IA » n'est pas tranchée et les données réellement disponibles sont incertaines (B05-F1, B05-F2).

Le projet est donc découpé en trois lots :
- **Lot 0** (exigence 7) : démonstration pour le comité commerce du 8 décembre 2026, sur un environnement hors production et des données synthétiques ou anonymisées. Ce n'est pas une mise en production, le gel ne s'y applique pas (`H19`).
- **Lot 1** (exigences 1 à 6 et 9) : relance par règles paramétrables et explicables, par e-mail seulement, avec remise plafonnée et mesure du CA incrémental (`H17`, `H30`). Mise en production au plus tôt le 12 janvier 2027, après le gel du 16 novembre au 11 janvier (`CT-07`) et après l'avis de la DPO (`CT-01`).
- **Lot 2** (exigence 8 et options de l'exigence 5) : modèle d'IA et canaux supplémentaires (notifications de l'application, SMS, messageries mobiles), après l'avis de la DPO et la confirmation des données disponibles (`H17`, `H30`).

## Glossaire

- **Panier abandonné** : panier constitué sur Vitrine par un client identifié et non transformé en commande. Le système qui détecte l'abandon et le délai retenu sont à confirmer (voir « Points à remonter »).
- **Relance** : message commercial envoyé au client à propos de son panier abandonné. C'est de la prospection : elle suppose le consentement du client, contrairement à un message de service (`CT-03` ne s'y applique pas).
- **Relance actuelle** : même e-mail envoyé à tous, 24 heures après l'abandon.
- **Règle de relance** : règle paramétrée par le marketing qui associe des critères (contenu du panier, historique de commandes, navigation) à un modèle de message, un délai d'envoi et un canal.
- **Règle de remise** : règle paramétrée par le marketing qui désigne les paniers recevant une remise et fixe son taux.
- **Plafond de remise** : taux maximal de remise par catégorie de client : 10 % en général, 15 % pour les membres Orvanne+ (valeurs provisoires, `Q33`).
- **Groupe témoin** : part des paniers, tirée au hasard, qui reçoit la relance actuelle (ou la relance sans remise pour les règles de remise), afin de mesurer l'effet du nouveau dispositif.
- **CA incrémental** : chiffre d'affaires supplémentaire attribuable au nouveau dispositif par rapport au groupe témoin, remises déduites.
- **Dernier contact** : date de référence de la limite de 3 ans des données de prospection ; sa définition est à fixer avec la DPO (`Q19`).
- **Décideur** : composant qui choisit message, moment, canal et remise. En lot 1, ce sont les règles ; en lot 2, un modèle d'IA peut le remplacer.
- **Avis de la DPO** : avis écrit de la déléguée à la protection des données, enregistré dans le paramétrage du système, qui conditionne l'activation d'un traitement ou d'un canal.

## Exigences

### Exigence 1 : éligibilité d'un panier à la relance (lot 1)

**User story :** En tant que chargée de CRM, je veux que seuls les paniers abandonnés de clients qui ont accepté la prospection soient relancés, afin de respecter leurs choix et de ne pas relancer un panier déjà commandé.

#### Critères d'acceptation

1. QUAND un panier abandonné est signalé par Vitrine, LE SYSTÈME DOIT l'enregistrer comme candidat à la relance, avec l'identifiant du client, les articles, le montant et l'horodatage d'abandon. _Source : B05-D1_
2. SI le panier n'est rattaché à aucun client identifié disposant d'une adresse e-mail, ALORS LE SYSTÈME NE DOIT PAS programmer de relance. _Source : B05-D1, H17_
3. SI le consentement enregistré du client ne couvre pas la prospection par e-mail, selon la portée validée par la DPO, ALORS LE SYSTÈME NE DOIT PAS programmer de relance. _Source : B05-D9, H17, CT-01_
4. SI le client s'est opposé à la prospection, ALORS LE SYSTÈME NE DOIT PAS programmer de relance. _Source : H17, CT-01_
5. LE SYSTÈME DOIT vérifier de nouveau, au moment de l'envoi, le consentement, l'absence d'opposition et l'absence de commande du panier. _Source : B05-D1, H17_
6. SI le panier a été transformé en commande avant l'heure d'envoi, ALORS LE SYSTÈME DOIT annuler la relance programmée. _Source : B05-D1_
7. LE SYSTÈME DOIT envoyer au plus une relance par panier abandonné. _Source : B05-D1_

### Exigence 2 : choix du message, du moment et du canal par règles (lot 1)

**User story :** En tant que chargée de CRM, je veux définir moi-même des règles qui choisissent le message, le moment et le canal de chaque relance, afin de remplacer la relance unique par une relance adaptée à chaque client.

#### Critères d'acceptation

1. LE SYSTÈME DOIT choisir, pour chaque panier éligible, un modèle de message, un délai d'envoi et un canal, en appliquant la première règle active qui s'applique dans l'ordre de priorité défini par le marketing. _Source : B05-D1, H30_
2. SI aucune règle active ne s'applique au panier, ALORS LE SYSTÈME DOIT appliquer la relance par défaut : e-mail, modèle par défaut, 24 heures après l'abandon. _Source : B05-D1, H30_
3. LE SYSTÈME DOIT permettre au marketing de créer, modifier, tester sur un échantillon de paniers, activer et désactiver une règle de relance ou un modèle de message, sans mise en production. _Source : B05-D1, H30_
4. LE SYSTÈME DOIT refuser l'enregistrement d'une règle qui utilise un critère hors des données autorisées par l'exigence 4. _Source : B05-D3, H18_
5. QUAND une relance est programmée, LE SYSTÈME DOIT enregistrer la règle appliquée et sa version, le modèle de message, l'heure d'envoi prévue, le canal et la remise éventuelle. _Source : H30_
6. LE SYSTÈME DOIT envoyer chaque relance à l'heure prévue, avec un écart inférieur à la tolérance paramétrée. _Source : B05-D1_
7. LE SYSTÈME DOIT conserver l'historique des versions de chaque règle et de chaque modèle de message, avec leur auteur et leur date d'activation. _Source : H30_

### Exigence 3 : remise ciblée et plafonnée (lot 1)

**User story :** En tant que responsable marketing, je veux proposer une remise au client qui hésite, mais pas à celui qui aurait acheté sans elle, afin d'augmenter les ventes sans distribuer de remises inutiles.

#### Critères d'acceptation

1. LE SYSTÈME NE DOIT PAS proposer de remise à un panier qu'aucune règle de remise active ne désigne. _Source : B05-D5, H30_
2. QUAND une règle de remise active désigne un panier, LE SYSTÈME DOIT joindre à la relance une remise au taux fixé par la règle, utilisable sur Vitrine par ce seul client. _Source : B05-D5_
3. LE SYSTÈME DOIT refuser l'activation d'une règle de remise dont le taux dépasse le plafond de la catégorie de client visée : 10 % en général, 15 % pour les membres Orvanne+. _Source : B05-D6_
4. QUAND un plafond de remise est abaissé, LE SYSTÈME DOIT suspendre les règles de remise actives qui le dépassent et en avertir leur auteur. _Source : B05-D6_
5. LE SYSTÈME DOIT permettre de modifier les plafonds de remise sans mise en production, et journaliser chaque modification avec son auteur et sa date. _Source : B05-D6_
6. SI l'appartenance du client à Orvanne+ ne peut pas être vérifiée au moment de la décision, ALORS LE SYSTÈME DOIT appliquer le plafond général. _Source : B05-D6_
7. LE SYSTÈME DOIT réserver, pour chaque règle de remise, un échantillon témoin tiré au hasard, de taille paramétrable, relancé sans remise. _Source : B05-D5, B05-D12_

### Exigence 4 : données utilisées pour la personnalisation (lot 1)

**User story :** En tant que DPO, je veux que la relance n'utilise que des données disponibles, nécessaires et récentes, afin de respecter les règles de conservation des données de prospection.

#### Critères d'acceptation

1. LE SYSTÈME DOIT limiter les données de personnalisation au contenu du panier, aux commandes du Lac et, pour les clients connectés, à la navigation disponible. _Source : B05-D3, H18_
2. LE SYSTÈME NE DOIT PAS utiliser de commande ni de donnée de navigation datant de plus de 3 ans avant le dernier contact du client. _Source : B05-D3, CT-05, H18_
3. LE SYSTÈME NE DOIT PAS utiliser de donnée de navigation recueillie hors d'une session connectée du client. _Source : B05-D3, H18_
4. LE SYSTÈME NE DOIT PAS lire ni utiliser le numéro de mobile du client tant que l'avis de la DPO sur cet usage n'est pas enregistré. _Source : CT-02_
5. LE SYSTÈME DOIT supprimer ou anonymiser les données de relance d'un client (paniers candidats, relances, remises) 3 ans après son dernier contact. _Source : CT-05_
6. LE SYSTÈME DOIT calculer la date de dernier contact selon la définition paramétrée, validée par la DPO. _Source : CT-05, H18_

### Exigence 5 : canaux de relance (lot 1 pour l'e-mail, lot 2 pour les autres canaux)

**User story :** En tant que chargée de CRM, je veux relancer d'abord par e-mail, puis ajouter les autres canaux quand ils sont autorisés, afin de joindre chaque client par le canal le plus adapté sans enfreindre les règles de la DPO.

#### Critères d'acceptation

1. LE SYSTÈME DOIT envoyer les relances du lot 1 par e-mail uniquement. _Source : B05-D4, H17_
2. LE SYSTÈME NE DOIT PAS permettre l'activation d'un canal autre que l'e-mail (notification de l'application, SMS, messagerie mobile) tant que l'avis de la DPO sur ce canal n'est pas enregistré. _Source : B05-D4, CT-01, CT-02, H17_
3. OÙ plusieurs canaux sont activés, LE SYSTÈME DOIT utiliser le canal défini par la règle applicable, parmi ceux pour lesquels le client a donné son consentement, et à défaut l'e-mail. _Source : B05-D1, B05-D4, H17_
4. SI l'envoi échoue sur le canal choisi, ALORS LE SYSTÈME DOIT réessayer selon la politique paramétrée, puis enregistrer la relance comme non envoyée avec son motif. _Source : B05-D1_

### Exigence 6 : mesure du chiffre d'affaires incrémental (lot 1)

**User story :** En tant que responsable marketing, je veux un tableau du CA incrémental de la relance, afin de démontrer au comité commerce ce qu'elle rapporte par rapport à la relance actuelle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT affecter au hasard une part paramétrable des paniers éligibles à un groupe témoin qui reçoit la relance actuelle (même e-mail, 24 heures après l'abandon). _Source : B05-D12, B05-D1_
2. LE SYSTÈME DOIT attribuer une commande à une relance quand la commande contient au moins un article du panier et qu'elle est passée dans la fenêtre d'attribution paramétrée après l'envoi. _Source : B05-D12_
3. LE SYSTÈME DOIT afficher, par période et par règle, pour le nouveau dispositif et pour le groupe témoin : paniers éligibles, relances envoyées, commandes attribuées, taux de conversion, CA attribué et montant des remises accordées. _Source : B05-D12_
4. LE SYSTÈME DOIT afficher le CA incrémental calculé selon la méthode décrite dans `design.md`, accompagné de la méthode, de la taille des deux groupes et de la période mesurée. _Source : B05-D12_
5. LE SYSTÈME DOIT réserver l'accès au tableau aux rôles marketing et finance, et permettre son export pour le comité commerce. _Source : B05-D12, CT-01_
6. LE SYSTÈME DOIT présenter dans le tableau et dans ses exports uniquement des agrégats, sans donnée nominative. _Source : B05-D12, CT-01_

### Exigence 7 : démonstration pour le comité commerce du 8 décembre 2026 (lot 0)

**User story :** En tant que responsable marketing, je veux montrer au comité commerce ce que la relance personnalisée décide et ce qu'elle pourrait rapporter, afin d'obtenir son soutien pour le projet.

#### Critères d'acceptation

1. LE SYSTÈME DOIT fournir, au plus tard le 8 décembre 2026, un environnement de démonstration qui applique des règles de relance et de remise à un jeu de paniers et affiche, pour chaque panier, le message, le moment, le canal, la remise et la règle appliquée. _Source : B05-D10, H19, H30_
2. LE SYSTÈME DOIT alimenter l'environnement de démonstration uniquement avec des données synthétiques ou anonymisées. _Source : B05-D11, CT-04, H19_
3. SI le jeu de démonstration est dérivé de données de production, ALORS LE SYSTÈME DOIT n'en charger que la version anonymisée validée par la DPO. _Source : B05-D11, CT-04, H19_
4. LE SYSTÈME DOIT afficher dans la démonstration un tableau de CA incrémental simulé, marqué « simulation sur données fictives », calculé avec la méthode de l'exigence 6. _Source : B05-D10, B05-D12, H19_
5. LE SYSTÈME NE DOIT PAS envoyer de message à une personne réelle depuis l'environnement de démonstration. _Source : B05-D10, H19_
6. LE SYSTÈME DOIT fonctionner, pour la démonstration, sur un environnement distinct de la production, sans aucune mise en production pendant le gel du 16 novembre au 11 janvier. _Source : H19, CT-07_

### Exigence 8 : modèle d'IA de choix des relances (lot 2)

**User story :** En tant que responsable marketing, je veux qu'un modèle d'IA puisse remplacer les règles pour choisir la relance, afin d'améliorer la conversion une fois les données confirmées et le traitement autorisé.

#### Critères d'acceptation

1. OÙ un modèle de choix est activé, LE SYSTÈME DOIT soumettre ses propositions aux mêmes contrôles que les règles : éligibilité (exigence 1), plafonds de remise (exigence 3), données autorisées (exigence 4) et canaux activés (exigence 5). _Source : B05-D2, H30_
2. LE SYSTÈME NE DOIT PAS permettre l'activation d'un modèle de choix tant que l'avis de la DPO sur ce traitement n'est pas enregistré. _Source : B05-D2, CT-01, H30_
3. OÙ un modèle de choix est activé, LE SYSTÈME DOIT enregistrer pour chaque relance la version du modèle et les principaux facteurs de sa décision. _Source : B05-D2, H30_
4. OÙ un modèle de choix est activé, LE SYSTÈME DOIT mesurer son CA incrémental par rapport aux règles du lot 1, sur un groupe de comparaison tiré au hasard et de taille paramétrable. _Source : B05-D2, B05-D12_
5. LE SYSTÈME DOIT permettre de désactiver le modèle et de revenir aux règles du lot 1 sans mise en production. _Source : B05-D2, H30_

### Exigence 9 : exigences non fonctionnelles et conformité

**User story :** En tant que DSI, je veux une solution conforme au RGPD, hébergée dans l'Union européenne, dimensionnée pour le pic et réversible, afin de pouvoir la mettre en service sans risque.

#### Critères d'acceptation

1. LE SYSTÈME NE DOIT PAS envoyer de relance personnalisée en production tant que l'avis de la DPO sur le traitement n'est pas enregistré dans le paramétrage. _Source : B05-D8, CT-01_
2. LE SYSTÈME DOIT être hébergé dans l'Union européenne, y compris l'environnement de démonstration et le service d'envoi des e-mails. _Source : CT-08_
3. LE SYSTÈME DOIT utiliser uniquement des données synthétiques ou anonymisées dans les environnements de développement, de test et de recette. _Source : CT-04_
4. LE SYSTÈME DOIT journaliser les modifications de règles, de modèles de message, de plafonds et de paramètres, ainsi que les accès au tableau de mesure, avec l'auteur et l'horodatage. _Source : B05-D6, H30, CT-01_
5. LE SYSTÈME DOIT traiter le volume de pointe de paniers abandonnés fixé lors du cadrage, pic de fin d'année compris, en respectant la tolérance d'envoi du critère 2.6. _Source : B05-D1_
6. LE SYSTÈME DOIT permettre de suspendre toutes les relances personnalisées et de revenir à la relance actuelle par un paramètre, sans mise en production. _Source : B05-D1, H30_

## Hors périmètre

- Code promo dans les messages de retard de livraison (`B05-D7`) : relève du projet retards (B05-F6), où il est exclu par `CT-03` (conflit `C07`, question `Q07`). Renvoyé vers P01.
- Historique d'achats depuis 2014 (`B05-D3`, en partie) : seuls les 3 ans précédant le dernier contact sont exploités (`H18`, `CT-05`). Aucun projet ne reprend l'historique plus ancien.
- Report de la question des données personnelles (`B05-D9`, en partie) : non retenu. Le consentement newsletter n'est utilisé que si la DPO en confirme la portée (critères 1.3 et 9.1).
- Démonstration « sur les vrais clients » (`B05-D11`, en partie) : remplacée par des données synthétiques ou anonymisées (`H19`, `CT-04`, question `Q20`).
- Modèle d'IA dès le lot 1 (`B05-D2`) : reporté au lot 2 (exigence 8, `H30`, question `Q33`).
- Canaux autres que l'e-mail dès le lot 1 (`B05-D4`, en partie) : reportés au lot 2, après avis de la DPO (critère 5.2, `H17`). Les « messageries mobiles » ne sont pas nommées (B05-F11) et le seront avant leur activation.
- Purge des historiques de prospection antérieurs à la limite de 3 ans dans les systèmes existants (`B07-D14`) : chantier sans porteur ni échéance (`Q31`). Le projet purge seulement ses propres données (critère 4.5). Aucun projet ne le reprend.
- Gestion des oppositions à la prospection et des demandes de droits : portée par P05. P04 lit les oppositions enregistrées (critère 1.4).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H17 | La V1 de la relance n'utilise que l'e-mail, pour les clients ayant consenti aux communications commerciales, sous réserve que la DPO confirme la portée du consentement newsletter. SMS, notifications et messageries mobiles sont ajoutés après analyse de la DPO (CT-01, CT-02). | C18 | oui |
| H18 | La personnalisation n'utilise que les commandes du Lac et, pour les clients connectés, la navigation disponible, limitées aux 3 ans précédant le dernier contact du client. L'historique depuis 2014 n'est pas exploité. | C19 | oui |
| H19 | La démo du comité commerce du 8 décembre utilise des données anonymisées ou synthétiques, sur un environnement hors production. Une démo n'étant pas une mise en production, le gel ne s'y applique pas. | C20 | oui |
| H30 | La V1 de la relance choisit le message, le moment et la remise par des règles paramétrables et explicables ; un modèle d'IA (B05-D2) vient en V2, une fois les données confirmées et l'avis de la DPO rendu. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q07 | Confirmez-vous l'abandon du code promo dans les messages de retard (CT-03) ? Souhaitez-vous à la place un message commercial distinct, soumis au consentement ? | Capucine Lorrain ; Hélène Marsac | non (hors périmètre de P04) |
| Q18 | Le consentement newsletter couvre-t-il une relance personnalisée des paniers abandonnés, les remises ciblées et chaque canal (e-mail, notifications, SMS, messageries) ? Quelle analyse faut-il avant le développement ? | Hélène Marsac | non (conditionne la mise en service du lot 1, critères 1.3 et 9.1, et l'activation des canaux, critère 5.2) |
| Q19 | Quelles données la relance peut-elle utiliser (commandes, navigation des clients connectés) et sur quelle profondeur, compte tenu de la limite de 3 ans ? Que contient réellement le Lac ? | Hélène Marsac ; équipe du Lac (Théo Bazin) | non (conditionne les critères 4.1, 4.2 et 4.6) |
| Q20 | Une démo sur données anonymisées ou synthétiques convient-elle au comité commerce du 8 décembre ? Qu'attendez-vous précisément de la démo ? | Capucine Lorrain ; Hélène Marsac | non (conditionne le contenu de l'exigence 7) |
| Q31 | Qui porte la purge des historiques de prospection de plus de 3 ans, et pour quelle échéance ? | Hélène Marsac ; Capucine Lorrain | non (hors périmètre de P04) |
| Q33 | La relance doit-elle reposer sur un modèle d'IA dès la V1, ou des règles suffisent-elles ? Les plafonds de remise (10 %, 15 % pour Orvanne+) sont-ils validés par la finance ? | Capucine Lorrain ; finance | non (conditionne les valeurs du critère 3.3 et le calendrier de l'exigence 8) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne (B01) s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis (B03, B07-D20) ? | DSI (comité d'architecture) | non (conditionne le choix d'hébergement, critère 9.2) |
| Q36 | Quand pouvez-vous examiner les traitements des projets P01, P02, P03, P04, P06 et P07 (CT-01) ? Lesquels exigent une analyse d'impact ? | Hélène Marsac | non (conditionne la date de mise en service du lot 1, critère 9.1) |

### Points à remonter à l'analyste (sans identifiant dans `work/analyse.json`)

Ces points ne figurent pas dans l'analyse. Ils ne bloquent pas la spec, mais conditionnent des tâches de cadrage (tâche 1 de `tasks.md`).

| Point | Destinataire proposé | Ce qu'il conditionne |
|---|---|---|
| Quel système détecte aujourd'hui les paniers abandonnés et envoie la relance à 24 h ? Après quel délai d'inactivité un panier est-il « abandonné » ? | Capucine Lorrain ; DSI | Critère 1.1 (intégration avec Vitrine) |
| Combien de paniers abandonnés par jour, en temps normal et pendant le pic ? (B05-F5) | Équipe du Lac (Théo Bazin) ; DSI | Critère 9.5 |
| Comment Vitrine applique-t-elle une remise individuelle (code à usage unique, remise rattachée au compte) ? Quelle durée de validité ? | DSI ; Capucine Lorrain ; finance | Critère 3.2 |
| Dans quel système l'appartenance à Orvanne+ est-elle enregistrée ? | Capucine Lorrain ; DSI | Critères 3.3 et 3.6 |
| Comment calculer le CA incrémental (B05-F10) : groupe témoin, taille, fenêtre d'attribution ? La méthode proposée dans `design.md` convient-elle ? | Capucine Lorrain ; finance | Critères 6.1, 6.2 et 6.4 |
| Une seule relance par panier, ou une séquence de relances ? | Capucine Lorrain | Critère 1.7 |
| L'outil d'e-mailing peut-il envoyer des relances personnalisées une à une, est-il hébergé dans l'UE, et quelles mentions (lien de désinscription) la DPO exige-t-elle ? | DSI ; Hélène Marsac | Critères 5.1 et 9.2 |
