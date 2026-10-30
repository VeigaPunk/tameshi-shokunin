import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S31')
report = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-59/w1/T59W1S31')
os.environ['TMPDIR'] = str(root)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
for key in list(os.environ):
    if key.startswith('GIT_'):
        del os.environ[key]
os.environ.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
repo = root / 'fixture'
gate = root / 'gate.py'

def run(cmd):
    p = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=30)
    return {'command': cmd, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

def git(*args, mutate=False):
    if mutate:
        check = run(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'])
        assert check['exit'] == 0 and check['stdout'].strip() == str(repo), check
    result = run(['git', '-C', str(repo), *args])
    assert result['exit'] == 0, result
    return result['stdout'].strip()

phase = sys.argv[1]
if phase == 'pristine':
    repo.mkdir()
    assert run(['git', '-C', str(repo), 'init', '-q'])['exit'] == 0
    assert git('rev-parse', '--show-toplevel') == str(repo)
    (repo/'tools').mkdir()
    for name in ('good.py', 'drift.py'):
        (repo/'tools'/name).write_text('print("trusted")\n')
    git('add', '--', 'tools', mutate=True)
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'trusted', mutate=True)
    trusted = git('rev-parse', 'HEAD')
    (repo/'tools/drift.py').write_text('print("changed")\n')
    git('add', '--', 'tools/drift.py', mutate=True)
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'changed', mutate=True)
    (root/'revisions.json').write_text(json.dumps({'trusted': trusted, 'candidate': git('rev-parse', 'HEAD')}))
    shutil.copyfile(gate, root/'gate.original.py')
    shutil.copyfile('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-59/measure.py', root/'measure.py')
revs = json.loads((root/'revisions.json').read_text())
work = root / ('counter-' + phase)
command = ['python3', '-I', str(root/'measure.py'), '--lane', str(repo), '--rev', revs['trusted'], '--work', str(work), '--tool', str(gate)]
result = {'phase': phase, 'gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(), 'counter_sha256': hashlib.sha256((root/'measure.py').read_bytes()).hexdigest(), 'revisions': revs, 'frozen': run(command), 'cases': []}
for paths, expected in [(['tools/good.py', 'tools/good.py'], 0), (['tools/good.py', 'tools/good.py', 'tools/drift.py'], 1), (['tools/good.py', 'tools/drift.py'], 1), (['tools/drift.py', 'tools/good.py', 'tools/good.py'], 1)]:
    command = ['python3', '-I', str(gate), '--repo', str(repo), '--trusted', revs['trusted'], '--candidate', revs['candidate']]
    for path in paths:
        command += ['--path', path]
    observed = run(command)
    observed.update(expected=expected, ok=observed['exit'] == expected)
    result['cases'].append(observed)
(report/(phase+'.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'phase': phase, 'sha256': result['gate_sha256'], 'frozen_exit': result['frozen']['exit'], 'frozen_summary': result['frozen']['stdout'].splitlines()[-1:] ,'cases': [{'exit': x['exit'], 'expected': x['expected'], 'stdout': x['stdout']} for x in result['cases']]}, indent=2))
