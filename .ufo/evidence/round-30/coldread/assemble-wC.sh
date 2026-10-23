#!/usr/bin/env bash
# Round 30 attempt 3 (from round-29 assemble.sh): assemble the wave-C cold-read reports, keep only the
# entries that meet the frozen binding v3 (bind-select-v3.py, landed 9207f226 before wave-C dispatch;
# every exclusion listed in bind-receipt-wC.json), append them to the ledger.
set -euo pipefail
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
E=.ufo/evidence/round-30/coldread
SESS=/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7/TameshiR30A3
REV=bb681566b18211adf8ae9c28df91e17678e3f545
python3 .ufo/evidence/round-18/coldread/assemble.py --reports '.ufo/waves/round-30/wC/Cold*.md' --repo . --out "$E/assembled-wC.json" > "$E/assemble-wC.out" 2>&1 || true
grep -v '^  start=' "$E/assemble-wC.out" | head -80
python3 - "$E/assembled-wC.json" <<'PY'
import json, sys
bad = {'SCORECARD.md', 'LOG.md', 'corpus/lessons/round-30.md', '.ufo/evidence/round-21/coldread/ledger.json'}
for e in json.load(open(sys.argv[1]))['entries']:
    hit = bad & set(e.get('inputs') or {})
    print('EXEMPT-INPUT' if hit else 'ok', e.get('seats'), e['heading'][:60], e['verdict'], sorted(hit))
PY
python3 "$E/bind-select-v3.py" --repo . --assembled "$E/assembled-wC.json" --registry .ufo/waves/round-30/wC/swarm-registry.json \
  --sessions "$SESS" --prefix TameshiR30A3. --out "$E/assembled-wC-bound.json" --receipt "$E/bind-receipt-wC.json"
python3 "$E/append-entries.py" --assembled "$E/assembled-wC-bound.json" --bindings "$E/bind-receipt-wC.json" --rev "$REV" \
  --ledger .ufo/evidence/round-21/coldread/ledger.json --receipt "$E/append-receipt-wC.json"
git diff --numstat -- .ufo/evidence/round-21/coldread/ledger.json
