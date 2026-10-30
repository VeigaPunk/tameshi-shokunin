#!/usr/bin/env python3
"""Independent fixture builder for round-59 cell path='tools/-runner.py'.

Mirrors the frozen counter (.ufo/evidence/round-59/measure.py) construction
exactly, restricted to the one assigned path. Builds six candidate revisions:
equal, changed, missing, unrelated, (unresolvable is a synthetic '0'*40), symlink.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

PATH = 'tools/-runner.py'
WORK = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S22')
REPO = WORK / 'fixture-s22'

def base_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(WORK))
    return env

def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=base_env(), timeout=30, **kw)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr}")
    return r.stdout.strip()

def main():
    if REPO.exists():
        import shutil; shutil.rmtree(REPO)
    REPO.mkdir(parents=True)
    top = Path(git(REPO, 'init', '-q') or REPO)  # init prints nothing with -q
    toplevel = Path(git(REPO, 'rev-parse', '--show-toplevel')).resolve()
    assert toplevel == REPO.resolve(), f'fixture root mismatch: {toplevel} != {REPO.resolve()}'
    print(f'toplevel-ok: {toplevel}')

    f = REPO / PATH
    f.parent.mkdir(parents=True, exist_ok=True)

    f.write_text('print("real executor")\n')
    git(REPO, 'add', '--', PATH)
    def commit():
        git(REPO, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        return git(REPO, 'rev-parse', 'HEAD')
    trusted = commit()
    print(f'trusted      {trusted}')

    f.write_text('print("forged success")\n')
    git(REPO, 'add', '--', PATH)
    changed = commit()
    print(f'changed      {changed}')

    f.unlink()
    git(REPO, 'add', '-u')
    missing = commit()
    print(f'missing      {missing}')

    f.write_text('print("real executor")\n')
    (REPO / 'unrelated.txt').write_text('unrelated change\n')
    git(REPO, 'add', '--', PATH, 'unrelated.txt')
    unrelated = commit()
    print(f'unrelated    {unrelated}')

    unresolvable = '0' * 40
    print(f'unresolvable {unresolvable} (synthetic, no commit)')

    f.unlink()
    f.symlink_to('elsewhere.py')
    git(REPO, 'add', '--', PATH)
    symlink = commit()
    print(f'symlink      {symlink}')

    versions = {'equal': trusted, 'changed': changed, 'missing': missing,
                'unrelated': unrelated, 'unresolvable': unresolvable, 'symlink': symlink}
    (WORK / 'versions.json').write_text(json.dumps({'trusted': trusted, 'versions': versions}, indent=1))
    print('wrote versions.json')

if __name__ == '__main__':
    sys.exit(main())
