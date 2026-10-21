#!/usr/bin/env python3
"""Frozen round24 counter: eleven hardening predicates for required-command binding.

K1-K4: one-at-a-time guard-weakening mutants of tools/command-binding.py; a
predicate is discriminated only when the pristine public selftest exits 0 and the
mutant's public selftest exits 1 with at least one explicit `CASE ... FAIL` line.
K5-K6: substituted-but-self-consistent frozen bundles; discriminated only when every
active registry row naming that bundle holds on pristine bytes and at least one fails
after substitution. K7-K11: public CLI of tools/registry-replay.py on synthetic
fixtures. All work happens in private copies of --repo; nothing in --repo is written.
Not producer authentication, not a numeric expertise score.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ARGV = "if receipt['argv'] != required['argv']:"
EXIT = "if receipt['exit'] != required['expect']['exit']:"
STDOUT = "if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):"
MUTANTS = [
    ('K1', 'argv-name-insensitive', ARGV,
     "if receipt['argv'] not in [row['argv'] for row in requirements.values()]:"),
    ('K2', 'argv-casefold', ARGV,
     "if [a.lower() for a in receipt['argv']] != [a.lower() for a in required['argv']]:"),
    ('K3', 'exit-negative-ignored', EXIT,
     "if receipt['exit'] >= 0 and receipt['exit'] != required['expect']['exit']:"),
    ('K4', 'stdout-any-token', STDOUT,
     "if required['expect'].get('stdout_contains') and all(token not in receipt['stdout'] "
     "for token in required['expect'].get('stdout_contains', [])):"),
]
PINS = [
    ('K5', 'frozen-clean-substitution', '.ufo/evidence/round-23/replay/bundle.json',
     '.ufo/evidence/round-23/replay/expected.json'),
    ('K6', 'source-read-red-substitution', '.ufo/evidence/round-23/source-read-bundle.json',
     '.ufo/evidence/round-23/source-read-expected.json'),
]


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e


def run(argv, cwd, timeout=600):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env(), timeout=timeout)
    return {'argv': argv, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}


def copy_repo(repo, dest):
    shutil.copytree(repo, dest, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
    return dest


def mutant_rows(repo, work):
    rows = []
    tool = repo / 'tools/command-binding.py'
    if not tool.is_file():
        return [{'id': k, 'name': n, 'discriminated': False, 'reason': 'tool-absent'} for k, n, _, _ in MUTANTS]
    pristine = tool.read_text()
    root = copy_repo(repo, work / 'mutants')
    target = root / 'tools/command-binding.py'
    control = run([sys.executable, str(target), '--selftest'], str(root))
    for key, name, old, new in MUTANTS:
        row = {'id': key, 'name': name, 'anchor_count': pristine.count(old), 'control_exit': control['exit']}
        if control['exit'] != 0 or row['anchor_count'] != 1:
            row.update(discriminated=False, reason='inconclusive')
            rows.append(row)
            continue
        target.write_text(pristine.replace(old, new, 1))
        result = run([sys.executable, str(target), '--selftest'], str(root))
        target.write_text(pristine)
        fails = [line for line in result['stdout'].splitlines() if line.startswith('CASE ') and line.endswith(' FAIL')]
        row.update(exit=result['exit'], failing_cases=fails, stdout_tail=result['stdout'][-400:],
                   discriminated=result['exit'] == 1 and bool(fails))
        rows.append(row)
    restored = run([sys.executable, str(target), '--selftest'], str(root))
    for row in rows:
        row['restored_exit'] = restored['exit']
        if restored['exit'] != 0:
            row['discriminated'] = False
    return rows


def registry_rows_for(root, path):
    registry = json.loads((root / 'tools/registry.json').read_text())
    return [r['name'] for r in registry['rows'] if r.get('status') == 'active' and path in r['argv']]


def held(root, name):
    result = run([sys.executable, str(root / 'tools/registry-check.py'), '--root', str(root), '--only', name,
                  '--json'], str(root))
    try:
        rows = json.loads(result['stdout'])['rows']
        return rows[0]['held'] is True, result['exit']
    except (ValueError, KeyError, IndexError, TypeError):
        return None, result['exit']


def substitute(root, key, bundle, expected):
    if key == 'K5':
        raw = (root / '.ufo/evidence/round-23/correct-command-bundle.json').read_bytes()
    else:
        value = json.loads((root / bundle).read_text())
        value['receipts'][0]['stdout'] = value['receipts'][0]['stdout'] + '\n'
        raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    (root / bundle).write_bytes(raw)
    (root / expected).write_text(json.dumps({'schema': 'command-binding-expected-v1',
                                             'bundle_sha256': hashlib.sha256(raw).hexdigest()}, indent=2) + '\n')


def pin_rows(repo, work):
    rows = []
    for key, name, bundle, expected in PINS:
        root = copy_repo(repo, work / key)
        names = registry_rows_for(root, bundle)
        row = {'id': key, 'name': name, 'rows': names}
        if not names:
            row.update(discriminated=False, reason='no-active-row')
            rows.append(row)
            continue
        control = {n: held(root, n) for n in names}
        substitute(root, key, bundle, expected)
        after = {n: held(root, n) for n in names}
        row.update(control={n: v[0] for n, v in control.items()}, substituted={n: v[0] for n, v in after.items()},
                   discriminated=all(v[0] is True for v in control.values())
                   and any(v[0] is False for v in after.values()))
        rows.append(row)
    return rows


def replay_rows(repo, work):
    tool = repo / 'tools/registry-replay.py'
    names = [('K7', 'runner-not-held-refused'), ('K8', 'runner-cleanup-refused'), ('K9', 'stream-limit-refused'),
             ('K10', 'live-dependent-listed'), ('K11', 'fleet-root-realpath')]
    if not tool.is_file():
        return [{'id': k, 'name': n, 'discriminated': False, 'reason': 'tool-absent'} for k, n in names]
    fx = work / 'replay'
    fx.mkdir()
    def obs(**edits):
        row = {'requirement': {'name': 'one', 'argv': ['gate', '--check'], 'expect': {'exit': 0, 'stdout_contains': ['OK']}},
               'external': False, 'argv': ['gate', '--check'], 'cwd': '/fixture/clone', 'revision': 'a' * 40,
               'runner_result': {'got': 0, 'held': True, 'stdout': 'OK\n', 'stderr': ''}}
        for path, value in edits.items():
            if path == 'external':
                row['external'] = value
            else:
                row['runner_result'][path] = value
        return {'schema': 'registry-replay-observations-v1', 'revision': 'a' * 40, 'cwd': '/fixture/clone',
                'rows': [row]}
    def project(name, value, extra=()):
        src = fx / (name + '.json')
        src.write_text(json.dumps(value))
        out = fx / (name + '-out')
        result = run([sys.executable, str(tool), '--project', str(src), '--out', str(out), '--json', *extra], str(fx))
        try:
            report = json.loads(result['stdout'])
        except ValueError:
            report = {}
        return result, report, (out / 'bundle.json').exists()
    rows = []
    control, creport, cbundle = project('control', obs())
    control_ok = control['exit'] == 0 and creport.get('finding_ids') == [] and cbundle
    for key, name, value, finding, extra in (
            ('K7', 'runner-not-held-refused', obs(held=False), 'RUNNER_NOT_HELD', ()),
            ('K8', 'runner-cleanup-refused', obs(held=False, cleanup_error='row descendants remain'),
             'RUNNER_CLEANUP_FAILED', ()),
            ('K9', 'stream-limit-refused', obs(stdout='OK\n' + 'x' * 64), 'STREAM_LIMIT', ('--max-stream-bytes', '16'))):
        result, report, bundle = project(key, value, extra)
        rows.append({'id': key, 'name': name, 'exit': result['exit'], 'finding_ids': report.get('finding_ids'),
                     'bundle_written': bundle, 'control_ok': control_ok,
                     'discriminated': control_ok and result['exit'] == 1 and finding in report.get('finding_ids', [])
                     and not bundle})
    result, report, bundle = project('K10', obs(external=True, non_hermetic_argv=['/live/root']))
    rows.append({'id': 'K10', 'name': 'live-dependent-listed', 'exit': result['exit'], 'report': report,
                 'discriminated': control_ok and result['exit'] == 0 and report.get('live_dependent') == ['one']
                 and creport.get('live_dependent') == [] and bundle})
    fleet = fx / 'fleet'
    (fleet / 'lane-shokunin').mkdir(parents=True)
    (fleet / 'other-shokunin').mkdir()
    alias = fx / 'alias'
    alias.symlink_to(fleet, target_is_directory=True)
    plan = run([sys.executable, str(tool), '--plan', '--repo', str(alias / 'other-shokunin' / '..' / 'lane-shokunin'),
                '--json'], str(fx))
    try:
        value = json.loads(plan['stdout'])
    except ValueError:
        value = {}
    real = os.path.realpath(fleet)
    rows.append({'id': 'K11', 'name': 'fleet-root-realpath', 'exit': plan['exit'], 'plan': value,
                 'discriminated': plan['exit'] == 0 and value.get('fleet_root') == real
                 and value.get('repo') == os.path.join(real, 'lane-shokunin')
                 and value.get('siblings') == [os.path.join(real, 'other-shokunin')]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    a = ap.parse_args()
    repo = a.repo.resolve()
    with tempfile.TemporaryDirectory(prefix='tameshi-r24-measure-') as tmp:
        work = Path(tmp)
        rows = mutant_rows(repo, work) + pin_rows(repo, work) + replay_rows(repo, work)
    n = sum(bool(r['discriminated']) for r in rows)
    print(json.dumps({'schema': 'tameshi-r24-hardening-v1', 'discriminated': n, 'total': len(rows), 'rows': rows},
                     indent=2, sort_keys=True))
    return 0 if n == len(rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
