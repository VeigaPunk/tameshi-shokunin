#!/usr/bin/env python3
"""Verify the round-72 plan role declaration span binds byte-exactly (read-only)."""
import re
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = 'a3dd35742eee608d1205843dacebc461b4242b9e'
SPAN = ('- Wave `w1`: 12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,\n'
        '  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.')
ROLES = [('executor', 3), ('scribe', 2), ('scout', 1), ('connector', 1),
         ('reviewer', 1), ('critic', 1), ('mutation-tester', 1),
         ('sentinel', 1), ('labrat', 1)]

raw = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob',
                      '%s:plans/round-72.plan.md' % REV],
                     stdout=subprocess.PIPE).stdout
span = SPAN.encode('utf-8')
print('span is byte substring:', span in raw, '| plan bytes', len(raw))
i = raw.find(span)
print('at bytes[%d:%d]' % (i, i + len(span)))
for role, n in ROLES:
    m = re.search((r'(?<![0-9])%d\s+%s\b' % (n, re.escape(role))).encode(), span)
    print(' ', role, n, 'token-present' if m else 'ABSENT')
