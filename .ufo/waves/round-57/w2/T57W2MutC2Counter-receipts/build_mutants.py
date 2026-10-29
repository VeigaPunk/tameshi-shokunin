#!/usr/bin/env python3
"""Build 12 single-edit mutants of the round-57 C2 counter (measure.py).

Each mutant is a copy of the pristine counter in its own fresh scratch dir, together
with a byte-identical copy of mutants.json (the counter's selftest reads mutants.json
from its own directory and pins its sha256).  The pristine lane file is NEVER touched.
"""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
COUNTER = LANE / '.ufo/evidence/round-57/c2/measure.py'
MUTANTS = LANE / '.ufo/evidence/round-57/c2/mutants.json'
ROOT = Path(sys.argv[1]).resolve()

# ---- the 12 mutants -------------------------------------------------------------------
MUTANTS_SPEC = [
    dict(id='M1', name='rows-arm-admits-selftest-rows',
         arm='rows',
         old="""    return (os.path.basename(argv[0]).startswith('python') and argv[1] == GATE
            and '--selftest' not in argv and '--receipt' in argv)""",
         new="""    return (os.path.basename(argv[0]).startswith('python') and argv[1] == GATE
            and ('--receipt' in argv or '--selftest' in argv))"""),
    dict(id='M2', name='exit-set-check-dropped',
         arm='rows',
         old="    missing = [e for e in WANT_EXITS if e not in exits]",
         new="    missing = []"),
    dict(id='M3', name='refusal-needle-check-dropped',
         arm='rows',
         old="""    unnamed = [r['name'] for r in rows
               if row_exit(r) in (2, 3) and not (row_named_codes(r) & set(codes))]""",
         new="    unnamed = []"),
    dict(id='M4', name='executed-arm-skips-rows',
         arm='executed',
         old="""        for r in rows:
            state, got = run_row(rc_path, lane, r['name'], rev, work, env)""",
         new="""        for r in []:
            state, got = run_row(rc_path, lane, r['name'], rev, work, env)"""),
    dict(id='M5', name='mutant-arm-kills-credit-from-non-admitted-rows',
         arm='mutants',
         old="""                    for r in rows:
                        if r['name'] not in baseline:
                            continue""",
         new="""                    for r in rows:
                        if False:
                            continue"""),
    dict(id='M6', name='mutant-pin-check-removed',
         arm='mutants',
         old="""        raw = show(lane, rev, MUTANTS_PATH)
        if raw is None or sha256(raw) != MUTANTS_SHA256:
            raw = None""",
         new="""        raw = show(lane, rev, MUTANTS_PATH)"""),
    dict(id='M7', name='skill-row-arm-accepts-any-0-token',
         arm='skill',
         old="        if len(have) == 3:",
         new="        if '0' in have:"),
    dict(id='M8', name='codes-arm-vacuous-pass-when-zero-tokens',
         arm='codes',
         old="    short['codes'] = (len(tokens) - len(known)) + (1 if not tokens else 0)",
         new="    short['codes'] = (len(tokens) - len(known))"),
    dict(id='M9', name='cell-arm-compares-with-in-instead-of-equality',
         arm='cell',
         old="    elif carried is not None and set(carried) == emitted:",
         new="    elif carried is not None and emitted.issubset(set(carried)):"),
    dict(id='M10', name='cell-arm-reads-committed-table-instead-of-running-gate',
         arm='cell',
         old="""    emitted, gexit, gverdict = set(), None, 'none'
    if gate_raw is not None:
        emitted, gexit, gverdict = build_cell_fixture(work, bindir / 'receipt-revision-gate.py')""",
         new="""    emitted, gexit, gverdict = set(), None, 'none'
    if gate_raw is not None:
        emitted, gexit, gverdict = set(carried or []), 3, 'REFUSED'"""),
    dict(id='M11', name='base-fixture-builder-drops-the-drifting-path',
         arm='fixture',
         old="    (d / 'fx' / 'drift.paths').write_text('surface/b.txt\\n')",
         new="    (d / 'fx' / 'drift.paths').write_text('surface/a.txt\\n')"),
    dict(id='M12', name='verdict-line-prints-PASS-on-total-gt-0',
         arm='verdict',
         old="               res['standing_cell'], res['total'], 'true' if res['total'] == 0 else 'false'))",
         new="               res['standing_cell'], res['total'], 'true'))"),
]


def main():
    pristine = COUNTER.read_bytes()
    mutants_bytes = MUTANTS.read_bytes()
    out = {'pristine_sha256': hashlib.sha256(pristine).hexdigest(),
           'mutants_json_sha256': hashlib.sha256(mutants_bytes).hexdigest(),
           'built': []}
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True)
    # baseline copy (pristine counter, no edit)
    base = ROOT / 'BASELINE'
    base.mkdir()
    (base / 'measure.py').write_bytes(pristine)
    (base / 'mutants.json').write_bytes(mutants_bytes)
    out['baseline_dir'] = str(base)
    for spec in MUTANTS_SPEC:
        text = pristine.decode('utf-8')
        n = text.count(spec['old'])
        if n != 1:
            print('FATAL %s: old string occurs %d times (must be exactly 1)' % (spec['id'], n))
            return 2
        mutated = text.replace(spec['old'], spec['new']).encode('utf-8')
        d = ROOT / spec['id']
        d.mkdir()
        (d / 'measure.py').write_bytes(mutated)
        (d / 'mutants.json').write_bytes(mutants_bytes)
        out['built'].append(dict(id=spec['id'], name=spec['name'], arm=spec['arm'], dir=str(d),
                                 mutant_sha256=hashlib.sha256(mutated).hexdigest(),
                                 delta_lines=len(spec['new'].splitlines()) - len(spec['old'].splitlines())))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
