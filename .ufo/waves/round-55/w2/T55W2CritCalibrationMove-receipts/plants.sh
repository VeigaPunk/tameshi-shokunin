#!/bin/bash
# T55W2CritCalibrationMove -- does the C1 counter's stale/derived structure generalise
# beyond the ten routed literals?  Each plant is an independent clone of the lane at C0
# with ONE committed record defect of the same class (a number the record asserts that
# the tree contradicts, receipt named), then the frozen C1 counter is run over it.
#
#   plants.sh LANE C0 COUNTER SCRATCH OUTDIR
#
# Prints "PLANT <id> <verdict line>" plus the class that should have moved.
set -u
LANE=$1; C0=$2; C1=$3; SCR=$4; OUT=$5
G=(git -c user.name=plant -c user.email=plant@invalid)
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1

clone_at () {  # clone_at NAME -> path
  local d="$SCR/$1"
  git clone --shared --quiet "$LANE" "$d" >/dev/null 2>&1 || return 1
  git -C "$d" checkout --quiet -B r55 "$C0" >/dev/null 2>&1 || return 1
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || return 1
  printf '%s' "$d"
}
commit () { git -C "$1" add -A >/dev/null && "${G[@]}" -C "$1" commit --quiet -m "$2"; }
score () {  # score CLONE TAG -> echoes verdict line, receipt at $OUT/TAG.stdout
  local w="$SCR/w-$1"; mkdir -p "$w"
  python3 "$C1" --lane "$SCR/$1" --rev "$(git -C "$SCR/$1" rev-parse HEAD)" \
          --work "$w" --explain > "$OUT/$1.stdout" 2>&1
  echo "exit=$?"
  tail -1 "$OUT/$1.stdout"
}
APPENDREC () { printf '%s\n' "$2" >> "$1"; }

# P0 -- do-nothing: the same counter bytes over BASE must still read red.
d=$(clone_at p0) || exit 2
git -C "$d" checkout --quiet -B r55 0a2010acd1e92e4e332774050825e21bcfc7e079
echo "PLANT P0_do_nothing_base"; score p0

# P1 -- same class as R54.3 (a quoted receipt total that disagrees with the receipt),
# different literal: the round-54 base C2 receipt prints total=13, the record now says 12.
d=$(clone_at p1) || exit 2
APPENDREC "$d/SCORECARD.md" ""
APPENDREC "$d/SCORECARD.md" "| round-54 C2 base receipt \`.ufo/evidence/round-54/before/c2.stdout\` | printed \`total=12\` before any repair |"
commit "$d" "plant P1: fresh wrong total with a named receipt"
echo "PLANT P1_fresh_total_12 (class R54.3)"; score p1

# P2 -- same class, this round's own receipt: base C2 prints grammar=6/9, record says 7/9.
d=$(clone_at p2) || exit 2
APPENDREC "$d/SCORECARD.md" ""
APPENDREC "$d/SCORECARD.md" "Round-55 base operability receipt \`.ufo/evidence/round-55/before/c2.stdout\` printed \`grammar=7/9\`."
commit "$d" "plant P2: fresh wrong grammar with a named receipt"
echo "PLANT P2_fresh_grammar_7_of_9"; score p2

# P3 -- a fresh wrong count in QUALITY.md, plausible receipt named (round-54 C1 receipt
# prints credited=60; record says 58).
d=$(clone_at p3) || exit 2
printf '\nThe round-54 C1 base receipt names `credited=58` in the lane record.\n' >> "$d/corpus/QUALITY.md"
commit "$d" "plant P3: fresh wrong count in QUALITY"
echo "PLANT P3_fresh_credited_58"; score p3

# P4 -- regression arm: the EXACT literal R54.1 pinned must be caught again.
d=$(clone_at p4) || exit 2
APPENDREC "$d/SCORECARD.md" ""
APPENDREC "$d/SCORECARD.md" "the round-54 phase-B positive control: CTL_POS_c1 true"
commit "$d" "plant P4: exact stale literal reintroduced"
echo "PLANT P4_exact_literal_reintroduced"; score p4

# P5 -- the corrections section may contradict itself: append the stale claim INSIDE the
# section (excluded from the stale scan) while every token the corrected arm wants stays.
d=$(clone_at p5) || exit 2
python3 - "$d/SCORECARD.md" <<'PY'
import sys, re
p = sys.argv[1]; body = open(p).read()
h = "## Round 55 - round-54 record corrections\n"
i = body.index(h) + len(h)
j = body.index("\n## ", i)
body = body[:j] + "\nER-R54-1 (restated): the positive control prints `rekeyed=7/7` and CTL_MISMATCH was 2/3.\n" + body[j:]
open(p, "w").write(body)
PY
commit "$d" "plant P5: stale claim re-asserted inside the corrections section"
echo "PLANT P5_stale_inside_corrections"; score p5

# P6 -- wrong freeze pointer, again with a literal outside R54.2's two known pointers.
d=$(clone_at p6) || exit 2
APPENDREC "$d/SCORECARD.md" ""
APPENDREC "$d/SCORECARD.md" "| round-54 counter freeze | \`deadbeef0\` (amendments 1-5) |"
commit "$d" "plant P6: fresh wrong freeze pointer"
echo "PLANT P6_fresh_freeze_pointer"; score p6
