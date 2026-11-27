# Plan d'implémentation : registre et traitement des demandes d'exercice de droits RGPD

Les tâches 1 à 9 forment le **lot 1** : registre, échéances, saisie par le service client, traçabilité manuelle des actions, export d'accès et tableau de bord. La mise en production a lieu au plus tôt le 12 janvier 2027, après le gel (`CT-07`), et avant le prochain contrôle interne si sa date le permet (`Q30`). Les tâches 10 et 11 forment le **lot 2** : orchestration des actions dans les systèmes (`H31`).

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre l'analyse du traitement du registre à la DPO : moyens de vérification de l'identité, durée de conservation des demandes, des pièces d'identité et du journal, mécanisme de remise de l'export, contenu du tableau de bord (CT-01)
    - Livrable : avis écrit de la DPO et valeurs initiales des paramètres de conservation
    - _Exigences : 1.6, 8.3, 8.7, 9.1, 11.4_
  - [ ] 1.2 Obtenir la date du prochain contrôle interne et la décision d'hébergement (Q30, Q34) ; caler la date de mise en production du lot 1 hors gel
    - Livrable : planning du lot 1 validé par la DPO et la DSI
    - _Exigences : 11.5_
  - [ ] 1.3 Analyser le classeur partagé actuel : colonnes, qualité des dates de réception, demandes non clôturées ; définir la correspondance avec le modèle du registre
    - Livrable : spécification de l'import
    - _Exigences : 1.8_
  - [ ] 1.4 Qualifier les possibilités d'extension de Comptoir (lien contextuel ou composant) et l'accès à l'authentification interne
    - Livrable : note de choix d'intégration
    - _Exigences : 5.5, 11.6_
  - [ ] 1.5 Constituer un jeu de données synthétique : 150 demandes couvrant les 4 types et les 4 canaux, prolongations, dépassements, demandes importées, extractions fictives par système ; copie anonymisée du classeur (CT-04)
    - _Exigences : 11.7_

- [ ] 2. Socle technique (dépend de 1.1 et 1.4)
  - [ ] 2.1 Créer le schéma du registre : Demande, Demandeur, VérificationIdentité, SystèmeCatalogue, SystèmeConcerné, Action, DonnéeIsolée, ObligationLégale, PièceJointe, Export, Paramètre, Journal
    - _Exigences : 1.1, 1.4, 1.5_
  - [ ] 2.2 Brancher l'authentification interne et définir les rôles `dpo`, `admin-dpo`, `service-client`, `comite-risques`, avec le contrôle d'accès sur chaque écran et chaque API
    - _Exigences : 11.2, 11.6, 5.4_
  - [ ] 2.3 Mettre en place le journal d'audit en ajout seul pour toutes les consultations et opérations
    - _Exigences : 11.1_
  - [ ] 2.4 Mettre en place le stockage chiffré des pièces, preuves et exports, et TLS sur tous les échanges ; déployer les environnements dans l'UE
    - _Exigences : 11.3, 11.5_
  - [ ] 2.5 Écrire les tests de sécurité du socle : rôles, journal non modifiable, chiffrement au repos
    - _Exigences : 11.1, 11.2, 11.3_

- [ ] 3. Registre, catalogue et saisie (dépend de 2.1 et 2.2)
  - [ ] 3.1 Développer la création et la fiche d'une demande : canal, date de réception, type, statuts horodatés, identifiant unique
    - _Exigences : 1.1, 1.2, 1.3, 1.4, 1.5_
  - [ ] 3.2 Développer la vérification d'identité : état, moyen paramétrable, auteur, date
    - _Exigences : 1.6_
  - [ ] 3.3 Développer la recherche multicritère et l'avertissement de doublon
    - _Exigences : 1.7, 1.9_
  - [ ] 3.4 Développer le catalogue des systèmes, initialisé avec Vitrine, Comptoir, Hangar, le Lac et l'outil d'e-mailing, et la proposition des systèmes concernés avec motif de retrait
    - _Exigences : 2.1, 2.2, 2.3_
  - [ ] 3.5 Développer l'écran de saisie du service client : message d'origine, date d'envoi du client, notification à l'équipe de la DPO, consultation limitée au statut et à l'échéance
    - _Exigences : 5.1, 5.2, 5.3, 5.4_
  - [ ] 3.6 Intégrer la saisie à Comptoir selon la note de choix, sans ressaisie de l'identité ni des coordonnées
    - _Exigences : 5.5_
  - [ ] 3.7 Écrire les tests de la tâche 3 : listes paramétrables, doublon, date d'envoi postérieure à la saisie refusée, droits du service client
    - _Exigences : 1.2, 1.3, 1.9, 5.2, 5.4_

- [ ] 4. Échéances, alertes et prolongation (dépend de 3.1)
  - [ ] 4.1 Développer le calcul de l'échéance (réception + 1 mois, jours calendaires) et l'affichage des jours restants
    - _Exigences : 3.1, 3.2_
  - [ ] 4.2 Développer le passage quotidien du moteur : alertes J+15 et J+25, marquage urgent, marquage hors délai conservé après clôture, rattrapage des passages manqués
    - _Exigences : 3.3, 3.4, 3.5_
  - [ ] 4.3 Développer l'écran des paramètres de délai et de seuils, avec journalisation
    - _Exigences : 3.6_
  - [ ] 4.4 Développer la page d'accueil triée par échéance croissante
    - _Exigences : 3.7_
  - [ ] 4.5 Développer la prolongation : motif obligatoire, réservée à l'équipe de la DPO, nouvelle échéance paramétrée, recalcul des alertes, plafond de deux mois
    - _Exigences : 4.1, 4.2, 4.3, 4.4, 4.5_
  - [ ] 4.6 Écrire les tests aux bornes : fins de mois, 29 février, réception un samedi, J+15, J+25, échéance, prolongation, modification d'un seuil
    - _Exigences : 3.1, 3.3, 3.4, 3.5, 3.6, 4.2, 4.3, 4.4_

- [ ] 5. Actions, effacement et clôture (dépend de 3.4)
  - [ ] 5.1 Développer la traçabilité des actions par système concerné : type d'action selon le type de demande, auteur, date, preuve
    - _Exigences : 6.1, 6.2_
  - [ ] 5.2 Développer le mode d'effacement (suppression, anonymisation, conservation légale), la saisie des données isolées et la liste paramétrable des obligations légales (factures : 10 ans)
    - _Exigences : 7.1, 7.2, 7.3_
  - [ ] 5.3 Développer l'alerte de fin de conservation des données isolées et le blocage du retrait du Lac pour un effacement
    - _Exigences : 7.4, 7.5_
  - [ ] 5.4 Développer la clôture : contrôle des actions manquantes, issue et motif, identité vérifiée pour l'issue `exécutée`, preuve de clôture, gel de la demande et compléments datés
    - _Exigences : 6.3, 6.4, 6.5, 6.6_
  - [ ] 5.5 Écrire les tests des règles de clôture et d'effacement
    - _Exigences : 6.3, 6.5, 6.6, 7.1, 7.2, 7.4, 7.5_

- [ ] 6. Export d'accès et espace de remise (dépend de 2.4 et 5.1)
  - [ ] 6.1 Développer le générateur d'export lisible, par système, avec libellés en français
    - _Exigences : 8.1_
  - [ ] 6.2 Développer l'espace de remise externe : vérification d'identité préalable, lien personnel, code transmis séparément, durée de validité, limite de tentatives
    - _Exigences : 8.2, 8.3_
  - [ ] 6.3 Développer l'expiration du lien avec alerte, la preuve de téléchargement et la remise par courrier
    - _Exigences : 8.4, 8.5, 8.6_
  - [ ] 6.4 Développer la purge des exports après le délai paramétré, en conservant preuve et empreinte
    - _Exigences : 8.7_
  - [ ] 6.5 Écrire les tests de sécurité de l'espace de remise (jeton, code, expiration, tentatives) et un test avec un export de 100 Mo
    - _Exigences : 8.2, 8.3, 8.4, 8.5_

- [ ] 7. Tableau de bord trimestriel (dépend de 4.2 et 5.4)
  - [ ] 7.1 Développer les indicateurs par trimestre civil, par type et par canal, dont le nombre de demandes importées sans preuve d'exécution
    - _Exigences : 9.1, 9.2_
  - [ ] 7.2 Développer l'export PDF et l'accès en lecture du comité des risques ; vérifier l'absence de donnée personnelle
    - _Exigences : 9.3, 9.4_

- [ ] 8. Conservation et reprise de l'existant (dépend de 1.3, 5.4 et 6.4)
  - [ ] 8.1 Développer la purge des demandes clôturées, de leurs pièces et de leurs preuves selon la durée paramétrée par la DPO
    - _Exigences : 11.4_
  - [ ] 8.2 Développer l'import du classeur avec rapport d'import et mention « antérieure à l'outil, preuve absente » ; répéter l'import sur la copie anonymisée
    - _Exigences : 1.8, 9.2, 11.7_
  - [ ] 8.3 Écrire les tests de conservation sur une horloge simulée
    - _Exigences : 8.7, 11.4_

- [ ] 9. Recette et mise en service du lot 1 (dépend de 3 à 8, et de 1.2 pour la date)
  - [ ] 9.1 Rédiger l'aide intégrée aux écrans et vérifier les libellés en français
    - _Exigences : 10.3_
  - [ ] 9.2 Faire le test d'utilisabilité : les 2 membres de l'équipe de la DPO et 2 conseillers du service client déroulent les scénarios sans assistance
    - _Exigences : 10.1, 10.2_
  - [ ] 9.3 Faire la recette métier sur un trimestre fictif rejoué (150 demandes synthétiques), tableau de bord compris
    - _Exigences : 1.1, 1.7, 3.3, 3.4, 3.5, 4.1, 6.4, 8.1, 9.1_
  - [ ] 9.4 Importer le classeur réel en production, faire contrôler le rapport d'import par l'équipe de la DPO, puis geler le classeur
    - _Exigences : 1.8_
  - [ ] 9.5 Mettre en production au plus tôt le 12 janvier 2027, dans l'UE, et ouvrir les accès par rôle
    - _Exigences : 11.2, 11.5_

- [ ] 10. Contrat d'interface et orchestrateur (lot 2, dépend de 9)
  - [ ] 10.1 Rédiger et publier le contrat d'interface unique (`rechercher`, `extraire`, `rectifier`, `effacer`, `opposer`, compte rendu), à transmettre aux projets P01, P02, P03, P06 et P07
    - _Exigences : 12.8_
  - [ ] 10.2 Développer l'orchestrateur : envoi après vérification d'identité et validation des systèmes par l'équipe de la DPO, suivi des comptes rendus, délai paramétré, repli manuel avec alerte
    - _Exigences : 12.1, 12.3, 12.4_
  - [ ] 10.3 Transmettre les catégories à isoler lors d'un effacement et intégrer les extractions reçues à l'export d'accès
    - _Exigences : 12.5, 12.6_
  - [ ] 10.4 Écrire les tests de l'orchestrateur avec un bouchon du contrat : succès, erreur, délai dépassé, compte rendu après clôture
    - _Exigences : 12.1, 12.3, 12.4_

- [ ] 11. Connecteurs des systèmes et recette du lot 2 (dépend de 10.1 et 10.2)
  - [ ] 11.1 Connecteurs Vitrine et Comptoir via Passerelle
    - _Exigences : 12.2_
  - [ ] 11.2 Connecteur Hangar via Passerelle
    - _Exigences : 12.2_
  - [ ] 11.3 Connecteur de l'outil d'e-mailing, opposition à la prospection comprise
    - _Exigences : 12.2, 12.7_
  - [ ] 11.4 Connecteur du Lac par traitement par lots
    - _Exigences : 12.2, 12.5_
  - [ ] 11.5 Faire la recette de bout en bout sur chaque système : accès, effacement avec isolation, opposition ; mettre en production hors gel
    - _Exigences : 12.1, 12.2, 12.3, 12.5, 12.6, 12.7_
