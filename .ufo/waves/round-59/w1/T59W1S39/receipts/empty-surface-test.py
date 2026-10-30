#!/usr/bin/env python3
"""Empty-source-blob surface probe: proposed supplementary CLI test for
tools/executor-source-pin.py. Builds scratch fixtures with git primitives
only, runs TOOL over the empty-blob matrix, checks exits/tokens.

This is the exact CLI test proposed to L1: it does NOT modify the frozen
counter; it is a bounded empirical probe for the adversarial surface the
frozen counter never exercises (empty committed source blobs).

Expected (contract exit map applied to empty blobs):
  EE      trusted empty, candidate empty        -> 0 EXECUTOR_SOURCE_BOUND
  TE      trusted empty, candidate text         -> 1 EXECUTOR_SOURCE_DRIFT
  ET      trusted text, candidate empty         -> 1 EXECUTOR_SOURCE_DRIFT
  TM      trusted text, candidate missing       -> 1 EXECUTOR_SOURCE_DRIFT
  TSYM    trusted text, candidate symlink       -> 1 EXECUTOR_SOURCE_DRIFT
  EE_UNR  trusted empty, candidate 000...0      -> 2 EXECUTOR_SOURCE_UNAVAILABLE
  EE4     equal-empty across all four spellings -> 0 EXECUTOR_SOURCE_BOUND
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
TEXT = 'print("real executor")\n'
ZERO = '0' * 40

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1')

def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout.strip()

def commit(repo):
    git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
    return git(repo, 'rev-parse', 'HEAD')

def build(repo):
    repo = Path(repo)
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, 'init', '-q')
    assert os.path.realpath(git(repo, 'rev-parse', '--show-toplevel')) == os.path.realpath(repo), 'fixture root mismatch'
    files = {p: repo / p for p in PATHS}
    for f in files.values():
        f.parent.mkdir(parents=True, exist_ok=True)
    # Trusted-empty commit: all four paths empty.
    for f in files.values():
        f.write_text('')
    git(repo, 'add', '--', *PATHS)
    t_empty = commit(repo)
    # Candidate-text commit (also serves as trusted-text for ET/TM/TSYM).
    for f in files.values():
        f.write_text(TEXT)
    git(repo, 'add', '--', *PATHS)
    t_text = commit(repo)
    # Candidate-empty commit: all four paths empty.
    for f in files.values():
        f.write_text('')
    git(repo, 'add', '--', *PATHS)
    c_empty = commit(repo)
    # Candidate-missing commit.
    for f in files.values():
        f.unlink()
    git(repo, 'add', '-u')
    c_missing = commit(repo)
    # Candidate-symlink commit.
    for f in files.values():
        f.symlink_to('elsewhere.py')
    git(repo, 'add', '--', *PATHS)
    c_symlink = commit(repo)
    return dict(t_empty=t_empty, t_text=t_text, c_empty=c_empty,
                c_missing=c_missing, c_symlink=c_symlink)

CASES = [
    ('EE',     't_empty', 't_empty',   0, 'EXECUTOR_SOURCE_BOUND'),
    ('TE',     't_empty', 't_text',    1, 'EXECUTOR_SOURCE_DRIFT'),
    ('ET',     't_text',  'c_empty',   1, 'EXECUTOR_SOURCE_DRIFT'),
    ('TM',     't_text',  'c_missing', 1, 'EXECUTOR_SOURCE_DRIFT'),
    ('TSYM',   't_text',  'c_symlink', 1, 'EXECUTOR_SOURCE_DRIFT'),
    ('EE_UNR', 't_empty', ZERO,        2, 'EXECUTOR_SOURCE_UNAVAILABLE'),
    ('EE4',    't_empty', 't_empty',   0, 'EXECUTOR_SOURCE_BOUND'),
]

def main():
    tool = sys.argv[1]
    work = tempfile.mkdtemp(prefix='empty-matrix-',
                            dir=os.environ.get('TMPDIR', '/tmp'))
    results = []
    try:
        vers = build(work)
        for name, tk, ck, exp_exit, token in CASES:
            candidate = ZERO if ck == ZERO else vers[ck]
            argv = [sys.executable, '-I', tool, '--repo', work,
                    '--trusted', vers[tk], '--candidate', candidate]
            paths = PATHS if name == 'EE4' else ['tools/runner.py']
            for p in paths:
                argv += ['--path', p]
            out = run(argv)
            ok = out.returncode == exp_exit and token in (out.stdout + out.stderr)
            results.append(dict(case=name, paths=len(paths), expected=exp_exit,
                                exit=out.returncode, ok=ok,
                                stdout=out.stdout.strip(), stderr=out.stderr.strip()))
        passed = sum(r['ok'] for r in results)
        print(json.dumps(results, ensure_ascii=False, indent=1))
        print(f'EMPTY_SURFACE passed={passed}/{len(results)} '
              f'EMPTY_SURFACE_PASS={str(passed == len(results)).lower()}')
        return 0 if passed == len(results) else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)

if __name__ == '__main__':
    sys.exit(main())
