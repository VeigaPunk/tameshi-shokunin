#!/bin/bash
# Round-46 QUALITY criteria 88-90: each block must FAIL its bad input and pass its good input; prints CRITERION-NN-FALSIFIER-OK.
# Usage: falsifiers.sh [HARDENED_REV]   (run from any cwd; reads the lane at the paths below)
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
Q=$L/.ufo/evidence/round-46/quality
E=$L/.ufo/evidence/round-46
REV=${1:-a6892b196f923efbed242ce9ea599a3f745b2138}
BASE=683eedde3a50441c34d85a22f5fd5346f8b1ec6d
T=$(mktemp -d)
# ---- 88: a no_harm monitor that is red at base is refused; the real list is green at base
cat > "$T/r44.json" <<'J'
{"monitors": [{"name": "r44-record-agreement",
  "command": "python3 .ufo/evidence/round-44/calibration/measure.py --lane \"$LANE\" --rev \"$REV\" --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e",
  "expect_contains": ["C2_R44_PASS=true"]}]}
J
python3 "$Q/no-harm-gate.py" --contract "$E/contract.json" --lane "$L" --rev "$BASE" --monitors-file "$T/r44.json" | tail -3; red=${PIPESTATUS[0]}
python3 "$Q/no-harm-gate.py" --contract "$E/contract.json" --lane "$L" --rev "$BASE" --monitors-file "$E/no-harm.sh" | tail -2; ok=${PIPESTATUS[0]}
echo "c88 red_monitor_exit=$red real_list_exit=$ok"
[ "$red" = 1 ] && [ "$ok" = 0 ] && echo CRITERION-88-FALSIFIER-OK || echo CRITERION-88-FALSIFIER-VACUOUS
# ---- 89: a selftest that pins its own bytes kills every mutant, so the neutral mutants must be what refuses it
python3 "$E/control/run-controls.py" 2>&1 | grep -E '^CTL_E' | cut -c1-260 | tee "$T/ctle"
python3 "$E/hardening/mutate.py" --lane "$L" --rev "$REV" --targets hardened | tail -1 | cut -c1-260 | tee "$T/real"
if grep -q 'neutral_killed=[1-9]' "$T/ctle" && grep -q 'C2_R46_PASS=false' "$T/ctle" && grep -q 'neutral_killed=0' "$T/real" && grep -q 'C2_R46_PASS=true' "$T/real"; then echo CRITERION-89-FALSIFIER-OK; else echo CRITERION-89-FALSIFIER-VACUOUS; fi
# ---- 90: a wave whose seat names are in use by another lane's concurrent wave is refused; a lane-unique spec passes
python3 "$Q/seat-name-check.py" "$L/.ufo/waves/round-46/spec-w1.json" --hours 100000 | grep -E 'COLLISION (MutC1Counter|ScribeQuality)' | head -2; bad=${PIPESTATUS[0]}
python3 - "$L/.ufo/waves/round-46/spec-w1.json" "$T/unique.json" <<'P'
import json,sys
s=json.load(open(sys.argv[1]))
for i in s['items']: i['name']='T46'+i['name']
json.dump(s,open(sys.argv[2],'w'))
P
python3 "$Q/seat-name-check.py" "$T/unique.json" --hours 100000 | tail -1; good=${PIPESTATUS[0]}
echo "c90 shared_names_exit=$bad unique_names_exit=$good"
[ "$bad" = 1 ] && [ "$good" = 0 ] && echo CRITERION-90-FALSIFIER-OK || echo CRITERION-90-FALSIFIER-VACUOUS
rm -rf "$T"
