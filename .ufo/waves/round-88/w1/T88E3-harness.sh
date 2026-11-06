#!/usr/bin/env bash
# T88E3 — no-harm sweep of the round-88 runner change (tameshi round 88, lane tameshi).
#
# Re-executes every measurement quoted in T88E3.md:
#   item 1  classify every line REMOVED by the runner diff base -> candidate
#   item 2  run the candidate runner's own --selftest from a `git show` extraction
#   item 3  run --regression at the candidate and compare the ten historical legs
#           with the frozen pre-freeze receipt
#   extra   two strictness probes (guards still catch an 11th-leg omission)
#
# Read-only on the lane and the fleet: clones/extractions/work dirs live under
# SCRATCH (removed on exit); receipts are written to OUT (default: the wave-1
# deliverable dir), so re-running this script regenerates the quoted outputs.
#
# usage: T88E3-harness.sh [all|diff|selftest|regression|probes]   (default: all)
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
BASE=f256302b394ae3253df014fe1131e2c20e2c16b6
CAND=28ec58858a084bc193a89ca5b0a751942694ccfb
RECEIPT=$LANE/.ufo/evidence/round-88/pre-freeze/runner-regression-base.txt
MODE=${1:-all}

SEAT=T88E3
SCRATCH=/fast/scratch/hyaku/tameshi-r88/$SEAT
OUT=${OUT:-$LANE/.ufo/waves/round-88/w1}
mkdir -p "$SCRATCH" "$OUT"
trap 'rm -rf -- "$SCRATCH"' EXIT
export LC_ALL=C TMPDIR=$SCRATCH

# --- a fleet root whose tameshi-shokunin/tools/<runner> is the extracted revision,
# --- every sibling repo symlinked from the real fleet (the runner resolves the
# --- fleet root from its own location: dirname(dirname($SELF))).
make_fleet() { # make_fleet <dir> <rev>
  local root=$1 rev=$2 b
  mkdir -p "$root/tameshi-shokunin/tools"
  for d in "$FLEET"/*; do
    b=$(basename "$d"); [ "$b" = tameshi-shokunin ] && continue
    ln -sfn "$d" "$root/$b"
  done
  git -C "$LANE" show "$rev":tools/mutate-and-run.sh > "$root/tameshi-shokunin/tools/mutate-and-run.sh"
  chmod 755 "$root/tameshi-shokunin/tools/mutate-and-run.sh"
  sha256sum "$root/tameshi-shokunin/tools/mutate-and-run.sh"
}

# ---------------------------------------------------------------- item 1
do_diff() {
  git -C "$LANE" diff -U0 "$BASE" "$CAND" -- tools/mutate-and-run.sh > "$OUT/T88E3-diff-u0.diff"
  awk '
    /^@@/ { split($2,a,","); start=substr(a[1],2)+0; nh++; hstart[nh]=start; next }
    /^-/ { cnt[nh]++; text[nh,cnt[nh]]=substr($0,2) }
    END {
      tot=0
      for (i=1;i<=nh;i++) { printf "HUNK %2d  old=%d removed=%d\n", i, hstart[i]+1, cnt[i]; tot+=cnt[i]
        for (j=1;j<=cnt[i];j++) printf "    | %s\n", text[i,j] }
      printf "TOTAL_REMOVED=%d HUNKS=%d\n", tot, nh
    }' "$OUT/T88E3-diff-u0.diff" | tee "$OUT/T88E3-removed-by-hunk.txt" | grep -E '^(HUNK|TOTAL)'
}

# ---------------------------------------------------------------- item 2
do_selftest() {
  local root=$SCRATCH/fleet-cand broot=$SCRATCH/fleet-base sha
  sha=$(make_fleet "$root" "$CAND")
  printf 'CANDIDATE_RUNNER %s\n' "$sha"
  ( cd "$SCRATCH" && bash "$root/tameshi-shokunin/tools/mutate-and-run.sh" --selftest ) \
    > "$OUT/T88E3-selftest-candidate.out" 2>&1
  echo "candidate_selftest_exit=$?"
  grep -E '^FAIL ' "$OUT/T88E3-selftest-candidate.out" || echo 'candidate failing cases: none'
  grep -E '^(MUTATE_SELFTEST|VERDICT)' "$OUT/T88E3-selftest-candidate.out"

  # base selftest, so a vanished pre-existing case would be visible
  make_fleet "$broot" "$BASE" >/dev/null
  ( cd "$SCRATCH" && bash "$broot/tameshi-shokunin/tools/mutate-and-run.sh" --selftest ) \
    > "$OUT/T88E3-selftest-base.out" 2>&1
  echo "base_selftest_exit=$?"
  grep -E '^(MUTATE_SELFTEST|VERDICT)' "$OUT/T88E3-selftest-base.out"
  sed -n 's/^PASS //p' "$OUT/T88E3-selftest-base.out" | sort -u > "$SCRATCH/base-cases.txt"
  sed -n 's/^PASS //p' "$OUT/T88E3-selftest-candidate.out" | sort -u > "$SCRATCH/cand-cases.txt"
  echo "base_cases=$(wc -l < "$SCRATCH/base-cases.txt") cand_cases=$(wc -l < "$SCRATCH/cand-cases.txt") shared=$(comm -12 "$SCRATCH/base-cases.txt" "$SCRATCH/cand-cases.txt" | wc -l)"
  echo '--- base cases with no verbatim candidate counterpart (each is a 10->11 rename; eyeball) ---'
  comm -23 "$SCRATCH/base-cases.txt" "$SCRATCH/cand-cases.txt"
  echo '--- candidate cases not in base (the 11-leg counterparts + one new leg case) ---'
  comm -13 "$SCRATCH/base-cases.txt" "$SCRATCH/cand-cases.txt"
}

# ---------------------------------------------------------------- item 3
do_regression() {
  local root=$SCRATCH/fleet-cand
  [ -x "$root/tameshi-shokunin/tools/mutate-and-run.sh" ] || make_fleet "$root" "$CAND" >/dev/null
  mkdir -p "$SCRATCH/reg"
  bash "$root/tameshi-shokunin/tools/mutate-and-run.sh" --regression --workdir "$SCRATCH/reg" --keep \
    > "$OUT/T88E3-regression-candidate.out" 2>&1
  echo "candidate_regression_exit=$?"
  grep -E '^(REGRESSION: |REGRESSION_EXPECT)' "$OUT/T88E3-regression-candidate.out"

  grep -E '^REGRESSION_(PIN|SWEEP|TABLE|CASE) ' "$RECEIPT" | sort > "$SCRATCH/base-legs.txt"
  # repo= in PIN lines echoes the fleet root the runner was pointed at; normalize it
  # back to the fleet path the frozen receipt used, then drop the new eleventh leg.
  sed "s#repo=$root/#repo=$FLEET/#" "$OUT/T88E3-regression-candidate.out" \
    | grep -E '^REGRESSION_(PIN|SWEEP|TABLE|CASE) ' | grep -v 'py-kake-ledger-guard' | sort \
    > "$SCRATCH/cand-ten-legs.txt"
  echo "base_leg_lines=$(wc -l < "$SCRATCH/base-legs.txt") cand_leg_lines=$(wc -l < "$SCRATCH/cand-ten-legs.txt")"
  if diff -u "$SCRATCH/base-legs.txt" "$SCRATCH/cand-ten-legs.txt" > "$OUT/T88E3-ten-leg-diff.txt"; then
    echo 'TEN_LEG_RECEIPTS_IDENTICAL'
  else
    echo 'TEN_LEG_RECEIPTS_DIFFER'; cat "$OUT/T88E3-ten-leg-diff.txt"
  fi
  grep -E '^(REGRESSION_PIN|REGRESSION_SWEEP|REGRESSION_TABLE|REGRESSION_CASE) py-kake-ledger-guard' \
    "$OUT/T88E3-regression-candidate.out"
}

# ---------------------------------------------------------------- extra: spec provenance
# The eleventh leg's embedded spec must still be the frozen pre-registration; a
# runner change that silently swapped it would be a harm the selftest cannot see
# (the selftest only checks the spec's ids against TABLE_KAKEGUARD).
do_spec() {
  local root=$SCRATCH/fleet-cand frozen=$LANE/.ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec
  if [ ! -x "$root/tameshi-shokunin/tools/mutate-and-run.sh" ]; then
    make_fleet "$root" "$CAND" >/dev/null
  fi
  awk '/^  cat >"\$d\/py-kake-ledger-guard\.spec" <<.EOT.$/{f=1;next} f&&/^EOT$/{exit} f' \
    "$root/tameshi-shokunin/tools/mutate-and-run.sh" > "$OUT/T88E3-embedded-spec.txt"
  sha256sum "$OUT/T88E3-embedded-spec.txt" "$frozen"
  echo "embedded_spec_defects=$(grep -cE '^@defect ' "$OUT/T88E3-embedded-spec.txt")"
  if diff -u "$frozen" "$OUT/T88E3-embedded-spec.txt" > "$SCRATCH/spec-diff.txt"; then
    echo 'EMBEDDED_SPEC_IDENTICAL_TO_PREREG'
  else
    echo 'EMBEDDED_SPEC_DIFFERS'; cat "$SCRATCH/spec-diff.txt"
  fi
}

# ---------------------------------------------------------------- extra probes
# Do the selftest's 11-leg guards still bite, or would they accept a shrunk ledger?
do_probes() {
  local src=$SCRATCH/fleet-cand/tameshi-shokunin/tools/mutate-and-run.sh
  if [ ! -x "$src" ]; then
    make_fleet "$SCRATCH/fleet-cand" "$CAND" >/dev/null
    src=$SCRATCH/fleet-cand/tameshi-shokunin/tools/mutate-and-run.sh
  fi
  probe() { # probe <id> <sed-expr>
    local id=$1 expr=$2 root=$SCRATCH/probe-$1 b rc
    mkdir -p "$root/tameshi-shokunin/tools"
    for d in "$FLEET"/*; do
      b=$(basename "$d"); [ "$b" = tameshi-shokunin ] && continue
      ln -sfn "$d" "$root/$b"
    done
    sed -E "$expr" "$src" > "$root/tameshi-shokunin/tools/mutate-and-run.sh"
    chmod 755 "$root/tameshi-shokunin/tools/mutate-and-run.sh"
    ( cd "$SCRATCH" && bash "$root/tameshi-shokunin/tools/mutate-and-run.sh" --selftest ) \
      > "$OUT/T88E3-probe-$id.out" 2>&1
    rc=$?
    printf '=== probe %s: exit=%s %s\n' "$id" "$rc" "$(grep -E '^MUTATE_SELFTEST' "$OUT/T88E3-probe-$id.out")"
    grep -E '^FAIL ' "$OUT/T88E3-probe-$id.out" || echo '  (no FAIL lines)'
  }
  # A: drop the eleventh leg from the selftest's own tuple array
  probe drop-tuple "/^    'py-kake-ledger-guard:py-kake-ledger-guard\.spec:TABLE_KAKEGUARD:10:5'\$/d"
  # B: put the tally count literal back to ten while eleven legs are still declared
  probe nlegs10 "s/^  local nlegs=11 npass=0 nfail=0 nsetup=0 st\$/  local nlegs=10 npass=0 nfail=0 nsetup=0 st/"
}

case $MODE in
  diff)       do_diff ;;
  selftest)   do_selftest ;;
  regression) do_regression ;;
  spec)       do_spec ;;
  probes)     do_probes ;;
  all)        do_diff; do_selftest; do_regression; do_spec; do_probes ;;
  *)          echo "unknown mode: $MODE" >&2; exit 64 ;;
esac
