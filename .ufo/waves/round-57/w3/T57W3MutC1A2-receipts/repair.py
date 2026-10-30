#!/usr/bin/env python3
"""Repair the round-57 C1 counter's selftest so the amendment-2 provenance arm has a fixture.

Why: on the pristine amendment-2 bytes the shipped selftest is RED (92/99). Cause: the selftest's
panel fixture writes only {'verdicts': panel} to PANEL_PATH, so panel_provenance() finds no
`detail` for any id, `seat` is None, the seat file is absent, and the shortfall is counted for
every id: counts['panel_prov'] == 3 on every panel case. The seven failing cases are exactly the
panel-arm cases. Without this repair no mutant can be adjudicated (a red baseline makes every
mutant inconclusive).

The repair touches ONLY the selftest harness (the `run()` helper and the cli pin), never the
counter's code region: the mutants are single edits of the amendment-2 code, and the repair is
applied identically to the pristine bytes and to every mutant.

Usage: repair.py <in-measure.py> <out-measure.py>
"""
import sys

OLD_RUN = """            pp = None
            if panel is not None:
                pblob = json.dumps({'verdicts': panel})
                write(PANEL_PATH, pblob)
                pp = hashlib.sha256(pblob.encode()).hexdigest()
"""

NEW_RUN = """            pp = None
            if panel is not None:
                # amendment-2 repair: the panel fixture carries `detail` (a seat per id), the seat's
                # own wave file, and the wave results list, so the provenance arm has a passing case.
                seat = 'T57W2SeatA'
                ids = ('R50.1', 'R50.2', 'R50.3')
                seatblob = json.dumps({'seat': seat,
                                       'verdicts': {i: {'verdict': panel.get(i)} for i in ids}})
                write('.ufo/waves/round-57/w2/%s.json' % seat, seatblob)
                write('.ufo/waves/round-57/w2-results.json',
                      json.dumps({'results': [{'name': seat}]}))
                pblob = json.dumps({'verdicts': panel,
                                    'detail': {i: {'seat': seat, 'commit': ''} for i in ids},
                                    'files': {seat: hashlib.sha256(seatblob.encode()).hexdigest()}})
                write(PANEL_PATH, pblob)
                pp = hashlib.sha256(pblob.encode()).hexdigest()
"""

OLD_CLI = """        psha = hashlib.sha256(json.dumps({'verdicts': GOOD_PANEL}).encode()).hexdigest()
"""

NEW_CLI = """        with open(os.path.join(repo, PANEL_PATH), 'rb') as fh:
            psha = hashlib.sha256(fh.read()).hexdigest()
"""


def repair(text):
    n1 = text.count(OLD_RUN)
    n2 = text.count(OLD_CLI)
    if n1 != 1 or n2 != 1:
        raise SystemExit('repair anchors not unique: run=%d cli=%d' % (n1, n2))
    out = text.replace(OLD_RUN, NEW_RUN, 1).replace(OLD_CLI, NEW_CLI, 1)
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    text = open(src, 'r', encoding='utf-8').read()
    out = repair(text)
    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write(out)
    print('repaired %s -> %s' % (src, dst))
    return 0


if __name__ == '__main__':
    sys.exit(main())
