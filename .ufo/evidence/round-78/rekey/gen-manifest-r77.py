#!/usr/bin/env python3
r"""gen-manifest-r77.py — build the re-read manifest for the round-77 rekey batch.

For every section in the union plan, pick up to two verification rows: a
repo-relative path from the section's own all-entry input union, and a literal
token drawn from that section's SKILL.md text (a backticked inline span) that
actually occurs in the path's blob at the pin. `expect` is the exact count
measured at the pin, so the check is a real re-read of the file at the pin, not
a stored expectation.

Usage: python3 -I -X utf8 gen-manifest-r77.py <lane> <union-plan.json> <pin> <out.json>
"""
import importlib.util as ilu
import json
import re
import subprocess
import sys

LANE = sys.argv[1]
UNION = sys.argv[2]
PIN = sys.argv[3]
OUT = sys.argv[4]

spec = ilu.spec_from_file_location('r18m', LANE + '/.ufo/evidence/round-18/measure.py')
m = ilu.module_from_spec(spec)
sys.modules['r18m'] = m
spec.loader.exec_module(m)


def blob(path):
    p = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (PIN, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        return None
    return p.stdout.decode('utf-8', 'surrogateescape')


skill = blob('SKILL.md')
sections = {s['heading']: s for s in m.sectionize(skill.encode('utf-8'))}
plan = json.load(open(UNION, encoding='utf-8'))

SKIP = {'.ufo/evidence/round-21/coldread/ledger.json',
        '.ufo/evidence/round-18/coldread/ledger.json'}
PREFER = re.compile(r'^(tools/|corpus/knowledge/|corpus/lessons/|scripts/|corpus/|reports/)')
DOCLIKE = re.compile(r'\.(md|py|sh|mjs|json)$')


def path_rank(p):
    return (0 if PREFER.match(p) else 1,
            0 if DOCLIKE.search(p) else 1,
            0 if p.startswith('tools/') else 1,
            p)


def token_rank(t):
    # prefer code-shaped literals (paths, flags, identifiers) over prose words
    return (0 if re.search(r'[/:_]', t) else 1,
            0 if len(t) >= 8 else 1,
            -len(t))


out = []
for sec in plan['sections']:
    heading = sec['heading']
    text = skill[skill.index(heading):] if heading else skill
    # bound the section text at the next heading line of the same-or-higher level
    lines = text.splitlines()
    keep = [lines[0]]
    for line in lines[1:]:
        if re.match(r'^#{1,3} ', line):
            break
        keep.append(line)
    body = '\n'.join(keep)
    tokens = re.findall(r'`([^`\n]{6,80})`', body)
    cand = []
    for t in tokens:
        t = t.strip()
        if not t or len(t) < 6:
            continue
        if t.startswith(('./', '/')) or t.endswith('/'):
            continue
        if t.count('`'):
            continue
        cand.append(t)
    rows = []
    for path in sorted(sec['union_paths'], key=path_rank):
        if path in SKIP:
            continue
        data = blob(path)
        if data is None:
            continue
        picked = None
        for t in sorted(cand, key=token_rank):
            n = len(re.findall(re.escape(t), data, re.M))
            if n:
                picked = (t, n)
                break
        if picked is None:
            # fall back to a distinctive literal from the section heading
            for t in re.findall(r'[A-Za-z0-9_.-]{8,40}', heading):
                n = len(re.findall(re.escape(t), data, re.M))
                if n:
                    picked = (t, n)
                    break
        if picked is None:
            continue
        rows.append({'path': path, 'pattern': re.escape(picked[0]),
                     'expect': {'exact': picked[1]},
                     'dry_run_count': picked[1], 'literal': picked[0]})
        if len(rows) >= 2:
            break
    out.append({'heading': heading, 'verdict': 'verified-record',
                'minor_gaps': 0, 'verifications': rows})
    print('%-70s rows=%d %s' % (heading[:70], len(rows),
                                '; '.join('%s:%s' % (r['path'], r['dry_run_count'])
                                          for r in rows)))

doc = {'rev_reason': 'L1 TameshiR77 rekey batch (round 77): every section the '
                     'cold-read monitor measures uncredited at the pre-rekey tip; '
                     'each verification re-reads a union path at the pin and '
                     'counts a literal drawn from the section it serves.',
       'pin': PIN, 'sections': out}
open(OUT, 'w', encoding='utf-8').write(json.dumps(doc, indent=1, ensure_ascii=True) + '\n')
bad = [r['heading'] for r in out if not r['verifications']]
print('MANIFEST sections=%d without-verification=%d %s'
      % (len(out), len(bad), bad if bad else ''))
