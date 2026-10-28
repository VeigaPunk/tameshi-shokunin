#!/bin/bash
# T55W2CritCalibrationMove -- second battery. P4b/P7/P10/P11 plant the OLD defect text
# back outside the corrections section (the stale arm R54.4-R54.8/R54.10 never scans for
# it); P8 moves the tree under a corrected row; P9 breaks the corrected value; P5 puts a
# stale claim inside the corrections block (excluded from the stale scan, which runs to EOF).
#
#   plants2.sh LANE C0 COUNTER SCRATCH OUTDIR
set -u
LANE=$1; C0=$2; C1=$3; SCR=$4; OUT=$5
G=(git -c user.name=plant -c user.email=plant@invalid)
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1

clone_at () {
  local d="$SCR/$1"
  rm -rf -- "$d"
  git clone --shared --quiet "$LANE" "$d" >/dev/null 2>&1 || return 1
  git -C "$d" checkout --quiet -B r55 "$C0" >/dev/null 2>&1 || return 1
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || return 1
  printf '%s' "$d"
}
commit () { git -C "$1" add -A >/dev/null && "${G[@]}" -C "$1" commit --quiet -m "$2"; }
score () {
  local w="$SCR/w-$1"; rm -rf -- "$w"; mkdir -p "$w"
  python3 "$C1" --lane "$SCR/$1" --rev "$(git -C "$SCR/$1" rev-parse HEAD)" \
          --work "$w" --explain > "$OUT/$1.stdout" 2>&1
  echo "exit=$?"
  tail -1 "$OUT/$1.stdout"
}
# insert BEFORE the corrections heading (SCORECARD's round-54 section ends at line 2620)
ins_before_corr () {  # ins_before_corr FILE TEXT
  python3 - "$1" "$2" <<'PY'
import sys
p, t = sys.argv[1], sys.argv[2]
body = open(p).read()
h = "## Round 55 - round-54 record corrections"
i = body.index(h)
open(p, "w").write(body[:i] + t + "\n\n" + body[i:])
PY
}

d=$(clone_at p4b) || exit 2
ins_before_corr "$d/SCORECARD.md" "| round-54 phase-B positive control | \`CTL_POS_c1 true\` (re-stated) |"
commit "$d" "plant P4b: exact R54.1 literal before the corrections block"
echo "PLANT P4b_exact_literal_before_corrections (class R54.1)"; score p4b

d=$(clone_at p10) || exit 2
ins_before_corr "$d/SCORECARD.md" "| round-54 C2 counter digest | \`49280fe5\` (re-stated) |"
commit "$d" "plant P10: exact R54.4 stale digest, record side"
echo "PLANT P10_old_digest_49280fe5 (class R54.4, row has stale=[] )"; score p10

d=$(clone_at p11) || exit 2
ins_before_corr "$d/SCORECARD.md" "| round-54 wave findings | 25 wave-1; 22 wave-2 in 9 sections |"
commit "$d" "plant P11: exact R54.5 stale finding counts"
echo "PLANT P11_old_counts_25_22 (class R54.5, row has stale=[] )"; score p11

d=$(clone_at p7) || exit 2
printf '\nThe round-54 C2 base receipt names `total=12` for the lane record.\n' >> "$d/LOG.md"
commit "$d" "plant P7: fresh wrong total inside LOG.md (a record file)"
echo "PLANT P7_fresh_total_12_in_LOG"; score p7

d=$(clone_at p8) || exit 2
sed -i 's/^total=13$/total=15/' "$d/.ufo/evidence/round-54/before/c2.stdout"
commit "$d" "plant P8: the tree moves under the corrected row"
echo "PLANT P8_tree_moves_receipt_total_15 (class R54.3)"; score p8

d=$(clone_at p9) || exit 2
python3 - "$d/SCORECARD.md" <<'PY'
import sys
p = sys.argv[1]; body = open(p).read()
old = "Old: `total=14` in the C2 claim row. Corrected: `total=13`."
assert body.count(old) == 1, body.count(old)
open(p, "w").write(body.replace(old, "Old: `total=14` in the C2 claim row. Corrected: `total=12`."))
PY
commit "$d" "plant P9: corrections section states a wrong derived value"
echo "PLANT P9_corrections_wrong_value (class R54.3)"; score p9

d=$(clone_at p5) || exit 2
python3 - "$d/SCORECARD.md" <<'PY'
import sys
p = sys.argv[1]
open(p, "a").write("\n**Appendix (inside this section).** Old: `CTL_POS_c1 true`; "
                   "the round-54 counter's positive control prints `rekeyed=7/7`; "
                   "`7883e0e5` was the freeze pointer; the other 84 staged `merge/tameshi` "
                   "entries; `49280fe5` is the deciding digest.\n")
PY
commit "$d" "plant P5: stale claims inside the corrections block (section runs to EOF)"
echo "PLANT P5_stale_inside_corrections_to_EOF"; score p5
