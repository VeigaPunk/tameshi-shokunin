#!/usr/bin/env python3
"""Build an AMENDED copy of the C2 counter carrying the six proposed selftest cases
(one per surviving mutant), as precise string edits on the pristine bytes."""
import hashlib
import json
import sys
from pathlib import Path

PRISTINE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c2/measure.py')


def edit(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        raise SystemExit('FATAL %s: old occurs %d times' % (tag, n))
    return text.replace(old, new)


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    t = PRISTINE.read_text()

    # --- imports the proposed cases need ---------------------------------------------
    t = edit(t, "import argparse\nimport ast\n",
             "import argparse\nimport ast\nimport contextlib\nimport io\n", 'imp')

    # --- A: fx_registry gains a needle_override knob (P1: M3) -------------------------
    t = edit(t,
             "def fx_registry(rev_a, drop=(), expect_override=None, selftest_argv=False):",
             "def fx_registry(rev_a, drop=(), expect_override=None, selftest_argv=False,\n"
             "                needle_override=None):",
             'A1')
    t = edit(t,
             """        if expect_override and name in expect_override:
            ex = expect_override[name]""",
             """        if expect_override and name in expect_override:
            ex = expect_override[name]
        if needle_override and name in needle_override:
            needle = needle_override[name]""",
             'A2')

    # --- B: build_lane gains skill_text and mutants_text knobs (P3: M6, P4: M8) -------
    t = edit(t,
             """def build_lane(parent, name, gate_bytes, rc_bytes, registry_fn=fx_registry, skill_kwargs=None,
               registry_kwargs=None):""",
             """def build_lane(parent, name, gate_bytes, rc_bytes, registry_fn=fx_registry, skill_kwargs=None,
               registry_kwargs=None, skill_text=None, mutants_text=None):""",
             'B1')
    t = edit(t,
             """    kw = dict(cell='RECEIPT_REV_CONTENT_DRIFT', extra='', row=FX_ROW)
    kw.update(skill_kwargs or {})
    (d / 'SKILL.md').write_text(FX_SKILL.format(**kw))""",
             """    kw = dict(cell='RECEIPT_REV_CONTENT_DRIFT', extra='', row=FX_ROW)
    kw.update(skill_kwargs or {})
    (d / 'SKILL.md').write_text(skill_text if skill_text is not None else FX_SKILL.format(**kw))
    if mutants_text is not None:
        (d / '.ufo' / 'evidence' / 'round-57' / 'c2').mkdir(parents=True)
        (d / '.ufo' / 'evidence' / 'round-57' / 'c2' / 'mutants.json').write_text(mutants_text)""",
             'B2')

    # --- C: a standing-rules template with no RECEIPT_* token (P4: M8) -----------------
    t = edit(t,
             "FX_ROW = ('| receipt revision gate | gate |",
             "FX_SKILL_NOCODES = \"\"\"# fixture\n\n## Standing rules\n\n"
             "- A receipt is evidence only for the revision it names. No code is named here.\n\n"
             "## Source notes\n\n### Gate/probe registry\n\n"
             "| Name | Kind | Entry command | Verdict map | Self-test command |\n"
             "|---|---|---|---|---|\n{row}\n## Later\n\ntext\n\"\"\"\n\n"
             "FX_ROW = ('| receipt revision gate | gate |",
             'C1')

    # --- D: helpers the proposed cases need ------------------------------------------
    t = edit(t,
             """def selftest(a):""",
             """def tampered_mutants():
    \"\"\"A byte-valid mutants.json whose sha256 differs from the pin (same mutants).\"\"\"
    data = json.loads((Path(__file__).resolve().parent / 'mutants.json').read_text('utf-8'))
    data['mutants'][0]['effect'] = data['mutants'][0]['effect'] + ' (tampered)'
    return json.dumps(data, indent=1) + '\\n'


def pin_case(lane_dir, head, work):
    \"\"\"Run the counter's own measurement entry point (main_measure) on a lane whose
    committed mutants.json fails the sha256 pin; it must refuse to grade the mutants.
    Returns (ok, detail).\"\"\"
    buf = io.StringIO()
    ns = argparse.Namespace(lane=lane_dir, rev=head, work=str(work), explain=True)
    with contextlib.redirect_stdout(buf):
        rc = main_measure(ns)
    out = buf.getvalue()
    ok = (rc != 0 and 'mutants.json unavailable or pin mismatch' in out
          and 'mutants=0/3' in out)
    lines = [ln for ln in out.strip().splitlines() if ln.strip()]
    return ok, (lines[-1][:160] if lines else 'no output')


def selftest(a):""",
             'D2')

    # --- E: run() records the lane it built ------------------------------------------
    t = edit(t,
             """    def run(name, **kw):
        parent = scratch / name
        parent.mkdir()
        gate = kw.pop('gate', gate_raw)
        lane_dir, head = build_lane(parent, 'lane', gate, rc_raw, **kw)
        return measure(lane_dir, head, scratch / (name + '-work'), mutants_raw, False)""",
             """    built = {}

    def run(name, **kw):
        parent = scratch / name
        parent.mkdir()
        gate = kw.pop('gate', gate_raw)
        lane_dir, head = build_lane(parent, 'lane', gate, rc_raw, **kw)
        built[name] = (lane_dir, head)
        return measure(lane_dir, head, scratch / (name + '-work'), mutants_raw, False)""",
             'E1')

    # --- F: the six proposed selftest cases ------------------------------------------
    old_tail = """        r = run('nogate', gate=b'import sys\\nsys.exit(0)\\n')
        case('cell arm: a gate that does not refuse -> WRONG:fixture',
             r['standing_cell'] == 'WRONG:fixture' and r['total'] > 0)"""
    new_tail = """        r = run('nogate', gate=b'import sys\\nsys.exit(0)\\n')
        case('cell arm: a gate that does not refuse -> WRONG:fixture',
             r['standing_cell'] == 'WRONG:fixture' and r['total'] > 0)

        # --- proposed cases (round-57 wave-2 mutation findings) -----------------------
        # P1 (kills M3): a refusal row whose named code the gate does not define is counted.
        r = run('badneedle', registry_kwargs=dict(needle_override={'c2-fx-drift': 'RECEIPT_REV_NOT_A_CODE'}))
        case('rows arm: a refusal row naming an undefined code is counted',
             r['short']['rows'] >= 1, 'short=%s' % r['short'])
        # P2 (kills M5): a row that did not hold at baseline cannot supply kill credit.
        r = run('unheld2', registry_kwargs=dict(expect_override={'c2-fx-drift': 0}))
        case('mutants arm: a row that did not hold at baseline supplies no kill credit',
             r['mutants'] == 1, 'mutants=%d/3 (only M3 killed by the exit-2 row)' % r['mutants'])
        # P3 (kills M6): a lane whose committed mutants.json fails the sha256 pin is refused.
        r = run('badpin', mutants_text=tampered_mutants())
        lane_dir, head = built['badpin']
        w = scratch / 'badpin-mainwork'
        w.mkdir()
        ok3, out3 = pin_case(lane_dir, head, w)
        case('mutants pin: a lane whose committed mutants.json fails the sha256 pin is refused',
             ok3, out3)
        # P4 (kills M8): a standing-rules section that names no code is a shortfall.
        r = run('nocodes', skill_text=FX_SKILL_NOCODES.format(row=FX_ROW))
        case('codes arm: a standing-rules section naming no code is a shortfall',
             r['codes_total'] == 0 and r['short']['codes'] >= 1,
             'codes_known=%d/%d short=%s' % (r['codes_known'], r['codes_total'], r['short']['codes']))
        # P5 (kills M9): a cell carrying the emitted code PLUS another code is WRONG.
        r = run('superset', skill_kwargs=dict(cell='RECEIPT_REV_CONTENT_DRIFT and `RECEIPT_REV_ABSENT`'))
        case('cell arm: a cell carrying the emitted code plus another code is WRONG',
             r['standing_cell'] != 'ok' and r['short']['cell'] == 1, r['standing_cell'])
        # P6 (kills M12): the verdict line's PASS field follows the total.
        r = run('good2')
        case('verdict line: C2_R57_PASS=false whenever the total is non-zero',
             'C2_R57_PASS=false' in verdict_line('-', 'x' * 12, dict(r, total=1)))"""
    t = edit(t, old_tail, new_tail, 'F1')

    out = out_dir / 'measure.py'
    out.write_text(t)
    print('wrote %s sha256=%s' % (out, hashlib.sha256(out.read_bytes()).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
