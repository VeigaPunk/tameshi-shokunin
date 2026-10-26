#!/bin/bash
# Round-50 no-harm monitors. Usage: no-harm.sh LANE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# Ten monitors: round 49's nine with the cold-read floor raised to the round-49 values (score >= 8, credited >= 64,
# observed at base e3729de8), the registry floor raised to 130, the tools-scope monitor allowing only the added
# shrinker and an edit of the round-49 generator (routed defect R49.1), plus the round-49 generator capability
# line, which must print byte-equal to its base output (an error-path fix must not move the generator's classes).
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r50/no-harm, removed on exit.
LANE=$1; REV=$2
BASE=e3729de862f73ae080d98fcf522a7081ce16e40a
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r50/no-harm
cd "$LANE" || exit 2
rm -rf "$SCR"; mkdir -p "$SCR"; trap 'rm -rf -- "$SCR"' EXIT
D=$(git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))')
[ "$D" = "recorded_cases=9 depth_score=9" ] && s=ok || s=RED; echo "NOHARM commandD $D $s"
CR=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print("score=%s credited=%d" % (d["calibration_restraint_score"], d["coldread"]["sections_covered"]))')
python3 -c 'import sys; s=dict(kv.split("=") for kv in sys.argv[1].split()); sys.exit(0 if int(s["score"])>=8 and int(s["credited"])>=64 else 1)' "$CR" && s=ok || s=RED; echo "NOHARM coldread-floor $CR $s"
F=$(python3 .ufo/evidence/round-45/freshness/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'population=[0-9]+|fresh=[0-9]+|C1_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$F" = "population=73 fresh=71 C1_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-freshness $F$s"
G=$(python3 .ufo/evidence/round-45/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C2_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$G" = "rows=2 entries=2 C2_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-coverage $G$s"
S=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ')
[ "$S" = 1 ] && s=ok || s=RED; echo "NOHARM S160-count $S $s"
R=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$R" -ge 130 ] && s=ok || s=RED; echo "NOHARM registry-rows-not-below-130 $R $s"
H=$(python3 .ufo/evidence/round-46/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R46_PASS=[a-z]+' | tr '\n' ' ')
[ "$H" = "rows=3 entries=3 C3_R46_PASS=true " ] && s=ok || s=RED; echo "NOHARM r46-coverage $H$s"
I=$(python3 .ufo/evidence/round-47/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R47_PASS=[a-z]+' | tr '\n' ' ')
[ "$I" = "rows=3 entries=3 C3_R47_PASS=true " ] && s=ok || s=RED; echo "NOHARM r47-coverage $I$s"
T=$(git diff --name-status --no-renames "$BASE" "$REV" -- tools | tr '\t' ':' | tr '\n' ' ')
s=ok; for t in $T; do case "$t" in A:tools/shrink-case.py|M:tools/pbt-staged-id.py) ;; *) s=RED;; esac; done
echo "NOHARM tools-scope [${T}] $s"
git show "$REV:tools/pbt-staged-id.py" > "$SCR/pbt.py"; git show "$REV:tools/staged-id-guard.py" > "$SCR/guard.py"
P=$(cd "$SCR" && TMPDIR="$SCR" python3 -I "$SCR/pbt.py" --guard "$SCR/guard.py" --seed 4949 --cases 400 --dump "$SCR/d.jsonl" | tail -1)
[ "$P" = "PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31" ] && s=ok || s=RED
echo "NOHARM r49-generator-capability [$P] $s"
