#!/usr/bin/env bash
# c1059-probe.sh — off-suite non-equivalence probe for survivor C1059
# (REPORT_MIN_BYTES 1024 -> 1059, round-gate.mjs :167 at 364f1d5,
#  blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9).
#
# Fixture: an otherwise-CLEAN audit whose round report is sized in [1024,1058]
# bytes (1040 here). Pristine gate (floor 1024) reports no REPORT_THIN -> exit 0;
# the C1059 mutant (floor 1059) must emit REPORT_THIN (bytes=1040) -> exit 1.
#
# The mutant is produced by re-cutting the C1059 spec edit from
# .ufo/evidence/round-16/round-gate/round-gate.defects.spec
# at lane commit c699c8c36d6e4eca4b796b81a8247904aa145ec8 (@old -> @new,
# single-occurrence literal replacement).
#
# Outputs (beside this script): c1059-pristine.log, c1059-mutant.log.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
LANE="$(git -C "$HERE" rev-parse --show-toplevel)"
SPEC_REV="${SPEC_REV:-c699c8c36d6e4eca4b796b81a8247904aa145ec8}"
SPEC_PATH=".ufo/evidence/round-16/round-gate/round-gate.defects.spec"
KUMITATE="${KUMITATE:-/home/vgpnk/Projects/shokunin/kumitate-shokunin}"
GATE_REV="364f1d5954158ef8844bca4a5fef57b05d2f2ca5"
GATE_SHA="f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9"
REPORT_BYTES=1040   # inside [REPORT_MIN_BYTES=1024, 1059): pristine passes, mutant thins

SCRATCH="$(mktemp -d /tmp/tameshi-r16w2-c1059-XXXXXX)" || exit 2
trap 'rm -rf "$SCRATCH"' EXIT
PRISTINE="$SCRATCH/round-gate.pristine.mjs"
MUTANT="$SCRATCH/round-gate.c1059.mjs"
SPEC="$SCRATCH/round-gate.defects.spec"

# --- 1. materialize pristine gate, pin the blob ------------------------------
git -C "$KUMITATE" show "$GATE_REV:scripts/round-gate.mjs" > "$PRISTINE" || exit 2
got_sha="$(sha256sum "$PRISTINE" | awk '{print $1}')"
if [ "$got_sha" != "$GATE_SHA" ]; then
  echo "FATAL: pristine blob sha256 $got_sha != $GATE_SHA" >&2; exit 2
fi

# --- 2. re-cut the C1059 spec edit -------------------------------------------
git -C "$LANE" show "$SPEC_REV:$SPEC_PATH" > "$SPEC" || exit 2
OLD="$(awk '/^@defect C1059 /{f=1;next} /^@defect /{f=0} f&&/^@old /{sub(/^@old /,"");print;exit}' "$SPEC")"
NEW="$(awk '/^@defect C1059 /{f=1;next} /^@defect /{f=0} f&&/^@new /{sub(/^@new /,"");print;exit}' "$SPEC")"
[ -n "$OLD" ] && [ -n "$NEW" ] || { echo "FATAL: C1059 @old/@new not found in spec" >&2; exit 2; }
cp "$PRISTINE" "$MUTANT"
node -e '
  const fs = require("fs");
  const [f, o, n] = process.argv.slice(1);
  const s = fs.readFileSync(f, "utf8");
  const hits = s.split(o).length - 1;
  if (hits !== 1) { console.error(`FATAL: @old occurs ${hits}x, need exactly 1`); process.exit(2); }
  fs.writeFileSync(f, s.replace(o, n));
' "$MUTANT" "$OLD" "$NEW" || exit 2
grep -nF "$NEW" "$MUTANT" >&2

# --- 3. fixture: clean audit + report of exactly $REPORT_BYTES bytes ---------
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t
export GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
export GIT_AUTHOR_DATE=2026-01-02T00:00:00+0000 GIT_COMMITTER_DATE=2026-01-02T00:00:00+0000

LANE_REPO="$SCRATCH/lane"; REPORTS="$SCRATCH/reports"; MAIN_REPO="$SCRATCH/main"; ORIGIN="$SCRATCH/origin"
git init -q -b main "$LANE_REPO"
cat > "$LANE_REPO/SCORECARD.md" <<'EOF'
# Scorecard

| round | axis | evidence |
|---|---|---|
| 5 | operability | fixture |
| 5 | coverage | fixture |

## Planned

round 6: the next fixture move.
EOF
printf -- '- 2026-01-02 — round 5 fixture entry (lane kumitate)\n' > "$LANE_REPO/LOG.md"
git -C "$LANE_REPO" add -A && git -C "$LANE_REPO" commit -q -m 'round-5 fixture seed'
git init -q -b main "$MAIN_REPO" && echo main > "$MAIN_REPO/README.md" \
  && git -C "$MAIN_REPO" add -A && git -C "$MAIN_REPO" commit -q -m 'main seed'
git init -q -b main "$ORIGIN" && echo origin > "$ORIGIN/origin.txt" \
  && git -C "$ORIGIN" add -A && git -C "$ORIGIN" commit -q -m 'origin seed'

REPORT="$REPORTS/round-5/kumitate.md"; mkdir -p "$(dirname "$REPORT")"
{
  printf '# round-5 lane report\n\n## SHONEN\n\n- lane checklist: fixture pass\n\n## Findings\n\n'
  printf 'The round-5 fixture landed with evidence on disk.\n'
} > "$REPORT"
have="$(wc -c < "$REPORT")"
pad=$(( REPORT_BYTES - have - 5 ))   # "pad:" + x*pad + "\n"
[ "$pad" -ge 0 ] || { echo "FATAL: base report $have B > $REPORT_BYTES" >&2; exit 2; }
printf 'pad:%s\n' "$(printf '%*s' "$pad" '' | tr ' ' x)" >> "$REPORT"
have="$(wc -c < "$REPORT")"
[ "$have" -eq "$REPORT_BYTES" ] || { echo "FATAL: report is $have B" >&2; exit 2; }

# --- 4. run pristine vs mutant (hermetic env) --------------------------------
mkdir -p "$SCRATCH/home" "$SCRATCH/tmp"
run_gate() {  # $1=gate file  $2=log path
  env -i PATH="$PATH" HOME="$SCRATCH/home" TMPDIR="$SCRATCH/tmp" \
    node "$1" --round 5 --repo "$LANE_REPO" --reports-dir "$REPORTS" \
      --main-repo "$MAIN_REPO" --origin "$ORIGIN" > "$2.out" 2> "$2.err"
  echo "$?"
}

{
  echo "probe=C1059 report_bytes=$have floor=1024 gate_rev=$GATE_REV sha256=$got_sha"
  echo "node=$(node --version) fixture=$SCRATCH"
  echo "cmd: node round-gate.pristine.mjs --round 5 --repo lane --reports-dir reports --main-repo main --origin origin"
  pe="$(run_gate "$PRISTINE" "$SCRATCH/pristine")"
  echo "exit=$pe"
  echo "--- stdout ---"; cat "$SCRATCH/pristine.out"
  echo "--- stderr ---"; cat "$SCRATCH/pristine.err"
} > "$HERE/c1059-pristine.log"

{
  echo "probe=C1059 report_bytes=$have floor=1059 spec=@$SPEC_REV:$SPEC_PATH"
  echo "edit: $OLD -> $NEW"
  echo "cmd: node round-gate.c1059.mjs --round 5 --repo lane --reports-dir reports --main-repo main --origin origin"
  me="$(run_gate "$MUTANT" "$SCRATCH/mutant")"
  echo "exit=$me"
  echo "--- stdout ---"; cat "$SCRATCH/mutant.out"
  echo "--- stderr ---"; cat "$SCRATCH/mutant.err"
} > "$HERE/c1059-mutant.log"

cat "$HERE/c1059-pristine.log" "$HERE/c1059-mutant.log"
