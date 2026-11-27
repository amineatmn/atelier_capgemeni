# Plan d'implémentation : Registre et traitement des demandes d'exercice de droits RGPD

Les tâches 1 à 7 forment le **lot V1**, à livrer avant le prochain contrôle interne (date à confirmer, Q30), avec une mise en production hors du gel du 16 novembre au 11 janvier (CT-07). La tâche 8 forme le **lot V2** (orchestration automatisée).

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre le traitement à la DPO et obtenir son avis : base légale, durées de conservation du registre et du journal (CT-01)
    - Livrable : avis écrit versé au dossier
    - _Exigences : 11.1_
  - [ ] 1.2 Confirmer avec la DPO la date du contrôle interne, le point de départ du délai et le traitement du Lac et des sauvegardes (Q30)
    - Livrable : note de décision
    - _Exigences : 2.1, 6.4, 10.1_
  - [ ] 1.3 Valider avec le comité d'architecture l'hébergement et le mode d'intégration (Q34)
    - Livrable : décision d'hébergement
    - _Exigences : 10.2, 10.3_
  - [ ] 1.4 Constituer un jeu de données synthétique de demandes aux bornes de délai (CT-04)
    - _Exigences : 11.2_

- [ ] 2. Socle du registre (dépend de 1.1)
  - [ ] 2.1 Créer le schéma de données (Demande, ActionSystème, Prolongation, Export, Paramètre, JournalAudit, CatégorieConservation)
    - _Exigences : 1.1, 1.2_
  - [ ] 2.2 Développer le service Registre : création, modification, clôture avec refus sans preuve
    - _Exigences : 1.1, 1.4_
  - [ ] 2.3 Mettre en place le journal d'audit en ajout seul et les rôles d'accès
    - _Exigences : 1.3, 4.2, 11.3_
  - [ ] 2.4 Écrire les tests unitaires du socle
    - _Exigences : 1.1, 1.3, 1.4_

- [ ] 3. Compte à rebours et prolongation (dépend de 2.1)
  - [ ] 3.1 Calculer l'échéance et les jours restants, et lire les seuils dans les paramètres
    - _Exigences : 2.1, 2.2, 2.5_
  - [ ] 3.2 Développer le planificateur d'alertes J+15 et J+25 avec nouvelle tentative en cas d'échec
    - _Exigences : 2.3, 2.4_
  - [ ] 3.3 Marquer les demandes clôturées hors délai
    - _Exigences : 2.6_
  - [ ] 3.4 Développer la prolongation motivée de 2 mois et son historique
    - _Exigences : 3.1, 3.2, 3.3_
  - [ ] 3.5 Écrire les tests unitaires des échéances, alertes et prolongations
    - _Exigences : 2.1, 2.3, 2.4, 3.1_

- [ ] 4. Saisie par le service client et interface (dépend de 2.2, 2.3)
  - [ ] 4.1 Développer l'écran de saisie avec droits limités du service client
    - _Exigences : 4.1, 4.2_
  - [ ] 4.2 Notifier l'équipe DPO dans les 5 minutes suivant une saisie
    - _Exigences : 4.3_
  - [ ] 4.3 Développer la liste triée par échéance et rédiger le guide d'une page
    - _Exigences : 9.1, 9.2_
  - [ ] 4.4 Tester la saisie, les droits et la notification
    - _Exigences : 4.1, 4.2, 4.3_

- [ ] 5. Suivi par système, accès et effacement (dépend de 2.2)
  - [ ] 5.1 Gérer la liste des systèmes concernés et le suivi manuel des actions, avec refus de clôture si une action manque
    - _Exigences : 7.1, 7.2, 7.3_
  - [ ] 5.2 Développer l'export lisible et sa remise par lien limité, avec contrôle de l'identité vérifiée
    - _Exigences : 5.1, 5.2, 5.3, 5.4_
  - [ ] 5.3 Développer le traitement de l'effacement et le référentiel des catégories de conservation (factures : 10 ans)
    - _Exigences : 6.1, 6.2, 6.3, 6.4_
  - [ ] 5.4 Tester l'export, l'effacement et les cas d'erreur d'extraction
    - _Exigences : 5.1, 5.3, 6.2, 6.3_

- [ ] 6. Tableau de bord trimestriel (dépend de 3.3)
  - [ ] 6.1 Calculer les indicateurs par type, canal, hors délai et prolongations
    - _Exigences : 8.2_
  - [ ] 6.2 Produire et exporter le tableau de bord pour un trimestre choisi
    - _Exigences : 8.1, 8.3_
  - [ ] 6.3 Tester les indicateurs sur le jeu synthétique
    - _Exigences : 8.2_

- [ ] 7. Recette et mise en service V1 (dépend de 3, 4, 5, 6)
  - [ ] 7.1 Tests de sécurité : droits par rôle, accès au journal, expiration du lien
    - _Exigences : 5.2, 11.3_
  - [ ] 7.2 Recette métier : l'équipe DPO traite 10 demandes de bout en bout avec le guide
    - _Exigences : 1.1, 2.3, 5.1, 6.1, 9.1_
  - [ ] 7.3 Planifier la mise en production hors gel et vérifier l'environnement UE
    - _Exigences : 10.1, 10.2_
  - [ ] 7.4 Vérifier l'absence de données de production non anonymisées dans les environnements de test
    - _Exigences : 11.2_

- [ ] 8. Orchestration automatisée, lot V2 (dépend de 7.3 et d'un accord budgétaire)
  - [ ] 8.1 Spécifier avec chaque équipe un connecteur par système : Vitrine, Comptoir, Hangar, le Lac, outil d'e-mailing
    - _Exigences : 7.1, 7.4_
  - [ ] 8.2 Développer l'orchestrateur et l'enregistrement des résultats
    - _Exigences : 7.4_
  - [ ] 8.3 Développer la déclaration d'un nouveau système sans développement du cœur
    - _Exigences : 7.5_
  - [ ] 8.4 Tester chaque connecteur hors production avec des données anonymisées
    - _Exigences : 7.4, 11.2_
