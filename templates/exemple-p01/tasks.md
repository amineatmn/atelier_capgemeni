# Plan d'implémentation : détection des retards de livraison, information du client et pilotage

Les tâches 1 à 5 forment le **lot 1** : outils internes, sans envoi aux clients, avec une mise en service possible avant le pic selon la réponse à Q03. Les tâches 6 à 9 forment le **lot 2** : Comptoir et messages, au T1 2027, après le gel des mises en production.

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre l'analyse du traitement à la DPO : base légale du message de service, durée de conservation (H10), usage éventuel du mobile (CT-02)
    - Livrable : avis écrit de la DPO, versé au dossier du projet
    - _Exigences : 9.3, 9.4_
  - [ ] 1.2 Vérifier avec l'équipe Passerelle les flux des 3 transporteurs (continu ou fichier du matin), leur format et la disponibilité de la date promise par colis (Q06, Q08)
    - Livrable : contrat d'interface du flux de statuts et des commandes
    - _Exigences : 1.1, 1.3, 2.1_
  - [ ] 1.3 Qualifier les possibilités d'extension de Comptoir (encart, file, liste) et le service d'envoi des e-mails transactionnels (Q07, Q09)
    - Livrable : note de choix d'intégration
    - _Exigences : 4.1, 6.2_
  - [ ] 1.4 Constituer un jeu de données synthétique : 210 000 colis, 3 transporteurs, 3 entrepôts, cas aux bornes (CT-04)
    - _Exigences : 9.1_

- [ ] 2. Référentiel de suivi et collecte des statuts (dépend de 1.2)
  - [ ] 2.1 Créer le schéma du référentiel (Colis, ÉvénementStatut, Paramètre, Journal) et ses index par commande, transporteur, entrepôt, département et niveau
    - _Exigences : 1.2, 9.4_
  - [ ] 2.2 Développer le collecteur : consommation du flux Passerelle, normalisation des codes de statut des 3 transporteurs, conservation du code d'origine, gestion des codes inconnus
    - _Exigences : 1.1, 1.3_
  - [ ] 2.3 Implémenter le dédoublonnage par clé (colis, code, horodatage transporteur)
    - _Exigences : 1.5_
  - [ ] 2.4 Rattacher chaque colis à sa commande, à son entrepôt, à son département de livraison et à sa date promise
    - _Exigences : 1.2_
  - [ ] 2.5 Mettre en place la supervision : fraîcheur des flux par transporteur, alerte au-delà de 4 h, délai de bout en bout de 15 min au plus
    - _Exigences : 1.4, 1.6_
  - [ ] 2.6 Écrire les tests unitaires et d'intégration du collecteur (doublons, codes inconnus, 3 transporteurs)
    - _Exigences : 1.1, 1.3, 1.5_

- [ ] 3. Moteur de retards (dépend de 2.1)
  - [ ] 3.1 Calculer le niveau de retard d'un colis à chaque nouveau statut : `à l'heure`, `à surveiller` après la date promise, `en retard` à 48 h, sortie du suivi à la livraison
    - _Exigences : 2.1, 2.2, 2.3, 2.4_
  - [ ] 3.2 Lire les deux seuils dans la table des paramètres et exposer leur modification dans un écran d'administration minimal
    - _Exigences : 2.5_
  - [ ] 3.3 Lancer le recalcul quotidien de tous les colis non livrés à 5 h 30, terminé avant 6 h 00
    - _Exigences : 2.6_
  - [ ] 3.4 Publier l'événement `NiveauModifié` à chaque changement de niveau
    - _Exigences : 2.1_
  - [ ] 3.5 Écrire les tests aux bornes : veille, jour J, J+1, J+2, livré, date promise absente, modification d'un seuil
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ] 4. API de suivi et tableau de bord (dépend de 3.1)
  - [ ] 4.1 Développer l'API de suivi en lecture (agrégats, listes, détail d'un colis), avec authentification SSO, rôles et journalisation des accès
    - _Exigences : 3.1, 3.2, 3.5, 9.5_
  - [ ] 4.2 Développer l'écran des ventilations par transporteur, entrepôt et région
    - _Exigences : 3.1_
  - [ ] 4.3 Développer les listes et le détail d'un colis, avec le code couleur et le tri (`en retard` en premier, par ancienneté décroissante)
    - _Exigences : 3.2, 3.3_
  - [ ] 4.4 Afficher la date de dernière mise à jour et le bandeau d'interruption de flux
    - _Exigences : 3.4, 1.6_
  - [ ] 4.5 Ajouter l'export CSV de la liste affichée
    - _Exigences : 3.6_
  - [ ] 4.6 Tester la charge du lot 1 : 100 statuts / s pendant 1 h, avec 210 000 colis en base
    - _Exigences : 1.4, 9.1_
  - [ ] 4.7 Faire la recette métier avec la logistique, sur une journée de données synthétiques rejouée
    - _Exigences : 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 5. Mise en service du lot 1 (dépend de 4, et de la réponse à Q03 pour la date)
  - [ ] 5.1 Déployer dans le cloud d'Orvanne (UE) et ouvrir les accès aux équipes transport, aux responsables d'entrepôt et au service client
    - _Exigences : 9.2, 3.5_

- [ ] 6. Intégration Comptoir (lot 2, dépend de 1.3 et 4.1)
  - [ ] 6.1 Ajouter l'encart de suivi des colis dans la fiche commande : dernier statut, horodatage, niveau, historique
    - _Exigences : 4.1, 4.3_
  - [ ] 6.2 Limiter l'attente à 1,5 s côté Comptoir et prévoir le mode dégradé « suivi momentanément indisponible »
    - _Exigences : 4.2, 4.4_
  - [ ] 6.3 Produire la liste quotidienne de 7 h 00, consultable dans Comptoir et exportable en CSV
    - _Exigences : 5.1, 5.2, 5.3_
  - [ ] 6.4 Afficher l'historique des messages de retard dans la commande
    - _Exigences : 6.8_

- [ ] 7. Back-office des modèles et des paramètres (lot 2, dépend de 3.2)
  - [ ] 7.1 Gérer les modèles par canal et par cas (avec ou sans date) : création, prévisualisation, activation, historique des versions
    - _Exigences : 8.1, 8.4_
  - [ ] 7.2 Restreindre les variables aux variables de service et contrôler les termes commerciaux à l'activation
    - _Exigences : 8.2, 8.3_
  - [ ] 7.3 Vérifier la longueur d'un SMS (160 caractères au plus, variables remplacées)
    - _Exigences : 8.5_
  - [ ] 7.4 Ajouter les paramètres : canal, niveau qui déclenche l'alerte, plage horaire, délai de validation Premium, durée de conservation, verrou du SMS tant que l'avis de la DPO n'est pas enregistré
    - _Exigences : 6.2, 6.3, 9.3, 9.4_
  - [ ] 7.5 Écrire les tests du contrôle anti-commercial et du verrou SMS
    - _Exigences : 8.3, 9.3_

- [ ] 8. Service de notification (lot 2, dépend de 3.4, 6.1 et 7.1)
  - [ ] 8.1 Consommer `NiveauModifié`, appliquer le niveau qui déclenche l'alerte, regrouper les colis par commande, garantir un seul message par commande et par niveau
    - _Exigences : 6.1, 6.6_
  - [ ] 8.2 Programmer les envois dans la plage de 8 h 00 à 20 h 00
    - _Exigences : 6.7_
  - [ ] 8.3 Vérifier l'absence de dossier ouvert dans Comptoir au moment de l'envoi ; reporter l'envoi si Comptoir est indisponible
    - _Exigences : 7.1, 7.2_
  - [ ] 8.4 Gérer la file de validation Premium : dépôt, validation avec nouvelle vérification, rejet motivé, expiration signalée au responsable
    - _Exigences : 7.3, 7.4, 7.5_
  - [ ] 8.5 Annuler les messages programmés ou en validation quand la commande est livrée
    - _Exigences : 7.6_
  - [ ] 8.6 Construire le message (avec ou sans nouvelle date), lire l'e-mail dans Vitrine, envoyer, et réessayer en cas d'erreur
    - _Exigences : 6.2, 6.4, 6.5_
  - [ ] 8.7 Implémenter le canal SMS derrière son option, désactivé par défaut
    - _Exigences : 6.3_
  - [ ] 8.8 Journaliser chaque message (date, canal, version du modèle, contenu, statut, motif) et les actions des conseillers
    - _Exigences : 6.8, 9.5_
  - [ ] 8.9 Écrire les tests unitaires des règles d'envoi : seuil, doublon, plage horaire, dossier ouvert, Premium, livraison avant envoi
    - _Exigences : 6.1, 6.6, 6.7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ] 9. Indicateurs, conservation et recette du lot 2 (dépend de 6, 7 et 8)
  - [ ] 9.1 Produire les indicateurs quotidiens des messages : envoyés, non envoyés à cause d'un dossier ouvert, validés, rejetés, expirés
    - _Exigences : 9.6_
  - [ ] 9.2 Implémenter la purge automatique selon la durée de conservation paramétrée
    - _Exigences : 9.4_
  - [ ] 9.3 Tester la charge et la résilience de bout en bout : pic, coupure de Comptoir, coupure du service d'envoi
    - _Exigences : 4.2, 4.4, 9.1_
  - [ ] 9.4 Faire la recette métier avec le service client : liste quotidienne, file Premium, modèles relus par la DPO
    - _Exigences : 5.1, 5.2, 7.3, 7.4, 8.1, 8.2_
  - [ ] 9.5 Mettre en service après le 11 janvier, avec le canal e-mail seul
    - _Exigences : 6.2, 9.2_
