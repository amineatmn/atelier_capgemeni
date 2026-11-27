#!/usr/bin/env python3
"""Contrôles automatiques des specs de .kiro/specs/ (CONTRATS.md §4).

Usage :
    python3 tools/valider_specs.py            # toutes les specs
    python3 tools/valider_specs.py <slug>     # une spec de .kiro/specs/
    python3 tools/valider_specs.py <dossier>  # n'importe quel dossier de spec (ex. templates/exemple-p01)

Vérifie : présence des fichiers, sections obligatoires, critères en EARS,
traçabilité des critères vers une source connue, couverture des exigences par les tâches,
présence de « _Exigences : …_ » sur chaque tâche terminale.

Spec bugfix (bugfix.md à la place de requirements.md, format provisoire en attendant le modèle de C) :
sections « Comportement actuel », « Comportement attendu » et « Comportement inchangé » ;
leurs items numérotés sont les critères 1.n, 2.n et 3.n, que les tâches référencent.
Les critères attendus et inchangés sont rédigés en EARS.
Code de sortie 0 si tout est conforme, 1 sinon. Responsable : D.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SPECS = RACINE / ".kiro" / "specs"

# Toutes les formes EARS de format-spec.md contiennent « LE SYSTÈME DOIT » (forme négative admise).
EARS = re.compile(r"\bLE SYSTÈME (?:NE )?DOIT\b")
SI_SANS_ALORS = re.compile(r"^SI\b(?!.*\bALORS\b)")
CRITERE = re.compile(r"^\s*(\d+)\.\s+(.+)$")
CRITERE_EXPLICITE = re.compile(r"^\s*(\d+\.\d+)\.?\s+(.+)$")
EXIGENCE = re.compile(r"^###\s+Exigence\s+(\d+)", re.IGNORECASE)
TITRE = re.compile(r"^(#+)\s+(.*)$")
SOURCE = re.compile(r"_Source\s*:\s*([^_]+)_")
REF_TACHE = re.compile(r"_Exigences\s*:\s*([^_]+)_")
CASE = re.compile(r"^\s*- \[[ x~-]\] ")
TACHE = re.compile(r"^\s*- \[[ x~-]\] (\d+(?:\.\d+)*)\.?\s")
SECTIONS_REQ = ["## Hors périmètre", "## Hypothèses", "## Questions ouvertes"]
SECTIONS_BUGFIX = ["Comportement actuel", "Comportement attendu", "Comportement inchangé"]
SECTIONS_DESIGN = ["## Architecture", "## Gestion des erreurs", "## Stratégie de test"]


def ids_connus() -> set:
    """IDs déclarés dans les fiches et l'analyse ; vide si l'amont n'existe pas encore."""
    ids = set()
    for f in (RACINE / "work" / "fiches").glob("B[0-9][0-9].json"):
        try:
            fiche = json.loads(f.read_text(encoding="utf-8"))
            ids |= {d.get("id") for d in fiche.get("demandes", [])}
        except (json.JSONDecodeError, OSError):
            pass
    analyse = RACINE / "work" / "analyse.json"
    if analyse.is_file():
        try:
            a = json.loads(analyse.read_text(encoding="utf-8"))
            for cle in ("contraintes_transverses", "hypotheses"):
                ids |= {x.get("id") for x in a.get(cle, [])}
        except (json.JSONDecodeError, OSError):
            pass
    return ids


def verifier_critere(lieu: str, contenu: str, connus: set, ears: bool, erreurs: list) -> None:
    if ears and not EARS.search(contenu):
        erreurs.append(f"{lieu} : critère non rédigé en EARS (« LE SYSTÈME DOIT » absent)")
    if ears and SI_SANS_ALORS.search(contenu):
        erreurs.append(f"{lieu} : « SI » sans « ALORS »")
    s = SOURCE.search(contenu)
    if not s:
        erreurs.append(f"{lieu} : critère sans « _Source : …_ »")
    elif connus:
        for src in (x.strip() for x in s.group(1).split(",")):
            if src and src not in connus:
                erreurs.append(f"{lieu} : source inconnue « {src} »")


def criteres_requirements(nom: str, texte: str, connus: set, erreurs: list) -> set:
    criteres = set()
    for s in SECTIONS_REQ:
        if s not in texte:
            erreurs.append(f"{nom}/requirements.md : section manquante « {s} »")
    exigence = None
    dans_criteres = False
    for ligne in texte.splitlines():
        m = EXIGENCE.match(ligne)
        if m:
            exigence, dans_criteres = m.group(1), False
            continue
        if ligne.startswith("## "):
            exigence = None
        if ligne.startswith("#### "):
            dans_criteres = "critère" in ligne.lower()
            continue
        m = CRITERE.match(ligne)
        if exigence and dans_criteres and m:
            ref = f"{exigence}.{m.group(1)}"
            criteres.add(ref)
            verifier_critere(f"{nom}/requirements.md {ref}", m.group(2), connus, True, erreurs)
    return criteres


def section_bugfix(titre: str):
    """Rang (1, 2, 3) de la section bugfix correspondant au titre, sinon None."""
    titre = titre.strip().lower()
    return next((i for i, s in enumerate(SECTIONS_BUGFIX, 1) if titre.startswith(s.lower())), None)


def criteres_bugfix(nom: str, texte: str, connus: set, erreurs: list) -> set:
    criteres = set()
    trouvees = set()
    section = None
    for ligne in texte.splitlines():
        t = TITRE.match(ligne)
        if t:
            rang = section_bugfix(t.group(2))
            if rang:
                trouvees.add(rang)
            # Un sous-titre (###) quelconque ne fait pas sortir de la section en cours.
            if rang or len(t.group(1)) <= 2:
                section = rang
            continue
        if section is None:
            continue
        m = CRITERE_EXPLICITE.match(ligne)
        if m:
            ref, contenu = m.group(1), m.group(2)
        else:
            m = CRITERE.match(ligne)
            if not m:
                continue
            ref, contenu = f"{section}.{m.group(1)}", m.group(2)
        criteres.add(ref)
        # Le comportement actuel décrit le défaut : pas de « LE SYSTÈME DOIT » attendu.
        verifier_critere(f"{nom}/bugfix.md {ref}", contenu, connus, section > 1, erreurs)
    for rang, s in enumerate(SECTIONS_BUGFIX, 1):
        if rang not in trouvees:
            erreurs.append(f"{nom}/bugfix.md : section manquante « {s} »")
    return criteres


def verifier_taches(nom: str, taches: str, criteres: set, erreurs: list) -> None:
    lignes = taches.splitlines()
    if not any(CASE.match(l) for l in lignes):
        erreurs.append(f"{nom}/tasks.md : aucune tâche à cocher")
    positions = []
    for i, ligne in enumerate(lignes):
        if CASE.match(ligne):
            m = TACHE.match(ligne)
            if m:
                positions.append((i, m.group(1)))
            else:
                erreurs.append(f"{nom}/tasks.md ligne {i + 1} : tâche non numérotée")
    idents = [ident for _, ident in positions]
    for k, (debut, ident) in enumerate(positions):
        fin = positions[k + 1][0] if k + 1 < len(positions) else len(lignes)
        terminale = not any(autre.startswith(ident + ".") for autre in idents)
        if terminale and not REF_TACHE.search("\n".join(lignes[debut:fin])):
            erreurs.append(f"{nom}/tasks.md : tâche {ident} sans « _Exigences : …_ »")

    couverts = set()
    for m in REF_TACHE.finditer(taches):
        for ref in (x.strip() for x in m.group(1).split(",")):
            if criteres and ref not in criteres:
                erreurs.append(f"{nom}/tasks.md : référence à un critère inexistant « {ref} »")
            couverts.add(ref)
    for ref in sorted(criteres - couverts, key=lambda r: [int(x) for x in r.split(".")]):
        erreurs.append(f"{nom} : critère {ref} couvert par aucune tâche")


def valider_spec(dossier: Path, connus: set) -> list:
    erreurs = []
    nom = dossier.name
    fichier_besoin = dossier / ("bugfix.md" if (dossier / "bugfix.md").is_file() else "requirements.md")
    for f in (fichier_besoin, dossier / "design.md", dossier / "tasks.md"):
        if not f.is_file():
            erreurs.append(f"{nom} : fichier manquant {f.name}")
    if erreurs:
        return erreurs

    texte = fichier_besoin.read_text(encoding="utf-8")
    if fichier_besoin.name == "requirements.md":
        criteres = criteres_requirements(nom, texte, connus, erreurs)
    else:
        criteres = criteres_bugfix(nom, texte, connus, erreurs)
    if not criteres:
        erreurs.append(f"{nom}/{fichier_besoin.name} : aucun critère d'acceptation détecté")

    design = (dossier / "design.md").read_text(encoding="utf-8")
    for s in SECTIONS_DESIGN:
        if s not in design:
            erreurs.append(f"{nom}/design.md : section manquante « {s} »")

    verifier_taches(nom, (dossier / "tasks.md").read_text(encoding="utf-8"), criteres, erreurs)
    return erreurs


def main(args: list) -> int:
    if not args and not SPECS.is_dir():
        print("Aucune spec (.kiro/specs/ absent).")
        return 0
    dossiers = ([Path(a) if Path(a).is_dir() else SPECS / a for a in args] if args
                else sorted(p for p in SPECS.iterdir() if p.is_dir()))
    connus = ids_connus()
    total = 0
    for d in dossiers:
        erreurs = valider_spec(d, connus)
        total += len(erreurs)
        print(f"[{'OK' if not erreurs else 'À corriger'}] {d.name}")
        for e in erreurs:
            print(f"  - {e}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
