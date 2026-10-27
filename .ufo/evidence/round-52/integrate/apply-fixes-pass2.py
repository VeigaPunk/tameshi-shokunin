#!/usr/bin/env python3
"""Pass 2: wave-2 replacements refused by pass 1 because their `old` lies in a child subsection of the seat's
section. Applied only when `old` occurs exactly once in the whole SKILL.md, `new` has no newline, and the line
count is unchanged. Usage: apply-fixes-pass2.py LANE"""
import json, os, sys
lane = sys.argv[1]; p = os.path.join(lane, 'SKILL.md'); s = open(p, encoding='utf-8').read(); n = s.count('\n')
for line in open(os.path.join(lane, '.ufo/evidence/round-52/integrate/apply-fixes.stdout')):
    if not line.startswith('REFUSE Fix') or ':' not in line.split()[1]:
        continue
    tag, k = line.split()[1].split(':')
    r = json.load(open(os.path.join(lane, '.ufo/waves/round-52/w2/T52W2%s.json' % tag)))['replacements'][int(k)]
    old, new = r['old'], r['new']
    c = s.count(old)
    if c == 1 and '\n' not in new and new != old:
        s = s.replace(old, new, 1); print('APPLY2 %s:%s %r -> %r' % (tag, k, old[:60], new[:60]))
    else:
        print('LEAVE2 %s:%s count=%d %r' % (tag, k, c, old[:60]))
assert s.count('\n') == n
open(p, 'w', encoding='utf-8').write(s)
