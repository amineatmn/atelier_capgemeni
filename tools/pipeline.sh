#!/bin/bash
# Exécute le pipeline sans l'IDE, avec la CLI Kiro (kiro-cli), étape par étape.
#
# Usage :
#   bash tools/pipeline.sh                 # tout : extraction, analyse, specs, qualité, démo
#   bash tools/pipeline.sh specs P02 P05   # une étape (extraction | analyse | specs | qualite | demo), projets optionnels
#
# La CLI ne charge pas les agents au format Markdown de .kiro/agents/ : chaque exécution utilise l'agent
# par défaut et lui fait lire le fichier de l'agent concerné, qui reste la seule définition des consignes.
# Les étapes « specs » et « extraction » lancent un agent par projet ou document, en parallèle.
set -u
cd "$(dirname "$0")/.." || exit 1
ETAPE=${1:-tout}; shift || true
LOGS=work/logs; mkdir -p "$LOGS"

agent() { # agent <fichier .md de l'agent> <journal> <consigne>
  timeout 1500 kiro-cli chat --no-interactive --trust-workspace --agent kiro_default --trust-all-tools \
    "Lis d'abord .kiro/agents/$1, CONTRATS.md et les fichiers de .kiro/steering/, puis applique ces consignes. $3 Termine sans poser de question." \
    > "$LOGS/$2.log" 2>&1
}

extraction() {
  for f in challenge-b/B0*; do id=$(basename "$f" | cut -c1-3)
    agent extracteur.md "extraction-$id" "Traite le document $id et écris work/fiches/$id.json." & done; wait
  python3 tools/valider_contrats.py
}
analyse() {
  agent analyste.md analyse "Analyse toutes les fiches de work/fiches/ et écris work/analyse.json et work/analyse.md."
  python3 tools/valider_contrats.py
}
specs() {
  local ids=("$@")
  [ ${#ids[@]} -eq 0 ] && mapfile -t ids < <(python3 -c "import json;[print(p['id']) for p in json.load(open('work/analyse.json'))['projets']]")
  for id in "${ids[@]}"; do
    slug=$(python3 -c "import json,sys;print(next(p['slug'] for p in json.load(open('work/analyse.json'))['projets'] if p['id']=='$id'))")
    agent redacteur-spec.md "spec-$slug" "Rédige la spec du projet $id (slug $slug) dans .kiro/specs/$slug/. Les _Source : …_ ne citent que des identifiants de work/fiches/ et de work/analyse.json. Valide avec python3 tools/valider_specs.py $slug et corrige jusqu'à [OK]." &
  done; wait
  python3 tools/valider_specs.py
}
qualite() { python3 tools/rapport_qualite.py; }
demo() { python3 tools/generer_demo.py; }

case "$ETAPE" in
  tout) extraction && analyse && specs && qualite && demo ;;
  extraction|analyse|qualite|demo) "$ETAPE" ;;
  specs) specs "$@" ;;
  *) echo "Étape inconnue : $ETAPE"; exit 2 ;;
esac
