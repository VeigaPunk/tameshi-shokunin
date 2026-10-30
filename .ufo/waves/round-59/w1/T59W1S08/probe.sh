#!/usr/bin/env bash
# Fixture probe for seat T59W1S08 — cell path='tools/space name.py' (measure.py index 1).
# Constructs the scratch fixture EXACTLY as the frozen counter does for this path,
# records git object evidence, then runs the independent oracle for classes
# 'equal' (skipped-work control: trusted vs trusted) and 'changed'.
set -euo pipefail

SEAT_SCRATCH="/fast/scratch/hyaku/tameshi-r59/T59W1S08"
FIX="${SEAT_SCRATCH}/fixture-1"   # measure.py: work/f'fixture-{ix}' with ix=1 for this path
PATH_UNDER_TEST='tools/space name.py'
export TMPDIR="${SEAT_SCRATCH}"
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_NOSYSTEM=1
export PYTHONDONTWRITEBYTECODE=1

cd "${SEAT_SCRATCH}"
rm -rf "${FIX}"
mkdir -p "${FIX}"

echo '=== fixture construction (mirrors frozen measure.py, path index 1) ==='
git -C "${FIX}" init -q
top="$(git -C "${FIX}" rev-parse --show-toplevel)"
echo "fixture toplevel: ${top}"
[ "$(readlink -f "${top}")" = "$(readlink -f "${FIX}")" ] || { echo 'ROOT MISMATCH'; exit 99; }

f="${FIX}/${PATH_UNDER_TEST}"
mkdir -p "$(dirname "${f}")"
printf 'print("real executor")\n' > "${f}"
git -C "${FIX}" add -- "${PATH_UNDER_TEST}"
git -C "${FIX}" -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
TRUSTED="$(git -C "${FIX}" rev-parse HEAD)"
echo "TRUSTED=${TRUSTED}"

printf 'print("forged success")\n' > "${f}"
git -C "${FIX}" add -- "${PATH_UNDER_TEST}"
git -C "${FIX}" -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
CHANGED="$(git -C "${FIX}" rev-parse HEAD)"
echo "CHANGED=${CHANGED}"

echo
echo '=== git object evidence: source-object type/mode/content ==='
echo "--- trusted commit ---"
git -C "${FIX}" ls-tree "${TRUSTED}" -- "${PATH_UNDER_TEST}"
git -C "${FIX}" cat-file -t "$(git -C "${FIX}" rev-parse "${TRUSTED}:${PATH_UNDER_TEST}")"
git -C "${FIX}" cat-file -p "${TRUSTED}:${PATH_UNDER_TEST}"
echo "--- changed commit ---"
git -C "${FIX}" ls-tree "${CHANGED}" -- "${PATH_UNDER_TEST}"
git -C "${FIX}" cat-file -t "$(git -C "${FIX}" rev-parse "${CHANGED}:${PATH_UNDER_TEST}")"
git -C "${FIX}" cat-file -p "${CHANGED}:${PATH_UNDER_TEST}"
echo "--- blob ids ---"
echo "trusted blob:  $(git -C "${FIX}" rev-parse "${TRUSTED}:${PATH_UNDER_TEST}")"
echo "changed blob:  $(git -C "${FIX}" rev-parse "${CHANGED}:${PATH_UNDER_TEST}")"
echo "--- trailing- newline/byte check ---"
git -C "${FIX}" cat-file blob "${TRUSTED}:${PATH_UNDER_TEST}" | od -c | head -3

echo
echo '=== oracle runs ==='
echo '--- class equal (control: candidate=trusted; frozen expectation exit=0, token EXECUTOR_SOURCE_BOUND) ---'
set +e
python3 -I "${SEAT_SCRATCH}/oracle.py" --repo "${FIX}" --trusted "${TRUSTED}" --candidate "${TRUSTED}" --path "${PATH_UNDER_TEST}"
echo "oracle exit: $?"
echo '--- class changed (frozen expectation exit=1, token EXECUTOR_SOURCE_DRIFT) ---'
python3 -I "${SEAT_SCRATCH}/oracle.py" --repo "${FIX}" --trusted "${TRUSTED}" --candidate "${CHANGED}" --path "${PATH_UNDER_TEST}"
echo "oracle exit: $?"
set -e

echo
echo '=== frozen-counter expected mapping for this cell (from measure.py) ==='
echo "expected=1 token=EXECUTOR_SOURCE_DRIFT for path='${PATH_UNDER_TEST}' class=changed"
