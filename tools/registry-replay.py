#!/usr/bin/env python3
"""tools/registry-replay.py — replay frozen registry requirements and project a binding bundle.

Successor of the round23 evidence instrument `.ufo/evidence/round-23/replay.py`
(which stays unchanged). Differences, each routed by round23 critics:

* projection refuses to publish a bundle when any runner row did not hold
  (RUNNER_NOT_HELD) or reported a cleanup failure (RUNNER_CLEANUP_FAILED);
* each retained stdout/stderr is bounded by --max-stream-bytes (STREAM_LIMIT);
* rows declared `external` in the source registry, or flagged by the runner
  with `non_hermetic_argv`, are listed in `live_dependent` instead of being
  silently reported as revision-pinned;
* the fleet root and sibling identities are realpath-normalised;
* the runner digest is taken from the clone copy that actually executes.

Receipt argv/cwd/revision are still the invocation parameters the instrument
passes to the runner, not independently observed process metadata, and this
tool authenticates no producer. Writes only under --out. Row commands run in a
private clone whose fleet mirror symlinks the live sibling repos, so rows are
not write-isolated from siblings; that is a limit, not a guarantee.

  registry-replay.py --run --repo LANE --rev REV --requirements FILE --registry-baseline FILE --out DIR
  registry-replay.py --project OBSERVATIONS --out DIR [--max-stream-bytes N] [--json]
  registry-replay.py --plan --repo LANE [--json]
  registry-replay.py --selftest

Exit: 0 bundle published / plan printed · 1 refused (findings) · 2 invalid or
unavailable input · 64 usage.
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
OBS_SCHEMA = 'registry-replay-observations-v1'
DEFAULT_MAX = 1 << 20


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print('registry-replay: ' + message, file=sys.stderr)
        raise SystemExit(64)


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e


def plan(repo):
    """Realpath-normalised lane, fleet root and sibling lanes (no cloning)."""
    real = os.path.realpath(repo)
    fleet = os.path.dirname(real)
    siblings = sorted(os.path.realpath(p) for p in Path(fleet).glob('*-shokunin')
                      if p.is_dir() and os.path.realpath(p) != real)
    return {'repo': real, 'fleet_root': fleet, 'siblings': siblings}


def project(observations, max_bytes):
    """Return (exit, report, bundle_or_None) from runner observations."""
    if (not isinstance(observations, dict) or observations.get('schema') != OBS_SCHEMA
            or not isinstance(observations.get('rows'), list) or not observations['rows']
            or not isinstance(observations.get('revision'), str) or not isinstance(observations.get('cwd'), str)):
        return 2, {'finding_ids': ['INVALID_OBSERVATIONS']}, None
    findings, refused, live = set(), [], []
    receipts, requirements = [], []
    for row in observations['rows']:
        result = row.get('runner_result') if isinstance(row, dict) else None
        requirement = row.get('requirement') if isinstance(row, dict) else None
        if not isinstance(result, dict) or not isinstance(requirement, dict) or not isinstance(requirement.get('name'), str):
            return 2, {'finding_ids': ['INVALID_OBSERVATIONS']}, None
        name = requirement['name']
        if result.get('cleanup_error'):
            findings.add('RUNNER_CLEANUP_FAILED')
            refused.append(name)
        elif result.get('held') is not True:
            findings.add('RUNNER_NOT_HELD')
            refused.append(name)
        for stream in ('stdout', 'stderr'):
            text = result.get(stream, '')
            if not isinstance(text, str):
                return 2, {'finding_ids': ['INVALID_OBSERVATIONS']}, None
            if len(text.encode('utf-8', 'surrogateescape')) > max_bytes:
                findings.add('STREAM_LIMIT')
                refused.append(name)
        if row.get('external') is True or result.get('non_hermetic_argv'):
            live.append(name)
        requirements.append(requirement)
        receipts.append({'name': name, 'argv': row.get('argv'), 'cwd': row.get('cwd'),
                         'revision': row.get('revision'), 'exit': result.get('got'),
                         'stdout': result.get('stdout', ''), 'stderr': result.get('stderr', '')})
    report = {'schema': 'registry-replay-report-v1', 'finding_ids': sorted(findings),
              'refused_rows': sorted(set(refused)), 'live_dependent': sorted(live),
              'revision_pinned': len(receipts) - len(set(live)), 'rows': len(receipts),
              'max_stream_bytes': max_bytes, 'bundle_sha256': None}
    if findings:
        return 1, report, None
    bundle = {'schema': 'command-binding-v1', 'revision': observations['revision'], 'cwd': observations['cwd'],
              'requirements': requirements, 'receipts': receipts}
    return 0, report, bundle


def publish(code, report, bundle, out):
    if bundle is None:
        return report
    out.mkdir(parents=True, exist_ok=True)
    raw = encode(bundle)
    report['bundle_sha256'] = hashlib.sha256(raw).hexdigest()
    (out / 'bundle.json').write_bytes(raw)
    (out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',
                                                'bundle_sha256': report['bundle_sha256']}))
    (out / 'live-dependent.json').write_bytes(encode({'live_dependent': report['live_dependent'],
                                                     'revision_pinned': report['revision_pinned'],
                                                     'rows': report['rows']}))
    return report


def run_replay(args):
    e = env()
    layout = plan(args.repo)
    repo = layout['repo']
    revision = subprocess.run(['git', '-C', repo, 'rev-parse', '--verify', '--end-of-options', args.rev + '^{commit}'],
                              check=True, capture_output=True, text=True, env=e).stdout.strip()
    frozen = json.loads(Path(args.requirements).read_bytes())
    raw_registry = Path(args.registry_baseline).read_bytes()
    if hashlib.sha256(raw_registry).hexdigest() != frozen['registry_sha256']:
        print('registry-replay: frozen registry digest mismatch', file=sys.stderr)
        return 2
    source_rows = {r['name']: r for r in json.loads(raw_registry)['rows'] if r['status'] == 'active'}
    requirements = [{'name': r['name'], 'argv': r['argv'], 'expect': r['expect']} for r in source_rows.values()]
    if requirements != frozen['requirements']:
        print('registry-replay: frozen requirements differ from source registry', file=sys.stderr)
        return 2
    rows = []
    started = datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix='tameshi-registry-replay-') as tmp:
        fleet = Path(tmp) / 'fleet'
        fleet.mkdir()
        clone = fleet / os.path.basename(repo)
        subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', repo, str(clone)], check=True, env=e)
        subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', revision], check=True, env=e)
        head = subprocess.run(['git', '-C', str(clone), 'rev-parse', 'HEAD'], check=True, capture_output=True,
                              text=True, env=e).stdout.strip()
        if head != revision:
            print('registry-replay: clone HEAD differs from requested revision', file=sys.stderr)
            return 2
        for sibling in layout['siblings']:
            (fleet / os.path.basename(sibling)).symlink_to(sibling, target_is_directory=True)
        runner_path = clone / 'tools/registry-check.py'
        runner_sha = hashlib.sha256(runner_path.read_bytes()).hexdigest()
        spec = importlib.util.spec_from_file_location('registry_runner', runner_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for requirement in requirements:
            row = source_rows[requirement['name']]
            begin = datetime.now(timezone.utc).isoformat()
            result = module.run_row(row, str(clone), layout['fleet_root'], retain_streams=True)
            end = datetime.now(timezone.utc).isoformat()
            rows.append({'requirement': requirement, 'external': row.get('external') is True,
                         'argv': list(row['argv']), 'cwd': str(clone), 'revision': head,
                         'measurement_interval': {'start': begin, 'end': end}, 'runner_result': result})
            print(row['name'], result.get('got'), result.get('held'), flush=True)
        observations = {'schema': OBS_SCHEMA, 'revision': head, 'cwd': str(clone), 'rows': rows,
                        'argv': sys.argv, 'plan': layout, 'runner_sha256_clone_copy': runner_sha,
                        'source_requirements_revision': frozen.get('source_revision'),
                        'registry_sha256': frozen['registry_sha256'],
                        'measurement_interval': {'start': started, 'end': datetime.now(timezone.utc).isoformat()}}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'observations.json').write_bytes(encode(observations))
    code, report, bundle = project(observations, args.max_stream_bytes)
    report = publish(code, report, bundle, out)
    print(json.dumps(report, sort_keys=True))
    return code


def selftest():
    """Public-CLI cases with literal expected outcomes."""
    def obs(**edits):
        row = {'requirement': {'name': 'one', 'argv': ['gate'], 'expect': {'exit': 0}}, 'external': False,
               'argv': ['gate'], 'cwd': '/c', 'revision': 'b' * 40,
               'runner_result': {'got': 0, 'held': True, 'stdout': 'ok', 'stderr': ''}}
        for key, value in edits.items():
            (row if key == 'external' else row['runner_result'])[key] = value
        return {'schema': OBS_SCHEMA, 'revision': 'b' * 40, 'cwd': '/c', 'rows': [row]}
    cases = [('clean', obs(), (), 0, [], True), ('not-held', obs(held=False), (), 1, ['RUNNER_NOT_HELD'], False),
             ('cleanup', obs(held=False, cleanup_error='x'), (), 1, ['RUNNER_CLEANUP_FAILED'], False),
             ('held-missing', obs(held=None), (), 1, ['RUNNER_NOT_HELD'], False),
             ('stream', obs(stderr='e' * 9), ('--max-stream-bytes', '8'), 1, ['STREAM_LIMIT'], False),
             ('stream-at-limit', obs(stdout='12345678'), ('--max-stream-bytes', '8'), 0, [], True),
             ('external', obs(external=True), (), 0, [], True),
             ('non-hermetic', obs(non_hermetic_argv=['/live']), (), 0, [], True),
             ('invalid', {'schema': 'other'}, (), 2, ['INVALID_OBSERVATIONS'], False)]
    passed = 0
    with tempfile.TemporaryDirectory(prefix='tameshi-registry-replay-selftest-') as tmp:
        for name, value, extra, code, findings, written in cases:
            src = Path(tmp) / (name + '.json')
            src.write_text(json.dumps(value))
            out = Path(tmp) / (name + '-out')
            r = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--project', str(src), '--out', str(out),
                                '--json', *extra], capture_output=True, text=True, timeout=30)
            try:
                rep = json.loads(r.stdout)
            except ValueError:
                rep = {}
            ok = (r.returncode == code and rep.get('finding_ids') == findings
                  and (out / 'bundle.json').exists() == written)
            if name in ('external', 'non-hermetic'):
                ok = ok and rep.get('live_dependent') == ['one'] and rep.get('revision_pinned') == 0
            if name == 'clean':
                ok = ok and rep.get('live_dependent') == [] and rep.get('revision_pinned') == 1
            passed += ok
            print('CASE', name, 'PASS' if ok else 'FAIL')
        fleet = Path(tmp) / 'fleet'
        (fleet / 'lane-shokunin').mkdir(parents=True)
        (fleet / 'peer-shokunin').mkdir()
        (Path(tmp) / 'alias').symlink_to(fleet, target_is_directory=True)
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--plan', '--repo',
                            str(Path(tmp) / 'alias' / 'peer-shokunin' / '..' / 'lane-shokunin'), '--json'],
                           capture_output=True, text=True, timeout=30)
        real = os.path.realpath(fleet)
        try:
            value = json.loads(r.stdout)
        except ValueError:
            value = {}
        ok = (r.returncode == 0 and value.get('fleet_root') == real
              and value.get('siblings') == [os.path.join(real, 'peer-shokunin')])
        passed += ok
        print('CASE plan-realpath', 'PASS' if ok else 'FAIL')
    total = len(cases) + 1
    print('REGISTRY_REPLAY_SELFTEST: %d/%d pass' % (passed, total))
    return 0 if passed == total else 1


def main():
    p = Parser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run', action='store_true')
    mode.add_argument('--project', metavar='OBSERVATIONS')
    mode.add_argument('--plan', action='store_true')
    mode.add_argument('--selftest', action='store_true')
    p.add_argument('--repo')
    p.add_argument('--rev')
    p.add_argument('--requirements')
    p.add_argument('--registry-baseline')
    p.add_argument('--out')
    p.add_argument('--max-stream-bytes', type=int, default=DEFAULT_MAX)
    p.add_argument('--json', action='store_true')
    a = p.parse_args()
    if a.max_stream_bytes < 1:
        p.error('--max-stream-bytes must be positive')
    if a.selftest:
        return selftest()
    if a.plan:
        if not a.repo:
            p.error('--plan needs --repo')
        value = plan(a.repo)
        print(json.dumps(value, sort_keys=True) if a.json else '\n'.join('%s: %s' % kv for kv in sorted(value.items())))
        return 0
    if a.project:
        if not a.out:
            p.error('--project needs --out')
        try:
            observations = json.loads(Path(a.project).read_bytes())
        except (OSError, ValueError, UnicodeError):
            print(json.dumps({'finding_ids': ['INVALID_OBSERVATIONS']}))
            return 2
        code, report, bundle = project(observations, a.max_stream_bytes)
        report = publish(code, report, bundle, Path(a.out))
        print(json.dumps(report, sort_keys=True))
        return code
    if not (a.repo and a.rev and a.requirements and a.registry_baseline and a.out):
        p.error('--run needs --repo --rev --requirements --registry-baseline --out')
    return run_replay(a)


if __name__ == '__main__':
    raise SystemExit(main())
