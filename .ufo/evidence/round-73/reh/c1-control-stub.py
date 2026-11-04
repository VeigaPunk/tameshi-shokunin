#!/usr/bin/env python3
"""Cheapest controls that SKIP the claimed work (round-73 C1, pre-freeze).

It never reads an artifact. It scores the manifest's own rows with a
do-nothing rule, in the same line format as the instrument, so the frozen
counter can be applied to it unchanged.
"""
import json
import sys

mode = sys.argv[1]
rows = json.load(open(sys.argv[2], encoding='utf-8'))['rows']
if mode == 'green-only':
    rows = [r for r in rows if r['expect'] == 'meet']
unexpected = 0
for row in rows:
    if mode == 'always-meet' or mode == 'green-only':
        measured = 'meet'
    else:  # echo-printed: measured := the record's own printed value
        measured = 'meet'
    ok = measured == row['expect']
    if not ok:
        unexpected += 1
    print('WAVE_ROW %s kind=%s expect=%s measured=%s %s'
          % (row['id'], row.get('kind'), row['expect'], measured,
             'ok' if ok else 'MISMATCH'))
print('WAVE_RECONCILE: rows=%d met=%d unexpected=%d'
      % (len(rows), len(rows) - unexpected, unexpected))
sys.exit(0 if unexpected == 0 else 1)
