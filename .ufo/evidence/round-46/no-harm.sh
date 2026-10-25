#!/bin/bash
# Round-46 no-harm monitors. Usage: no-harm.sh LANE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# Round-bound counters (the round-44 record-agreement counter) are deliberately NOT here: it is red at
# the round-45 base by construction (corpus/lessons/round-45-verifier-spotcheck.md defect 1).
LANE=$1; REV=$2
cd "$LANE" || exit 2
D=$(git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))')
[ "$D" = "recorded_cases=9 depth_score=9" ] && s=ok || s=RED; echo "NOHARM commandD $D $s"
CR=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print("score=%s box3_full_page=%s" % (d["calibration_restraint_score"], d["coldread"]["box3_full_page"]))')
[ "$CR" = "score=6 box3_full_page=False" ] && s=ok || s=RED; echo "NOHARM coldread $CR $s"
F=$(python3 .ufo/evidence/round-45/freshness/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'population=[0-9]+|fresh=[0-9]+|C1_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$F" = "population=73 fresh=71 C1_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-freshness $F$s"
G=$(python3 .ufo/evidence/round-45/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C2_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$G" = "rows=2 entries=2 C2_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-coverage $G$s"
S=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ')
[ "$S" = 1 ] && s=ok || s=RED; echo "NOHARM S160-count $S $s"
R=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$R" -ge 117 ] && s=ok || s=RED; echo "NOHARM registry-rows-not-below-117 $R $s"
