#!/usr/bin/env python3
"""Recipe step-5 uniqueness gate: literal count(old)==1 per defect, print count
and first matching line, final literal line 'all unique'; also assert new != old."""
import sys

def unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            n = s[i + 1]
            out.append({'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}[n])
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)

def parse(path):
    defects = []
    cur = None
    for no, line in enumerate(open(path, encoding='utf-8').read().split('\n'), 1):
        if line.startswith('@defect '):
            if cur: defects.append(cur)
            cur = {'id': line[len('@defect '):].split('|')[0].strip(), 'line': no}
        elif line.startswith('@old '):
            cur['old'] = unescape(line[len('@old '):])
        elif line.startswith('@new ') or line == '@new':
            cur['new'] = unescape('' if line == '@new' else line[len('@new '):])
    if cur: defects.append(cur)
    return defects

spec, target = sys.argv[1], sys.argv[2]
text = open(target, encoding='utf-8').read()
bad = 0
for d in parse(spec):
    n = text.count(d['old'])
    first = text.split(d['old'], 1)[0].count('\n') + 1 if n else '-'
    print('%s count=%d first-line=%s' % (d['id'], n, first))
    if n != 1 or d['new'] == d['old']:
        bad += 1
print('all unique' if bad == 0 else 'CHECK: FAIL (%d defects)' % bad)
sys.exit(0 if bad == 0 else 1)
