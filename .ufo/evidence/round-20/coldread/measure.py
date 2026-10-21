#!/usr/bin/env python3
"""Select the round-20 ledger using the unchanged round-18 credit algorithm.

--selftest exercises this packaged selector in isolated synthetic repositories;
the frozen implementation's own suite remains separately registered.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
IMPLEMENTATION = ROOT / '.ufo/evidence/round-18/measure.py'
spec = importlib.util.spec_from_file_location('tameshi_round18_measure', IMPLEMENTATION)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
LEDGER = '.ufo/evidence/round-20/coldread/ledger.json'


def selftest():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1')
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r20-selector-', dir='/tmp') as tmp:
        repo = Path(tmp) / 'repo'
        repo.mkdir()
        env['HOME'] = tmp
        def git(*args):
            return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo),
                                   *args], env=env, capture_output=True, check=True).stdout
        def put(path, text):
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding='utf-8')
        git('init', '--quiet', '-b', 'master')
        put('tools/mutate-and-run.sh', module.RUNNER_TEXT)
        put('SKILL.md', '\n'.join(module.SKILL_LINES) + '\n')
        put('SHONEN.md', module.SHONEN_TEXT.replace(module.DEFAULT_LEDGER_PATH, LEDGER))
        put('corpus/SOURCES.md', module.SOURCES_TEXT)
        put(module.INPUT_FILE, module.INPUT_V1)
        put(module.TRACE_PATH, module.trace_receipt({module.INPUT_FILE: module.INPUT_V1_SHA}))
        put(LEDGER, module.ledger_json())
        put(module.DEFAULT_LEDGER_PATH, module.ledger_json())
        wrapper = '.ufo/evidence/round-20/coldread/measure.py'
        put(wrapper, Path(__file__).read_text(encoding='utf-8'))
        put('.ufo/evidence/round-18/measure.py', IMPLEMENTATION.read_text(encoding='utf-8'))
        def commit():
            git('add', '--all')
            git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                'commit', '--quiet', '-m', 'selector fixture')
            return git('rev-parse', 'HEAD').decode().strip()
        rev = commit()
        def invoke(*extra):
            return subprocess.run([sys.executable, str(repo / wrapper), '--rev', rev, *extra],
                                  cwd=tmp, env=env, capture_output=True, timeout=30)
        run = invoke('--repo', str(repo))
        result = json.loads(run.stdout)
        outcomes.append(('configured-default-ledger', run.returncode == 0
                         and result['coldread']['sections_covered'] == 4
                         and result['calibration_restraint_score'] == 8
                         and result['overrides_used'] is False and result['trace_gate'] == 'strict'))
        run = invoke()
        result = json.loads(run.stdout)
        outcomes.append(('relocated-package-default-repo', run.returncode == 0
                         and result['coldread']['sections_covered'] == 4))
        (repo / LEDGER).unlink()
        rev = commit()
        run = invoke('--repo', str(repo))
        result = json.loads(run.stdout)
        outcomes.append(('no-historical-ledger-fallback', run.returncode == 0
                         and result['coldread']['sections_covered'] == 0
                         and result['calibration_restraint_score'] == 6))
    for name, ok in outcomes:
        print('CASE', name, 'PASS' if ok else 'FAIL')
    passed = sum(ok for _, ok in outcomes)
    print(f'SELECTOR_SELFTEST: {passed}/{len(outcomes)} pass')
    return 0 if passed == len(outcomes) else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        sys.exit(selftest())
    module.DEFAULT_LEDGER_PATH = LEDGER
    module.LEDGER_PATH = LEDGER
    module.BOX3_LINK = LEDGER
    module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))
    sys.exit(module.main())
