#!/usr/bin/env python3
"""Round23 evidence instrument: execute frozen registry requirements in a clone.

Uses the existing registry runner's bounded cleanup and opt-in complete streams.
The projection records invocation fields beside each newly executed row; it
never fills those fields into historical observations. Output names are local
arguments. No live lane or sibling writes, network, ref or index mutations.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
sys.dont_write_bytecode = True

def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--rev', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    revision = subprocess.run(['git', '-C', str(args.repo), 'rev-parse', '--verify', '--end-of-options',
                               args.rev + '^{commit}'], check=True, capture_output=True, text=True, env=env).stdout.strip()
    frozen = json.loads((Path(__file__).parent / 'requirements.json').read_bytes())
    raw_registry = (Path(__file__).parent / 'registry-baseline.json').read_bytes()
    if hashlib.sha256(raw_registry).hexdigest() != frozen['registry_sha256']:
        raise SystemExit('frozen registry digest mismatch')
    source_rows = {r['name']: r for r in json.loads(raw_registry)['rows'] if r['status'] == 'active'}
    requirements = [{'name': r['name'], 'argv': r['argv'], 'expect': r['expect']} for r in source_rows.values()]
    if requirements != frozen['requirements']:
        raise SystemExit('frozen requirements differ from source registry')
    args.out.mkdir(parents=True, exist_ok=True)
    observations = []
    started = datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix='tameshi-r23-replay-') as tmp:
        fleet = Path(tmp) / 'fleet'
        fleet.mkdir()
        clone = fleet / args.repo.name
        subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', str(args.repo), str(clone)], check=True, env=env)
        subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', revision], check=True, env=env)
        for sibling in args.repo.parent.glob('*-shokunin'):
            if sibling != args.repo and sibling.is_dir():
                (fleet / sibling.name).symlink_to(sibling, target_is_directory=True)
        spec = importlib.util.spec_from_file_location('registry_runner', clone / 'tools/registry-check.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for requirement in requirements:
            row = source_rows[requirement['name']]
            begin = datetime.now(timezone.utc).isoformat()
            result = module.run_row(row, str(clone), str(args.repo.parent), retain_streams=True)
            end = datetime.now(timezone.utc).isoformat()
            observations.append({'requirement': requirement, 'argv': list(row['argv']), 'cwd': str(clone),
                                 'revision': revision, 'measurement_interval': {'start': begin, 'end': end},
                                 'runner_result': result})
            print(row['name'], result.get('got'), result.get('held'), flush=True)
        bundle = {'schema': 'command-binding-v1', 'revision': revision, 'cwd': str(clone),
                  'requirements': requirements, 'receipts': [
                      {'name': o['requirement']['name'], 'argv': o['argv'], 'cwd': o['cwd'],
                       'revision': o['revision'], 'exit': o['runner_result'].get('got'),
                       'stdout': o['runner_result'].get('stdout', ''),
                       'stderr': o['runner_result'].get('stderr', '')} for o in observations]}
    raw = encode(bundle)
    (args.out / 'bundle.json').write_bytes(raw)
    (args.out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',
                                                    'bundle_sha256': hashlib.sha256(raw).hexdigest()}))
    (args.out / 'observations.json').write_bytes(encode({'argv': sys.argv, 'revision': revision,
        'source_requirements_revision': frozen['source_revision'], 'registry_sha256': frozen['registry_sha256'],
        'runner_sha256': hashlib.sha256((args.repo / 'tools/registry-check.py').read_bytes()).hexdigest(),
        'capture': 'complete decoded stdout/stderr; original runner tails retained separately',
        'measurement_interval': {'start': started, 'end': datetime.now(timezone.utc).isoformat()},
        'rows': observations}))
    held = sum(o['runner_result'].get('held') is True for o in observations)
    print('REPLAY:', held, '/', len(observations))
    return 0 if held == len(observations) else 1

if __name__ == '__main__':
    raise SystemExit(main())
