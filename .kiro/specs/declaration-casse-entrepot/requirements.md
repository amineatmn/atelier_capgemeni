# Exigences : Déclaration de casse à la douchette, blocage du stock dans Hangar et litiges transporteurs

<!-- Projet P03, slug declaration-casse-entrepot. Commanditaire : Exploitation entrepôt E2 (rattachement de direction à confirmer). Sources : B06, B04. -->

## Introduction

Sur l'entrepôt E2, la casse est déclarée sur une fiche papier. Environ 40 cas sont déclarés par jour et le volume réel est estimé à 80 par jour (le double, non mesuré). Une fois sur deux, les litiges transporteurs sont déclarés hors délai. Le stock abîmé n'est pas bloqué dans Hangar, ce qui expose à revendre un article cassé. Cette spec remplace la fiche papier par une déclaration à la douchette (scan, photo facultative, type de dégât) qui crée le dossier, prévient le chef d'équipe et le transport, et bloque le stock dans Hangar, y compris sans réseau.

Le périmètre est découpé en deux lots :

- **V1** : exigences 1 à 7 et 9, déployées sur E2 uniquement. Mise en production au plus tôt le 12 janvier, après le gel (CT-07) et l'avis de la DPO sur les photos (H16).
- **V2** : exigence 8 (photo depuis un téléphone de chef d'équipe, retours abîmés avec note A / B / C, saisie de la note au contrôle qualité).

## Glossaire

- **Douchette** : terminal de scan des entrepôts ; environ 60 sur E2, dont les deux tiers d'anciens modèles sans appareil photo.
- **Déclaration de casse** : saisie d'un colis abîmé (colis scanné, type de dégât, photos éventuelles).
- **Dossier de casse** : enregistrement créé à la validation d'une déclaration.
- **Hangar** : système de gestion des entrepôts ; porte le stock et son blocage.
- **Passerelle** : plateforme d'échange de flux, utilisée pour les notifications et les échanges avec Hangar.
- **Litige transporteur** : réclamation auprès du transporteur pour un colis abîmé en transport, soumise à un délai de déclaration.
- **Grille A / B / C** : note de contrôle qualité d'un retour (A remis en stock, B déstockage, C rebut).
- **Transport** : destinataire de l'alerte de casse (service interne ou transporteur, à préciser : Q29).

## Exigences

### Exigence 1 : Déclarer un colis abîmé à la douchette

**User story :** En tant que préparateur ou cariste de l'entrepôt E2, je veux déclarer un colis abîmé en le scannant, afin de remplacer la fiche papier.

#### Critères d'acceptation

1. QUAND un utilisateur scanne un colis depuis l'écran de déclaration de casse, LE SYSTÈME DOIT identifier le colis et afficher la liste des types de dégâts. _Source : B06-D1, B06-D3_
2. LE SYSTÈME DOIT exiger la sélection d'un type de dégât dans une liste paramétrable avant de valider la déclaration. _Source : B06-D3_
3. QUAND l'utilisateur valide une déclaration complète, LE SYSTÈME DOIT créer automatiquement le dossier de casse, sans autre saisie. _Source : B06-D4_
4. SI le code scanné ne correspond à aucun colis connu, ALORS LE SYSTÈME DOIT refuser la déclaration et afficher un message d'erreur sur la douchette. _Source : B06-D1_

### Exigence 2 : Joindre des photos selon l'équipement

**User story :** En tant que préparateur ou cariste, je veux joindre une ou deux photos quand ma douchette le permet, afin de documenter la casse sans bloquer ceux qui n'ont pas d'appareil photo.

#### Critères d'acceptation

1. OÙ la douchette dispose d'un appareil photo, LE SYSTÈME DOIT proposer d'ajouter 1 à 2 photos à la déclaration. _Source : B06-D2, B06-D6, H15_
2. LE SYSTÈME DOIT accepter la validation d'une déclaration sans photo. _Source : B06-D6, H15_
3. LE SYSTÈME NE DOIT PAS accepter plus de 2 photos par déclaration. _Source : B06-D2_
4. LE SYSTÈME DOIT traiter les photos comme des données personnelles et en limiter l'accès aux rôles autorisés. _Source : CT-06_

### Exigence 3 : Prévenir le chef d'équipe et le transport

**User story :** En tant que chef d'équipe ou membre du transport, je veux être prévenu dès qu'une casse est déclarée, afin d'agir sans attendre.

#### Critères d'acceptation

1. QUAND un dossier de casse est créé, LE SYSTÈME DOIT notifier le chef d'équipe de l'entrepôt concerné, avec le lien vers le dossier. _Source : B06-D5_
2. QUAND un dossier de casse est créé, LE SYSTÈME DOIT notifier le destinataire « transport » défini en paramètre. _Source : B06-D5, H28_
3. SI l'envoi d'une notification échoue, ALORS LE SYSTÈME DOIT réessayer puis signaler l'échec dans le dossier sans annuler sa création. _Source : B06-D5_

### Exigence 4 : Déclarer sans réseau

**User story :** En tant que préparateur ou cariste travaillant dans une zone sans couverture, je veux déclarer hors ligne, afin de ne pas perdre de déclaration.

#### Critères d'acceptation

1. PENDANT QUE la douchette n'a pas de réseau, LE SYSTÈME DOIT enregistrer la déclaration localement et la marquer « en attente de synchronisation ». _Source : B06-D8_
2. QUAND le réseau redevient disponible, LE SYSTÈME DOIT synchroniser les déclarations en attente dans l'ordre de saisie, sans doublon. _Source : B06-D8_
3. LE SYSTÈME DOIT conserver la date et l'heure de saisie d'origine lors de la synchronisation. _Source : B06-D8_
4. LE SYSTÈME DOIT afficher le nombre de déclarations en attente de synchronisation. _Source : B06-D8_

### Exigence 5 : Bloquer le stock dans Hangar

**User story :** En tant que responsable du stock, je veux que le stock concerné soit bloqué dans Hangar, afin de ne pas revendre un article cassé.

#### Critères d'acceptation

1. QUAND un dossier de casse est créé, LE SYSTÈME DOIT transmettre à Hangar une demande de blocage du stock concerné. _Source : B06-D9_
2. SI Hangar est indisponible, ALORS LE SYSTÈME DOIT conserver la demande de blocage et la rejouer jusqu'à son acquittement. _Source : B06-D9_
3. LE SYSTÈME DOIT afficher dans le dossier l'état du blocage (demandé, confirmé, en échec). _Source : B06-D9_

### Exigence 6 : Suivre le délai des litiges transporteurs

**User story :** En tant que membre du transport, je veux connaître la date limite de déclaration du litige, afin de ne plus déclarer hors délai.

#### Critères d'acceptation

1. LE SYSTÈME DOIT lire le délai de déclaration des litiges transporteurs dans un paramètre, valeur provisoire 7 jours. _Source : B06-D11, H28_
2. QUAND un dossier de casse est créé, LE SYSTÈME DOIT y afficher la date limite de déclaration du litige. _Source : B06-D11, H28_
3. QUAND un dossier non clos atteint un jour avant sa date limite, LE SYSTÈME DOIT relancer le destinataire « transport ». _Source : B06-D11, H28_

### Exigence 7 : Déploiement progressif et calendrier

**User story :** En tant que responsable de l'exploitation E2, je veux un déploiement d'abord sur E2, afin de sécuriser la bascule avant les autres sites.

#### Critères d'acceptation

1. LE SYSTÈME DOIT être activable par entrepôt, seul E2 étant activé en V1. _Source : B06-D12_
2. LE SYSTÈME NE DOIT PAS être mis en production entre le 16 novembre et le 11 janvier. _Source : CT-07, B06-D13_
3. SI l'inventaire de janvier a lieu avant la mise en production, ALORS l'exploitation E2 DOIT utiliser la fiche papier actuelle et LE SYSTÈME DOIT rester inactif. _Source : B06-D13, H16_
4. LE SYSTÈME DOIT être mis en production sur E2 au plus tôt le 12 janvier et après l'avis de la DPO sur les photos. _Source : B06-D13, H16, CT-01_

### Exigence 8 : Évolutions V2

**User story :** En tant que responsable de l'exploitation E2, je veux étendre la saisie aux téléphones des chefs d'équipe et aux retours abîmés, afin de couvrir les cas hors douchette photo.

#### Critères d'acceptation

1. OÙ la fonction est activée, LE SYSTÈME DOIT permettre à un chef d'équipe d'ajouter une photo à une déclaration depuis un téléphone. _Source : B06-D7, H15_
2. OÙ la fonction est activée, LE SYSTÈME DOIT permettre de déclarer un retour abîmé depuis le même écran, avec une note A / B / C. _Source : B06-D10, B04-D11_
3. OÙ la fonction est activée, LE SYSTÈME DOIT permettre de saisir la note de contrôle qualité et une photo depuis la douchette. _Source : B04-D13_
4. QUAND une note C est saisie, LE SYSTÈME DOIT signaler le retour pour traitement manuel par le service client, sans réduction automatique du remboursement. _Source : B04-D13, H11_

### Exigence 9 : Conformité, hébergement et tests

**User story :** En tant que DPO et DSI, je veux que le traitement respecte les règles du groupe, afin d'éviter tout risque de conformité.

#### Critères d'acceptation

1. LE SYSTÈME DOIT n'être développé qu'après examen du traitement par la DPO. _Source : CT-01_
2. LE SYSTÈME NE DOIT PAS utiliser de données de production non anonymisées pour les tests et démonstrations. _Source : CT-04_
3. LE SYSTÈME DOIT être hébergé dans l'Union européenne. _Source : CT-08_
4. LE SYSTÈME DOIT journaliser la création, la consultation et la suppression des photos. _Source : CT-06_
5. LE SYSTÈME DOIT absorber 80 déclarations par jour, soit le double des 40 déclarées, sur E2. _Source : B06-D4_

## Hors périmètre

- Extension aux entrepôts E1 et E3 (`B06-D12`) : seul E2 est traité en V1 ; E1 utilise un tableur propre, extension non cadrée, renvoyée vers aucun projet.
- Réduction automatique du remboursement selon la note (`B04-D12` non inclus) : arbitrage juridique en attente (C12), traitement manuel en V1 (H11).

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H11 | En V1, le montant remboursé ne dépend pas de la note ; une note C déclenche un signalement manuel. | C12 | oui |
| H15 | La photo est facultative ; l'ajout depuis un téléphone de chef d'équipe est prévu en V2. | C16 | oui |
| H16 | Déploiement sur E2 au plus tôt le 12 janvier ; sinon fiche papier pour l'inventaire. | C17 | oui |
| H28 | Délai de déclaration des litiges paramétrable, 7 jours provisoires, date limite affichée. | aucun | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q12 | Est-il légal de réduire le remboursement selon la note ? Quels montants ? | Direction juridique et conformité | non (traité par H11) |
| Q16 | La photo est-elle obligatoire ? Faut-il équiper les chefs d'équipe ou renouveler des douchettes ? | Karim Benhaddou ; DSI | non (exigence 2) |
| Q17 | À quelle date a lieu l'inventaire de janvier sur E2 ? | Karim Benhaddou | non (exigence 7) |
| Q29 | Quel est le délai contractuel par transporteur ? Qui est « le transport » ? | Service transport | non (exigences 3 et 6) |
| Q34 | L'hébergement dans le cloud d'Orvanne s'applique-t-il à tous les projets ? | DSI | non (exigence 9) |
| Q36 | Quand la DPO peut-elle examiner le traitement ? Analyse d'impact requise ? | Hélène Marsac | non (exigence 9) |
| Q37 | La note A / B / C se saisit-elle sur la même application douchette ? | Karim Benhaddou ; Inès Rouvière | non (exigence 8) |
