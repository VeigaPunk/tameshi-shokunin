#!/usr/bin/env python3
"""Assemble a hardened round-45 counter: the round-45 source + seat additions, deterministically.

  assemble.py --group freshness|coverage --add FILE.py [--add FILE2.py ...] --out OUT.py

Each addition file defines exactly one `extra_<name>()` function (plus helpers whose names start `_x`) that
runs its cases, prints `PASS <case>` / `FAIL <case>` lines and returns (cases, failed). The assembler
 * repoints SELF_PATH at the hardened copy's committed path,
 * inserts every addition before `def main():`,
 * extends the selftest tally with every `extra_*` call, printing the same label as the round-45 selftest.
Nothing else in the round-45 source changes (the declared mutants in mutants.json target those lines).
"""
import argparse
import os
import re
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GROUPS = {
    'freshness': dict(
        orig='.ufo/evidence/round-45/freshness/measure.py',
        self_old="SELF_PATH = '.ufo/evidence/round-45/freshness/measure.py'",
        self_new="SELF_PATH = '.ufo/evidence/round-46/hardening/freshness-counter.py'",
        tally_old="    print('C1_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + 4, failed))\n",
        tally_new_head="    extra_cases = 0\n",
        tally_print="    print('C1_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + 4 + extra_cases, failed))\n"),
    'coverage': dict(
        orig='.ufo/evidence/round-45/coverage/measure.py',
        self_old="SELF_PATH = '.ufo/evidence/round-45/coverage/measure.py'",
        self_new="SELF_PATH = '.ufo/evidence/round-46/hardening/coverage-counter.py'",
        tally_old="    print('C2_R45_SELFTEST: cases=%d failed=%d' % (len(cases), failed))\n",
        tally_new_head="    extra_cases = 0\n",
        tally_print="    print('C2_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + extra_cases, failed))\n"),
}


def assemble(group, adds):
    g = GROUPS[group]
    src = open(os.path.join(LANE, g['orig']), encoding='utf-8').read()
    for needle in (g['self_old'], g['tally_old'], '\ndef main():\n'):
        if src.count(needle) != 1:
            sys.exit('refused: %r occurs %d times in %s' % (needle, src.count(needle), g['orig']))
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
    calls = g['tally_new_head'] + ''.join(
        '    _c, _f = %s()\n    extra_cases += _c\n    failed += _f\n' % n for n in names)
    src = src.replace(g['tally_old'], calls + g['tally_print'])
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
