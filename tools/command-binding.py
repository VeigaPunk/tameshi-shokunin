#!/usr/bin/env python3
"""Validate declared required-command receipts against a digest-pinned bundle.

python3 tools/command-binding.py --bundle BUNDLE --expected EXPECTED --json
python3 tools/command-binding.py --selftest

A bundle declares a finite nonempty requirement set and receipts. Exact name,
argv (no shell normalization), canonical absolute cwd, full revision, integer
exit and required stdout tokens must match. Expected nonzero child exits are
valid. Source-read counts, held flags and filenames never establish execution.
The expected file is the trusted caller-owned commitment: it pins all bundle
bytes. This validates retained declarations, not their producer authenticity,
continuous checkout identity, complete page coverage or independent cold reads.

0 clean; 1 failed binding/outcome; 2 could-not-evaluate (shape or integrity);
64 usage. Read-only except isolated public selftest scratch. Owner: tameshi.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SCHEMA = 'command-binding-v1'
EXPECTED = 'command-binding-expected-v1'
REVISION = re.compile(r'^[0-9a-f]{40}$')
SHA256 = re.compile(r'^[0-9a-f]{64}$')

class Invalid(ValueError):
    pass

class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, '%s: error: %s\n' % (self.prog, message))

def unique_pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise Invalid('duplicate JSON key: ' + key)
        value[key] = item
    return value

def decode(raw):
    return json.loads(raw, object_pairs_hook=unique_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(Invalid('nonfinite JSON')))

def strings(value, nonempty=False):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(isinstance(item, str) and bool(item) and '\x00' not in item for item in value))

def canonical_cwd(value):
    return (isinstance(value, str) and value.startswith('/') and '\x00' not in value
            and not value.startswith('//') and os.path.normpath(value) == value)

def revision(value):
    return isinstance(value, str) and REVISION.fullmatch(value) is not None

def evaluate(bundle):
    """Return stable finding IDs; invalid shapes never become mismatch passes."""
    if (not isinstance(bundle, dict) or bundle.get('schema') != SCHEMA
            or set(bundle) != {'schema', 'revision', 'cwd', 'requirements', 'receipts'}
            or not revision(bundle.get('revision')) or not canonical_cwd(bundle.get('cwd'))
            or not isinstance(bundle.get('requirements'), list) or not bundle['requirements']
            or not isinstance(bundle.get('receipts'), list)):
        return 2, ['INVALID_BUNDLE']
    requirements = {}
    for row in bundle['requirements']:
        if (not isinstance(row, dict) or not isinstance(row.get('name'), str) or not row['name']
                or set(row) != {'name', 'argv', 'expect'}
                or not strings(row.get('argv'), True) or not isinstance(row.get('expect'), dict)
                or not {'exit'} <= set(row['expect']) <= {'exit', 'stdout_contains'}
                or type(row['expect'].get('exit')) is not int
                or not strings(row['expect'].get('stdout_contains', []))):
            return 2, ['INVALID_REQUIREMENT']
        if row['name'] in requirements:
            return 2, ['DUPLICATE_REQUIREMENT']
        requirements[row['name']] = row
    receipts = {}
    for row in bundle['receipts']:
        if (not isinstance(row, dict) or not isinstance(row.get('name'), str) or not row['name']
                or set(row) != {'name', 'argv', 'cwd', 'revision', 'exit', 'stdout', 'stderr'}
                or not strings(row.get('argv'), True) or not canonical_cwd(row.get('cwd'))
                or not revision(row.get('revision')) or type(row.get('exit')) is not int
                or not isinstance(row.get('stdout'), str) or not isinstance(row.get('stderr'), str)):
            return 2, ['INVALID_RECEIPT']
    # Complete structural validation before any semantic duplicate failure.
    for row in bundle['receipts']:
        if row['name'] in receipts:
            return 1, ['DUPLICATE_COMMAND']
        receipts[row['name']] = row
    findings = set()
    if set(receipts) != set(requirements):
        findings.add('MEMBERSHIP_MISMATCH')
    for name in sorted(set(receipts) & set(requirements)):
        receipt, required = receipts[name], requirements[name]
        if receipt['argv'] != required['argv']:
            findings.add('ARGV_MISMATCH')
        if receipt['cwd'] != bundle['cwd']:
            findings.add('CWD_MISMATCH')
        if receipt['revision'] != bundle['revision']:
            findings.add('REVISION_MISMATCH')
        if receipt['exit'] != required['expect']['exit']:
            findings.add('EXIT_MISMATCH')
        if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):
            findings.add('STDOUT_MISMATCH')
    return (1 if findings else 0), sorted(findings)

def check(bundle_path, expected_path):
    try:
        raw = Path(bundle_path).read_bytes()
        expected = decode(Path(expected_path).read_bytes())
        if (not isinstance(expected, dict) or expected.get('schema') != EXPECTED
                or set(expected) != {'schema', 'bundle_sha256'}
                or not isinstance(expected.get('bundle_sha256'), str)
                or SHA256.fullmatch(expected['bundle_sha256']) is None):
            return 2, ['INVALID_EXPECTED'], None
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected['bundle_sha256']:
            return 2, ['SNAPSHOT_TAMPERED'], digest
        code, findings = evaluate(decode(raw))
        return code, findings, digest
    except (OSError, ValueError, RecursionError, UnicodeError) as exc:
        return 2, ['INVALID_INPUT'], None

def selftest():
    """Public CLI tests; literal expected outcomes are independent of evaluate."""
    base = {'schema': SCHEMA, 'revision': '1' * 40, 'cwd': '/fixture/repo',
            'requirements': [{'name': 'clean', 'argv': ['gate', '--check'],
                              'expect': {'exit': 0, 'stdout_contains': ['CLEAN']}},
                             {'name': 'red', 'argv': ['gate', '--bad'],
                              'expect': {'exit': 1, 'stdout_contains': ['REJECT']}}],
            'receipts': [{'name': 'clean', 'argv': ['gate', '--check'], 'cwd': '/fixture/repo',
                          'revision': '1' * 40, 'exit': 0, 'stdout': 'CLEAN\n', 'stderr': ''},
                         {'name': 'red', 'argv': ['gate', '--bad'], 'cwd': '/fixture/repo',
                          'revision': '1' * 40, 'exit': 1, 'stdout': 'REJECT\n', 'stderr': ''}]}
    cases = [('clean-with-expected-red', base, 0, [])]
    def changed(name, edit, code, finding):
        bundle = copy.deepcopy(base)
        edit(bundle)
        cases.append((name, bundle, code, [finding]))
    changed('source-read-not-command', lambda b: b['receipts'][0].update(argv=['cat', 'gate']), 1, 'ARGV_MISMATCH')
    changed('wrong-cwd', lambda b: b['receipts'][0].update(cwd='/other'), 1, 'CWD_MISMATCH')
    changed('stale-revision', lambda b: b['receipts'][0].update(revision='2' * 40), 1, 'REVISION_MISMATCH')
    changed('missing', lambda b: b['receipts'].pop(), 1, 'MEMBERSHIP_MISMATCH')
    changed('duplicate', lambda b: b['receipts'].append(copy.deepcopy(b['receipts'][0])), 1, 'DUPLICATE_COMMAND')
    changed('unknown', lambda b: b['receipts'][0].update(name='other'), 1, 'MEMBERSHIP_MISMATCH')
    changed('wrong-exit', lambda b: b['receipts'][0].update(exit=1), 1, 'EXIT_MISMATCH')
    changed('stderr-cannot-supply-token', lambda b: b['receipts'][0].update(stdout='', stderr='CLEAN'), 1, 'STDOUT_MISMATCH')
    changed('bool-exit', lambda b: b['receipts'][0].update(exit=False), 2, 'INVALID_RECEIPT')
    changed('empty-requirements', lambda b: b.update(requirements=[]), 2, 'INVALID_BUNDLE')
    changed('duplicate-requirement', lambda b: b['requirements'].append(copy.deepcopy(b['requirements'][0])), 2, 'DUPLICATE_REQUIREMENT')
    changed('noncanonical-cwd', lambda b: b.update(cwd='/fixture/../repo'), 2, 'INVALID_BUNDLE')
    changed('short-revision', lambda b: b.update(revision='1234567'), 2, 'INVALID_BUNDLE')
    changed('string-exit', lambda b: b['receipts'][0].update(exit='0'), 2, 'INVALID_RECEIPT')
    changed('bool-expected-exit', lambda b: b['requirements'][0]['expect'].update(exit=False), 2, 'INVALID_REQUIREMENT')
    changed('blank-argv', lambda b: b['requirements'][0].update(argv=[]), 2, 'INVALID_REQUIREMENT')
    fixtures = Path(__file__).resolve().parents[1] / '.ufo/evidence/round-23/extra-cases.json'
    try:
        supplemental = decode(fixtures.read_bytes())['cases']
        cases.extend((row['name'], row['bundle'], row['expected_exit'], row['finding_ids'])
                     for row in supplemental)
    except (OSError, ValueError, KeyError, TypeError):
        print('COMMAND_BINDING_SELFTEST: fixture-unavailable')
        return 1
    passed = 0
    with tempfile.TemporaryDirectory(prefix='tameshi-command-binding-') as tmp:
        bundle_path, expected_path = Path(tmp) / 'bundle.json', Path(tmp) / 'expected.json'
        for name, bundle, code, findings in cases + [('tampered', base, 2, ['SNAPSHOT_TAMPERED']),
                                                     ('duplicate-json-key', base, 2, ['INVALID_INPUT'])]:
            raw = (json.dumps(bundle, sort_keys=True) + '\n').encode()
            if name == 'duplicate-json-key':
                raw = raw.replace(b'"schema":', b'"schema":"ignored","schema":', 1)
            digest = hashlib.sha256(raw).hexdigest()
            expected_path.write_text(json.dumps({'schema': EXPECTED, 'bundle_sha256': digest}))
            bundle_path.write_bytes(raw + (b' ' if name == 'tampered' else b''))
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--bundle', str(bundle_path),
                                  '--expected', str(expected_path), '--json'], capture_output=True, text=True, timeout=15)
            try:
                value = json.loads(run.stdout)
            except ValueError:
                value = {}
            ok = run.returncode == code and value.get('finding_ids') == findings
            passed += ok
            print('CASE', name, 'PASS' if ok else 'FAIL')
    print('COMMAND_BINDING_SELFTEST: %d/%d pass' % (passed, len(cases) + 2))
    return 0 if passed == len(cases) + 2 else 1

def main():
    parser = Parser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--bundle')
    parser.add_argument('--expected')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        if args.bundle or args.expected or args.json:
            parser.error('--selftest takes no other arguments')
        return selftest()
    if not args.bundle or not args.expected:
        parser.error('--bundle and --expected are required')
    code, findings, digest = check(args.bundle, args.expected)
    value = {'schema': 'command-binding-report-v1', 'exit': code, 'finding_ids': findings,
             'bundle_sha256': digest}
    if args.json:
        print(json.dumps(value, sort_keys=True))
    else:
        print('COMMAND_BINDING:', 'CLEAN' if code == 0 else 'FAILED' if code == 1 else 'COULD_NOT_EVALUATE',
              ','.join(findings) or 'none')
    return code

if __name__ == '__main__':
    raise SystemExit(main())
