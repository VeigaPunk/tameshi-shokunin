#!/usr/bin/env python3
"""Frozen round23 ruler; ten public CLI predicates, no authenticity claim."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

CASES = [('argv-mismatch', 'ARGV_MISMATCH', 1), ('cwd-mismatch', 'CWD_MISMATCH', 1),
         ('revision-mismatch', 'REVISION_MISMATCH', 1), ('missing-required-command', 'MEMBERSHIP_MISMATCH', 1),
         ('duplicate-command', 'DUPLICATE_COMMAND', 1), ('unknown-command', 'MEMBERSHIP_MISMATCH', 1),
         ('wrong-exit', 'EXIT_MISMATCH', 1), ('missing-stdout-token', 'STDOUT_MISMATCH', 1),
         ('bool-exit', 'INVALID_RECEIPT', 2), ('tampered-bundle', 'SNAPSHOT_TAMPERED', 2)]

def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()

def fixture():
    return {'schema': 'command-binding-v1', 'revision': 'a' * 40, 'cwd': '/fixture/repo',
            'requirements': [{'name': 'one', 'argv': ['python3', 'gate.py', '--selftest'],
                              'expect': {'exit': 0, 'stdout_contains': ['PASS']}},
                             {'name': 'two', 'argv': ['python3', 'gate.py', '--bad'],
                              'expect': {'exit': 1, 'stdout_contains': ['REJECTED']}}],
            'receipts': [{'name': 'one', 'argv': ['python3', 'gate.py', '--selftest'],
                          'cwd': '/fixture/repo', 'revision': 'a' * 40,
                          'exit': 0, 'stdout': 'PASS\n', 'stderr': ''},
                         {'name': 'two', 'argv': ['python3', 'gate.py', '--bad'],
                          'cwd': '/fixture/repo', 'revision': 'a' * 40,
                          'exit': 1, 'stdout': 'REJECTED\n', 'stderr': ''}]}

def attack(bundle, name):
    if name == 'argv-mismatch':
        bundle['receipts'][0]['argv'] = ['cat', 'gate.py']
    elif name == 'cwd-mismatch':
        bundle['receipts'][0]['cwd'] = '/other'
    elif name == 'revision-mismatch':
        bundle['receipts'][0]['revision'] = 'b' * 40
    elif name == 'missing-required-command':
        bundle['receipts'].pop()
    elif name == 'duplicate-command':
        bundle['receipts'].append(copy.deepcopy(bundle['receipts'][0]))
    elif name == 'unknown-command':
        bundle['receipts'][0]['name'] = 'other'
    elif name == 'wrong-exit':
        bundle['receipts'][0]['exit'] = 1
    elif name == 'missing-stdout-token':
        bundle['receipts'][0]['stdout'] = ''
    elif name == 'bool-exit':
        bundle['receipts'][0]['exit'] = False


def measure(repo):
    tool = repo / 'tools/command-binding.py'
    if not tool.is_file():
        return {'tool_present': False, 'discriminated': 0, 'total': 10, 'cases': []}, 1
    rows = []
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    with tempfile.TemporaryDirectory(prefix='tameshi-r23-ruler-') as tmp:
        work = Path(tmp)
        def invoke(bundle, tamper=False):
            data = encode(bundle)
            (work / 'bundle.json').write_bytes(data)
            (work / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',
                'bundle_sha256': hashlib.sha256(data).hexdigest()}))
            if tamper:
                (work / 'bundle.json').write_bytes(data + b' ')
            argv = ['python3', str(tool), '--bundle', str(work / 'bundle.json'),
                    '--expected', str(work / 'expected.json'), '--json']
            p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=20)
            try:
                value = json.loads(p.stdout)
            except ValueError:
                value = {}
            return p, value, argv
        p, value, argv = invoke(fixture())
        control = {'argv': argv, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
        if p.returncode != 0 or value.get('finding_ids') != []:
            return {'tool_present': True, 'discriminated': 0, 'total': 10, 'control': control}, 2
        for name, finding, code in CASES:
            bundle = fixture()
            attack(bundle, name)
            p, value, argv = invoke(bundle, name == 'tampered-bundle')
            ok = p.returncode == code and finding in value.get('finding_ids', [])
            rows.append({'name': name, 'expected_finding': finding, 'expected_exit': code,
                         'argv': argv, 'exit': p.returncode, 'stdout': p.stdout,
                         'stderr': p.stderr, 'discriminated': ok})
    n = sum(row['discriminated'] for row in rows)
    return {'tool_present': True, 'tool_sha256': hashlib.sha256(tool.read_bytes()).hexdigest(),
            'discriminated': n, 'total': 10, 'control': control, 'cases': rows}, 0 if n == 10 else 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    result, code = measure(args.repo)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(code)
