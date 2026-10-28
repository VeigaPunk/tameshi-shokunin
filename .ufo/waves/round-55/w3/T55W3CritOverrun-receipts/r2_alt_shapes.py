#!/usr/bin/env python3
"""R2: cost the three alternatives to the dispatched shape, off the specs themselves.

Usage: python3 r2_alt_shapes.py LANE
"""
import json
import sys

LANE = sys.argv[1]
W = LANE + '/.ufo/waves/round-55'
spec = {w: json.load(open('%s/spec-%s.json' % (W, w))) for w in ('w1', 'w2', 'w3')}
n = {w: len(spec[w]['items']) for w in spec}
lost = json.load(open(LANE + '/.ufo/evidence/round-55/c1/lost-headings-at-c0.json'))
readers = [i for i in spec['w3']['items'] if i['role'] == 'scribe']
attacks = [i for i in spec['w3']['items'] if i['role'] != 'scribe']

print('dispatched: w1=%d (band 64-128) w2=%d w3=%d (band 32-64 each) total=%d'
      % (n['w1'], n['w2'], n['w3'], sum(n.values())))
print('w3 composition: %d re-key readers + %d attack seats = %d (the v1 wave floor)'
      % (len(readers), len(attacks), n['w3']))
print('lost headings that force a reader: %d; w3 reader count: %d -> %s'
      % (len(lost), len(readers), 'one reader per lost section' if len(lost) == len(readers) else 'MISMATCH'))

print('\n[A] RED floor, no re-key (disclose the miss):')
print('    cost measured at C0 by r3: credited 46/64, score 6; the round pre-registered')
print('    NOHARM coldread-floor at credited>=64 and score>=8 -> RED on both terms, and')
print('    deciding-run.sh:70-71 gates on coldread-precheck -> the deciding run cannot exit 0.')

print('\n[B] smaller wave:')
print('    a reader-only wave is %d seats; the v1 wave floor is 32 (ufo-swarm-wave.mjs:16-18:'
      % len(readers))
print('    "a wave with spawn lanes carries waveMinLanes..waveMaxLanes").')
print('    %d < 32 -> refused, so 32 is the minimum legal standalone reader wave;' % len(readers))
print('    the extra %d attack seats are what the floor costs, not padding.' % len(attacks))

print('\n[C] two waves, readers folded into wave 2 (the strongest counterexample):')
cap2 = 64
folded = n['w2'] + len(readers)
print('    wave 2 capacity %d; %d + %d readers = %d (fits)' % (cap2, n['w2'], len(readers), folded))
with_attacks = folded + len(attacks)
print('    plus w3\'s %d attacks = %d -> over the %d ceiling by %d'
      % (len(attacks), with_attacks, cap2, with_attacks - cap2))
trim = with_attacks - cap2
print('    to shape-conform: wave 2 = %d, drop %d attack seat(s), total = %d seats, 2 waves'
      % (cap2, trim, n['w1'] + cap2))
print('    preconditions checked: C0 lands before wave-2 dispatch (r4 timestamps);')
print('    the w3 attack items read C0/frozen bytes, not wave-2 reports, except')
print('    T55W3RevW2 which audits wave-2 deliverables.')
print('\nDELTA vs dispatched: +1 wave; dispatched carries %d more attack seats than [C].' % trim)
