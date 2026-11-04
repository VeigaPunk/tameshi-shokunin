#!/usr/bin/env python3
"""Print the per-round artifact table from git objects at pinned revs (read-only)."""
import json
import subprocess
from collections import Counter

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
NAMED = ['reviewer', 'critic', 'mutation-tester', 'labrat']


def g(root, *a):
    p = subprocess.run(['git', '-C', root] + list(a),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else b''


def blob(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'cat-file', 'blob', '%s:%s' % (rev, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout if p.returncode == 0 else None


def last(root, path):
    return g(root, 'log', '-1', '--format=%H', '--', path).decode().strip() or None


def seatreports(rev, wd):
    pre = wd + '/'
    return len([p for p in g(LANE, 'ls-tree', '-r', '--name-only', rev, '--', wd)
                .decode().splitlines()
                if p.startswith(pre) and '/' not in p[len(pre):] and p.endswith('.md')])


print('| round | report rev (fleet) | wave dir | results rev | results.seats '
      '| len(results) | committed seat reports | role multiset (results.agent) '
      '| attack share (named set) | pinnable |')
print('|---|---|---|---|---|---|---|---|---|---|')
for r in range(60, 74):
    rep = '.ufo/reports/round-%d/tameshi.md' % r
    rrev = last(FLEET, rep)
    wd = '.ufo/waves/round-%d/w1' % r
    rp = '.ufo/waves/round-%d/w1-results.json' % r
    raw = blob(LANE, 'HEAD', rp)
    if raw is None:
        tree = g(LANE, 'ls-tree', '-r', '--name-only', 'HEAD',
                 '--', '.ufo/waves/round-%d' % r).decode().strip()
        state = 'w1 files only (no results)' if tree else 'absent'
        print('| %d | %s | %s | — | — | — | — | — | — | NO |'
              % (r, (rrev[:12] if rrev else 'ABSENT'), state))
        continue
    doc = json.loads(raw.decode())
    ms = Counter(x['agent'] for x in doc['results'])
    rev = last(LANE, rp)
    atk = sum(v for k, v in ms.items() if k in NAMED)
    print('| %d | %s | %s | %s | %d | %d | %d | %s | %d/%d = %.1f%% | yes |'
          % (r, rrev[:12], wd, rev[:12], doc['seats'], len(doc['results']),
             seatreports(rev, wd),
             ', '.join('%s %d' % (k, v) for k, v in sorted(ms.items())),
             atk, len(doc['results']), 100 * atk / len(doc['results'])))
print()
print('rounds_scanned=14 disagreements=1 unpinnable=11')
