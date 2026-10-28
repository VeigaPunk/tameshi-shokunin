#!/bin/bash
# Seat T55W2RevToolDiffs — TMPDIR pairs for the three round-55 tool diffs.
# usage: run-arms.sh <clone> <tag>    (clone checked out at the revision under test)
set -u
CLONE=$1
TAG=$2
R=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w2/T55W2RevToolDiffs-receipts
S=/fast/scratch/hyaku/tameshi-r55/T55W2RevToolDiffs
mkdir -p "$R/$TAG" "$S/tmp-ok"

arm() { # arm <label> <tmpdir> <argv...>
  local label=$1 tmpdir=$2; shift 2
  local dir="$R/$TAG/$label"
  ( cd "$CLONE" && TMPDIR="$tmpdir" "$@" >"$dir.stdout" 2>"$dir.stderr"; echo $? >"$dir.rc" )
  local rc; rc=$(cat "$dir.rc")
  echo "ARM $TAG/$label rc=$rc"
  echo "  stdout: $(sed -n '1,4p' "$dir.stdout" | tr '\n' '|' | cut -c1-300)"
  echo "  stderr: $(sed -n '1,4p' "$dir.stderr" | tr '\n' '|' | cut -c1-300)"
}

NU=/nonexistent/x
GOOD=$S/tmp-ok
py=python3

arm rc-selftest-unusable      "$NU"   $py tools/repeat-control.py --selftest
arm rc-selftest-usable        "$GOOD" $py tools/repeat-control.py --selftest
arm rc-snapshot-unusable      "$NU"   $py tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
arm rc-snapshot-usable        "$GOOD" $py tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
rm -rf "$S/rc-run-u" "$S/rc-run-o"
arm rc-run-unusable           "$NU"   $py tools/repeat-control.py --runs 3 --out "$S/rc-run-u" -- /bin/true
arm rc-run-usable             "$GOOD" $py tools/repeat-control.py --runs 3 --out "$S/rc-run-o" -- /bin/true
arm rc-help-unusable          "$NU"   $py tools/repeat-control.py --help

arm cc-selftest-unusable      "$NU"   $py tools/context-capture.py --selftest
arm cc-selftest-usable        "$GOOD" $py tools/context-capture.py --selftest
arm cc-check-unusable         "$NU"   $py tools/context-capture.py --check --json
arm cc-check-usable           "$GOOD" $py tools/context-capture.py --check --json
arm cc-noargs-unusable        "$NU"   $py tools/context-capture.py
arm cc-help-unusable          "$NU"   $py tools/context-capture.py --help

arm rcg-selftest-unusable     "$NU"   $py tools/registry-check.py --selftest
arm rcg-selftest-usable       "$GOOD" $py tools/registry-check.py --selftest
arm rcg-rev-unusable          "$NU"   $py tools/registry-check.py --rev HEAD
arm rcg-rev-json-unusable     "$NU"   $py tools/registry-check.py --rev HEAD --json
arm rcg-rev-badrev-json       "$NU"   $py tools/registry-check.py --rev deadbeefdeadbeef --json
arm rcg-root-missing-json     "$NU"   $py tools/registry-check.py --root /nonexistent --json
arm rcg-live-only-unusable    "$NU"   $py tools/registry-check.py --root . --only repeat-control-selftest --json
arm rcg-live-only-usable      "$GOOD" $py tools/registry-check.py --root . --only repeat-control-selftest --json
