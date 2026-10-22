#!/usr/bin/env bash
# Round 28: assemble the wave-1 cold-read reports that exist, append them to the round-21 ledger.
set -euo pipefail
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
E=.ufo/evidence/round-28/coldread
python3 .ufo/evidence/round-18/coldread/assemble.py --reports '.ufo/waves/round-28/w1/Read*.md' --repo . --out "$E/assembled-w1.json" > "$E/assemble-w1.out" 2>&1 || true
cat "$E/assemble-w1.out" | grep -v '^  start=' | head -40
python3 - "$E/assembled-w1.json" <<'EOF'
import json, sys
bad = {'SCORECARD.md', 'LOG.md', 'corpus/lessons/round-28.md'}
for e in json.load(open(sys.argv[1]))['entries']:
    hit = bad & set(e.get('inputs') or {})
    print('EXEMPT-INPUT' if hit else 'ok', e.get('seats'), e['heading'][:60], e['verdict'], sorted(hit))
EOF
python3 "$E/append-entries.py" --assembled "$E/assembled-w1.json" --ledger .ufo/evidence/round-21/coldread/ledger.json --receipt "$E/append-receipt-w1.json"
git diff --numstat -- .ufo/evidence/round-21/coldread/ledger.json
