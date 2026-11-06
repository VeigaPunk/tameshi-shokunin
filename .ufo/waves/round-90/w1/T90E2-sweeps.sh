#!/usr/bin/env bash
# T90E2 (round 90, seat T90E2) — standing no-harm sweep driver.
#
# Runs the lane's five standing sweeps from a checked-out root and prints one
# machine-readable SWEEP line per sweep plus the sweep's summary line, so the
# base / freeze / freeze+fixes states can be compared row by row.
#
#   T90E2-sweeps.sh ROOT OUTDIR TMPBASE
#
# ROOT     a checkout (or --shared clone) of tameshi-shokunin to measure
# OUTDIR   directory for the per-sweep full logs (created if absent)
# TMPBASE  scratch directory; each sweep gets its own fresh TMPDIR below it
#
# The five sweeps (all read the repo at ROOT, never the live lane):
#   1 selfstate   python3 -I -X utf8 tools/selfstate-freshness.py --repo . \
#                     --manifest tools/selfstate-freshness.json        (SELFSTATE:)
#   2 pin-audit   the same tool with --pin-audit --pin-rev HEAD        (SELFSTATE_PINS:)
#   3 figure-bind python3 -I -X utf8 tools/registry-figure-bind.py --repo .  (REGISTRY_BIND:)
#   4 pointer     python3 -I -X utf8 tools/pointer-recheck.py --repo . \
#                     --manifest tools/pointer-recheck.json            (POINTER_RECHECK:)
#   5 registry    python3 -I tools/registry-check.py --root .          (REGISTRY_CHECK:)
#
# Exit: 0 when all five sweeps exited with their declared no-harm state
# (selfstate 0|1 as a standing red arm is legitimate: the row summary carries
# `unexpected=U` and that is what is compared; this driver does NOT judge, it
# only reports exit codes and summaries). The driver's own exit is the number
# of sweeps whose exit code was >=2 (setup / could-not-evaluate), so callers
# cannot mistake a setup refusal for a measured state.
set -u

ROOT=${1:?usage: T90E2-sweeps.sh ROOT OUTDIR TMPBASE}
OUT=${2:?usage: T90E2-sweeps.sh ROOT OUTDIR TMPBASE}
TMPBASE=${3:?usage: T90E2-sweeps.sh ROOT OUTDIR TMPBASE}
ROOT=$(realpath -- "$ROOT") || exit 3
mkdir -p "$OUT" "$TMPBASE" || exit 3
OUT=$(realpath -- "$OUT")
TMPBASE=$(realpath -- "$TMPBASE")

export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C.UTF-8

setup_refusals=0
n=0

# run NAME SUMMARY_RE CMD...
run() {
    local name=$1 sumre=$2
    shift 2
    local mine="$TMPBASE/$name"
    mkdir -p "$mine" || return 3
    ( cd "$ROOT" && TMPDIR="$mine" "$@" ) >"$OUT/$name.log" 2>&1
    local rc=$?
    local sum
    sum=$(grep -E "$sumre" "$OUT/$name.log" | tail -1)
    echo "SWEEP $name exit=$rc summary=${sum:-<no-summary>}"
    n=$((n + 1))
    [ "$rc" -ge 2 ] && setup_refusals=$((setup_refusals + 1))
    return 0
}

run selfstate '^SELFSTATE: ' \
    python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json
run pin-audit '^SELFSTATE_PINS: ' \
    python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --pin-audit --pin-rev HEAD
run figure-bind '^REGISTRY_BIND: ' \
    python3 -I -X utf8 tools/registry-figure-bind.py --repo . --manifest tools/registry-figure-bind.json
run pointer '^POINTER_RECHECK: ' \
    python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json
run registry '^REGISTRY_CHECK: ' \
    python3 -I tools/registry-check.py --root .

echo "SWEEPS root=$ROOT runs=$n setup_refusals=$setup_refusals"
exit "$setup_refusals"
