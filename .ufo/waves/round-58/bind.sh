#!/bin/bash
# Round-58 re-key bind (adapted from the round-57 binder) - the sequence the L1 (TameshiR58) runs at the content commit C0.
#
# What differs from round 56: the drift set is NOT a frozen list. Round 56 froze the
# eighteen lost headings at base; this round's edits (SOURCES/QUALITY/README/SKILL/tools)
# move ledger input digests by amounts nobody can list before the content is final, so
# step 1 COMPUTES the lost headings at C0:
#       lost = (headings credited at FLOOR) minus (headings credited at C0)
# with the round-21 monitor, cross-checks the set against the round-48 precheck's LOST
# lines (two instruments, one answer), and writes it to
#       .ufo/evidence/round-58/c1/lost-headings-at-c0.json
# The same script then refuses unless every lost heading has exactly one committed reader
# report (`T58W2*Read*.json` + `.md` beside it, `cand` == C0, `section_sha256` == that
# section's sha256 at C0), binds them with the round-55 binder, and measures the monitor
# at BIND_REV (credited == total, score 8, box3 full page; exit 8 otherwise).
#
# C0  = the content-final commit; the readers read SKILL.md at it.
# PIN = the revision the entries' input digests are pinned at (default C0; must descend
#       from C0). BIND_REV = the L1's own commit of the binder output.
#
# THIS SCRIPT COMMITS NOTHING. The binder writes into the LANE WORKING TREE and every
# instrument reads git objects, so the run is two-phase and the same command both times:
#   phase 1 (BIND_REV unset): steps 0-3 -> BIND_STAGED, exit 0. The working tree now
#           carries the ledger, the rekey-r58-<c0> directory and lost-headings-at-c0.json;
#           the L1 commits exactly those (jj-lane.sh) and notes the commit id.
#   phase 2 (BIND_REV=<that commit>): re-runs steps 0-3 (byte-identical: the binder reads
#           the ledger at C0 and every argv path is stable), requires the working tree's
#           bind output to equal BIND_REV's blobs (exit 5 otherwise), then steps 3c-5.
#
# PRE-CONDITIONS, checked here:
#   * every content edit is committed at or before PIN. Only LOG.md, SCORECARD.md and
#     SKILL.md are dropped from an entry's input set by the binder (plus the ledger);
#     any other byte change to a pinned path uncredits that section at the deciding
#     revision (round 53/55 failure mode) - step 3c and the step-4 precheck catch it.
#   * reader reports: committed at PIN, in $WAVES, named `T58W2*Read*.json`. The binder
#     globs `*.json` and accepts the FIRST sorted file that matches heading+cand+sha, so
#     a non-reader JSON carrying a `heading` key could be bound by mistake. Step 1c
#     therefore requires exactly ONE matching file per heading and that it is a reader
#     file (exit 9 otherwise).
#   * reader findings: --resolutions points at a path that does not exist, so ZERO
#     findings are allowed per heading (the binder would otherwise fall back to an older
#     round's grants). Set RESOLUTIONS=<file> to opt into adjudicated findings.
#
# R56.4 (resolved here): the binder labels each `external_inputs` key `tameshi@<C0>:<path>`
# but pins the digest from the blob at PIN. After binding, step 2b lists every entry whose
# label names a blob whose sha256 at the labelled revision is not the recorded digest and
# prints `BIND_LABELS: n_mismatch=<k>` (0 whenever PIN == C0). Informational; never fatal.
#
# Usage:
#   C0=<40-hex> bash .ufo/waves/round-58/bind.sh                       # PIN defaults to C0
#   C0=.. PIN=.. WAVES=.ufo/waves/round-58/w2 bash .../bind.sh
#   BIND_REV=<rev> C0=.. PIN=.. bash .../bind.sh                       # phase 2
# Exit: 0 pass/staged; 2 usage/guard; 3 monitor and precheck disagree on the lost set;
#       4 binder SKIP; 5 unexpected working-tree changes / BIND_REV is not the binder
#       output; 6 a pinned input moved between PIN and BIND_REV; 7 precheck RED at
#       BIND_REV; 8 monitor short at BIND_REV (or at C0 when nothing was lost);
#       9 reader reports missing/invalid/ambiguous.
set -euo pipefail

LANE=${LANE:-/home/vgpnk/Projects/shokunin/tameshi-shokunin}
FLOOR=${FLOOR:-2a32aa8228d5f86a85c81a923a3148bf792a9538}
MON=$LANE/.ufo/evidence/round-21/coldread/measure.py
PRECHECK=$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh
BINDER=$LANE/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py
LOSTREL=.ufo/evidence/round-58/c1/lost-headings-at-c0.json
LOST=$LANE/$LOSTREL
WAVES=${WAVES:-.ufo/waves/round-58/w2}
LABEL=${LABEL:-'L1 TameshiR58 re-key (round 58)'}
RESOLUTIONS=${RESOLUTIONS:-/nonexistent/round-58-resolutions.json}
C0=${C0:?set C0 to the content-final commit the readers read (full 40-hex)}
PIN=${PIN:-$C0}
BIND_REV=${BIND_REV:-}
: "${HYAKU_SCRATCH:=/fast/scratch/hyaku}"
W=${W:-$HYAKU_SCRATCH/tameshi-r58/L1-bind}
mkdir -p "$W"

# ---- 0. guards -----------------------------------------------------------------
[ -d "$LANE" ] || { echo "BIND error=lane-missing $LANE"; exit 2; }
[ "$(git -C "$LANE" rev-parse --show-toplevel)" = "$LANE" ] || {
  echo "BIND error=lane-not-toplevel"; exit 2; }
case $C0$PIN in *[!0-9a-f]*) echo "BIND error=rev-not-full-hex"; exit 2;; esac
[ ${#C0} -eq 40 ] && [ ${#PIN} -eq 40 ] || { echo "BIND error=rev-not-full-hex"; exit 2; }
C0=$(git -C "$LANE" rev-parse --verify --quiet "$C0^{commit}") || {
  echo "BIND error=c0-unresolvable"; exit 2; }
PIN=$(git -C "$LANE" rev-parse --verify --quiet "$PIN^{commit}") || {
  echo "BIND error=pin-unresolvable"; exit 2; }
FLOOR=$(git -C "$LANE" rev-parse --verify --quiet "$FLOOR^{commit}") || {
  echo "BIND error=floor-unresolvable"; exit 2; }
git -C "$LANE" merge-base --is-ancestor "$C0" "$PIN" || {
  echo "BIND error=c0-not-ancestor-of-pin"; exit 2; }
[ -f "$BINDER" ] && [ -f "$MON" ] && [ -f "$PRECHECK" ] || {
  echo "BIND error=instrument-missing"; exit 2; }
echo "BIND lane=$LANE floor=${FLOOR:0:12} c0=$C0 pin=$PIN waves=$WAVES label=$LABEL"

# ---- 1. the drift set at C0, computed: floor-credited minus C0-credited --------
python3 "$MON" --repo "$LANE" --rev "$FLOOR" > "$W/floor.json"
python3 "$MON" --repo "$LANE" --rev "$C0" --explain > "$W/c0.json"
mkdir -p "$(dirname "$LOST")"
python3 - "$W/floor.json" "$W/c0.json" "$LOST" <<'PY'
import json, sys
fl = json.load(open(sys.argv[1]))['coldread']
c0 = json.load(open(sys.argv[2]))['coldread']
floor = {s['heading'] for s in fl['sections'] if s['credited']}
if len(floor) != fl['sections_total'] or fl['sections_covered'] != fl['sections_total']:
    print('BIND error=floor-not-full credited=%d total=%d (the floor must credit every section)'
          % (len(floor), fl['sections_total']))
    sys.exit(2)
cur = {s['heading']: s for s in c0['sections']}
absent = sorted(floor - set(cur))
if absent:
    print('BIND error=heading-absent-at-c0 %s' % absent)
    sys.exit(2)
lost = sorted(h for h in floor if not cur[h]['credited'])
json.dump(lost, open(sys.argv[3], 'w'), indent=1)
for h in lost:
    print('LOST %s | %s' % (h, cur[h]['reason'][:400]))
print('DRIFT floor_credited=%d c0_credited=%d lost=%d' % (len(floor), c0['sections_covered'], len(lost)))
PY

# ---- 1a. the precheck must name the same set (two instruments, one answer) -----
set +e
bash "$PRECHECK" "$LANE" "$FLOOR" "$C0" > "$W/precheck-c0.stdout"
set -e
python3 - "$W/precheck-c0.stdout" "$LOST" <<'PY'
import json, sys
lines = open(sys.argv[1]).read().splitlines()
pre = sorted(l[len('LOST '):].rpartition(' | drifted=')[0] for l in lines if l.startswith('LOST '))
mon = json.load(open(sys.argv[2]))
tail = [l for l in lines if l.startswith('COLDREAD_PRECHECK ')]
print('PRECHECK_C0 %s' % (tail[-1] if tail else 'NO-VERDICT-LINE'))
if not tail or pre != mon:
    print('BIND error=lost-set-disagree monitor=%d precheck=%d' % (len(mon), len(pre)))
    for h in sorted(set(mon) ^ set(pre)):
        print('DISAGREE %s' % h)
    sys.exit(3)
PY

N=$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$LOST")
if [ "$N" -eq 0 ]; then
  # nothing drifted at C0: nothing to bind; the monitor at C0 is the answer
  python3 "$MON" --repo "$LANE" --rev "$C0" --explain > "$W/bind-monitor.json"
  python3 - "$W/bind-monitor.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); c = d['coldread']
print('MONITOR covered=%d/%d score=%s box3=%s trace_gate=%s overrides=%s'
      % (c['sections_covered'], c['sections_total'], d['calibration_restraint_score'],
         c['box3_full_page'], d['trace_gate'], d['overrides_used']))
sys.exit(0 if (c['sections_covered'] == c['sections_total']
               and d['calibration_restraint_score'] == 8 and c['box3_full_page']) else 8)
PY
  echo "BIND_LABELS: n_mismatch=0"
  echo "BIND_PASS c0=$C0 pin=$PIN rev=$C0 headings=0 (no drift; nothing bound)"
  exit 0
fi

# ---- 1b. exactly one round-58 re-key directory may exist -----------------------
shopt -s nullglob
WT_DIRS=( "$LANE"/.ufo/evidence/round-21/coldread/rekey-r58-* )
shopt -u nullglob
for d in "${WT_DIRS[@]+"${WT_DIRS[@]}"}"; do
  [ "$(basename "$d")" = "rekey-r58-${C0:0:12}" ] || {
    echo "BIND error=stale-rekey-dir $(basename "$d") (exactly one rekey-r58-<c0> may exist)"; exit 2; }
done
if git -C "$LANE" ls-tree -r --name-only "$PIN" .ufo/evidence/round-21/coldread/ \
   | grep -oE 'rekey-r58-[0-9a-f]{12}' | sort -u | grep -vx "rekey-r58-${C0:0:12}" >&2; then
  echo "BIND error=stale-rekey-dir-at-pin (exactly one rekey-r58-<c0> may exist)"; exit 2
fi

# ---- 1c. one committed, exact reader report per lost heading -------------------
python3 - "$LANE" "$C0" "$PIN" "$WAVES" "$LOST" <<'PY'
import fnmatch, hashlib, importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path
lane, c0, pin, waves, lostf = sys.argv[1:6]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
def git(*a):
    return subprocess.run(['git', '-C', lane] + list(a), env=env, capture_output=True)
def show(rev, p):
    r = git('show', '%s:%s' % (rev, p))
    return r.stdout if r.returncode == 0 else None
tmp = tempfile.mkdtemp(prefix='bind-r18-', dir=os.environ.get('TMPDIR') or None)
src = Path(tmp) / 'r18.py'
src.write_bytes(show(c0, '.ufo/evidence/round-18/measure.py'))
spec = importlib.util.spec_from_file_location('r18_sect', src)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
sections = {s['heading']: s for s in mod.sectionize(show(c0, 'SKILL.md'))}
lost = json.load(open(lostf))
wdir = Path(lane, waves)
files = sorted(wdir.glob('*.json'))
reports = []
for f in files:
    try:
        d = json.loads(f.read_text('utf-8'))
    except ValueError:
        continue
    if isinstance(d, dict) and isinstance(d.get('heading'), str):
        reports.append((f, d))
bad = []
used = set()
for h in lost:
    sec = sections.get(h)
    if sec is None:
        bad.append('%s | no-section-at-c0' % h); continue
    match = [(f, d) for f, d in reports
             if d['heading'] == h and d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']]
    if len(match) != 1:
        bad.append('%s | matching-reports=%d (want exactly 1 with cand=C0 and section_sha256=%s)'
                   % (h, len(match), sec['sha256'][:12]))
        continue
    f, d = match[0]
    rel = os.path.relpath(f, lane)
    md = rel[:-5] + '.md'
    used.add(f)
    if not fnmatch.fnmatch(f.name, 'T58W2*Read*.json'):
        bad.append('%s | report %s is not named T58W2*Read*.json' % (h, rel)); continue
    for p in (rel, md):
        blob = show(pin, p)
        if blob is None:
            bad.append('%s | %s not committed at PIN' % (h, p))
        elif not (Path(lane, p).is_file() and Path(lane, p).read_bytes() == blob):
            bad.append('%s | %s differs between PIN and the working tree' % (h, p))
    print('READER %s | %s findings=%d' % (h[:70], f.name, len(d.get('findings') or [])))
for f, d in reports:
    if f not in used and fnmatch.fnmatch(f.name, 'T58W2*Read*.json') and d['heading'] not in lost:
        print('READER-EXTRA %s | %s (heading not in the lost set; ignored)' % (d['heading'][:70], f.name))
print('READERS lost=%d bad=%d' % (len(lost), len(bad)))
for b in bad:
    print('READER-BAD ' + b)
sys.exit(9 if bad else 0)
PY

# ---- 2. bind (replace-safe: a second pass over the same C0 replaces, never grows)
OUT=$LANE/.ufo/evidence/round-21/coldread/rekey-r58-${C0:0:12}
mkdir -p "$OUT" "$W/binder-tmp"
# TMPDIR: the binder writes the extracted round-18 sectionizer there; without it the
# file lands in OUT and would be committed into the evidence tree.
set +e
TMPDIR=$W/binder-tmp python3 "$BINDER" "$LANE" "$C0" "$PIN" "$OUT" \
  --headings "$LOST" \
  --waves "$WAVES" \
  --resolutions "$RESOLUTIONS" \
  --label "$LABEL" | tee "$W/binder.stdout"
binc=$?
set -e

# ---- 3. refuse on any SKIP ------------------------------------------------------
[ "$binc" -eq 0 ] || {
  echo "BIND error=binder-exit-$binc (adjudicate every SKIP/error line above before committing)"
  echo "BIND note=the binder has ALREADY written the successful subset to ledger.json"
  echo "  and $OUT - restore the ledger or re-run after adjudication; a second pass"
  echo "  replaces the entries, it does not grow them."
  exit 4; }
tail_line=$(grep '^REFRESH ' "$W/binder.stdout" | tail -1)
[ "$tail_line" = "REFRESH rekeyed=$N skipped=0 headings=$N" ] || {
  echo "BIND error=binder-tail expected='REFRESH rekeyed=$N skipped=0 headings=$N' got='$tail_line'"
  exit 4; }
[ "$(ls -1 "$OUT"/traces/section-*.json | wc -l)" -eq "$N" ] || {
  echo "BIND error=trace-count"; exit 4; }

# ---- 3a. R56.4: does each external_inputs label name the blob it digests? ------
python3 - "$LANE" "$C0" "$OUT" <<'PY'
import json, os, re, subprocess, sys, hashlib
lane, c0, out = sys.argv[1:4]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
rekey = os.path.relpath(out, lane)
ledger = json.load(open(os.path.join(lane, '.ufo/evidence/round-21/coldread/ledger.json')))
mism, labels, entries = [], 0, 0
for e in ledger['entries']:
    if not (isinstance(e, dict) and e.get('read_rev') == c0
            and any(isinstance(t, str) and t.startswith(rekey + '/') for t in (e.get('traces') or []))):
        continue
    entries += 1
    for label, digest in sorted((e.get('external_inputs') or {}).items()):
        labels += 1
        m = re.match(r'^tameshi@([0-9a-f]{40}):(.+)$', label)
        if not m:
            mism.append((e['heading'], label, digest, 'unparseable-label')); continue
        r = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (m.group(1), m.group(2))],
                           capture_output=True, env=env)
        got = hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else 'ABSENT'
        if got != digest:
            mism.append((e['heading'], label, digest, got))
for h, label, digest, got in mism:
    print('BIND_LABEL_MISMATCH %s | %s | recorded=%s blob-at-label=%s'
          % (h[:70], label, digest[:12], got[:12]))
print('BIND_LABELS: n_mismatch=%d' % len(mism))
print('BIND_LABELS_DETAIL entries=%d labels=%d (digest pinned at PIN; label names C0)'
      % (entries, labels))
PY

# ---- 3b. phase 1 stops here; phase 2 proves BIND_REV is this output -------------
if [ -z "$BIND_REV" ]; then
  stray=$(git -C "$LANE" status --porcelain --untracked-files=all \
    | grep -vE '^(..|\?\?) (\.ufo/evidence/round-21/coldread/|'"${LOSTREL//./\\.}"'$)' || true)
  if [ -n "$stray" ]; then
    echo "BIND error=tree-dirty-outside-bind-output"; printf '%s\n' "$stray"; exit 5
  fi
  echo "BIND_STAGED c0=$C0 pin=$PIN headings=$N ledger+rekey-r58-${C0:0:12}+$LOSTREL await the L1's commit;"
  echo "  then: BIND_REV=<that commit> C0=$C0 PIN=$PIN bash <this script>"
  exit 0
fi
BIND_REV=$(git -C "$LANE" rev-parse --verify --quiet "$BIND_REV^{commit}") || {
  echo "BIND error=bind-rev-unresolvable"; exit 2; }
git -C "$LANE" merge-base --is-ancestor "$PIN" "$BIND_REV" || {
  echo "BIND error=pin-not-ancestor-of-bind-rev"; exit 2; }
git -C "$LANE" ls-tree -r --name-only "$BIND_REV" ".ufo/evidence/round-21/coldread/rekey-r58-${C0:0:12}/" \
  | grep -q '/traces/section-' || { echo "BIND error=bind-rev-lacks-rekey-dir"; exit 5; }
python3 - "$LANE" "$BIND_REV" "$OUT" "$LOSTREL" <<'PY'
import os, subprocess, sys
from pathlib import Path
lane, rev, out, lostrel = sys.argv[1:5]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
rekey = os.path.relpath(out, lane)
want = subprocess.run(['git', '-C', lane, 'ls-tree', '-r', '--name-only', rev, rekey + '/'],
                      capture_output=True, text=True, env=env, check=True).stdout.split('\n')
want = [p for p in want if p] + ['.ufo/evidence/round-21/coldread/ledger.json', lostrel]
have = sorted(str(p.relative_to(lane)) for p in Path(out).rglob('*') if p.is_file())
bad = ['extra-in-tree ' + p for p in have if p not in want]
for p in want:
    r = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, p)], capture_output=True, env=env)
    f = Path(lane, p)
    if r.returncode != 0:
        bad.append('absent-at-bind-rev ' + p)
    elif not f.is_file() or f.read_bytes() != r.stdout:
        bad.append('differs-from-bind-rev ' + p)
print('BIND_TREE files=%d bad=%d' % (len(want), len(bad)))
for b in bad:
    print('BIND_TREE-BAD ' + b)
sys.exit(5 if bad else 0)
PY
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
