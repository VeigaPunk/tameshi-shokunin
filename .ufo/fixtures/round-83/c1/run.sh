#!/usr/bin/env bash
# R83-C1 counter: does the self-state sweep refuse a narrowed manifest and a
# line-breaking row id?
#
#   .ufo/fixtures/round-83/c1/run.sh [--rev REV] [--tool PATH] [--manifest-rev REV] [--case narrow|idforge]
#
# --rev          the lane revision to clone (default: origin/master)
# --tool         the selfstate-freshness.py to run (default: the clone's own)
# --manifest-rev the value of --manifest-rev to pass (default: none)
#
# Prints one block per case: CASE, EXIT, the SELFSTATE: verdict lines the run
# printed, and STDOUT/STDERR. It never writes the lane: every fixture is a
# --shared clone under HYAKU_SCRATCH/TMPDIR, removed on exit.
set -ueuo pipefail
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FIX="$LANE/.ufo/fixtures/round-83/c1"
REV=origin/master
TOOL=""
MREV=""
CASES="narrow idforge"
while [ $# -gt 0 ]; do
  case "$1" in
    --rev) REV="$2"; shift 2 ;;
    --tool) TOOL="$2"; shift 2 ;;
    --manifest-rev) MREV="$2"; shift 2 ;;
    --case) CASES="$2"; shift 2 ;;
    *) echo "usage: $0 [--rev REV] [--tool PATH] [--manifest-rev REV]" >&2; exit 64 ;;
  esac
done
ROOT="${HYAKU_SCRATCH:-${TMPDIR:-/tmp}}"
mkdir -p "$ROOT"
S=$(mktemp -d "$ROOT/tameshi-r83-c1.XXXXXX")
trap 'rm -rf -- "$S"' EXIT

case_run() {
  local name="$1" script="$2"
  local dir="$S/$name"
  git clone -q --shared "$LANE" "$dir"
  git -C "$dir" checkout -q "$REV"
  python3 "$FIX/$script" "$dir/tools/selfstate-freshness.json"
  local tool="${TOOL:-$dir/tools/selfstate-freshness.py}"
  echo "CASE $name"
  echo "TOOL $tool"
  set +e
  ( cd "$dir" && python3 -I -X utf8 "$tool" --repo . --manifest tools/selfstate-freshness.json ${MREV:+--manifest-rev "$MREV"} ) \
    > "$S/$name.out" 2> "$S/$name.err"
  local rc=$?
  set -e
  echo "EXIT $rc"
  echo "VERDICT_LINES $(grep -c '^SELFSTATE:' "$S/$name.out" || true)"
  grep '^SELFSTATE:' "$S/$name.out" || true
  echo "--- stdout ---"; cat "$S/$name.out"
  echo "--- stderr ---"; cat "$S/$name.err"
  echo "CASE_END $name"
}

for c in $CASES; do case "$c" in narrow) case_run narrow narrow.py ;; idforge) case_run idforge idforge.py ;; *) echo "unknown case $c" >&2; exit 64 ;; esac; done
