#!/usr/bin/env python3
"""Round-75 C2 landing-tip reachability control (seat T75W1E2).

Reads SCORECARD at 21ef81e9, applies the seven live-cell supersessions the
round-75 plan names (row-scoped, never global), and re-measures with the
candidate's own evaluate path and the real pinned instrument runner. Two
controls:

  per-repair   each repair alone must flip EXACTLY its named row from stale to
               match and leave every other row (including the frozen span row)
               unchanged;
  all-repairs  the combined doc must read rows=17 match=16 stale=1
               unexpected=0 exit 0.

This is a scratch simulation of the landing tip; the landing-tip run itself is
the L1's post-landing measurement.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    'tools', 'selfstate-freshness.py')
REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '21ef81e99966198cf8cdb2c6d8e56aa3c482da56'
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'tools', 'selfstate-freshness.json')

spec = importlib.util.spec_from_file_location('ssf', SPEC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base_text = mod.GitReader(REPO).blob(REV, 'SCORECARD.md').decode('utf-8')
with open(MANIFEST, encoding='utf-8') as fh:
    rows = json.load(fh)['rows']
caps = mod.parse_capabilities(base_text)

REPAIRS = [
    ('commit-bind-selftest', 'commit-message receipt binding sweep',
     'RECEIPT_COMMIT_BIND_SELFTEST: 4/4 pass',
     'RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass'),
    ('quoted-line-selftest', 'quoted-line receipt backability',
     'QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass',
     'QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass'),
    ('arm-liveness-selftest', 'counter-arm liveness check',
     'ARM_LIVENESS_SELFTEST: 4/4 pass',
     'ARM_LIVENESS_SELFTEST: 5/5 pass'),
    ('arm-liveness-rows', 'counter-arm liveness check',
     'rows=3 live=3 dead=0', 'rows=9 live=9 dead=0'),
    ('anchor-drift-rows', 'anchor-drift sweep',
     'ANCHOR_DRIFT: rows=4 met=4 unexpected=0',
     'ANCHOR_DRIFT: rows=16 met=16 unexpected=0'),
    ('pointer-rows', 'line-pointer recheck',
     'POINTER_RECHECK: rows=8 met=8 unexpected=0',
     'POINTER_RECHECK: rows=12 met=12 unexpected=0'),
    ('additivity-rows', 'round-range additivity sweep',
     'ADDRANGE: rows=6 met=6 unexpected=0',
     'ADDRANGE: rows=11 met=11 unexpected=0'),
]


def apply(targets):
    text = base_text
    for rid, cap, old, new in targets:
        line = mod.parse_capabilities(text)[cap]
        if old not in line:
            raise SystemExit('repair %s: %r absent from its row' % (rid, old))
        if line.count(old) != 1:
            raise SystemExit('repair %s: %r occurs %d times in its row'
                             % (rid, old, line.count(old)))
        text = text.replace(line, line.replace(old, new), 1)
    return text


def measure(text, runner):
    results = mod.evaluate([dict(r) for r in rows], text.encode('utf-8'),
                           text, runner)
    return {r['id']: r for r in results}


workdir = tempfile.mkdtemp(prefix='selfstate-sim-',
                           dir=os.environ.get('TMPDIR') or None)
failures = 0
try:
    runner = mod.GitInstrumentRunner(REPO, workdir)
    base = measure(base_text, runner)
    print('BASE: measured match=%d stale=%d'
          % (sum(1 for r in base.values() if r['measured'] == 'match'),
             sum(1 for r in base.values() if r['measured'] == 'stale')))
    for repair in REPAIRS:
        after = measure(apply([repair]), runner)
        changed = [rid for rid in base if base[rid]['measured'] != after[rid]['measured']]
        target = repair[0]
        ok = (changed == [target]
              and after[target]['measured'] == 'match'
              and after['r74-frozen-addr-six']['measured'] == 'stale')
        print('SIM_ROW_REPAIR %-24s flips=%-24s target_measured=%-5s '
              'frozen=%s %s'
              % (target, ','.join(changed) or '-', after[target]['measured'],
                 after['r74-frozen-addr-six']['measured'],
                 'ok' if ok else 'UNEXPECTED'))
        if not ok:
            failures += 1
    landing = measure(apply(REPAIRS), runner)
    print('--- combined landing-tip simulation ---')
    rc = mod.emit([landing[r['id']] for r in rows], sys.stdout)
    print('SIM exit=%d' % rc)
    if rc != 0:
        failures += 1
finally:
    shutil.rmtree(workdir, ignore_errors=True)

print('SIM_CONTROL: %s' % ('GREEN' if failures == 0 else 'RED'))
sys.exit(0 if failures == 0 else 1)
