#!/usr/bin/env python3
"""Variant B: SEAT_FILES carries the wave/ prefix (matching the listing key and
the `dir` the seat_reports rows name), gains the nested report, and the arm
reads dir 'wave'. No second listing key."""
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
src = open(SRC, encoding='utf-8').read()

old = 'SELFTEST_ARMS = 12\n'
assert src.count(old) == 1
src = src.replace(old, 'SELFTEST_ARMS = 13\n')

old = ("SEAT_FILES = ['%s/T1W1S%02d.md' % ('x', i) for i in range(12)] + ['x/swarm-registry.json']\n")
new = ("SEAT_FILES = (['%s/T1W1S%02d.md' % ('wave', i) for i in range(12)]\n"
       "              + ['wave/swarm-registry.json', 'wave/nested/deep.md'])\n")
assert src.count(old) == 1
src = src.replace(old, new)

anchor = """        arm('arm12-declaration-absent-refused', 'setup',
            lambda: measure_row(kind='roles', declaration={
                'form': 'text-tokens', 'path': 'plan.md', 'rev': REV,
                'span': '12 seats - 3 executor, 2 scribe',
                'roles': {'executor': 3, 'scribe': 2, 'wizard': 7}}))
"""
arm15 = """        # arm15: `seat_reports` counts the *.md files at the TOP of the wave
        # dir only. 12 top-level reports, a nested report (wave/nested/deep.md)
        # and a non-md registry sit in the same fixture dir.
        arm('arm15-seatreports-top-level-only', 'meet',
            lambda: measure_row(kind='seat_reports',
                                record={'path': 'report.md', 'rev': REV,
                                        'span': '12 seats', 'printed': 12},
                                wave={'dir': 'wave', 'results': 'results.json',
                                      'rev': REV}))
"""
assert src.count(anchor) == 1
src = src.replace(anchor, anchor + arm15)
open(OUT, 'w', encoding='utf-8').write(src)
print('wrote', OUT)
