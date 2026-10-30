#!/usr/bin/env python3
"""Probe driver: exact CLI contract invocations, no shell quoting."""
import subprocess, sys, json, os, unicodedata

ROOT = '/fast/scratch/hyaku/tameshi-r59/T59W1S32'
REPO = ROOT + '/probes/mp'
T = 'bb0f386bef139fa3708ccd94b924f1ec804e3514'
SECOND = 'b5f2c442d2cf02749f608d5883d70d1dbd062b0f'  # tools/space name.py changed
FIRST = '0e3a04dc302a169bb1a561b1b9a8a1e3d5880cf7'   # tools/runner.py changed
UNREL = '07594ca478ce55826d1ee1b3eade79d324f33f39'
MISS = 'f25caaf961997b976307239cc9e39cb58021ed27'    # 日本語.py deleted
SYM = 'd7870ee279674e0f836de0581d14d0c6aea0f65f'     # -runner.py -> symlink
GL = 'a6f93f3d3f8e12e89f270c25348e776ccd71b827'      # runner.py -> gitlink (mode 160000)
CAFE = 'b0f423e9a65d092102ebd12ee879186d74388f7c'    # NFC tools/café.py added, declared paths untouched

ALL = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
CAFE_NFC = unicodedata.normalize('NFC', 'tools/café.py')
CAFE_NFD = unicodedata.normalize('NFD', 'tools/café.py')
assert CAFE_NFC != CAFE_NFD

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1', TMPDIR=ROOT)

def run(tool, cand, paths):
    argv = [sys.executable, '-I', f'{ROOT}/probes/{tool}', '--repo', REPO,
            '--trusted', T, '--candidate', cand]
    for p in paths:
        argv += ['--path', p]
    r = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30)
    out = (r.stdout + r.stderr).strip().replace('\n', ' | ')
    return r.returncode, out

PROBES = [
 ('P1 first-only, drift in 2nd path, runner first (expect WRONG 0)', 'strawman_first_only.py', SECOND, ALL),
 ('P2 first-only, same evidence, changed path FIRST (order-dependent verdict)',
  'strawman_first_only.py', SECOND, ['tools/space name.py'] + [p for p in ALL if p != 'tools/space name.py']),
 ('P3 any-equal, drift in 1st path (expect WRONG 0)', 'strawman_any_equal.py', FIRST, ALL),
 ('P4a ref SECOND (expect 1)', 'reference_gate.py', SECOND, ALL),
 ('P4b ref FIRST (expect 1)', 'reference_gate.py', FIRST, ALL),
 ('P4c ref UNREL (expect 0)', 'reference_gate.py', UNREL, ALL),
 ('P4d ref MISS (expect 1)', 'reference_gate.py', MISS, ALL),
 ('P4e ref SYMLINK (expect 1)', 'reference_gate.py', SYM, ALL),
 ('P4f ref GITLINK (expect 1)', 'reference_gate.py', GL, ALL),
 ('P5 ref unresolvable candidate (expect 2)', 'reference_gate.py', '0'*40, ALL),
 ('P6 ref duplicate --path (expect 0)', 'reference_gate.py', T, ['tools/runner.py']*3),
 ('P7 ref spelling variants, drift in canonical (expect 1)', 'reference_gate.py', SECOND,
  ['./tools/runner.py', 'tools//runner.py', 'tools/space name.py']),
 ('P8 ref vacuous path absent both revs (expect 2)', 'reference_gate.py', T, ['tools/ghost.py']),
 ('P10a ref cafe-extra candidate, 4 canonical paths (expect 0)', 'reference_gate.py', CAFE, ALL),
 ('P10b ref NFD spelling of NFC-committed café (expect 2: strict spelling)',
  'reference_gate.py', CAFE, [CAFE_NFD]),
 ('P10c ref NFC café declared but only present at candidate (expect 2: absent at trusted)',
  'reference_gate.py', CAFE, [CAFE_NFC]),
 ('P11a ref SECOND, canonical order (expect 1)', 'reference_gate.py', SECOND, ALL),
 ('P11b ref SECOND, reversed order (expect 1, same verdict)', 'reference_gate.py', SECOND, list(reversed(ALL))),
 ('P11c ref SECOND, rotated order (expect 1, same verdict)', 'reference_gate.py', SECOND, ALL[1:] + ALL[:1]),
]

for label, tool, cand, paths in PROBES:
    code, out = run(tool, cand, paths)
    print(f'### {label}\n  exit={code} :: {out}\n')
