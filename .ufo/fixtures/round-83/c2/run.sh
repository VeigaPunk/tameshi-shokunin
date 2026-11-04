#!/usr/bin/env bash
# R83-C2 counter: does the registry binding measure the defect-bind figures?
#
#   .ufo/fixtures/round-83/c2/run.sh [--rev REV] [--tool PATH]
#
# Clones the lane, degrades `defect-bind-selftest` in tools/registry.json (the
# edit a binding would have to catch) and runs the registry-figure binding.
# It never writes the lane: the fixture is a --shared clone under
# HYAKU_SCRATCH/TMPDIR, removed on exit.
set -ueuo pipefail
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FIX="$LANE/.ufo/fixtures/round-83/c2"
REV=origin/master
TOOL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --rev) REV="$2"; shift 2 ;;
    --tool) TOOL="$2"; shift 2 ;;
    *) echo "usage: $0 [--rev REV] [--tool PATH]" >&2; exit 64 ;;
  esac
done
ROOT="${HYAKU_SCRATCH:-${TMPDIR:-/tmp}}"
mkdir -p "$ROOT"
S=$(mktemp -d "$ROOT/tameshi-r83-c2.XXXXXX")
trap 'rm -rf -- "$S"' EXIT
git clone -q --shared "$LANE" "$S/lane"
git -C "$S/lane" checkout -q "$REV"
python3 "$FIX/degrade.py" "$S/lane/tools/registry.json"
tool="${TOOL:-$S/lane/tools/registry-figure-bind.py}"
echo "TOOL $tool"
set +e
( cd "$S/lane" && python3 -I -X utf8 "$tool" --repo . --manifest tools/registry-figure-bind.json ) \
  > "$S/out" 2> "$S/err"
rc=$?
set -e
echo "EXIT $rc"
grep '^REGISTRY_BIND' "$S/out" || true
echo "--- stdout ---"; cat "$S/out"
echo "--- stderr ---"; cat "$S/err"
