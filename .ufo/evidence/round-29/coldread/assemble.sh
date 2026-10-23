#!/usr/bin/env bash
# Round 29 (from round-28 land.sh): assemble the wave-1 cold-read reports, keep only entries that meet
# the frozen C1 binding check (select-bound.py; every exclusion listed in select-receipt-w1.json), append them.
set -euo pipefail
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
E=.ufo/evidence/round-29/coldread
python3 .ufo/evidence/round-18/coldread/assemble.py --reports '.ufo/waves/round-29/w1/Read*.md' --repo . --out "$E/assembled-w1.json" > "$E/assemble-w1.out" 2>&1 || true
grep -v '^  start=' "$E/assemble-w1.out" | head -60
python3 - "$E/assembled-w1.json" <<'PY'
import json, sys
bad = {'SCORECARD.md', 'LOG.md', 'corpus/lessons/round-29.md', '.ufo/evidence/round-21/coldread/ledger.json'}
for e in json.load(open(sys.argv[1]))['entries']:
    hit = bad & set(e.get('inputs') or {})
    print('EXEMPT-INPUT' if hit else 'ok', e.get('seats'), e['heading'][:60], e['verdict'], sorted(hit))
PY
python3 "$E/select-bound.py" --assembled "$E/assembled-w1.json" --out "$E/assembled-w1-bound.json" --receipt "$E/select-receipt-w1.json"
python3 "$E/append-entries.py" --assembled "$E/assembled-w1-bound.json" --ledger .ufo/evidence/round-21/coldread/ledger.json --receipt "$E/append-receipt-w1.json"
git diff --numstat -- .ufo/evidence/round-21/coldread/ledger.json
