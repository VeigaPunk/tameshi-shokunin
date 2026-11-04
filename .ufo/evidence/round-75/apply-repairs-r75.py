#!/usr/bin/env python3
"""Apply the round-75 SCORECARD capability-cell repairs, row-scoped.

Every replacement is bound to its capability row (exact first cell in the
`## Capabilities` section) and asserted to occur exactly once inside THAT row.
A file-wide replace would corrupt the historical round blocks, which quote the
same old tokens 3-5 times (T75W1R2 §3); the row scope is the whole guard.
Exit 0 when every repair applied; 2 on a precondition miss (no partial write).
"""
import sys

REPAIRS = [
 ('commit-message receipt binding sweep',
  'tools/receipt-commit-bind.py --selftest` \u2192 `RECEIPT_COMMIT_BIND_SELFTEST: 4/4 pass`',
  'tools/receipt-commit-bind.py --selftest` \u2192 `RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass`'),
 ('quoted-line receipt backability',
  'tools/quoted-line-exists.py --selftest` \u2192 `QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass`',
  'tools/quoted-line-exists.py --selftest` \u2192 `QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass`'),
 ('counter-arm liveness check',
  'tools/arm-liveness.py --selftest` \u2192 `ARM_LIVENESS_SELFTEST: 4/4 pass`',
  'tools/arm-liveness.py --selftest` \u2192 `ARM_LIVENESS_SELFTEST: 5/5 pass`'),
 ('counter-arm liveness check',
  'the standing manifest \u2192 `rows=3 live=3 dead=0`',
  'the standing manifest \u2192 `rows=9 live=9 dead=0`'),
 ('anchor-drift sweep',
  'the standing manifest \u2192 `ANCHOR_DRIFT: rows=4 met=4 unexpected=0`',
  'the standing manifest \u2192 `ANCHOR_DRIFT: rows=16 met=16 unexpected=0`'),
 ('line-pointer recheck',
  'the standing manifest -> `POINTER_RECHECK: rows=8 met=8 unexpected=0`',
  'the standing manifest -> `POINTER_RECHECK: rows=12 met=12 unexpected=0`'),
 ('round-range additivity sweep',
  '--manifest tools/additivity-range.json` \u2192 `ADDRANGE: rows=6 met=6 unexpected=0`',
  '--manifest tools/additivity-range.json` \u2192 `ADDRANGE: rows=11 met=11 unexpected=0`'),
 # out-of-population extras (T75W1E3 sweep, T75W1R2 §4): repaired the same way,
 # measured outside the frozen 17-row R75-C2 population and reported as such.
 ('mutation sweep runner',
  '`MUTATE_SELFTEST: 80/80 pass`',
  '`MUTATE_SELFTEST: 107/107 pass`'),
 ('wave-record reconciliation',
  '`WAVE_RECONCILE_SELFTEST: 12/12 pass`',
  '`WAVE_RECONCILE_SELFTEST: 18/18 pass`'),
]


def main(argv):
    check = '--check' in argv
    paths = [a for a in argv[1:] if not a.startswith('--')]
    if len(paths) != 1:
        print('usage: apply-repairs-r75.py [--check] <SCORECARD.md>', file=sys.stderr)
        return 2
    path = paths[0]
    lines = open(path, encoding='utf-8', newline='').read().split('\n')
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith('## Capabilities'):
            start = i
        elif start is not None and line.startswith('## '):
            end = i
            break
    if start is None or end is None:
        print('apply: capabilities-section-absent', file=sys.stderr)
        return 2
    index = {}
    for i in range(start, end):
        line = lines[i]
        if line.startswith('|') and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if cells and cells[0] != 'Capability':
                index[cells[0]] = i
    pending = []
    for cap, old, new in REPAIRS:
        if cap not in index:
            print('apply: capability-row-absent:%s' % cap, file=sys.stderr)
            return 2
        i = index[cap]
        n = lines[i].count(old)
        if n != 1:
            print('apply: old-not-unique-in-row:%s:%d' % (cap, n), file=sys.stderr)
            return 2
        pending.append((i, old, new, cap))
    for i, old, new, cap in pending:
        lines[i] = lines[i].replace(old, new, 1)
        print('repair %-38s line=%d %s' % (cap[:38], i + 1,
                                           'checked' if check else 'applied'))
    if not check:
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(lines))
    print('APPLY_REPAIRS: rows=%d %s' % (len(pending),
                                         'checked' if check else 'applied'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
