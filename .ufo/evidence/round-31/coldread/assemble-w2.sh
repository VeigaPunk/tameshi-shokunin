#!/usr/bin/env bash
# Round 31 (from round-30 assemble-wC.sh): assemble the wave-2 cold-read reports, keep only the entries
# that meet binding v5 (bind-select-v5.py, committed 87eb64eb before the wave-2 dispatch record 3351738a;
# every exclusion listed in bind-receipt-w2.json), append them to the ledger.
set -euo pipefail
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
E=.ufo/evidence/round-31/coldread
SESS=/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7/TameshiR31
REV=2da841bd9913a2037d2bf612793382e572c9d205
python3 .ufo/evidence/round-18/coldread/assemble.py --reports '.ufo/waves/round-31/w2/Cold*.md' --repo . --out "$E/assembled-w2.json" > "$E/assemble-w2.out" 2>&1 || true
grep -v '^  start=' "$E/assemble-w2.out" | head -80
python3 - "$E/assembled-w2.json" <<'PY'
import json, sys
bad = {'SCORECARD.md', 'LOG.md', 'corpus/lessons/round-31.md', '.ufo/evidence/round-21/coldread/ledger.json'}
for e in json.load(open(sys.argv[1]))['entries']:
    hit = bad & set(e.get('inputs') or {})
    print('EXEMPT-INPUT' if hit else 'ok', e.get('seats'), e['heading'][:60], e['verdict'], sorted(hit))
PY
python3 "$E/bind-select-v5.py" --repo . --assembled "$E/assembled-w2.json" --registry .ufo/waves/round-31/w2/swarm-registry.json \
  --sessions "$SESS" --prefix TameshiR31. --out "$E/assembled-w2-bound.json" --receipt "$E/bind-receipt-w2.json"
python3 "$E/append-entries.py" --assembled "$E/assembled-w2-bound.json" --bindings "$E/bind-receipt-w2.json" --rev "$REV" \
  --ledger .ufo/evidence/round-21/coldread/ledger.json --receipt "$E/append-receipt-w2.json"
git diff --numstat -- .ufo/evidence/round-21/coldread/ledger.json
