#!/bin/bash
# T55W3CritRekeyLoop — reproduces every receipt in this directory.
# Read-only on the lane: every mutation happens in `git clone --shared` copies
# under $S. The shared scratch parent is never removed; only $S is.
#
# usage: run.sh [OUTDIR]     (default: this directory)
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
OUT=${1:-$LANE/.ufo/waves/round-55/w3/T55W3CritRekeyLoop-receipts}
S=$HYAKU_SCRATCH/tameshi-r55/T55W3CritRekeyLoop
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
PIN=4f7a7040a57e7aed17db941be9c27b300aafb783
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/tmp" "$S/receipts" "$OUT"
cd "$S" || exit 2

say() { echo "### $*"; }

say "clone at HEAD ($PIN)"
git clone --shared --quiet "$LANE" lane || exit 2
git -C lane rev-parse --show-toplevel

say "1. floor before the re-key (C0 and PIN)"
{
  for r in "$C0" "$PIN"; do
    echo "== rev $r"
    python3 lane/.ufo/evidence/round-21/coldread/measure.py --repo "$S/lane" --rev "$r" |
      python3 -c "import json,sys;d=json.load(sys.stdin);print('score',d['calibration_restraint_score'],'covered',d['coldread']['sections_covered'],'of',d['coldread']['sections_total'],'box3',d['coldread']['box3_full_page'])"
  done
} | tee "$S/receipts/floor-before.out"

say "2. binder as committed (unpatched loader)"
mkdir -p lane/.ufo/evidence/round-21/coldread/rekey-r55-test
{ TMPDIR="$S/tmp" python3 lane/.ufo/evidence/round-55/integrate/binder.py "$S/lane" "$C0" "$PIN" \
    "$S/lane/.ufo/evidence/round-21/coldread/rekey-r55-test" 2>&1; echo "RC=$?"; } |
  tee "$S/receipts/binder-as-committed.out" | tail -4

say "3. inherited input set per heading (union of prior entries, C0 vs PIN blobs)"
python3 "$OUT/provenance.py" "$S/lane" "$C0" "$PIN" | tee "$S/receipts/provenance.out"

say "4. 18 reader files that read nothing (clone lane2)"
git clone --shared --quiet "$LANE" lane2 || exit 2
mkdir -p lane2/.ufo/waves/round-55/w3 lane2/.ufo/waves/round-55/w2
python3 "$OUT/make-fixture.py" "$S/lane2" "$C0" | tee "$S/receipts/fixture.out"

say "5. repair ONLY the resolutions loader (fixture patch), bind, commit, measure"
python3 - "$S/lane2/.ufo/evidence/round-55/integrate/binder.py" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
old = """if RES_PATH.exists():
    for item in json.loads(RES_PATH.read_text('utf-8')):
        RES[item['heading']] = int(item['n'])"""
new = """if RES_PATH.exists():
    for item in json.loads(RES_PATH.read_text('utf-8')):
        if isinstance(item, dict) and 'heading' in item and 'n' in item:
            RES[item['heading']] = int(item['n'])"""
assert old in t
p.write_text(t.replace(old, new))
print('loader patched (fixture only)')
PY
mkdir -p lane2/.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b
TMPDIR="$S/tmp" python3 -u lane2/.ufo/evidence/round-55/integrate/binder.py "$S/lane2" "$C0" "$PIN" \
  "$S/lane2/.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b" 2>&1 |
  tee "$S/receipts/binder-patched.out" | tail -3
test "$(git -C "$S/lane2" rev-parse --show-toplevel)" = "$S/lane2" || exit 2
git -C lane2 add -A
git -C lane2 -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "fixture: 18 non-reading readers + binder output"
R=$(git -C lane2 rev-parse HEAD)
echo "fixture-rev=$R" > "$S/receipts/ritual-measure.out"
python3 lane2/.ufo/evidence/round-21/coldread/measure.py --repo "$S/lane2" --rev "$R" |
  python3 -c "
import json,sys
d=json.load(sys.stdin)
print('score',d['calibration_restraint_score'])
print('covered',d['coldread']['sections_covered'],'/',d['coldread']['sections_total'])
print('box3',d['coldread']['box3_full_page'])
print('reasons',d['coldread']['reasons'])
print('uncovered',[m['heading'] for m in d['coldread']['missing']])" |
  tee -a "$S/receipts/ritual-measure.out"

say "6. two carried FAIL verdicts rewritten to a passing one"
python3 - "$S" <<'PY' | tee "$S/receipts/laundered-verdicts.out"
import json, sys
S = sys.argv[1]
new = json.load(open(S + '/lane2/.ufo/evidence/round-21/coldread/ledger.json'))['entries']
old = json.load(open(S + '/lane/.ufo/evidence/round-21/coldread/ledger.json'))['entries']
for h in ('### Round-15 gate/probe registry', '### Triggers T1\u2013T3 and the re-pin rule'):
    prior = [e for e in old if e.get('heading') == h]
    pick = max(prior, key=lambda e: str(e.get('read_rev', '')))
    got = [e for e in new if e.get('heading') == h and str(e.get('read_rev', '')).startswith('9cf0146')
           and any('/rekey-' in t for t in e.get('traces') or [])]
    print('HEADING', h)
    print('  prior pick     : verdict=%s class=%s read_rev=%s' % (pick.get('verdict'), pick.get('class'), pick.get('read_rev')[:12]))
    print('  new entry      : verdict=%s class=%s read_rev=%s blocking_gaps=%s wrong_expectations=%s commands=%s inputs=%d' % (
        got[0]['verdict'], got[0]['class'], got[0]['read_rev'][:12], got[0]['blocking_gaps'],
        got[0]['wrong_expectations'], got[0]['commands_executed_count'], len(got[0]['inputs'])))
    print('  evidence added : %s' % got[0]['reports'])
PY

say "7. replay of a recorded per-section argv"
python3 - "$S" <<'PY' | tee "$S/receipts/argv-replay.out"
import hashlib, json, os, subprocess, sys
S = sys.argv[1]; L = S + '/lane2'
tr = json.load(open(L + '/.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b/traces/section-07.json'))
ledger = L + '/.ufo/evidence/round-21/coldread/ledger.json'
before = hashlib.sha256(open(ledger, 'rb').read()).hexdigest()
print('recorded argv:', json.dumps(tr['argv']))
r = subprocess.run(tr['argv'], cwd=S + '/tmp', capture_output=True, text=True,
                   env={**os.environ, 'TMPDIR': S + '/tmp'}, timeout=900)
lines = r.stdout.strip().split('\n')
print('replay exit:', r.returncode, 'stdout lines:', len(lines))
print('first line:', lines[0][:110])
print('last line:', lines[-1])
print('REKEY lines on replay:', sum(1 for x in lines if x.startswith('REKEY')))
after = hashlib.sha256(open(ledger, 'rb').read()).hexdigest()
print('ledger sha before:', before[:16], 'after:', after[:16], 'unchanged:', before == after)
PY

say "8. an honest finding vs a zero-findings file for the same heading (lane3)"
git clone --shared --quiet "$LANE" lane3 || exit 2
mkdir -p lane3/.ufo/waves/round-55/w3 lane3/.ufo/evidence/round-21/coldread/rekey-probe
R07=$LANE/.ufo/waves/round-55/w3/T55W3R07.json
if [ -f "$R07" ]; then
  cp "$R07" "${R07%.json}.md" lane3/.ufo/waves/round-55/w3/ 2>/dev/null
  python3 - "$S" <<'PY'
import json, pathlib, sys
S = sys.argv[1]
src = json.load(open(S + '/lane3/.ufo/waves/round-55/w3/T55W3R07.json'))
assert src['findings']
fake = {'heading': src['heading'], 'cand': src['cand'],
        'section_sha256': src['section_sha256'], 'findings': []}
pathlib.Path(S + '/lane3/.ufo/waves/round-55/w3/AAA07.json').write_text(json.dumps(fake, indent=1) + '\n')
pathlib.Path(S + '/lane3/.ufo/waves/round-55/w3/AAA07.md').write_text(
    '# AAA07\n\nNo read. Copied T55W3R07 metadata; findings emptied.\n')
print('honest reader findings:', len(src['findings']), 'fake findings: 0, same sha')
PY
  python3 - "$S/lane3/.ufo/evidence/round-55/integrate/binder.py" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
old = """if RES_PATH.exists():
    for item in json.loads(RES_PATH.read_text('utf-8')):
        RES[item['heading']] = int(item['n'])"""
new = """if RES_PATH.exists():
    for item in json.loads(RES_PATH.read_text('utf-8')):
        if isinstance(item, dict) and 'heading' in item and 'n' in item:
            RES[item['heading']] = int(item['n'])"""
p.write_text(t.replace(old, new))
PY
  mv lane3/.ufo/waves/round-55/w3/AAA07.json "$S/AAA07.json.off"
  mv lane3/.ufo/waves/round-55/w3/AAA07.md "$S/AAA07.md.off"
  { echo "=== RUN A: honest reader only (findings=2)"
    TMPDIR="$S/tmp" python3 -u lane3/.ufo/evidence/round-55/integrate/binder.py "$S/lane3" "$C0" "$PIN" \
      "$S/lane3/.ufo/evidence/round-21/coldread/rekey-probe" 2>&1 | grep -E "Standing rules|REFRESH"
    mv "$S/AAA07.json.off" lane3/.ufo/waves/round-55/w3/AAA07.json
    mv "$S/AAA07.md.off" lane3/.ufo/waves/round-55/w3/AAA07.md
    echo "=== RUN B: honest reader + a zero-findings file for the same heading"
    TMPDIR="$S/tmp" python3 -u lane3/.ufo/evidence/round-55/integrate/binder.py "$S/lane3" "$C0" "$PIN" \
      "$S/lane3/.ufo/evidence/round-21/coldread/rekey-probe" 2>&1 | grep -E "Standing rules|REFRESH"
  } | tee "$S/receipts/selection.out"
else
  echo "T55W3R07.json absent in the lane; selection probe skipped" | tee "$S/receipts/selection.out"
fi

cp "$S/receipts/"*.out "$OUT/"
echo "DONE — receipts in $OUT"
