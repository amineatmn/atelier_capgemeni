#!/usr/bin/env python3
"""Aide à la relecture des fiches d'extraction (étape 1, CONTRATS.md §2).

Usage :
    python3 tools/extracteur.py verifier            # toutes les fiches de work/fiches/
    python3 tools/extracteur.py verifier B06 B09    # fiches précises

Complète tools/valider_contrats.py, qui contrôle le format. Ce script signale ce qu'une
relecture doit regarder :
  - les passages du document source qu'aucune citation ne couvre (demande oubliée ?) ;
  - les nombres du document absents de la fiche (chiffre oublié ?) ;
  - les systèmes du glossaire présents dans le document mais absents de systemes_cites ;
  - pour chaque citation introuvable, le passage le plus proche dans la source ;
  - les identifiants qui ne suivent pas l'ordre d'apparition dans le document.
Ce sont des avertissements, pas des erreurs : un passage de contexte peut rester non cité.

Code de sortie : 0 rien à signaler, 1 avertissements, 2 fiche ou source illisible.
Aucune dépendance externe. Responsable : A.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import io
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / "challenge-b"
FICHES = RACINE / "work" / "fiches"
GLOSSAIRE = RACINE / ".kiro" / "steering" / "glossaire-orvanne.md"

MOTS_MIN_NON_COUVERT = 6  # en dessous, un passage non cité n'est pas signalé

# Lignes d'en-tête déjà reprises dans l'identité de la fiche (emetteur, date…).
LIGNE_META = re.compile(
    r"^\s*(\[.*\]|De\s*:|À\s*:|Pour\s*:|Cc\s*:|Date\s*:|Objet\s*:|Diffusion\s*:|Canal\s*:|"
    r"Reçu le|Référence\s*:|Rédaction\s*:|Participants\s*:|présents\s*:|excusée?\s*:|"
    r"\|\s*-+|\|\s*Champ\s*\||\|\s*Id\s*\||\|\s*Action\s*\|)",
    re.IGNORECASE,
)
NOMBRE = re.compile(r"(?<![\w-])(?:J[+-])?\d+(?:[ \u00a0\u202f]\d{3})*(?:[.,]\d+)?(?:\s?%)?")
NOMBRES_EN_LETTRES = re.compile(
    r"\b(?:une?\s+)?(?:deux|trois|quatre|cinq|six|sept|huit|neuf|dix(?:-sept|-huit|-neuf)?|onze|douze|quinze|"
    r"vingt|trente|quarante|cinquante|soixante|cent|mille|dizaine|vingtaine|trentaine|quarantaine|"
    r"cinquantaine|soixantaine|centaine|double|triple|moitié|tiers|quart)s?\b",
    re.IGNORECASE,
)


# --- Texte normalisé avec correspondance vers le texte brut ------------------------------------

def normaliser_avec_index(texte: str) -> tuple[str, list[int]]:
    """Même normalisation que valider_contrats.normaliser, en gardant la position d'origine
    de chaque caractère, pour savoir quelle partie du texte brut une citation couvre."""
    sortie, index = [], []
    espace = False
    for i, c in enumerate(texte):
        if c in "\u00a0\u202f" or c.isspace():
            espace = True
            continue
        if espace and sortie:
            sortie.append(" ")
            index.append(i - 1)
        espace = False
        c = "'" if c == "\u2019" else c.lower()
        sortie.extend(c)
        index.extend([i] * len(c))
    return "".join(sortie), index


def normaliser(texte: str) -> str:
    return normaliser_avec_index(texte)[0]


# --- Lecture ------------------------------------------------------------------------------------

def charger_systemes() -> dict[str, list[str]]:
    """Nom canonique -> formes à chercher, depuis le tableau « Systèmes d'information » du glossaire."""
    systemes: dict[str, list[str]] = {}
    if not GLOSSAIRE.is_file():
        return systemes
    dans_tableau = False
    for ligne in GLOSSAIRE.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("## "):
            dans_tableau = ligne.startswith("## Systèmes")
            continue
        if not dans_tableau or not ligne.startswith("|") or re.match(r"^\|\s*(-|Nom\s*\|)", ligne):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        nom = cellules[0]
        variantes = [v.strip() for v in cellules[2].split(",")] if len(cellules) >= 4 else []
        formes = {re.sub(r"^(le|la|les|l')\s*", "", nom, flags=re.IGNORECASE)} | {v for v in variantes if v}
        systemes[nom] = sorted(formes)
    return systemes


def lignes_a_couvrir(texte: str, fichier: str) -> list[tuple[int, int]]:
    """(début, fin) dans le texte brut des lignes dont le contenu devrait être cité."""
    plages, pos = [], 0
    est_csv = fichier.endswith(".csv")
    for n, ligne in enumerate(texte.splitlines(keepends=True)):
        debut, fin = pos, pos + len(ligne.rstrip("\r\n"))
        pos += len(ligne)
        if not ligne.strip() or LIGNE_META.match(ligne) or (est_csv and n == 0):
            continue
        if est_csv:
            # Seules les colonnes de texte comptent : on saute ref et date_demande.
            separateurs = [m.start() for m in re.finditer(";", ligne)]
            if len(separateurs) >= 2:
                debut += separateurs[1] + 1
        plages.append((debut, fin))
    return plages


def texte_hors_colonnes_csv(texte: str) -> str:
    """Pour la recherche des nombres dans un CSV : on ignore ref et date_demande."""
    lignes = list(csv.reader(io.StringIO(texte), delimiter=";"))
    return "\n".join(";".join(l[2:]) for l in lignes[1:])


# --- Contrôles ----------------------------------------------------------------------------------

def elements_cites(fiche: dict) -> list[tuple[str, str, str]]:
    """(id, famille, citation) pour les demandes, chiffres et points flous."""
    out = []
    for famille in ("demandes", "chiffres", "points_flous"):
        for e in fiche.get(famille, []):
            if e.get("citation"):
                out.append((str(e.get("id", "?")), famille, e["citation"]))
    return out


def champs_recopies(fiche: dict) -> list[str]:
    """priorite_exprimee et echeance_exprimee : recopiées du document, elles couvrent leur passage."""
    return [v for d in fiche.get("demandes", [])
            for v in (d.get("priorite_exprimee"), d.get("echeance_exprimee")) if isinstance(v, str) and v]


def passage_le_plus_proche(citation: str, source_norm: str) -> tuple[str, float]:
    cit = normaliser(citation)
    sm = difflib.SequenceMatcher(None, source_norm, cit, autojunk=False)
    m = sm.find_longest_match(0, len(source_norm), 0, len(cit))
    debut = max(0, m.a - m.b)
    candidat = source_norm[debut:debut + len(cit) + 10]
    ratio = difflib.SequenceMatcher(None, candidat, cit, autojunk=False).ratio()
    return candidat.strip(), ratio


def hors_sequence(elements: list[tuple[str, int]]) -> list[str]:
    """Identifiants à déplacer pour que les positions soient croissantes (complément de la plus
    longue sous-suite croissante) : on désigne le moins d'éléments possible."""
    n = len(elements)
    longueur, precedent = [1] * n, [-1] * n
    for i in range(n):
        for j in range(i):
            if elements[j][1] <= elements[i][1] and longueur[j] + 1 > longueur[i]:
                longueur[i], precedent[i] = longueur[j] + 1, j
    garde, i = set(), (max(range(n), key=longueur.__getitem__) if n else -1)
    while i >= 0:
        garde.add(i)
        i = precedent[i]
    return [elements[k][0] for k in range(n) if k not in garde]


def verifier_fiche(chemin: Path) -> tuple[list[str], bool]:
    """Retourne (avertissements, erreur bloquante)."""
    try:
        fiche = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"fiche illisible ({exc})"], True
    source_path = SOURCES / str(fiche.get("fichier", ""))
    if not source_path.is_file():
        return [f"source introuvable « {fiche.get('fichier')} »"], True
    texte = source_path.read_text(encoding="utf-8")
    source_norm, index = normaliser_avec_index(texte)
    alertes: list[str] = []

    # 1. Citations : position dans la source, citations introuvables.
    couvert = [False] * len(texte)
    positions: dict[str, int] = {}
    for ident, famille, citation in elements_cites(fiche):
        cit = normaliser(citation)
        p = source_norm.find(cit) if cit else -1
        if p < 0:
            proche, ratio = passage_le_plus_proche(citation, source_norm)
            alertes.append(f"[citation] {ident} introuvable. Passage le plus proche ({ratio:.0%}) : « {proche} »")
            continue
        positions[ident] = index[p]
        while p >= 0:
            for i in range(index[p], index[p + len(cit) - 1] + 1):
                couvert[i] = True
            p = source_norm.find(cit, p + 1)

    for valeur in champs_recopies(fiche):
        cit = normaliser(valeur)
        p = source_norm.find(cit) if len(cit) >= 4 else -1
        while p >= 0:
            for i in range(index[p], index[p + len(cit) - 1] + 1):
                couvert[i] = True
            p = source_norm.find(cit, p + 1)

    # 2. Passages non cités.
    for debut, fin in lignes_a_couvrir(texte, source_path.name):
        i = debut
        while i < fin:
            if couvert[i]:
                i += 1
                continue
            j = i
            while j < fin and not couvert[j]:
                j += 1
            morceau = texte[i:j].strip(" ;|-*#\t")
            if len(re.findall(r"\w+", morceau)) >= MOTS_MIN_NON_COUVERT:
                alertes.append(f"[non cité] « {morceau} »")
            i = j

    # 3. Nombres absents de la fiche.
    texte_nombres = texte_hors_colonnes_csv(texte) if source_path.suffix == ".csv" else "\n".join(
        l for l in texte.splitlines() if not LIGNE_META.match(l))
    fiche_norm = normaliser(json.dumps(fiche, ensure_ascii=False))
    fiche_chiffres = normaliser(" ".join(
        f"{n.get('valeur', '')} {n.get('citation', '')} {n.get('libelle', '')}" for n in fiche.get("chiffres", [])))
    vus = set()
    for m in list(NOMBRE.finditer(texte_nombres)) + list(NOMBRES_EN_LETTRES.finditer(texte_nombres)):
        brut = m.group(0).strip()
        debut_ligne = texte_nombres.rfind("\n", 0, m.start()) + 1
        if not texte_nombres[debut_ligne:m.start()].strip() and texte_nombres[m.end():m.end() + 1] in (".", ")"):
            continue
        cle = normaliser(brut)
        if cle in vus:
            continue
        vus.add(cle)
        if cle in fiche_chiffres:
            continue
        compact = re.sub(r"[ %]", "", cle)
        if compact and compact in fiche_chiffres.replace(" ", ""):
            continue
        contexte = normaliser(texte_nombres[max(0, m.start() - 40):m.end() + 40])
        ou = "ailleurs dans la fiche" if cle in fiche_norm else "absent de la fiche"
        alertes.append(f"[chiffre] « {brut} » hors de chiffres ({ou}) : … {contexte} …")

    # 4. Systèmes du glossaire.
    cites = {normaliser(s) for s in fiche.get("systemes_cites", [])}
    for nom, formes in charger_systemes().items():
        trouve = any(re.search(rf"(?<!\w){re.escape(normaliser(f))}(?!\w)", source_norm) for f in formes)
        if trouve and normaliser(nom) not in cites:
            alertes.append(f"[système] « {nom} » apparaît dans le document mais pas dans systemes_cites")

    # 5. Ordre des identifiants.
    for famille, lettre in (("demandes", "D"), ("chiffres", "N"), ("points_flous", "F")):
        elements = fiche.get(famille, [])
        numeros = [int(m.group(1)) for e in elements
                   if (m := re.fullmatch(rf"B0\d-{lettre}(\d+)", str(e.get("id", ""))))]
        if numeros and numeros != list(range(1, len(numeros) + 1)):
            alertes.append(f"[ordre] {famille} : numérotation avec trous ou désordre {numeros}")
        if famille == "demandes":
            hors_ordre = hors_sequence([(str(e.get("id")), positions[str(e.get("id"))])
                                        for e in elements if str(e.get("id")) in positions])
            if hors_ordre:
                alertes.append("[ordre] demandes hors de l'ordre d'apparition dans le document : "
                               + ", ".join(hors_ordre))
    return alertes, False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Aide à la relecture des fiches d'extraction.")
    sous = parser.add_subparsers(dest="commande", required=True)
    v = sous.add_parser("verifier", help="signale les manques probables d'une ou plusieurs fiches")
    v.add_argument("docs", nargs="*", help="B01 … B09 (par défaut : toutes les fiches présentes)")
    args = parser.parse_args(argv)

    cibles = [FICHES / f"{d.upper()}.json" for d in args.docs] or sorted(FICHES.glob("B0*.json"))
    if not cibles:
        print("Aucune fiche dans work/fiches/.")
        return 0
    code = 0
    for chemin in cibles:
        alertes, bloquant = verifier_fiche(chemin)
        print(f"\n== {chemin.stem} : {len(alertes)} point(s) à relire")
        for a in alertes:
            print(f"  - {a}")
        code = max(code, 2 if bloquant else (1 if alertes else 0))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
