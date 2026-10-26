#!/bin/sh
# Fixture proof for seat-report-append-only.py.
# usage: fixture-driver.sh SCRATCH_ROOT RECEIPT_DIR CHECKER
# Runs a throw-away git fixture under SCRATCH_ROOT and records exit codes,
# stdout and stderr per case. No lane state is touched.
set -u

S=${1:?scratch root}
OUT=${2:?receipt dir}
PY=${3:?checker path}
CHECKER=$(readlink -f "$PY")

REC="$OUT/fixture"
rm -rf "$REC"
mkdir -p "$REC"

D=$(mktemp -d -p "$S" fixture.XXXXXX) || exit 9
{
  echo "fixture=$D"
} > "$REC/00-fixture.path"

git -C "$D" init -q || exit 9
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 9
echo "git -C \"\$D\" rev-parse --show-toplevel -> $TOP" >> "$REC/00-fixture.path"
if [ "$(readlink -f "$TOP")" != "$(readlink -f "$D")" ]; then
  echo "TOPLEVEL-MISMATCH" >> "$REC/00-fixture.path"
  exit 9
fi
echo "toplevel verified equal to fixture dir" >> "$REC/00-fixture.path"
git -C "$D" config user.email fixture@example.invalid
git -C "$D" config user.name fixture

mkdir -p "$D/.ufo/waves/round-01" "$D/.ufo/waves/other"
printf '# Seat report A\nline 1\nline 2\n' > "$D/.ufo/waves/round-01/A.md"
printf '# Seat report B\nline 1\n' > "$D/.ufo/waves/round-01/B.md"
printf 'not a round artifact\n' > "$D/.ufo/waves/other/n.md"
git -C "$D" add -A
git -C "$D" commit -q -m "c1: base"
C1=$(git -C "$D" rev-parse HEAD)

run() { # case-name from to
  case_name=$1; from=$2; to=$3
  "$CHECKER" "$D" "$from" "$to" > "$REC/$case_name.stdout" 2> "$REC/$case_name.stderr"
  echo $? > "$REC/$case_name.exit"
}

judge() { # case-name expected-exit
  case_name=$1; want=$2
  got=$(cat "$REC/$case_name.exit")
  if [ "$got" = "$want" ]; then
    echo "PASS $case_name exit=$got (want $want)"
  else
    echo "FAIL $case_name exit=$got (want $want)"
  fi
}

: > "$REC/results.txt"

# 1. append only: A and B each gain trailing bytes; C is new at TO.
printf 'appended line\n' >> "$D/.ufo/waves/round-01/A.md"
printf 'appended line\n' >> "$D/.ufo/waves/round-01/B.md"
printf '# Seat report C\nline 1\n' > "$D/.ufo/waves/round-01/C.md"
git -C "$D" add -A
git -C "$D" commit -q -m "c2: pure appends plus a new report"
C2=$(git -C "$D" rev-parse HEAD)
run 01-append "$C1" "$C2"
judge 01-append 0

# 2. in-place edit of a landed report: A's second line changes.
printf '# Seat report A\nline 1 CHANGED\nline 2\nappended line\n' > "$D/.ufo/waves/round-01/A.md"
git -C "$D" add -A
git -C "$D" commit -q -m "c3: edit A in place"
C3=$(git -C "$D" rev-parse HEAD)
run 02-edit-in-place "$C2" "$C3"
judge 02-edit-in-place 1

# 3. deletion of a landed report.
git -C "$D" rm -q .ufo/waves/round-01/B.md
git -C "$D" commit -q -m "c4: delete B"
C4=$(git -C "$D" rev-parse HEAD)
run 03-deleted "$C3" "$C4"
judge 03-deleted 1

# 4. truncation: C loses its trailing line, so TO does not extend FROM.
printf '# Seat report C\n' > "$D/.ufo/waves/round-01/C.md"
git -C "$D" add -A
git -C "$D" commit -q -m "c5: truncate C"
C5=$(git -C "$D" rev-parse HEAD)
run 04-truncated "$C4" "$C5"
judge 04-truncated 1

# 5. non-round file rewritten in place: outside the checked scope.
printf 'changed\n' > "$D/.ufo/waves/other/n.md"
git -C "$D" add -A
git -C "$D" commit -q -m "c6: edit non-round file"
C6=$(git -C "$D" rev-parse HEAD)
run 05-non-round-ignored "$C5" "$C6"
judge 05-non-round-ignored 0

# 6. identical revisions.
run 06-identical "$C6" "$C6"
judge 06-identical 0

# 7. rename inside the round tree: the old path is deleted.
git -C "$D" mv .ufo/waves/round-01/C.md .ufo/waves/round-01/C2.md
git -C "$D" commit -q -m "c7: rename C to C2"
C7=$(git -C "$D" rev-parse HEAD)
run 07-renamed "$C6" "$C7"
judge 07-renamed 1

# 8. setup errors: unresolvable revision, missing argument, non-repository path.
"$CHECKER" "$D" no-such-revision "$C7" > "$REC/08-bad-rev.stdout" 2> "$REC/08-bad-rev.stderr"
echo $? > "$REC/08-bad-rev.exit"
judge 08-bad-rev 2

"$CHECKER" "$D" > "$REC/09-missing-arg.stdout" 2> "$REC/09-missing-arg.stderr"
echo $? > "$REC/09-missing-arg.exit"
judge 09-missing-arg 2

NONREPO=$(mktemp -d -p "$S" nonrepo.XXXXXX)
"$CHECKER" "$NONREPO" "$C1" "$C1" > "$REC/10-non-repo.stdout" 2> "$REC/10-non-repo.stderr"
echo $? > "$REC/10-non-repo.exit"
judge 10-non-repo 2

# 9. missing (nonexistent) LANE path.
"$CHECKER" "$S/definitely-not-here" "$C1" "$C1" > "$REC/11-missing-lane.stdout" 2> "$REC/11-missing-lane.stderr"
echo $? > "$REC/11-missing-lane.exit"
judge 11-missing-lane 2

# Assertions on what the failures report.
{
  echo "--- 02-edit-in-place stdout"
  cat "$REC/02-edit-in-place.stdout"
  echo "--- 03-deleted stdout"
  cat "$REC/03-deleted.stdout"
  echo "--- 04-truncated stdout"
  cat "$REC/04-truncated.stdout"
  echo "--- 07-renamed stdout"
  cat "$REC/07-renamed.stdout"
  echo "--- 01-append stdout"
  cat "$REC/01-append.stdout"
} > "$REC/violation-output.txt"

if grep -q 'REWRITTEN	.ufo/waves/round-01/A.md	prefix-lost' "$REC/02-edit-in-place.stdout"; then
  echo "PASS edit case names A.md prefix-lost"
else
  echo "FAIL edit case does not name A.md prefix-lost"
fi
if grep -q 'REWRITTEN	.ufo/waves/round-01/B.md	deleted' "$REC/03-deleted.stdout"; then
  echo "PASS delete case names B.md deleted"
else
  echo "FAIL delete case does not name B.md deleted"
fi
if grep -q 'REWRITTEN	.ufo/waves/round-01/C.md	prefix-lost' "$REC/04-truncated.stdout"; then
  echo "PASS truncation case names C.md prefix-lost"
else
  echo "FAIL truncation case does not name C.md prefix-lost"
fi
if grep -q 'REWRITTEN	.ufo/waves/round-01/C.md	deleted' "$REC/07-renamed.stdout"; then
  echo "PASS rename case names old path deleted"
else
  echo "FAIL rename case does not name old path deleted"
fi
if grep -q 'SUMMARY	checked=2	rewritten=0' "$REC/01-append.stdout"; then
  echo "PASS append case checked 2 round files at FROM, 0 rewritten"
else
  echo "FAIL append case summary unexpected"
fi

# Fixture history for the record.
git -C "$D" log --format='%H %s' > "$REC/fixture-history.txt"
git -C "$D" status --porcelain > "$REC/fixture-status.txt"
