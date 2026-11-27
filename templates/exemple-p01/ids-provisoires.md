# Identifiants provisoires utilisés par la spec étalon P01

La spec `templates/exemple-p01/` a été écrite avant les fiches B02 et B05. Elle utilise la numérotation ci-dessous, qui suit l'ordre d'apparition dans le document.

- **A (extraction)** : si l'extracteur numérote autrement, prévenir C, qui remettra la spec étalon à jour.
- **B (analyse)** : `work/exemples/analyse.json` utilise les mêmes identifiants.

## B02 : ticket EVOL-2291 (service client)

| Id | Type | Énoncé | Citation |
|---|---|---|---|
| B02-D1 | fonctionnelle | Dernier statut et historique du colis dans la fiche commande de Comptoir | « Le conseiller doit voir le dernier statut du colis et son historique sans sortir de Comptoir. » |
| B02-D2 | non_fonctionnelle | Affichage en moins de 2 secondes | « Temps d'affichage acceptable : moins de 2 secondes » |
| B02-D3 | fonctionnelle | Message proactif au client quand sa commande est en retard | « Message proactif au client quand sa commande est en retard » |
| B02-D4 | contrainte | Envoi par e-mail uniquement | « Envoi par e-mail uniquement. » |
| B02-D5 | regle_metier | En retard dès que la date promise affichée sur Vitrine est dépassée (J+1 matin) | « Une commande est en retard dès que la date promise affichée sur Vitrine est dépassée, donc à J+1 matin. » |
| B02-D6 | regle_metier | Pas d'envoi si un dossier est ouvert sur la commande | « Pas d'envoi si un dossier est déjà ouvert sur la commande dans Comptoir » |
| B02-D7 | regle_metier | Message validé par un conseiller pour les clients Premium | « Pour les clients Premium, le message est validé par un conseiller avant envoi. » |
| B02-D8 | fonctionnelle | Textes modifiables par le service client sans la DSI | « Le texte des messages doit être modifiable par mon équipe sans passer par la DSI. » |
| B02-D9 | contrainte | Message d'information sans contenu commercial | « Message d'information uniquement, sans contenu commercial. » |
| B02-D10 | fonctionnelle | Statut visible pour les 3 transporteurs | « Le statut colis est visible dans la fiche commande pour les 3 transporteurs. » |
| B02-D11 | indicateur | Baisse de 30 % du taux de contacts WISMO | « Le taux de contacts WISMO baisse de 30 %. » |
| B02-D12 | echeance | Pas de mise en service avant janvier (gel du 16/11 au 11/01), T1 | « il y a le gel des mises en production du 16 novembre au 11 janvier » |
| B02-D13 | contrainte | Aucun message aux clients sans que le service client le sache | « je ne veux pas que des messages partent vers les clients sans que mon équipe le sache » |
| B02-D14 | fonctionnelle | Liste quotidienne des commandes concernées | « juste de la liste des commandes concernées chaque matin pour anticiper les appels » |

Chiffres : B02-N1 2 600 contacts / jour ; B02-N2 plus de 5 000 pendant les fêtes ; B02-N3 4 contacts sur 10 en WISMO.

## B05 : messagerie marketing

| Id | Énoncé | Citation |
|---|---|---|
| B05-D9 | Code promo dans les messages de retard | « dans les messages de retard de livraison que prépare la logistique, je voudrais qu'on glisse un code promo » |
