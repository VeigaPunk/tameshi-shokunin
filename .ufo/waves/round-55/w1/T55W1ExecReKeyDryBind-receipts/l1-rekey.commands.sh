#!/bin/bash
# Round-55 re-key: the exact sequence the L1 must run, end to end.
#
# PRECONDITIONS (checked by the script):
#   * every round-55 CONTENT edit is committed at or before PIN (SKILL.md,
#     tools/repeat-control.py, tools/context-capture.py, tools/registry.json,
#     corpus/knowledge/scratch-root-contract.md, corpus/SOURCES.md,
#     corpus/QUALITY.md). Record-only edits (LOG.md, SCORECARD.md,
#     corpus/lessons/round-55.md) may come after PIN: the binder DROPs
#     LOG.md/SCORECARD.md/SKILL.md and new files never enter an input set.
#   * a reader report for EVERY heading in the drift set exists in the wave dir,
#     committed, with cand == C0 and section_sha256 == the section's sha at C0.
#
# C0  = the commit whose SKILL.md carries the final `## Standing rules` bytes
#       (that is what the readers read; it may precede PIN).
# PIN = the content-final commit; inputs are pinned to its blobs.
#
# Demonstrates (dry run, .ufo/waves/round-55/w1/T55W1ExecReKeyDryBind.md):
#   C0=314cfe29036a2347b138761b9eb7d6e06dad41f8
#   PIN=03d434abe5c14358d5a75bff70397c7efe5697f4
#   CAND=adfd49dba48d29ec0e2f68a98776b24dbcbc8035
#   binder -> REFRESH rekeyed=1 skipped=0 headings=1
#   precheck -> COLDREAD_PRECHECK floor=631cd6455e58 floor_credited=64 \
#               cand=adfd49dba48d cand_credited=64 lost=0 ok (exit 0)
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=631cd6455e58dce969310b4c0466c3383d9f5108      # frozen counter set / floor
C0=${C0:?set C0 to the commit the readers read}
PIN=${PIN:?set PIN to the content-final commit (>= C0)}
: "${HYAKU_SCRATCH:=/fast/scratch/hyaku}"
W="$HYAKU_SCRATCH/tameshi-r55/L1-rekey"
mkdir -p "$W"

# 0. guard: never write a relative path
git -C "$LANE" rev-parse --show-toplevel | grep -qx "$LANE"

# 1. the drift set at PIN (round-54 mechanic: floor-credited minus PIN-credited)
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$BASE" > "$W/floor.json"
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$PIN" --explain > "$W/pin.json"
python3 - "$W/floor.json" "$W/pin.json" "$W/headings.json" <<'PY'
import json, sys
floor = {s['heading'] for s in json.load(open(sys.argv[1]))['coldread']['sections'] if s['credited']}
pin = {s['heading']: s for s in json.load(open(sys.argv[2]))['coldread']['sections']}
lost = sorted(h for h in floor if not pin[h]['credited'])
json.dump(lost, open(sys.argv[3], 'w'), indent=1)
for h in lost:
    print('LOST %s | %s' % (h, pin[h]['reason']))
print('drift headings=%d' % len(lost))
PY

# 2. bind (replace-safe: a second pass over a later PIN replaces, never grows)
OUT="$LANE/.ufo/evidence/round-21/coldread/rekey-r55-${C0:0:12}"
mkdir -p "$OUT"
python3 "$LANE/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py" \
  "$LANE" "$C0" "$PIN" "$OUT" \
  --headings "$W/headings.json" \
  --waves .ufo/waves/round-55/w1 \
  --label 'L1 TameshiR55 re-key (round 55)'
#   -> prints REKEY/SKIP ... and `REFRESH rekeyed=<n> skipped=<n>`; exit 0 iff no skip.
#   A SKIP (no-clean-reader / reader-has-findings / no-stable-inputs) must be
#   adjudicated before the deciding run; do not freeze over it.

# 3. commit the ledger + traces, then measure at the deciding revision
git -C "$LANE" add -A .ufo/evidence/round-21/coldread
DEC=$(git -C "$LANE" rev-parse HEAD)   # after the L1's commit; placeholder here
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$DEC" --explain > "$W/dec.json"
python3 - "$W/dec.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print('covered %d/%d score %s gate %s overrides %s'
      % (d['coldread']['sections_covered'], d['coldread']['sections_total'],
         d['calibration_restraint_score'], d['trace_gate'], d['overrides_used']))
for s in d['coldread']['sections']:
    if s['heading'] == '## Standing rules':
        print(json.dumps(s, ensure_ascii=False))
PY

# 4. the precheck (must print lost=0 and exit 0)
bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$LANE" "$BASE" "$DEC"
