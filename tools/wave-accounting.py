#!/usr/bin/env python3
"""Reconcile retained callback outcomes with exact wave membership.

Reports are artifacts, never terminal-state authority. This gate validates
caller-declared retained data and its persisted digest, not provider telemetry.
Exit 0 clean; 1 failed invariant; 2 invalid/unavailable/tampered input;
64 usage (could-not-evaluate). Read-only except isolated --selftest fixtures.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import os
import subprocess
import tempfile
import sys


# Loading the frozen selftest oracle must not create a live-tree __pycache__.
sys.dont_write_bytecode = True

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def decode(data):
    return json.loads(data, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON: ' + value)))


def string(value):
    return isinstance(value, str) and bool(value.strip())


def evaluate(bundle):
    if not isinstance(bundle, dict) or bundle.get('schema') != 'wave-accounting-v1':
        raise ValueError('unsupported bundle schema')
    waves = bundle.get('waves')
    if not isinstance(waves, list) or not waves:
        raise ValueError('waves must be a nonempty list')
    findings = []
    summaries = []
    wave_names = set()
    all_agents = set()

    def finding(code, wave, detail):
        findings.append({'id': code, 'wave': wave, 'detail': detail})

    for wave in waves:
        if not isinstance(wave, dict) or not string(wave.get('name')):
            raise ValueError('wave requires nonempty name')
        name = wave['name']
        if name in wave_names:
            finding('DUPLICATE_WAVE', name, name)
        wave_names.add(name)
        members, outcomes, reports = (wave.get(k) for k in ('members', 'outcomes', 'reports'))
        if not isinstance(members, list) or not members or not isinstance(outcomes, list) or not isinstance(reports, list):
            raise ValueError(name + ': invalid member/outcome/report lists')
        if not all(string(r) for r in reports) or len(set(reports)) != len(reports):
            raise ValueError(name + ': reports must be unique nonempty seat names')
        by_name = {}
        member_agents = set()
        for member in members:
            if not isinstance(member, dict) or not all(string(member.get(k)) for k in ('name', 'id', 'role')):
                raise ValueError(name + ': malformed member')
            seat, agent = member['name'], member['id']
            if seat in by_name:
                finding('DUPLICATE_MEMBER', name, seat)
            if agent in member_agents or agent in all_agents:
                finding('DUPLICATE_AGENT', name, agent)
            by_name[seat] = member
            member_agents.add(agent)
            all_agents.add(agent)
        seen = set()
        outcome_agents = set()
        completed = dead = 0
        partial = []
        for outcome in outcomes:
            if not isinstance(outcome, dict) or not all(string(outcome.get(k)) for k in ('name', 'id', 'role', 'status')):
                raise ValueError(name + ': malformed outcome')
            seat, agent = outcome['name'], outcome['id']
            if seat in seen:
                finding('DUPLICATE_OUTCOME', name, seat)
            seen.add(seat)
            if agent in outcome_agents:
                finding('DUPLICATE_AGENT', name, agent)
            outcome_agents.add(agent)
            member = by_name.get(seat)
            if member is not None and (agent != member['id'] or outcome['role'] != member['role']):
                finding('IDENTITY_MISMATCH', name, seat)
            if outcome.get('replaced') is not False:
                finding('REPLACEMENT_FORBIDDEN', name, seat)
            status = outcome['status']
            if status == 'completed':
                completed += 1
            elif status == 'failed':
                dead += 1
                if seat in reports:
                    partial.append(seat)
            else:
                finding('UNKNOWN_STATUS', name, seat + ':' + status)
        if seen != set(by_name):
            finding('MEMBERSHIP_MISMATCH', name, 'missing=' + repr(sorted(set(by_name) - seen)) + ' extra=' + repr(sorted(seen - set(by_name))))
        if not set(reports).issubset(by_name):
            finding('UNKNOWN_REPORT', name, repr(sorted(set(reports) - set(by_name))))
        summary = {'seats': len(members), 'completed': completed, 'dead': dead}
        claimed = wave.get('claimed')
        if not isinstance(claimed, dict) or set(claimed) != set(summary) or any(type(claimed[k]) is not int or claimed[k] < 0 for k in summary):
            raise ValueError(name + ': claimed totals require exactly three nonnegative integers')
        if claimed != summary:
            finding('TOTAL_MISMATCH', name, 'claimed=' + repr(claimed) + ' observed=' + repr(summary))
        summaries.append(dict(summary, name=name, report_artifacts=len(reports), failed_with_report=sorted(partial)))
    total = {k: sum(w[k] for w in summaries) for k in ('seats', 'completed', 'dead')}
    return {'schema': 'wave-accounting-result-v1', 'waves': summaries, 'total': total,
            'finding_ids': sorted({f['id'] for f in findings}), 'findings': findings,
            'authority': 'declared retained callbacks; report presence never completion; not provider authentication'}, 1 if findings else 0


def run(bundle_path, expected_path):
    try:
        data = bundle_path.read_bytes()
        expected = decode(expected_path.read_bytes())
        if not isinstance(expected, dict) or expected.get('schema') != 'wave-accounting-expected-v1':
            raise ValueError('unsupported expected schema')
        digest = expected.get('bundle_sha256')
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('expected requires lowercase SHA-256')
        if hashlib.sha256(data).hexdigest() != digest:
            return {'finding_ids': ['SNAPSHOT_TAMPERED'], 'error': 'bundle digest differs from persisted expected input'}, 2
        result, code = evaluate(decode(data))
        result['bundle_sha256'] = digest
        return result, code
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError) as exc:
        return {'finding_ids': ['INVALID_INPUT'], 'error': str(exc)}, 2


def selftest():
    # The original eight expectations remain frozen, independently of
    # evaluate(). Supplemental fixtures cover the other shipped guards.
    root = Path(__file__).resolve().parent.parent
    try:
        path = root / '.ufo/evidence/round-22/measure.py'
        spec = importlib.util.spec_from_file_location('round22_frozen_measure', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result, code = module.measure(root)
        cases = decode((root / '.ufo/evidence/round-22/accounting-extra-cases.json').read_bytes())['cases']
        outcomes = []
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        with tempfile.TemporaryDirectory(prefix='tameshi-r22-accounting-') as directory:
            work = Path(directory)
            for case in cases:
                raw = case['raw'].encode()
                (work / 'bundle.json').write_bytes(raw)
                (work / 'expected.json').write_text(json.dumps({
                    'schema': 'wave-accounting-expected-v1',
                    'bundle_sha256': hashlib.sha256(raw).hexdigest(),
                }))
                run = subprocess.run([
                    sys.executable, str(Path(__file__).resolve()),
                    '--bundle', str(work / 'bundle.json'),
                    '--expected', str(work / 'expected.json'), '--json',
                ], capture_output=True, text=True, env=env, timeout=15)
                observed = decode(run.stdout)
                ok = run.returncode == case['expected_exit']
                if case['expected_finding'] is None:
                    ok = ok and observed.get('finding_ids') == [] and observed.get('total') == {
                        'seats': 2, 'completed': 1, 'dead': 1}
                else:
                    ok = ok and case['expected_finding'] in observed.get('finding_ids', [])
                outcomes.append((case['name'], ok))
    except (OSError, ValueError, TypeError, KeyError, UnicodeError,
            RecursionError, subprocess.TimeoutExpired) as exc:
        print('FINDING: SELFTEST_UNAVAILABLE ' + str(exc))
        return 2
    for case in result.get('cases', []):
        print('ACCOUNTING_CASE ' + case['name'] + (' ok' if case['discriminated'] else ' FAIL'))
    print('ACCOUNTING_SELFTEST: ' + str(result['discriminated']) + '/8 pass')
    for name, ok in outcomes:
        print('ACCOUNTING_EXTRA_CASE ' + name + (' ok' if ok else ' FAIL'))
    good = sum(ok for _, ok in outcomes)
    print('ACCOUNTING_EXTRA_SELFTEST: ' + str(good) + '/' + str(len(cases)) + ' pass')
    code = code if code else (0 if good == len(cases) else 1)
    print('FINDING: ' + ('SELFTEST_PASS' if code == 0 else 'SELFTEST_FAIL'))
    return code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--bundle', type=Path)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        if args.bundle or args.expected or args.json:
            parser.print_usage(sys.stderr)
            return 64
        return selftest()
    if not args.bundle or not args.expected:
        parser.print_usage(sys.stderr)
        return 64
    result, code = run(args.bundle, args.expected)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print('WAVE_ACCOUNTING: ' + ('clean' if code == 0 else 'failed' if code == 1 else 'could-not-evaluate'))
        print('FINDINGS: ' + ','.join(result['finding_ids']))
        if 'total' in result:
            print(json.dumps(result['total'], sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
