# Plan d'implémentation : déclaration de casse à la douchette, blocage du stock dans Hangar et litiges transporteurs

Les tâches 1 à 8 forment le **lot 1** : déclaration de casse sur E2. Le développement peut avancer pendant le gel, mais la mise en service (tâche 8.3) a lieu au plus tôt le 12 janvier 2027, après l'avis de la DPO (CT-07, H16). Les tâches 9 à 11 forment le **lot 2** : téléphones des chefs d'équipe et note A / B / C des retours. Elles dépendent du portail de retours (P02) et des réponses à Q16 et Q37.

- [ ] 1. Prérequis et cadrage (aucune dépendance, sous-tâches parallélisables)
  - [ ] 1.1 Soumettre le traitement à la DPO : photos (CT-06), identifiant des déclarants, durées de conservation, accès, usage futur des téléphones (Q36)
    - Livrable : avis écrit de la DPO, versé au dossier du projet, et durées de conservation à saisir dans le back-office
    - _Exigences : 1.8, 10.1, 10.2, 10.4_
  - [ ] 1.2 Inventorier le parc de douchettes de E2 (modèles, système, mémoire, appareil photo, possibilité d'installer une application) et relever la couverture réseau des allées, zone C comprise
    - Livrable : note de choix de la technologie du terminal (application native ou web installable)
    - _Exigences : 1.7, 2.1, 2.3_
  - [ ] 1.3 Établir avec l'équipe Hangar le contrat d'interface : nature du code scanné, consultation par identifiant (articles, quantités, emplacement, transporteur, date de réception), demande de blocage, granularité possible, confirmation
    - Livrable : contrat d'interface validé par la DSI
    - _Exigences : 3.3, 5.1, 5.2, 5.3, 6.2, 6.5_
  - [ ] 1.4 Recueillir auprès de l'exploitation E2 et du transport la liste initiale des types de dégât, les destinataires des notifications, le délai contractuel par transporteur et son point de départ (Q29)
    - Livrable : fichier de paramétrage initial de E2
    - _Exigences : 1.4, 4.3, 6.1, 6.3_
  - [ ] 1.5 Constituer un jeu de données synthétique : identifiants et articles Hangar fictifs, 3 transporteurs, cas aux bornes, photos fabriquées sans étiquette réelle (CT-04)
    - _Exigences : 10.7_

- [ ] 2. Socle serveur (dépend de 1.3)
  - [ ] 2.1 Créer le schéma (DossierCasse, Déclaration, Photo, TypeDégât, Paramètre, Notification, Journal) et ses index par site, identifiant, statut et date limite
    - _Exigences : 3.1, 3.5_
  - [ ] 2.2 Développer l'API de déclaration : réception idempotente par identifiant de déclaration, envoi des photos par morceaux, stockage chiffré des photos, accusé de réception
    - _Exigences : 2.6, 3.1, 10.5_
  - [ ] 2.3 Rattacher une déclaration au dossier non clos existant pour le même identifiant et le même site
    - _Exigences : 3.2_
  - [ ] 2.4 Brancher l'authentification interne, les rôles limités au site, et le refus des déclarations des sites non activés
    - _Exigences : 7.4, 10.2_
  - [ ] 2.5 Écrire les tests unitaires et d'intégration du socle : doublons, rattachement, rôles, site non activé
    - _Exigences : 2.6, 3.2, 7.4, 10.2_

- [ ] 3. Application de déclaration sur douchette (dépend de 1.2 et 2.2)
  - [ ] 3.1 Développer l'écran de déclaration : scan, pré-remplissage (site, terminal, utilisateur, horodatage), saisie manuelle de secours
    - _Exigences : 1.1, 1.2_
  - [ ] 3.2 Imposer le type de dégât et conserver localement la dernière liste reçue
    - _Exigences : 1.3, 2.2_
  - [ ] 3.3 Gérer les photos selon le terminal : de 0 à 2, masquées sans appareil photo, verrouillées tant que l'avis de la DPO n'est pas enregistré, validation possible sans photo
    - _Exigences : 1.5, 1.6, 1.7, 1.8_
  - [ ] 3.4 Développer la file locale chiffrée : capacité de 80 déclarations avec 2 photos, persistance au redémarrage, accusé « transmise » ou « en attente », compteur permanent
    - _Exigences : 1.9, 2.1, 2.3, 2.7, 10.5_
  - [ ] 3.5 Développer l'agent de synchronisation : envoi automatique au retour du réseau, ordre de saisie, horodatage du terminal conservé, reprise avec le même identifiant
    - _Exigences : 2.4, 2.5, 2.6_
  - [ ] 3.6 Effacer la déclaration et ses photos après l'accusé, interdire la galerie, afficher que le stock n'est pas encore bloqué quand la déclaration est validée hors réseau
    - _Exigences : 2.8, 2.9, 5.6_
  - [ ] 3.7 Tester sur chaque modèle de douchette de E2 et hors réseau en conditions réelles : 80 déclarations, redémarrage forcé, batterie retirée, retour du réseau
    - _Exigences : 1.7, 2.1, 2.3, 2.4, 2.5, 2.8, 2.9_

- [ ] 4. Dossiers, Hangar et notifications (dépend de 2.1 et 1.3)
  - [ ] 4.1 Créer automatiquement le dossier, le compléter avec les données de Hangar et passer en « à vérifier » si l'identifiant est inconnu
    - _Exigences : 3.1, 3.3, 3.4_
  - [ ] 4.2 Développer le connecteur Hangar pour le blocage : demande, granularité paramétrée (totalité par défaut), enregistrement de la confirmation, nouvelles tentatives, alerte à l'issue du délai paramétré
    - _Exigences : 5.1, 5.2, 5.3, 5.4_
  - [ ] 4.3 Développer le service de notification : destinataires par site, contenu (identifiant, type, date, nombre de photos, date limite, lien), aucune photo jointe, statut « non notifié » après échec
    - _Exigences : 4.1, 4.2, 4.4, 4.5_
  - [ ] 4.4 Tester l'intégration avec Hangar en recette (consultation, blocage, refus, indisponibilité) et le service de notification avec des bouchons
    - _Exigences : 3.3, 3.4, 4.5, 5.1, 5.3, 5.4_

- [ ] 5. Écran de suivi et litiges transporteurs (dépend de 4.1)
  - [ ] 5.1 Développer l'écran web de suivi : liste et détail des dossiers avec photos, statuts, clôture, correction de l'identifiant d'un dossier « à vérifier » avec historique
    - _Exigences : 3.5, 3.6, 3.7_
  - [ ] 5.2 Calculer la date limite : délai par transporteur (7 jours par défaut), point de départ paramétré, affichage des jours restants dans le dossier, la notification et l'écran
    - _Exigences : 6.1, 6.2, 6.3, 6.4_
  - [ ] 5.3 Reprendre le transporteur depuis Hangar ou le faire saisir, et enregistrer la qualification « litige déclaré » ou « sans litige »
    - _Exigences : 6.5, 6.6_
  - [ ] 5.4 Envoyer l'alerte avant la date limite et trier les dossiers « ouverts » par date limite croissante
    - _Exigences : 6.7, 6.8_
  - [ ] 5.5 Afficher la liste des dossiers dont le blocage n'est pas confirmé
    - _Exigences : 5.5_
  - [ ] 5.6 Produire les indicateurs quotidiens par site et par transporteur : dossiers créés, litiges dans le délai, hors délai, échéance dépassée
    - _Exigences : 6.9_
  - [ ] 5.7 Écrire les tests aux bornes de la date limite : J-1, J, J+1, date de réception inconnue, transporteur inconnu, modification d'un paramètre
    - _Exigences : 6.1, 6.2, 6.3, 6.7_

- [ ] 6. Back-office et activation par site (dépend de 2.1)
  - [ ] 6.1 Développer le back-office : types de dégât, destinataires, délais, point de départ, délai d'alerte, granularité du blocage, avis de la DPO, durées de conservation, activation par site
    - _Exigences : 1.4, 1.8, 4.3, 5.2, 7.1, 7.3_
  - [ ] 6.2 Charger le paramétrage initial de E2 (tâche 1.4) et activer E2 seul
    - _Exigences : 7.2_
  - [ ] 6.3 Tester le paramétrage : modification sans mise en production, site désactivé, verrou des photos
    - _Exigences : 1.4, 1.8, 7.1, 7.4_

- [ ] 7. Sécurité, RGPD et exploitation (dépend de 2.1)
  - [ ] 7.1 Journaliser les créations, modifications et qualifications de dossiers, les consultations de photos et les modifications de paramètres
    - _Exigences : 10.3_
  - [ ] 7.2 Implémenter la purge automatique des photos puis des dossiers selon les durées paramétrées
    - _Exigences : 10.4_
  - [ ] 7.3 Configurer le chiffrement au repos et en transit et l'hébergement dans l'UE (cloud d'Orvanne selon la réponse à Q34)
    - _Exigences : 10.5, 10.6_
  - [ ] 7.4 Vérifier que les environnements hors production ne contiennent que les données synthétiques de la tâche 1.5
    - _Exigences : 10.7_
  - [ ] 7.5 Tester la charge : 60 terminaux synchronisés en même temps avec 10 déclarations et photos chacun, 160 déclarations par jour
    - _Exigences : 10.8_
  - [ ] 7.6 Tester la conformité : photos absentes de la galerie et des notifications, purge, verrou DPO, toutes les photos traitées comme données personnelles
    - _Exigences : 1.8, 2.9, 4.4, 10.1, 10.4_

- [ ] 8. Recette et mise en service du lot 1 (dépend de 3 à 7, et de 1.1 pour la mise en service)
  - [ ] 8.1 Faire la recette métier à E2 sur une semaine de cas rejoués : préparateurs, caristes, chefs d'équipe et transport, scénarios hors réseau, litige proche de sa date limite
    - _Exigences : 1.1, 1.3, 2.4, 3.1, 4.1, 5.1, 6.6, 6.7_
  - [ ] 8.2 Rédiger le mode opératoire pour E2 (déclaration, synchronisation, suivi) et former les chefs d'équipe
    - _Exigences : 1.9, 2.7, 5.6_
  - [ ] 8.3 Mettre en service sur E2 au plus tôt le 12 janvier 2027, après l'avis de la DPO ; conserver la fiche papier si l'inventaire de janvier a lieu avant (Q17)
    - _Exigences : 7.2, 10.6_

- [ ] 9. Lot 2 : téléphones des chefs d'équipe (dépend de 8 et de la réponse à Q16)
  - [ ] 9.1 Permettre à un chef d'équipe de retrouver un dossier par scan ou saisie et d'y ajouter jusqu'à 2 photos
    - _Exigences : 8.1_
  - [ ] 9.2 Permettre une déclaration de casse complète depuis le téléphone
    - _Exigences : 8.2_
  - [ ] 9.3 Réserver l'usage du téléphone au rôle chef d'équipe
    - _Exigences : 8.3_
  - [ ] 9.4 Appliquer sur le téléphone le fonctionnement hors réseau et les règles sur les photos, et le tester sur les téléphones retenus
    - _Exigences : 8.4_

- [ ] 10. Lot 2 : note A / B / C des retours abîmés (dépend de 8, de l'interface du portail de retours P02 et de la réponse à Q37)
  - [ ] 10.1 Établir avec l'équipe P02 le contrat d'interface de transmission de la note et le traitement des refus
    - _Exigences : 9.4, 9.7_
  - [ ] 10.2 Ajouter le mode « retour » sur le même écran : identification par scan, note A, B ou C obligatoire, 0 à 2 photos
    - _Exigences : 9.1, 9.2, 9.3_
  - [ ] 10.3 Transmettre la note au portail de retours sans aucun montant, et placer en anomalie les retours non reconnus
    - _Exigences : 9.4, 9.5, 9.7_
  - [ ] 10.4 Appliquer au mode « retour » la file locale et la synchronisation
    - _Exigences : 9.6_
  - [ ] 10.5 Tester le mode « retour » : note obligatoire, absence de montant, charge de 2 200 notes par jour
    - _Exigences : 9.2, 9.5, 9.8_

- [ ] 11. Recette et mise en service du lot 2 (dépend de 9 et 10)
  - [ ] 11.1 Faire la recette avec E2 et l'équipe du portail de retours : photos depuis un téléphone, contrôle qualité de retours rejoués, anomalies
    - _Exigences : 8.1, 8.2, 9.1, 9.2, 9.4, 9.7_
  - [ ] 11.2 Mettre en service le lot 2 hors période de gel, après mise à jour de l'avis de la DPO sur les téléphones et le transfert des photos au portail
    - _Exigences : 8.4, 9.6_
