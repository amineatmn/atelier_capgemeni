# Plan d'implémentation : Déclaration de casse à la douchette, blocage du stock dans Hangar et litiges transporteurs

Les tâches 1 à 7 forment la **V1** (E2), mise en production au plus tôt le 12 janvier (CT-07, H16). La tâche 8 forme la **V2**.

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre le traitement et les photos à la DPO (CT-01, CT-06) et fixer les durées de conservation
    - _Exigences : 9.1, 2.4_
  - [ ] 1.2 Définir avec l'équipe Passerelle et Hangar le contrat d'interface du blocage de stock (colis, article ou quantité, déblocage)
    - _Exigences : 5.1, 5.2_
  - [ ] 1.3 Constituer un jeu de données synthétique : colis, types de dégâts, cas hors ligne (CT-04)
    - _Exigences : 9.2_
  - [ ] 1.4 Obtenir la liste des types de dégâts, les destinataires « transport » et le délai par transporteur (Q29)
    - _Exigences : 1.2, 3.2, 6.1_

- [ ] 2. Service casse et modèle de données (dépend de 1.1)
  - [ ] 2.1 Créer le schéma (DossierCasse, Photo, Notification, Paramètre, JournalAccès) hébergé dans l'UE
    - _Exigences : 1.3, 9.3, 9.4_
  - [ ] 2.2 Développer l'API de création de dossier avec dédoublonnage et date limite de litige
    - _Exigences : 1.3, 4.2, 6.1, 6.2_
  - [ ] 2.3 Développer l'écran de paramétrage (types de dégâts, délai, destinataires, entrepôts actifs)
    - _Exigences : 1.2, 6.1, 7.1_
  - [ ] 2.4 Écrire les tests unitaires du service
    - _Exigences : 1.2, 1.3, 1.4, 6.2_

- [ ] 3. Application douchette (dépend de 2.2)
  - [ ] 3.1 Développer l'écran de scan, de choix du type de dégât et de validation
    - _Exigences : 1.1, 1.2, 1.3, 1.4_
  - [ ] 3.2 Ajouter la photo facultative, limitée à 2, selon l'équipement
    - _Exigences : 2.1, 2.2, 2.3_
  - [ ] 3.3 Implémenter la file locale, la synchronisation ordonnée et le compteur d'attente
    - _Exigences : 4.1, 4.2, 4.3, 4.4_
  - [ ] 3.4 Tester hors ligne : coupure, reprise, doublons
    - _Exigences : 4.1, 4.2, 4.3_

- [ ] 4. Blocage du stock dans Hangar (dépend de 1.2, 2.2)
  - [ ] 4.1 Développer le connecteur Passerelle vers Hangar avec rejeu et état du blocage
    - _Exigences : 5.1, 5.2, 5.3_
  - [ ] 4.2 Tester l'indisponibilité de Hangar et le rejeu
    - _Exigences : 5.2, 5.3_

- [ ] 5. Notifications et litiges (dépend de 1.4, 2.2)
  - [ ] 5.1 Notifier le chef d'équipe et le transport à la création du dossier, avec réessais
    - _Exigences : 3.1, 3.2, 3.3_
  - [ ] 5.2 Relancer le transport à J-1 de la date limite pour les dossiers non clos
    - _Exigences : 6.3_
  - [ ] 5.3 Tester les notifications et la relance
    - _Exigences : 3.1, 3.2, 3.3, 6.3_

- [ ] 6. Sécurité des photos (dépend de 2.1)
  - [ ] 6.1 Chiffrer les photos, contrôler l'accès par rôle et journaliser les accès
    - _Exigences : 2.4, 9.4_
  - [ ] 6.2 Tester la charge : 240 déclarations par jour avec photos
    - _Exigences : 9.5_

- [ ] 7. Recette et mise en service sur E2 (dépend de 3, 4, 5, 6)
  - [ ] 7.1 Faire la recette métier avec l'exploitation E2, avec et sans appareil photo
    - _Exigences : 1.3, 2.1, 2.2, 4.1, 5.1_
  - [ ] 7.2 Activer E2 au plus tôt le 12 janvier, après le gel et l'avis de la DPO, sinon conserver la fiche papier
    - _Exigences : 7.1, 7.2, 7.3, 7.4_

- [ ] 8. V2 (dépend de 7)
  - [ ] 8.1 Photo depuis le téléphone d'un chef d'équipe
    - _Exigences : 8.1_
  - [ ] 8.2 Retours abîmés avec note A / B / C et signalement manuel d'une note C
    - _Exigences : 8.2, 8.4_
  - [ ] 8.3 Saisie de la note et d'une photo au contrôle qualité sur douchette
    - _Exigences : 8.3_
  - [ ] 8.4 Tester les évolutions V2
    - _Exigences : 8.1, 8.2, 8.3, 8.4_
