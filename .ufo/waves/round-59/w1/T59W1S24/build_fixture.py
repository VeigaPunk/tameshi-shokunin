#!/usr/bin/env python3
"""Independent scratch fixture for T59W1S24 cell: path tools/-runner.py, class symlink.
Replicates measure.py fixture construction for PATHS[3] only, with the same
env sanitization (no GIT_*, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1).
Prints the six class -> commit map as JSON for downstream oracle probing.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

SEAT = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S24')
REPO = SEAT / 'fixture'
PATH = 'tools/-runner.py'

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SEAT))

def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(f'git {" ".join(args)} -> rc={r.returncode}: {r.stderr}')
    return r.stdout.strip()

def main():
    if REPO.exists():
        import shutil; shutil.rmtree(REPO)
    REPO.mkdir(parents=True)
    git(REPO, 'init', '-q')
    top = Path(git(REPO, 'rev-parse', '--show-toplevel')).resolve()
    assert top == REPO.resolve(), f'fixture root mismatch: {top} != {REPO.resolve()}'

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

    print(json.dumps({'repo': str(REPO), 'path': PATH, 'trusted': trusted,
                      'versions': versions}, indent=1))

if __name__ == '__main__':
    sys.exit(main())
