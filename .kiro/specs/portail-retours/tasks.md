# Plan d'implémentation : Portail de retours en libre-service, remboursement et visibilité des entrepôts

Lots : V1 (pilote, mise en service au plus tôt le 12 janvier, hors gel) puis V2 (photos, marketplace).

- [ ] 1. Prérequis
  - [ ] 1.1 Obtenir l'avis de la DPO sur le traitement (analyse d'impact, durées de conservation, base légale)
    - _Exigences : 14.3, 15.2_
  - [ ] 1.2 Figer les contrats d'interface (Passerelle, API transporteurs, prestataire de paiement, fichier Hangar, note de contrôle de P03)
    - _Exigences : 3.4, 4.1, 6.2, 8.2_
  - [ ] 1.3 Produire un jeu de données synthétique (commandes, clients, retours), sans donnée de production
    - _Exigences : 14.4_
  - [ ] 1.4 Confirmer l'hébergement UE et les exigences RGAA avec la DSI
    - _Exigences : 14.1, 14.2_
  - [ ] 1.5 Caler le calendrier de mise en service hors gel avec la DSI
    - _Exigences : 15.1, 15.2, 15.3_

- [ ] 2. Socle de données et paramètres (dépend de 1.1, 1.2)
  - [ ] 2.1 Modèle de données Retour, Ligne, Remboursement, Paramètres historisés
    - _Exigences : 5.1, 6.6_
  - [ ] 2.2 Paramètres : déclencheur, délais par catégorie, frais par motif, seuils
    - _Exigences : 2.2, 6.1, 7.1_
  - [ ] 2.3 Tests unitaires du modèle et des paramètres
    - _Exigences : 2.2, 6.1, 7.1_

- [ ] 3. Parcours client (dépend de 2.1, 2.2)
  - [ ] 3.1 Accès sans compte et accès connecté, limité à la commande saisie
    - _Exigences : 1.1, 1.2, 1.3_
  - [ ] 3.2 Message uniforme et blocage des essais
    - _Exigences : 1.4_
  - [ ] 3.3 Lecture des commandes via Passerelle et gestion de son indisponibilité
    - _Exigences : 3.4, 3.5_
  - [ ] 3.4 Moteur d'éligibilité et affichage par article
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.5_
  - [ ] 3.5 Absence d'échange et renvoi vers une nouvelle commande
    - _Exigences : 2.6_
  - [ ] 3.6 Sélection des articles, quantité, motif, mode de retour
    - _Exigences : 3.1, 3.2, 3.3_
  - [ ] 3.7 Affichage des frais avant validation
    - _Exigences : 7.3_
  - [ ] 3.8 Interface RGAA et mobile
    - _Exigences : 14.1_
  - [ ] 3.9 Tests unitaires et d'intégration du parcours
    - _Exigences : 1.1, 1.2, 1.3, 1.4, 2.1, 2.6, 3.1, 3.2, 3.5_

- [ ] 4. Étiquette, RMA et e-mails (dépend de 2.1, 1.2)
  - [ ] 4.1 Adaptateur transporteurs : étiquette PDF et QR
    - _Exigences : 4.1_
  - [ ] 4.2 Envoi par e-mail sans offre commerciale et affichage
    - _Exigences : 4.2, 4.5_
  - [ ] 4.3 Génération du RMA en PDF
    - _Exigences : 4.3_
  - [ ] 4.4 Reprise automatique en cas de panne du transporteur
    - _Exigences : 4.4_
  - [ ] 4.5 Tests d'intégration avec doubles de transporteur
    - _Exigences : 4.1, 4.4, 4.5_

- [ ] 5. Suivi et remboursement (dépend de 2.2, 4.1)
  - [ ] 5.1 Statuts du retour et suivi côté client
    - _Exigences : 5.1, 5.3_
  - [ ] 5.2 Consommation du premier scan transporteur via Passerelle
    - _Exigences : 5.2_
  - [ ] 5.3 Moteur de remboursement paramétré, moyen de paiement d'origine, idempotence
    - _Exigences : 6.1, 6.2, 6.3, 6.4_
  - [ ] 5.4 Réception de la note A / B / C et signalement note C
    - _Exigences : 6.6, 6.7, 6.8_
  - [ ] 5.5 Reprises et alertes en cas d'échec du paiement
    - _Exigences : 6.5_
  - [ ] 5.6 Retenue des frais paramétrée
    - _Exigences : 7.1, 7.2_
  - [ ] 5.7 Tests unitaires et d'intégration (scan en double, paiement en échec)
    - _Exigences : 5.2, 6.2, 6.4, 6.5, 6.7, 7.2_

- [ ] 6. Entrepôts et service client (dépend de 2.1)
  - [ ] 6.1 Liste prévisionnelle par entrepôt
    - _Exigences : 8.1_
  - [ ] 6.2 Fichier quotidien Hangar et reprise sur échec
    - _Exigences : 8.2, 8.3_
  - [ ] 6.3 Extension Comptoir : création et correction de retours
    - _Exigences : 9.1_
  - [ ] 6.4 Journal d'audit et preuve d'exécution
    - _Exigences : 9.2, 9.3_
  - [ ] 6.5 Tests d'intégration Hangar et Comptoir
    - _Exigences : 8.1, 8.3, 9.1, 9.2_

- [ ] 7. Marketplace en V1 : non éligibles (dépend de 3.4)
  - [ ] 7.1 Affichage de l'inéligibilité et renvoi vers le circuit actuel
    - _Exigences : 10.1_

- [ ] 8. Qualité et recette V1 (dépend de 3, 4, 5, 6, 7)
  - [ ] 8.1 Test de charge à 300 utilisateurs simultanés, disponibilité et supervision
    - _Exigences : 12.1, 12.2_
  - [ ] 8.2 Indicateur mensuel des contacts liés aux retours
    - _Exigences : 13.2_
  - [ ] 8.3 Recette de bout en bout sur mobile, étiquette en moins de 3 minutes
    - _Exigences : 13.1, 13.3_
  - [ ] 8.4 Mise en service du pilote hors gel
    - _Exigences : 15.1, 15.2, 15.3_

- [ ] 9. Lot V2 (dépend de 8.4)
  - [ ] 9.1 Photos jointes (3 maximum), stockage UE, purge
    - _Exigences : 11.1, 11.3_
  - [ ] 9.2 Consultation des photos par E2
    - _Exigences : 11.2_
  - [ ] 9.3 Retours marketplace : circuit vendeur et étiquettes distinctes
    - _Exigences : 10.2_
  - [ ] 9.4 Suivi des retours et litiges par le vendeur (avec P07)
    - _Exigences : 10.3_
  - [ ] 9.5 Tests et recette V2
    - _Exigences : 10.2, 10.3, 11.1, 11.3_
