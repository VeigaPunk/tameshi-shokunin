#!/usr/bin/env python3
"""Round-25 C1 suite for tools/mutate-and-run.sh (--suite runs it with $MUTANT set).

  c1-suite.py multitoken MUTANT   ruler-owned multi-token stdout fixtures
                                  (multitoken-cases.json next to this file) run
                                  through MUTANT's public CLI; prints one
                                  `FIXTURE <name> PASS|FAIL` line per case.
  c1-suite.py selftest MUTANT     MUTANT's own --selftest, staged in a private
                                  tree that carries the round-23/24 fixture files
                                  the selftest loads relative to its own path.

Exit: 0 every case passed · 1 at least one explicit FAIL · 3 setup error (no
fixture verdict). The lane runner counts any nonzero exit as KILLED; the C1
measure therefore credits a kill only when the evidence log holds an explicit
FAIL witness line, never for exit 3 alone.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def bundle_for(case, revision, cwd):
    requirements, receipts = [], []
    for name, tokens, stdout in case['requirements']:
        argv = ['gate', '--check', name]
        requirements.append({'name': name, 'argv': argv,
                             'expect': {'exit': 0, 'stdout_contains': tokens}})
        receipts.append({'name': name, 'argv': argv, 'cwd': cwd, 'revision': revision,
                         'exit': 0, 'stdout': stdout, 'stderr': ''})
    return {'schema': 'command-binding-v1', 'revision': revision, 'cwd': cwd,
            'requirements': requirements, 'receipts': receipts}


def multitoken(mutant):
    try:
        spec = json.loads((HERE / 'multitoken-cases.json').read_text())
        cases = spec['cases']
        if spec.get('schema') != 'tameshi-r25-multitoken-cases-v1' or not cases:
            raise ValueError('bad fixture schema')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('MULTITOKEN_SUITE: setup (%s)' % exc)
        return 3
    passed = 0
    with tempfile.TemporaryDirectory(prefix='tameshi-r25-mt-') as tmp:
        bundle_path, expected_path = Path(tmp) / 'bundle.json', Path(tmp) / 'expected.json'
        for case in cases:
            raw = (json.dumps(bundle_for(case, spec['revision'], spec['cwd']), sort_keys=True) + '\n').encode()
            bundle_path.write_bytes(raw)
            expected_path.write_text(json.dumps({'schema': 'command-binding-expected-v1',
                                                 'bundle_sha256': hashlib.sha256(raw).hexdigest()}))
            run = subprocess.run([sys.executable, mutant, '--bundle', str(bundle_path),
                                  '--expected', str(expected_path), '--json'],
                                 capture_output=True, text=True, timeout=30)
            try:
                value = json.loads(run.stdout)
            except ValueError:
                value = {}
            ok = run.returncode == case['expected_exit'] and value.get('finding_ids') == case['finding_ids']
            passed += ok
            print('FIXTURE %s %s (exit=%s findings=%s)' % (case['name'], 'PASS' if ok else 'FAIL',
                                                         run.returncode, value.get('finding_ids')))
    print('MULTITOKEN_SUITE: %d/%d pass' % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def selftest(mutant):
    with tempfile.TemporaryDirectory(prefix='tameshi-r25-st-') as tmp:
        root = Path(tmp)
        (root / 'tools').mkdir()
        shutil.copyfile(mutant, root / 'tools/command-binding.py')
        for rnd in ('round-23', 'round-24'):
            src = REPO / '.ufo/evidence' / rnd / 'extra-cases.json'
            if not src.is_file():
                print('GUARD_SUITE: setup (missing %s)' % src)
                return 3
            (root / '.ufo/evidence' / rnd).mkdir(parents=True)
            shutil.copyfile(src, root / '.ufo/evidence' / rnd / 'extra-cases.json')
        run = subprocess.run([sys.executable, str(root / 'tools/command-binding.py'), '--selftest'],
                             capture_output=True, text=True, timeout=300)
        sys.stdout.write(run.stdout)
        if run.returncode == 0:
            return 0
        return 1 if ' FAIL' in run.stdout else 3


def main(argv):
    if len(argv) != 3 or argv[1] not in ('multitoken', 'selftest'):
        print('usage: c1-suite.py multitoken|selftest MUTANT', file=sys.stderr)
        return 64
    return (multitoken if argv[1] == 'multitoken' else selftest)(argv[2])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
