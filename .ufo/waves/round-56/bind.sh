#!/bin/bash
# Round-56 re-key bind — the exact sequence the L1 (TameshiR56) runs, end to end.
#
# The problem it closes: the eighteen headings frozen in
# `.ufo/evidence/round-56/c1/lost-headings-at-base.json` credit at the floor
# (0a2010acd1e9, 64/64) and not at the base (981c5e8b, 46/64) because their ledger
# entries pin input digests that later rounds moved. The round-21 monitor credits a
# section only through an entry whose inputs still verify at the measured revision,
# so the repair is one re-key: fresh reader reports at C0, one bound entry per
# heading with inputs pinned at PIN, the ledger committed, the precheck at the
# commit that carries it.
#
# C0  = the commit whose SKILL.md carries the final `## Standing rules` bytes (that
#       is what the readers read; it may precede PIN).
# PIN = the content-final commit; the entries' inputs are pinned to its blobs.
#
# WHAT THIS SCRIPT DOES (and why step 4 is not literally "at PIN"): the binder
# writes the ledger into the LANE WORKING TREE, and every instrument reads git
# objects at a revision. A precheck at PIN would therefore measure the ledger as
# PIN carries it - the unbound one - and read the same 18 lost sections step 1 just
# named (RED by construction, not a pass). Step 4 measures the commit this script
# makes out of the binder's output instead. Pass BIND_REV=<rev> to skip the commit
# and measure a revision the L1 made itself; it must contain the re-key directory.
#
# PRE-CONDITIONS, checked here:
#   * every round-56 content edit is committed at or before PIN. Only LOG.md,
#     SCORECARD.md and SKILL.md are dropped by the binder; new files are inert;
#     any other byte change to a path in an entry's input set uncredits that
#     section at the deciding revision (round 53/55 failure mode). The binder DROP
#     list covers LOG.md, SCORECARD.md, SKILL.md and the ledger - nothing else.
#   * one reader report per frozen heading, committed at or before PIN, named
#     `T56W*...Read*.json` (the C1 counter's arm-4 pattern) with a `.md` beside it,
#     `cand` == C0 and `section_sha256` == that section's sha256 at C0. The binder
#     globs `*.json` in the wave dir and accepts the FIRST file (sorted) that
#     matches heading+cand+sha, so a non-reader JSON that carries a `heading` key
#     can be bound by mistake; keep the reader names unique and the shape exact.
#   * reader findings: this script passes `--resolutions` pointing at a path that
#     does not exist, so ZERO findings are allowed per heading. Without that flag
#     the binder falls back to `.ufo/evidence/round-54/integrate/resolutions.json`,
#     which grants 1-11 findings to ten of the eighteen headings here and would
#     bind a reader with findings as `verdict gap-minor` without the L1 ever
#     adjudicating it. Set RESOLUTIONS=<file> to opt into that deliberately.
#
# Usage:
#   C0=<full 40-hex> PIN=<full 40-hex> bash .ufo/waves/round-56/bind.sh
#   WAVES=.ufo/waves/round-56/w3 C0=.. PIN=.. bash .../bind.sh   # readers in w3
#   BIND_REV=<rev> C0=.. PIN=.. bash .../bind.sh                 # L1 already committed
# Exit: 0 pass; 2 usage/guard; 3 drift set != the frozen eighteen; 4 binder SKIP;
#       5 unexpected working-tree changes at commit time; 6 a pinned input moved
#       between PIN and the bound revision; 7 precheck RED; 8 monitor short.
set -euo pipefail

LANE=${LANE:-/home/vgpnk/Projects/shokunin/tameshi-shokunin}
FLOOR=0a2010acd1e92e4e332774050825e21bcfc7e079
FROZEN=$LANE/.ufo/evidence/round-56/c1/lost-headings-at-base.json
MON=$LANE/.ufo/evidence/round-21/coldread/measure.py
PRECHECK=$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh
BINDER=$LANE/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py
WAVES=${WAVES:-.ufo/waves/round-56/w2}
LABEL=${LABEL:-'L1 TameshiR56 re-key (round 56)'}
RESOLUTIONS=${RESOLUTIONS:-/nonexistent/round-56-resolutions.json}
C0=${C0:?set C0 to the commit the readers read (full 40-hex)}
PIN=${PIN:?set PIN to the content-final commit (full 40-hex, >= C0)}
BIND_REV=${BIND_REV:-}
: "${HYAKU_SCRATCH:=/fast/scratch/hyaku}"
W=${W:-$HYAKU_SCRATCH/tameshi-r56/L1-bind}
mkdir -p "$W"

# ---- 0. guards -----------------------------------------------------------------
[ -d "$LANE" ] || { echo "BIND error=lane-missing $LANE"; exit 2; }
[ "$(git -C "$LANE" rev-parse --show-toplevel)" = "$LANE" ] || {
  echo "BIND error=lane-not-toplevel"; exit 2; }
C0=$(git -C "$LANE" rev-parse --verify --quiet "$C0^{commit}") || {
  echo "BIND error=c0-unresolvable"; exit 2; }
PIN=$(git -C "$LANE" rev-parse --verify --quiet "$PIN^{commit}") || {
  echo "BIND error=pin-unresolvable"; exit 2; }
case $C0$PIN in *[!0-9a-f]*) echo "BIND error=rev-not-full-hex"; exit 2;; esac
[ ${#C0} -eq 40 ] && [ ${#PIN} -eq 40 ] || { echo "BIND error=rev-not-full-hex"; exit 2; }
git -C "$LANE" merge-base --is-ancestor "$C0" "$PIN" || {
  echo "BIND error=c0-not-ancestor-of-pin"; exit 2; }
[ -f "$BINDER" ] && [ -f "$MON" ] && [ -f "$PRECHECK" ] && [ -f "$FROZEN" ] || {
  echo "BIND error=instrument-missing"; exit 2; }
echo "BIND lane=$LANE c0=$C0 pin=$PIN waves=$WAVES label=$LABEL"

# ---- 1. the drift set at PIN must be EXACTLY the eighteen frozen headings ------
python3 "$MON" --repo "$LANE" --rev "$FLOOR" > "$W/floor.json"
python3 "$MON" --repo "$LANE" --rev "$PIN" --explain > "$W/pin.json"
python3 - "$W/floor.json" "$W/pin.json" "$FROZEN" "$W/headings.json" <<'PY'
import json, sys
floor = {s['heading'] for s in json.load(open(sys.argv[1]))['coldread']['sections']
         if s['credited']}
pin = {s['heading']: s for s in json.load(open(sys.argv[2]))['coldread']['sections']}
frozen = json.load(open(sys.argv[3]))
lost = sorted(h for h in floor if not pin[h]['credited'])
json.dump(lost, open(sys.argv[4], 'w'), indent=1)
for h in lost:
    print('LOST %s | %s' % (h, pin[h]['reason'][:400]))
extra = sorted(set(lost) - set(frozen))
missing = sorted(set(frozen) - set(lost))
print('DRIFT headings=%d frozen=%d extra=%d missing=%d' %
      (len(lost), len(frozen), len(extra), len(missing)))
for h in extra:
    print('DRIFT-EXTRA %s | %s' % (h, pin[h]['reason'][:400]))
for h in missing:
    print('DRIFT-MISSING %s' % h)
sys.exit(0 if lost == sorted(frozen) else 3)
PY

# ---- 1b. exactly one round-56 re-key directory may exist (C1 arm 3) ------------
shopt -s nullglob
WT_DIRS=( "$LANE"/.ufo/evidence/round-21/coldread/rekey-r56-* )
shopt -u nullglob
for d in "${WT_DIRS[@]+"${WT_DIRS[@]}"}"; do
  [ "$(basename "$d")" = "rekey-r56-${C0:0:12}" ] || {
    echo "BIND error=stale-rekey-dir $(basename "$d") (C1 arm 3 requires exactly one)"; exit 2; }
done
if git -C "$LANE" ls-tree -r --name-only "$PIN" .ufo/evidence/round-21/coldread/ \
   | grep -oE 'rekey-r56-[0-9a-f]{12}' | sort -u | grep -vx "rekey-r56-${C0:0:12}" >&2; then
  echo "BIND error=stale-rekey-dir-at-pin (C1 arm 3 requires exactly one)"; exit 2
fi

# ---- 2. bind (replace-safe: a second pass over a later PIN replaces, never grows)
OUT=$LANE/.ufo/evidence/round-21/coldread/rekey-r56-${C0:0:12}
mkdir -p "$OUT"
# TMPDIR: the binder writes the extracted round-18 sectionizer there; without it the
# file lands in OUT and `git add -A` would commit it into the evidence tree.
set +e
TMPDIR=$W/binder-tmp python3 "$BINDER" "$LANE" "$C0" "$PIN" "$OUT" \
  --headings "$W/headings.json" \
  --waves "$WAVES" \
  --resolutions "$RESOLUTIONS" \
  --label "$LABEL" | tee "$W/binder.stdout"
binc=$?
set -e

# ---- 3. refuse on any SKIP ------------------------------------------------------
N=$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$W/headings.json")
[ "$binc" -eq 0 ] || {
  echo "BIND error=binder-exit-$binc (adjudicate every SKIP/error line above before freezing)"
  echo "BIND note=the binder has ALREADY written the successful subset to ledger.json"
  echo "  and $OUT (refresh-receipts.json + traces) - restore the ledger or re-run"
  echo "  after adjudication; a second pass replaces the entries, it does not grow them."
  exit 4; }
tail_line=$(grep '^REFRESH ' "$W/binder.stdout" | tail -1)
[ "$tail_line" = "REFRESH rekeyed=$N skipped=0 headings=$N" ] || {
  echo "BIND error=binder-tail expected='REFRESH rekeyed=$N skipped=0 headings=$N' got='$tail_line'"
  exit 4; }
[ "$(ls -1 "$OUT"/traces/section-*.json | wc -l)" -eq "$N" ] || {
  echo "BIND error=trace-count"; exit 4; }

# ---- 3b. commit the ledger + traces (the L1's own commit) -----------------------
if [ -z "$BIND_REV" ]; then
  stray=$(git -C "$LANE" status --porcelain | grep -vE '^(..|\?\?) \.ufo/evidence/round-21/coldread/' || true)
  if [ -n "$stray" ]; then
    echo "BIND error=tree-dirty-outside-bind-output"; printf '%s\n' "$stray"; exit 5
  fi
  git -C "$LANE" add -A .ufo/evidence/round-21/coldread
  git -C "$LANE" commit --quiet -m "round-56: bind the ${N} base-lost cold-read headings at ${C0:0:12} (C1 re-key)"
  BIND_REV=$(git -C "$LANE" rev-parse HEAD)
else
  BIND_REV=$(git -C "$LANE" rev-parse --verify --quiet "$BIND_REV^{commit}") || {
    echo "BIND error=bind-rev-unresolvable"; exit 2; }
fi
git -C "$LANE" ls-tree -r --name-only "$BIND_REV" ".ufo/evidence/round-21/coldread/rekey-r56-${C0:0:12}/" \
  | grep -q '/traces/section-' || { echo "BIND error=bind-rev-lacks-rekey-dir"; exit 5; }
echo "BIND rev=$BIND_REV"

# ---- 3c. no pinned input may move between PIN and the bound revision -----------
python3 - "$LANE" "$PIN" "$BIND_REV" "$OUT" <<'PY'
import glob, json, subprocess, sys
lane, pin, rev, out = sys.argv[1:5]
pinned = set()
for f in glob.glob(out + '/traces/*.json'):
    pinned |= set(json.load(open(f)).get('inputs') or {})
changed = set(subprocess.run(['git', '-C', lane, 'diff', '--name-only', pin, rev],
                             capture_output=True, text=True, check=True).stdout.split('\n'))
changed.discard('')
bad = sorted(pinned & changed)
print('PINNED inputs=%d changed=%d pinned-changed=%d' % (len(pinned), len(changed), len(bad)))
for p in bad:
    print('PINNED-CHANGED ' + p)
sys.exit(6 if bad else 0)
PY

# ---- 4. the precheck at the bound revision (must print lost=0 and exit 0) ------
bash "$PRECHECK" "$LANE" "$FLOOR" "$BIND_REV" | tee "$W/precheck.stdout"
grep -q 'lost=0 ok' "$W/precheck.stdout" || { echo "BIND error=precheck-red"; exit 7; }

# ---- 5. the monitor at the bound revision: the score the standing row must state
python3 "$MON" --repo "$LANE" --rev "$BIND_REV" --explain > "$W/bind-monitor.json"
python3 - "$W/bind-monitor.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
c = d['coldread']
print('MONITOR covered=%d/%d score=%s box3=%s trace_gate=%s overrides=%s'
      % (c['sections_covered'], c['sections_total'], d['calibration_restraint_score'],
         c['box3_full_page'], d['trace_gate'], d['overrides_used']))
sys.exit(0 if (c['sections_covered'] == c['sections_total']
               and d['calibration_restraint_score'] == 8
               and c['box3_full_page']) else 8)
PY
echo "BIND_PASS c0=$C0 pin=$PIN rev=$BIND_REV headings=$N"
