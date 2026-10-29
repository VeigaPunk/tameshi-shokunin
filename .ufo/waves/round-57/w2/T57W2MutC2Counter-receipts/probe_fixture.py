#!/usr/bin/env python3
"""Differential probe: for a given counter file, run ONE named fixture and dump the arm
tallies, so a survivor's semantics can be stated exactly (which fixture, which field).
Usage: probe_fixture.py <counter.py> <fixture-name> <lane> <rev>
"""
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path


def load(path):
    spec = importlib.util.spec_from_file_location('m_' + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    counter_path, fixture, lane, rev = sys.argv[1:5]
    mod = load(counter_path)
    lane = str(Path(lane).resolve())
    rev = mod.resolve(lane, rev)
    gate_raw = mod.show(lane, rev, mod.GATE)
    rc_raw = mod.show(lane, rev, mod.REGCHECK)
    mutants_raw = (Path(counter_path).resolve().parent / 'mutants.json').read_bytes()
    scratch = Path(tempfile.mkdtemp(prefix='c2-probe-'))
    parent = scratch / fixture
    parent.mkdir()
    kw = {}
    if fixture == 'norefusal':
        kw = dict(registry_kwargs=dict(drop=('c2-fx-unresolvable',)))
    elif fixture == 'unheld':
        kw = dict(registry_kwargs=dict(expect_override={'c2-fx-drift': 0}))
    elif fixture == 'onlyok':
        kw = dict(registry_kwargs=dict(drop=('c2-fx-drift', 'c2-fx-unresolvable')))
    elif fixture == 'nodrift':
        kw = dict(registry_kwargs=dict(drop=('c2-fx-drift',)))
    elif fixture == 'cellgone':
        kw = dict(skill_kwargs=dict(cell='see the gate'))
    lane_dir, head = mod.build_lane(parent, 'lane', gate_raw, rc_raw, **kw)
    res = mod.measure(lane_dir, head, scratch / 'work', mutants_raw, False)
    out = {'fixture': fixture, 'total': res['total'], 'short': res['short'],
           'mutants': res['mutants'], 'held': res['held'], 'rows_n': res['rows_n'],
           'gate_rows': res['gate_rows'], 'exits': res['exits'],
           'skill_row': res['skill_row'], 'codes_known': res['codes_known'],
           'codes_total': res['codes_total'], 'standing_cell': res['standing_cell'],
           'verdict': mod.verdict_line('-', 'x' * 12, res)}
    print(json.dumps(out, indent=1))
    import shutil
    shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
