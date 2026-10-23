#!/usr/bin/env python3
"""Round 29 (copied from round 28, provenance text only changed): append wave-1 independent cold-read entries to the current cold-read ledger.

Usage: append-entries.py --assembled FILE --ledger .ufo/evidence/round-21/coldread/ledger.json --receipt OUT.json

FILE is the ledger that .ufo/evidence/round-18/coldread/assemble.py wrote from the wave-1
seat reports alone (no --carry). Its entries are appended after the existing entries; the
existing entries and every other top-level key stay byte-for-byte equal as data. Trace paths
under the lane root are rewritten lane-relative so the committed receipts resolve at the
revision. Each appended entry gets `provenance` naming the seat(s) and the recipe, and
`historical_failure_indexes_preserved: []`. Writes the ledger and a preservation receipt.
"""
import argparse
import hashlib
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
PROVENANCE = ('independent seat cold read, round 29 wave 1 ({seats}), read at content revision 9f3084bc60ad56aac01e4556ef4c7653df2f65e5; recipe SKILL.md "Recipe for one bucket, cold"; '
              'fresh non-author seats dispatched by the L1, not blind to the round')


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode('utf-8')).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--assembled', required=True)
    ap.add_argument('--ledger', required=True)
    ap.add_argument('--receipt', required=True)
    a = ap.parse_args()
    ledger_path = Path(a.ledger)
    raw = ledger_path.read_bytes()
    ledger = json.loads(raw)
    prior = ledger['entries']
    prior_digest = digest(prior)
    others = {k: v for k, v in ledger.items() if k != 'entries'}
    new = json.loads(Path(a.assembled).read_text())['entries']
    out = []
    for e in new:
        e = dict(e)
        e['traces'] = [t[len(LANE) + 1:] if t.startswith(LANE + '/') else t for t in e.get('traces', [])]
        e['provenance'] = PROVENANCE.format(seats=', '.join(e.get('seats', [])))
        e['historical_failure_indexes_preserved'] = []
        out.append(e)
    ledger['entries'] = prior + out
    ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')
    after = json.loads(ledger_path.read_text())
    receipt = {
        'prior_entries': len(prior), 'appended': len(out), 'current_entries': len(after['entries']),
        'prefix_entries_equal_as_data': after['entries'][:len(prior)] == prior,
        'prefix_entries_sha256': prior_digest,
        'other_top_level_keys_unchanged': {k: v for k, v in after.items() if k != 'entries'} == others,
        'prior_ledger_file_sha256': hashlib.sha256(raw).hexdigest(),
        'digest_canonicalization': 'UTF-8 json.dumps(entries, sort_keys=True), default separators/ensure_ascii',
        'appended_headings': [e['heading'] for e in out],
        'appended_verdicts': [e['verdict'] for e in out],
    }
    Path(a.receipt).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('prior_entries', 'appended', 'current_entries',
                                              'prefix_entries_equal_as_data', 'other_top_level_keys_unchanged')}))
    return 0 if receipt['prefix_entries_equal_as_data'] and receipt['other_top_level_keys_unchanged'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
