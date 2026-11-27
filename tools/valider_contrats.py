#!/usr/bin/env python3
"""Valide les fichiers intermédiaires du pipeline (CONTRATS.md §2 et §3).

Usage :
    python3 tools/valider_contrats.py                 # valide work/fiches/*.json et work/analyse.json
    python3 tools/valider_contrats.py <fichier.json>  # valide un fichier précis

Code de sortie 0 si tout est valide, 1 sinon. Aucune dépendance externe.
Responsable : D (les règles suivent CONTRATS.md ; toute évolution du contrat se reporte ici).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / "challenge-b"

FORMATS = {"email", "ticket", "cahier_des_charges", "notes_reunion", "messagerie",
           "transcription_vocale", "note_interne", "compte_rendu", "tableau"}
TYPES_DEMANDE = {"fonctionnelle", "non_fonctionnelle", "regle_metier", "contrainte", "indicateur", "echeance"}
STATUTS = {"demande", "rejete_en_seance", "idee", "v2"}
GRAVITES = {"bloquant", "majeur", "mineur"}


def normaliser(texte: str) -> str:
    """Espaces et apostrophes uniformisés pour comparer une citation au texte source."""
    texte = texte.replace("\u2019", "'").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", texte).strip().lower()


def exiger(obj: dict, champs, contexte: str, erreurs: list) -> None:
    for champ in champs:
        if champ not in obj:
            erreurs.append(f"{contexte} : champ obligatoire manquant « {champ} »")


def valider_fiche(chemin: Path, erreurs: list) -> dict | None:
    try:
        fiche = json.loads(chemin.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        erreurs.append(f"{chemin.name} : JSON illisible ({exc})")
        return None

    exiger(fiche, ["doc_id", "fichier", "format", "emetteur", "date", "resume",
                   "demandes", "chiffres", "systemes_cites", "points_flous"], chemin.name, erreurs)
    doc_id = fiche.get("doc_id", "?")
    if not re.fullmatch(r"B0[1-9]", str(doc_id)):
        erreurs.append(f"{chemin.name} : doc_id invalide « {doc_id} »")
    if chemin.stem != doc_id:
        erreurs.append(f"{chemin.name} : le nom du fichier doit être {doc_id}.json")
    if fiche.get("format") not in FORMATS:
        erreurs.append(f"{chemin.name} : format inconnu « {fiche.get('format')} »")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fiche.get("date", ""))):
        erreurs.append(f"{chemin.name} : date attendue au format AAAA-MM-JJ")

    source = SOURCES / str(fiche.get("fichier", ""))
    texte_source = normaliser(source.read_text(encoding="utf-8")) if source.is_file() else None
    if texte_source is None:
        erreurs.append(f"{chemin.name} : fichier source introuvable « {fiche.get('fichier')} »")

    ids_vus = set()

    def verifier_element(elem: dict, prefixe: str, champs, liste: str) -> None:
        ident = elem.get("id", "?")
        ctx = f"{chemin.name} {ident}"
        exiger(elem, champs, ctx, erreurs)
        if not re.fullmatch(rf"{doc_id}-{prefixe}\d+", str(ident)):
            erreurs.append(f"{ctx} : identifiant attendu {doc_id}-{prefixe}n dans « {liste} »")
        if ident in ids_vus:
            erreurs.append(f"{ctx} : identifiant en double")
        ids_vus.add(ident)
        citation = elem.get("citation")
        if citation and texte_source is not None and normaliser(citation) not in texte_source:
            erreurs.append(f"{ctx} : citation introuvable mot pour mot dans la source")

    for d in fiche.get("demandes", []):
        verifier_element(d, "D", ["id", "type", "enonce", "citation"], "demandes")
        if d.get("type") not in TYPES_DEMANDE:
            erreurs.append(f"{chemin.name} {d.get('id')} : type inconnu « {d.get('type')} »")
        if d.get("statut_source", "demande") not in STATUTS:
            erreurs.append(f"{chemin.name} {d.get('id')} : statut_source inconnu")
    for n in fiche.get("chiffres", []):
        verifier_element(n, "N", ["id", "libelle", "valeur", "citation"], "chiffres")
    for f in fiche.get("points_flous", []):
        verifier_element(f, "F", ["id", "description"], "points_flous")

    if not fiche.get("demandes"):
        erreurs.append(f"{chemin.name} : aucune demande extraite")
    return fiche


def valider_analyse(chemin: Path, ids_fiches: set, erreurs: list) -> None:
    try:
        analyse = json.loads(chemin.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        erreurs.append(f"{chemin.name} : JSON illisible ({exc})")
        return
    exiger(analyse, ["projets", "contraintes_transverses", "conflits", "hypotheses", "questions"], chemin.name, erreurs)

    ids = {
        "P": {p.get("id") for p in analyse.get("projets", [])},
        "CT": {c.get("id") for c in analyse.get("contraintes_transverses", [])},
        "C": {c.get("id") for c in analyse.get("conflits", [])},
        "H": {h.get("id") for h in analyse.get("hypotheses", [])},
        "Q": {q.get("id") for q in analyse.get("questions", [])},
    }

    def ref_connue(ref, famille, ctx):
        if ref is not None and ref not in ids[famille]:
            erreurs.append(f"{ctx} : référence inconnue « {ref} »")

    def demande_connue(ref, ctx):
        # Ne contrôle les demandes que si les fiches sont présentes (travail en parallèle avec des données factices).
        if ids_fiches and ref not in ids_fiches:
            erreurs.append(f"{ctx} : demande « {ref} » absente des fiches")

    couverture = {}
    for p in analyse.get("projets", []):
        ctx = f"analyse {p.get('id', '?')}"
        exiger(p, ["id", "slug", "titre", "type_spec", "commanditaire", "parties_prenantes", "documents",
                   "demandes_incluses", "demandes_exclues", "contraintes", "conflits", "dependances"], ctx, erreurs)
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(p.get("slug", ""))):
            erreurs.append(f"{ctx} : slug non kebab-case")
        if p.get("type_spec") not in {"feature", "bugfix"}:
            erreurs.append(f"{ctx} : type_spec doit valoir feature ou bugfix")
        for d in p.get("demandes_incluses", []):
            demande_connue(d, ctx)
            couverture.setdefault(d, []).append(p.get("id"))
        for ex in p.get("demandes_exclues", []):
            demande_connue(ex.get("id"), ctx)
            if not ex.get("raison"):
                erreurs.append(f"{ctx} : exclusion {ex.get('id')} sans raison")
            ref_connue(ex.get("renvoi"), "P", ctx)
        for c in p.get("contraintes", []):
            ref_connue(c, "CT", ctx)
        for c in p.get("conflits", []):
            ref_connue(c, "C", ctx)
        for dep in p.get("dependances", []):
            ref_connue(dep.get("projet"), "P", ctx)

    for d, projets in couverture.items():
        if len(projets) > 1:
            erreurs.append(f"analyse : la demande {d} est incluse dans plusieurs projets {projets}")
    exclues = {ex.get("id") for p in analyse.get("projets", []) for ex in p.get("demandes_exclues", [])}
    for d in sorted(ids_fiches - set(couverture) - exclues):
        erreurs.append(f"analyse : la demande {d} n'est ni incluse ni exclue")

    for c in analyse.get("conflits", []):
        ctx = f"analyse {c.get('id', '?')}"
        exiger(c, ["id", "sujet", "positions", "gravite", "arbitre", "hypothese", "question"], ctx, erreurs)
        if c.get("gravite") not in GRAVITES:
            erreurs.append(f"{ctx} : gravité inconnue")
        if len(c.get("positions", [])) < 2:
            erreurs.append(f"{ctx} : un conflit oppose au moins deux positions")
        if c.get("hypothese") is None and c.get("gravite") in {"majeur", "mineur"}:
            erreurs.append(f"{ctx} : conflit {c.get('gravite')} sans hypothèse (null est réservé aux conflits bloquants)")
        ref_connue(c.get("hypothese"), "H", ctx)
        ref_connue(c.get("question"), "Q", ctx)
    for h in analyse.get("hypotheses", []):
        exiger(h, ["id", "enonce", "justification", "conflit", "reversible"], f"analyse {h.get('id', '?')}", erreurs)
    for q in analyse.get("questions", []):
        ctx = f"analyse {q.get('id', '?')}"
        exiger(q, ["id", "question", "destinataire", "projets", "bloquante"], ctx, erreurs)
        for p in q.get("projets", []):
            ref_connue(p, "P", ctx)


def main(args: list) -> int:
    erreurs: list = []
    if args:
        cibles = [Path(a).resolve() for a in args]
    else:
        cibles = sorted((RACINE / "work" / "fiches").glob("B0*.json"))
        if (RACINE / "work" / "analyse.json").is_file():
            cibles.append(RACINE / "work" / "analyse.json")

    ids_fiches = set()
    for f in sorted((RACINE / "work" / "fiches").glob("B0*.json")):
        try:
            fiche = json.loads(f.read_text(encoding="utf-8"))
            ids_fiches |= {d.get("id") for d in fiche.get("demandes", [])}
        except (json.JSONDecodeError, OSError):
            pass

    for cible in cibles:
        if cible.name == "analyse.json":
            valider_analyse(cible, ids_fiches, erreurs)
        else:
            valider_fiche(cible, erreurs)

    if not cibles:
        print("Aucun fichier à valider (work/fiches/ est vide).")
        return 0
    if erreurs:
        print(f"{len(erreurs)} erreur(s) :")
        for e in erreurs:
            print(f"  - {e}")
        return 1
    print(f"OK : {len(cibles)} fichier(s) conforme(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
