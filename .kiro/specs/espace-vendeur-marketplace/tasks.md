# Plan d'implémentation : Évolutions de l'espace vendeur de la marketplace

Les tâches 1 à 6 forment le **lot 1** (alerte vendeur au 15/01/2027, MKP-01 au T1 2027, MKP-03 fin mars, IBAN dès que possible). Les tâches 7 à 10 forment le **lot 2** (S1 à T2 2027). Aucune mise en production du 16/11 au 11/01 (CT-07). Les correctifs du projet P08 sont à livrer avant la tâche 2.

- [ ] 1. Prérequis et cadrage (aucune dépendance)
  - [ ] 1.1 Soumettre le traitement des IBAN et des échanges à la DPO (CT-01, Q36)
    - Livrable : avis écrit de la DPO
    - _Exigences : 10.5, 5.2_
  - [ ] 1.2 Obtenir de la direction marketplace la définition de « commande expédiée en retard » et la liste des chargés de compte par vendeur (Q26)
    - _Exigences : 3.4, 4.1_
  - [ ] 1.3 Faire fixer par la finance les deux valideurs d'IBAN (Q25)
    - _Exigences : 5.6_
  - [ ] 1.4 Constituer un jeu de données synthétique de vendeurs, commandes et factures (CT-04)
    - _Exigences : 10.1_

- [ ] 2. Vue des ventes (dépend de 1.4)
  - [ ] 2.1 Développer le service Ventes (jour, semaine, mois) et l'écran
    - _Exigences : 1.1, 1.2_
  - [ ] 2.2 Gérer l'indisponibilité des données
    - _Exigences : 1.3_
  - [ ] 2.3 Écrire les tests unitaires et d'isolement entre vendeurs
    - _Exigences : 1.1, 1.2, 1.3_

- [ ] 3. Factures de commission (dépend de 1.4)
  - [ ] 3.1 Mettre en place le dépôt mensuel des PDF et le téléchargement contrôlé par vendeur
    - _Exigences : 2.1, 2.2, 2.3_
  - [ ] 3.2 Gérer le mois sans PDF et tester l'accès croisé entre vendeurs
    - _Exigences : 2.3, 2.4_

- [ ] 4. Alertes de retard (dépend de 1.2, 1.4)
  - [ ] 4.1 Développer le calcul des taux sur 30 et 7 jours glissants avec règles paramétrables
    - _Exigences : 3.1, 3.3, 3.4, 4.1, 4.3_
  - [ ] 4.2 Émettre l'alerte aux chargés de compte (2 %) sans doublon
    - _Exigences : 3.2, 3.5_
  - [ ] 4.3 Émettre l'alerte au vendeur (5 %) avec information du chargé de compte
    - _Exigences : 4.2, 4.4, 4.5_
  - [ ] 4.4 Tester les bornes exactes de 2 % et 5 %
    - _Exigences : 3.2, 4.2_

- [ ] 5. Modification de l'IBAN (dépend de 1.1, 1.3)
  - [ ] 5.1 Développer la demande, ses états et le maintien de l'ancien IBAN
    - _Exigences : 5.1, 5.3_
  - [ ] 5.2 Développer la double validation par deux personnes distinctes, le refus et les notifications
    - _Exigences : 5.2, 5.4, 5.7_
  - [ ] 5.3 Mettre en place le journal d'audit sans IBAN en clair
    - _Exigences : 5.5, 10.4_
  - [ ] 5.4 Écrire les tests unitaires et de sécurité du flux
    - _Exigences : 5.1, 5.2, 5.4, 5.5_

- [ ] 6. Recette du lot 1 (dépend de 2, 3, 4, 5)
  - [ ] 6.1 Recette métier avec finance, chargés de compte et vendeurs du top 20
    - _Exigences : 1.1, 2.2, 3.2, 4.2, 5.2_
  - [ ] 6.2 Planifier la mise en production hors gel et vérifier l'hébergement dans l'UE
    - _Exigences : 10.2, 10.3_

- [ ] 7. Messagerie vendeur-client (lot 2, dépend de 6.2)
  - [ ] 7.1 Arbitrer le canal (Comptoir ou messagerie dédiée) puis le développer
    - _Exigences : 6.1, 6.2, 6.3, 6.4_
  - [ ] 7.2 Tester la remise des réponses au client
    - _Exigences : 6.1, 6.2_

- [ ] 8. Ouverture européenne (lot 2, dépend de 6.2)
  - [ ] 8.1 Paramétrer pays et langues, et traduire les écrans de l'Allemagne et de l'Espagne
    - _Exigences : 7.1, 7.2, 7.3_
  - [ ] 8.2 Tester l'accès et l'affichage par pays
    - _Exigences : 7.1, 7.2_

- [ ] 9. Reversements lisibles (lot 2, dépend de 6.2)
  - [ ] 9.1 Développer l'écran de détail des reversements
    - _Exigences : 8.1_
  - [ ] 9.2 Faire un test d'usage avec au moins 5 vendeurs
    - _Exigences : 8.2_

- [ ] 10. Mobile et accessibilité (lot 2, dépend de 2.1)
  - [ ] 10.1 Adapter le tableau de bord aux smartphones
    - _Exigences : 9.1, 9.2_
  - [ ] 10.2 Contrôler la conformité RGAA
    - _Exigences : 9.3_
