#!/usr/bin/env python3
"""Replicate frozen measure.py fixture construction for PATHS[2]='tools/日本語.py' only.

Mirrors measure.py exactly: same env scrub (strip GIT_*, GIT_CONFIG_GLOBAL=/dev/null,
GIT_CONFIG_NOSYSTEM=1, PYTHONDONTWRITEBYTECODE, TMPDIR), same commit sequence, same
author/committer, same file contents. Fixture is KEPT for object-level inspection
(measure.py deletes its --work dir in a finally block; we retain ours for probing).
"""
import json
import os
from pathlib import Path
import subprocess
import sys

SEAT = os.environ["TSEAT"]
WORK = Path(f"/fast/scratch/hyaku/tameshi-r59/{SEAT}")
PATH = 'tools/日本語.py'

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(WORK))

def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)} -> {r.returncode}: {r.stderr}")
    return r.stdout.strip()

def main():
    repo = WORK / 'fixture-2'
    if repo.exists():
        raise SystemExit(f"fixture dir already exists: {repo}")
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    top = Path(git(repo, 'rev-parse', '--show-toplevel')).resolve()
    assert top == repo.resolve(), f"fixture root mismatch: {top} != {repo.resolve()}"
    f = repo / PATH
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', PATH)
    def commit():
        git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        return git(repo, 'rev-parse', 'HEAD')
    versions = {'equal': commit()}
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', PATH)
    versions['changed'] = commit()
    f.unlink()
    git(repo, 'add', '-u')
    versions['missing'] = commit()
    f.write_text('print("real executor")\n')
    (repo / 'unrelated.txt').write_text('unrelated change\n')
    git(repo, 'add', '--', PATH, 'unrelated.txt')
    versions['unrelated'] = commit()
    versions['unresolvable'] = '0' * 40
    f.unlink()
    f.symlink_to('elsewhere.py')
    git(repo, 'add', '--', PATH)
    versions['symlink'] = commit()
    (WORK / 'versions.json').write_text(json.dumps({'path': PATH, 'versions': versions}, indent=1))
    print(json.dumps({'path': PATH, 'versions': versions}, indent=1))
    # Final worktree state (what measure.py leaves in place while running all probes):
    print("final worktree entry:", git(repo, 'status', '--porcelain', '--', PATH))
    print("final HEAD:", git(repo, 'rev-parse', 'HEAD'), "(symlink commit)")

if __name__ == '__main__':
    sys.exit(main())
