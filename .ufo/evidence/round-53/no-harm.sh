#!/bin/bash
# Round-53 no-harm monitors. Usage: no-harm.sh LANE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# The eleven round-52 monitors are carried with declared re-bases (registry-rows floor 134; tools-scope allows
# the round-53 C2-declared tool edits M:tools/registry-check.py + M:tools/env-diff.py alongside the round-52
# pair), plus one new monitor:
#  - r53-scratch-hygiene: no dir="/tmp"-class hardcode under tools/ at REV (the C2 surface; the full C2 claim
#    additionally runs both selftests, the CR47 arm and the SKILL.md doc check in its own counter).
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r53/no-harm, removed on exit.
LANE=$1; REV=$2
BASE=ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r53/no-harm
cd "$LANE" || exit 2
rm -rf "$SCR"; mkdir -p "$SCR"; trap 'rm -rf -- "$SCR"' EXIT; export TMPDIR="$SCR"
D=$(git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))')
python3 -c 'import sys; sys.exit(0 if int(sys.argv[1].split("depth_score=")[1]) >= 10 else 1)' "$D" && s=ok || s=RED; echo "NOHARM commandD $D $s"
CR=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print("score=%s credited=%d" % (d["calibration_restraint_score"], d["coldread"]["sections_covered"]))')
python3 -c 'import sys; s=dict(kv.split("=") for kv in sys.argv[1].split()); sys.exit(0 if int(s["score"])>=8 and int(s["credited"])>=64 else 1)' "$CR" && s=ok || s=RED; echo "NOHARM coldread-floor $CR $s"
F=$(python3 .ufo/evidence/round-45/freshness/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'population=[0-9]+|fresh=[0-9]+' | tr '\n' ' ')
python3 -c 'import sys; s=dict(kv.split("=") for kv in sys.argv[1].split()); p=int(s["population"]); f=int(s["fresh"]); print("score=%d" % (10*f//p)); sys.exit(0 if f>=71 and 10*f//p>=9 else 1)' "$F" > "$SCR/fs" && s=ok || s=RED; echo "NOHARM r45-freshness ${F}$(cat "$SCR/fs") $s"
G=$(python3 .ufo/evidence/round-45/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C2_R45_PASS=[a-z]+' | tr '\n' ' ')
[ "$G" = "rows=2 entries=2 C2_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-coverage $G$s"
S=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ')
[ "$S" = 1 ] && s=ok || s=RED; echo "NOHARM S160-count $S $s"
R=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$R" -ge 134 ] && s=ok || s=RED; echo "NOHARM registry-rows-not-below-134 $R $s"
H=$(python3 .ufo/evidence/round-46/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R46_PASS=[a-z]+' | tr '\n' ' ')
[ "$H" = "rows=3 entries=3 C3_R46_PASS=true " ] && s=ok || s=RED; echo "NOHARM r46-coverage $H$s"
I=$(python3 .ufo/evidence/round-47/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R47_PASS=[a-z]+' | tr '\n' ' ')
[ "$I" = "rows=3 entries=3 C3_R47_PASS=true " ] && s=ok || s=RED; echo "NOHARM r47-coverage $I$s"
T=$(git diff --name-status --no-renames "$BASE" "$REV" -- tools | tr '\t' ':' | tr '\n' ' ')
s=ok; for t in $T; do case "$t" in M:tools/registry.json|M:tools/round21-measure.py|M:tools/registry-check.py|M:tools/env-diff.py) ;; *) s=RED;; esac; done
echo "NOHARM tools-scope [${T}] $s"
git show "$REV:tools/pbt-staged-id.py" > "$SCR/pbt.py"; git show "$REV:tools/staged-id-guard.py" > "$SCR/guard.py"
P=$(cd "$SCR" && python3 -I "$SCR/pbt.py" --guard "$SCR/guard.py" --seed 4949 --cases 400 --dump "$SCR/d.jsonl" | tail -1)
[ "$P" = "PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31" ] && s=ok || s=RED
echo "NOHARM r49-generator-capability [$P] $s"
git show "$REV:tools/shrink-case.py" > "$SCR/shrink.py"
K=$(cd "$SCR" && python3 -I "$SCR/shrink.py" --selftest 2>&1 | tail -1)
case "$K" in *" failed=0") s=ok;; *) s=RED;; esac; echo "NOHARM r50-shrinker-selftest [$K] $s"
Q=$(git grep -c -E 'dir\s*=\s*["\']/tmp' "$REV" -- tools/ 2>/dev/null | awk -F: '{s+=$NF} END {print s+0}')
[ "$Q" = 0 ] && s=ok || s=RED; echo "NOHARM r53-scratch-hygiene tmp_hits=$Q $s"
