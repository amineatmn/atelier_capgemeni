#!/usr/bin/env python3
"""Génère demo/index.html : une page autonome (sans serveur ni dépendance) qui présente
les sorties du pipeline : documents et demandes, projets et conflits, specs Kiro, rapport qualité.
Chaque identifiant (B0x-Dn, Cnn, Hnn, Qnn, CT-nn) est cliquable et affiche sa preuve.

Usage :
    python3 tools/generer_demo.py      # puis ouvrir demo/index.html dans un navigateur
Responsable : D.
"""
from __future__ import annotations

import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def main() -> int:
    analyse = json.loads(lire(RACINE / "work" / "analyse.json"))
    fiches = [json.loads(lire(f)) for f in sorted((RACINE / "work" / "fiches").glob("B[0-9][0-9].json"))]
    specs = {}
    for p in analyse["projets"]:
        d = RACINE / ".kiro" / "specs" / p["slug"]
        specs[p["slug"]] = {n: lire(d / n) for n in ("requirements.md", "bugfix.md", "design.md", "tasks.md") if (d / n).is_file()}
    donnees = {"analyse": analyse, "fiches": fiches, "specs": specs,
               "rapport": lire(RACINE / "work" / "rapport-qualite.md"),
               "sources": {f.name: lire(f) for f in sorted((RACINE / "challenge-b").glob("B[0-9][0-9]_*"))}}
    html = MODELE.replace("__DONNEES__", json.dumps(donnees, ensure_ascii=False).replace("</", "<\\/"))
    sortie = RACINE / "demo" / "index.html"
    sortie.parent.mkdir(exist_ok=True)
    sortie.write_text(html, encoding="utf-8")
    print(f"Démo écrite : {sortie.relative_to(RACINE)} ({sortie.stat().st_size // 1024} Ko)")
    return 0


MODELE = r"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orvanne : des expressions de besoin aux specs Kiro</title>
<style>
:root{--bleu:#1f4e79;--clair:#eef3f8;--gris:#666;--rouge:#b3261e;--orange:#c77700;--vert:#2e7d32}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#222;background:#fafbfc}
header{background:var(--bleu);color:#fff;padding:18px 28px}header h1{margin:0;font-size:22px}header p{margin:4px 0 0;opacity:.85}
.flux{display:flex;gap:8px;align-items:stretch;padding:16px 28px;background:#fff;border-bottom:1px solid #ddd;flex-wrap:wrap}
.etape{flex:1;min-width:150px;background:var(--clair);border-radius:8px;padding:10px 14px;cursor:pointer;border:2px solid transparent}
.etape.actif{border-color:var(--bleu)}.etape b{display:block;font-size:26px;color:var(--bleu)}.etape small{color:var(--gris)}
.fleche{align-self:center;font-size:22px;color:#999}
main{display:flex;min-height:calc(100vh - 190px)}nav{width:300px;border-right:1px solid #ddd;background:#fff;overflow:auto;max-height:calc(100vh - 190px)}
nav div{padding:9px 16px;border-bottom:1px solid #eee;cursor:pointer}nav div:hover,nav div.actif{background:var(--clair)}
nav small{color:var(--gris);display:block}#contenu{flex:1;padding:20px 32px;overflow:auto;max-height:calc(100vh - 190px)}
table{border-collapse:collapse;margin:10px 0;width:100%;font-size:14px}td,th{border:1px solid #ddd;padding:5px 8px;vertical-align:top;text-align:left}th{background:var(--clair)}
.id{color:var(--bleu);font-weight:600;cursor:pointer;border-bottom:1px dotted var(--bleu);white-space:nowrap}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;color:#fff}.bloquant{background:var(--rouge)}.majeur{background:var(--orange)}.mineur{background:#888}
.onglets span{display:inline-block;padding:6px 14px;margin-right:4px;border-radius:6px 6px 0 0;background:#e5e9ee;cursor:pointer}.onglets span.actif{background:var(--bleu);color:#fff}
pre{background:#f3f4f6;padding:10px;overflow:auto;font-size:13px}code{background:#f3f4f6;padding:0 3px}
#bulle{position:fixed;right:20px;bottom:20px;width:440px;max-height:60vh;overflow:auto;background:#fff;border:2px solid var(--bleu);border-radius:10px;padding:14px 18px;box-shadow:0 6px 24px #0003;display:none}
#bulle .fermer{float:right;cursor:pointer;font-size:18px}blockquote{margin:6px 0;padding:6px 12px;border-left:4px solid var(--bleu);background:var(--clair)}
input#recherche{width:100%;padding:8px 12px;border:0;border-bottom:1px solid #ddd;font-size:14px}
</style></head><body>
<header><h1>Orvanne : des expressions de besoin aux specs Kiro</h1>
<p>Pipeline agentique Kiro : extraction → analyse transverse → rédaction des specs → contrôle qualité. Cliquez sur un identifiant pour voir sa preuve.</p></header>
<div class="flux" id="flux"></div>
<main><nav id="nav"></nav><section id="contenu"></section></main>
<div id="bulle"><span class="fermer" onclick="this.parentNode.style.display='none'">×</span><div id="bulle-texte"></div></div>
<script>
const D = __DONNEES__;
const A = D.analyse, idx = {};
D.fiches.forEach(f => { f.demandes.forEach(x => idx[x.id] = {type:"demande", doc:f, x}); (f.chiffres||[]).forEach(x => idx[x.id] = {type:"chiffre", doc:f, x}); (f.points_flous||[]).forEach(x => idx[x.id] = {type:"flou", doc:f, x}); });
A.conflits.forEach(x => idx[x.id] = {type:"conflit", x}); A.hypotheses.forEach(x => idx[x.id] = {type:"hypothese", x});
A.questions.forEach(x => idx[x.id] = {type:"question", x}); A.contraintes_transverses.forEach(x => idx[x.id] = {type:"contrainte", x});
A.projets.forEach(x => idx[x.id] = {type:"projet", x});
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const RE_ID = /\b(B\d\d-[DNF]\d+|CT-\d+|C\d{2}|H\d{2}|Q\d{2}|P0\d)\b/g;
const lier = s => s.replace(RE_ID, m => idx[m] ? `<span class="id" onclick="montrer('${m}')">${m}</span>` : m);
const badge = g => `<span class="badge ${g}">${g}</span>`;
function montrer(id){ const e = idx[id]; if(!e) return; let h = `<h3>${id}</h3>`;
  if (e.doc) h += `<p><b>${esc(e.doc.doc_id)}</b> · ${esc(e.doc.fichier)} · ${esc(e.doc.emetteur?.nom || e.doc.emetteur?.direction || "")}</p>`;
  const x = e.x;
  if (e.type==="demande") h += `<p><i>${esc(x.type)}</i> · ${esc(x.statut_source||"demande")}${x.priorite_exprimee?` · priorité « ${esc(x.priorite_exprimee)} »`:""}</p><p>${esc(x.enonce)}</p><blockquote>« ${esc(x.citation)} »</blockquote>${projetDe(id)}`;
  else if (e.type==="chiffre") h += `<p>${esc(x.libelle)} : <b>${esc(x.valeur)} ${esc(x.unite||"")}</b></p><blockquote>« ${esc(x.citation)} »</blockquote>`;
  else if (e.type==="flou") h += `<p>${esc(x.description)}</p>${x.citation?`<blockquote>« ${esc(x.citation)} »</blockquote>`:""}`;
  else if (e.type==="conflit") h += `<p>${badge(x.gravite)} <b>${esc(x.sujet)}</b></p><ul>${x.positions.map(p=>`<li>${lier(esc(p.source))} : ${esc(p.position)}</li>`).join("")}</ul><p>Arbitre : ${esc(x.arbitre)}</p><p>Hypothèse : ${x.hypothese?lier(x.hypothese)+" "+esc(idx[x.hypothese]?.x.enonce):"aucune (bloquant)"}</p><p>Question : ${x.question?lier(x.question)+" "+esc(idx[x.question]?.x.question):"—"}</p>`;
  else if (e.type==="hypothese") h += `<p>${esc(x.enonce)}</p><p><small>${esc(x.justification)}</small></p><p>Conflit : ${x.conflit?lier(x.conflit):"—"} · réversible : ${x.reversible?"oui":"non"}</p>`;
  else if (e.type==="question") h += `<p>${esc(x.question)}</p><p>Destinataire : ${esc(x.destinataire)} · ${x.bloquante?'<span class="badge bloquant">bloquante</span>':"non bloquante"}</p>`;
  else if (e.type==="contrainte") h += `<p>${esc(x.enonce)}</p><p>Sources : ${lier(esc((x.sources||[]).join(", ")))}</p>`;
  else if (e.type==="projet") h += `<p><b>${esc(x.titre)}</b> (${esc(x.type_spec)})</p><p><a href="#" onclick="vueSpec('${x.slug}');return false">Ouvrir la spec</a></p>`;
  document.getElementById("bulle-texte").innerHTML = h; document.getElementById("bulle").style.display = "block"; }
function projetDe(id){ const p = A.projets.find(p => p.demandes_incluses.includes(id)); const ex = A.projets.find(p => p.demandes_exclues.some(e=>e.id===id));
  if (p) return `<p>Incluse dans ${lier(p.id)} ${esc(p.titre)}</p>`; if (ex) { const e = ex.demandes_exclues.find(e=>e.id===id); return `<p>Exclue de ${lier(ex.id)} : ${esc(e.raison)}</p>`; } return ""; }
function md(t){ const L = t.split("\n"); let o = "", i = 0, liste = false;
  const inl = s => lier(esc(s)).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/`([^`]+)`/g,"<code>$1</code>").replace(/_Source : ([^_]+)_/g,"<small>Source : $1</small>").replace(/_Exigences : ([^_]+)_/g,"<small>Exigences : $1</small>");
  while (i < L.length) { let l = L[i];
    if (l.startsWith("```")) { let b = []; i++; while (i < L.length && !L[i].startsWith("```")) b.push(L[i++]); o += `<pre>${esc(b.join("\n"))}</pre>`; i++; continue; }
    if (/^\s*\|/.test(l)) { let r = []; while (i < L.length && /^\s*\|/.test(L[i])) r.push(L[i++]); r = r.filter(x => !/^\s*\|[\s\-:|]+\|\s*$/.test(x));
      o += "<table>" + r.map((x,k) => "<tr>" + x.trim().replace(/^\||\|$/g,"").split("|").map(c => k? `<td>${inl(c.trim())}</td>` : `<th>${inl(c.trim())}</th>`).join("") + "</tr>").join("") + "</table>"; continue; }
    const h = l.match(/^(#{1,4})\s+(.*)/); if (h) { o += `<h${h[1].length+1}>${inl(h[2])}</h${h[1].length+1}>`; i++; continue; }
    const li = l.match(/^\s*(?:[-*]|\d+\.)\s+(.*)/); if (li) { o += `<div style="margin-left:${l.search(/\S/)*8+8}px">• ${inl(li[1].replace(/^\[[ x]\]\s*/,"☐ "))}</div>`; i++; continue; }
    if (l.startsWith("<!--")) { while (i < L.length && !L[i].includes("-->")) i++; i++; continue; }
    if (l.trim()) o += `<p>${inl(l)}</p>`; i++; }
  return o; }
const C = document.getElementById("contenu"), N = document.getElementById("nav");
function etapes(actif){ const nbD = D.fiches.reduce((s,f)=>s+f.demandes.length,0);
  const e = [["documents","9","documents sources",D.fiches.length+" fiches"],["demandes",nbD,"demandes extraites","avec citation exacte"],["projets",A.projets.length,"projets",A.conflits.length+" conflits, "+A.hypotheses.length+" hypothèses"],["specs",Object.keys(D.specs).length,"specs Kiro","requirements, design, tasks"],["qualite","✓","rapport qualité","contrôles et couverture"]];
  document.getElementById("flux").innerHTML = e.map((x,k)=>`${k?'<span class="fleche">→</span>':""}<div class="etape ${x[0]===actif?"actif":""}" onclick="vue('${x[0]}')"><b>${x[1]}</b>${x[2]}<br><small>${x[3]}</small></div>`).join(""); }
function vue(v){ etapes(v); ({documents:vueDocs, demandes:vueDocs, projets:vueProjets, specs:()=>vueSpec(A.projets[0].slug), qualite:vueQualite})[v](); }
function vueDocs(){ N.innerHTML = D.fiches.map(f=>`<div onclick="docDetail('${f.doc_id}')"><b>${f.doc_id}</b> ${esc(f.format)}<small>${esc(f.emetteur?.nom||f.emetteur?.direction||"")} · ${f.demandes.length} demandes</small></div>`).join(""); docDetail(D.fiches[0].doc_id); }
function docDetail(id){ const f = D.fiches.find(f=>f.doc_id===id); [...N.children].forEach(n=>n.classList.toggle("actif", n.textContent.startsWith(id)));
  C.innerHTML = `<h2>${id} · ${esc(f.fichier)}</h2><p>${esc(f.resume)}</p><div class="onglets"><span class="actif" onclick="ongletDoc(this,'${id}','d')">Demandes (${f.demandes.length})</span><span onclick="ongletDoc(this,'${id}','f')">Points flous (${f.points_flous.length})</span><span onclick="ongletDoc(this,'${id}','s')">Document source</span></div><div id="od"></div>`; ongletDoc(C.querySelector(".onglets span"), id, "d"); }
function ongletDoc(el,id,t){ [...el.parentNode.children].forEach(s=>s.classList.toggle("actif", s===el)); const f = D.fiches.find(f=>f.doc_id===id), o = document.getElementById("od");
  if (t==="d") o.innerHTML = `<table><tr><th>Id</th><th>Type</th><th>Énoncé</th><th>Citation</th><th>Projet</th></tr>${f.demandes.map(x=>`<tr><td>${lier(x.id)}</td><td>${esc(x.type)}</td><td>${esc(x.enonce)}</td><td><i>« ${esc(x.citation)} »</i></td><td>${lier((A.projets.find(p=>p.demandes_incluses.includes(x.id))||{}).id||"exclue")}</td></tr>`).join("")}</table>`;
  else if (t==="f") o.innerHTML = `<table>${f.points_flous.map(x=>`<tr><td>${lier(x.id)}</td><td>${esc(x.description)}</td></tr>`).join("")}</table>`;
  else o.innerHTML = `<pre>${esc(D.sources[f.fichier])}</pre>`; }
function vueProjets(){ N.innerHTML = A.projets.map(p=>`<div onclick="projet('${p.id}')"><b>${p.id}</b> ${esc(p.titre)}<small>${p.type_spec} · ${p.documents.join(", ")} · ${p.conflits.length} conflits</small></div>`).join("") + `<div onclick="tousConflits()"><b>Tous les conflits</b><small>${A.conflits.length} conflits, ${A.questions.length} questions</small></div>`; projet(A.projets[0].id); }
function projet(id){ const p = A.projets.find(p=>p.id===id); [...N.children].forEach(n=>n.classList.toggle("actif", n.textContent.startsWith(id)));
  const cs = A.conflits.filter(c=>p.conflits.includes(c.id)), qs = A.questions.filter(q=>q.projets.includes(id));
  C.innerHTML = `<h2>${id} · ${esc(p.titre)}</h2><p>Commanditaire : ${esc(p.commanditaire)} · Parties prenantes : ${esc(p.parties_prenantes.join(", "))}</p><p>Documents : ${p.documents.join(", ")} · ${p.demandes_incluses.length} demandes incluses, ${p.demandes_exclues.length} exclues · contraintes ${lier(p.contraintes.join(", "))}</p><p><a href="#" onclick="vueSpec('${p.slug}');return false">→ Ouvrir la spec ${p.slug}</a></p>
  <h3>Conflits</h3><table><tr><th>Id</th><th>Gravité</th><th>Sujet</th><th>Positions</th><th>Hypothèse retenue</th></tr>${cs.map(c=>`<tr><td>${lier(c.id)}</td><td>${badge(c.gravite)}</td><td>${esc(c.sujet)}</td><td>${c.positions.map(x=>lier(esc(x.source))+" : "+esc(x.position)).join("<br>")}</td><td>${c.hypothese?lier(c.hypothese)+" "+esc(idx[c.hypothese]?.x.enonce):"<b>à arbitrer</b>"}</td></tr>`).join("")||"<tr><td colspan=5>Aucun</td></tr>"}</table>
  <h3>Demandes exclues</h3><table>${p.demandes_exclues.map(e=>`<tr><td>${lier(e.id)}</td><td>${esc(e.raison)}</td><td>${e.renvoi?lier(e.renvoi):"—"}</td></tr>`).join("")||"<tr><td>Aucune</td></tr>"}</table>
  <h3>Questions ouvertes</h3><table>${qs.map(q=>`<tr><td>${lier(q.id)}</td><td>${esc(q.question)}</td><td>${esc(q.destinataire)}</td><td>${q.bloquante?badge("bloquant"):""}</td></tr>`).join("")}</table>`; }
function tousConflits(){ C.innerHTML = `<h2>Registre des conflits</h2><table><tr><th>Id</th><th>Gravité</th><th>Sujet</th><th>Projets</th><th>Arbitre</th><th>Hypothèse</th></tr>${A.conflits.map(c=>`<tr><td>${lier(c.id)}</td><td>${badge(c.gravite)}</td><td>${esc(c.sujet)}</td><td>${lier(A.projets.filter(p=>p.conflits.includes(c.id)).map(p=>p.id).join(", "))}</td><td>${esc(c.arbitre)}</td><td>${c.hypothese?lier(c.hypothese):"à arbitrer"}</td></tr>`).join("")}</table>`; }
function vueSpec(slug){ etapes("specs"); N.innerHTML = A.projets.map(p=>`<div class="${p.slug===slug?"actif":""}" onclick="vueSpec('${p.slug}')"><b>${p.id}</b> ${esc(p.slug)}<small>${p.type_spec}</small></div>`).join("");
  const s = D.specs[slug], noms = Object.keys(s); C.innerHTML = `<div class="onglets">${noms.map((n,k)=>`<span class="${k?"":"actif"}" onclick="ongletSpec(this,'${slug}','${n}')">${n}</span>`).join("")}</div><div id="os"></div>`; ongletSpec(C.querySelector(".onglets span"), slug, noms[0]); }
function ongletSpec(el,slug,n){ [...el.parentNode.children].forEach(s=>s.classList.toggle("actif", s===el)); document.getElementById("os").innerHTML = md(D.specs[slug][n]); }
function vueQualite(){ N.innerHTML = ""; C.innerHTML = md(D.rapport || "Rapport absent : lancer python3 tools/rapport_qualite.py"); }
document.getElementById("nav").insertAdjacentHTML("beforebegin","");
vue("projets");
</script></body></html>
"""

if __name__ == "__main__":
    raise SystemExit(main())
