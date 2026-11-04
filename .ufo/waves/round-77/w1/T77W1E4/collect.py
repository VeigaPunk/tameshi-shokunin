import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

L = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
B = 'ac6baf7a46df613b171b4c1ab834c888cd6321b9'
R = L / '.ufo/waves/round-77/w1/T77W1E4'
S = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'tameshi-r77/T77W1E4'
S.mkdir(parents=True, exist_ok=True)
(S / 'tmp').mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(S / 'tmp'), PYTHONDONTWRITEBYTECODE='1')

def git(*args):
    return subprocess.check_output(['git', '-C', str(L), *args])

def run(argv, cwd):
    p = subprocess.run(argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return '$ ' + shlex.join(argv) + '\nCWD=' + str(cwd) + '\nTMPDIR=' + env['TMPDIR'] + '\n' + p.stdout + p.stderr + 'EXIT=' + str(p.returncode) + '\n'

try:
    clone = S / 'base'
    setup = run(['git', 'clone', '--shared', '--no-checkout', str(L), str(clone)], S)
    top = subprocess.check_output(['git', '-C', str(clone), 'rev-parse', '--show-toplevel'], text=True).strip()
    assert top == str(clone), (top, str(clone))
    setup += 'TOPLEVEL_ASSERT=' + top + '\n'
    setup += run(['git', '-C', str(clone), 'checkout', '--detach', B], S)
    actual = subprocess.check_output(['git', '-C', str(clone), 'rev-parse', 'HEAD'], text=True).strip()
    assert actual == B
    (R / 'setup.txt').write_text(setup)
    def sweeps():
        out = 'REV=' + B + '\n'
        for tool in ['wave-reconcile.py', 'selfstate-freshness.py']:
            out += 'TOOL=' + 'tools/' + tool + ' SHA256=' + hashlib.sha256((clone / 'tools' / tool).read_bytes()).hexdigest() + '\n'
        out += run(['python3', '-I', '-X', 'utf8', 'tools/wave-reconcile.py', '--repo', '.', '--extra-root', 'fleet=/home/vgpnk/Projects/shokunin', '--manifest', 'tools/wave-reconcile.json'], clone)
        out += run(['python3', '-I', '-X', 'utf8', 'tools/selfstate-freshness.py', '--repo', '.', '--manifest', 'tools/selfstate-freshness.json'], clone)
        (R / 'standing-sweeps.txt').write_text(out)
        return out
    def mechanical():
        out = 'REV=' + B + '\n'
        for revision_range in ['451ed5cb..d2d00e3f', '5b7bbe1a..d2d00e3f', '451ed5cb^..d2d00e3f']:
            out += run(['git', '-C', str(L), 'rev-list', '--count', revision_range], L)
        paths = git('ls-tree', '-r', '--name-only', B, '--', 'tools').decode().splitlines()
        population = sorted(p for p in paths if p.endswith(('.py', '.sh')) and b'--selftest' in git('show', B + ':' + p))
        registry = json.loads(git('show', B + ':tools/registry.json'))
        registered = {a for row in registry['rows'] for a in row.get('argv', []) if a in paths}
        missing = sorted(set(population) - registered)
        out += 'CENSUS_RULE=tracked tools/**/*.py or tools/**/*.sh with literal --selftest; registry membership is exact path in any row.argv (all statuses)\n'
        out += f'SELFTEST_TOOLS={len(population)} REGISTERED={len(set(population) & registered)} MISSING={len(missing)}\n'
        out += 'POPULATION\n' + '\n'.join(population) + '\nMISSING_PATHS\n' + '\n'.join(missing) + '\n'
        out += 'ALL_SUFFIX_LITERAL_COUNT=' + str(sum(b'--selftest' in git('show', B + ':' + p) for p in paths)) + '\n'
        for p in ['.ufo/evidence/round-76/c1-landed-selftest-wr.txt', '.ufo/evidence/round-76/c1-landed-selftest-ss.txt']:
            data = git('show', B + ':' + p)
            out += '$ git -C ' + str(L) + ' show ' + B + ':' + p + '\n' + data.decode()
            out += 'RECEIPT_SHA256=' + hashlib.sha256(data).hexdigest() + '\n'
        (R / 'mechanical.txt').write_text(out)
        return out
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(sweeps), pool.submit(mechanical)]
        for f in futures:
            print(f.result(), end='')
finally:
    shutil.rmtree(S)
    print('SCRATCH_REMOVED=' + str(S))
