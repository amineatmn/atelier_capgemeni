---
inclusion: auto
name: contraintes-transverses
description: Contraintes transverses d'Orvanne (RGPD, gel des mises en production, hébergement, canaux de message). À utiliser pour analyser les besoins, rédiger ou contrôler une spec.
---
# Contraintes transverses

<!-- Responsable : B. Ces contraintes deviennent les CT-nn de work/analyse.json. Garder les deux synchronisés. -->

| Id | Contrainte | Source | Projets touchés (provisoire) |
|---|---|---|---|
| CT-01 | Tout nouveau traitement de données personnelles est soumis à la DPO avant développement | B07 | tous |
| CT-02 | Le numéro de mobile est collecté pour la livraison ; tout autre usage suppose une analyse préalable | B07 | P01, P04 |
| CT-03 | Un message de service ne contient pas d'offre commerciale | B07, B02 | P01 |
| CT-04 | Aucune donnée de production pour des démos ou des tests sans anonymisation | B07 | P04, tous |
| CT-05 | Données de prospection conservées au plus 3 ans après le dernier contact | B07 | P04 |
| CT-06 | Photos et pièces jointes = données personnelles si une étiquette ou une personne est visible | B07 | P02, P03 |
| CT-07 | Gel des mises en production du 16/11 au 11/01 | B02 | tous |
| CT-08 | Hébergement dans le cloud d'Orvanne / dans l'UE | B01, B03 | à confirmer pour tous |

<!-- À compléter : accessibilité RGAA (B03), journalisation des actions du service client (B03), fournisseurs non francophones (B08)… -->
