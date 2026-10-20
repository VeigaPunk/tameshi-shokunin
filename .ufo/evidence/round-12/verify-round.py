#!/usr/bin/env python3
"""Round-12 reproducible evidence; all command outputs and expected exits retained."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / '.ufo/evidence/round-12'
checks = []

def run(name, argv, expected, token=None):
    result = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    out = result.stdout.decode('utf-8', 'replace')
    err = result.stderr.decode('utf-8', 'replace')
    good = result.returncode == expected and (token is None or token in out)
    checks.append(dict(name=name, argv=[str(x) for x in argv], expected_exit=expected,
                       required_stdout=token, observed_exit=result.returncode,
                       stdout=out, stderr=err, passed=good))
    print(f'{name}: exit={result.returncode} expected={expected} passed={good}', flush=True)
    with (EVIDENCE / 'verification-progress.json').open('w') as output:
        json.dump(checks, output, indent=2)
        output.write('\n')
    return good

with tempfile.TemporaryDirectory(prefix='tameshi-r12-integrated-') as tmp:
    scratch = Path(tmp)
    gate = ROOT / 'tools/repeat-control.py'
    control = EVIDENCE / 'ControlGate'
    run('repeat-control-selftest', [sys.executable, gate, '--selftest'], 0, 'SELFTEST: PASS')
    run('frozen-match', [sys.executable, gate, '--snapshot', control], 0, 'REPEAT_CONTROL: controls_match')
    run('frozen-mismatch', [sys.executable, gate, '--snapshot', control / 'mismatch'], 1, 'REPEAT_CONTROL: controls_mismatch')
    run('real-pristine-three-controls', [sys.executable, gate, '--runs', '3', '--out', scratch / 'real-controls', '--', 'env', '-u', 'THE_JANITOR_BIN', '-u', 'SQLITE3_BIN', '-u', 'CENSUS_BREAK', '-u', 'DEEP', 'bash', EVIDENCE / 'BashWitness/pristine.sh', '--selftest'], 0, 'REPEAT_CONTROL: controls_match')
    source = gate.read_text()
    old = 'for index in range(1, runs + 1):\n        record = run_once(command, index, out_dir)'
    assert source.count(old) == 1, 'single-control mutation anchor must be unique'
    mutant = scratch / 'single-control-mutant.py'
    mutant.write_text(source.replace(old, 'for index in range(1, 2):\n        record = run_once(command, index, out_dir)'))
    oracle = EVIDENCE / 'FailureOracle/verify_gate.py'
    fixture = scratch / 'changing-fixture.sh'
    fixture_source = (EVIDENCE / 'FailureOracle/fixture.sh').read_text()
    fixture.write_text(fixture_source.replace("printf 'CONTROL\\n'", "if [ \"$count\" -eq 1 ]; then printf 'CONTROL\\n'; else printf 'ALTERNATE\\n'; fi"))
    run('red-before-single-control-mutant', [sys.executable, oracle, '--gate', mutant, '--fixture', fixture, '--out', scratch / 'red-before', '--expect', 'controls_mismatch'], 1, 'VERDICT: FAIL')
    run('green-after-restored-repetition', [sys.executable, oracle, '--gate', gate, '--fixture', fixture, '--out', scratch / 'green-after', '--expect', 'controls_mismatch'], 0, 'VERDICT: PASS')
    checks[-2]['only_delta'] = checks[-1]['only_delta'] = old + ' -> for index in range(1, 2): (mutant only)'
    run('runner-selftest', ['bash', 'tools/mutate-and-run.sh', '--selftest'], 0, 'MUTATE_SELFTEST: 80/80 pass')
    run('runner-six-leg-regression', ['bash', 'tools/mutate-and-run.sh', '--regression'], 0, 'REGRESSION: PASS')
    run('witness-integrity', [sys.executable, 'tools/bash-witness-study.py', 'check'], 0)
    run('witness-count', [sys.executable, 'tools/bash-witness-study.py', 'count'], 0)
    copied = EVIDENCE / 'replayed-controls'
    if copied.exists():
        raise RuntimeError('Evidence destination exists; never overwrite prior replay')
    shutil.copytree(scratch / 'real-controls', copied)

payload = dict(checks=checks, passed=all(c['passed'] for c in checks),
               tool_sha256=hashlib.sha256(gate.read_bytes()).hexdigest(),
               source_scope='worktree content; exact measured commit recorded by subsequent measurement receipt')
destination = EVIDENCE / 'verification.json'
with destination.open('x') as output:
    json.dump(payload, output, indent=2)
    output.write('\n')
sys.exit(0 if payload['passed'] else 1)
