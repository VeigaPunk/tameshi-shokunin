#!/usr/bin/env python3
"""Bind faithfully (OUT inside the lane, as bind.sh does), commit, then run the
frozen round-56 C1 counter at the bound revision so its arm 4 (readers) can be
read on the tampered sets.

usage: bind_faithful.py TAG
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r56/T56W2SentReaders')
import harness as H  # noqa: E402

TAG = sys.argv[1]
S = H.S
COUNTER = H.LANE / '.ufo/evidence/round-56/c1/measure.py'
res = json.loads((S / 'results.json').read_text('utf-8'))
scen = next(s for s in res['scenarios'] if s['tag'] == TAG)
clone = S / ('clone-' + TAG.split('-')[0])
OUT = clone / '.ufo/evidence/round-21/coldread' / ('rekey-r56-' + H.C0[:12])
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
tmp = S / ('tmp2-' + TAG)
tmp.mkdir(parents=True, exist_ok=True)
env = dict(H.ENV, TMPDIR=str(tmp))
r = subprocess.run([sys.executable, str(H.BINDER), str(clone), H.C0, H.C0, str(OUT),
                    '--headings', str(H.HEADINGS_FILE),
                    '--waves', '.ufo/waves/round-56/w2',
                    '--resolutions', '/nonexistent/round-56-resolutions.json',
                    '--label', 'L1 TameshiR56 re-key (round 56)'],
                   env=env, capture_output=True, text=True)
(S / ('binder-' + TAG + '.stdout')).write_text(r.stdout, encoding='utf-8')
# commit the bind output (the ledger + the re-key directory) exactly like bind.sh step 3b
H.git(clone, 'add', '-A')
H.git(clone, '-c', 'user.name=harness', '-c', 'user.email=harness@example.invalid',
     'commit', '--quiet', '-m', 'round-56 bind output (%s)' % TAG)
bound = H.git(clone, 'rev-parse', 'HEAD').stdout.strip()
work = S / ('cwork2-' + TAG)
if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
c = subprocess.run([sys.executable, str(COUNTER), '--lane', str(clone),
                    '--rev', bound, '--work', str(work), '--explain'],
                   capture_output=True, text=True,
                   env={'PATH': '/usr/bin:/bin', 'HOME': '/home/vgpnk',
                        'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1'})
(S / ('counter-' + TAG + '.stdout')).write_text(c.stdout + c.stderr, encoding='utf-8')
out = {'tag': TAG, 'bound_rev': bound, 'binder_rc': r.returncode,
       'binder_tail': [l for l in r.stdout.splitlines() if l.startswith('REFRESH ')],
       'binder_skips': [l for l in r.stdout.splitlines() if l.startswith('SKIP ')],
       'counter_rc': c.returncode,
       'counter_lines': [l for l in (c.stdout + c.stderr).splitlines()
                         if l.startswith('C1_R56:') or 'arm4' in l]}
(S / ('faithful-' + TAG + '.json')).write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')
print(json.dumps(out, indent=1))
