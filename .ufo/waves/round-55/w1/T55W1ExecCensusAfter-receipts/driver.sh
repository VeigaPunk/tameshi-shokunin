#!/usr/bin/env bash
# Round-55 T55W1ExecCensusAfter: candidate append + guard fixtures.
# Scratch-only; reads the lane, writes receipts into the seat receipts dir.
set -u
S=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCensusAfter
R=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ExecCensusAfter-receipts
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CEN=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
TODAY=2026-10-28
mkdir -p "$R"

# used-by paths in the registry are lane-root relative: two point at tools/
mkdir -p "$S/tools"
cp -a "$L/tools/tally-audit.py" "$L/tools/tally-audit-v3.py" "$S/tools/"

SUMMARY="$R/fixtures-summary.tsv"
: > "$SUMMARY"
printf 'fixture	rc	rows	E	W	ok_line	file\n' >> "$SUMMARY"

rows_of() { grep -cE '^ {0,3}\| S[0-9]{3,} \|' "$1" || true; }

# run <name> <rootdir>  (rootdir holds corpus/SOURCES.md and tools/)
run() {
  local name=$1 root=$2 rc rows E W okline
  "$CEN" validate --today "$TODAY" --file "$root/corpus/SOURCES.md" \
      > "$R/$name.tsv" 2> "$R/$name.err"
  rc=$?
  rows=$(rows_of "$root/corpus/SOURCES.md")
  E=$(grep -cE '	E[0-9]+	' "$R/$name.tsv" || true)
  W=$(grep -cE '	W[0-9]+	' "$R/$name.tsv" || true)
  okline=$(grep -cE '	ok	' "$R/$name.tsv" || true)
  printf '%s	%s	%s	%s	%s	%s	%s\n' "$name" "$rc" "$rows" "$E" "$W" "$okline" \
      "${root#/fast/scratch/hyaku/tameshi-r55/}" >> "$SUMMARY"
  printf '%-24s rc=%s rows=%s E=%s W=%s ok=%s errbytes=%s\n' \
      "$name" "$rc" "$rows" "$E" "$W" "$okline" "$(wc -c < "$R/$name.err")"
}

# mkroot <name>: fresh root with a copy of corpus/ + tools/
mkroot() {
  local name=$1 root="$S/fx/$1"
  rm -rf -- "$root"; mkdir -p "$root"
  cp -a "$S/corpus" "$root/corpus"
  cp -a "$S/tools" "$root/tools"
  printf '%s' "$root"
}

# insert_before_paths <file> <line>  (last-in-Registry insertion point)
insert_before_paths() {
  local f=$1 line=$2 tmp="$1.tmp"
  awk -v line="$line" '/^## Paths$/ && !done { print line; done=1 } { print }' "$f" > "$tmp" \
    && mv "$tmp" "$f"
}

S280_ROW=$(cat "$S/lane-S280-row.txt")
PROPOSED_ROW=$(cat "$S/proposed-S280-row.txt")

# --- candidate 0: lane corpus as-is (no append block, sanity baseline) ------
run cand0-lane-as-is "$S"

# --- candidate 1: the append block = round-55's single row, corrected form --
C1=$(mkroot cand1-corrected-s280)
python3 - "$C1/corpus/SOURCES.md" "$S/proposed-S280-row.txt" <<'PY'
import sys
path, roww = sys.argv[1], sys.argv[2]
row = open(roww, encoding='utf-8').read().rstrip('\n')
lines = open(path, encoding='utf-8').read().split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith('| S280 ')]
assert len(idx) == 1, idx
lines[idx[0]] = row
open(path, 'w', encoding='utf-8').write('\n'.join(lines))
PY
sha256sum "$C1/corpus/SOURCES.md" | sed 's#/fast/scratch.*/##' > "$R/cand1-sha.txt"
run cand1-corrected-s280 "$C1"

# --- defect fixtures -------------------------------------------------------
# fx-dup-Nsp: the exact S280 row re-inserted at N-space indent (0,1,2,3,4)
for n in 0 1 2 3 4; do
  name="fx-dup-${n}sp"
  root=$(mkroot "$name")
  pad=$(printf '%*s' "$n" '')
  insert_before_paths "$root/corpus/SOURCES.md" "${pad}${S280_ROW}"
  run "$name" "$root"
done

# fx-dup-diff-url: S280's id on a different URL/scope -> id guard alone
name=fx-dup-diff-url
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  '| S280 | A different source entirely — https://example.example/other | docs | B | unrelated scope | §1 | an unrelated claim | queued | 2026-10-28 | 30d | — |'
run "$name" "$root"

# fx-pipe-11col: an 11-column row whose teaches cell carries a literal pipe
name=fx-pipe-11col
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  '| S281 | Pipe fixture — https://example.example/pipe | docs | B | pipe parsing fixture | §1 | teaches text | with a literal pipe | queued | 2026-10-28 | 30d | — |'
run "$name" "$root"

# fx-pipe-4sp: the same row indented 4 -> parser never sees it
name=fx-pipe-4sp
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  '    | S281 | Pipe fixture — https://example.example/pipe | docs | B | pipe parsing fixture | §1 | teaches text | with a literal pipe | queued | 2026-10-28 | 30d | — |'
run "$name" "$root"

# fx-pipe-absorbed: literal pipe in the teaches cell + one cell omitted =>
# 11 split groups again; the arithmetic guard cannot see it.
name=fx-pipe-absorbed
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  '| S281 | Pipe absorbed — https://example.example/absorb | docs | B | absorbed pipe fixture | §1 | teaches text | queued | 2026-10-28 | 30d | — |'
run "$name" "$root"

# fx-supersedes: the contract's correction form (new id, same URL+scope,
# teaches opens "supersedes S280") -- admissible, no E04 and no W04
SCOPE="the line shape of a noninteractive program's error message"
URL='https://www.gnu.org/prep/standards/html_node/Errors.html'
name=fx-supersedes
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  "| S281 | Formatting Error Messages (GNU Coding Standards §4.4), correction of S280 — $URL | spec | A | $SCOPE | §4.4 Formatting Error Messages @ fetched 2026-10-28 | supersedes S280 — the message starts lower-case and ends without a period, and the section states no exit code | mined | 2026-10-28 | 730d | corpus/knowledge/scratch-root-contract.md |"
run "$name" "$root"

# fx-supersedes-absent: same URL+scope, new id, no supersedes token -> E04
name=fx-supersedes-absent
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  "| S281 | Formatting Error Messages (GNU Coding Standards §4.4), duplicate claim — $URL | spec | A | $SCOPE | §4.4 Formatting Error Messages @ fetched 2026-10-28 | the same claim restated, without the supersedes token | mined | 2026-10-28 | 730d | corpus/knowledge/scratch-root-contract.md |"
run "$name" "$root"

# fx-dup-tab: tab-indented duplicate -> parser never sees it
name=fx-dup-tab
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" "$(printf '	')${S280_ROW}"
run "$name" "$root"

# fx-pipe-shift: literal pipe + one omitted cell -> NF=13 again; the misparse
# surfaces only as enum noise (E07/E08), never as "malformed row"
name=fx-pipe-shift
root=$(mkroot "$name")
insert_before_paths "$root/corpus/SOURCES.md" \
  '| S281 | Pipe shift — https://example.example/shift | docs | B | shifted pipe fixture | §1 | teaches with a | pipe | mined | 2026-10-28 | 30d |'
run "$name" "$root"

# fx-eof-outside: row appended at EOF, after ## Id allocation -> E12
name=fx-eof-outside
root=$(mkroot "$name")
printf '%s\n' '| S281 | Outside fixture — https://example.example/outside | docs | B | outside registry | §1 | row appended after the registry | queued | 2026-10-28 | 30d | — |' \
  >> "$root/corpus/SOURCES.md"
run "$name" "$root"

# --- warning-set delta: cand1 vs cand0 (the append must add no finding) -----
grep -E '	[EW][0-9]+	' "$R/cand0-lane-as-is.tsv" | sed 's/^file	//' | sort > "$S/w-cand0.txt"
grep -E '	[EW][0-9]+	' "$R/cand1-corrected-s280.tsv" | sed 's/^file	//' | sort > "$S/w-cand1.txt"
diff -u "$S/w-cand0.txt" "$S/w-cand1.txt" > "$R/append-warning-delta.stdout"
printf 'append warning delta lines: %s (0 = the candidate append adds no finding)\n' \
  "$(grep -cE '^[+-][^+-]' "$R/append-warning-delta.stdout" || true)"

# --- column structure of the candidate rows --------------------------------
{
  echo "# field counts by row (NF must be 13; 11 cells + 2 boundary pipes)"
  for f in "$S/corpus/SOURCES.md" "$C1/corpus/SOURCES.md"; do
    echo "== ${f#/fast/scratch/hyaku/tameshi-r55/}"
    awk -F'|' '/^ {0,3}\| S[0-9]{3,}/{n=NF; c[n]++} END{for(k in c) printf "  NF=%s rows=%s\n",k,c[k]}' "$f" | sort
  done
} > "$R/candidate-field-counts.stdout"
cat "$R/candidate-field-counts.stdout"

# --- cross-check: candidate warning set vs the round's base-rev receipt ------
BASE=$L/.ufo/waves/round-55/w1/T55W1ExecCensus-receipts/base-validate.tsv
if [ -f "$BASE" ]; then
  grep -E '	[EW][0-9]+	' "$BASE" | cut -f2- | sort > "$S/w-base.txt"
  cut -f2- "$S/w-cand0.txt" | sort > "$S/w-cand0-norm.txt"
  diff -u "$S/w-base.txt" "$S/w-cand0-norm.txt" > "$R/warnings-vs-base.stdout"
  printf 'candidate-vs-base warning diff lines: %s\n' "$(grep -cE '^[+-][^+-]' "$R/warnings-vs-base.stdout" || true)"
  printf 'base bytes/lines: %s lines %s\n' "$(wc -l < "$BASE")" "$(wc -l < "$S/w-base.txt")"
fi

echo "=== summary ==="
cat "$SUMMARY"
