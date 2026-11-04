import hashlib
import json
from pathlib import Path
import subprocess

L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
B = 'ac6baf7a46df613b171b4c1ab834c888cd6321b9'
R = Path(L) / '.ufo/waves/round-77/w1/T77W1E4'
def git(*args):
    return subprocess.check_output(['git', '-C', L, *args])
paths = git('ls-tree', '-r', '--name-only', B, '--', 'tools').decode().splitlines()
registry = json.loads(git('show', B + ':tools/registry.json'))
registered = {a for row in registry['rows'] for a in row.get('argv', [])}
population = sorted(p for p in paths if p.endswith('.py') and b'--selftest' in git('show', B + ':' + p))
missing = sorted(set(population) - registered)
lines = ['REV=' + B, 'CENSUS_RULE=tracked tools/**/*.py containing literal --selftest; exact path in any registry row.argv, all statuses', f'SELFTEST_PYTHON_TOOLS={len(population)} REGISTERED={len(set(population) & registered)} MISSING={len(missing)}', 'MISSING_PATHS', *missing]
for p in ['tools/mutate-and-run.sh']:
    lines.append('SHELL_ADDITION=' + p + ' REGISTERED=' + str(p in registered))
for rev in ['451ed5cb', '5b7bbe1a^', '5b7bbe1a']:
    lines.extend(['$ git -C ' + L + ' rev-parse ' + rev, git('rev-parse', rev).decode().strip()])
lines.extend(['$ git -C ' + L + " rev-list --count '5b7bbe1a^..d2d00e3f'", git('rev-list', '--count', '5b7bbe1a^..d2d00e3f').decode().strip()])
for p in ['tools/wave-reconcile.py', 'tools/selfstate-freshness.py']:
    lines.append('HEADER_EXAMPLE REV=' + B + ' TOOL=' + p + ' SHA256=' + hashlib.sha256(git('show', B + ':' + p)).hexdigest())
out = '\n'.join(lines) + '\n'
(R / 'census-clarification.txt').write_text(out)
print(out, end='')
