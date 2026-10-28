#!/bin/bash
# Seat T55W3RevBinderInputs — one runnable receipt for the round-55 binder-input choice.
# Read-only against the lane: every git mutation happens in $S (a --shared clone).
# Usage: repro.sh            (scratch defaults to /fast/scratch/hyaku)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
PIN=${PIN:-$C0}
HDR=52075b7d5351
S=${S:-/fast/scratch/hyaku/tameshi-r55/T55W3RevBinderInputs/repro}
unset GIT_DIR GIT_WORK_TREE
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 PYTHONDONTWRITEBYTECODE=1
rm -rf -- "$S"; mkdir -p "$S/out" "$S/bind" "$S/logs"
OUT=$HERE

echo "### 0. clone (--shared) at HEAD so the post-freeze lost-headings file exists in the worktree"
git clone --shared --quiet --no-checkout "$LANE" "$S/clone"
C=$S/clone
top=$(git -C "$C" rev-parse --show-toplevel) || exit 2
[ "$top" = "$C" ] || { echo "TOPLEVEL_MISMATCH: $top"; exit 2; }
git -C "$C" checkout --quiet --detach 4f7a7040a57e7aed17db941be9c27b300aafb783
echo "clone=$C head=$(git -C "$C" rev-parse HEAD)"
echo "radix=$HDR"

echo
echo "### 1. independent derivation of the lost set at C0 (derive.py)"
python3 "$HERE/derive.py" "$C" "$LANE" "$C0" "$BASE" | tee "$S/logs/01-derive.out"

echo
echo "### 2. the committed round-55 resolutions.json cannot feed the binder's RES map"
python3 - "$LANE" <<'PY' | tee "$S/logs/02-resolutions.out"
import json, sys
lane = sys.argv[1]
for name in ('.ufo/evidence/round-54/integrate/resolutions.json',
             '.ufo/evidence/round-55/integrate/resolutions.json'):
    items = json.load(open(lane + '/' + name))
    keys = sorted({k for i in items for k in i})
    print('%-52s items=%2d keys=%s' % (name.split('round-')[1], len(items), keys))
print('round-54 items carry heading+n (the per-heading findings budget); '
      'round-55 items carry neither -> binder.py:54 KeyError: n')
PY
cp "$LANE/.ufo/evidence/round-55/integrate/binder.py" "$S/bind/binder.py"
echo '--- as committed, against the round-55 tree:'
python3 "$S/bind/binder.py" "$C" "$C0" "$PIN" "$S/out" 2>&1 | tail -4 | tee -a "$S/logs/02-resolutions.out"

echo
echo "### 3. scratch-only adaptation (tolerate the round-55 schema) + bind at PIN=$PIN"
sed -i "s/^        RES\[item\['heading'\]\] = int(item\['n'\])$/        if 'heading' in item and 'n' in item:\n            RES[item['heading']] = int(item['n'])/" "$S/bind/binder.py"
grep -n -A2 "^if RES_PATH.exists" "$S/bind/binder.py" | tee -a "$S/logs/02-resolutions.out"
echo '--- synthetic reader reports for the three attacked headings (scratch clone only):'
python3 - "$C" "$LANE" "$C0" <<'PY'
import hashlib, importlib.util, json, sys
clone, lane, c0 = sys.argv[1:4]
import subprocess
spec = importlib.util.spec_from_file_location('r18', lane + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
skill = subprocess.run(['git', '-C', clone, 'show', c0 + ':SKILL.md'], capture_output=True).stdout
secs = {s['heading']: s for s in m.sectionize(skill)}
picks = ['## The leg ledger — replay, receipt, and how it is read (round 7, measured)',
         '### Gate/probe registry',
         '### Round-21 gate/probe registry — finite environment differential']
import os
d = clone + '/.ufo/waves/round-55/w3'; os.makedirs(d, exist_ok=True)
for i, h in enumerate(picks, 1):
    p = '%s/T55W3BinderProbe%02d.json' % (d, i)
    open(p, 'w').write(json.dumps({'heading': h, 'cand': c0,
                                   'section_sha256': secs[h]['sha256'], 'findings': []}, indent=1) + '\n')
    open(p[:-5] + '.md', 'w').write('# synthetic reader (scratch clone only)\n')
print('wrote 3 synthetic readers under', d)
PY
(cd "$S/bind" && python3 "$S/bind/binder.py" "$C" "$C0" "$PIN" "$S/out" > "$S/logs/03-binder.out" 2>&1)
echo "rc=$?"; grep -E '^(REKEY|REFRESH)' "$S/logs/03-binder.out" | tee -a "$S/logs/03-binder.out.only"

echo
echo "### 4. the three input sets as they would be written (entry.inputs, PIN=$PIN)"
python3 - "$C" "$LANE" "$C0" "$OUT" <<'PY' | tee "$S/logs/04-sets.out"
import json, sys
clone, lane, c0, outdir = sys.argv[1:5]
ledger = json.load(open(clone + '/.ufo/evidence/round-21/coldread/ledger.json'))
picks = ['## The leg ledger — replay, receipt, and how it is read (round 7, measured)',
         '### Gate/probe registry',
         '### Round-21 gate/probe registry — finite environment differential']
changed = set(__import__('subprocess').run(
    ['git', '-C', clone, 'diff', '--name-only',
     '0a2010acd1e92e4e332774050825e21bcfc7e079', c0], capture_output=True).stdout.decode().split())
sets = {}
for h in picks:
    es = [e for e in ledger['entries'] if e.get('heading') == h and e.get('read_rev') == c0]
    e = es[-1]
    sets[h] = {'class': e['class'], 'verdict': e['verdict'], 'read_rev': e['read_rev'],
               'commands_executed_count': e['commands_executed_count'],
               'seats': e['seats'], 'traces': e['traces'],
               'inputs': e['inputs']}
    cause = [p for p in e['inputs'] if p in changed]
    print('%-62s inputs=%4d class=%s verdict=%s cmd=%d'
          % (h[:62], len(e['inputs']), e['class'], e['verdict'], e['commands_executed_count']))
    print('    round cause among them: %s' % cause)
    print('    seats: %s' % e['seats'])
json.dump(sets, open(outdir + '/04-three-input-sets.json', 'w'), indent=1)
print('wrote', outdir + '/04-three-input-sets.json')
PY

echo
echo "### 5. pinned vs cited (does the written set match the section's claims?)"
python3 - "$C" "$LANE" "$C0" "$OUT" <<'PY' | tee "$S/logs/05-pinned-vs-cited.out"
import importlib.util, json, subprocess, sys
clone, lane, c0, outdir = sys.argv[1:5]
spec = importlib.util.spec_from_file_location('r18', lane + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
skill = subprocess.run(['git', '-C', clone, 'show', c0 + ':SKILL.md'], capture_output=True).stdout
lines = skill.decode('utf-8', 'surrogateescape').splitlines()
secs = {s['heading']: s for s in m.sectionize(skill)}
sets = {h: set(v['inputs']) for h, v in json.load(open(outdir + '/04-three-input-sets.json')).items()}
probes = {
 '## The leg ledger — replay, receipt, and how it is read (round 7, measured)':
   ['tools/mutate-and-run.sh', 'corpus/knowledge/fleet-kill-rate-ledger.md', 'corpus/README.md', 'corpus/SOURCES.md'],
 '### Gate/probe registry':
   ['tools/repeat-control.py', 'tools/bash-witness-study.py', '.ufo/evidence/round-12/ControlGate/expected.json',
    '.ufo/evidence/round-12/ControlGate/mismatch/expected.json', '.ufo/evidence/round-12/BashWitness/declaration.json',
    '.ufo/evidence/round-12/BashWitness/declared.tsv', '.ufo/evidence/round-12/BashWitness/manifest.json',
    'SHONEN.md', 'corpus/lessons/round-1-verifier-spotcheck.md'],
 '### Round-21 gate/probe registry — finite environment differential':
   ['corpus/QUALITY.md', 'corpus/lessons/round-21.md', 'corpus/knowledge/hermetic-env-differential.md',
    'tools/env-diff.py', 'tools/wave-route-mix.py', 'tools/round21-measure.py', 'tools/wave-accounting.py',
    '.ufo/evidence/round-21/c2-contract.json', '.ufo/evidence/round-21/f5/receipt.json',
    'tools/registry-check.py', 'tools/registry.json', 'corpus/SOURCES.md'],
}
for h, ps in probes.items():
    s = secs[h]
    text = '\n'.join(lines[s['start'] - 1:s['end']])
    print('== %s (lines %d-%d, %d pins written)' % (h, s['start'], s['end'], len(sets[h])))
    for p in ps:
        cite = p.split('/')[-1] in text or p in text or (p == 'corpus/QUALITY.md' and 'QUALITY' in text)
        print('   %-5s %-8s %s' % ('CITED' if cite else '.', 'PINNED' if p in sets[h] else 'MISSING', p))
    cited_n = sum(1 for p in ps if (p.split('/')[-1] in text or p in text) and p in sets[h])
    print('   cited-and-pinned=%d  pinned-total=%d  uncited-pins=%d'
          % (cited_n, len(sets[h]), len(sets[h]) - cited_n))
PY

echo
echo "### 6. what the round plans to edit AFTER the readers read C0 (its own resolutions)"
for cmd in "tools/repeat-control.py --selftest" "tools/bash-witness-study.py selftest" "tools/pin-disposition.py --selftest" \
           "tools/evidence-disposition.py --selftest" "tools/context-capture.py --selftest" \
           "tools/registry-check.py --selftest" "tools/env-diff.py --selftest"; do
  set -- $cmd; tool=$1; shift
  errf=$S/logs/err.$$; env TMPDIR=/nonexistent/x python3 "$C/$tool" "$@" >/dev/null 2>"$errf"; rc=$?
  line=$(head -1 "$errf")
  printf '%-42s rc=%s  %s\n' "$cmd" "$rc" "$line"
done | tee "$S/logs/06-tools.out"
echo '--- F1 (write failure must still be exit 2):' | tee -a "$S/logs/06-tools.out"
env TMPDIR=/nonexistent/x python3 "$C/tools/context-capture.py" --selftest 2>/dev/full; echo "context-capture --selftest 2>/dev/full rc=$?" | tee -a "$S/logs/06-tools.out"
echo '--- F2 (--json must still emit the machine report):' | tee -a "$S/logs/06-tools.out"
env TMPDIR=/nonexistent/x python3 "$C/tools/registry-check.py" --rev HEAD --json > "$S/logs/f2.out" 2>/dev/null
echo "registry-check --rev --json stdout bytes=$(wc -c < "$S/logs/f2.out")" | tee -a "$S/logs/06-tools.out"
echo '--- the seven registry cells vs the tokens the tools actually print (C0):' | tee -a "$S/logs/06-tools.out"
python3 - "$C" <<'PY' | tee -a "$S/logs/06-tools.out"
import json, subprocess, sys
clone = sys.argv[1]
cells = {}
reg = json.loads(subprocess.run(['git', '-C', clone, 'show', '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb:tools/registry.json'],
                                capture_output=True).stdout)['rows']
for row in reg:
    if 'scratch_root' in row:
        cells[row['name']] = row['scratch_root'].split('"')[1].split(':')[0] + ':'
actual = {}
for name, argv in [('repeat-control-selftest', ['tools/repeat-control.py', '--selftest']),
                   ('bash-witness-selftest', ['tools/bash-witness-study.py', 'selftest']),
                   ('pin-disposition-selftest', ['tools/pin-disposition.py', '--selftest']),
                   ('evidence-disposition-selftest', ['tools/evidence-disposition.py', '--selftest']),
                   ('context-capture-selftest', ['tools/context-capture.py', '--selftest']),
                   ('registry-check-selftest', ['tools/registry-check.py', '--selftest']),
                   ('env-diff-selftest', ['tools/env-diff.py', '--selftest'])]:
    r = subprocess.run(['python3', clone + '/' + argv[0]] + argv[1:], capture_output=True,
                       env={'TMPDIR': '/nonexistent/x', 'PATH': '/usr/bin:/bin'})
    actual[name] = r.stderr.decode().split(':')[0] + ':'
for name in sorted(cells):
    print('  %-30s cell=%-24s actual=%-16s %s'
          % (name, cells[name], actual[name], 'OK' if cells[name] == actual[name] else 'FALSE'))
PY

echo
echo "### 7. C1 exposure: re-keyed sections whose written set holds a file the round will edit"
python3 - "$C" "$LANE" "$C0" "$OUT" <<'PY' | tee "$S/logs/07-exposure.out"
import json, sys
clone, lane, c0, outdir = sys.argv[1:5]
ledger = json.load(open(clone + '/.ufo/evidence/round-21/coldread/ledger.json'))
DROP = ('LOG.md', 'SCORECARD.md', 'SKILL.md', '.ufo/evidence/round-21/coldread/ledger.json')
C1 = ['tools/registry.json', 'tools/context-capture.py', 'tools/registry-check.py']
declared = json.load(open(lane + '/.ufo/evidence/round-55/c1/lost-headings-at-c0.json'))
total = exposed = 0
for h in declared:
    u = {}
    for e in ledger['entries']:
        if isinstance(e, dict) and e.get('heading') == h:
            for p in (e.get('inputs') or {}):
                if p not in DROP:
                    u[p] = 1
    total += len(u)
    hit = [p for p in C1 if p in u]
    if hit:
        exposed += 1
        print('  %5d pins  %-58s %s' % (len(u), h[:58], hit))
print('pins written over the 18 headings: %d' % total)
print('EXPOSED=%d/18 sections re-drift if the round lands its own C1 tool/registry edits with PIN=%s'
      % (exposed, c0))
PY

echo
echo "### 7b. counterfactual: what a bigger DROP list would credit WITHOUT a read"
python3 - "$C" "$LANE" "$C0" <<'PY' | tee "$S/logs/07b-drop.out"
import hashlib, importlib.util, json, subprocess, sys
clone, lane, c0 = sys.argv[1:4]
BASE = '0a2010acd1e92e4e332774050825e21bcfc7e079'
spec = importlib.util.spec_from_file_location('r18', lane + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ledger = json.loads(subprocess.run(['git', '-C', clone, 'show', c0 + ':.ufo/evidence/round-21/coldread/ledger.json'],
                                   capture_output=True).stdout)
IGN = frozenset(('SKILL.md', '.ufo/evidence/round-17/coldread/ledger.json',
                 '.ufo/evidence/round-18/coldread/ledger.json', '.ufo/evidence/round-21/coldread/ledger.json'))
paths = sorted({p for e in ledger['entries'] if isinstance(e, dict)
                for p in (e.get('inputs') or {}) if p not in IGN})
out = subprocess.run(['git', '-C', clone, 'cat-file', '--batch'],
                     input=('\n'.join('%s:%s' % (c0, p) for p in paths) + '\n').encode(),
                     capture_output=True).stdout
sha, i = {}, 0
for p in paths:
    nl = out.index(b'\n', i); parts = out[i:nl].decode().split()
    if len(parts) < 3:
        i = nl + 1; continue
    size = int(parts[2]); sha[p] = hashlib.sha256(out[nl + 1:nl + 1 + size]).hexdigest()
    i = nl + 1 + size + 1
changed = set(subprocess.run(['git', '-C', clone, 'diff', '--name-only', BASE, c0],
                             capture_output=True).stdout.decode().split())
by = {}
for e in ledger['entries']:
    if isinstance(e, dict) and isinstance(e.get('sha256'), str):
        by.setdefault(e['sha256'], []).append(e)
declared = set(json.load(open(lane + '/.ufo/evidence/round-55/c1/lost-headings-at-c0.json')))
sections = [s for s in m.sectionize(subprocess.run(['git', '-C', clone, 'show', c0 + ':SKILL.md'],
                                                  capture_output=True).stdout) if s['heading'] in declared]
# per declared-lost section: the drift causes its entries carry from this round's changed files
causes = {}
for sec in sections:
    ms = by.get(sec['sha256'], [])
    drift = {p for e in ms for p, s in (e.get('inputs') or {}).items()
             if p not in IGN and sha.get(p) != s}
    if drift:
        causes[sec['heading']] = drift & changed
for candidate in (('corpus/SOURCES.md',), ('corpus/QUALITY.md',), ('tools/registry.json',),
                  ('tools/context-capture.py', 'tools/registry-check.py'),
                  ('tools/repeat-control.py',), tuple(sorted(changed))):
    freed = [h for h, c in causes.items() if c and set(c) <= set(candidate)]
    print('DROP+%-68s frees %2d of %d declared-lost sections with no read: %s'
          % (','.join(candidate)[:70], len(freed), len(causes),
             ', '.join(sorted(h.split('—')[0].strip()[:24] for h in freed))[:110] or '-'))
PY

echo
echo "### 8. provenance of the binder's heading input"
echo "\$ git -C LANE cat-file -e $C0:.ufo/evidence/round-55/c1/lost-headings-at-c0.json; echo rc=\$?"
git -C "$LANE" cat-file -e "$C0:.ufo/evidence/round-55/c1/lost-headings-at-c0.json" 2>/dev/null; echo "rc=$?"
echo "\$ git -C LANE log --oneline -- .ufo/evidence/round-55/c1/lost-headings-at-c0.json"
git -C "$LANE" log --oneline -- .ufo/evidence/round-55/c1/lost-headings-at-c0.json
echo "\$ jq -r .frozen_paths[] contract.json | grep lost-headings  (contract freeze at 133b2ce)"
python3 -c "
import json;d=json.load(open('$LANE/.ufo/evidence/round-55/contract.json'))
print('frozen_paths:', d['frozen_paths'])
print('lost-headings frozen?', any('lost-headings' in p for p in d['frozen_paths']))"
echo "\$ the binder reads it from the WORKING TREE, not from a rev:"
grep -n "lost-headings-at-c0" "$LANE/.ufo/evidence/round-55/integrate/binder.py"
echo "\$ docstring says w1, code reads w2+w3:"
grep -n "w1/\*.json\|WAVE_DIRS" "$LANE/.ufo/evidence/round-55/integrate/binder.py"
echo "\$ stale round label in the written seats field:"
grep -n "re-key (round 54)" "$LANE/.ufo/evidence/round-55/integrate/binder.py"

echo
echo "### done: receipts under $OUT ; scratch kept at $S"
