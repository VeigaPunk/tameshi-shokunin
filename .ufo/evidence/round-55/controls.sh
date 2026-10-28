#!/bin/bash
# Round-55 controls. Phase A is scored at the FREEZE bytes, before any round work;
# phase B at the final content revision, before the deciding run.
#
#   controls.sh a LANE FREEZE BASE OUTDIR
#   controls.sh b LANE FREEZE REV  OUTDIR
#
# Every control runs the FROZEN counter bytes (extracted from FREEZE into scratch) over a
# `git clone --shared` of the lane at the revision the control names, and is RE-SCORED at
# that same revision (round 54's phase-B control cloned the freeze commit, which predates
# the work it was meant to certify - routed as R54.1). Prints "CTL <name> <counter line>"
# and "CONTROLS_A/B: <n>/<n> as pre-registered" (exit 0 iff every control printed the
# pre-registered verdict). Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r55/controls-*, removed on exit.
set -u
PHASE=$1; LANE=$2; FREEZE=$3; REV=$4; OUT=$5
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
E=.ufo/evidence/round-55
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r55/controls-$PHASE
rm -rf "$SCR"; mkdir -p "$SCR/code" "$SCR/clones"; trap 'rm -rf -- "$SCR"' EXIT
export TMPDIR="$SCR"
cd "$LANE" || exit 2
FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
for f in c1/measure.py c2/measure.py; do
  mkdir -p "$SCR/code/$(dirname $f)"; git show "$FREEZE:$E/$f" > "$SCR/code/$f" || exit 2
done
C1="$SCR/code/c1/measure.py"; C2="$SCR/code/c2/measure.py"
pass=0; fail=0
check () { if [ "$2" = "$3" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "CTL_MISMATCH $1 expected=$2 actual=$3"; fi; }
clone_at () {  # clone_at SRC REV NAME -> path
  local d="$SCR/clones/$3"; git clone --shared --quiet "$1" "$d" >/dev/null 2>&1 || return 1
  git -C "$d" -c advice.detachedHead=false checkout --quiet "$2" >/dev/null 2>&1 || return 1
  printf '%s' "$d"
}
verdict () { grep -oE "$2=(true|false)" "$1" | tail -1 | cut -d= -f2; }
score () {  # score COUNTER CLONE TAG WORKPREFIX -> echoes verdict, leaves receipt at $SCR/<tag>.out
  local py=$1 d=$2 tag=$3 w=$4
  python3 "$py" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/$w" > "$SCR/$tag.out" 2>&1
  tail -1 "$SCR/$tag.out"
}
mkwork () { mkdir -p "$SCR/$1"; }
gitcommit () {  # gitcommit CLONE MESSAGE
  local env=(-c user.name=ctl -c user.email=ctl@invalid)
  git -C "$1" add -A >/dev/null
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$1" "${env[@]}" commit --quiet -m "$2"
}

if [ "$PHASE" = a ]; then
  # CTL_0 -- do nothing: the base tree must fail both counters.
  d=$(clone_at "$LANE" "$REV" base) || exit 2
  mkwork w0a; score "$C1" "$d" c0a w0a >/dev/null; v=$(verdict "$SCR/c0a.out" C1_R55_PASS)
  echo "CTL CTL_0_c1 $(tail -1 "$SCR/c0a.out")"; check CTL_0_c1 false "$v"
  mkwork w0b; score "$C2" "$d" c0b w0b >/dev/null; v=$(verdict "$SCR/c0b.out" C2_R55_PASS)
  echo "CTL CTL_0_c2 $(tail -1 "$SCR/c0b.out")"; check CTL_0_c2 false "$v"

  # CTL_SKIP_c1 -- the cheapest way to skip the work: paste a corrections block carrying
  # every corrected value, fix no stale assertion. The counter must refuse it.
  d=$(clone_at "$LANE" "$REV" skip1) || exit 2
  ADD=$(git -C "$LANE" log --format=%H --diff-filter=A "$REV" -- .ufo/waves/round-54/w2/T54W2Sent03.md | head -1 | cut -c1-7)
  REN=$(git -C "$LANE" log --format=%H --diff-filter=R "$REV" -- .ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json | head -1 | cut -c1-7)
  cat >> "$d/SCORECARD.md" <<EOF

## Round 55 - round-54 record corrections

values-only control: CTL_MISMATCH expected=true actual=false 2/3 077d431e total=13
8528ee85 c2/measure.py w1=28 w2=25 sections=12 $ADD renamed $REN config.yml
fabricated superseded reviewers=5 attack=21/76 seats=76 staged=81
controls-a.stdout rekeyed=0/7 r53-counter-at-88afa941
EOF
  gitcommit "$d" "skip control: values without the fix" || exit 2
  mkwork wsk1; score "$C1" "$d" csk1 wsk1 >/dev/null; v=$(verdict "$SCR/csk1.out" C1_R55_PASS)
  echo "CTL CTL_SKIP_c1 $(tail -1 "$SCR/csk1.out")"; check CTL_SKIP_c1 false "$v"

  # CTL_FAB_c1 -- a corrections block whose values are invented: the corrected arm must
  # bind to the derived value, not to a plausible literal.
  d=$(clone_at "$LANE" "$REV" fab1) || exit 2
  cat >> "$d/SCORECARD.md" <<'EOF'

## Round 55 - round-54 record corrections

fabricated control: CTL_MISMATCH 9/9 deadbeef00 deadbeef total=9999
deadbeef c2/measure.py w1=99 w2=99 sections=99 0000000 renamed 0000000 config.yml
fabricated superseded reviewers=99 attack=99/99 seats=99 staged=999
controls-a.stdout rekeyed=0/99 r53-counter-at-999999
EOF
  gitcommit "$d" "fabricated control" || exit 2
  mkwork wfab1; score "$C1" "$d" cfab1 wfab1 >/dev/null; v=$(verdict "$SCR/cfab1.out" C1_R55_PASS)
  echo "CTL CTL_FAB_c1 $(tail -1 "$SCR/cfab1.out")"; check CTL_FAB_c1 false "$v"

  # CTL_SKIP_c2 -- documentation only (cells, note, one SKILL.md line), no tool edited:
  # the grammar arm must still refuse the two tools that print the raw exception type.
  d=$(clone_at "$LANE" "$REV" skip2) || exit 2
  python3 - "$d" <<'PY'
import json, sys, pathlib
lane = pathlib.Path(sys.argv[1])
mark = "could-not-evaluate: cannot create clone scratch under the scratch root"
reg = json.loads((lane / "tools/registry.json").read_text())
for row in reg["rows"]:
    if row.get("scratch_root"):
        row["scratch_root"] = row["scratch_root"] + " | control: " + mark
(lane / "tools/registry.json").write_text(json.dumps(reg, indent=1) + "\n")
note = lane / "corpus/knowledge/scratch-root-contract.md"
modes = ["env-diff --selftest", "env-diff --contract", "repeat-control --selftest",
         "registry-check --selftest", "bash-witness-study selftest",
         "pin-disposition --selftest", "evidence-disposition --selftest",
         "context-capture --selftest"]
note.write_text(note.read_text() + "\n\n" + mark + "\n\n" + ", ".join(modes) + "\n")
skill = lane / "SKILL.md"
skill.write_text(skill.read_text() + "\n<!-- control: " + mark + " -->\n")
PY
  gitcommit "$d" "skip control: documentation only" || exit 2
  mkwork wsk2; score "$C2" "$d" csk2 wsk2 >/dev/null; v=$(verdict "$SCR/csk2.out" C2_R55_PASS)
  echo "CTL CTL_SKIP_c2 $(tail -1 "$SCR/csk2.out")"; check CTL_SKIP_c2 false "$v"

  echo "CONTROLS_A: $pass/$((pass+fail)) as pre-registered"
  [ "$fail" = 0 ] || exit 1
  exit 0
fi

if [ "$PHASE" = b ]; then
  # CTL_POS -- the real repair AT THE REVISION IT CERTIFIES must pass both counters.
  d=$(clone_at "$LANE" "$REV" pos) || exit 2
  mkwork wposa; score "$C1" "$d" cposa wposa >/dev/null; v=$(verdict "$SCR/cposa.out" C1_R55_PASS)
  echo "CTL CTL_POS_c1 $(tail -1 "$SCR/cposa.out")"; check CTL_POS_c1 true "$v"
  mkwork wposb; score "$C2" "$d" cposb wposb >/dev/null; v=$(verdict "$SCR/cposb.out" C2_R55_PASS)
  echo "CTL CTL_POS_c2 $(tail -1 "$SCR/cposb.out")"; check CTL_POS_c2 true "$v"

  # CTL_BREAK_c2 -- put the raw exception type back on ONE tool's class line: the grammar
  # arm must lose exactly that mode.
  d=$(clone_at "$LANE" "$REV" brk) || exit 2
  python3 - "$d" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1]) / "tools/repeat-control.py"
src = path.read_text()
old = 'emit_err(f"repeat-control: could-not-evaluate: {exc}")'
assert src.count(old) == 1, "anchor not unique: %d" % src.count(old)
path.write_text(src.replace(old, 'emit_err(f"repeat-control: setup: RuntimeError: {exc}")'))
PY
  gitcommit "$d" "break control: raw exception type on one line" || exit 2
  mkwork wbrk; score "$C2" "$d" cbrk wbrk >/dev/null; v=$(verdict "$SCR/cbrk.out" C2_R55_PASS)
  echo "CTL CTL_BREAK_c2 $(tail -1 "$SCR/cbrk.out")"; check CTL_BREAK_c2 false "$v"

  echo "CONTROLS_B: $pass/$((pass+fail)) as pre-registered"
  [ "$fail" = 0 ] || exit 1
  exit 0
fi
echo "phase must be a or b"; exit 2
