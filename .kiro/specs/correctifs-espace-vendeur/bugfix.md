# Correctif : export des ventes et temps de réponse de l'espace vendeur

<!-- Projet P08, slug correctifs-espace-vendeur, type bugfix. Commanditaire : direction marketplace.
     Parties prenantes : DSI, vendeurs. Source : B09 (lignes MKP-07 et MKP-11).
     Demandes incluses : B09-D9, B09-D10, B09-D11, B09-D17. Contraintes : CT-04, CT-07, CT-08 (CT-01 conditionnelle, voir critère 2.5). -->

## Introduction

L'espace vendeur de la marketplace présente deux défauts signalés dans le tableau de la direction marketplace (B09).

- **MKP-07**, saisi par la DSI le 30/09/2026 en priorité P3 : l'export des ventes tombe en erreur au-delà de 50 000 lignes (`B09-N5`). La DSI propose d'ajouter un index sur la table des lignes de commande et de passer l'export en asynchrone. Ces deux solutions sont traitées comme des pistes de conception, pas comme des exigences (H27).
- **MKP-11**, verbatim de l'enquête vendeurs du 20/10/2026 : « L'espace vendeur est trop lent ». Ni les pages concernées, ni les temps de réponse, ni le nombre de vendeurs touchés ne sont connus (`B09-F8`). Le correctif commence donc par une mesure ; le seuil attendu sera fixé avec la direction marketplace à partir de cette mesure (H27, Q28).

Le système qui porte l'espace vendeur n'est pas nommé dans les sources (`B09-F15`).

Le correctif est livré en deux lots, hors du gel des mises en production du 16 novembre au 11 janvier (`CT-07`) :
- **Lot 1** (critères 1.1, 2.1 à 2.7, 3.1, 3.2, 3.4) : export des ventes. La caractérisation et les tests de reproduction peuvent se faire pendant le gel ; la mise en production a lieu au plus tôt le 12 janvier 2027, sauf livraison avant le 16 novembre 2026.
- **Lot 2** (critères 1.2, 2.8 à 2.11, 3.3) : temps de réponse, après la mesure initiale et la fixation des seuils.

Les deux lots précèdent les nouvelles vues de ventes du projet P07 (MKP-01, MKP-12) et n'en dépendent pas.

## Glossaire

- **Espace vendeur** : application de la marketplace utilisée par les vendeurs partenaires (système porteur à identifier, `B09-F15`).
- **Export des ventes** : fichier des lignes de ventes d'un vendeur, produit à sa demande depuis l'espace vendeur.
- **Export en différé** : export préparé en arrière-plan puis mis à disposition du vendeur, par opposition au téléchargement immédiat (piste `B09-D11`).
- **Seuil de temps de réponse** : durée maximale d'affichage d'une page, fixée par page avec la direction marketplace après la mesure initiale (H27).
- **Mesure initiale** : relevé des temps de réponse actuels des pages de l'espace vendeur, réalisé avant tout correctif (H27).

## Comportement actuel

### Export des ventes (MKP-07)

1. QUAND un vendeur lance l'export de ses ventes et que le résultat dépasse 50 000 lignes, ALORS LE SYSTÈME tombe en erreur au lieu de produire le fichier d'export. _Source : B09-D9_

### Temps de réponse (MKP-11)

2. QUAND un vendeur utilise l'espace vendeur, ALORS LE SYSTÈME est jugé trop lent par ce vendeur, sans que les pages concernées, les temps de réponse ni le nombre de vendeurs touchés soient connus. _Source : B09-D17_

## Comportement attendu

### Export des ventes (MKP-07)

1. QUAND un vendeur lance l'export de ses ventes et que le résultat dépasse 50 000 lignes, LE SYSTÈME DOIT produire le fichier d'export complet, sans erreur. _Source : B09-D9_
2. QUAND un export est produit, LE SYSTÈME DOIT y inclure exactement les lignes de ventes qui répondent à la demande du vendeur, sans ligne manquante ni doublon : le nombre de lignes du fichier est égal au nombre de lignes de ventes en base pour les mêmes critères. _Source : B09-D9_
3. QUAND le vendeur qui a le plus de lignes de ventes en production lance l'export sur la période la plus longue que l'espace vendeur propose, LE SYSTÈME DOIT produire le fichier complet, sans erreur. _Source : B09-D9_
4. QUAND un export est produit en différé, LE SYSTÈME DOIT indiquer au vendeur que l'export est en préparation, puis mettre le fichier à sa disposition dans l'espace vendeur dès qu'il est prêt. _Source : B09-D9, B09-D11, H27_
5. QUAND un fichier d'export est conservé pour un téléchargement différé, LE SYSTÈME DOIT en réserver le téléchargement au vendeur qui l'a demandé et le supprimer à l'issue d'une durée de conservation paramétrable. _Source : B09-D11, CT-01_
6. QUAND le correctif conserve des fichiers d'export ou des mesures de temps de réponse, LE SYSTÈME DOIT les héberger dans l'Union européenne. _Source : CT-08_
7. QUAND la production d'un export échoue pour une cause technique, LE SYSTÈME DOIT afficher au vendeur un message d'échec qui l'invite à relancer l'export, et enregistrer l'erreur avec le nombre de lignes demandé, à l'intention de la DSI. _Source : B09-D9_

### Temps de réponse (MKP-11)

8. QUAND un vendeur affiche une page de l'espace vendeur, LE SYSTÈME DOIT enregistrer le temps de réponse de cette page, avec l'identifiant de la page et l'horodatage, sans donnée personnelle. _Source : B09-D17, H27_
9. QUAND un vendeur affiche une page de l'espace vendeur, LE SYSTÈME DOIT répondre dans le seuil de temps de réponse fixé pour cette page ; le seuil et le centile sont des paramètres, sans valeur tant que la mesure initiale n'a pas été faite et validée par la direction marketplace. _Source : B09-D17, H27_
10. QUAND un export de plus de 50 000 lignes est en cours de production, LE SYSTÈME DOIT afficher les autres pages de l'espace vendeur dans les seuils du critère 2.9. _Source : B09-D9, B09-D17, H27_
11. QUAND le temps de réponse d'une page dépasse son seuil sur la période d'observation paramétrée, LE SYSTÈME DOIT alerter la supervision de la DSI. _Source : B09-D17, H27_

## Comportement inchangé

1. QUAND un vendeur exporte ses ventes et que le résultat compte 50 000 lignes ou moins, LE SYSTÈME DOIT CONTINUER À produire le fichier avec le même contenu, les mêmes colonnes, le même format et le même mode de téléchargement qu'avant le correctif. _Source : B09-D9_
2. QUAND un vendeur exporte ses ventes, quel que soit le volume, LE SYSTÈME DOIT CONTINUER À n'inclure que les ventes de ce vendeur. _Source : B09-D9_
3. QUAND un vendeur utilise une fonction existante de l'espace vendeur, LE SYSTÈME DOIT CONTINUER À afficher les mêmes informations et à offrir les mêmes fonctions, le correctif ne modifiant que les temps de réponse. _Source : B09-D17, H27_
4. QUAND un traitement existant lit ou écrit dans la table des lignes de commande, LE SYSTÈME DOIT CONTINUER À l'exécuter dans une durée au plus égale à celle mesurée avant le correctif, index éventuel compris. _Source : B09-D10, H27_

## Hors périmètre

- Index sur la table des lignes de commande (`B09-D10`) : solution proposée par la DSI, pas une exigence (H27). Elle est étudiée comme piste dans `design.md` et son impact est encadré par le critère 3.4.
- Export en asynchrone (`B09-D11`) : solution proposée par la DSI, pas une exigence (H27). Elle est retenue comme piste dans `design.md` ; si elle est mise en œuvre, les critères 2.4 et 2.5 s'appliquent.
- Reversements incompréhensibles (`B09-D18`, même ligne MKP-11) : besoin fonctionnel et non défaut de performance, traité par P07.
- Nouvelles vues de ventes, tableau de bord mobile et autres évolutions de l'espace vendeur (MKP-01 à MKP-12 hors MKP-07 et MKP-11) : traitées par P07.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H27 | Pour MKP-11, le correctif commence par mesurer les temps de réponse des pages de l'espace vendeur ; le seuil chiffré attendu est fixé avec la direction marketplace à partir de cette mesure. Les solutions de la DSI pour MKP-07 (index, export asynchrone) sont des pistes de conception, pas des exigences. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q28 | Quelles pages de l'espace vendeur sont jugées lentes, et quel temps de réponse est attendu ? Combien de vendeurs se plaignent ? | Direction marketplace ; DSI | non selon l'analyse, mais la valeur du seuil du critère 2.9 reste vide tant que la mesure et la réponse manquent (lot 2) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne s'applique-t-elle à tous les projets, ou un hébergement dans l'UE chez un éditeur est-il admis ? | DSI (comité d'architecture) | non (critère 2.6 limité à l'UE en attendant) |
| à créer | Quelle erreur précise survient au-delà de 50 000 lignes (message, délai avant l'erreur, fréquence, vendeurs touchés) ? Quel est le format actuel de l'export ? | DSI | non (tâche 1.3) |
| à créer | Un export en différé est-il acceptable pour les vendeurs, et quel délai d'obtention d'un gros export est acceptable ? | Direction marketplace | non (critère 2.4) |
| à créer | L'export des ventes contient-il des données personnelles de clients (nom, adresse de livraison) ? Si oui, la conservation des fichiers différés doit être soumise à la DPO (CT-01), qui n'est pas listée dans les contraintes de P08. | DSI ; Hélène Marsac (DPO) | non (critère 2.5, durée de conservation) |
| à créer | Quel système porte l'espace vendeur, et la mise en production est-elle visée avant le 16 novembre 2026 ou à partir du 12 janvier 2027 ? | DSI | non (planning des lots) |

Les questions marquées « à créer » ne figurent pas encore dans `work/analyse.json` : l'analyste doit leur attribuer un identifiant `Qnn`.
