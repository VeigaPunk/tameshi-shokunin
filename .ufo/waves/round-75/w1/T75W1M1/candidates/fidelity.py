#!/usr/bin/env python3
"""Fidelity check: run the unmutated stub's sweep on the real SCORECARD at
21ef81e9 with a 17-row manifest. Runner = extraction into a repo-shaped
mirror (<work>/tools/<name> plus the one __file__-relative frozen dependency)
so that rekey-cost.py's selftest resolves its frozen path.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
STUB = os.path.join(S, 'selfstate-freshness.py')
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '21ef81e9'
DEP = '.ufo/evidence/round-18/measure.py'


def blob(rev, path):
    return subprocess.run(['git', '-C', LANE, 'cat-file', 'blob',
                           '%s:%s' % (rev, path)],
                          capture_output=True, check=True).stdout


def mirror_runner(rev, path, argv):
    work = tempfile.mkdtemp(prefix='ssf-mirror-',
                            dir=os.environ.get('TMPDIR') or None)
    try:
        target = os.path.join(work, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'wb') as fh:
            fh.write(blob(rev, path))
        try:
            dep = blob(rev, DEP)
        except subprocess.CalledProcessError:
            dep = None
        if dep is not None:
            dpath = os.path.join(work, DEP)
            os.makedirs(os.path.dirname(dpath), exist_ok=True)
            with open(dpath, 'wb') as fh:
                fh.write(dep)
        run = subprocess.run([sys.executable, '-I', '-X', 'utf8', target]
                             + list(argv), cwd=LANE,
                             capture_output=True)
        return (run.stdout + run.stderr).decode('utf-8', 'replace')
    finally:
        shutil.rmtree(work, ignore_errors=True)


def row(rid, cap, figure, argv, expect='match'):
    return {'id': rid, 'mode': 'capability', 'capability': cap,
            'figure': figure, 'expect': expect,
            'instrument': {'path': 'tools/' + argv[0], 'rev': REV,
                           'argv': argv[1:]}}


ROWS = [
    row('r-receipt-exists', 'receipt-existence sweep',
        r'RECEIPT_EXISTS_SELFTEST: \d+/\d+ pass',
        ['receipt-exists.py', '--selftest']),
    row('r-commit-bind', 'commit-message receipt binding sweep',
        r'RECEIPT_COMMIT_BIND_SELFTEST: \d+/\d+ pass',
        ['receipt-commit-bind.py', '--selftest']),
    row('r-quoted-line', 'quoted-line receipt backability',
        r'QUOTED_LINE_EXISTS_SELFTEST: \d+/\d+ pass',
        ['quoted-line-exists.py', '--selftest']),
    row('r-arm-live-selftest', 'counter-arm liveness check',
        r'ARM_LIVENESS_SELFTEST: \d+/\d+ pass',
        ['arm-liveness.py', '--selftest']),
    row('r-arm-live-sweep', 'counter-arm liveness check',
        r'rows=\d+ live=\d+ dead=\d+',
        ['arm-liveness.py', '--repo', '.', '--manifest',
         'tools/arm-liveness.json']),
    row('r-fig-attr-selftest', 'figure-attribution check',
        r'FIGURE_ATTRIBUTION_SELFTEST: \d+/\d+ pass',
        ['figure-attribution.py', '--selftest']),
    row('r-fig-attr-sweep', 'figure-attribution check',
        r'FIGURE_ATTRIBUTION: rows=\d+ met=\d+ unexpected=\d+',
        ['figure-attribution.py', '--repo', '.', '--manifest',
         'tools/figure-attribution.json']),
    row('r-anchor-selftest', 'anchor-drift sweep',
        r'ANCHOR_DRIFT_SELFTEST: \d+/\d+ pass',
        ['anchor-drift-sweep.py', '--selftest']),
    row('r-anchor-sweep', 'anchor-drift sweep',
        r'ANCHOR_DRIFT: rows=\d+ met=\d+ unexpected=\d+',
        ['anchor-drift-sweep.py', '--repo', '.', '--manifest',
         'tools/anchor-drift-sweep.json']),
    row('r-count-selftest', 'printed-count recheck',
        r'COUNT_RECHECK_SELFTEST: \d+/\d+ pass',
        ['count-recheck.py', '--selftest']),
    row('r-count-sweep', 'printed-count recheck',
        r'COUNT_RECHECK: rows=\d+ met=\d+ unexpected=\d+',
        ['count-recheck.py', '--repo', '.', '--manifest',
         'tools/count-recheck.json']),
    row('r-pointer-selftest', 'line-pointer recheck',
        r'POINTER_RECHECK_SELFTEST: \d+/\d+ pass',
        ['pointer-recheck.py', '--selftest']),
    row('r-pointer-sweep', 'line-pointer recheck',
        r'POINTER_RECHECK: rows=\d+ met=\d+ unexpected=\d+',
        ['pointer-recheck.py', '--repo', '.', '--manifest',
         'tools/pointer-recheck.json']),
    row('r-rekey-selftest', 'rekey-cost forecast',
        r'REKEY_COST_SELFTEST: \d+/\d+ pass',
        ['rekey-cost.py', '--selftest']),
    row('r-addr-sweep', 'round-range additivity sweep',
        r'ADDRANGE: rows=\d+ met=\d+ unexpected=\d+',
        ['additivity-range.py', '--repo', '.', '--manifest',
         'tools/additivity-range.json']),
    row('r-add-selftest', 'round-range additivity sweep',
        r'ADDITIVITY_RANGE_SELFTEST: \d+/\d+ pass',
        ['additivity-range.py', '--selftest']),
    {'id': 'r74-frozen-addr-six', 'mode': 'span',
     'span': 'ADDRANGE: rows=6 met=6 unexpected=0',
     'figure': r'ADDRANGE: rows=\d+ met=\d+ unexpected=\d+',
     'expect': 'stale',
     'instrument': {'path': 'tools/additivity-range.py', 'rev': REV,
                    'argv': ['--repo', '.', '--manifest',
                             'tools/additivity-range.json']}},
]

spec = importlib.util.spec_from_file_location('ssf', STUB)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

with open(os.path.join(S, 'manifest17.json'), 'w', encoding='utf-8') as fh:
    json.dump({'schema': 'tameshi-selfstate-freshness-v1', 'rows': ROWS}, fh,
              indent=1)

doc = m.load_doc(LANE, REV, 'SCORECARD.md', m.GitReader(LANE))
rows, match, stale, unexpected = m.sweep(
    {'rows': ROWS}, doc, m.GitReader(LANE), mirror_runner)
for r in rows:
    print('SELFSTATE_ROW %s expect=%s measured=%s %s'
          % (r['id'], r['expect'], r['state'],
             'ok' if r['ok'] else 'UNEXPECTED'))
    print('SELFSTATE_TOKEN %s doc=%s instrument=%s'
          % (r['id'], r['doc_token'], r['instrument_token']))
print('SELFSTATE: rows=%d match=%d stale=%d unexpected=%d'
      % (len(rows), match, stale, unexpected))
sys.exit(0 if unexpected == 0 else 1)
