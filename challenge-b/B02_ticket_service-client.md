# [EVOL-2291] Prévenir les clients en cas de retard et afficher le suivi colis dans Comptoir

| Champ | Valeur |
|---|---|
| Outil | Guichet DSI (demandes d'évolution) |
| Type | Évolution |
| Demandeur | Yanis Mercadier, responsable du service client |
| Créé le | 21/10/2026 09:17 |
| Application | Comptoir |
| Priorité | Bloquant |
| Échéance souhaitée | T1 2027 |
| Statut | À qualifier |
| Affecté à | (personne) |

## Description

Depuis septembre, 4 contacts sur 10 sont du WISMO. On reçoit environ 2 600 contacts par jour (téléphone, chat et e-mail confondus) et on monte à plus de 5 000 pendant les fêtes. Les conseillers passent leur temps à copier le numéro de suivi depuis Comptoir pour le coller sur le site du transporteur.

Deux demandes.

**A. Suivi colis dans la fiche commande de Comptoir**

Le conseiller doit voir le dernier statut du colis et son historique sans sortir de Comptoir. Temps d'affichage acceptable : moins de 2 secondes, sinon ils continueront à ouvrir le site du transporteur.

**B. Message proactif au client quand sa commande est en retard**

- Envoi par e-mail uniquement. Le SMS a été étudié l'an dernier et refusé pour une question de budget, et nous n'avons pas le numéro de mobile de tous les clients.
- Une commande est en retard dès que la date promise affichée sur Vitrine est dépassée, donc à J+1 matin. Attendre plus longtemps n'a pas de sens : c'est précisément à ce moment que le client nous appelle.
- Pas d'envoi si un dossier est déjà ouvert sur la commande dans Comptoir, pour ne pas dire deux choses différentes au client.
- Pour les clients Premium, le message est validé par un conseiller avant envoi.
- Le texte des messages doit être modifiable par mon équipe sans passer par la DSI.
- Message d'information uniquement, sans contenu commercial.

## Critères d'acceptation

- [ ] Le statut colis est visible dans la fiche commande pour les 3 transporteurs.
- [ ] Le taux de contacts WISMO baisse de 30 %.
- [ ] Aucun message n'est envoyé pour une commande ayant un dossier ouvert.

## Commentaires

**21/10/2026 11:02, Yanis Mercadier**
Précision : inutile de viser une mise en service avant janvier, il y a le gel des mises en production du 16 novembre au 11 janvier. Je préfère quelque chose de propre au premier trimestre.

**23/10/2026 08:55, Yanis Mercadier**
J'apprends que la logistique prépare quelque chose de son côté sur les retards. La relation client, c'est nous : je ne veux pas que des messages partent vers les clients sans que mon équipe le sache. Et je n'ai pas besoin d'un tableau de bord, juste de la liste des commandes concernées chaque matin pour anticiper les appels.
