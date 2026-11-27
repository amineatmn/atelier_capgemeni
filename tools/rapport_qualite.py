#!/usr/bin/env python3
"""Génère work/rapport-qualite.md (étape 4, CONTRATS.md §5).

Usage :
    python3 tools/rapport_qualite.py

Pour chaque spec : résultat de tools/valider_specs.py, couverture des demandes du projet,
des conflits (hypothèse citée), des contraintes transverses et des questions bloquantes.
Ensuite : couverture de la référence humaine work/exemples/conflits-attendus.md par l'analyse.
Aucune dépendance externe. Responsable : D.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SPECS = RACINE / ".kiro" / "specs"
SORTIE = RACINE / "work" / "rapport-qualite.md"
ID_DEMANDE = re.compile(r"B0\d-D\d+(?!\d)")

# Correspondance établie à la lecture entre la référence humaine (Rnn) et l'analyse.
# Valeur : (éléments de work/analyse.json qui la traitent, couverture : oui / partiel / non, commentaire).
REFERENCE = {
    "R01": (["C01"], "oui", ""), "R02": (["C02"], "oui", ""), "R03": (["C04"], "oui", ""),
    "R04": (["C04"], "partiel", "La propriété des messages (logistique ou service client) n'est traitée que sous l'angle du contrôle des envois."),
    "R05": (["C03"], "oui", ""), "R06": (["C07"], "oui", ""),
    "R07": (["C09"], "oui", ""), "R08": (["C10"], "oui", ""), "R09": (["C08"], "oui", ""),
    "R10": (["C11"], "oui", ""), "R11": (["C13"], "oui", ""), "R12": (["C12"], "oui", ""),
    "R13": (["CT-06"], "partiel", "Traité comme contrainte transverse, sans conflit explicite entre EF-09 et la DPO."),
    "R14": (["C15"], "oui", ""), "R15": (["C14"], "oui", ""),
    "R16": ([], "non", "Le bon d'achat majoré de 5 % (B04) n'apparaît ni en conflit ni en hypothèse."),
    "R17": (["C16"], "oui", ""),
    "R18": (["H11", "Q37"], "partiel", "La note A / B / C est traitée, pas le choix du périmètre « casse seule ou casse et retours »."),
    "R19": (["C17"], "oui", ""),
    "R20": (["C20"], "oui", ""), "R21": (["C19"], "oui", ""), "R22": (["C18"], "oui", ""),
    "R23": (["Q33"], "partiel", "Les plafonds de remise sont une question, pas un conflit."),
    "R24": (["C21"], "oui", ""), "R25": (["C22"], "oui", ""), "R26": (["C23"], "oui", ""), "R27": (["C24"], "oui", ""),
    "R28": (["C26"], "oui", ""), "R29": (["C25"], "oui", ""),
    "R30": ([], "non", "L'hétérogénéité des priorités de B09 n'est relevée que dans la fiche (point flou)."),
    "R31": (["C11"], "partiel", "Le suivi des retours par les vendeurs (MKP-06) est lié au conflit sur les retours marketplace."),
    "R32": (["C02", "C26"], "partiel", "Les sens du mot « retard » sont traités projet par projet, pas comme une définition commune."),
    "R33": (["CT-01"], "oui", "Traité comme contrainte transverse sur tous les projets."),
    "R34": (["H08", "Q04", "Q09"], "partiel", "La relation entre Premium et Orvanne+ est posée en question."),
}


def charger_analyse() -> dict:
    return json.loads((RACINE / "work" / "analyse.json").read_text(encoding="utf-8"))


def resultat_validateur() -> dict:
    sortie = subprocess.run([sys.executable, str(RACINE / "tools" / "valider_specs.py")],
                            capture_output=True, text=True, cwd=RACINE).stdout
    res, courant = {}, None
    for ligne in sortie.splitlines():
        m = re.match(r"\[(.+?)\] (.+)$", ligne)
        if m:
            courant = m.group(2)
            res[courant] = [m.group(1)]
        elif courant and ligne.strip().startswith("- "):
            res[courant].append(ligne.strip()[2:])
    return res


def controler_spec(p: dict, a: dict, valid: dict) -> dict:
    dossier = SPECS / p["slug"]
    fichiers = {f.name: f.read_text(encoding="utf-8") for f in dossier.glob("*.md")}
    texte = "".join(fichiers.values())
    besoin = fichiers.get("bugfix.md") or fichiers.get("requirements.md", "")
    cites = set(ID_DEMANDE.findall(texte))
    attendues = p["demandes_incluses"] + [e["id"] for e in p["demandes_exclues"]]
    conflits = [c for c in a["conflits"] if c["id"] in p["conflits"]]
    constats = []
    for d in attendues:
        if d not in cites:
            constats.append(f"Demande `{d}` absente de la spec.")
    sans_hyp = [c for c in conflits if c["hypothese"] and not re.search(rf"\b{c['hypothese']}\b", texte)]
    for c in sans_hyp:
        constats.append(f"Conflit `{c['id']}` ({c['sujet']}) : hypothèse `{c['hypothese']}` non citée.")
    for ct in p["contraintes"]:
        if not re.search(rf"\b{ct}\b", texte):
            constats.append(f"Contrainte `{ct}` applicable mais non citée.")
    for q in a["questions"]:
        if q["bloquante"] and p["id"] in q["projets"] and q["id"] not in texte and q["question"][:40] not in texte:
            constats.append(f"Question bloquante `{q['id']}` non reprise.")
    if "## Volumétrie" not in fichiers.get("design.md", "") and p["type_spec"] == "feature":
        constats.append("design.md sans section « Volumétrie et performance ».")
    statut_valid = valid.get(p["slug"], ["absente"])
    verdict = "OK" if statut_valid[0] == "OK" and not constats else "À corriger"
    if any(q["bloquante"] and p["id"] in q["projets"] for q in a["questions"]):
        verdict += " (question bloquante ouverte)"
    return {
        "verdict": verdict, "valid": statut_valid,
        "criteres": len(re.findall(r"^\d+\. ", besoin, re.M)),
        "taches": len(re.findall(r"^\s*- \[ \] \d+\.\d+", fichiers.get("tasks.md", ""), re.M)),
        "demandes": f"{len([d for d in attendues if d in cites])}/{len(attendues)}",
        "conflits": f"{len(conflits) - len(sans_hyp)}/{len(conflits)}",
        "constats": constats,
    }


def main() -> int:
    a = charger_analyse()
    valid = resultat_validateur()
    lignes = ["# Rapport qualité", "",
              "Généré par `tools/rapport_qualite.py`. Contrôles automatiques : `tools/valider_specs.py` (structure, EARS, "
              "sources existantes, couverture des critères par les tâches) et couverture de l'analyse (demandes, conflits, "
              "contraintes, questions bloquantes).", "",
              "## Synthèse par spec", "",
              "| Projet | Spec | Type | Validateur | Critères | Sous-tâches | Demandes citées | Conflits avec hypothèse citée | Verdict |",
              "|---|---|---|---|---|---|---|---|---|"]
    details = []
    for p in a["projets"]:
        r = controler_spec(p, a, valid)
        lignes.append(f"| {p['id']} | `{p['slug']}` | {p['type_spec']} | {r['valid'][0]} | {r['criteres']} | {r['taches']} | "
                      f"{r['demandes']} | {r['conflits']} | {r['verdict']} |")
        details += [f"### {p['id']} {p['titre']}", ""]
        details += [f"- {c}" for c in r["valid"][1:] + r["constats"]] or ["- Aucun constat."]
        qb = [q for q in a["questions"] if q["bloquante"] and p["id"] in q["projets"]]
        for q in qb:
            details.append(f"- Question bloquante `{q['id']}` ({q['destinataire']}) : {q['question']}")
        details.append("")
    lignes += ["", "## Détail par spec", ""] + details

    ok = sum(1 for v in REFERENCE.values() if v[1] == "oui")
    part = sum(1 for v in REFERENCE.values() if v[1] == "partiel")
    lignes += ["## Couverture de la référence humaine des conflits", "",
               f"Référence : `work/exemples/conflits-attendus.md` ({len(REFERENCE)} conflits attendus). "
               f"Couverts : {ok}, partiellement : {part}, non couverts : {len(REFERENCE) - ok - part}.", "",
               "| Réf. | Traité par | Couverture | Commentaire |", "|---|---|---|---|"]
    for ref, (ids, cov, com) in REFERENCE.items():
        lignes.append(f"| {ref} | {', '.join(ids) or '—'} | {cov} | {com} |")
    lignes += ["", "## Limites", "",
               "- Les contrôles vérifient la présence et la cohérence des références, pas la justesse métier de chaque critère : "
               "une relecture humaine des specs reste nécessaire avant développement.",
               "- La correspondance avec la référence humaine a été établie à la lecture ; elle est à revoir si l'analyse est régénérée.", ""]
    SORTIE.write_text("\n".join(lignes), encoding="utf-8")
    print(f"Rapport écrit : {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
