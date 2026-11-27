# Contrats d'interface du pipeline

Ce fichier est la référence commune des 4 membres de l'équipe. **On ne le modifie qu'ensemble** (ou en prévenant tout le monde), car chaque étape dépend du format produit par la précédente.

```
challenge-b/*  →  [1] extracteur  →  work/fiches/B0x.json
                                            ↓
                  [2] analyste     →  work/analyse.json  (+ work/analyse.md, rendu lisible)
                                            ↓
                  [3] redacteur-spec → .kiro/specs/<slug>/{requirements,design,tasks}.md
                                            ↓
                  [4] controleur   →  work/rapport-qualite.md
```

Exemples remplis : `work/exemples/`. Validation automatique : `python3 tools/valider_contrats.py` et `python3 tools/valider_specs.py`.

---

## 1. Identifiants (communs à toutes les étapes)

| Préfixe | Objet | Exemple | Créé par |
|---|---|---|---|
| `B0x` | Document source | `B01` | README du challenge |
| `B0x-Dn` | Demande élémentaire extraite d'un document | `B01-D2` | extracteur |
| `B0x-Nn` | Donnée chiffrée | `B01-N1` | extracteur |
| `B0x-Fn` | Point flou ou implicite dans un document | `B01-F1` | extracteur |
| `CT-nn` | Contrainte transverse (s'applique à plusieurs projets) | `CT-01` | analyste |
| `Cnn` | Conflit entre demandes | `C01` | analyste |
| `Hnn` | Hypothèse retenue faute d'arbitrage | `H01` | analyste |
| `Qnn` | Question ouverte à poser à un interlocuteur | `Q01` | analyste |
| `Pnn` | Projet (= une spec Kiro) | `P01` | analyste |

Règle d'or : **toute exigence d'une spec cite au moins une source** (`B0x-Dn`, `CT-nn` ou `Hnn`). Rien n'est inventé sans être marqué comme hypothèse.

---

## 2. Fiche document : `work/fiches/B0x.json` (étape 1)

Une fiche par document source. Champs obligatoires en **gras**.

| Champ | Type | Description |
|---|---|---|
| **`doc_id`** | string | `B01` à `B09` |
| **`fichier`** | string | Nom du fichier source |
| **`format`** | enum | `email`, `ticket`, `cahier_des_charges`, `notes_reunion`, `messagerie`, `transcription_vocale`, `note_interne`, `compte_rendu`, `tableau` |
| **`emetteur`** | object | `{nom, fonction, direction}` (valeurs `null` si inconnues) |
| `autres_parties` | array | Personnes citées : `{nom, fonction, role}` (destinataire, participant, mentionné…) |
| **`date`** | string | ISO `AAAA-MM-JJ` |
| **`resume`** | string | 2 à 3 phrases |
| **`demandes`** | array | Voir ci-dessous |
| **`chiffres`** | array | `{id, libelle, valeur, unite, citation}` |
| **`systemes_cites`** | array | Noms du glossaire (`Comptoir`, `Vitrine`, `Hangar`, `Passerelle`, `Lac`, …) |
| **`points_flous`** | array | `{id, description, citation}` : ambiguïtés, contradictions internes, implicites |

Chaque élément de `demandes` :

| Champ | Type | Description |
|---|---|---|
| **`id`** | string | `B0x-Dn` |
| **`type`** | enum | `fonctionnelle`, `non_fonctionnelle`, `regle_metier`, `contrainte`, `indicateur`, `echeance` |
| **`enonce`** | string | Reformulation neutre, une seule idée |
| **`citation`** | string | Extrait **verbatim** du document (preuve) |
| `acteurs` | array | Qui utilise / subit |
| `systemes` | array | Systèmes concernés |
| `priorite_exprimee` | string\|null | Telle qu'écrite par l'émetteur (`"P1"`, `"Bloquant"`, `"urgent"`…), sans normaliser |
| `echeance_exprimee` | string\|null | Telle qu'écrite (`"T1 2027"`, `"avant le pic"`…) |
| `statut_source` | enum | `demande` (par défaut), `rejete_en_seance`, `idee`, `v2` : pour les comptes rendus où tout n'est pas validé |

Pour B09 (CSV) : une ligne = au moins une demande, et `MKP-xx` est repris dans `enonce`.

---

## 3. Analyse transverse : `work/analyse.json` (étape 2)

```json
{
  "projets": [ ... ],
  "contraintes_transverses": [ ... ],
  "conflits": [ ... ],
  "hypotheses": [ ... ],
  "questions": [ ... ]
}
```

**Projet**

| Champ | Type | Description |
|---|---|---|
| **`id`** | string | `P01`… |
| **`slug`** | string | kebab-case, nom du dossier `.kiro/specs/<slug>/` |
| **`titre`** | string | |
| **`type_spec`** | enum | `feature` ou `bugfix` |
| **`commanditaire`** | string | Direction porteuse |
| **`parties_prenantes`** | array | Autres directions concernées |
| **`documents`** | array | `["B01","B02"]` |
| **`demandes_incluses`** | array | IDs `B0x-Dn` couverts par la spec |
| **`demandes_exclues`** | array | `{id, raison, renvoi}`, avec `renvoi` = autre `Pnn` ou `null` (hors périmètre) |
| **`contraintes`** | array | IDs `CT-nn` applicables |
| **`conflits`** | array | IDs `Cnn` concernés |
| **`dependances`** | array | `{projet, nature}` |
| `decoupage_versions` | object | `{"V1": [...ids], "V2": [...ids]}` si pertinent |

**Contrainte transverse** : `{id, enonce, sources: [B0x-Dn...], projets: [Pnn...]}`

**Conflit**

| Champ | Description |
|---|---|
| **`id`** | `Cnn` |
| **`sujet`** | Court libellé |
| **`positions`** | `[{source: "B01-D3", position: "SMS"}, {source: "B02-D4", position: "e-mail"}]` |
| **`gravite`** | `bloquant` (empêche de spécifier), `majeur` (change la conception), `mineur` |
| **`arbitre`** | Qui doit trancher (personne ou instance) |
| **`hypothese`** | `Hnn` retenue en attendant, ou `null` si bloquant |
| **`question`** | `Qnn` associée |

**Hypothèse** : `{id, enonce, justification, conflit: Cnn|null, reversible: bool}`

**Question** : `{id, question, destinataire, projets: [Pnn], bloquante: bool}`

`work/analyse.md` est un rendu lisible (registre des conflits et questions) pour les humains. La source de vérité est le JSON.

---

## 4. Spec Kiro : `.kiro/specs/<slug>/` (étape 3)

Trois fichiers, structure détaillée dans `.kiro/steering/format-spec.md` et `templates/`.

- `requirements.md` : introduction, glossaire, exigences numérotées `1`, `2`… avec user story et critères d'acceptation numérotés `1.1`, `1.2`… en EARS. **Chaque critère se termine par sa traçabilité** : `_Source : B01-D2, CT-01_` ou `_Source : H03_`. Sections finales obligatoires : `Hors périmètre`, `Hypothèses`, `Questions ouvertes`.
- `design.md` : vue d'ensemble, architecture (diagramme Mermaid), composants et interfaces, modèle de données, gestion des erreurs, sécurité et RGPD, stratégie de test.
- `tasks.md` : tâches à cases `- [ ] 1.` / `- [ ] 1.1`, sous-tâches avec `_Exigences : 1.1, 1.2_`. Toutes les exigences doivent être couvertes par au moins une tâche.

Pour une spec `bugfix`, `bugfix.md` remplace `requirements.md` (comportement actuel / attendu / inchangé).

---

## 5. Rapport qualité : `work/rapport-qualite.md` (étape 4)

Par spec : résultat des contrôles automatiques (`tools/valider_specs.py`) + revue de l'agent contrôleur (exigences non testables, conflit caché, demande source non couverte, contrainte transverse oubliée). Verdict : `OK`, `À corriger`, `Bloqué (question ouverte)`.

---

## 6. Décisions à confirmer au lancement

- [ ] Langue des mots-clés EARS : français (`QUAND … LE SYSTÈME DOIT …`), retenu par défaut, ou anglais.
- [ ] Liste provisoire des projets (ci-dessous) : l'analyste peut la modifier, mais il prévient C et D.

| Id | Slug | Documents |
|---|---|---|
| P01 | `alertes-retards-livraison` | B01, B02, B05 (code promo) |
| P02 | `portail-retours` | B03, B04, B09 (MKP-06) |
| P03 | `declaration-casse-entrepot` | B06 |
| P04 | `relance-paniers-abandonnes` | B05 |
| P05 | `registre-droits-rgpd` | B07 |
| P06 | `rdv-livraisons-fournisseurs` | B08 |
| P07 | `espace-vendeur-marketplace` | B09 (à découper ? MKP-07 ressemble à un bugfix) |
