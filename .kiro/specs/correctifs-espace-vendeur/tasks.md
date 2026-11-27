# Plan d'implémentation : correctif de l'export des ventes et des temps de réponse de l'espace vendeur

La tâche 1 (mesure et caractérisation) ne demande aucune mise en production et peut se faire pendant le gel du 16 novembre au 11 janvier (`CT-07`), donc pendant le pic. Les tâches 2 et 3 forment le **lot 1** (export des ventes), la tâche 4 le **lot 2** (temps de réponse). Les mises en production (tâche 5) ont lieu hors gel : au plus tôt le 12 janvier 2027, sauf livraison avant le 16 novembre 2026. Les deux lots précèdent les nouvelles vues de ventes de P07.

- [ ] 1. Mesure, caractérisation et prérequis (aucune dépendance)
  - [ ] 1.1 Mesurer les temps de réponse actuels des pages de l'espace vendeur (H27)
    - À partir des journaux d'accès existants si possible ; sinon, prévoir une instrumentation applicative à mettre en production hors gel
    - Livrable : rapport par page (nombre d'affichages, médiane, 95e centile), ventilé par classe de volume du vendeur, sur au moins 2 semaines, pic compris si la période le permet
    - _Exigences : 1.2_
  - [ ] 1.2 Faire fixer par la direction marketplace un seuil et un centile par page à partir du rapport de 1.1 (Q28)
    - Livrable : tableau des seuils validé par écrit, et liste des pages à corriger classées par priorité (affichages multipliés par le dépassement)
    - _Exigences : 2.9_
  - [ ] 1.3 Caractériser le défaut d'export : erreur exacte dans les journaux, délai avant l'erreur, présence d'une limite de 50 000 lignes dans la configuration ou le code, mémoire consommée, plan d'exécution de la requête d'export
    - Relever aussi, par simple comptage en production, le nombre de lignes du plus gros export de vendeur (aucune extraction de lignes, `CT-04`)
    - Livrable : note de cause confirmée (A, B, C ou D de `design.md`) et volume maximal relevé
    - _Exigences : 1.1, 2.3_
  - [ ] 1.4 Vérifier avec la DSI le contenu de l'export ; s'il contient des données de clients, soumettre la conservation des fichiers différés à la DPO (`CT-01`) et faire fixer la durée de conservation
    - Livrable : avis écrit de la DPO ou constat qu'aucune donnée de client n'est exportée
    - _Exigences : 2.5_
  - [ ] 1.5 Confirmer avec la DSI l'emplacement du stockage des fichiers et des mesures dans l'UE (`CT-08`, Q34)
    - Livrable : contrat d'interface du stockage (région, contrôle d'accès, liens à durée limitée)
    - _Exigences : 2.6_
  - [ ] 1.6 Constituer le jeu de données synthétique (`CT-04`) : vendeurs à 1, 10 000, 49 999, 50 000, 50 001 et 100 000 lignes, un vendeur à 2 fois le volume relevé en 1.3, et des ventes d'autres vendeurs mêlées dans la même base
    - _Exigences : 2.1, 2.3, 3.2_
  - [ ] 1.7 Produire les références de l'existant sur le jeu synthétique : fichiers d'export de 1, 10 000 et 50 000 lignes générés par la version actuelle, durée des traitements qui lisent ou écrivent les lignes de commande, inventaire des fonctions et informations de chaque page
    - _Exigences : 3.1, 3.3, 3.4_

- [ ] 2. Tests de reproduction et de non-régression de l'export (dépend de 1.3, 1.6 et 1.7)
  - [ ] 2.1 Écrire le test automatisé de l'export de 50 001 lignes ; vérifier qu'il échoue sur la version actuelle avec l'erreur décrite en 1.3
    - _Exigences : 1.1_
  - [ ] 2.2 Écrire les tests de non-régression : comparaison des exports de 1, 10 000 et 50 000 lignes aux fichiers de référence, et absence de ventes d'autres vendeurs dans chaque export
    - _Exigences : 3.1, 3.2_

- [ ] 3. Correctif de l'export des ventes, lot 1 (dépend de 2)
  - [ ] 3.1 Supprimer la cause confirmée en 1.3 et produire l'export par flux (lecture par lots, écriture progressive), au format et avec les colonnes actuels
    - _Exigences : 2.1, 2.2, 3.1_
  - [ ] 3.2 Contrôler le nombre de lignes écrites par rapport au nombre attendu et rejeter tout fichier incomplet
    - _Exigences : 2.2, 2.7_
  - [ ] 3.3 Ajouter le mode différé au-delà du seuil paramétrable (50 000 lignes par défaut, proposition) : file des demandes, traitement en arrière-plan à concurrence limitée, états « en préparation », « prêt », « en échec »
    - _Exigences : 2.4, 2.10_
  - [ ] 3.4 Stocker les fichiers différés dans l'UE, réserver le téléchargement au vendeur demandeur et mettre en place la purge à l'échéance de la durée paramétrée
    - _Exigences : 2.5, 2.6, 3.2_
  - [ ] 3.5 Gérer les échecs : message au vendeur avec invitation à relancer, nouvelles tentatives du traitement en arrière-plan, enregistrement de l'erreur avec le nombre de lignes, alerte à la supervision
    - _Exigences : 2.7_
  - [ ] 3.6 Si la cause D est confirmée en 1.3, créer l'index sur la table des lignes de commande (piste `B09-D10`) et mesurer la durée des traitements existants avant et après
    - Livrable : comparaison avec les références de 1.7 ; index retiré ou redéfini si une durée dépasse la référence
    - _Exigences : 3.4_
  - [ ] 3.7 Tester le correctif : le test de 2.1 passe ; exports de 100 000 lignes et du double du volume relevé ; comptages ; accès d'un autre vendeur et lien expiré ; purge ; pannes simulées ; les tests de 2.2 passent toujours
    - _Exigences : 2.1, 2.2, 2.3, 2.4, 2.5, 2.7, 3.1, 3.2_

- [ ] 4. Correctif des temps de réponse, lot 2 (dépend de 1.2 ; 4.4 dépend aussi de 3.3)
  - [ ] 4.1 Mettre en place l'instrumentation permanente des temps de réponse par page (page, horodatage, durée, classe de volume, sans donnée personnelle), stockée dans l'UE
    - _Exigences : 2.8, 2.6_
  - [ ] 4.2 Corriger les pages au-dessus de leur seuil, dans l'ordre de priorité de 1.2 ; créer une sous-tâche par page à l'issue de 1.2, chacune avec son test de charge au double du trafic relevé
    - _Exigences : 2.9_
  - [ ] 4.3 Paramétrer les seuils, le centile et la période d'observation dans la supervision, et l'alerte en cas de dépassement
    - _Exigences : 2.11_
  - [ ] 4.4 Tester la charge des pages pendant 2 exports simultanés du plus gros volume
    - _Exigences : 2.10_
  - [ ] 4.5 Rejouer l'inventaire fonctionnel de 1.7 sur les pages corrigées
    - _Exigences : 3.3_

- [ ] 5. Recette et mise en production (dépend de 3 pour le lot 1, de 4 pour le lot 2 ; hors gel, `CT-07`)
  - [ ] 5.1 Faire la recette du lot 1 avec la direction marketplace et des vendeurs pilotes, sur le jeu synthétique en environnement de recette
    - _Exigences : 2.1, 2.4, 3.1_
  - [ ] 5.2 Mettre le lot 1 en production hors gel, avant les nouvelles vues de ventes de P07, et vérifier en production la région de stockage des fichiers
    - _Exigences : 2.6, 3.4_
  - [ ] 5.3 Faire la recette du lot 2 avec la direction marketplace : rapport de mesure avant et après correctif
    - _Exigences : 2.9, 3.3_
  - [ ] 5.4 Mettre le lot 2 en production hors gel, puis mesurer pendant 2 semaines : seuils par page respectés, alertes reçues, durée des traitements sur les lignes de commande au plus égale à la référence
    - _Exigences : 2.8, 2.9, 2.11, 3.4_
