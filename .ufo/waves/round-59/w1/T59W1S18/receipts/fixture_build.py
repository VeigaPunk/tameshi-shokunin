#!/usr/bin/env python3
"""Independent fixture builder for round-59 cell: path 'tools/日本語.py' (PATHS index 2).

Mirrors frozen measure.py fixture construction exactly, for this one path only.
Emits per-version Git object inspection (type/mode/content) as JSON for oracle checks.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

PATH = 'tools/日本語.py'  # PATHS[2] in frozen measure.py
WORK = Path(os.environ['PROBE_WORK'])

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(WORK))

def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(f'git {" ".join(args)}: {r.stderr}')
    return r.stdout.strip()

def inspect(repo, commit, path):
    """Return dict describing the git source-object for path at commit."""
    out = git(repo, 'ls-tree', commit, '--', path)
    rec = {'raw': out}
    if out:
        meta, name = out.split('\t', 1)
        mode, typ, oid = meta.split()
        rec.update(mode=mode, type=typ, oid=oid, name=name)
        if typ == 'blob':
            rec['size'] = int(git(repo, 'cat-file', '-s', oid))
            content = run(['git', '-C', str(repo), 'cat-file', '-p', oid]).stdout
            rec['content_repr'] = repr(content)
    else:
        rec.update(mode=None, type=None, oid=None)
    return rec

def main():
    repo = WORK / 'fixture-2'  # same index naming as frozen counter
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    top = Path(git(repo, 'rev-parse', '--show-toplevel')).resolve()
    assert top == repo.resolve(), f'fixture root mismatch: {top} != {repo.resolve()}'
    f = repo / PATH
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', PATH)
    def commit():
        git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        return git(repo, 'rev-parse', 'HEAD')
    versions = {}
    inspection = {}
    versions['equal'] = commit()
    inspection['equal'] = inspect(repo, versions['equal'], PATH)
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', PATH)
    versions['changed'] = commit()
    inspection['changed'] = inspect(repo, versions['changed'], PATH)
    f.unlink()
    git(repo, 'add', '-u')
    versions['missing'] = commit()
    inspection['missing'] = inspect(repo, versions['missing'], PATH)
    f.write_text('print("real executor")\n')
    (repo / 'unrelated.txt').write_text('unrelated change\n')
    git(repo, 'add', '--', PATH, 'unrelated.txt')
    versions['unrelated'] = commit()
    inspection['unrelated'] = inspect(repo, versions['unrelated'], PATH)
    versions['unresolvable'] = '0' * 40
    inspection['unresolvable'] = None  # not a commit; resolution probe separate
    f.unlink()
    f.symlink_to('elsewhere.py')
    git(repo, 'add', '--', PATH)
    versions['symlink'] = commit()
    inspection['symlink'] = inspect(repo, versions['symlink'], PATH)
    # dangling check
    link_state = {'is_symlink': f.is_symlink(), 'is_file': f.is_file(),
                  'readlink': os.readlink(f) if f.is_symlink() else None,
                  'exists': f.exists(), 'lexists': os.path.lexists(f)}
    report = {'path': PATH, 'repo': str(repo), 'versions': versions,
              'inspection': inspection, 'worktree_link_state': link_state,
              'env': {k: env[k] for k in ('GIT_CONFIG_GLOBAL', 'GIT_CONFIG_NOSYSTEM',
                                          'PYTHONDONTWRITEBYTECODE', 'TMPDIR')},
              'python': sys.version, 'git': git(repo, '--version')}
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0

if __name__ == '__main__':
    sys.exit(main())
