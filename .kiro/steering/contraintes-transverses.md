---
inclusion: auto
name: contraintes-transverses
description: Contraintes transverses d'Orvanne (RGPD, gel des mises en production, hébergement, canaux de message). À utiliser pour analyser les besoins, rédiger ou contrôler une spec.
---
# Contraintes transverses

<!-- Les identifiants CT-nn sont ceux de work/analyse.json (source de vérité, cités par les specs).
     Les propositions de B sans équivalent dans l'analyse sont listées à la fin, sans identifiant :
     l'analyste les numérotera à sa prochaine exécution. -->

| Id | Contrainte | Sources | Projets |
|---|---|---|---|
| CT-01 | Tout nouveau traitement de données personnelles est soumis à la DPO avant développement. | B07-D10 | P01, P02, P03, P04, P05, P06, P07 |
| CT-02 | Le numéro de mobile est collecté pour la livraison ; tout autre usage (alerte, relance) suppose une analyse préalable de la DPO. | B07-D11 | P01, P04 |
| CT-03 | Un message de service ne contient pas d'offre commerciale. | B07-D12, B02-D10 | P01, P02, P06 |
| CT-04 | Aucune donnée de production ne sert à des démonstrations ou à des tests sans anonymisation. | B07-D16 | P01, P02, P03, P04, P05, P06, P07, P08 |
| CT-05 | Les données de prospection ne sont pas conservées plus de 3 ans après le dernier contact du client. | B07-D13 | P04 |
| CT-06 | Les photos et pièces jointes, transmises par les clients ou prises en entrepôt, sont des données personnelles dès qu'une étiquette ou une personne y est visible. | B07-D15 | P02, P03 |
| CT-07 | Aucune mise en production pendant le gel, du 16 novembre au 11 janvier. | B02-D12 | P01, P02, P03, P04, P05, P06, P07, P08 |
| CT-08 | Hébergement dans l'Union européenne (B03) ; pour P01, dans le cloud d'Orvanne et non chez un éditeur (B01). La généralisation de l'exigence « cloud d'Orvanne » aux autres projets est à confirmer (Q34). | B01-D9, B03-D21 | P01, P02, P03, P04, P05, P06, P07, P08 |
| CT-09 | Les interfaces utilisées par des personnes extérieures à Orvanne sont conformes au RGAA et utilisables sur mobile. Exigé pour le portail de retours ; extension au portail fournisseurs et à l'espace vendeur à confirmer (Q35). | B03-D22 | P02, P06, P07 |
| CT-10 | Les actions réalisées par un collaborateur pour le compte d'un client ou d'un tiers sont journalisées et conservent une preuve d'exécution. | B03-D23, B07-D1 | P01, P02, P05, P07 |
| CT-11 | Une partie des utilisateurs externes n'est pas francophone (fournisseurs étrangers, vendeurs européens) : les écrans et messages doivent pouvoir être proposés dans d'autres langues. | B08-D21, B09-D15 | P06, P07 |

## Propositions de B à intégrer à la prochaine analyse

| Id | Contrainte | Source | Statut | Projets touchés (provisoire) |
|---|---|---|---|---|
| (à numéroter) | Les échanges avec les systèmes existants (commandes, livraisons, statuts transporteurs, commandes d'achat) passent par Passerelle | B01, B03 §6, B08 §5 | Établie | P01, P02, P06 |
| (à numéroter) | Tout système qui stocke des données clients doit pouvoir être piloté par l'outil de gestion des droits : export des données d'une personne, effacement ou anonymisation, isolement des données à conservation légale (factures : 10 ans), preuve d'exécution | B07 « Besoin » 3 à 5, « Constat » | Établie | P01, P02, P03, P04, P05, P07 |
| (à numéroter) | Le service client est informé de tout message envoyé aux clients et modifie lui-même les textes des messages, sans passer par la DSI | B02 §B, commentaire du 23/10 ; B01 (« le service client sera informé ») | Établie pour P01, généralisée pour les autres | P01, P02 ; P04 à confirmer |
