#!/usr/bin/env python3
"""Spec-only cheat forecasts for the R72-C1 control (seat T72W1S07).

Knowledge base is the plan's frozen per-arm table ONLY (per-path single-edit
losses); no ledger reading, no union rule. Three cheats:

  constant13  any non-empty planned set -> 13
  constant0   any non-empty planned set -> 0
  sumarms     sum of per-path single-arm losses (union ignored)
"""
import sys

# Frozen per-path single-edit losses, plans/round-72.plan.md table.
PER_PATH = {
    'corpus/SOURCES.md': 13,
    'PROVINCE.md': 6,
    'corpus/QUALITY.md': 6,
    'SCORECARD.md': 0,
    'tools/pointer-recheck.json': 0,
}
ARMS = [
    ('sources-only', ['corpus/SOURCES.md'], 13),
    ('province-only', ['PROVINCE.md'], 6),
    ('quality-only', ['corpus/QUALITY.md'], 6),
    ('scorecard-only', ['SCORECARD.md'], 0),
    ('pointer-recheck-json-only', ['tools/pointer-recheck.json'], 0),
    ('province+sources', ['PROVINCE.md', 'corpus/SOURCES.md'], 17),
    ('no-planned-path', [], 'error exit 2'),
]


def constant13(paths):
    return 13 if paths else None


def constant0(paths):
    return 0 if paths else None


def sumarms(paths):
    if not paths:
        return 0  # a sum over an empty set: no union rule, no error
    return sum(PER_PATH.get(p, 0) for p in paths)


def main():
    modes = (('constant13', constant13), ('constant0', constant0),
             ('sumarms', sumarms))
    for name, fn in modes:
        for arm_name, paths, want in ARMS:
            got = fn(paths)
            if want == 'error exit 2':
                verdict = 'FAIL (printed value instead of error)' \
                    if got is not None else 'PASS error'
                print('CHEAT %-10s | %-24s -> %s | want=%s | %s'
                      % (name, arm_name, got, want, verdict))
            else:
                verdict = 'FAIL' if got != want else 'PASS'
                print('CHEAT %-10s | %-24s -> at_risk=%s | want=%d | %s'
                      % (name, arm_name, got, want, verdict))


main()
