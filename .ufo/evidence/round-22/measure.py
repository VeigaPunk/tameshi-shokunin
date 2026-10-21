#!/usr/bin/env python3
"""Frozen round22 counter: eight public-CLI rejection predicates, not an authenticity claim."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

CASES = [
    ('false-completion-count', 'TOTAL_MISMATCH'),
    ('failed-with-report-counted-completed', 'TOTAL_MISMATCH'),
    ('missing-outcome', 'MEMBERSHIP_MISMATCH'),
    ('duplicate-agent', 'DUPLICATE_AGENT'),
    ('unknown-status', 'UNKNOWN_STATUS'),
    ('registry-id-mismatch', 'IDENTITY_MISMATCH'),
    ('replacement-seat', 'REPLACEMENT_FORBIDDEN'),
    ('snapshot-tampering', 'SNAPSHOT_TAMPERED'),
]

def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()

def measure(repo):
    tool = repo / 'tools/wave-accounting.py'
    if not tool.is_file():
        return {'discriminated': 0, 'total': 8, 'tool_present': False, 'cases': []}, 1
    fixture = {'schema': 'wave-accounting-v1', 'waves': [{
        'name': 'probe',
        'members': [{'name': 'pass', 'id': 'seat.pass', 'role': 'reviewer'},
                    {'name': 'dead', 'id': 'seat.dead', 'role': 'critic'}],
        'outcomes': [{'name': 'pass', 'id': 'seat.pass', 'role': 'reviewer', 'status': 'completed', 'replaced': False},
                     {'name': 'dead', 'id': 'seat.dead', 'role': 'critic', 'status': 'failed', 'replaced': False}],
        'reports': ['pass', 'dead'],
        'claimed': {'seats': 2, 'completed': 1, 'dead': 1}}]}
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    rows = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r22-measure-') as d:
        work = Path(d)
        def invoke(bundle, tamper=False):
            data = encode(bundle)
            (work / 'bundle.json').write_bytes(data)
            expected = {'schema': 'wave-accounting-expected-v1', 'bundle_sha256': hashlib.sha256(data).hexdigest()}
            (work / 'expected.json').write_bytes(encode(expected))
            if tamper:
                (work / 'bundle.json').write_bytes(data + b' ')
            p = subprocess.run(['python3', str(tool), '--bundle', str(work / 'bundle.json'), '--expected', str(work / 'expected.json'), '--json'], capture_output=True, text=True, env=env, timeout=15)
            try:
                result = json.loads(p.stdout)
            except ValueError:
                result = {}
            return p, result
        control, control_result = invoke(fixture)
        if control.returncode != 0 or control_result.get('finding_ids') != []:
            return {'discriminated': 0, 'total': 8, 'control_exit': control.returncode, 'control_stdout': control.stdout, 'control_stderr': control.stderr}, 2
        for name, finding in CASES:
            b = copy.deepcopy(fixture)
            w = b['waves'][0]
            if name == 'false-completion-count':
                w['claimed']['seats'] = 3
            elif name == 'failed-with-report-counted-completed':
                w['claimed'].update(completed=2, dead=0)
            elif name == 'missing-outcome':
                w['outcomes'].pop()
            elif name == 'duplicate-agent':
                w['members'][1]['id'] = 'seat.pass'
                w['outcomes'][1]['id'] = 'seat.pass'
            elif name == 'unknown-status':
                w['outcomes'][1]['status'] = 'unknown'
            elif name == 'registry-id-mismatch':
                w['outcomes'][1]['id'] = 'seat.other'
            elif name == 'replacement-seat':
                w['outcomes'][1]['replaced'] = True
            p, result = invoke(b, name == 'snapshot-tampering')
            expected_exit = 2 if name == 'snapshot-tampering' else 1
            ok = p.returncode == expected_exit and finding in result.get('finding_ids', [])
            rows.append({'name': name, 'expected_finding': finding, 'expected_exit': expected_exit, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr, 'discriminated': ok})
    n = sum(r['discriminated'] for r in rows)
    return {'discriminated': n, 'total': len(CASES), 'tool_present': True, 'tool_sha256': hashlib.sha256(tool.read_bytes()).hexdigest(), 'control_exit': control.returncode, 'cases': rows}, 0 if n == 8 else 1

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    a = ap.parse_args()
    result, code = measure(a.repo)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(code)
