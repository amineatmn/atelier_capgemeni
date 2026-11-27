# Exigences : relance personnalisée des paniers abandonnés

<!-- Projet P04, slug relance-paniers-abandonnes. Commanditaire : Marketing (CRM et fidélité). Sources : B05. -->

## Introduction

Aujourd'hui, Orvanne envoie le même e-mail de relance à tous les clients 24 heures après l'abandon du panier, et cette relance convertit à « 2 et quelques % ». Le marketing veut une relance qui choisit, pour chaque client, le message, le moment, le canal et la remise éventuelle. La volumétrie des paniers abandonnés n'est pas connue (« aucune idée, beaucoup »), et les données réellement disponibles dans le Lac sont plus limitées que ce que suppose le marketing.

Les contraintes transverses priment sur les demandes du marketing : avis préalable de la DPO (`CT-01`), mobile réservé à la livraison sans analyse (`CT-02`), conservation de 3 ans au plus (`CT-05`), aucune donnée de production non anonymisée en démo (`CT-04`).

La spec est livrée en lots, car le comité commerce du 8 décembre tombe pendant le gel des mises en production du 16 novembre au 11 janvier (`CT-07`) :
- **Lot 1 (démo)** : exigence 7, sur un environnement hors production, avec données anonymisées ou synthétiques. Une démo n'est pas une mise en production (`H19`).
- **Lot 2 (V1 en production)** : exigences 1 à 6, 8 et 9, après le gel et l'avis de la DPO, par règles paramétrables et pour l'e-mail seul (`H17`, `H30`).
- **V2** : modèle d'IA (`B05-D2`) et canaux supplémentaires, après analyse de la DPO.

## Glossaire

- **Panier abandonné** : panier d'un client identifié, non converti en commande. Le délai d'abandon est un paramètre (valeur initiale : 24 heures, comme la relance actuelle).
- **Relance** : message envoyé à un client pour l'inciter à finaliser son panier abandonné.
- **Règle de décision** : règle paramétrable et explicable qui détermine message, moment, canal et remise d'une relance (`H30`).
- **Client qui hésite** : client dont le comportement correspond aux critères paramétrés d'hésitation (critères à définir, `B05-D5`).
- **Orvanne+** : programme de fidélité, avec plafond de remise majoré.
- **Groupe témoin** : clients éligibles volontairement non relancés ou relancés sans remise, pour mesurer le CA incrémental.
- **CA incrémental** : chiffre d'affaires attribuable à la relance par comparaison avec le groupe témoin (méthode à valider, `Q33`).
- **Lac** : entrepôt de données contenant les commandes et historiques.
- **Opposition** : refus d'un client de recevoir de la prospection, géré par le registre des droits (P05).

## Exigences

### Exigence 1 : détection du panier abandonné et relance par e-mail

**User story :** En tant que responsable CRM, je veux que chaque panier abandonné éligible déclenche une relance, afin de récupérer des ventes aujourd'hui perdues.

#### Critères d'acceptation

1. QUAND un panier d'un client identifié n'est pas converti en commande dans le délai d'abandon paramétré (24 heures par défaut), LE SYSTÈME DOIT le marquer comme panier abandonné éligible à la relance. _Source : B05-D1, B05-D5_
2. LE SYSTÈME DOIT permettre de modifier le délai d'abandon sans nouvelle mise en production. _Source : B05-D1, H30_
3. QUAND un panier abandonné éligible est identifié, LE SYSTÈME DOIT produire une décision de relance (message, moment, canal, remise éventuelle) et la journaliser avec le motif de la règle appliquée. _Source : B05-D1, H30_
4. QUAND un client commande après un panier abandonné, LE SYSTÈME DOIT annuler toute relance non encore envoyée pour ce panier. _Source : B05-D1_
5. LE SYSTÈME NE DOIT PAS envoyer plus de relances par panier abandonné que le maximum paramétré (1 par défaut, valeur prudente). _Source : B05-D1, H30_

### Exigence 2 : choix du message, du moment et du canal par règles

**User story :** En tant que responsable CRM, je veux des règles paramétrables qui choisissent message et moment par client, afin de remplacer le même e-mail envoyé à tous à 24 heures.

#### Critères d'acceptation

1. LE SYSTÈME DOIT choisir le message, le moment d'envoi et le canal à partir de règles de décision paramétrables et explicables, sans modèle d'IA en V1. _Source : B05-D1, H30_
2. LE SYSTÈME DOIT conserver, pour chaque relance, la règle appliquée et les données d'entrée utilisées, afin de pouvoir l'expliquer. _Source : B05-D1, H30_
3. LE SYSTÈME DOIT isoler le moteur de décision derrière une interface remplaçable, de façon qu'un modèle d'IA puisse être branché en V2 sans modifier l'envoi. _Source : B05-D2, H30_
4. LE SYSTÈME NE DOIT PAS activer de modèle d'IA pour décider d'une relance avant l'avis de la DPO et la confirmation des données disponibles. _Source : B05-D2, H30, CT-01_
5. LE SYSTÈME DOIT permettre au marketing de modifier les règles sans mise en production. _Source : B05-D1, H30_

### Exigence 3 : données exploitées et durée de conservation

**User story :** En tant que DPO, je veux que la relance n'exploite que des données autorisées et récentes, afin de respecter la durée de conservation de 3 ans.

#### Critères d'acceptation

1. LE SYSTÈME DOIT utiliser pour la personnalisation les commandes du Lac et, pour les clients connectés, la navigation disponible. _Source : B05-D3, H18_
2. LE SYSTÈME DOIT limiter les données exploitées aux 3 ans précédant le dernier contact du client. _Source : B05-D3, H18, CT-05_
3. LE SYSTÈME NE DOIT PAS exploiter l'historique d'achats antérieur à cette limite, même s'il existe dans le Lac depuis 2014. _Source : B05-D3, CT-05, H18_
4. SI aucune donnée de navigation n'est disponible pour un client, ALORS LE SYSTÈME DOIT décider la relance à partir de ses seules commandes. _Source : B05-D3, H18_
5. LE SYSTÈME DOIT supprimer ou anonymiser les données de relance d'un client 3 ans après son dernier contact. _Source : CT-05_

### Exigence 4 : canaux de relance

**User story :** En tant que client, je veux être relancé uniquement par un canal que j'ai accepté, afin de maîtriser l'usage de mes coordonnées.

#### Critères d'acceptation

1. LE SYSTÈME DOIT n'utiliser que l'e-mail comme canal de relance en V1. _Source : B05-D4, H17_
2. LE SYSTÈME NE DOIT PAS envoyer de relance par SMS en V1, ni utiliser le numéro de mobile collecté pour la livraison. _Source : B05-D4, CT-02, H17_
3. LE SYSTÈME NE DOIT PAS envoyer de notification d'application ni de message par messagerie mobile en V1. _Source : B05-D4, H17, CT-01_
4. OÙ un canal supplémentaire est activé après analyse de la DPO, LE SYSTÈME DOIT l'ajouter comme canal paramétrable par client, sans modifier les règles existantes. _Source : B05-D4, H17_
5. LE SYSTÈME DOIT n'envoyer une relance qu'aux clients ayant consenti aux communications commerciales. _Source : B05-D9, H17_

### Exigence 5 : remise ciblée et plafonds

**User story :** En tant que responsable CRM, je veux proposer une remise seulement au client qui hésite, afin de ne pas rogner la marge sur ceux qui achèteraient de toute façon.

#### Critères d'acceptation

1. SI un client est classé « qui hésite » selon les critères paramétrés, ALORS LE SYSTÈME DOIT pouvoir lui associer une remise. _Source : B05-D5_
2. SI un client n'est pas classé « qui hésite », ALORS LE SYSTÈME NE DOIT PAS lui associer de remise. _Source : B05-D5_
3. LE SYSTÈME DOIT plafonner la remise à 10 % du panier, et à 15 % pour un client Orvanne+. _Source : B05-D6_
4. LE SYSTÈME DOIT lire ces plafonds dans un paramètre modifiable sans mise en production. _Source : B05-D6_
5. LE SYSTÈME DOIT refuser toute règle de décision dont la remise dépasse le plafond applicable. _Source : B05-D6_
6. LE SYSTÈME DOIT désactiver l'envoi de remises tant que les critères d'hésitation et les plafonds ne sont pas validés. _Source : B05-D5, B05-D6_

### Exigence 6 : conformité RGPD et opposition

**User story :** En tant que DPO, je veux valider le traitement avant son développement et exclure les clients opposés, afin de rester conforme.

#### Critères d'acceptation

1. LE SYSTÈME NE DOIT PAS être mis en production avant l'avis écrit de la DPO sur le traitement, sa base légale et la portée du consentement newsletter. _Source : B05-D8, B05-D9, CT-01, H17_
2. SI un client a enregistré une opposition à la prospection, ALORS LE SYSTÈME DOIT l'exclure de toute relance. _Source : CT-05, H17_
3. SI le statut de consentement d'un client est inconnu ou indisponible, ALORS LE SYSTÈME DOIT ne pas le relancer. _Source : B05-D9, H17_
4. LE SYSTÈME DOIT journaliser pour chaque relance le consentement vérifié, le canal et l'horodatage. _Source : B05-D8, CT-01_
5. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_

### Exigence 7 : démo pour le comité commerce du 8 décembre

**User story :** En tant que membre du comité commerce, je veux voir la relance personnalisée fonctionner, afin de décider de la suite du projet.

#### Critères d'acceptation

1. LE SYSTÈME DOIT proposer, avant le 8 décembre, une démo de la relance sur un environnement hors production. _Source : B05-D10, H19_
2. LE SYSTÈME DOIT utiliser pour la démo des données anonymisées ou synthétiques, et jamais de données de vrais clients non anonymisées. _Source : B05-D11, CT-04, H19_
3. LE SYSTÈME NE DOIT PAS envoyer de message réel à un client pendant la démo. _Source : B05-D10, CT-01, H19_
4. LE SYSTÈME DOIT montrer dans la démo au moins trois clients types recevant des relances différentes, avec la règle appliquée. _Source : B05-D1, B05-D10, H19_
5. LE SYSTÈME DOIT ne rien déployer en production entre le 16 novembre et le 11 janvier. _Source : CT-07_

### Exigence 8 : tableau du CA incrémental

**User story :** En tant que membre du comité commerce, je veux mesurer le CA incrémental de la relance, afin de juger son intérêt par rapport à la relance actuelle.

#### Critères d'acceptation

1. LE SYSTÈME DOIT présenter un tableau du CA incrémental de la relance, avec le taux de conversion de référence de la relance actuelle (2 et quelques %). _Source : B05-D12_
2. LE SYSTÈME DOIT calculer le CA incrémental par comparaison avec un groupe témoin non relancé par la règle testée. _Source : B05-D12, B05-D5_
3. LE SYSTÈME DOIT afficher la taille du groupe témoin et la période de mesure. _Source : B05-D12_
4. LE SYSTÈME DOIT présenter le tableau de la démo sur des données synthétiques, marquées comme telles. _Source : B05-D12, CT-04, H19_
5. LE SYSTÈME DOIT n'afficher dans ce tableau que des agrégats, sans identité de client. _Source : B05-D12, CT-01_

### Exigence 9 : volumétrie et exploitation

**User story :** En tant que DSI, je veux dimensionner et exploiter la relance sans risque pour le pic, afin de ne pas dégrader les autres systèmes.

#### Critères d'acceptation

1. LE SYSTÈME DOIT mesurer la volumétrie réelle des paniers abandonnés avant le dimensionnement final. _Source : B05-D1_
2. LE SYSTÈME DOIT lire les données du Lac sans dégrader les traitements existants, hors des heures de forte charge paramétrées. _Source : B05-D3, H18_
3. SI l'envoi d'une relance échoue, ALORS LE SYSTÈME DOIT journaliser l'échec et ne pas renvoyer le message plus de fois que le nombre de tentatives paramétré (valeur initiale à fixer avec la DSI). _Source : B05-D1_
4. LE SYSTÈME DOIT utiliser des données anonymisées ou synthétiques pour tous les tests. _Source : CT-04_

## Hors périmètre

- Code promo dans les messages de retard de livraison (`B05-D7`) : relève du projet retards et est exclu par `CT-03` (message de service sans offre commerciale, `H06`), renvoyé vers P01.
- Modèle d'IA (`B05-D2`) : reporté en V2 ; la V1 repose sur des règles (`H30`). Seule l'interface remplaçable est spécifiée (critère 2.3).
- Canaux SMS, notifications d'application et messageries mobiles (`B05-D4`) : hors V1, dans l'attente de l'analyse de la DPO (`H17`).
- Gestion du registre des oppositions et purge des historiques de plus de 3 ans : portées par P05 (registre des droits).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H06 | L'alerte de retard ne contient ni code promo ni offre commerciale ; une offre éventuelle est un message marketing distinct, hors P01. | C07 | oui |
| H17 | La V1 n'utilise que l'e-mail, pour les clients ayant consenti aux communications commerciales, sous réserve de l'avis de la DPO sur la portée du consentement newsletter. | C18 | oui |
| H18 | La personnalisation n'utilise que les commandes du Lac et la navigation des clients connectés, limitées aux 3 ans précédant le dernier contact. | C19 | oui |
| H19 | La démo du 8 décembre utilise des données anonymisées ou synthétiques, hors production ; le gel ne s'y applique pas. | C20 | oui |
| H30 | La V1 choisit message, moment et remise par des règles paramétrables et explicables ; l'IA vient en V2. | aucun | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q07 | Abandon du code promo dans les messages de retard confirmé ? Message commercial distinct souhaité ? | Capucine Lorrain ; Hélène Marsac | non |
| Q18 | Le consentement newsletter couvre-t-il la relance personnalisée, les remises ciblées et chaque canal ? | Hélène Marsac | non (mise en production : exigence 6) |
| Q19 | Quelles données utiliser et sur quelle profondeur ? Que contient réellement le Lac ? | Hélène Marsac ; Théo Bazin | non |
| Q20 | Une démo sur données anonymisées ou synthétiques convient-elle au comité du 8 décembre ? | Capucine Lorrain ; Hélène Marsac | non |
| Q31 | Qui porte la purge des historiques de prospection de plus de 3 ans, et pour quelle échéance ? | Hélène Marsac ; Capucine Lorrain | non (exigence 3) |
| Q33 | Règles ou modèle d'IA dès la V1 ? Plafonds de remise validés par la finance ? Méthode du CA incrémental ? | Capucine Lorrain ; finance | non (exigences 5 et 8) |
| Q34 | L'hébergement dans le cloud d'Orvanne s'applique-t-il, ou l'UE chez un éditeur est-elle admise ? | DSI | non (exigence 6) |
| Q36 | Quand la DPO peut-elle examiner le traitement ? Une analyse d'impact est-elle requise ? | Hélène Marsac | non (exigence 6) |
