#!/usr/bin/env python3
"""Add amendment-2 (A8 tie / A9 provenance) selftest cases to the round-57 C1 counter.

The amendment-2 arms of the counter are exercised by no case in the shipped selftest: nine of the
eleven mutants of the amendment-2 code survive it. This module adds the missing cases, so the
arms have a fixture that moves the tally off zero and an independent control that passes.

It rewrites the selftest's `run()` helper to accept the fixture knobs the new cases need
(panel_opt / panel_detail) and inserts the new cases. It never touches the counter's code region.

Usage: addcases.py <in-measure.py> <out-measure.py> [<diff-out>]
"""
import difflib
import sys

OLD_SIG = """        def run(new, old=None, pin=True, floor=1, cap=1, mutate=None, trf=1, base=None, spots=(SPOT_PATH,),
                defs=None, panel=None, ppin=None, allowed=PANEL_ALLOWED, dflt=False):
"""

NEW_SIG = """        def run(new, old=None, pin=True, floor=1, cap=1, mutate=None, trf=1, base=None, spots=(SPOT_PATH,),
                defs=None, panel=None, ppin=None, allowed=PANEL_ALLOWED, dflt=False,
                panel_opt=None, panel_detail=None):
"""

OLD_PANEL = """                seat = 'T57W2SeatA'
                ids = ('R50.1', 'R50.2', 'R50.3')
                seatblob = json.dumps({'seat': seat,
                                       'verdicts': {i: {'verdict': panel.get(i)} for i in ids}})
                write('.ufo/waves/round-57/w2/%s.json' % seat, seatblob)
                write('.ufo/waves/round-57/w2-results.json',
                      json.dumps({'results': [{'name': seat}]}))
                pblob = json.dumps({'verdicts': panel,
                                    'detail': {i: {'seat': seat, 'commit': ''} for i in ids},
                                    'files': {seat: hashlib.sha256(seatblob.encode()).hexdigest()}})
"""

NEW_PANEL = """                opt = panel_opt or {}
                seat = opt.get('seat', 'T57W2SeatA')
                wave = opt.get('wave', 'w2')
                ids = ('R50.1', 'R50.2', 'R50.3')
                seatverdicts = {i: {'verdict': opt.get('seat_verdicts', {}).get(i, panel.get(i))}
                                for i in ids}
                seatblob = json.dumps({'seat': seat, 'verdicts': seatverdicts})
                write('.ufo/waves/round-57/%s/%s.json' % (wave, seat), seatblob)
                listed = [seat] if opt.get('listed', True) else []
                write('.ufo/waves/round-57/%s-results.json' % wave,
                      json.dumps({'results': [{'name': n} for n in listed]}))
                det = {i: {'seat': seat, 'commit': (panel_detail or {}).get(i, '')} for i in ids}
                files = {seat: hashlib.sha256(seatblob.encode()).hexdigest()}
                if opt.get('sha') is False:
                    files[seat] = 'f' * 64
                pblob = json.dumps({'verdicts': panel, 'detail': det, 'files': files})
"""

ANCHOR = "        # HARD paths\n        hards = ("

NEW_CASES = '''        # (5c) amendment-2 arms (T57W3MutC1A2): the blind-panel commit tie (A8) and the panel
        # provenance (A9). Each case moves its tally off zero; each has an independent control.
        # A8: the panel's commit for a `fixed` id ties the row when it is a prefix of the row's
        # commit, even when the commit message names no id and the item text names no path.
        tied = variant(lambda r: refix(r[0], q_forge, 'tools/z.py', '1-1', EX, status_at_base='fixed'))
        counts, stat, total, kv, _ = run(tied, base=q_forge, panel={'R50.1': 'fixed'},
                                         panel_detail={'R50.1': q_forge[:7]}, trf=0)
        case('A8 tie: a panel commit prefix admits the row',
             total == 0 and stat['fixed'] == 1 and kv['C1_R57_PASS'] == 'true')
        counts, _, total, kv, _ = run(tied, base=q_forge, panel={'R50.1': 'fixed'},
                                       panel_detail={'R50.1': 'deadbeef'}, trf=0)
        case('A8 tie control: a panel commit that is not a prefix refuses the row',
             counts['fixed_bad'] == 1 and total == 1)
        counts, _, total, kv, _ = run(tied, base=q_forge, panel={'R50.1': 'fixed'},
                                       panel_detail={'R50.1': q_forge[:3]}, trf=0)
        case('A8 tie: a panel commit shorter than 7 hex chars does not tie the row',
             counts['fixed_bad'] == 1 and total == 1)
        counts, _, total, kv, _ = run(tied, base=q_forge, panel={'R50.1': 'open'},
                                       panel_detail={'R50.1': q_forge[:7]}, trf=0)
        case('A8 tie: a non-fixed panel verdict does not tie the row',
             counts['fixed_bad'] == 1 and total == 1)
        # A9: the provenance of the panel's seat.
        counts, _, total, kv, _ = run(good, panel=GOOD_PANEL, panel_opt={'sha': False})
        case('A9 provenance: a seat file whose sha does not match the panel pin counts a shortfall',
             counts['panel_prov'] == 3 and total == 3)
        counts, _, total, kv, _ = run(good, panel=GOOD_PANEL,
                                       panel_opt={'seat_verdicts': {'R50.1': 'declined'}})
        case('A9 provenance: a seat verdict that differs from the panel verdict counts a shortfall',
             counts['panel_prov'] == 1 and total == 1)
        counts, _, total, kv, _ = run(good, panel=GOOD_PANEL, panel_opt={'listed': False})
        case('A9 provenance: a seat that the wave results do not list counts a shortfall',
             counts['panel_prov'] == 3 and total == 3)
        counts, _, total, kv, _ = run(good, panel=GOOD_PANEL,
                                       panel_opt={'seat': 'T57W3SeatA', 'wave': 'w3'})
        case('A9 provenance: a w3 seat is looked up in w3', counts['panel_prov'] == 0 and total == 0)
        counts, _, total, kv, _ = run(good, panel=GOOD_PANEL, panel_opt={'sha': False})
        case('A9 provenance: a shortfall makes the verdict line fail',
             kv['total'] == '3' and kv['C1_R57_PASS'] == 'false')
        counts, _, total, kv, _ = run(good, panel=GOOD_PANEL,
                                       panel_opt={'seat_verdicts': {'R50.3': 'open'}})
        case('A9 provenance: a declined id is counted too', counts['panel_prov'] == 1 and total == 1)
        counts, _, total, kv, res = run(good, panel=GOOD_PANEL)
        case('A9: the terms line carries panel_prov', 'panel_prov=' in terms_line(res))
'''

FIXTURE_COMMIT = """        write('tools/q.py', EX + '  # pre-base fix\\n')
        prebase = commit('pre-base extractor fix')
"""


def add_cases(text):
    n = text.count(OLD_SIG)
    if n != 1:
        raise SystemExit('run() signature anchor count=%d' % n)
    n = text.count(OLD_PANEL)
    if n != 1:
        raise SystemExit('panel fixture anchor count=%d' % n)
    n = text.count(ANCHOR)
    if n != 1:
        raise SystemExit('case insertion anchor count=%d' % n)
    out = text.replace(OLD_SIG, NEW_SIG, 1).replace(OLD_PANEL, NEW_PANEL, 1)
    out = out.replace(ANCHOR, NEW_CASES + ANCHOR, 1)
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    text = open(src, 'r', encoding='utf-8').read()
    out = add_cases(text)
    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write(out)
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w', encoding='utf-8') as fh:
            fh.write(''.join(difflib.unified_diff(text.splitlines(True), out.splitlines(True),
                                                  fromfile=src, tofile=dst)))
    print('added amendment-2 cases: %s -> %s' % (src, dst))
    return 0


if __name__ == '__main__':
    sys.exit(main())
