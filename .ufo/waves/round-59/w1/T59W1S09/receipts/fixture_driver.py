#!/usr/bin/env python3
"""T59W1S09 independent fixture construction for cell path tools/space name.py.

Mirrors frozen measure.py construction exactly (same contents, same git add
forms, same commit identity flags, same env scrubbing) for PATHS[1] only.
Writes scratch/versions.json with trusted + all six candidate commits.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

SCRATCH = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S09').resolve()
REPO = SCRATCH / 'fixture-1'
PATH = 'tools/space name.py'

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SCRATCH / 'tmp'))
(SCRATCH / 'tmp').mkdir(parents=True, exist_ok=True)

def run(argv):
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(f'git {" ".join(args)} failed: {r.stderr}')
    return r.stdout.strip()

if REPO.exists():
    import shutil
    shutil.rmtree(REPO)
REPO.mkdir(parents=True)
git(REPO, 'init', '-q')
top = Path(git(REPO, 'rev-parse', '--show-toplevel')).resolve()
assert top == REPO, f'fixture root mismatch: {top} != {REPO}'

f = REPO / PATH
f.parent.mkdir(parents=True, exist_ok=True)
f.write_text('print("real executor")\n')
git(REPO, 'add', '--', PATH)

def commit():
    git(REPO, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
    return git(REPO, 'rev-parse', 'HEAD')

trusted = commit()
versions = {'equal': trusted}
f.write_text('print("forged success")\n')
git(REPO, 'add', '--', PATH)
versions['changed'] = commit()
f.unlink()
git(REPO, 'add', '-u')
versions['missing'] = commit()
f.write_text('print("real executor")\n')
(REPO / 'unrelated.txt').write_text('unrelated change\n')
git(REPO, 'add', '--', PATH, 'unrelated.txt')
versions['unrelated'] = commit()
versions['unresolvable'] = '0' * 40
f.unlink()
f.symlink_to('elsewhere.py')
git(REPO, 'add', '--', PATH)
versions['symlink'] = commit()

out = {'path': PATH, 'repo': str(REPO), 'trusted': trusted, 'versions': versions}
(SCRATCH / 'versions.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
