# Plan d'implémentation : relance personnalisée des paniers abandonnés

Les tâches 1 à 3 forment le **lot 1** : démo hors production pour le comité commerce du 8 décembre, sur données synthétiques. Les tâches 4 à 7 forment le **lot 2** : V1 en production, après le gel (11 janvier) et l'avis de la DPO.

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre le traitement à la DPO : base légale, portée du consentement newsletter, canaux, analyse d'impact (`CT-01`, `Q18`, `Q36`)
    - Livrable : avis écrit de la DPO
    - _Exigences : 6.1, 4.5_
  - [ ] 1.2 Mesurer dans le Lac la volumétrie des paniers et les données disponibles (commandes, navigation) (`Q19`)
    - _Exigences : 9.1, 3.1_
  - [ ] 1.3 Définir les contrats d'interface avec Vitrine, le registre des droits (P05) et l'outil d'e-mailing
    - _Exigences : 6.2, 1.1_
  - [ ] 1.4 Constituer un jeu de données synthétique de clients et de paniers (`CT-04`)
    - _Exigences : 7.2, 9.4_

- [ ] 2. Moteur de règles (dépend de 1.2)
  - [ ] 2.1 Créer le schéma des paramètres, décisions et paniers, avec durée de conservation de 3 ans
    - _Exigences : 1.2, 3.5_
  - [ ] 2.2 Implémenter le moteur de règles derrière une interface remplaçable, avec journal de la règle appliquée
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.5_
  - [ ] 2.3 Implémenter le filtre de données limité aux 3 ans et le repli sans navigation
    - _Exigences : 3.1, 3.2, 3.3, 3.4_
  - [ ] 2.4 Implémenter remise ciblée et plafonds paramétrables
    - _Exigences : 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [ ] 2.5 Écrire les tests unitaires du moteur
    - _Exigences : 2.1, 3.2, 5.3, 5.5_

- [ ] 3. Démo du comité commerce (dépend de 1.4, 2.2)
  - [ ] 3.1 Monter l'environnement de démo hors production sans envoi réel
    - _Exigences : 7.1, 7.3, 7.5_
  - [ ] 3.2 Préparer trois clients types et l'affichage de la règle appliquée
    - _Exigences : 7.2, 7.4_
  - [ ] 3.3 Construire le tableau du CA incrémental sur données synthétiques
    - _Exigences : 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 4. Détection et conformité (dépend de 1.1, 1.3, 2.1)
  - [ ] 4.1 Développer le détecteur de paniers abandonnés et l'annulation à la commande
    - _Exigences : 1.1, 1.4_
  - [ ] 4.2 Développer le contrôle de consentement et d'opposition, par défaut « ne pas relancer »
    - _Exigences : 6.2, 6.3, 6.4, 4.5_
  - [ ] 4.3 Verrouiller les canaux : e-mail seul, mobile jamais utilisé
    - _Exigences : 4.1, 4.2, 4.3, 4.4_
  - [ ] 4.4 Écrire les tests de conformité
    - _Exigences : 4.2, 6.2, 6.3_

- [ ] 5. Envoi et mesure (dépend de 4.1, 4.2)
  - [ ] 5.1 Intégrer l'outil d'e-mailing, avec nouvelles tentatives limitées et plafond de relances par panier
    - _Exigences : 1.3, 1.5, 9.3_
  - [ ] 5.2 Mettre en place le groupe témoin et le calcul du CA incrémental réel
    - _Exigences : 8.1, 8.2, 8.3_
  - [ ] 5.3 Hébergement dans l'UE et gestion des accès
    - _Exigences : 6.5_

- [ ] 6. Tests de charge et recette (dépend de 5.1)
  - [ ] 6.1 Tester la charge au volume mesuré, doublé pour le pic
    - _Exigences : 9.1, 9.2_
  - [ ] 6.2 Recette métier de bout en bout sur données synthétiques
    - _Exigences : 1.1, 2.1, 4.1, 5.3, 9.4_

- [ ] 7. Mise en production (dépend de 6.2, 1.1)
  - [ ] 7.1 Planifier le déploiement après le 11 janvier et vérifier l'avis de la DPO
    - _Exigences : 6.1, 7.5_
