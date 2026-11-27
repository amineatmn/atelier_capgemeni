---
inclusion: auto
name: contraintes-transverses
description: Contraintes transverses d'Orvanne (RGPD, gel des mises en production, hébergement, canaux de message). À utiliser pour analyser les besoins, rédiger ou contrôler une spec.
---
# Contraintes transverses
<!-- Responsable : B. Ces contraintes deviennent les CT-nn de work/analyse.json. Garder les deux synchronisés. Ne pas renuméroter CT-01 à CT-08 : l'exemple d'analyse et les autres agents les utilisent. -->

Une contrainte transverse s'applique à plusieurs projets et ne se négocie pas projet par projet. Elle vient d'une autorité (DPO, DSI, règle déjà en vigueur) ou d'un constat partagé par plusieurs documents.

Statut :
- **Établie** : énoncée telle quelle dans une source par une personne qui a autorité sur le sujet.
- **Généralisée** : énoncée pour un seul projet et étendue aux autres par l'analyse. À confirmer ; une spec qui l'applique la cite avec l'hypothèse correspondante.

## Registre

| Id | Contrainte | Source | Statut | Projets touchés (provisoire) |
|---|---|---|---|---|
| CT-01 | Tout nouveau traitement de données personnelles est soumis à la DPO avant développement | B07 « Points d'attention » | Établie | tous |
| CT-02 | Le numéro de mobile est collecté pour la livraison ; tout autre usage, y compris une notification de service par SMS, suppose une analyse préalable de la DPO | B07 | Établie | P01, P04 |
| CT-03 | Un message de service ne contient pas d'offre commerciale (code promo, remise, recommandation) | B07, B02 §B | Établie | P01, P02 |
| CT-04 | Aucune donnée de production pour des démos ou des tests sans anonymisation | B07 | Établie | tous, P04 en premier |
| CT-05 | Données de prospection conservées au plus 3 ans après le dernier contact ; les historiques antérieurs doivent être purgés ou anonymisés | B07 | Établie | P04, P05 |
| CT-06 | Photos et pièces jointes = données personnelles si une étiquette ou une personne est visible | B07 | Établie | P02, P03 |
| CT-07 | Gel des mises en production du 16/11/2026 au 11/01/2027 : aucune mise en service dans cette période (le développement reste possible) | B02 commentaire du 21/10 | Établie (portée à confirmer : la source est le service client, pas la DSI) | tous |
| CT-08 | Hébergement dans le cloud d'Orvanne, dans l'UE ; une solution intégrée à l'existant est préférée à l'achat d'un produit d'éditeur | B01, B03 ENF-03, B07 « Attentes » | Établie | tous |
| CT-09 | Les échanges avec les systèmes existants (commandes, livraisons, statuts transporteurs, commandes d'achat) passent par Passerelle | B01, B03 §6, B08 §5 | Établie | P01, P02, P06 |
| CT-10 | Tout système qui stocke des données clients doit pouvoir être piloté par l'outil de gestion des droits : export des données d'une personne, effacement ou anonymisation, isolement des données à conservation légale (factures : 10 ans), preuve d'exécution | B07 « Besoin » 3 à 5, « Constat » | Établie | P01, P02, P03, P04, P05, P07 |
| CT-11 | Le service client est informé de tout message envoyé aux clients et modifie lui-même les textes des messages, sans passer par la DSI | B02 §B, commentaire du 23/10 ; B01 (« le service client sera informé ») | Établie pour P01, généralisée pour les autres | P01, P02 ; P04 à confirmer |
| CT-12 | Les actions des utilisateurs internes sur des données client ou sensibles (création, correction, validation, modification bancaire) sont journalisées | B03 ENF-05, B07 (preuve de clôture), B09 MKP-05 | Généralisée | P01, P02, P05, P07 |
| CT-13 | Les interfaces destinées aux clients et aux partenaires externes sont accessibles (RGAA) et utilisables sur mobile | B03 ENF-04, B09 MKP-12 | Généralisée | P02 ; P06, P07 à confirmer |
| CT-14 | Les interfaces et messages destinés aux partenaires externes tiennent compte des utilisateurs non francophones | B08 §3 (15 % de fournisseurs étrangers), B09 MKP-10 | Généralisée, langues non définies | P06, P07 |

## Comment appliquer ces contraintes

**Dans l'analyse (agent analyste)**
- Chaque `CT-nn` de `work/analyse.json` reprend l'énoncé ci-dessus et cite comme `sources` les demandes `B0x-Dn` des fiches qui l'expriment. Si aucune demande ne l'exprime encore dans les fiches, le signaler dans `work/analyse.md` (l'extracteur a peut-être manqué une phrase).
- Une demande contraire à une contrainte **établie** devient un conflit `Cnn` dont l'hypothèse applique la contrainte. La demande est ensuite exclue avec la raison « contraire à CT-nn, voir Cnn ». Elle n'est jamais exclue sans conflit : le demandeur doit savoir pourquoi.
- Une demande contraire à une contrainte **généralisée** devient un conflit ordinaire : la contrainte n'a pas d'autorité tant qu'elle n'est pas confirmée.
- Une contrainte découverte en cours d'analyse est ajoutée avec l'identifiant libre suivant (CT-15, CT-16…) et signalée à B pour mise à jour de ce fichier.

**Dans les specs (rédacteur et contrôleur)**
- CT-01 : la spec contient une section sur les données personnelles et le plan de tâches commence par la revue DPO des traitements concernés.
- CT-02, CT-03 : tout canal SMS est désactivé par défaut ; aucun gabarit de message de service ne contient de champ promotionnel.
- CT-04 : les tâches de test et de démo précisent des données synthétiques ou anonymisées.
- CT-07 : aucune date de mise en service entre le 16/11/2026 et le 11/01/2027. Toute échéance demandée dans cette période devient un conflit.
- CT-10 : la conception décrit comment le projet exporte et efface les données d'une personne.
- CT-12 : le modèle de données comporte un journal (qui, quoi, quand, avant/après).

## Repères de calendrier pour CT-07

Ces dates ne viennent pas des sources ; elles servent à détecter les échéances incompatibles avec le gel. À confirmer avant de les citer comme faits.

| Date | Événement | Projets |
|---|---|---|
| 27/11/2026 | Black Friday, début probable du « pic » de B01 | P01 |
| ~06/01/2027 | Début probable des soldes d'hiver (règle du premier ou deuxième mercredi de janvier, à vérifier) | P02 |
| Janvier 2027 | Inventaire de E2, date inconnue | P03 |

## Ce qui n'est pas une contrainte transverse

- Les seuils de retard (48 h, J+1, 2 %, 5 %, 20 minutes) : ce sont des règles propres à chaque projet, souvent en conflit.
- Le statut Premium ou Orvanne+ : c'est un terme du glossaire, dont la définition est une question ouverte.
- La disponibilité de 99,5 % et le temps d'affichage de 2 secondes (B02, B03) : ils restent des exigences du projet qui les exprime.
