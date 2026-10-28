#!/usr/bin/env python3
"""A6b re-run: snapshot the laundered fixture pair INTO the receipts before the binder runs."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r55/T55W3MutReader')
import run as R
import run2 as R2

REC = R.REC
H1, H2 = R.H1, R.H2


def main():
    R.setup()
    secs, _ = R.section_shas()
    R.write_res([{'heading': H2, 'n': 2}])
    R.build_fixtures(secs, {H2: 'empty'})
    R2.keep_md_findings()
    snap = REC / 'A6b-fixtures'
    shutil.rmtree(snap, ignore_errors=True)
    snap.mkdir(parents=True)
    for f in sorted(R.W.glob('T55W3FIX*.json')):
        d = json.loads(f.read_text('utf-8'))
        if d['heading'] != H2:
            continue
        shutil.copy2(f, snap / f.name)
        shutil.copy2(str(f)[:-5] + '.md', snap / (f.stem + '.md'))
    print('snapshot:', sorted(p.name for p in snap.iterdir()))
    print((snap / [p.name for p in snap.glob('*.json')][0]).read_text('utf-8'))
    R2.capture('A6c-emptied-snapshot', (H1, H2))
    R.git('checkout', '--', R.LEDGER)


if __name__ == '__main__':
    main()
