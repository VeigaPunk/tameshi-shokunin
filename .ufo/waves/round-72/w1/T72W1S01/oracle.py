#!/usr/bin/env python3
"""Independent oracle for the round-72 rekey-cost forecast rule.

Rule restated from plans/round-72.plan.md (and the tool docstring's prose,
not its implementation): a SKILL.md section is at risk for a planned edit
set P when its NEWEST ledger entry, in append order, records a planned path
inside that entry's ``inputs``; the entry's own key for SKILL.md and the two
cold-read ledger paths are self-references and are ignored.

This file shares no code with tools/rekey-cost.py or with
.ufo/evidence/round-18/measure.py.  Section headings are derived here, by
this file's own parser: every SKILL.md line beginning '## ' or '### ', in
file order, plus the leading preamble section (heading '').

Usage:
  python3 -I oracle.py --repo <lane> --edit corpus/SOURCES.md [--edit ...]
  python3 -I oracle.py --repo <lane> --edit PROVINCE.md --detail
"""

import argparse
import json
import os
import sys

LEDGER = os.path.join('.ufo', 'evidence', 'round-21', 'coldread', 'ledger.json')
SKILL = 'SKILL.md'
IGNORED = frozenset((
    'SKILL.md',
    '.ufo/evidence/round-17/coldread/ledger.json',
    '.ufo/evidence/round-21/coldread/ledger.json',
))
PREAMBLE = ''


def sections(skill_path):
    """Headings in file order: '## '/'### ' lines plus the preamble."""
    out = [PREAMBLE]
    with open(skill_path, encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('## ') or line.startswith('### '):
                out.append(line)
    return out


def newest_inputs(entries):
    """heading -> inputs of its last entry in append order."""
    newest = {}
    for entry in entries:
        newest[entry.get('heading', PREAMBLE)] = entry.get('inputs') or {}
    return newest


def main(argv=None):
    ap = argparse.ArgumentParser(description='independent rekey-cost oracle')
    ap.add_argument('--repo', default='.')
    ap.add_argument('--ledger', default=LEDGER)
    ap.add_argument('--skill', default=SKILL)
    ap.add_argument('--edit', action='append', default=[])
    ap.add_argument('--detail', action='store_true')
    args = ap.parse_args(argv)

    repo = args.repo
    ledger_path = args.ledger if os.path.isabs(args.ledger) else os.path.join(repo, args.ledger)
    skill_path = args.skill if os.path.isabs(args.skill) else os.path.join(repo, args.skill)

    planned = [p for p in args.edit if p not in IGNORED]
    if not planned:
        print('ORACLE error=no-planned-path', file=sys.stderr)
        return 2

    with open(ledger_path, encoding='utf-8') as fh:
        entries = json.load(fh)['entries']
    newest = newest_inputs(entries)
    wanted = set(planned)
    heads = sections(skill_path)
    at_risk = [h for h in heads
               if h in newest and (set(newest[h]) - IGNORED) & wanted]

    print('ORACLE at_risk=%d sections=%d' % (len(at_risk), len(heads)))
    if args.detail:
        for head in at_risk:
            print('RISK %s' % (head or '<preamble>'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
