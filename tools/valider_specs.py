#!/usr/bin/env python3
"""Contrôles automatiques des specs de .kiro/specs/ (CONTRATS.md §4).

Usage :
    python3 tools/valider_specs.py            # toutes les specs
    python3 tools/valider_specs.py <slug>     # une spec

Vérifie : présence des fichiers, sections obligatoires, critères en EARS,
traçabilité des critères vers une source connue, couverture des exigences par les tâches.
Code de sortie 0 si tout est conforme, 1 sinon. Responsable : D.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SPECS = RACINE / ".kiro" / "specs"

EARS = re.compile(r"\b(LE SYSTÈME DOIT|QUAND|PENDANT QUE|OÙ|SI .+ALORS)\b")
CRITERE = re.compile(r"^\s*(\d+)\.\s+(.+)$")
EXIGENCE = re.compile(r"^###\s+Exigence\s+(\d+)", re.IGNORECASE)
SOURCE = re.compile(r"_Source\s*:\s*([^_]+)_")
REF_TACHE = re.compile(r"_Exigences\s*:\s*([^_]+)_")
SECTIONS_REQ = ["## Hors périmètre", "## Hypothèses", "## Questions ouvertes"]
SECTIONS_DESIGN = ["## Architecture", "## Gestion des erreurs", "## Stratégie de test"]


def ids_connus() -> set:
    """IDs déclarés dans les fiches et l'analyse ; vide si l'amont n'existe pas encore."""
    ids = set()
    for f in (RACINE / "work" / "fiches").glob("B0*.json"):
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


def valider_spec(dossier: Path, connus: set) -> list:
    erreurs = []
    nom = dossier.name
    fichier_besoin = dossier / ("bugfix.md" if (dossier / "bugfix.md").is_file() else "requirements.md")
    for f in (fichier_besoin, dossier / "design.md", dossier / "tasks.md"):
        if not f.is_file():
            erreurs.append(f"{nom} : fichier manquant {f.name}")
    if erreurs:
        return erreurs

    criteres = set()
    if fichier_besoin.name == "requirements.md":
        texte = fichier_besoin.read_text(encoding="utf-8")
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
                contenu = m.group(2)
                if not EARS.search(contenu):
                    erreurs.append(f"{nom}/requirements.md {ref} : critère non rédigé en EARS")
                s = SOURCE.search(contenu)
                if not s:
                    erreurs.append(f"{nom}/requirements.md {ref} : critère sans « _Source : …_ »")
                elif connus:
                    for src in (x.strip() for x in s.group(1).split(",")):
                        if src and src not in connus:
                            erreurs.append(f"{nom}/requirements.md {ref} : source inconnue « {src} »")
        if not criteres:
            erreurs.append(f"{nom}/requirements.md : aucun critère d'acceptation détecté")

    design = (dossier / "design.md").read_text(encoding="utf-8")
    for s in SECTIONS_DESIGN:
        if s not in design:
            erreurs.append(f"{nom}/design.md : section manquante « {s} »")

    taches = (dossier / "tasks.md").read_text(encoding="utf-8")
    if not re.search(r"^\s*- \[[ x~-]\] ", taches, re.MULTILINE):
        erreurs.append(f"{nom}/tasks.md : aucune tâche à cocher")
    couverts = set()
    for m in REF_TACHE.finditer(taches):
        for ref in (x.strip() for x in m.group(1).split(",")):
            if criteres and ref not in criteres:
                erreurs.append(f"{nom}/tasks.md : référence à un critère inexistant « {ref} »")
            couverts.add(ref)
    for ref in sorted(criteres - couverts, key=lambda r: [int(x) for x in r.split(".")]):
        erreurs.append(f"{nom} : critère {ref} couvert par aucune tâche")
    return erreurs


def main(args: list) -> int:
    if not SPECS.is_dir():
        print("Aucune spec (.kiro/specs/ absent).")
        return 0
    dossiers = [SPECS / a for a in args] if args else sorted(p for p in SPECS.iterdir() if p.is_dir())
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
