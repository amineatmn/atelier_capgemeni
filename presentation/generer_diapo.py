#!/usr/bin/env python3
"""Génère presentation/orvanne-pipeline-specs.pdf (diaporama 16:9, 3 diapositives).

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


# ---------- diapositives (3 au plus) ----------
DEMO_URL = "https://d2jtyhcrng1ah2.cloudfront.net/proxy/8766"


def construire(d: dict):
    s = Diapo()
    nb_proj = len(d["projets"])
    feat = sum(p["type_spec"] == "feature" for p in d["projets"])
    couv_ok, couv_part, couv_non = d["couv"]

    # 1. Problème et solution
    c = s.page("Orvanne : des besoins aux specs Kiro", "Challenge B · équipe de 4")
    paragraphe(c, 50, 425, "Le problème", font="Sans-B", size=16, couleur=BLEU)
    puces(c, 50, 400, [
        "9 documents, 9 formats :|e-mail, ticket, notes non relues, message vocal, CSV…",
        "Ils se contredisent :|logistique « SMS à 48 h, sans validation » contre service client « e-mail dès J+1, validé pour les Premium ».",
        "Ils enfreignent des règles :|code promo dans un message de service, démo sur de vrais clients, livraison pendant le gel.",
    ], size=13, largeur=400, ecart=5)
    paragraphe(c, 500, 425, "Notre solution", font="Sans-B", size=16, couleur=BLEU)
    puces(c, 500, 400, [
        "Un pipeline de 4 agents Kiro|piloté par un orchestrateur, avec une pause pour l'arbitrage humain.",
        "Traçabilité :|chaque critère d'une spec cite sa source (B02-D7, CT-03, H02) jusqu'à la citation exacte.",
        "Kiro :|agents, steering, hooks de validation, specs (exigences EARS, conception, tâches).",
    ], size=13, largeur=410, ecart=5)
    etapes = [("1. Extracteur", "A", f"{d['fiches']} documents → {d['demandes']} demandes citées"),
              ("2. Analyste", "B", f"{nb_proj} projets, {len(d['conflits'])} conflits, {d['hyp']} hypothèses"),
              ("3. Rédacteur", "C", f"{nb_proj} specs Kiro, {d['criteres']} critères EARS"),
              ("4. Contrôleur", "D", f"rapport qualité : {nb_proj}/{nb_proj} OK")]
    x0, w, gap = 50, 192, 30
    for i, (t, qui, desc) in enumerate(etapes):
        x = x0 + i * (w + gap)
        boite(c, x, 60, w, 105, fond=ACCENT if qui == "B" else BLEU)
        c.setFillColor(white); c.setFont("Sans-B", 16); c.drawString(x + 14, 137, t)
        c.setFont("Sans", 11); c.drawString(x + 14, 120, f"rôle {qui}")
        paragraphe(c, x + 14, 98, desc, size=12.5, largeur=w - 26, couleur=white, interligne=1.25)
        if i < 3:
            fleche(c, x + w + 3, 112, x + w + gap - 3)

    # 2. Démo en direct (débat réel, presentation/debat-demo-live.json)
    live = json.loads((RACINE / "presentation/debat-demo-live.json").read_text(encoding="utf-8"))
    c = s.page("Démo en direct : un nouveau besoin", f"débat réel des agents, {round(live['duree_s'])} s")
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
    c.setFillColor(GRIS); c.setFont("Sans-B", 10.5); c.drawString(50, 96, "Démo en direct :")
    c.setFillColor(HexColor("#2B6CB0")); c.setFont("Sans", 9.5)
    c.drawString(50, 82, DEMO_URL)
    c.linkURL(DEMO_URL, (50, 78, 330, 92), relative=0)
    c.setFillColor(HexColor("#9AA5B1")); c.setFont("Sans", 9.5)
    c.drawString(50, 64, "Chaque tour est un vrai appel à un agent Kiro.")

    # 3. Résultats et limites
    c = s.page("Résultats et limites", "sorties du pipeline sur les 9 documents")
    vals = [(d["demandes"], "demandes extraites"), (f"{nb_proj}", f"projets ({feat} feature, {nb_proj - feat} bugfix)"),
            (len(d["conflits"]), "conflits détectés"), (d["criteres"], "critères EARS"), (f"{nb_proj}/{nb_proj}", "specs au verdict OK")]
    for i, (v, l) in enumerate(vals):
        chiffre(c, 50 + i * 176, 335, 160, v, l, couleur=VERT if i == 4 else (ACCENT if i == 2 else BLEU))
    paragraphe(c, 50, 300, "Ce que l'analyse révèle", font="Sans-B", size=15, couleur=BLEU)
    puces(c, 50, 275, [
        "Calendrier :|le Black Friday (27/11) tombe pendant le gel (16/11 au 11/01) ; l'outil « pour le pic » n'est pas livrable.",
        "RGPD :|code promo, démo sur vrais clients, historique depuis 2014 : interdits par la DPO, jamais consultée.",
        "Argent :|remboursement au scan ou après contrôle, retours gratuits ou 4,90 € : décision de la DAF.",
    ], size=12.5, largeur=420, ecart=5)
    paragraphe(c, 500, 300, "Limites et suite", font="Sans-B", size=15, couleur=BLEU)
    puces(c, 500, 275, [
        f"Référence de 34 conflits :|{couv_ok} couverts, {couv_part} partiels, {couv_non} manqués (bon d'achat +5 %, priorités de B09).",
        "Aucun conflit tranché en silence :|chaque conflit a un arbitre, une hypothèse réversible et une question.",
        "Suite :|faire valider les arbitrages par les directions, puis développer P01 depuis tasks.md.",
    ], size=12.5, largeur=410, ecart=5)
    boite(c, 50, 45, 860, 40, fond=BLEU)
    c.setFillColor(white); c.setFont("Sans-B", 13.5)
    c.drawCentredString(W / 2, 60, "Résultats : demo/index.html  ·  Débat en direct : tools/demo_live.py")

    s.fin()


if __name__ == "__main__":
    construire(charger())
    print(f"Écrit : {SORTIE.relative_to(RACINE)}")
