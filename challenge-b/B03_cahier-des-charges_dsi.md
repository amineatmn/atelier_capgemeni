# Cahier des charges : portail de retours en libre-service (extrait)

Référence : CDC-RET-2026. Version 0.3 du 06/10/2026. Statut : en relecture.
Rédaction : Inès Rouvière (DSI, cheffe de projet digital). Commanditaire : direction de l'expérience client.
Extrait : sections 2 à 6. Les sections 1 (contexte du groupe), 7 (budget) et 8 (planning détaillé) ne sont pas reproduites ici.

## 2. Objectifs

Aujourd'hui, un client qui souhaite retourner un article doit contacter le service client, qui crée la demande dans Comptoir et lui envoie l'étiquette par e-mail. Ce parcours représente environ 900 demandes par jour ouvré, avec un délai moyen de 2,5 jours entre la demande et la réception de l'étiquette.

Le portail doit permettre :
- O1 : au client de déclarer un retour et d'obtenir son étiquette en moins de 3 minutes, sans contact avec un conseiller ;
- O2 : de réduire de 60 % les contacts liés aux retours en 6 mois ;
- O3 : de donner aux entrepôts une visibilité sur les retours attendus.

## 3. Périmètre

Inclus : articles vendus et expédiés par Orvanne, France métropolitaine, commandes passées sur Vitrine (site web et application mobile).

Exclus : articles des vendeurs partenaires de la marketplace, articles volumineux livrés sur rendez-vous, échanges (un échange reste un retour suivi d'une nouvelle commande).

Le portail est accessible sans création de compte, à partir du numéro de commande et de l'adresse e-mail utilisée lors de l'achat.

## 4. Exigences fonctionnelles

| Id | Exigence | Priorité |
|---|---|---|
| EF-01 | Le client retrouve sa commande et voit, pour chaque article, s'il est éligible au retour. | Indispensable |
| EF-02 | Un article est éligible pendant 30 jours à compter de la livraison, s'il n'appartient pas à une catégorie exclue (hygiène, produits personnalisés, denrées). | Indispensable |
| EF-03 | Le client connecté à son compte sélectionne les articles, la quantité et un motif dans une liste fermée. | Indispensable |
| EF-04 | Le client choisit un mode de retour : dépôt en point relais ou enlèvement à domicile. | Indispensable |
| EF-05 | Le portail génère une étiquette prépayée (PDF et QR code) et l'envoie par e-mail. | Indispensable |
| EF-06 | Le client suit l'avancement de son retour (déclaré, déposé, reçu, remboursé). | Important |
| EF-07 | Le remboursement est déclenché automatiquement dès le premier scan du colis par le transporteur. | Indispensable |
| EF-08 | L'entrepôt de destination reçoit la liste prévisionnelle des retours attendus. | Important |
| EF-09 | Le client peut joindre jusqu'à 3 photos lorsque le motif est « article endommagé ». | Souhaitable |
| EF-10 | Le service client peut créer ou corriger un retour pour le compte d'un client. | Important |

## 5. Exigences non fonctionnelles

- ENF-01 : disponibilité de 99,5 %, mesurée chaque mois.
- ENF-02 : pages affichées en moins de 2 secondes pour 95 % des requêtes, jusqu'à 300 utilisateurs simultanés.
- ENF-03 : conformité RGPD, hébergement dans l'Union européenne.
- ENF-04 : interface conforme au RGAA et utilisable sur mobile.
- ENF-05 : journalisation des actions réalisées par le service client.

## 6. Interfaces et contraintes

- Commandes et livraisons : lecture dans le système de gestion des commandes, via Passerelle.
- Étiquettes : API des transporteurs.
- Remboursements : appel au prestataire de paiement ; le remboursement est effectué sur le moyen de paiement d'origine.
- Entrepôts : alimentation de Hangar par fichier quotidien.
- Les retours sont gratuits pour le client.
- Mise en service visée : avant les soldes d'hiver, sur un périmètre pilote.

Critère de recette global : lors des tests utilisateurs, un retour standard est réalisé de bout en bout par un client non accompagné, sur mobile.
