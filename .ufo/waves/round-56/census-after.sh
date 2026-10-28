#!/usr/bin/env bash
# census-after.sh — round-56 after-harness for corpus/SOURCES.md.
#
# Runs the fleet census (scripts/sources-census.sh) unchanged, prints
# `CENSUS exit=N rows=M`, then shape-checks every row NEW relative to --base:
#   11 columns · no literal or escaped pipe · ISO `opened` · valid `status`.
# Read-only: never writes the registry; writes only stdout or --out.
#
#   census-after.sh [--lane DIR] [--root DIR] [--sources PATH] [--base REV]
#                   [--label NAME] [--shape-only] [--out PATH]
#
#   --lane DIR      lane repo (default /home/vgpnk/Projects/shokunin/tameshi-shokunin)
#   --root DIR      fleet root handed to sources-census.sh (default its parent)
#   --sources PATH  registry to shape-check (default LANE/corpus/SOURCES.md);
#                   when it is not the lane file, the census runs with --file
#   --base REV      revision whose registry defines "old" rows
#                   (default: the `base` field of .ufo/evidence/round-56/contract.json)
#   --label NAME    label for the shape lines (default: lane id, or the dir above corpus/)
#   --shape-only    skip the census run and shape-check only
#
# Output: the census's own TSV, then
#   CENSUS exit=N rows=M                      (exact line, always printed)
#   CENSUS_ROWS_SELFCHECK census=M grep=G     (registry rows seen by each reader)
#   CENSUS_SHAPE<TAB>lane<TAB>id<TAB>CODE<TAB>detail   (one per finding)
#   CENSUS_SHAPE new_rows=K findings=F
#
# Codes: SHAPE_COLUMNS (11 columns) · SHAPE_PIPE (literal or escaped pipe)
#        · SHAPE_OPENED (ISO date, real calendar day, not future)
#        · SHAPE_STATUS (queued|mined|rejected) · SHAPE_SECTION (row outside ## Registry)
#
# exit: 0 clean · 1 shape findings (or row-count mismatch) · 2 usage/env or an
#       unresolvable --base · otherwise the census's own exit code (1 findings, 2 env).
# An empty new-row set is a measured no-change: reported as new_rows=0, never an error.
set -u

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
ROOT=/home/vgpnk/Projects/shokunin
SOURCES=""; BASE=""; SHAPE_ONLY=0; OUT=""; LABEL=""
CONTRACT=""

die() { echo "ERROR: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --lane)      [ $# -ge 2 ] || die "--lane needs a path";    LANE=$2; shift 2 ;;
    --root)      [ $# -ge 2 ] || die "--root needs a path";    ROOT=$2; shift 2 ;;
    --sources)   [ $# -ge 2 ] || die "--sources needs a path"; SOURCES=$2; shift 2 ;;
    --base)      [ $# -ge 2 ] || die "--base needs a rev";     BASE=$2; shift 2 ;;
    --label)     [ $# -ge 2 ] || die "--label needs a name";   LABEL=$2; shift 2 ;;
    --shape-only) SHAPE_ONLY=1; shift ;;
    --out)       [ $# -ge 2 ] || die "--out needs a path";     OUT=$2; shift 2 ;;
    -h|--help)   sed -n '2,30p' "$0"; exit 0 ;;
    *)           die "unknown argument: $1" ;;
  esac
done

[ -d "$LANE" ] || die "lane not a directory: $LANE"
[ -d "$ROOT" ] || die "root not a directory: $ROOT"
[ -n "$SOURCES" ] || SOURCES=$LANE/corpus/SOURCES.md
[ -f "$SOURCES" ] || die "registry not found: $SOURCES"
CENSUS=$ROOT/scripts/sources-census.sh
[ -x "$CENSUS" ] || die "census script not executable: $CENSUS"
CONTRACT=$LANE/.ufo/evidence/round-56/contract.json

if [ -z "$BASE" ]; then
  [ -f "$CONTRACT" ] || die "no --base and contract missing: $CONTRACT"
  BASE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["base"])' "$CONTRACT" 2>/dev/null) \
    || die "cannot read the base revision from $CONTRACT"
  [ -n "$BASE" ] || die "contract has no base field: $CONTRACT"
fi
git -C "$LANE" cat-file -e "$BASE^{commit}" 2>/dev/null \
  || die "--base not a commit in $LANE: $BASE"

emit() { if [ -n "$OUT" ]; then printf '%s\n' "$*" >> "$OUT"; else printf '%s\n' "$*"; fi; }
sink() { if [ -n "$OUT" ]; then cat >> "$OUT"; else cat; fi; }

TMP=$(mktemp -d "${TMPDIR:-/tmp}/census-after.XXXXXX") || die "mktemp failed"
trap 'rm -rf -- "$TMP"' EXIT

# ---- target arguments: the lane registry keeps the roster path, anything else is --file
LANE_SOURCES=$(realpath -- "$LANE/corpus/SOURCES.md")
SOURCES_ABS=$(realpath -- "$SOURCES")
if [ "$SOURCES_ABS" = "$LANE_SOURCES" ]; then
  set -- --root "$ROOT" tameshi
  LANE_LABEL=tameshi
else
  set -- --file "$SOURCES_ABS"
  src_dir=$(dirname -- "$SOURCES_ABS")
  lane_dir=$(dirname -- "$src_dir")
  LANE_LABEL=$(basename -- "$lane_dir")
fi
[ -n "$LABEL" ] && LANE_LABEL=$LABEL

[ -n "$OUT" ] && : > "$OUT"

# ---- 1. the census, unchanged -------------------------------------------------
CENSUS_EXIT=0
if [ "$SHAPE_ONLY" = 0 ]; then
  "$CENSUS" validate --today "$(date -u +%F)" "$@" > "$TMP/validate.out" 2> "$TMP/validate.err"
  CENSUS_EXIT=$?
  cat "$TMP/validate.err" >&2
  cat "$TMP/validate.out" | sink
  "$CENSUS" census "$@" > "$TMP/census.out" 2>> "$TMP/validate.err"
  CENSUS_CENSUS_EXIT=$?
  cat "$TMP/census.out" | sink
  [ "$CENSUS_EXIT" = 0 ] && CENSUS_EXIT=$CENSUS_CENSUS_EXIT
  ROWS=$(awk -F'\t' '$2=="rows"{r=$3} END{print r+0}' "$TMP/census.out")
else
  ROWS=0
fi

# ---- 2. rows the registry reader counts (the self-check denominator) ----------
GREP_ROWS=$(grep -cE '^ {0,3}\| S[0-9]{3,} \|' "$SOURCES_ABS" || true)

# ---- 3. old rows at --base ----------------------------------------------------
git -C "$LANE" show "$BASE:corpus/SOURCES.md" > "$TMP/base.md" 2>/dev/null \
  || die "cannot read $BASE:corpus/SOURCES.md in $LANE"
gawk -F'|' '
  /^ {0,3}\|/ { id=$2; gsub(/^[ \t]+|[ \t]+$/,"",id)
                if (id ~ /^S[0-9]{3,}$/) print id }' "$TMP/base.md" | sort -u > "$TMP/base.ids"

# ---- 4. shape of every new row ------------------------------------------------
gawk -F'|' -v lane="$LANE_LABEL" -v basefile="$TMP/base.ids" -v today="$(date -u +%F)" '
  function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
  function epoch(s,   a,y,m,d,t) {
    if (s !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) return -1e15
    split(s,a,"-"); y=a[1]+0; m=a[2]+0; d=a[3]+0
    if (y==0) return -1e15
    t=mktime(sprintf("%04d %02d %02d 00 00 00",y,m,d),1)
    if (strftime("%Y-%m-%d",t,1)!=s) return -1e15
    return t
  }
  function finding(id,code,detail) { printf "%s\tCENSUS_SHAPE\t%s\t%s\t%s\n",lane,id,code,detail; findings++ }
  BEGIN {
    while ((getline line < basefile) > 0) if (line!="") old[line]=1
    today_epoch=epoch(today)
    in_registry=0
  }
  {
    line=$0
    if (line ~ /^ {0,3}##[ \t]/) { sub(/^ {0,3}/,"",line); in_registry=(trim(substr(line,3))=="Registry"); next }
    if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
    if (line !~ /^ {0,3}\|/) next
    if (line ~ /^\|[ \t]*id[ \t]*\|/) next              # header
    if (line ~ /^\|[ \t]*:?-+:?[ \t]*\|/) next          # separator
    id=trim($2)
    if (id !~ /^S[0-9]{3,}$/) next
    if (id in old) { seen++ ; next }
    newrows++
    # a literal pipe inside a cell splits the row; an escaped one splits it too,
    # so both shift every cell after them: name the cause, never the shifted symptom.
    pipes=gsub(/\|/,"|",line)
    pipebad=0
    if (line ~ /\\\|/) { finding(id,"SHAPE_PIPE","escaped pipe (\\|) in row"); pipebad=1 }
    else if (pipes>12) { finding(id,"SHAPE_PIPE","literal pipes=" pipes " want=12"); pipebad=1 }
    if (!in_registry) finding(id,"SHAPE_SECTION","row outside ## Registry section")
    if (pipebad) next
    if (NF!=13) { finding(id,"SHAPE_COLUMNS","columns=" (NF-2) " want=11"); next }
    status=trim($9); opened=trim($10)
    if (status !~ /^(queued|mined|rejected)$/) finding(id,"SHAPE_STATUS","status=" status)
    oe=epoch(opened)
    if (oe==-1e15) finding(id,"SHAPE_OPENED","opened=" opened " not an ISO calendar date")
    else if (oe>today_epoch) finding(id,"SHAPE_OPENED","opened=" opened " is in the future")
  }
  END { printf "%s\tCENSUS_SHAPE\tnew_rows=%d findings=%d\n",lane,newrows+0,findings+0
        exit (findings>0 ? 1 : 0) }' "$SOURCES_ABS" | tee "$TMP/shape.out" | sink
SHAPE_EXIT=${PIPESTATUS[0]}

# ---- 5. verdict lines ---------------------------------------------------------
NEWROWS=$(awk -F'\t' '$2=="CENSUS_SHAPE" && $3 ~ /^new_rows=/ {
  sub(/^new_rows=/,"",$3); sub(/ .*/,"",$3); print $3 }' "$TMP/shape.out")
FINDINGS=$(awk -F'\t' '$2=="CENSUS_SHAPE" && $3 ~ /^new_rows=/ {
  sub(/^.*findings=/,"",$3); print $3 }' "$TMP/shape.out")

VERDICT_EXIT=0
[ "$SHAPE_EXIT" != 0 ] && VERDICT_EXIT=1
if [ "$SHAPE_ONLY" = 0 ]; then
  emit "CENSUS exit=$CENSUS_EXIT rows=$ROWS"
  emit "CENSUS_ROWS_SELFCHECK census=$ROWS grep=$GREP_ROWS"
  if [ "$ROWS" != "$GREP_ROWS" ]; then MISMATCH=true; VERDICT_EXIT=1; else MISMATCH=false; fi
  [ "$CENSUS_EXIT" != 0 ] && VERDICT_EXIT=$CENSUS_EXIT
else
  emit "CENSUS exit=skipped rows=-"
  MISMATCH=n/a
fi
emit "CENSUS_SHAPE_VERDICT pass=$([ "$VERDICT_EXIT" = 0 ] && echo true || echo false) new_rows=${NEWROWS:-0} findings=${FINDINGS:-0} rows_mismatch=$MISMATCH"
exit "$VERDICT_EXIT"
