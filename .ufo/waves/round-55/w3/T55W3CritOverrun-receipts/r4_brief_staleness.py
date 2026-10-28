#!/usr/bin/env python3
"""R4: was the third wave assembled, or copied? Timestamps, the brief it shipped,
and where its readers actually wrote.

Usage: python3 r4_brief_staleness.py LANE
"""
import json
import os
import subprocess
import sys
from collections import Counter

LANE = sys.argv[1]
W = LANE + '/.ufo/waves/round-55'
C0 = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'


def git(*a):
    return subprocess.run(['git', '-C', LANE] + list(a), capture_output=True, text=True).stdout.strip()


print('timeline:')
print('  C0 commit      ', git('log', '-1', '--format=%ci', C0))
for f in ('w1.ready', 'w2-dispatch.json', 'w2.ready', 'w3-dispatch.json', 'w3.ready'):
    t = subprocess.run(['stat', '-c', '%y', '%s/%s' % (W, f)], capture_output=True, text=True).stdout.strip()
    print('  %-16s' % f, t)
print('  -> C0 precedes wave-2 dispatch: readers were dispatchable inside wave 2.')

b = json.loads(git('show', '133b2ce6d4d86d783db38607343c3654350194b8:.ufo/evidence/round-55/freeze.json'))
print('\nfreeze.json at the revision w3\'s brief names (133b2ce): %d amendments' % len(b['amendments']))
ctx3 = json.load(open(W + '/spec-w3.json'))['context']
ctx2 = json.load(open(W + '/spec-w2.json'))['context']
import re
m = re.search(r'\((\d+) amendments, all pre-control', ctx3)
print('w3 brief says: %s amendments (stale by %d at the revision it names)'
      % (m.group(1), len(b['amendments']) - int(m.group(1))))
print('w3 brief reader-discipline line:', [l for l in ctx3.splitlines() if 'only the three reader seats' in l])
print('w3 brief heading the discipline names:', [l[:60] for l in ctx3.splitlines() if l.startswith('Read `##')])
print('w3 brief reader JSON path occurrences of /w2/:', ctx3.count('round-55/w2/'),
      ' of /w3/:', ctx3.count('round-55/w3/'))
print('w3 items that are readers:', len([i for i in json.load(open(W + '/spec-w3.json'))['items'] if i['role'] == 'scribe']))

place = Counter()
for w in ('w1', 'w2', 'w3'):
    for f in os.listdir('%s/%s' % (W, w)) if os.path.isdir('%s/%s' % (W, w)) else []:
        if f.startswith('T55W3R') and f.endswith('.json'):
            place[w] += 1
print('\nwave-3 reader JSONs found, by directory:', dict(place))
print('  (the brief told every reader to write into w2/)')
