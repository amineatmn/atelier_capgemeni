# Note interne : outillage des demandes d'exercice de droits

De : Hélène Marsac, déléguée à la protection des données (direction juridique et conformité)
Pour : comité d'architecture de la DSI
Date : 9 novembre 2026
Diffusion : restreinte

## Constat

Orvanne reçoit des demandes de clients qui souhaitent accéder à leurs données, les faire rectifier ou effacer, ou s'opposer à la prospection. Ces demandes arrivent par l'adresse dédiée et par courrier, mais aussi par le chat et les réseaux sociaux, où elles ne sont pas toujours reconnues comme telles. Elles sont suivies dans un classeur partagé tenu par mon équipe (2 personnes).

Sur les neuf premiers mois de 2026, nous avons enregistré 412 demandes, dont 61 % de demandes d'effacement. Dix-sept ont été traitées au-delà du délai légal d'un mois. La dernière revue interne a relevé qu'aucune preuve de l'exécution effective n'est conservée, et que les données restent présentes dans le Lac et dans les sauvegardes après leur effacement dans Vitrine.

## Besoin

1. Un registre unique des demandes, avec pour chacune : canal, date de réception, type, identité vérifiée ou non, systèmes concernés, échéance, statut, preuve de clôture.
2. Un compte à rebours par demande, avec des alertes à J+15 et J+25, et la possibilité de prolonger le délai de deux mois en motivant la décision.
3. Une orchestration des actions dans les systèmes concernés : Vitrine, Comptoir, Hangar, le Lac, l'outil d'e-mailing, et tout nouveau système qui stockerait des données clients.
4. Pour l'accès : la constitution d'un export lisible, remis au demandeur par un canal sécurisé.
5. Pour l'effacement : la suppression ou l'anonymisation, sauf pour les données à conserver au titre d'une obligation légale (factures : 10 ans), qui doivent être isolées.
6. Un tableau de bord trimestriel pour le comité des risques.

## Points d'attention pour les projets en cours

- Tout nouveau traitement doit m'être soumis avant développement. Je n'ai été consultée ni sur les alertes de retard, ni sur le portail de retours, ni sur les projets de personnalisation du marketing.
- Le numéro de mobile est collecté pour la livraison. Tout autre usage suppose une analyse préalable. Un message de service ne contient pas d'offre commerciale.
- Les données de prospection ne sont pas conservées plus de 3 ans après le dernier contact du client. Les historiques antérieurs doivent être purgés ou anonymisés ; ce chantier n'a pas commencé.
- Les photos et pièces jointes transmises par les clients ou prises en entrepôt sont des données personnelles dès lors qu'une étiquette ou une personne y est visible.
- Aucune donnée de production ne sert à des démonstrations ou à des tests sans anonymisation.

## Attentes

L'outil doit être utilisable par mon équipe sans formation lourde, et par le service client pour l'enregistrement des demandes reçues sur ses canaux. Je souhaite une première version avant le prochain contrôle interne. Le budget n'est pas arrêté ; une solution intégrée à l'existant serait préférable à l'achat d'un produit.
