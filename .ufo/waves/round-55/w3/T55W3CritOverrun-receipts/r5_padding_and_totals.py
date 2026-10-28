#!/usr/bin/env python3
"""R5: padding check + calibration against the last ten rounds.

(a) attack share per wave under the LOG's taxonomy (reviewer/critic/mutation-tester/labrat);
(b) is any wave-3 attack item a duplicate of a wave-2 attack item (content-word Jaccard);
(c) round seat totals for rounds 45-54 beside round 55.

Usage: python3 r5_padding_and_totals.py LANE
"""
import glob
import json
import os
import re
import sys

LANE = sys.argv[1]
W = LANE + '/.ufo/waves/round-55'
ATTACK = ('reviewer', 'critic', 'mutation-tester', 'labrat')
STOP = set('the a an of to in on at is are be by and or for with that this it as from not no '
           'into its their each every any all one two three only than then so if what which who '
           'do does did can could would should must may might will shall read check run report'.split())


def words(s):
    return {w for w in re.findall(r'[a-z][a-z0-9_-]{3,}', s.lower()) if w not in STOP}


spec = {w: json.load(open('%s/spec-%s.json' % (W, w)))['items'] for w in ('w1', 'w2', 'w3')}
print('attack share per wave (reviewer/critic/mutation-tester/labrat, the LOG taxonomy):')
for w in ('w1', 'w2', 'w3'):
    a = sum(1 for i in spec[w] if i['role'] in ATTACK)
    print('  %s %d/%d = %.1f%%  (policy floor 25%%)' % (w, a, len(spec[w]), 100.0 * a / len(spec[w])))

w2a = [i for i in spec['w2'] if i['role'] in ATTACK or i['role'] in ('sentinel', 'revenger')]
w3a = [i for i in spec['w3'] if i['role'] in ATTACK or i['role'] in ('sentinel', 'revenger')]
print('\nmost similar wave-3 attack to any wave-2 attack (content words, Jaccard):')
pairs = []
for i in w3a:
    wi = words(i['item'])
    best = max(((len(wi & words(j['item'])) / max(1, len(wi | words(j['item']))), j['name']) for j in w2a))
    pairs.append((best[0], i['name'], best[1], i['milestone']))
for s, n, m, ms in sorted(pairs, reverse=True)[:4]:
    print('  %.3f  %s  ~  %s   (%s)' % (s, n, m, ms))
print('  -> highest overlap %.3f; a duplicate would sit far above 0.25' % max(p[0] for p in pairs))

print('\nround seat totals (sum over each round\'s dispatch files):')
for r in range(45, 56):
    tot = 0
    files = sorted(glob.glob('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-%d/*dispatch*.json' % r))
    for f in files:
        try:
            tot += int(json.load(open(f)).get('counts', {}).get('total', 0))
        except Exception:
            pass
    if files:
        print('  r%d: %d seats across %d dispatch file(s)' % (r, tot, len(files)))
