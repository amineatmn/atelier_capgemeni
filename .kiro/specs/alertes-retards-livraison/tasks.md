# Plan d'implémentation : détection des retards de livraison, suivi colis dans Comptoir et information du client

Les tâches 1 à 5 forment le **lot 1** : outils internes, sans envoi aux clients. Leur date de mise en service (tâche 5) dépend de la question bloquante **Q03** : dérogation au gel avant le 16 novembre, ou mise en service après le 11 janvier.
Les tâches 6 à 9 forment le **lot 2** : Comptoir, liste quotidienne et message par e-mail, au T1 2027, après le gel (CT-07).
Les tâches 10 et 11 forment le **lot 3 (V2)** : validation Premium (après réponse à Q04) et canal SMS (après avis de la DPO sur le mobile, CT-02, et accord budgétaire, Q01).

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre l'analyse du traitement à la DPO (CT-01, Q36) : base légale du message de service, durée de conservation, liste des variables de service, liste des termes commerciaux interdits ; préparer le dossier mobile (CT-02) pour le lot 3
    - Livrable : avis écrit de la DPO versé au dossier du projet ; listes validées
    - _Exigences : 11.3, 9.2, 9.3, 10.3_
  - [ ] 1.2 Obtenir l'arbitrage de la DSI sur Q03 et produire le planning des lots demandé par la logistique (B01-D11)
    - Livrable : planning daté des lots 1, 2 et 3, avec ou sans dérogation au gel
    - _Exigences : 11.7_
  - [ ] 1.3 Établir avec l'équipe Passerelle le contrat d'interface des statuts et des commandes : couverture des 3 transporteurs, fréquence de réception (Q05), codes de statut, date promise, entrepôt, adresse de livraison, nouvelle date de livraison
    - Livrable : contrat d'interface signé par l'équipe Passerelle
    - _Exigences : 1.1, 1.2, 1.3_
  - [ ] 1.4 Qualifier les capacités d'extension de Comptoir (encart, liste, file de validation, lecture des dossiers ouverts, historique) et le service d'envoi des e-mails transactionnels
    - Livrable : note de choix d'intégration
    - _Exigences : 4.1, 5.4, 7.2, 6.3_
  - [ ] 1.5 Constituer un jeu de données synthétique : 210 000 colis, 3 transporteurs, E1 à E3, commandes multi-colis, dates promises absentes, cas aux bornes J à J+2, dossiers ouverts (CT-04)
    - _Exigences : 11.8_
  - [ ] 1.6 Définir avec la logistique et le service client le découpage en régions, la définition d'un dossier ouvert et les valeurs initiales des paramètres
    - Livrable : fiche de paramétrage initial ; points remontés à l'analyste (section « Points à ajouter à l'analyse »)
    - _Exigences : 3.1, 2.5, 7.1_

- [ ] 2. Référentiel de suivi et collecte des statuts (dépend de 1.3)
  - [ ] 2.1 Créer le schéma du référentiel (Colis, ÉvénementStatut, FraîcheurFlux, Paramètre, Journal) et ses index par commande, transporteur, entrepôt, région et niveau
    - _Exigences : 1.2_
  - [ ] 2.2 Développer le collecteur : consommation du flux Passerelle, normalisation des codes des 3 transporteurs, conservation du code d'origine, gestion des codes inconnus
    - _Exigences : 1.1, 1.3, 1.5_
  - [ ] 2.3 Implémenter le dédoublonnage par clé (colis, code normalisé, horodatage d'origine)
    - _Exigences : 1.4_
  - [ ] 2.4 Rattacher chaque colis à sa commande, son entrepôt, sa région de livraison et sa date promise
    - _Exigences : 1.2_
  - [ ] 2.5 Intégrer les statuts au fil de l'eau et calculer chaque jour la médiane et le 95e centile du délai de réception par transporteur
    - _Exigences : 1.6, 1.7_
  - [ ] 2.6 Mettre en place la supervision de la fraîcheur des flux et l'alerte d'interruption au-delà du seuil paramétré
    - _Exigences : 1.8_
  - [ ] 2.7 Écrire les tests unitaires et d'intégration du collecteur : doublons, codes inconnus, 3 transporteurs, interruption de flux
    - _Exigences : 1.1, 1.3, 1.4, 1.5, 1.8_

- [ ] 3. Moteur de retards (dépend de 2.1)
  - [ ] 3.1 Calculer le niveau d'un colis à chaque nouveau statut : `à l'heure`, `à surveiller` à J+1, `en retard` à J+2, sortie du suivi à la livraison
    - _Exigences : 2.1, 2.2, 2.3, 2.4_
  - [ ] 3.2 Lire les seuils dans les paramètres et exposer leur modification dans un écran d'administration minimal
    - _Exigences : 2.5_
  - [ ] 3.3 Planifier le recalcul matinal de tous les colis non livrés, terminé avant l'heure de publication de la liste
    - _Exigences : 2.6_
  - [ ] 3.4 Exclure du calcul et compter à part les colis sans date promise
    - _Exigences : 2.7_
  - [ ] 3.5 Publier l'événement `NiveauModifié` à chaque changement de niveau
    - _Exigences : 2.1_
  - [ ] 3.6 Écrire les tests aux bornes : J, J+1, J+2, livré, date promise absente, modification d'un seuil, recalcul matinal
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [ ] 4. API de suivi et tableau de bord (dépend de 3.1)
  - [ ] 4.1 Développer l'API de suivi en lecture (agrégats, listes, détail d'un colis), avec authentification, rôles et journalisation des accès
    - _Exigences : 3.5, 11.4_
  - [ ] 4.2 Développer l'écran des ventilations par transporteur, entrepôt et région
    - _Exigences : 3.1_
  - [ ] 4.3 Développer les listes et le détail d'un colis (commande, historique, date promise, nouvelle date)
    - _Exigences : 3.2_
  - [ ] 4.4 Appliquer le rouge au niveau prioritaire paramétré et le tri par ancienneté du retard décroissante
    - _Exigences : 3.3_
  - [ ] 4.5 Afficher la dernière mise à jour par transporteur et le bandeau d'interruption de flux
    - _Exigences : 3.4, 1.8_
  - [ ] 4.6 Tester la charge du lot 1 : 100 statuts / s pendant 1 h, rafale de 420 000 statuts, 210 000 colis en base
    - _Exigences : 1.6, 11.1_
  - [ ] 4.7 Faire la recette métier avec la logistique sur une journée de données synthétiques rejouée
    - _Exigences : 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 5. Mise en service du lot 1 (dépend de 4 et de la réponse à Q03 pour la date)
  - [ ] 5.1 Livrer l'interrupteur global des envois clients, désactivé, et vérifier qu'aucun envoi n'est possible
    - _Exigences : 11.7_
  - [ ] 5.2 Déployer dans le cloud d'Orvanne (UE) et ouvrir les accès aux équipes transport et aux responsables d'entrepôt
    - _Exigences : 11.2, 3.5_

- [ ] 6. Intégration Comptoir (lot 2, dépend de 1.4 et 4.1)
  - [ ] 6.1 Ajouter l'encart de suivi des colis dans la fiche commande : dernier statut, horodatage, niveau, historique, pour les 3 transporteurs
    - _Exigences : 4.1, 4.3_
  - [ ] 6.2 Limiter l'attente côté Comptoir et afficher le mode dégradé « suivi momentanément indisponible »
    - _Exigences : 4.2, 4.4_
  - [ ] 6.3 Produire la liste quotidienne à l'heure paramétrée et la rendre consultable dans Comptoir
    - _Exigences : 5.1, 5.3, 5.4_
  - [ ] 6.4 Afficher l'historique des messages de retard dans la fiche commande
    - _Exigences : 6.7_

- [ ] 7. Back-office des modèles et des paramètres (lot 2, dépend de 1.1 et 3.2)
  - [ ] 7.1 Gérer les modèles par canal et par cas (avec ou sans date) : création, prévisualisation sur données synthétiques, activation, historique des versions
    - _Exigences : 9.1, 9.4, 9.5_
  - [ ] 7.2 Restreindre les variables à la liste fermée validée par la DPO et contrôler les termes commerciaux à l'activation
    - _Exigences : 9.2, 9.3_
  - [ ] 7.3 Ajouter les paramètres du lot 2 : niveau d'alerte client, heure de publication, nombre de tentatives, durée de conservation
    - _Exigences : 6.2, 11.3_
  - [ ] 7.4 Écrire les tests du contrôle des variables et des termes commerciaux
    - _Exigences : 9.2, 9.3_

- [ ] 8. Service de notification par e-mail (lot 2, dépend de 3.5, 6.3 et 7.1)
  - [ ] 8.1 Consommer `NiveauModifié`, programmer le message quand le niveau d'alerte est atteint, regrouper les colis, garantir un seul message par commande
    - _Exigences : 6.1, 6.4_
  - [ ] 8.2 N'autoriser les envois du jour qu'après publication de la liste quotidienne
    - _Exigences : 5.2_
  - [ ] 8.3 Vérifier l'absence de dossier ouvert dans Comptoir au moment de l'envoi ; reporter l'envoi si Comptoir ne répond pas
    - _Exigences : 7.1, 7.2, 7.3_
  - [ ] 8.4 Construire le message avec ou sans nouvelle date, lire l'e-mail dans Vitrine et envoyer par e-mail
    - _Exigences : 6.3, 6.5, 6.6_
  - [ ] 8.5 Gérer les erreurs d'envoi (tentatives puis « erreur technique ») et les coordonnées absentes ou invalides
    - _Exigences : 6.8, 6.9_
  - [ ] 8.6 Annuler les messages programmés ou en attente quand la commande est livrée
    - _Exigences : 6.10_
  - [ ] 8.7 Journaliser chaque message (date, canal, version, contenu, état, motif) et l'inscrire dans l'historique de la commande
    - _Exigences : 6.7, 11.4_
  - [ ] 8.8 Écrire les tests unitaires des règles d'envoi : niveau d'alerte, un message par commande, publication préalable, dossier ouvert, Comptoir indisponible, erreurs, coordonnées, livraison avant envoi
    - _Exigences : 5.2, 6.1, 6.2, 6.4, 6.8, 6.9, 6.10, 7.1, 7.2, 7.3_

- [ ] 9. Indicateurs, conservation, droits et recette du lot 2 (dépend de 6, 7 et 8)
  - [ ] 9.1 Produire et exporter les indicateurs quotidiens des messages par état et par motif
    - _Exigences : 11.5_
  - [ ] 9.2 Implémenter la purge automatique selon la durée de conservation paramétrée
    - _Exigences : 11.3_
  - [ ] 9.3 Implémenter l'extraction et la suppression des messages d'un client, et déclarer ce stockage au projet P05
    - _Exigences : 11.6_
  - [ ] 9.4 Tester la charge et la résilience de bout en bout : pic, coupure de Comptoir, coupure du service d'envoi
    - _Exigences : 4.2, 4.4, 7.3, 11.1_
  - [ ] 9.5 Faire la recette métier avec le service client : encart Comptoir, liste quotidienne, messages reçus, modèles relus par la DPO
    - _Exigences : 4.1, 5.1, 5.3, 6.1, 6.5, 6.6, 9.1_
  - [ ] 9.6 Mettre en service après le 11 janvier, canal e-mail seul, puis activer l'interrupteur des envois
    - _Exigences : 6.3, 11.2, 11.7_

- [ ] 10. Validation des messages Premium (lot 3, dépend de 8 et de la réponse à Q04)
  - [ ] 10.1 Paramétrer la règle d'identification des clients Premium et verrouiller l'option tant qu'elle est absente
    - _Exigences : 8.2_
  - [ ] 10.2 Déposer les messages Premium dans la file de validation de Comptoir
    - _Exigences : 8.1_
  - [ ] 10.3 Traiter la validation (nouvelle vérification du dossier ouvert puis envoi) et le rejet motivé, avec journalisation du conseiller
    - _Exigences : 8.3, 8.4, 8.6_
  - [ ] 10.4 Appliquer l'action d'expiration paramétrée et signaler le message au responsable du service client
    - _Exigences : 8.5_
  - [ ] 10.5 Écrire les tests et faire la recette de la file Premium avec le service client
    - _Exigences : 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [ ] 11. Canal SMS (lot 3, dépend de 8, de l'avis de la DPO sur le mobile et de la réponse à Q01)
  - [ ] 11.1 Ajouter le paramètre de canal (e-mail seul, SMS avec repli sur l'e-mail)
    - _Exigences : 10.1_
  - [ ] 11.2 Verrouiller l'activation du SMS tant que l'avis favorable de la DPO n'est pas enregistré
    - _Exigences : 10.3_
  - [ ] 11.3 Lire le mobile dans Vitrine au moment de l'envoi, envoyer par SMS, sinon par e-mail
    - _Exigences : 10.2_
  - [ ] 11.4 Contrôler la longueur des modèles SMS à l'activation
    - _Exigences : 10.4_
  - [ ] 11.5 Écrire les tests du canal SMS : verrou, repli sur l'e-mail, longueur
    - _Exigences : 10.1, 10.2, 10.3, 10.4_
