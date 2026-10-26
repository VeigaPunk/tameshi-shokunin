#!/bin/sh
# Scale proof for seat-report-append-only.py on real lane bytes.
# usage: clone-driver.sh SCRATCH RECEIPT_DIR CHECKER LANE
# Clones the lane (shared objects) into SCRATCH, checks out the round-43
# base, then commits an append and an in-place rewrite to prove the
# checker reads real seat-report bytes and separates the two cases.
set -u

S=${1:?scratch}
OUT=${2:?receipt dir}
CHECKER=${3:?checker}
LANE=${4:?lane}

REC="$OUT/clone-scale"
rm -rf "$REC"
mkdir -p "$REC"
D="$S/lane"
rm -rf "$D"
git clone -q --shared "$LANE" "$D" || exit 9
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 9
if [ "$(readlink -f "$TOP")" != "$(readlink -f "$D")" ]; then
  echo "TOPLEVEL-MISMATCH: $TOP" > "$REC/00-clone.path"
  exit 9
fi
{
  echo "clone=$D"
  echo "git -C \"\$D\" rev-parse --show-toplevel -> $TOP"
  echo "toplevel verified equal to clone dir"
} > "$REC/00-clone.path"

git -C "$D" config user.email fixture@example.invalid
git -C "$D" config user.name fixture
git -C "$D" checkout -q 487b8f0da89fa0e2b8bea6930068accbf36e70a9 || exit 9
C0=$(git -C "$D" rev-parse HEAD)
echo "C0=$C0" >> "$REC/00-clone.path"

run() { # name from to
  case_name=$1; from=$2; to=$3
  "$CHECKER" "$D" "$from" "$to" > "$REC/$case_name.stdout" 2> "$REC/$case_name.stderr"
  echo $? > "$REC/$case_name.exit"
}

judge() {
  case_name=$1; want=$2
  got=$(cat "$REC/$case_name.exit")
  if [ "$got" = "$want" ]; then
    echo "PASS $case_name exit=$got (want $want)"
  else
    echo "FAIL $case_name exit=$got (want $want)"
  fi
}

# Append to a landed file in the real tree.
printf 'clone-scale append probe\n' >> "$D/.ufo/waves/round-20/plan1.err"
git -C "$D" commit -q -am "clone probe: append to a landed round artifact"
C1=$(git -C "$D" rev-parse HEAD)
run 01-append "$C0" "$C1"
judge 01-append 0

# Rewrite a landed seat report in place: a new first line before the old bytes.
F=.ufo/waves/round-42/w1/MutC1M10.md
{
  printf 'PROBE-REWRITE\n'
  git -C "$D" show "$C0:$F"
} > "$D/$F"
git -C "$D" commit -q -am "clone probe: rewrite a landed seat report"
C2=$(git -C "$D" rev-parse HEAD)
run 02-rewrite "$C1" "$C2"
judge 02-rewrite 1

grep -q 'SUMMARY	checked=2819	rewritten=0' "$REC/01-append.stdout" &&
  echo "PASS append receipt checked 2819 real round files, 0 rewritten" ||
  echo "FAIL append receipt summary unexpected"
grep -q "REWRITTEN	$F	prefix-lost" "$REC/02-rewrite.stdout" &&
  echo "PASS rewrite receipt names $F prefix-lost" ||
  echo "FAIL rewrite receipt does not name $F"

git -C "$D" log --format='%H %s' "$C0^..$C2" > "$REC/clone-probe-history.txt"
