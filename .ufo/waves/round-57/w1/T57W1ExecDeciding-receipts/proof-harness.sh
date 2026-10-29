#!/bin/bash
# Proof harness for deciding-run.sh: builds synthetic stub lanes in scratch and drives the script. Never touches the real lane.
# Usage: proof-harness.sh SCRIPT_UNDER_TEST   (prints one "CASE <name> exit=<n> <first refusal line>" per case)
set -u
SUT=$1
GATE=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/T57W1ExecDeciding-proof; rm -rf "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
export TMPDIR=$S HYAKU_SCRATCH=$S/hy
E=.ufo/evidence/round-57
G() { git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid "$@"; }
# build NAME [c2-verdict true|false] [precheck ok|RED] ; leaves lane at $D with HEAD=REV, BASE in $BASE
build() {
  D=$S/$1; mkdir -p "$D"; git -C "$D" init -q -b main; [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture toplevel mismatch"; exit 9; }
  mkdir -p "$D/tools" "$D/.ufo/evidence/round-48/quality" "$D/$E/c1" "$D/$E/c2" "$D/$E/control"
  cp "$GATE" "$D/tools/receipt-revision-gate.py"
  printf '#!/bin/bash\necho "COLDREAD_PRECHECK floor=x floor_credited=64 cand=y cand_credited=64 lost=0 ok"\n' > "$D/.ufo/evidence/round-48/quality/coldread-precheck.sh"
  echo base > "$D/README"; G add -A; G commit -qm base; BASE=$(git -C "$D" rev-parse HEAD)
  for k in c1 c2; do cat > "$D/$E/$k/measure.py" <<PY
import sys
a = sys.argv; rev = a[a.index('--rev') + 1][:12]
print('explain: stub counter, nothing to explain')
print('${k^^}_R57: rev=%s total=0 ${k^^}_R57_PASS=${2:-true}' % rev if '$k' == 'c2' else '${k^^}_R57: rev=%s total=0 ${k^^}_R57_PASS=true' % rev)
PY
  done
  { echo '#!/bin/bash'; for i in $(seq 1 18); do echo "echo \"NOHARM stub$i 1 ok\""; done; } > "$D/$E/no-harm.sh"
  cat > "$D/$E/contract.json" <<J
{"round": 57, "base": "$BASE", "frozen_paths": ["$E/contract.json", "$E/freeze.json", "$E/c1/measure.py", "$E/c2/measure.py", "$E/no-harm.sh", "$E/deciding-run.sh", "tools/receipt-revision-gate.py"]}
J
  cp "$SUT" "$D/$E/deciding-run.sh"
  [ "${3:-ok}" = RED ] && printf '#!/bin/bash\necho "LOST heading | drifted=x"\necho "COLDREAD_PRECHECK floor=x floor_credited=64 cand=y cand_credited=63 lost=1 RED"\nexit 1\n' > "$D/.ufo/evidence/round-48/quality/coldread-precheck.sh"
  [ -n "${PRE_FREEZE:-}" ] && eval "$PRE_FREEZE"
  python3 - "$D" "$BASE" "$E" <<'PY'
import hashlib, json, sys
d, base, E = sys.argv[1:4]
files = {}
for rel in ('c1/measure.py', 'c2/measure.py', 'no-harm.sh', 'deciding-run.sh', 'contract.json'):
    files[rel] = hashlib.sha256(open('%s/%s/%s' % (d, E, rel), 'rb').read()).hexdigest()
files['tools/receipt-revision-gate.py'] = hashlib.sha256(open(d + '/tools/receipt-revision-gate.py', 'rb').read()).hexdigest()
json.dump({'schema': 'tameshi-freeze-v1', 'round': 57, 'lane': 'tameshi', 'base': base, 'files': files, 'amendments': []},
          open('%s/%s/freeze.json' % (d, E), 'w'), indent=1)
PY
  G add -A; G commit -qm freeze; FREEZE=$(git -C "$D" rev-parse HEAD)
  printf 'CTL CTL_0 x total=1\nCTL_MATCH CTL_0 expected=false actual=false\nCONTROLS_A: 1/1 as pre-registered\n' > "$D/$E/control/controls-a.stdout"
  printf 'CTL CTL_POS y total=0\nCTL_MATCH CTL_POS expected=true actual=true\nCONTROLS_B: 1/1 as pre-registered\n' > "$D/$E/control/controls-b.stdout"
  for ab in a b; do echo 0 > "$D/$E/control/controls-$ab.exit"; sha256sum < "$D/$E/control/controls-$ab.stdout" | awk '{print $1"  controls-'$ab'.stdout"}' > "$D/$E/control/controls-$ab.stdout.sha256"; done
  G add -A; G commit -qm controls; REV=$(git -C "$D" rev-parse HEAD)
  # census stub fleet
  mkdir -p "$S/fleet-$1/scripts"; printf '#!/bin/bash\necho "census ok rows=142"\nexit 0\n' > "$S/fleet-$1/scripts/sources-census.sh"; chmod +x "$S/fleet-$1/scripts/sources-census.sh"
  mkdir -p "$D/$E/after-$1"; OUTD=$D/$E/after-$1
}
run() { # name -- run with args; $@ = LANE BASE REV OUT overrides via vars
  local name=$1; shift
  DECIDING_FLEET=$S/fleet-$CASEDIR bash "$D/$E/deciding-run.sh" "$@" > "$S/$name.out" 2>&1; local rc=$?
  echo "CASE $name exit=$rc :: $(grep -E 'DECIDING_REFUSED|DECIDING_RUN_EXIT' "$S/$name.out" | head -1)"
  cp "$S/$name.out" "${RECEIPTS:-$S}/case-$name.out" 2>/dev/null
}
CASEDIR=happy; build happy
run happy "$D" "$BASE" "$REV" "$OUTD"; ls "$OUTD" | tr '\n' ' '; echo
run happy-second-invocation "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=badrev; build badrev
run wrong-rev-ancestor "$D" "$BASE" "$FREEZE" "$OUTD"
run wrong-rev-unresolvable "$D" "$BASE" deadbeefdeadbeef "$OUTD"
run wrong-base-is-rev "$D" "$REV" "$REV" "$OUTD"
CASEDIR=detached; build detached; G checkout -q --detach "$FREEZE"; run wrong-rev-lane-head-moved "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=tamper1; build tamper1
python3 - "$D/$E/freeze.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d['files']['c1/measure.py'] = '0' * 64; json.dump(d, open(p, 'w'), indent=1)
PY
G commit -qam 'tamper freeze digest'; REV=$(git -C "$D" rev-parse HEAD)
run tampered-freeze-digest "$D" "$BASE" "$REV" "$OUTD"; grep FREEZE_ "$S/tampered-freeze-digest.out"
CASEDIR=tamper2; build tamper2
echo '# edited after freeze' >> "$D/$E/c1/measure.py"; G commit -qam 'edit frozen counter'; REV=$(git -C "$D" rev-parse HEAD)
run tampered-frozen-file-after-freeze "$D" "$BASE" "$REV" "$OUTD"; grep FREEZE_ "$S/tampered-frozen-file-after-freeze.out"
CASEDIR=tamper3; build tamper3
echo '# edited' >> "$D/$E/deciding-run.sh"; G commit -qam 'edit script'; REV=$(git -C "$D" rev-parse HEAD)
DECIDING_FLEET=$S/fleet-tamper3 bash "$SUT" "$D" "$BASE" "$REV" "$OUTD" > "$S/x.out" 2>&1; echo "CASE script-differs-from-committed exit=$? :: $(head -1 "$S/x.out")"
CASEDIR=miss; build miss
G rm -q "$E/c2/measure.py"; G commit -qm 'drop counter'; REV=$(git -C "$D" rev-parse HEAD)
run missing-counter "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=nh; build nh
G rm -q "$E/no-harm.sh"; G commit -qm 'drop no-harm'; REV=$(git -C "$D" rev-parse HEAD)
run missing-no-harm "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=ctl; build ctl
echo 'CTL_MISMATCH CTL_0 expected=false actual=true' >> "$D/$E/control/controls-a.stdout"; sha256sum < "$D/$E/control/controls-a.stdout" | awk '{print $1"  controls-a.stdout"}' > "$D/$E/control/controls-a.stdout.sha256"
G commit -qam 'mismatch line'; REV=$(git -C "$D" rev-parse HEAD)
run ctl-mismatch "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=ctlb; build ctlb
printf 'CTL CTL_POS y\nCTL_MISMATCH CTL_POS expected=true actual=false\nCONTROLS_B: 1/2 as pre-registered\n' > "$D/$E/control/controls-b.stdout"; sha256sum < "$D/$E/control/controls-b.stdout" | awk '{print $1"  controls-b.stdout"}' > "$D/$E/control/controls-b.stdout.sha256"
G commit -qam 'b 1/2'; REV=$(git -C "$D" rev-parse HEAD)
run controls-b-verdict-missing "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=noctl; build noctl
G rm -q "$E/control/controls-b.stdout" "$E/control/controls-b.exit" "$E/control/controls-b.stdout.sha256"; G commit -qm 'drop controls-b'; REV=$(git -C "$D" rev-parse HEAD)
run control-receipt-missing "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=red; build red true RED
run precheck-red "$D" "$BASE" "$REV" "$OUTD"; ls "$OUTD" | wc -l
CASEDIR=c2f; build c2f false
run counter-fails-pass-false "$D" "$BASE" "$REV" "$OUTD"; grep -E 'COUNTER_|DECIDING_RUN' "$S/counter-fails-pass-false.out"
CASEDIR=dirty; build dirty
echo x > "$D/stray.txt"; run dirty-tree "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=dirty2; build dirty2
echo y > "$OUTD/preexisting"; run outdir-not-empty "$D" "$BASE" "$REV" "$OUTD"
CASEDIR=out; build out
run outdir-missing "$D" "$BASE" "$REV" "$D/$E/nope"
run outdir-outside-lane "$D" "$BASE" "$REV" "$S"
run relative-lane relative "$BASE" "$REV" "$OUTD"
# extra cases (stub edits applied BEFORE the freeze digest, so the freeze is honest): final-gate refusal, no-harm RED, too few monitors, non-zero counter exit
CASEDIR=gate; PRE_FREEZE='echo "print(\"C1_R57: rev=deadbeefdead total=0 C1_R57_PASS=true\")" > "$D/$E/c1/measure.py"' build gate
run final-gate-refuses-verdict-naming-unresolvable-rev "$D" "$BASE" "$REV" "$OUTD"; grep -E '^GATE' "$S/final-gate-refuses-verdict-naming-unresolvable-rev.out"
CASEDIR=nhred; PRE_FREEZE='echo "echo \"NOHARM stubRED 0 RED\"" >> "$D/$E/no-harm.sh"' build nhred
run no-harm-red "$D" "$BASE" "$REV" "$OUTD"; grep -E 'NOHARM_' "$S/no-harm-red.out"
CASEDIR=nhfew; PRE_FREEZE='sed -i "/stub1[0-8] /d" "$D/$E/no-harm.sh"' build nhfew
run no-harm-too-few "$D" "$BASE" "$REV" "$OUTD"; grep -E 'NOHARM_' "$S/no-harm-too-few.out"
CASEDIR=cexit; PRE_FREEZE='echo "sys.exit(4)" >> "$D/$E/c2/measure.py"' build cexit
run counter-exit-nonzero "$D" "$BASE" "$REV" "$OUTD"; grep -E 'COUNTER_' "$S/counter-exit-nonzero.out"
