#!/usr/bin/env python3
"""Probe: does the round-54 C2 'docs' arm read prose, or three substrings?

`TOOLS` is imported from the frozen counter itself; the loop below is copied
verbatim from .ufo/evidence/round-54/c2/measure.py:147-150. Nothing is
re-implemented: `docs` counts exactly what the counter would count.
"""
import copy
import json
import sys

sys.path.insert(0, '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c2')
import measure  # noqa: E402  (import-safe: main() is __main__-guarded)

TOOLS = measure.TOOLS
BASE = json.load(open(sys.argv[1], encoding='utf-8'))
NAME = 'env-diff-selftest'
CELL = [r for r in BASE['rows'] if r['name'] == NAME][0]['scratch_root']

VARIANTS = {
    'A_as-landed': None,
    'B_pointer_short': 'TMPDIR: could-not-evaluate/empty/usable \u2014 corpus/knowledge/scratch-root-contract.md',
    'B2_pointer_arms': ('TMPDIR set-unusable => exit 2 could-not-evaluate; empty => unset; '
                        'usable => all mkdtemp, none under /tmp \u2014 corpus/knowledge/scratch-root-contract.md'),
    'C_one_word': 'contract',
    'C_one_word_plus_top_level_note': 'contract',
    'E_typo_drops_empty_token': CELL.replace('TMPDIR empty', 'TMPDIR empty').replace('; TMPDIR empty', '; TMPDIR empty').replace('empty', 'blank'),
    'F_tokens_only_no_anchor': 'TMPDIR empty could-not-evaluate',
}


def docs_arm(registry):
    """Verbatim measure.py:147-150."""
    docs = 0
    rows = registry.get('rows') if isinstance(registry, dict) else registry
    by_name = {}
    for row in rows if isinstance(rows, list) else []:
        by_name[row.get('name')] = row
    for _name, _path, _arg, row_name in TOOLS:
        cell = (by_name.get(row_name) or {}).get('scratch_root')
        if isinstance(cell, str) and all(k in cell for k in ('TMPDIR', 'empty', 'could-not-evaluate')):
            docs += 1
    return docs


def build(key):
    reg = copy.deepcopy(BASE)
    if key == 'A_as-landed':
        return reg
    for row in reg['rows']:
        if 'scratch_root' in row:
            row['scratch_root'] = VARIANTS[key]
    if key == 'C_one_word_plus_top_level_note':
        reg['notes'] = {'scratch_root': CELL}
    return reg


print('tools=%d  as-landed cell: %d bytes / %d words' % (len(TOOLS), len(CELL), len(CELL.split())))
print()
print('%-32s %-5s %-6s %s' % ('variant', 'docs', 'total+', 'first cell (truncated)'))
for key in VARIANTS:
    reg = build(key)
    d = docs_arm(reg)
    first = [r for r in reg['rows'] if r['name'] == NAME][0].get('scratch_root', '')
    print('%-32s %d/7   +%-5d %r' % (key, d, len(TOOLS) - d, first[:88]))
    json.dump(reg, open('%s/%s.json' % (sys.argv[2], key), 'w'), indent=2)
