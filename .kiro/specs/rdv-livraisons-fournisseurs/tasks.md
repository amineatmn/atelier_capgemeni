# Plan d'implémentation : prise de rendez-vous des livraisons fournisseurs

Pilote sur E1 au printemps avec une vingtaine de fournisseurs. Aucune mise en production du 16/11 au 11/01 (CT-07) : le développement et la recette se font en préproduction, la première mise en production a lieu après le gel.

- [ ] 1. Prérequis (aucune dépendance)
  - [ ] 1.1 Soumettre l'analyse du traitement à la DPO (CT-01) et inscrire les contacts au registre (P05)
    - _Exigences : 1.2, 11.4_
  - [ ] 1.2 Vérifier que les commandes d'achat sont disponibles dans Passerelle (échéance 27/11) et établir le contrat d'interface
    - _Exigences : 4.1, 4.3_
  - [ ] 1.3 Obtenir des achats la liste d'une vingtaine de fournisseurs pilotes (27/11) et de la DSI le chiffrage (décembre)
    - _Exigences : 1.1, 11.1_
  - [ ] 1.4 Recueillir le paramétrage cible de E1 (04/12) et les horaires des sites
    - _Exigences : 2.1, 2.2, 2.3_
  - [ ] 1.5 Constituer un jeu de données synthétique (CT-04)
    - _Exigences : 11.5_

- [ ] 2. Socle (dépend de 1.1)
  - [ ] 2.1 Créer le schéma de la base, dont l'unicité (quai, début de créneau)
    - _Exigences : 3.7, 11.3_
  - [ ] 2.2 Mettre en place l'authentification des comptes externes, le SSO interne, les rôles et le journal
    - _Exigences : 1.2, 11.4_
  - [ ] 2.3 Développer le rattachement des transporteurs par les fournisseurs
    - _Exigences : 1.3_
  - [ ] 2.4 Mettre en place le catalogue de langues, le RGAA et l'affichage mobile du portail
    - _Exigences : 1.4, 1.5, 6.5_

- [ ] 3. Paramétrage des sites (dépend de 2.1)
  - [ ] 3.1 Développer l'écran : quais, horaires, jours fermés, durée de créneau, bornes, heure du rappel
    - _Exigences : 2.1, 2.2, 2.3, 3.4, 6.2_
  - [ ] 3.2 Afficher la capacité résultante et refuser une modification qui touche des réservations
    - _Exigences : 2.4, 2.5_

- [ ] 4. Commandes d'achat (dépend de 1.2 et 2.1)
  - [ ] 4.1 Synchroniser la copie locale et contrôler une commande à la saisie
    - _Exigences : 4.1, 4.2, 4.5_
  - [ ] 4.2 Développer le mode dégradé « à revérifier » et l'alerte si une commande est soldée
    - _Exigences : 4.3, 4.4_

- [ ] 5. Réservation (dépend de 3.1, 4.1 et 2.3)
  - [ ] 5.1 Développer la recherche de créneaux libres (1 ou 2 consécutifs) dans les bornes
    - _Exigences : 3.1, 3.3, 3.4, 3.5_
  - [ ] 5.2 Développer la création : commandes, quai attribué, numéro, e-mail du transporteur
    - _Exigences : 3.2, 3.6, 3.8, 1.1_
  - [ ] 5.3 Développer la modification et l'annulation jusqu'à la clôture
    - _Exigences : 5.1, 5.2, 5.3_
  - [ ] 5.4 Écrire les tests unitaires des règles et le test de concurrence (50 réservations simultanées)
    - _Exigences : 3.4, 3.7, 5.2_

- [ ] 6. E-mails (dépend de 5.2)
  - [ ] 6.1 Envoyer confirmation, rappel et informations liées aux actions du chef de quai, avec reprise sur erreur
    - _Exigences : 6.1, 6.2, 6.3, 6.4_
  - [ ] 6.2 Rédiger les modèles d'e-mail, limités aux informations de service, dans chaque langue
    - _Exigences : 6.5_

- [ ] 7. Espace du chef de quai (dépend de 5.2)
  - [ ] 7.1 Développer la vue planning par jour et par quai et la charge du lendemain
    - _Exigences : 8.1, 8.2_
  - [ ] 7.2 Développer déplacer, forcer avec motif, bloquer (dont plage fixe pour les messageries) et la journalisation
    - _Exigences : 7.1, 7.2, 7.3, 7.4, 7.5_
  - [ ] 7.3 Ajouter la saisie du début et de la fin du déchargement
    - _Exigences : 8.3_

- [ ] 8. Poste de garde (dépend de 5.2)
  - [ ] 8.1 Développer le pointage : recherche de la réservation, heure d'arrivée, tolérance de 20 minutes, créneau perdu
    - _Exigences : 9.1, 9.2, 9.5_
  - [ ] 8.2 Gérer les arrivées sans réservation et la liste présentée au chef de quai
    - _Exigences : 9.3, 9.4_

- [ ] 9. Indicateurs (dépend de 7.3 et 8.1)
  - [ ] 9.1 Calculer les indicateurs : sans rendez-vous, attente moyenne, occupation, ponctualité par fournisseur
    - _Exigences : 10.1, 10.2, 10.3, 10.4, 11.3_
  - [ ] 9.2 Développer l'export CSV, sans notation ni pénalité
    - _Exigences : 10.5, 10.6_

- [ ] 10. Recette et pilote (dépend de 6 à 9)
  - [ ] 10.1 Tester la performance avec le double des volumes actuels
    - _Exigences : 11.1_
  - [ ] 10.2 Déployer dans le cloud d'Orvanne après le gel et démarrer le pilote sur E1
    - _Exigences : 11.2, 11.6_
  - [ ] 10.3 Faire la recette métier avec le chef de quai et le poste de garde de E1
    - _Exigences : 7.2, 8.1, 9.1, 9.2_
