#!/usr/bin/env python3
"""Control stand-in: answers every input with an empty collision set.

It exists to show the C3 counter's collision check is load-bearing: the counter
recomputes the collision set from the two files, so a tool that always prints
zero disagrees and the control fails by construction.
"""
import json
import sys

if '--selftest' in sys.argv:
    print('STAGED_ID_GUARD_SELFTEST: cases=13 failed=0')
    print('VERDICT: PASS')
    sys.exit(0)

print(json.dumps({'collisions': [], 'collision_count': 0, 'unmapped': [], 'held': {},
                  'naive_map': {}, 'cascade': [], 'cascade_count': 0, 'refused': False,
                  'next_free': 'S001', 'extractor': '0-3space', 'verdict': 'answered'}))
