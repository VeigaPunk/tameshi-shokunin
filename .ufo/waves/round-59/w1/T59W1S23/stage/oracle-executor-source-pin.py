#!/usr/bin/env python3
"""INDEPENDENT ORACLE PROBE for frozen round-59 cell (path='tools/-runner.py', class='unresolvable').
Not the production gate. Independently re-derives the expected contract from git plumbing:
  candidate must resolve to a commit in --repo, else EXECUTOR_SOURCE_UNAVAILABLE + exit 2.
For resolvable candidates, declared source blob (mode/type/content) must equal trusted's,
else EXECUTOR_SOURCE_DRIFT + exit 1; equal -> EXECUTOR_SOURCE_BOUND + exit 0.
Trusted commit must itself resolve and contain the declared path, else UNAVAILABLE + exit 2."""
import argparse, os, subprocess, sys

def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True,
                          env=env, timeout=30)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()
    if len(a.path) != 1:
        print('EXECUTOR_SOURCE_UNAVAILABLE: oracle handles exactly one declared path', file=sys.stderr)
        return 2
    path = a.path[0]

    t = git(a.repo, 'rev-parse', '--verify', a.trusted + '^{commit}')
    if t.returncode:
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted commit does not resolve', file=sys.stderr)
        return 2
    c = git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}')
    if c.returncode:
        print(f'EXECUTOR_SOURCE_UNAVAILABLE: candidate {a.candidate} does not resolve to a commit',
              file=sys.stderr)
        return 2
    tsrc = git(a.repo, 'ls-tree', t.stdout.strip(), '--', path)
    csrc = git(a.repo, 'ls-tree', c.stdout.strip(), '--', path)
    toks = tsrc.stdout.split()
    coks = csrc.stdout.split()
    if not toks or toks[1] != 'blob' or not coks or coks[1] != 'blob' or toks[0] != '100644' or coks[0] != '100644':
        print(f'EXECUTOR_SOURCE_DRIFT: declared source missing or nonregular at candidate: {path}',
              file=sys.stderr)
        return 1
    if toks[2] != coks[2]:
        print(f'EXECUTOR_SOURCE_DRIFT: declared source differs: {path}', file=sys.stderr)
        return 1
    print('EXECUTOR_SOURCE_BOUND: declared source matches trusted', file=sys.stdout)
    return 0

if __name__ == '__main__':
    sys.exit(main())
