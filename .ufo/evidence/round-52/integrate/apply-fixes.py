#!/usr/bin/env python3
"""Round-52 L1 integration: apply the wave-2 fix-read replacements to SKILL.md (in-line only).

Usage: apply-fixes.py LANE CAND0 [--check] [--skip FixNN:k,...]
For each .ufo/waves/round-52/w2/T52W2FixNN.json: the heading must be one SKILL.md section at CAND0; every
replacement's `old` must occur exactly once inside that section's lines in the working SKILL.md, `new` must contain
no newline and differ from `old`. Replacements are applied in order; the line count of SKILL.md must not change and
every changed line must lie inside the named section. --skip drops named replacements (index k, 0-based) with the
reason recorded by the L1 in the integration notes. Prints one APPLY/REFUSE line per replacement.
"""
import glob, json, os, re, sys

lane, cand0 = sys.argv[1], sys.argv[2]
check = '--check' in sys.argv
skip = set()
if '--skip' in sys.argv:
    skip = set(sys.argv[sys.argv.index('--skip') + 1].split(','))
path = os.path.join(lane, 'SKILL.md')
lines = open(path, encoding='utf-8').read().split('\n')
n0 = len(lines)
HEAD = re.compile(r'^(#{1,3}) ')


def span(heading):
    idx = [i for i, l in enumerate(lines) if l == heading]
    if len(idx) != 1:
        return None
    s = idx[0]; e = s + 1
    while e < len(lines) and not HEAD.match(lines[e]):
        e += 1
    return s, e


applied = refused = 0
for f in sorted(glob.glob(os.path.join(lane, '.ufo/waves/round-52/w2/T52W2Fix[0-9][0-9].json'))):
    tag = os.path.basename(f)[5:10]
    try:
        d = json.load(open(f, encoding='utf-8'))
    except ValueError as exc:
        print('REFUSE %s unreadable %s' % (tag, exc)); refused += 1; continue
    sp = span(d.get('heading'))
    if sp is None:
        print('REFUSE %s heading-not-unique %r' % (tag, d.get('heading'))); refused += 1; continue
    for k, r in enumerate(d.get('replacements') or []):
        key = '%s:%d' % (tag, k)
        if key in skip:
            print('SKIP %s' % key); continue
        old, new = r.get('old'), r.get('new')
        s, e = span(d['heading'])
        hits = [i for i in range(s, e) if isinstance(old, str) and old and old in lines[i]]
        count = sum(lines[i].count(old) for i in hits) if hits else 0
        if not isinstance(new, str) or '\n' in new or new == old or count != 1:
            print('REFUSE %s count=%d %r' % (key, count, (old or '')[:80])); refused += 1; continue
        lines[hits[0]] = lines[hits[0]].replace(old, new, 1)
        applied += 1
        print('APPLY %s line=%d %r -> %r' % (key, hits[0] + 1, old[:70], new[:70]))
assert len(lines) == n0, 'line count changed'
print('FIXES: applied=%d refused=%d' % (applied, refused))
if not check:
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
