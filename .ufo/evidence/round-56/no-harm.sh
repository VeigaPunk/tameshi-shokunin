#!/bin/bash
# Round-56 no-harm monitors. Usage: no-harm.sh LANE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# Carried from round 55 with three declared re-bases: tools-scope admits the one new tool this round adds
# (tools/receipt-revision-gate.py) and the registry file whose cells it grows, registry-row-names becomes
# registry-rows-not-shrunk (a cell for the new tool is an addition, not a rename), and the cold-read floor
# stays at 64/64 because the re-key is this round's C1 obligation.
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r56/no-harm, removed on exit.
LANE=$1; REV=$2
BASE=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r56/no-harm
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
[ "$R" -ge 140 ] && s=ok || s=RED; echo "NOHARM registry-rows-not-below-140 $R $s"
H=$(python3 .ufo/evidence/round-46/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R46_PASS=[a-z]+' | tr '\n' ' ')
[ "$H" = "rows=3 entries=3 C3_R46_PASS=true " ] && s=ok || s=RED; echo "NOHARM r46-coverage $H$s"
I=$(python3 .ufo/evidence/round-47/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 | grep -oE 'rows=[0-9]+|entries=[0-9]+|C3_R47_PASS=[a-z]+' | tr '\n' ' ')
[ "$I" = "rows=3 entries=3 C3_R47_PASS=true " ] && s=ok || s=RED; echo "NOHARM r47-coverage $I$s"
T=$(git diff --name-status --no-renames "$BASE" "$REV" -- tools | tr '\t' ':' | tr '\n' ' ')
s=ok; for t in $T; do case "$t" in M:tools/registry.json|M:tools/registry-check.py|M:tools/env-diff.py|M:tools/bash-witness-study.py|M:tools/context-capture.py|M:tools/evidence-disposition.py|M:tools/pin-disposition.py|M:tools/repeat-control.py|A:tools/receipt-revision-gate.py) ;; *) s=RED;; esac; done
echo "NOHARM tools-scope [${T}] $s"
N0=$(git show "$BASE:tools/registry.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["rows"]))')
N1=$(git show "$REV:tools/registry.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["rows"]))')
[ "$N1" -ge "$N0" ] && s=ok || s=RED; echo "NOHARM registry-rows-not-shrunk base=$N0 rev=$N1 $s"
git show "$REV:tools/pbt-staged-id.py" > "$SCR/pbt.py"; git show "$REV:tools/staged-id-guard.py" > "$SCR/guard.py"
P=$(cd "$SCR" && python3 -I "$SCR/pbt.py" --guard "$SCR/guard.py" --seed 4949 --cases 400 --dump "$SCR/d.jsonl" | tail -1)
[ "$P" = "PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31" ] && s=ok || s=RED
echo "NOHARM r49-generator-capability [$P] $s"
git show "$REV:tools/shrink-case.py" > "$SCR/shrink.py"
K=$(cd "$SCR" && python3 -I "$SCR/shrink.py" --selftest 2>&1 | tail -1)
case "$K" in *" failed=0") s=ok;; *) s=RED;; esac; echo "NOHARM r50-shrinker-selftest [$K] $s"
Q=$(git grep -c -E "dir\\s*=\\s*[\"']/tmp" "$REV" -- tools/ 2>/dev/null | awk -F: "{s+=\$NF} END {print s+0}")
[ "$Q" = 0 ] && s=ok || s=RED; echo "NOHARM r53-scratch-hygiene tmp_hits=$Q $s"
L0=$(git show "$BASE:.ufo/evidence/round-21/coldread/ledger.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["entries"]))')
L1=$(git show "$REV:.ufo/evidence/round-21/coldread/ledger.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["entries"]))')
[ "$L1" -ge "$L0" ] && s=ok || s=RED; echo "NOHARM ledger-not-shrunk base=$L0 rev=$L1 $s"
C0=$(git show "$BASE:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
C1N=$(git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$C1N" -ge "$C0" ] && s=ok || s=RED; echo "NOHARM sources-not-shrunk base=$C0 rev=$C1N $s"
