#!/bin/bash
# Round-48 (attempt 3) fix for the mined mistake "a claim's record edits drop cold-read credited sections, seen
# only at the deciding run" (corpus/lessons/round-48.md, attempt-3 section). Run on a candidate content revision
# BEFORE it is frozen as the deciding revision: it counts the round-21 cold-read monitor's credited sections at
# CAND and at FLOOR_REV and prints RED (exit 1) when CAND credits fewer, naming every section that lost credit and
# the input paths that drifted. Read-only: it reads git objects only.
# Usage: coldread-precheck.sh LANE FLOOR_REV CAND_REV
set -u
LANE=$1; FLOOR=$2; CAND=$3
cd "$LANE" || exit 2
M=.ufo/evidence/round-21/coldread/measure.py
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r48/coldread-precheck.$$
mkdir -p "$SCR"; trap 'rm -rf -- "$SCR"' EXIT
python3 "$M" --repo "$LANE" --rev "$FLOOR" > "$SCR/floor.json" 2>/dev/null || { echo "COLDREAD_PRECHECK error=floor-measure"; exit 2; }
python3 "$M" --repo "$LANE" --rev "$CAND" > "$SCR/cand.json" 2>/dev/null || { echo "COLDREAD_PRECHECK error=cand-measure"; exit 2; }
python3 - "$SCR/floor.json" "$SCR/cand.json" "$FLOOR" "$CAND" <<'PY'
import json, sys
f = json.load(open(sys.argv[1]))['coldread']['sections']
c = json.load(open(sys.argv[2]))['coldread']['sections']
fc = {s['heading'] for s in f if s['credited']}
cc = {s['heading'] for s in c if s['credited']}
lost = sorted(fc - cc)
for h in lost:
    reason = next(s['reason'] for s in c if s['heading'] == h)
    paths = sorted({r.split(':', 1)[1] for r in reason.split(';') if r.startswith('input-drift:')})
    print('LOST %s | drifted=%s' % (h, ','.join(paths)))
state = 'RED' if len(cc) < len(fc) else 'ok'
print('COLDREAD_PRECHECK floor=%s floor_credited=%d cand=%s cand_credited=%d lost=%d %s'
      % (sys.argv[3][:12], len(fc), sys.argv[4][:12], len(cc), len(lost), state))
sys.exit(1 if state == 'RED' else 0)
PY
