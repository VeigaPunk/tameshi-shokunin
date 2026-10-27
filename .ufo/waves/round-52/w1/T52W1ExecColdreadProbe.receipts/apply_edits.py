#!/usr/bin/env python3
"""Apply the round-52 planned edits (a)-(e) inside a scratch clone at base.

Usage: apply_edits.py <clone> <which...>
Writes files in place; the caller commits.  Prints one line per replacement
with the file and occurrence count so the driver can assert non-zero.
"""
import json
import sys
from pathlib import Path

CLONE = Path(sys.argv[1])
WHICH = set(sys.argv[2:])


def sub(rel, old, new, expect=None, label=''):
    p = CLONE / rel
    raw = p.read_text(encoding='utf-8')
    n = raw.count(old)
    if expect is not None and n != expect:
        sys.exit('ABORT %s: %r occurrences=%d expected=%d' % (rel, old[:60], n, expect))
    if n == 0:
        sys.exit('ABORT %s: %r absent' % (rel, old[:60]))
    p.write_text(raw.replace(old, new), encoding='utf-8')
    print('EDIT %s %s count=%d' % (rel, label or old[:50], n))


if 'a' in WHICH:
    sub('tools/registry.json',
        '"MTE_INTEROP: PASS legs_conforming=9/9"',
        '"MTE_INTEROP: PASS legs_conforming=10/10"', expect=1, label='(a) registry needle')

if 'b' in WHICH:
    # base tools/round21-measure.py:8; one line in, one line out
    sub('tools/round21-measure.py',
        'execution authenticity. Exits: 0 clean, 1 failed, 2 could-not-evaluate,\n',
        'execution authenticity (round 52: fleet-bound selftest). Exits: 0 clean, 1 failed, 2 could-not-evaluate,\n',
        expect=1, label='(b) round21-measure one-line')

if 'c' in WHICH:
    sub('SKILL.md', 'the nine ledger legs', 'the ten ledger legs', expect=1, label='(c1) nine->ten')
    sub('SKILL.md', '`mte-interop-check` (9/9)', '`mte-interop-check` (10/10)', expect=1, label='(c2) 9/9->10/10')
    sub('SKILL.md', '`tools/mutate-and-run.sh:425`', '`tools/mutate-and-run.sh:434`', expect=1, label='(c3) :425->:434')
    sub('SKILL.md', '`tools/mutate-and-run.sh:569-574`', '`tools/mutate-and-run.sh:579-583`', expect=1, label='(c4) :569-574->:579-583')
    # exact-string bullet at SKILL.md:937 (backticked whole path, not the mktemp -d form at :1321)
    sub('SKILL.md', '  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks.',
        '  `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after prerequisite checks.',
        expect=1, label='(c5) TMPDIR bullet :937')
    # the fleet-mutation-runner row of the round-51 registry: both 'under /tmp' cells
    raw = (CLONE / 'SKILL.md').read_text(encoding='utf-8')
    lines = raw.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('| fleet mutation runner |')]
    if len(idx) != 1:
        sys.exit('ABORT: fleet-mutation-runner rows=%d' % len(idx))
    i = idx[0]
    n = lines[i].count('under /tmp')
    if n == 0:
        sys.exit('ABORT: no "under /tmp" in row')
    lines[i] = lines[i].replace('under /tmp', 'under ${TMPDIR:-/tmp}')
    (CLONE / 'SKILL.md').write_text('\n'.join(lines), encoding='utf-8')
    print('EDIT SKILL.md (c6) row=%d under-/tmp count=%d' % (i + 1, n))

if 'd' in WHICH:
    p = CLONE / 'corpus/knowledge/fleet-kill-rate-ledger.md'
    raw = p.read_text(encoding='utf-8')
    if not raw.endswith('\n'):
        raw += '\n'
    raw += ('\nSupersession (round 52): the drift-pins cell of the round-51 block above is superseded — '
            'the runner now allocates `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX`, so a pin that names '
            '`/tmp/...` is read as `${TMPDIR:-/tmp}/...`.\n')
    p.write_text(raw, encoding='utf-8')
    print('EDIT corpus/knowledge/fleet-kill-rate-ledger.md (d) appended 3-line supersession')

if 'e' in WHICH:
    p = CLONE / '.ufo/evidence/round-21/coldread/ledger.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    if 'corrections' in d:
        sys.exit('ABORT: corrections already present')
    d['corrections'] = [{
        'round': 51,
        'entry_sha256': 'synthetic-probe',
        'finding': 'synthetic correction record for precheck tolerance probe',
        'wrong_expectations_before': 1,
        'findings': ['synthetic finding'],
    }]
    p.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
    print('EDIT ledger.json (e) top-level corrections key, keys now=%s' % ','.join(d.keys()))
