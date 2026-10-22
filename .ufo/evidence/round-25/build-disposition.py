#!/usr/bin/env python3
"""Build dead-falsifier-disposition.json from the round-25 re-attack seat reports.

  python3 .ufo/evidence/round-25/build-disposition.py --outcomes OUTCOMES.json

OUTCOMES.json maps seat name (e.g. ReReplay01) to {"status": "completed"|"failed",
"error": "<last error text>"} as delivered by the task callbacks (completion
authority: the callback, never the presence of a report file). A completed seat's
report must end with `R23-REATTACK <name>: AGREE|FINDING`; a completed seat without
that line is recorded as died-equivalent with the reason, never guessed.
"""
import argparse
import json
from pathlib import Path
import re

LANE = Path(__file__).resolve().parents[3]
W = '.ufo/waves/round-25/w1'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outcomes', required=True, type=Path)
    outcomes = json.loads(parser.parse_args().outcomes.read_text())
    r23 = json.loads((LANE / '.ufo/waves/round-23/original-outcomes2.json').read_text())
    dead = sorted(r['name'] for r in r23['rows'] if r['status'] != 'completed')
    rows = []
    for name in dead:
        seat = 'Re' + name
        rel = '%s/%s.md' % (W, seat)
        outcome = outcomes.get(seat, {'status': 'missing', 'error': 'no callback recorded'})
        row = {'name': name, 'seat': 'TameshiR25.' + seat, 'callback_status': outcome['status']}
        path = LANE / rel
        verdicts = (re.findall(r'^R23-REATTACK %s: (AGREE|FINDING)\b' % re.escape(name),
                               path.read_text(errors='replace'), re.M) if path.is_file() else [])
        if outcome['status'] == 'completed' and len(verdicts) == 1:
            row.update(status='reattacked-agree' if verdicts[0] == 'AGREE' else 'reattacked-finding', report=rel)
        else:
            row.update(status='reattack-seat-died',
                       error=outcome.get('error') or ('completed callback but report verdict lines %r' % verdicts))
        rows.append(row)
    out = {'schema': 'tameshi-r25-dead-falsifier-disposition-v1',
           'population': '.ufo/waves/round-23/original-outcomes2.json rows with status != completed',
           'dead_round23_seats': len(dead), 'rows': rows}
    (LANE / '.ufo/evidence/round-25/dead-falsifier-disposition.json').write_text(json.dumps(out, indent=1) + '\n')
    counts = {}
    for r in rows:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    main()
