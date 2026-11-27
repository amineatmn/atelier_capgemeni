# Plan d'implémentation : prise de rendez-vous des livraisons fournisseurs

Pilote sur E1 au printemps, avec une vingtaine de fournisseurs. Aucune mise en production pendant le gel du 16/11 au 11/01 (CT-07).

- [ ] 1. Prérequis (aucune dépendance)
  - [ ] 1.1 Soumettre l'analyse du traitement à la DPO : base légale, durées de conservation, ouverture à des tiers (Q13)
    - _Exigences : 11.4, 11.5_
  - [ ] 1.2 Établir le contrat d'interface des commandes d'achat avec Passerelle (Q06)
    - _Exigences : 4.1, 4.2_
  - [ ] 1.3 Recueillir le paramétrage de E1 et la liste des fournisseurs pilotes
    - _Exigences : 2.1, 2.2_
  - [ ] 1.4 Constituer un jeu de données synthétique (CT-04)
    - _Exigences : 11.1_

- [ ] 2. Socle (dépend de 1.1)
  - [ ] 2.1 Créer le schéma de la base, dont la contrainte d'unicité (quai, début de créneau)
    - _Exigences : 3.6, 11.4_
  - [ ] 2.2 Mettre en place l'authentification des comptes externes, le SSO interne, les rôles et le journal
    - _Exigences : 1.5, 11.5_
  - [ ] 2.3 Développer la gestion des comptes fournisseurs et le rattachement des transporteurs
    - _Exigences : 1.1, 1.2, 1.3_
  - [ ] 2.4 Mettre en place l'internationalisation (français et anglais) du portail et des e-mails
    - _Exigences : 1.4_

- [ ] 3. Paramétrage des sites (dépend de 2.1)
  - [ ] 3.1 Développer l'écran de paramétrage : quais, horaires, jours fermés, durée de créneau, bornes
    - _Exigences : 2.1, 2.2, 2.3_
  - [ ] 3.2 Afficher la capacité qui résulte du paramétrage
    - _Exigences : 2.4_
  - [ ] 3.3 Refuser une modification qui touche des réservations, en listant celles-ci
    - _Exigences : 2.5_

- [ ] 4. Commandes d'achat (dépend de 1.2 et 2.1)
  - [ ] 4.1 Synchroniser la copie locale et contrôler une commande à la saisie
    - _Exigences : 4.1, 4.2, 4.3_
  - [ ] 4.2 Prévoir le mode dégradé « à revérifier » et l'alerte si une commande est soldée
    - _Exigences : 4.4, 4.5_

- [ ] 5. Réservation (dépend de 3.1 et 4.1)
  - [ ] 5.1 Développer la recherche de créneaux libres (1 ou 2 consécutifs) dans les bornes
    - _Exigences : 3.1, 3.3, 3.4_
  - [ ] 5.2 Développer la création d'une réservation : commandes, quai attribué, numéro, e-mail du transporteur
    - _Exigences : 3.2, 3.5, 3.7_
  - [ ] 5.3 Développer la modification et l'annulation jusqu'à la clôture
    - _Exigences : 5.1, 5.2, 5.3_
  - [ ] 5.4 Écrire les tests unitaires des règles et le test de concurrence (50 réservations simultanées)
    - _Exigences : 3.4, 3.6, 5.2_

- [ ] 6. E-mails (dépend de 5.2)
  - [ ] 6.1 Envoyer la confirmation, le rappel et les e-mails liés aux actions du chef de quai, avec reprise sur erreur
    - _Exigences : 6.1, 6.2, 6.3_
  - [ ] 6.2 Utiliser des modèles d'e-mail limités aux informations de service
    - _Exigences : 6.4_

- [ ] 7. Espace du chef de quai (dépend de 5.2)
  - [ ] 7.1 Développer la vue planning par jour et par quai, la charge du lendemain et le rafraîchissement en moins de 60 s
    - _Exigences : 8.1, 8.2, 8.3_
  - [ ] 7.2 Développer les actions déplacer, forcer avec motif et bloquer (y compris de façon récurrente), et leur journalisation
    - _Exigences : 7.1, 7.2, 7.3, 7.4, 7.5_
  - [ ] 7.3 Ajouter la saisie du début et de la fin du déchargement
    - _Exigences : 8.4_

- [ ] 8. Poste de garde (dépend de 5.2)
  - [ ] 8.1 Développer le pointage : recherche de la réservation, heure d'arrivée, tolérance de 20 minutes, statut « perdue »
    - _Exigences : 9.1, 9.2_
  - [ ] 8.2 Gérer les arrivées sans réservation par catégorie et la liste à affecter par le chef de quai, sans donnée sur le chauffeur
    - _Exigences : 9.3, 9.4, 9.5_

- [ ] 9. Indicateurs (dépend de 7.3 et 8.1)
  - [ ] 9.1 Calculer chaque nuit les indicateurs (définitions de H12), disponibles à 6 h 00
    - _Exigences : 10.1, 10.2, 10.3_
  - [ ] 9.2 Développer l'export CSV, sans notation des fournisseurs
    - _Exigences : 10.4, 10.5_

- [ ] 10. Recette et pilote (dépend de 6 à 9)
  - [ ] 10.1 Tester la performance et la disponibilité
    - _Exigences : 11.1, 11.2_
  - [ ] 10.2 Déployer dans le cloud d'Orvanne et démarrer le pilote sur E1
    - _Exigences : 11.3_
  - [ ] 10.3 Faire la recette métier avec le chef de quai et le poste de garde de E1
    - _Exigences : 7.2, 8.1, 9.1, 9.2_
