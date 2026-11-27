# Référence : conflits attendus dans l'analyse

<!-- Responsable : B. Référence humaine établie par lecture croisée des 9 documents. Elle sert à vérifier que l'analyste détecte les conflits connus (critère de fin du rôle B) ; l'agent la consulte en autocontrôle, il ne la recopie pas. -->

Identifiants `Rnn` propres à ce fichier, indépendants des `Cnn` générés. Sources au niveau du document (§, ligne ou heure), car les `B0x-Dn` dépendent des fiches.

Utilisation : après une exécution de l'analyste, chaque ligne doit correspondre à un `Cnn` de `work/analyse.json`, ou à une justification dans la section « Écarts avec la référence » de `work/analyse.md`.

## P01 Retards de livraison

| Réf. | Sujet | Positions | Gravité attendue | Arbitre | Hypothèse attendue |
|---|---|---|---|---|---|
| R01 | Canal de l'alerte | SMS [B01 point 2] / e-mail seul [B02 §B] / mobile réservé à la livraison [B07, CT-02] | majeur | Comité de direction, avis DPO | E-mail en V1, SMS désactivé |
| R02 | Seuil de retard | 48 h [B01] / J+1 matin [B02 §B] | majeur ou mineur si paramétré | Comité de direction | Deux seuils paramétrables |
| R03 | Validation avant envoi | Aucune intervention manuelle [B01] / validation pour les Premium [B02 §B] | majeur | Comité de direction | Automatique sauf Premium, paramètre |
| R04 | Propriété du projet et des messages | Logistique [B01] / « la relation client, c'est nous » [B02 commentaire 23/10] | majeur | Comité de direction | Détection à la logistique, messages au service client |
| R05 | Échéance | Pour le pic [B01] / gel 16/11 au 11/01 [B02, CT-07] | majeur | DSI | Mise en service après le 11/01 |
| R06 | Code promo dans le message | Code promo [B05 10:25] / sans contenu commercial [B02 §B, B07, CT-03] | mineur | DPO | Refusé |

Points de P01 qui ne sont pas des conflits, mais des questions ou des hypothèses : « temps réel » contre fichiers du matin [B01] ; « les rouges » [B01] ; source de la nouvelle date [B01] ; retard par colis ou par commande [B01 / B02] ; liste matinale [B02] en complément du tableau de bord [B01], pas en concurrence.

## P02 Portail de retours

| Réf. | Sujet | Positions | Gravité attendue | Arbitre | Hypothèse attendue |
|---|---|---|---|---|---|
| R07 | Délai de retour | 30 jours [B03 EF-02] / 14 jours, 30 pour Orvanne+ [B04] | mineur (paramètre) | Direction juridique (CGV) | Délai par segment, valeurs des CGV |
| R08 | Frais de retour | Gratuit [B03 §6] / 4,90 € sauf défaut ou erreur [B04, finance] / gratuit au lancement [B04, marketing] | majeur | Finance (DAF) | Frais par motif, règle de la finance |
| R09 | Déclenchement du remboursement | Au premier scan [B03 EF-07] / après contrôle [B04, finance] / au dépôt pour les bons clients [B04, marketing] | majeur | Finance (DAF), comité de direction | Après contrôle, déclencheur paramétrable |
| R10 | Articles de la marketplace | Exclus [B03 §3] / indispensables en V1, 35 % des demandes [B04, Yanis] / autre circuit [B04, Karim] / suivi par les vendeurs [B09 MKP-06] | majeur | Direction de l'expérience client et direction marketplace | Exclus de la V1, circuit prévu en V2 |
| R11 | Identification du client | Sans compte [B03 §3] / « client connecté à son compte » [B03 EF-03] | mineur (contradiction interne) | Rédactrice du CDC (Inès Rouvière) | Sans compte |
| R12 | Remboursement selon la note C | Montant réduit [B04, Karim] / « légalement non » [B04, Yanis] | majeur | Direction juridique | Remboursement intégral |
| R13 | Photos du client | Souhaitable, motif « endommagé » [B03 EF-09] / l'entrepôt veut les voir avant réception [B04] / données personnelles [B07, CT-06] | mineur | DPO | Facultatives, durée de conservation limitée |
| R14 | Échéance | Pilote avant les soldes d'hiver [B03 §6] / gel jusqu'au 11/01 [CT-07] | majeur | Direction de l'expérience client, DSI | Pilote après le 11/01 |
| R15 | Bon de retour (RMA) | RMA imprimé dans le colis [B04] / étiquette PDF ou QR code [B03 EF-05] | mineur | Exploitation E2 | Numéro de retour sur l'étiquette et document imprimable facultatif |
| R16 | Bon d'achat +5 % | Idée marketing, accord de principe de la finance [B04] / absent du CDC [B03] | mineur | Finance, marketing | V2 ou hors périmètre |

## P03 Casse et contrôle en entrepôt

| Réf. | Sujet | Positions | Gravité attendue | Arbitre | Hypothèse attendue |
|---|---|---|---|---|---|
| R17 | Terminal de saisie | Douchette avec photo [B06] / deux tiers des douchettes sans appareil photo [B06] | majeur (faisabilité, interne au document) | Exploitation E2, DSI | Douchettes récentes et téléphones des chefs d'équipe |
| R18 | Casse seule ou casse et retours | Même écran avec note A/B/C [B06] / application de contrôle hors CDC [B04] | majeur | DSI, exploitation E2 | Modèle commun, retours en lot 2 |
| R19 | Échéance | Inventaire de janvier [B06] / gel jusqu'au 11/01 [CT-07] | majeur | Exploitation E2, DSI | Après le 11/01 |

## P04 Paniers abandonnés

| Réf. | Sujet | Positions | Gravité attendue | Arbitre | Hypothèse attendue |
|---|---|---|---|---|---|
| R20 | Démo sur données réelles | « Sur les vrais clients » [B05 10:31] / anonymisation obligatoire [B07, CT-04] | mineur | DPO | Démo sur données anonymisées |
| R21 | Profondeur d'historique | Depuis 2014 [B05 10:15] / 3 ans maximum [B07, CT-05] | majeur | DPO | Données conformes à CT-05 uniquement |
| R22 | Base légale et canaux | « On a le consentement newsletter » [B05 10:28] / avis DPO préalable [CT-01], mobile réservé [CT-02] | bloquant | DPO | Aucune (avis DPO attendu) |
| R23 | Plafonds de remise | 10 %, 15 % Orvanne+, « pour l'instant » [B05 10:22] / non validés par la finance [B05 10:21] | mineur | Finance | Plafond à 0 % tant que non validé |

## P06 Rendez-vous fournisseurs

| Réf. | Sujet | Positions | Gravité attendue | Arbitre | Hypothèse attendue |
|---|---|---|---|---|---|
| R24 | Durée des créneaux | 30 minutes [B08 R2, Rémi] / une heure sur E2 [B08 §3, Karim] / « créneaux d'une heure » dans l'action de E1 [B08 §5] | mineur (paramètre par site) | Approvisionnement (Grégory Thibaudeau) | Paramètre par site, 30 minutes par défaut |
| R25 | Nombre de quais de E1 | 6 quais [B08 §1] / 4 quais [B08 §5] | mineur | Rémi Vasseur | Paramètre de site |
| R26 | Messageries sans commande d'achat | Hors périmètre [B08 §3, Grégory] / indispensable [B08 §3, Rémi] | majeur | Approvisionnement | Hors réservation en V1, créneau bloqué par le chef de quai (R7) |
| R27 | Notation des fournisseurs | Notation et pénalités [B08 §3, achats] / attendre un an [B08 §3, approvisionnement] | mineur (tranché en V2 par B08 §4) | Approvisionnement, achats | Ponctualité collectée en V1, notation en V2 |

## P07 Espace vendeur

| Réf. | Sujet | Positions | Gravité attendue | Arbitre | Hypothèse attendue |
|---|---|---|---|---|---|
| R28 | Alertes de retard des vendeurs | 2 % sur 30 jours au chargé de compte [MKP-03] / 5 % sur 7 jours au vendeur [MKP-08] | mineur (deux alertes distinctes) | Direction marketplace | Deux alertes paramétrables |
| R29 | Modification de l'IBAN | Par le vendeur seul [MKP-04] / double validation interne [MKP-05] | majeur | Finance | Saisie par le vendeur, double validation avant prise en compte |
| R30 | Échelle de priorité | P1, Haute, urgent, 1, moyenne, vide [B09] | mineur | Direction marketplace | Échelle normalisée proposée |
| R31 | Retours marketplace | Suivi des retours par les vendeurs [MKP-06] / marketplace exclue du portail [B03 §3] | majeur (dépendance avec R10) | Direction marketplace | MKP-06 en V2, après R10 |

## Transverses

| Réf. | Sujet | Constat | Attendu |
|---|---|---|---|
| R32 | Plusieurs sens du mot « retard » | Retard de livraison [B01, B02], d'expédition vendeur [MKP-03, MKP-08], d'arrivée d'un camion [B08 R5] | Trois termes distincts, signalés au glossaire (A) |
| R33 | DPO non consultée | P01, P02 et P04 [B07] | CT-01 appliquée à ces projets |
| R34 | « Premium » et « Orvanne+ » | Deux noms de segment [B02, B04, B05] | Question au marketing et au service client |
