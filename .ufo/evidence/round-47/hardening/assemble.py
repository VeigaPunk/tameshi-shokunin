#!/usr/bin/env python3
"""Assemble the round-47 (v2) hardened counter: the round-46 hardened source + seat additions.

  assemble.py --group freshness|coverage --add FILE.py [--add FILE2.py ...] --out OUT.py

Each addition file defines exactly one `extra_<name>()` function (plus helpers whose names start `_x`)
that runs its cases, prints `PASS <case>` / `FAIL <case>` lines (a failing case MUST print a line
that starts `FAIL `, because the pool counts a mutant killed only on a named FAIL line) and returns
(cases, failed). The assembler
 * repoints SELF_PATH at the v2 copy's committed path,
 * inserts every addition before `def main():`,
 * calls every `extra_*` from the selftest, after the round-46 calls, before the tally print.
Nothing else in the round-46 source changes: the pool addresses the rule code by function and ordinal.
"""
import argparse
import os
import re
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GROUPS = {
    'freshness': dict(
        base='.ufo/evidence/round-46/hardening/freshness-counter.py',
        self_old="SELF_PATH = '.ufo/evidence/round-46/hardening/freshness-counter.py'",
        self_new="SELF_PATH = '.ufo/evidence/round-47/hardening/freshness-counter.py'",
        tally_old="    print('C1_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + 4 + extra_cases, failed))\n"),
    'coverage': dict(
        base='.ufo/evidence/round-46/hardening/coverage-counter.py',
        self_old="SELF_PATH = '.ufo/evidence/round-46/hardening/coverage-counter.py'",
        self_new="SELF_PATH = '.ufo/evidence/round-47/hardening/coverage-counter.py'",
        tally_old="    print('C2_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + extra_cases, failed))\n"),
}


def assemble(group, adds, base_dir=None):
    g = GROUPS[group]
    src = open(os.path.join(base_dir or LANE, g['base']), encoding='utf-8').read()
    for needle in (g['self_old'], g['tally_old'], '\ndef main():\n'):
        if src.count(needle) != 1:
            sys.exit('refused: %r occurs %d times in %s' % (needle, src.count(needle), g['base']))
    names, blocks = [], []
    for path in adds:
        text = open(path, encoding='utf-8').read().rstrip() + '\n'
        found = re.findall(r'^def (extra_\w+)\(\)', text, re.M)
        if len(found) != 1:
            sys.exit('refused: %s must define exactly one extra_*() function (found %s)' % (path, found))
        names.append(found[0])
        blocks.append(text)
    src = src.replace(g['self_old'], g['self_new'])
    src = src.replace('\ndef main():\n', '\n' + '\n\n'.join(blocks) + '\n\ndef main():\n')
    calls = ''.join('    _c, _f = %s()\n    extra_cases += _c\n    failed += _f\n' % n for n in names)
    src = src.replace(g['tally_old'], calls + g['tally_old'])
    return src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--group', required=True, choices=sorted(GROUPS))
    ap.add_argument('--add', action='append', default=[])
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    with open(a.out, 'w', encoding='utf-8') as fh:
        fh.write(assemble(a.group, a.add))
    print('wrote %s (%d additions)' % (a.out, len(a.add)))


if __name__ == '__main__':
    main()
