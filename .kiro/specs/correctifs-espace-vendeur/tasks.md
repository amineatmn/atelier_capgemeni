# Plan d'implémentation : correctifs de l'espace vendeur (export des ventes et temps de réponse)

Livraison en un seul lot, hors gel des mises en production (16 novembre au 11 janvier, CT-07). Ces correctifs précèdent le projet P07 et n'en dépendent pas.

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Confirmer avec la DSI le système et l'hébergement de l'espace vendeur (Q34, CT-08) et soumettre à la DPO l'éventuel fichier d'export asynchrone (CT-01)
    - Livrable : note de cadrage et avis de la DPO
    - _Exigences : 2.5_
  - [ ] 1.2 Constituer un jeu de données synthétique de ventes (50 000, 50 001 et 500 000 lignes) sans donnée de production (CT-04)
    - _Exigences : 1.1_
  - [ ] 1.3 Interroger la direction marketplace et la DSI sur les pages lentes et le temps attendu (Q28)
    - _Exigences : 2.4_

- [ ] 2. Reproduction et mesure (dépend de 1.2)
  - [ ] 2.1 Écrire le test qui reproduit l'erreur d'export au-delà de 50 000 lignes et relever le plan d'exécution
    - _Exigences : 1.1_
  - [ ] 2.2 Instrumenter les pages de l'espace vendeur (médiane et 95e centile) et relever la situation actuelle
    - _Exigences : 1.2, 2.3_

- [ ] 3. Correctif de l'export (dépend de 2.1)
  - [ ] 3.1 Corriger la cause constatée : index sur les lignes de commande et/ou lecture par blocs
    - _Exigences : 2.1_
  - [ ] 3.2 Passer l'export en asynchrone au-delà d'un seuil paramétrable si la reproduction le justifie, avec mise à disposition du fichier au vendeur
    - _Exigences : 2.1, 2.2_
  - [ ] 3.3 Gérer et journaliser les échecs d'export avec un message explicite
    - _Exigences : 2.2_
  - [ ] 3.4 Tests de correction : 50 001 et 500 000 lignes, échec simulé
    - _Exigences : 2.1, 2.2_
  - [ ] 3.5 Tests de non-régression : export de 50 000 lignes ou moins identique à la référence
    - _Exigences : 3.1_

- [ ] 4. Correctif de la lenteur (dépend de 2.2 et 1.3)
  - [ ] 4.1 Paramétrer le seuil de temps de réponse au 95e centile et le fixer avec la direction marketplace à partir de la mesure
    - _Exigences : 2.4_
  - [ ] 4.2 Optimiser les pages dépassant le seuil
    - _Exigences : 2.4_
  - [ ] 4.3 Tests de correction : temps de réponse sous le seuil après correctif
    - _Exigences : 2.3, 2.4_
  - [ ] 4.4 Tests de non-régression : résultats et droits d'accès des fonctions existantes
    - _Exigences : 3.2_

- [ ] 5. Recette et mise en production (dépend de 3.4, 3.5, 4.3 et 4.4)
  - [ ] 5.1 Vérifier que le déploiement est indépendant de P07
    - _Exigences : 3.3_
  - [ ] 5.2 Planifier la mise en production hors gel (reportée au 12 janvier au plus tôt si nécessaire) et faire la recette avec la direction marketplace
    - _Exigences : 2.5, 2.1, 2.4_
