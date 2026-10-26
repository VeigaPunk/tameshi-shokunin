#!/bin/bash
# Round-49 no-harm monitors. Usage: no-harm.sh LANE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# Nine monitors: round 48's eight, with the cold-read line turned into a floor (C1 is allowed to raise it, never
# to lower it: credited >= 57 and score >= 6, the base values at 8ca67421), plus a tools-scope monitor (the only
# tools/ change allowed this round is the added generator tools/pbt-staged-id.py; every pinned tool stays byte-equal).
# Round-bound record-agreement counters are deliberately NOT here (QUALITY criterion 88).
LANE=$1; REV=$2
BASE=8ca67421111fa354b47b803358391d0b07fc6db9
cd "$LANE" || exit 2
D=$(git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))')
[ "$D" = "recorded_cases=9 depth_score=9" ] && s=ok || s=RED; echo "NOHARM commandD $D $s"
CR=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print("score=%s credited=%d" % (d["calibration_restraint_score"], d["coldread"]["sections_covered"]))')
python3 -c 'import sys; s=dict(kv.split("=") for kv in sys.argv[1].split()); sys.exit(0 if int(s["score"])>=6 and int(s["credited"])>=57 else 1)' "$CR" && s=ok || s=RED; echo "NOHARM coldread-floor $CR $s"
F=$(python3 .ufo/evidence/round-45/freshness/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'population=[0-9]+|fresh=[0-9]+|C1_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$F" = "population=73 fresh=71 C1_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-freshness $F$s"
G=$(python3 .ufo/evidence/round-45/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C2_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$G" = "rows=2 entries=2 C2_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-coverage $G$s"
S=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ')
[ "$S" = 1 ] && s=ok || s=RED; echo "NOHARM S160-count $S $s"
R=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$R" -ge 128 ] && s=ok || s=RED; echo "NOHARM registry-rows-not-below-128 $R $s"
H=$(python3 .ufo/evidence/round-46/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R46_PASS=[a-z]+' | tr '\n' ' ')
[ "$H" = "rows=3 entries=3 C3_R46_PASS=true " ] && s=ok || s=RED; echo "NOHARM r46-coverage $H$s"
I=$(python3 .ufo/evidence/round-47/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R47_PASS=[a-z]+' | tr '\n' ' ')
[ "$I" = "rows=3 entries=3 C3_R47_PASS=true " ] && s=ok || s=RED; echo "NOHARM r47-coverage $I$s"
T=$(git diff --name-status --no-renames "$BASE" "$REV" -- tools | tr '\t\n' ': ')
case "$T" in ""|"A:tools/pbt-staged-id.py ") s=ok;; *) s=RED;; esac; echo "NOHARM tools-scope [${T}] $s"
