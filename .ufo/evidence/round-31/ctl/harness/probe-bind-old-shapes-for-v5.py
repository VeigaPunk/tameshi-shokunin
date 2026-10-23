#!/usr/bin/env python3
"""Replay only the assigned round-30 controls and seven shapes against frozen v4.

The copied round-30 harness builds the exact same transcript structures, keeps
its synthetic session labels, and restores all seven mutation stores in finally.
Only its detector path is rebound; the assembly, registry and prefix are unchanged.
The v3 figures below are historical references, not fresh v3 executions.
"""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('retained_v3_probe', ROOT / 'probe-bind-v3.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.BIND = probe.LANE / '.ufo/evidence/round-31/coldread/bind-select-v5.py'
V3 = {
    'promptonly': (0, 1), 'donothing': (0, 1), 'textmention': (0, 1),
    'noresult': (0, 1), 'forged': (30, 0),
    'different_tool': (31, 0), 'different_result_id': (0, 1),
    'user_authored_call': (0, 1), 'error_result': (31, 0),
    'comment_only_shell': (31, 0), 'result_before_call': (31, 0),
    'reused_call_id': (31, 0),
}


def control_hashes():
    return {name: probe.manifest(ROOT / 'controls' / name) for name in probe.CONTROLS}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=('controls', 'shapes'), required=True)
    phase = parser.parse_args().phase
    before = probe.frozen_hashes()
    controls_before = control_hashes() if phase == 'controls' else None
    results = probe.controls() if phase == 'controls' else probe.shapes()
    after = probe.frozen_hashes()
    controls_after = control_hashes() if phase == 'controls' else None
    data = {
        'seat': 'CtlBindV4Old', 'phase': phase,
        'axes': ['calibration', 'false retention resistance', 'reproducibility',
                 'exact restoration'],
        'copied_v3_harness_sha256': probe.sha((ROOT / 'probe-bind-v3.py').read_bytes()),
        'before_frozen_hashes': before, 'after_frozen_hashes': after,
        'frozen_inputs_unchanged': before == after,
        'before_control_hashes': controls_before, 'after_control_hashes': controls_after,
        'control_bytes_unchanged': controls_before == controls_after if phase == 'controls' else None,
        'results': results,
    }
    probe.put(ROOT / ('results-' + phase + '.json'), data)
    for r in results:
        measured = r if phase == 'controls' else r.get('mutated') or {}
        line = {
            'shape': r['shape'], 'v3_kept': V3[r['shape']][0],
            'v3_exit': V3[r['shape']][1], 'v4_kept': measured.get('kept'),
            'assembled': measured.get('assembled'), 'v4_exit': measured.get('exit'),
        }
        if phase == 'shapes':
            line.update({
                'verdict': r['verdict'],
                'pristine': [r['pristine'].get('kept'), r['pristine']['exit']],
                'restored': [r['restored'].get('kept'), r['restored']['exit']],
                'restored_exact': r['restored_exact'],
            })
        else:
            line['verdict'] = 'rejected' if (measured.get('kept'), measured.get('exit')) == (0, 1) else 'finding'
        print(json.dumps(line), flush=True)
    print('frozen_inputs_unchanged=' + str(before == after).lower(), flush=True)
    if phase == 'controls':
        print('control_bytes_unchanged=' + str(controls_before == controls_after).lower(), flush=True)


if __name__ == '__main__':
    main()
