# Correctif : export des ventes en erreur et lenteur de l'espace vendeur

<!-- Projet P08, slug correctifs-espace-vendeur, type bugfix. Ce fichier remplace requirements.md. Sources : B09. -->

## Contexte

Le tableau de la marketplace (B09) décrit deux défauts de l'espace vendeur existant, portés par la direction marketplace :

- **MKP-07** : l'export des ventes tombe en erreur au-delà de 50 000 lignes. Priorité exprimée : P3, sans échéance. La DSI propose deux pistes : un index sur la table des lignes de commande et un export asynchrone.
- **MKP-11** : un vendeur juge l'espace vendeur « trop lent » (verbatim d'enquête). Ni priorité, ni échéance, ni page concernée, ni temps attendu ne sont donnés.

Les pistes de la DSI sont traitées comme des pistes de conception, pas comme des exigences (H27). Le comportement attendu de MKP-11 ne peut pas être chiffré avant une mesure : le correctif commence donc par mesurer les temps de réponse (H27).

Ces correctifs précèdent les nouvelles fonctions du projet P07 (espace vendeur) et ne doivent pas en dépendre. Aucune mise en production n'a lieu pendant le gel du 16 novembre au 11 janvier (CT-07) : le correctif est livré en un seul lot, hors période de gel.

## Comportement actuel

1. QUAND un vendeur exporte plus de 50 000 lignes de ventes, ALORS LE SYSTÈME tombe en erreur et ne fournit pas le fichier. _Source : B09-D9_
2. QUAND un vendeur utilise l'espace vendeur, ALORS LE SYSTÈME est jugé trop lent par au moins un vendeur, sans que les pages concernées ni les temps de réponse soient connus. _Source : B09-D17, H27_

## Comportement attendu

1. QUAND un vendeur exporte un volume de ventes supérieur à 50 000 lignes, LE SYSTÈME DOIT produire l'export complet sans erreur. _Source : B09-D9_
2. SI un export échoue malgré tout, ALORS LE SYSTÈME DOIT informer le vendeur de l'échec avec un message explicite et journaliser l'erreur avec le volume demandé. _Source : B09-D9, H27_
3. LE SYSTÈME DOIT mesurer et enregistrer le temps de réponse de chaque page de l'espace vendeur (médiane et 95e centile), avant toute optimisation. _Source : B09-D17, H27_
4. QUAND la mesure est disponible, LE SYSTÈME DOIT respecter, pour chaque page identifiée comme lente, un temps de réponse au 95e centile inférieur ou égal à un seuil paramétrable, dont la valeur est fixée avec la direction marketplace à partir de la mesure (Q28). _Source : B09-D17, H27_
5. LE SYSTÈME NE DOIT PAS être mis en production entre le 16 novembre et le 11 janvier. _Source : CT-07_

## Comportement inchangé

1. QUAND un vendeur exporte 50 000 lignes de ventes ou moins, LE SYSTÈME DOIT CONTINUER À produire un export au contenu identique à celui d'avant le correctif. _Source : B09-D9_
2. QUAND un vendeur utilise les fonctions existantes de l'espace vendeur, LE SYSTÈME DOIT CONTINUER À fournir les mêmes résultats et les mêmes droits d'accès qu'avant le correctif. _Source : B09-D17, H27_
3. QUAND les nouvelles fonctions de l'espace vendeur (projet P07) ne sont pas livrées, LE SYSTÈME DOIT CONTINUER À fonctionner avec le correctif seul. _Source : B09-D9, B09-D17_

## Hors périmètre

- Ajout d'un index sur la table des lignes de commande (`B09-D10`) : solution proposée par la DSI, traitée comme piste de conception dans `design.md` (H27), pas comme exigence.
- Passage de l'export en asynchrone (`B09-D11`) : solution proposée par la DSI, traitée comme piste de conception dans `design.md` (H27), pas comme exigence.
- Les nouvelles fonctions de l'espace vendeur (suivi des ventes, factures, alertes, coordonnées bancaires, etc.) : relèvent du projet P07.
- Compréhension des reversements, évoquée dans le verbatim de MKP-11 (B09-F8) : non détaillée dans les sources.

## Hypothèses

| Id | Hypothèse | Conflit | Réversible |
|---|---|---|---|
| H27 | Pour MKP-11, la spec commence par mesurer les temps de réponse des pages de l'espace vendeur ; le seuil attendu est fixé avec la direction marketplace à partir de cette mesure. Les solutions de la DSI pour MKP-07 (index, export asynchrone) sont des pistes de conception, pas des exigences. | — | oui |

## Questions ouvertes

| Id | Question | Destinataire | Bloquante |
|---|---|---|---|
| Q28 | Quelles pages de l'espace vendeur sont jugées lentes, quel temps de réponse est attendu et combien de vendeurs se plaignent ? | Direction marketplace ; DSI | non (le seuil du critère 2.4 reste un paramètre en attendant) |
| Q34 | L'exigence d'hébergement dans le cloud d'Orvanne s'applique-t-elle à ce projet, ou un hébergement dans l'UE chez un éditeur est-il admis (CT-08) ? | DSI (comité d'architecture) | non |
