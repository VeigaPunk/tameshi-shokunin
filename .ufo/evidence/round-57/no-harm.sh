#!/bin/bash
# Round-57 no-harm monitors. Usage: no-harm.sh LANE BASE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# Carried from round 56 with declared re-bases: BASE is an argument (round-57 base 5e3569969b532310d2b8a3d130901757a3df356b),
# tools-scope admits exactly the round-57 tool changes: M:tools/registry.json, A:tools/cold-read-forecast.py and the three
# A:tools/fixtures/receipt-gate/ files (accept.receipt drift.paths drift.receipt) and nothing else; three monitors are new: r56-gate-selftest,
# registry-check-full (REV held count not below the measured BASE count, 48), old49-ledger (BASE's routed-defects rows unchanged at REV).
# Every monitor reads git objects at REV only (tools are extracted to $SCR). Scratch: $HYAKU_SCRATCH
# (default /fast/scratch/hyaku)/tameshi-r57/no-harm, removed on exit; TMPDIR points there.
LANE=$1; BASE=$2; REV=$3
[ -n "$LANE" ] && [ -n "$BASE" ] && [ -n "$REV" ] || { echo "usage: no-harm.sh LANE BASE REV" >&2; exit 64; }
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/no-harm
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
# round-57 admitted set (exactly five paths): the registry gate rows (M), the cold-read forecast tool (A) and the three receipt-gate fixtures (A).
# No other tool changes: M:tools/receipt-revision-gate.py is NOT admitted (C2 changes registry rows, not the gate itself), no glob admits extra fixtures.
ADM="A:tools/cold-read-forecast.py A:tools/fixtures/receipt-gate/accept.receipt A:tools/fixtures/receipt-gate/drift.paths A:tools/fixtures/receipt-gate/drift.receipt M:tools/registry.json"
s=ok; [ "$(printf '%s\n' $T | LC_ALL=C sort | tr '\n' ' ')" = "$(printf '%s\n' $ADM | LC_ALL=C sort | tr '\n' ' ')" ] || s=RED
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
# --- round-57 additions ---
mkdir -p "$SCR/gate"; git show "$REV:tools/receipt-revision-gate.py" > "$SCR/gate/receipt-revision-gate.py"
GS=$(cd "$SCR/gate" && python3 -I receipt-revision-gate.py --selftest 2>&1 | tail -1)
[ "$GS" = "GATE_SELFTEST: 19/19 pass" ] && s=ok || s=RED; echo "NOHARM r56-gate-selftest [$GS] $s"
# BASE_HELD is the held count of registry-check.py at BASE 5e35699 (measured round 57: REGISTRY_CHECK: held=48/50 superseded=7,
# exit 1 because sources-census and verify-round15 differ in the clone layout; ~620 s wall under host load). Measuring BASE again
# at every run would double the wall time, so the constant is the measured BASE value; pass BASE_HELD=<n> in the env to override.
BASE_HELD=${BASE_HELD:-48}
git show "$REV:tools/registry-check.py" > "$SCR/rc-rev.py" && RV=$(python3 "$SCR/rc-rev.py" --root "$LANE" --rev "$REV" 2>/dev/null | tail -1)
RVH=$(echo "$RV" | sed -nE 's/^REGISTRY_CHECK: held=([0-9]+)\/[0-9]+.*/\1/p')
[ -n "$RVH" ] && [ "$RVH" -ge "$BASE_HELD" ] && s=ok || s=RED; echo "NOHARM registry-check-full base_held=$BASE_HELD rev=[$RV] $s"
python3 -c '
import json,subprocess,sys
def load(r):
    return json.loads(subprocess.run(["git","show",r+":corpus/routed-defects.json"],capture_output=True,check=True).stdout)["defects"]
b=load(sys.argv[1]); v=load(sys.argv[2])
print("base_rows=%d rev_rows=%d" % (len(b), len(v)))
sys.exit(0 if len(v)>=len(b) and v[:len(b)]==b else 1)' "$BASE" "$REV" > "$SCR/o49" 2>&1 && s=ok || s=RED
echo "NOHARM old49-ledger $(tail -1 "$SCR/o49") $s"
