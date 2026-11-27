# Plan d'implémentation : évolutions de l'espace vendeur de la marketplace

Le plan suit les trois lots de `requirements.md`. Aucune mise en production n'a lieu pendant le gel du 16 novembre au 11 janvier (CT-07). Le développement peut se poursuivre pendant le gel.

- **Lot 1a** (tâches 1 à 6) : taux de retard, alerte au vendeur, modification encadrée de l'IBAN. Mise en production au plus tôt le 12 janvier 2027, pour l'échéance de MKP-08 du 15/01/2027.
- **Lot 1b** (tâches 7 et 8) : vue des ventes, factures de commission, alerte aux chargés de compte. Mise en production au T1 2027, après les correctifs de P08 (MKP-03 : « fin mars »).
- **Lot 2** (tâches 9 à 13) : reversements, questions des clients, ouverture européenne, mobile. S1 et T2 2027.

- [ ] 1. Prérequis et cadrage (aucune dépendance ; tâches parallélisables)
  - [ ] 1.1 Soumettre à la DPO les traitements de P07 : coordonnées bancaires des vendeurs personnes physiques, échanges vendeur-client et données du client visibles par le vendeur, journal, durées de conservation (CT-01, Q36)
    - Livrable : avis écrit de la DPO, liste des données du client autorisées, durées de conservation
    - _Exigences : 9.5, 9.6, 9.7_
  - [ ] 1.2 Identifier avec la DSI le système qui porte l'espace vendeur, la source des données de ventes et d'expédition, le système de reversement, le rattachement vendeur - chargé de compte et les volumes réels, pic compris (Q-P07-2, Q-P07-8)
    - Livrable : contrats d'interface et fiche de volumétrie remplaçant les valeurs de travail de `design.md`
    - _Exigences : 1.4, 3.3, 5.3, 7.4_
  - [ ] 1.3 Obtenir de la direction marketplace la définition du retard d'expédition (Q26) et de la finance les règles d'attribution du rôle de valideur (Q25)
    - Livrable : définition validée, prête à saisir comme version 1 de `DéfinitionRetard` ; liste des rôles de valideur
    - _Exigences : 3.1, 7.3_
  - [ ] 1.4 Fixer avec la comptabilité le mode de dépôt des factures PDF, leur nommage et la profondeur d'historique (Q-P07-5)
    - Livrable : contrat de dépôt des factures
    - _Exigences : 2.1_
  - [ ] 1.5 Constituer un jeu de données synthétique : 10 000 vendeurs dont un à 100 000 lignes sur 30 jours, cas aux bornes des seuils, IBAN de test fictifs français, allemands et espagnols, factures PDF de test (CT-04)
    - _Exigences : 12.5_
  - [ ] 1.6 Faire confirmer par le comité d'architecture l'hébergement (Q34) et l'application du RGAA à l'espace vendeur (Q35)
    - _Exigences : 12.2, 11.3_

- [ ] 2. Socle commun (dépend de 1.2)
  - [ ] 2.1 Mettre en place le cloisonnement par vendeur dans toutes les nouvelles API : identifiant du vendeur lu dans le jeton de session
    - _Exigences : 12.1_
  - [ ] 2.2 Créer le journal d'audit (écriture seule) : actions pour le compte d'un vendeur, modifications de paramètres avec ancienne et nouvelle valeur
    - _Exigences : 12.3, 12.6_
  - [ ] 2.3 Créer le catalogue de textes externalisés, renseigner le français et implémenter le repli sur le français
    - _Exigences : 10.1, 10.2, 10.4_
  - [ ] 2.4 Écrire les tests d'accès croisé entre vendeurs et les tests du journal
    - _Exigences : 12.1, 12.3_

- [ ] 3. Moteur de taux de retard, lot 1a (dépend de 1.3 et 2.2)
  - [ ] 3.1 Créer les entités `DéfinitionRetard` (versionnée) et `RègleAlerte`, leur écran d'administration dans le back-office, et le refus d'activation des règles sans définition validée
    - _Exigences : 3.1, 3.4, 3.6, 12.6_
  - [ ] 3.2 Implémenter le calcul du taux par vendeur sur la fenêtre de chaque règle (7 jours, 30 jours glissants) et l'enregistrement de `CalculTaux` (compteurs, version de la définition, commandes exclues)
    - _Exigences : 3.1, 3.2, 3.5_
  - [ ] 3.3 Ordonnancer le calcul à la fréquence paramétrée, avec reprise après interruption et sans alerte sur un calcul partiel
    - _Exigences : 3.3_
  - [ ] 3.4 Écrire les tests aux bornes : fenêtres, définition absente, changement de version, commandes sans date d'expédition
    - _Exigences : 3.1, 3.2, 3.5, 3.6_

- [ ] 4. Alerte au vendeur, lot 1a (dépend de 3.2 et 2.3)
  - [ ] 4.1 Implémenter la règle « vendeur » (strictement plus de 5 % sur 7 jours), l'événement `SeuilFranchi` et le contenu de l'alerte (taux, seuil, fenêtre, nombre et liste des commandes en retard)
    - _Exigences : 4.1, 4.3_
  - [ ] 4.2 Afficher l'alerte dans l'espace vendeur et l'envoyer par e-mail selon les canaux paramétrés, avec 3 nouvelles tentatives en cas d'échec
    - _Exigences : 4.2_
  - [ ] 4.3 Rendre l'alerte du vendeur visible à son chargé de compte dans le back-office
    - _Exigences : 4.4_
  - [ ] 4.4 Écrire les tests : 5,00 % sans alerte, 5,01 % avec alerte, échec d'envoi de l'e-mail, contenu de l'alerte
    - _Exigences : 4.1, 4.2, 4.3_

- [ ] 5. Modification de l'IBAN avec double validation, lot 1a (dépend de 1.3 et 2.2)
  - [ ] 5.1 Développer l'écran de saisie du nouvel IBAN et le contrôle de structure et de clé
    - _Exigences : 6.1, 6.2_
  - [ ] 5.2 Gérer le cycle de vie de la demande côté vendeur : états affichés, IBAN en vigueur conservé pendant l'attente, information en cas de refus
    - _Exigences : 6.3, 6.4, 6.5_
  - [ ] 5.3 Développer la file de validation du back-office : deux valideurs distincts, contrôle du rôle, refus motivé qui clôt la demande
    - _Exigences : 7.1, 7.2, 7.3, 7.5_
  - [ ] 5.4 Transmettre l'IBAN validé au système de reversement, attendre l'accusé de prise en compte avant de changer l'IBAN en vigueur, informer le vendeur
    - _Exigences : 7.4_
  - [ ] 5.5 Chiffrer l'IBAN au repos, le masquer à l'affichage et journaliser chaque saisie, validation et refus sans IBAN en clair
    - _Exigences : 7.6_
  - [ ] 5.6 Écrire les tests de sécurité : même valideur deux fois, collaborateur sans rôle, refus, indisponibilité du système de reversement, absence d'IBAN en clair dans les journaux
    - _Exigences : 7.1, 7.2, 7.3, 7.4, 7.6_

- [ ] 6. Recette et mise en service du lot 1a (dépend de 1.1, 4 et 5)
  - [ ] 6.1 Tester la charge du calcul des taux sur le jeu synthétique et mesurer les temps de réponse des nouveaux écrans par rapport au seuil de P08
    - _Exigences : 3.3, 12.4_
  - [ ] 6.2 Faire la recette métier avec la finance (double validation) et les chargés de compte (alertes vendeur), sur données synthétiques
    - _Exigences : 4.1, 4.2, 4.3, 4.4, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 12.5_
  - [ ] 6.3 Mettre en production dans l'UE au plus tôt le 12 janvier 2027
    - _Exigences : 12.2_

- [ ] 7. Vue des ventes et factures de commission, lot 1b (dépend de 2.1, de 1.4 et de la livraison des correctifs de P08)
  - [ ] 7.1 Développer le service ventes : agrégats précalculés du jour, de la semaine et du mois en cours, sur la source de l'export, avec l'horodatage de mise à jour
    - _Exigences : 1.1, 1.3_
  - [ ] 7.2 Développer l'écran du tableau de bord avec les trois périodes sur le même écran
    - _Exigences : 1.2_
  - [ ] 7.3 Mettre en place le test de cohérence quotidien entre le tableau de bord et l'export des ventes
    - _Exigences : 1.4_
  - [ ] 7.4 Développer la réception des factures PDF : rattachement au vendeur, empreinte, refus des fichiers orphelins ou illisibles et signalement à la comptabilité
    - _Exigences : 2.1, 2.3, 2.4_
  - [ ] 7.5 Développer la liste des factures par mois et le téléchargement du fichier d'origine
    - _Exigences : 2.2, 2.3_
  - [ ] 7.6 Écrire les tests : bornes des périodes (minuit, lundi, 1er du mois), facture orpheline, fichier non PDF, identité du fichier téléchargé
    - _Exigences : 1.1, 2.1, 2.3, 2.4_

- [ ] 8. Alerte aux chargés de compte et mise en service du lot 1b (dépend de 3 et 7)
  - [ ] 8.1 Implémenter la règle « chargés de compte » (strictement plus de 2 % sur 30 jours glissants) et le destinataire de repli
    - _Exigences : 5.1, 5.3_
  - [ ] 8.2 Développer dans le back-office la liste des vendeurs en alerte, triée par taux décroissant
    - _Exigences : 5.2_
  - [ ] 8.3 Écrire les tests : 2,00 % sans alerte, 2,01 % avec alerte, vendeur sans chargé de compte
    - _Exigences : 5.1, 5.3_
  - [ ] 8.4 Faire la recette métier avec des vendeurs pilotes, les chargés de compte et la comptabilité, puis mettre en production au T1 2027
    - _Exigences : 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 5.1, 5.2, 12.4_

- [ ] 9. Détail des reversements, lot 2 (dépend de 1.2, 7.5 et de la réponse à Q-P07-4)
  - [ ] 9.1 Développer le connecteur de lecture des reversements et de leurs lignes dans le système de la finance
    - _Exigences : 8.1, 8.2_
  - [ ] 9.2 Afficher les libellés explicatifs des lignes et le lien vers la facture de commission
    - _Exigences : 8.3_
  - [ ] 9.3 Implémenter le contrôle de somme, le masquage du détail en cas d'écart et le signalement à la finance
    - _Exigences : 8.4_
  - [ ] 9.4 Écrire les tests : reversement équilibré, écart de somme, ligne de commission sans facture
    - _Exigences : 8.2, 8.3, 8.4_

- [ ] 10. Réponses aux questions des clients, lot 2 (dépend de 1.1 et de la réponse à Q-P07-1)
  - [ ] 10.1 Développer l'interface commune et l'adaptateur du canal retenu (Comptoir ou messagerie dédiée) : réception des questions, envoi des réponses, nouvelles tentatives
    - _Exigences : 9.1, 9.2_
  - [ ] 10.2 Afficher l'historique de chaque échange au vendeur
    - _Exigences : 9.3_
  - [ ] 10.3 Si le canal Comptoir est retenu, rendre les échanges consultables par le service client dans Comptoir
    - _Exigences : 9.4_
  - [ ] 10.4 Filtrer les données du client selon la liste de la DPO et poser le verrou d'activation lié à son avis
    - _Exigences : 9.5, 9.6_
  - [ ] 10.5 Implémenter la purge des échanges selon la durée paramétrée et déclarer ce stockage au registre des droits (P05)
    - _Exigences : 9.7_
  - [ ] 10.6 Écrire les tests : transmission, canal indisponible, données client masquées, verrou, purge
    - _Exigences : 9.1, 9.2, 9.3, 9.5, 9.6, 9.7_

- [ ] 11. Ouverture aux vendeurs européens, lot 2 (dépend de 2.3, 5.1 et de la réponse à Q27)
  - [ ] 11.1 Permettre au vendeur de choisir sa langue parmi les langues activées et l'appliquer aux écrans, aux alertes et aux e-mails
    - _Exigences : 10.3_
  - [ ] 11.2 Créer le paramétrage des pays ouverts, avec l'Allemagne et l'Espagne activables
    - _Exigences : 10.5, 10.6_
  - [ ] 11.3 Étendre le contrôle de l'IBAN aux pays ouverts
    - _Exigences : 10.7_
  - [ ] 11.4 Écrire les tests : langue choisie, texte manquant, IBAN allemand et espagnol, IBAN d'un pays non ouvert
    - _Exigences : 10.3, 10.4, 10.7_

- [ ] 12. Tableau de bord sur mobile et accessibilité, lot 2 (dépend de 7.2, 4.2 et 1.6)
  - [ ] 12.1 Adapter le tableau de bord vendeur (ventes et alertes) au smartphone, sans défilement horizontal
    - _Exigences : 11.1, 11.2_
  - [ ] 12.2 Faire l'audit RGAA des écrans créés ou modifiés par P07 et corriger les écarts
    - _Exigences : 11.3_
  - [ ] 12.3 Écrire les tests sur smartphone : mêmes chiffres que sur ordinateur, largeur de 360 px
    - _Exigences : 11.1, 11.2_

- [ ] 13. Recette et mise en service du lot 2 (dépend de 9, 10, 11 et 12)
  - [ ] 13.1 Mesurer les temps de réponse des écrans du lot 2 par rapport au seuil de P08
    - _Exigences : 12.4_
  - [ ] 13.2 Faire la recette métier avec des vendeurs pilotes, dont des vendeurs allemands et espagnols, la finance et le service client, sur données synthétiques
    - _Exigences : 8.1, 8.2, 8.3, 9.1, 9.2, 9.3, 9.4, 10.3, 10.5, 10.6, 11.1, 12.5_
  - [ ] 13.3 Mettre en production dans l'UE, hors période de gel
    - _Exigences : 12.2_
