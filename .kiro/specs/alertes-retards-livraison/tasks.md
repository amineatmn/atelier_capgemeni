# Plan d'implémentation : détection des retards de livraison, suivi colis dans Comptoir et information du client

Les tâches 1 à 5 forment le **lot 1** : outils internes, sans envoi aux clients, mis en service avant le pic seulement si une dérogation au gel est accordée (Q03, CT-07). Les tâches 6 à 9 forment le **lot 2** : Comptoir et messages, au T1 2027, après le 11 janvier.

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre le traitement à la DPO : base légale du message de service, durée de conservation, usage éventuel du mobile (CT-01, CT-02)
    - Livrable : avis écrit de la DPO
    - _Exigences : 9.3, 9.4_
  - [ ] 1.2 Vérifier avec l'équipe Passerelle les flux des 3 transporteurs (fréquence, format) et la disponibilité de la date promise par colis (Q05)
    - Livrable : contrat d'interface du flux de statuts
    - _Exigences : 1.1, 1.3, 1.4, 2.8_
  - [ ] 1.3 Qualifier les possibilités d'extension de Comptoir (encart, file, liste) et le service d'envoi des e-mails de service
    - Livrable : note de choix d'intégration
    - _Exigences : 4.1, 6.2_
  - [ ] 1.4 Constituer un jeu de données synthétique : 210 000 colis, 3 transporteurs, 3 entrepôts, cas aux bornes (CT-04)
    - _Exigences : 9.1, 9.7_

- [ ] 2. Référentiel de suivi et collecte des statuts (dépend de 1.2)
  - [ ] 2.1 Créer le schéma du référentiel (Colis, ÉvénementStatut, Paramètre, Journal) et ses index
    - _Exigences : 1.2, 9.4_
  - [ ] 2.2 Développer le collecteur : consommation du flux Passerelle, normalisation des codes des 3 transporteurs, codes inconnus
    - _Exigences : 1.1, 1.3_
  - [ ] 2.3 Implémenter le dédoublonnage par clé (colis, code, horodatage)
    - _Exigences : 1.5_
  - [ ] 2.4 Rattacher chaque colis à sa commande, son entrepôt, sa région et sa date promise
    - _Exigences : 1.2_
  - [ ] 2.5 Mettre en place la supervision : fraîcheur par transporteur, alerte d'interruption, délai de bout en bout
    - _Exigences : 1.4, 1.6_
  - [ ] 2.6 Écrire les tests unitaires et d'intégration du collecteur
    - _Exigences : 1.1, 1.3, 1.5_

- [ ] 3. Moteur de retards (dépend de 2.1)
  - [ ] 3.1 Calculer le niveau de chaque colis : `à surveiller` à J+1 matin, `en retard` à 48 h, sortie à la livraison, prise en compte d'une date promise modifiée
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.7_
  - [ ] 3.2 Lire les seuils et le niveau d'alerte dans les paramètres, avec écran d'administration minimal
    - _Exigences : 2.5_
  - [ ] 3.3 Lancer le recalcul quotidien de tous les colis non livrés avant la liste du matin
    - _Exigences : 2.6_
  - [ ] 3.4 Gérer la date promise absente et publier `NiveauModifié`
    - _Exigences : 2.1, 2.8_
  - [ ] 3.5 Écrire les tests aux bornes : veille, J, J+1, J+2, livré, date modifiée, date absente, seuil modifié
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_

- [ ] 4. API de suivi et tableau de bord (dépend de 3.1)
  - [ ] 4.1 Développer l'API de suivi en lecture avec SSO, rôles et journalisation des accès
    - _Exigences : 3.1, 3.2, 3.5, 9.5_
  - [ ] 4.2 Développer les ventilations par transporteur, entrepôt et région
    - _Exigences : 3.1_
  - [ ] 4.3 Développer les listes et le détail d'un colis, avec code couleur et tri
    - _Exigences : 3.2, 3.3_
  - [ ] 4.4 Afficher l'heure de dernière mise à jour et le bandeau d'interruption de flux
    - _Exigences : 3.4, 1.6_
  - [ ] 4.5 Ajouter l'export CSV
    - _Exigences : 3.6_
  - [ ] 4.6 Tester la charge : 100 statuts / s pendant 1 h avec 210 000 colis en base
    - _Exigences : 1.4, 9.1_
  - [ ] 4.7 Faire la recette métier avec la logistique sur une journée synthétique rejouée
    - _Exigences : 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 5. Mise en service du lot 1 (dépend de 4, et de Q03 pour la date)
  - [ ] 5.1 Déployer dans le cloud d'Orvanne (UE), hors période de gel sauf dérogation, et ouvrir les accès
    - _Exigences : 9.2, 9.8, 3.5_

- [ ] 6. Intégration Comptoir (lot 2, dépend de 1.3 et 4.1)
  - [ ] 6.1 Ajouter l'encart de suivi dans la fiche commande pour les 3 transporteurs
    - _Exigences : 4.1, 4.3_
  - [ ] 6.2 Limiter l'attente à 1,5 s et prévoir le mode dégradé
    - _Exigences : 4.2, 4.4_
  - [ ] 6.3 Produire la liste quotidienne, consultable dans Comptoir et exportable en CSV, avec les commandes à dossier ouvert signalées
    - _Exigences : 5.1, 5.2, 5.3, 5.4_
  - [ ] 6.4 Afficher l'historique des messages de retard dans la commande
    - _Exigences : 6.8_

- [ ] 7. Back-office des modèles et paramètres (lot 2, dépend de 3.2)
  - [ ] 7.1 Gérer les modèles par canal et par cas : création, prévisualisation, activation, versions
    - _Exigences : 8.1, 8.4_
  - [ ] 7.2 Restreindre les variables et refuser les contenus commerciaux à l'activation
    - _Exigences : 8.2, 8.3_
  - [ ] 7.3 Vérifier la longueur d'un SMS (160 caractères)
    - _Exigences : 8.5_
  - [ ] 7.4 Ajouter les paramètres : canal, plage horaire, délai de validation, validation Premium, conservation, verrou SMS
    - _Exigences : 6.2, 6.3, 6.7, 7.5, 7.9, 9.3, 9.4_
  - [ ] 7.5 Écrire les tests du contrôle anti-commercial et du verrou SMS
    - _Exigences : 8.3, 9.3_

- [ ] 8. Service de notification (lot 2, dépend de 3.4, 6.1 et 7.1)
  - [ ] 8.1 Consommer `NiveauModifié`, regrouper les colis par commande, garantir un message par commande et par niveau, sans contenu commercial
    - _Exigences : 6.1, 6.6, 6.9_
  - [ ] 8.2 Programmer les envois dans la plage horaire et après la liste du matin
    - _Exigences : 6.7, 7.4_
  - [ ] 8.3 Vérifier l'absence de dossier ouvert à l'envoi, reporter si Comptoir est indisponible
    - _Exigences : 7.1, 7.2, 7.3_
  - [ ] 8.4 Gérer la file de validation Premium (option désactivée par défaut) : dépôt, validation, rejet motivé, expiration
    - _Exigences : 7.5, 7.6, 7.7, 7.9_
  - [ ] 8.5 Annuler les messages programmés quand la commande est livrée
    - _Exigences : 7.8_
  - [ ] 8.6 Construire le message avec ou sans nouvelle date, lire l'e-mail dans Vitrine, envoyer, réessayer
    - _Exigences : 6.2, 6.4, 6.5_
  - [ ] 8.7 Implémenter le canal SMS derrière son option, désactivé par défaut
    - _Exigences : 6.3_
  - [ ] 8.8 Journaliser chaque message et les actions des conseillers
    - _Exigences : 6.8, 9.5_
  - [ ] 8.9 Écrire les tests des règles d'envoi : seuil, doublon, plage horaire, dossier ouvert, Premium, livraison avant envoi
    - _Exigences : 6.1, 6.6, 6.7, 7.1, 7.2, 7.5, 7.6, 7.7, 7.8_

- [ ] 9. Indicateurs, conservation et recette du lot 2 (dépend de 6, 7 et 8)
  - [ ] 9.1 Produire les indicateurs quotidiens des messages
    - _Exigences : 9.6_
  - [ ] 9.2 Implémenter la purge selon la durée de conservation paramétrée
    - _Exigences : 9.4_
  - [ ] 9.3 Tester la charge et la résilience de bout en bout : pic, coupure de Comptoir, coupure du service d'envoi
    - _Exigences : 4.2, 4.4, 7.3, 9.1_
  - [ ] 9.4 Faire la recette métier avec le service client : liste, file Premium, modèles relus par la DPO
    - _Exigences : 5.1, 5.2, 7.4, 7.5, 8.1, 8.2_
  - [ ] 9.5 Mettre en service après le 11 janvier avec le canal e-mail seul
    - _Exigences : 6.2, 9.2, 9.8_
