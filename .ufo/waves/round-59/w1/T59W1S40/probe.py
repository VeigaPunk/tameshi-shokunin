#!/usr/bin/env python3
"""Disposable Git-only closure-omission probe; no candidate implementation supplied."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

scratch = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S40')
report = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-59/w1/T59W1S40')
source = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-59')
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(TMPDIR=str(scratch/'tmp'), GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
repo = scratch/'fixture'
repo.mkdir()
records = []
def run(argv):
    p = subprocess.run(argv, cwd=scratch, env=env, text=True, capture_output=True, timeout=30)
    r = dict(argv=argv, exit=p.returncode, stdout=p.stdout, stderr=p.stderr)
    records.append(r)
    return r
def git(*args, mutation=False):
    if mutation:
        root = run(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'])
        assert root['exit'] == 0 and Path(root['stdout'].strip()).resolve() == repo.resolve(), root
    r = run(['git', '-C', str(repo), *args])
    assert r['exit'] == 0, r
    return r['stdout'].strip()
def commit(label):
    git('add', '--', 'tools/runner.py', 'tools/helper.py', mutation=True)
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', label, mutation=True)
    return git('rev-parse', 'HEAD')

try:
    # Initialization is the sole operation before a Git root exists.
    init = run(['git', '-C', str(repo), 'init', '-q'])
    assert init['exit'] == 0, init
    assert Path(git('rev-parse', '--show-toplevel')).resolve() == repo.resolve()
    tools = repo/'tools'
    tools.mkdir()
    runner = tools/'runner.py'
    helper = tools/'helper.py'
    runner.write_bytes(b'from helper import run\nrun()\n')
    original = b'def run():\n    print("real executor")\n'
    mutant = b'def run():\n    print("forged success")\n'
    helper.write_bytes(original)
    trusted = commit('trusted executor and helper')
    shutil.copyfile(source/'measure.py', scratch/'measure.py')
    results = []
    for state, content in [('pristine', original), ('mutated', mutant), ('restored', original)]:
        helper.write_bytes(content)
        candidate = trusted if state == 'pristine' else commit(state)
        declared = run(['git', '-C', str(repo), 'diff', '--quiet', trusted, candidate, '--', 'tools/runner.py'])
        complete = run(['git', '-C', str(repo), 'diff', '--quiet', trusted, candidate, '--', 'tools/runner.py', 'tools/helper.py'])
        counter = run([sys.executable, '-I', str(scratch/'measure.py'), '--lane', str(repo), '--rev', candidate, '--work', str(scratch/('counter-'+state))])
        results.append(dict(state=state, trusted=trusted, candidate=candidate,
            helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),
            runner_blob=git('rev-parse', candidate+':tools/runner.py'),
            helper_blob=git('rev-parse', candidate+':tools/helper.py'),
            tree=git('rev-parse', candidate+'^{tree}'), declared_detector=declared,
            complete_detector=complete, frozen_counter=counter))
    assert helper.read_bytes() == original
    assert results[0]['tree'] == results[2]['tree']
    payload = dict(seat='T59W1S40', axes=['claim fidelity', 'omission observability', 'exact restoration', 'operability'],
        implementation_observed=False, mutant='Change only omitted tools/helper.py output literal in committed source',
        expected_detector='Declared-path Git diff cannot detect omitted helper; complete-path Git diff must exit 1',
        results=results, commands=records,
        verdict='survived declared-path Git detector; killed complete-closure Git detector; actual gate/counter implementation probe inconclusive (tool absent)',
        boundary='Closure omission is outside frozen claim: verifier supplies complete closure.',
        installs=[], restoration=dict(exact_helper_bytes=True, identical_tree=True,
            before_sha256=results[0]['helper_sha256'], after_sha256=results[2]['helper_sha256']))
    (report/'receipts.json').write_text(json.dumps(payload, indent=2)+'\n')
    print(json.dumps(payload, indent=2))
finally:
    # Exact restoration is attempted even on failure; receipts copied before deletion on success.
    if 'helper' in globals() and helper.parent.exists():
        helper.write_bytes(original)
    shutil.rmtree(scratch)
