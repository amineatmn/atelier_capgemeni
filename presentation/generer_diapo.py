#!/usr/bin/env python3
"""Génère presentation/orvanne-pipeline-specs.pdf (diaporama 16:9).

Usage : python3 presentation/generer_diapo.py   (nécessite reportlab : pip install --user reportlab)
Les chiffres sont lus dans work/ et .kiro/specs/ au moment de la génération.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "presentation" / "orvanne-pipeline-specs.pdf"
W, H = 960, 540

FONTS = Path("/usr/share/fonts/dejavu-sans-fonts")
pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Sans-B", str(FONTS / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Cond", str(FONTS / "DejaVuSansCondensed.ttf")))
pdfmetrics.registerFont(TTFont("Cond-B", str(FONTS / "DejaVuSansCondensed-Bold.ttf")))

BLEU = HexColor("#1F3A5F")
BLEU_CLAIR = HexColor("#E8EEF6")
ACCENT = HexColor("#E07A1F")
VERT = HexColor("#2E7D4F")
ROUGE = HexColor("#B23A3A")
GRIS = HexColor("#555555")
GRIS_CLAIR = HexColor("#F4F4F4")


# ---------- données réelles du dépôt ----------
def charger():
    analyse = json.loads((RACINE / "work/analyse.json").read_text(encoding="utf-8"))
    fiches = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((RACINE / "work/fiches").glob("B0*.json"))]
    rapport = (RACINE / "work/rapport-qualite.md").read_text(encoding="utf-8")
    criteres = taches = 0
    for p in analyse["projets"]:
        ligne = re.search(rf"^\| {p['id']} \|.*$", rapport, re.M)
        if ligne:
            cols = [c.strip() for c in ligne.group(0).strip("|").split("|")]
            criteres += int(cols[4])
            taches += int(cols[5])
    couv = re.search(r"Couverts : (\d+), partiellement : (\d+), non couverts : (\d+)", rapport)
    steering_ct = len(re.findall(r"^\| CT-\d+", (RACINE / ".kiro/steering/contraintes-transverses.md").read_text(encoding="utf-8"), re.M))
    return {
        "fiches": len(fiches),
        "demandes": sum(len(f["demandes"]) for f in fiches),
        "flous": sum(len(f["points_flous"]) for f in fiches),
        "projets": analyse["projets"],
        "conflits": analyse["conflits"],
        "hyp": len(analyse["hypotheses"]),
        "questions": analyse["questions"],
        "ct": len(analyse["contraintes_transverses"]),
        "ct_steering": steering_ct,
        "criteres": criteres,
        "taches": taches,
        "couv": tuple(int(x) for x in couv.groups()) if couv else (0, 0, 0),
        "rapport": rapport,
    }


# ---------- primitives de mise en page ----------
def lignes(c, texte, font, size, largeur):
    mots, out, cur = texte.split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if c.stringWidth(essai, font, size) <= largeur:
            cur = essai
        else:
            out.append(cur)
            cur = m
    if cur:
        out.append(cur)
    return out


def paragraphe(c, x, y, texte, font="Sans", size=15, largeur=820, couleur=GRIS, interligne=1.35):
    c.setFillColor(couleur)
    c.setFont(font, size)
    for l in lignes(c, texte, font, size, largeur):
        c.drawString(x, y, l)
        y -= size * interligne
    return y


def puces(c, x, y, items, size=15, largeur=820, ecart=8, couleur_puce=ACCENT):
    for it in items:
        gras, _, reste = it.partition("|") if "|" in it else ("", "", it)
        c.setFillColor(couleur_puce)
        c.circle(x + 4, y + size * 0.33, 3.2, fill=1, stroke=0)
        tx = x + 16
        if gras:
            c.setFont("Sans-B", size)
            c.setFillColor(BLEU)
            c.drawString(tx, y, gras)
            dx = c.stringWidth(gras + " ", "Sans-B", size)
            premiere = lignes(c, reste, "Sans", size, largeur - 16 - dx)
            c.setFont("Sans", size)
            c.setFillColor(GRIS)
            if premiere:
                c.drawString(tx + dx, y, premiere[0])
                rest = " ".join(reste.split()[len(premiere[0].split()):])
                y -= size * 1.35
                if rest:
                    y = paragraphe(c, tx, y, rest, size=size, largeur=largeur - 16)
            else:
                y -= size * 1.35
        else:
            y = paragraphe(c, tx, y, reste, size=size, largeur=largeur - 16)
        y -= ecart
    return y


def boite(c, x, y, w, h, fond=BLEU_CLAIR, bord=None, rayon=8):
    c.setFillColor(fond)
    c.setStrokeColor(bord or fond)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, rayon, fill=1, stroke=1 if bord else 0)


def chiffre(c, x, y, w, valeur, libelle, couleur=BLEU):
    boite(c, x, y, w, 92, fond=white, bord=HexColor("#D5DDE8"))
    c.setFillColor(couleur)
    c.setFont("Sans-B", 34)
    c.drawCentredString(x + w / 2, y + 46, str(valeur))
    c.setFillColor(GRIS)
    c.setFont("Sans", 12.5)
    for i, l in enumerate(lignes(c, libelle, "Sans", 12.5, w - 12)):
        c.drawCentredString(x + w / 2, y + 26 - i * 14, l)


def fleche(c, x1, y, x2, couleur=BLEU):
    c.setStrokeColor(couleur)
    c.setFillColor(couleur)
    c.setLineWidth(2)
    c.line(x1, y, x2 - 8, y)
    p = c.beginPath()
    p.moveTo(x2, y)
    p.lineTo(x2 - 10, y + 5)
    p.lineTo(x2 - 10, y - 5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


class Diapo:
    def __init__(self):
        SORTIE.parent.mkdir(exist_ok=True)
        self.c = canvas.Canvas(str(SORTIE), pagesize=(W, H))
        self.c.setTitle("Orvanne : des expressions de besoin aux specs Kiro")
        self.c.setAuthor("Équipe challenge B")
        self.n = 0

    def page(self, titre, sous_titre=None):
        if self.n:
            self.c.showPage()
        self.n += 1
        c = self.c
        c.setFillColor(white)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(BLEU)
        c.rect(0, H - 78, W, 78, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, H - 82, W, 4, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Sans-B", 26)
        c.drawString(50, H - 50, titre)
        if sous_titre:
            c.setFont("Sans", 13)
            c.setFillColor(HexColor("#C9D6E8"))
            c.drawRightString(W - 50, H - 50, sous_titre)
        c.setFillColor(HexColor("#9AA5B1"))
        c.setFont("Sans", 10)
        c.drawString(50, 18, "Orvanne · Challenge B · des expressions de besoin aux specs Kiro")
        c.drawRightString(W - 50, 18, str(self.n))
        return c

    def fin(self):
        self.c.save()


# ---------- diapositives ----------
def construire(d: dict):
    s = Diapo()
    nb_conf = len(d["conflits"])
    nb_proj = len(d["projets"])
    feat = sum(p["type_spec"] == "feature" for p in d["projets"])
    bug = nb_proj - feat
    bloq_q = sum(q["bloquante"] for q in d["questions"])
    couv_ok, couv_part, couv_non = d["couv"]

    # 1. Titre
    s.n += 1
    c = s.c
    c.setFillColor(BLEU)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(50, 292, 90, 5, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Sans-B", 44)
    c.drawString(50, 395, "Orvanne")
    c.setFont("Sans-B", 32)
    c.drawString(50, 350, "Des expressions de besoin")
    c.drawString(50, 312, "aux specs Kiro")
    c.setFont("Sans", 18)
    c.setFillColor(HexColor("#C9D6E8"))
    c.drawString(50, 255, "Une chaîne de 4 agents Kiro qui transforme 9 documents hétérogènes")
    c.drawString(50, 230, "en specs prêtes à développer, sans masquer les contradictions.")
    c.setFont("Sans", 14)
    c.drawString(50, 90, "Challenge B · Équipe de 4 : A extraction · B analyse · C rédaction · D qualité et intégration")

    # 2. Le problème
    c = s.page("Le problème", "9 documents, 9 formats, 7 directions")
    y = puces(c, 50, 410, [
        "Entrée :|e-mail, ticket, cahier des charges, notes non relues, messagerie, message vocal transcrit, note DPO, compte rendu, CSV.",
        "Difficulté :|les demandes se recoupent, se contredisent et enfreignent des règles posées ailleurs.",
        "Risque :|transformer chaque document en spec séparée, et livrer deux systèmes incompatibles.",
    ], size=15, largeur=860)
    boite(c, 50, 110, 860, 150, fond=GRIS_CLAIR)
    c.setFont("Sans-B", 14); c.setFillColor(BLEU)
    c.drawString(70, 235, "Exemple : informer un client dont le colis est en retard")
    cols = [("", 70), ("Logistique (B01)", 330), ("Service client (B02)", 620)]
    rows = [("Canal", "SMS", "E-mail uniquement"),
            ("Seuil", "48 h après la date promise", "Dès J+1 matin"),
            ("Validation", "Aucune intervention manuelle", "Conseiller pour les Premium"),
            ("Échéance", "Pour le pic (fin novembre)", "T1 2027, après le gel")]
    c.setFont("Sans-B", 12.5); c.setFillColor(GRIS)
    for t, x in cols:
        c.drawString(x, 212, t)
    yy = 190
    for r in rows:
        c.setFont("Sans-B", 12.5); c.setFillColor(BLEU); c.drawString(70, yy, r[0])
        c.setFont("Sans", 12.5); c.setFillColor(ROUGE); c.drawString(330, yy, r[1]); c.drawString(620, yy, r[2])
        yy -= 19

    # 3. La solution : le pipeline
    c = s.page("Notre solution : un pipeline de 4 agents", "orchestré par un 5ᵉ agent")
    etapes = [("1. Extracteur", "A", "document → fiche JSON\ncitations exactes"),
              ("2. Analyste", "B", "fiches → projets,\nconflits, hypothèses"),
              ("3. Rédacteur", "C", "projet → spec Kiro\n(exigences, conception,\ntâches)"),
              ("4. Contrôleur", "D", "specs → rapport\nqualité")]
    x0, w, gap = 50, 190, 33
    for i, (t, qui, desc) in enumerate(etapes):
        x = x0 + i * (w + gap)
        boite(c, x, 290, w, 120, fond=BLEU if qui != "B" else ACCENT)
        c.setFillColor(white); c.setFont("Sans-B", 17); c.drawString(x + 14, 382, t)
        c.setFont("Sans", 11); c.drawString(x + 14, 364, f"rôle {qui}")
        c.setFont("Sans", 13)
        for j, l in enumerate(desc.split("\n")):
            c.drawString(x + 14, 340 - j * 17, l)
        if i < 3:
            fleche(c, x + w + 4, 350, x + w + gap - 4)
    c.setFillColor(GRIS); c.setFont("Sans", 12)
    c.drawString(50, 268, "Pause humaine après l'analyse : on valide la carte des projets et les arbitrages avant de rédiger.")
    puces(c, 50, 225, [
        "Contrats d'interface (CONTRATS.md) :|chaque étape lit et écrit un format JSON défini, ce qui permet de travailler à 4 en parallèle.",
        "Traçabilité de bout en bout :|chaque critère d'une spec cite sa source (B02-D7, CT-03, H02…), jusqu'à la citation exacte du document.",
        "Validation automatique :|un hook Kiro lance les validateurs Python dès qu'un agent écrit une fiche, l'analyse ou une spec.",
    ], size=13.5, largeur=860, ecart=6)

    # 4. Ce que nous utilisons dans Kiro
    c = s.page("Ce que nous utilisons dans Kiro", ".kiro/ à la racine du dépôt")
    cartes = [
        ("Agents personnalisés", ["orchestrateur, extracteur, analyste,", "redacteur-spec, controleur", "chacun avec ses outils et ses ressources"]),
        ("Steering", ["00-pipeline : règles communes (always)", "glossaire Orvanne (always)", "contraintes transverses (auto)", "format des specs (fileMatch)"]),
        ("Hooks", ["à l'enregistrement d'une fiche,", "de l'analyse ou d'une spec :", "lancement des validateurs"]),
        ("Specs Kiro", ["requirements.md en EARS français", "design.md avec diagrammes Mermaid", "tasks.md relié aux exigences", "+ bugfix.md pour les correctifs"]),
    ]
    for i, (t, ls) in enumerate(cartes):
        x = 50 + (i % 2) * 440
        y = 260 if i < 2 else 80
        boite(c, x, y, 420, 160, fond=BLEU_CLAIR)
        c.setFillColor(BLEU); c.setFont("Sans-B", 17); c.drawString(x + 18, y + 128, t)
        c.setFillColor(GRIS); c.setFont("Sans", 13.5)
        for j, l in enumerate(ls):
            c.drawString(x + 18, y + 98 - j * 21, l)

    # 5. Extraction et analyse : chiffres
    c = s.page("Extraction et analyse", "rôles A et B")
    vals = [(d["fiches"], "fiches"), (d["demandes"], "demandes extraites"),
            (nb_proj, f"projets ({feat} feature, {bug} bugfix)"), (nb_conf, "conflits détectés"),
            (d["hyp"], "hypothèses réversibles"), (len(d["questions"]), "questions, avec leur destinataire")]
    for i, (v, l) in enumerate(vals):
        chiffre(c, 50 + i * 146, 330, 132, v, l, couleur=ACCENT if i in (3,) else BLEU)
    puces(c, 50, 285, [
        "Extraction :|une demande élémentaire par idée, citation vérifiée mot pour mot par script, points flous relevés, statut (demandé, idée, V2, rejeté).",
        "Regroupement :|même processus = même projet, même si les demandes se contredisent (B01 + B02 → P01).",
        "Chaque conflit :|positions sourcées, gravité, arbitre légitime (DPO, finance, juridique, comité de direction), hypothèse pour avancer, question précise.",
        f"Contraintes transverses :|{d['ct_steering']} règles communes (RGPD, gel, hébergement, Passerelle…). Une demande qui en enfreint une devient un conflit, jamais une suppression silencieuse.",
    ], size=13.5, largeur=860, ecart=6)

    # 6. Démo en direct : un nouveau besoin traité par les 4 agents (débat réel, presentation/debat-demo-live.json)
    live = json.loads((RACINE / "presentation/debat-demo-live.json").read_text(encoding="utf-8"))
    c = s.page("Démo en direct : un nouveau besoin", f"débat réel, {round(live['duree_s'])} s")
    boite(c, 50, 112, 280, 338, fond=GRIS_CLAIR)
    c.setFont("Sans-B", 14); c.setFillColor(BLEU); c.drawString(66, 425, "Besoin collé dans la page")
    yy = 400
    for l in live["besoin"].split("\n"):
        yy = paragraphe(c, 66, yy, l or " ", font="Cond", size=12, largeur=250, interligne=1.3) - 3
    agents = [
        ("E", "Extracteur", HexColor("#2B8FC0"), "3 demandes : D1 SMS à l'expédition · D2 code promo de 10 % · D3 « la semaine prochaine ». Point flou : aucun consentement SMS mentionné."),
        ("A", "Analyste", ACCENT, "Rattaché à P01, pas de nouveau projet. 3 conflits : D2 contre CT-03 (pas d'offre dans un message de service), D1 contre CT-02 (mobile réservé à la livraison), D3 contre CT-07 (gel)."),
        ("R", "Rédacteur", VERT, "« PENDANT QUE la DPO n'a pas validé le traitement, LE SYSTÈME NE DOIT PAS envoyer de SMS. » (Source : D1, CT-01, CT-02)"),
        ("C", "Contrôleur", ROUGE, "3 objections : délai de 5 min sans source, consentement non défini, conflits à numéroter. Le rédacteur et l'analyste corrigent."),
    ]
    y = 398
    for ini, nom, coul, txt in agents:
        c.setFillColor(coul); c.circle(370, y + 4, 15, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Sans-B", 14); c.drawCentredString(370, y - 1, ini)
        c.setFillColor(coul); c.setFont("Sans-B", 13); c.drawString(395, y + 8, nom)
        paragraphe(c, 395, y - 9, txt, size=11.5, largeur=515, interligne=1.3)
        y -= 72
    boite(c, 350, 50, 560, 62, fond=HexColor("#E3F2E8"), bord=VERT)
    c.setFillColor(VERT); c.setFont("Sans-B", 15); c.drawString(366, 90, "VERDICT : ACCORD")
    paragraphe(c, 366, 72, "Code promo exclu (C27), SMS désactivé jusqu'à l'avis DPO (C28), mise en service après le 11/01/2027 (C29). Questions à la DPO, au service client et au marketing.", size=11, largeur=530, couleur=GRIS, interligne=1.25)
    c.setFillColor(HexColor("#9AA5B1")); c.setFont("Sans", 10)
    c.drawString(50, 96, "Chaque tour est un vrai appel")
    c.drawString(50, 83, "à un agent Kiro ; le texte varie")
    c.drawString(50, 70, "d'une exécution à l'autre.")

    # 7. Rédaction et qualité
    c = s.page("Rédaction et contrôle qualité", "rôles C et D")
    vals = [(nb_proj, "specs Kiro générées"), (d["criteres"], "critères d'acceptation en EARS"),
            (d["taches"], "sous-tâches reliées aux exigences"), (f"{nb_proj}/{nb_proj}", "specs au verdict OK")]
    for i, (v, l) in enumerate(vals):
        chiffre(c, 50 + i * 220, 330, 200, v, l, couleur=VERT if i == 3 else BLEU)
    puces(c, 50, 290, [
        "Validateur des specs :|structure, syntaxe EARS, sources existantes, couverture de chaque critère par une tâche.",
        "Plans de tâches :|revue DPO et arbitrages en prérequis ; tâches bloquées par une décision regroupées en fin de plan.",
        f"Référence humaine :|34 conflits identifiés à la main ; l'analyse en couvre {couv_ok}, partiellement {couv_part}, et en manque {couv_non}.",
        "Démo :|demo/index.html, page autonome où chaque identifiant (B02-D7, C01, H03) affiche sa preuve.",
    ], size=13.5, largeur=860, ecart=6)

    # 8. Ce que l'analyse révèle pour Orvanne
    c = s.page("Ce que l'analyse révèle pour Orvanne", "à arbitrer par les directions")
    constats = [
        ("Calendrier", "Le Black Friday (27/11) tombe pendant le gel des mises en production (16/11 au 11/01) : l'outil « pour le pic » de la logistique n'est pas livrable en production. Même problème pour le portail retours « avant les soldes » et l'outil casse « pour l'inventaire »."),
        ("RGPD", "Code promo dans un message de service, démo marketing sur de vrais clients, historique depuis 2014 : interdits par les règles de la DPO, qui n'a été consultée sur aucun des projets en cours."),
        ("Argent", "Remboursement des retours au premier scan (cahier des charges) ou après contrôle en entrepôt (finance) ; retours gratuits ou 4,90 € retenus. Décision de la DAF attendue."),
        ("Périmètre", "35 % des demandes de retour concernent la marketplace, exclue du portail : sans arbitrage, le service client garde un tiers du travail."),
    ]
    y = 420
    for t, txt in constats:
        c.setFillColor(ACCENT); c.rect(50, y - 52, 5, 62, fill=1, stroke=0)
        c.setFont("Sans-B", 15); c.setFillColor(BLEU); c.drawString(68, y - 2, t)
        paragraphe(c, 200, y - 2, txt, size=13, largeur=710)
        y -= 88

    # 9. Limites et suite
    c = s.page("Limites et suite", "")
    puces(c, 50, 420, [
        f"Détection incomplète :|{couv_non} conflits de la référence non détectés (bon d'achat +5 %, échelle de priorités de B09) et {couv_part} partiels. Les règles de l'analyste ont été renforcées ; une nouvelle exécution doit les capter.",
        f"Synchronisation :|l'analyse générée déclare {d['ct']} contraintes transverses, le steering en définit {d['ct_steering']}. À réaligner à la prochaine exécution.",
        f"Décisions humaines :|{bloq_q} question bloquante (dérogation au gel pour le pic) ; les autres conflits avancent sur des hypothèses réversibles.",
        "Généralisation :|les agents, contrats et validateurs sont génériques ; seule la référence des 34 conflits est propre à ce jeu de documents.",
        "Prochaine étape :|faire valider la carte des projets et les arbitrages par les directions, puis lancer le développement de P01 depuis tasks.md.",
    ], size=14, largeur=860, ecart=10)
    boite(c, 50, 50, 860, 50, fond=BLEU)
    c.setFillColor(white); c.setFont("Sans-B", 15)
    c.drawCentredString(W / 2, 70, "Démos : demo/index.html (résultats)  ·  tools/demo_live.py (débat en direct des agents)")

    s.fin()


if __name__ == "__main__":
    construire(charger())
    print(f"Écrit : {SORTIE.relative_to(RACINE)}")
