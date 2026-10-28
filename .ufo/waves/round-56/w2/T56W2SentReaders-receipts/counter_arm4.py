#!/usr/bin/env python3
"""Run the frozen round-56 C1 counter's arm 4 over the tampered clones: does the
counter itself notice the tampered reader sets?"""
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
C0 = 'c0137451f5b7f22d65f748fc69f1b181f55e1378'
S = Path('/fast/scratch/hyaku/tameshi-r56/T56W2SentReaders')
COUNTER = LANE / '.ufo/evidence/round-56/c1/measure.py'
res = json.loads((S / 'results.json').read_text('utf-8'))
out = {}
for s in res['scenarios']:
    tag = s['tag']
    clone = S / ('clone-' + tag.split('-')[0])
    work = S / ('cwork-' + tag)
    if work.exists():
        import shutil
        shutil.rmtree(work)
    work.mkdir(parents=True)
    r = subprocess.run([sys.executable, str(COUNTER), '--lane', str(clone),
                        '--rev', s['rev'], '--work', str(work), '--explain'],
                       capture_output=True, text=True,
                       env={'PATH': '/usr/bin:/bin', 'HOME': '/home/vgpnk',
                            'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1'})
    lines = [l for l in (r.stdout + r.stderr).splitlines()
             if 'arm4' in l or l.startswith('C1_R56:') or 'reader' in l.lower()]
    out[tag] = {'rc': r.returncode, 'lines': lines}
    print('== %s rc=%d' % (tag, r.returncode))
    for l in lines[:6]:
        print('   %s' % l[:220])
(S / 'counter-arm4.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n',
                                     encoding='utf-8')
print('-> %s' % (S / 'counter-arm4.json'))
