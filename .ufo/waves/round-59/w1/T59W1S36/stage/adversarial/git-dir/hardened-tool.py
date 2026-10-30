#!/usr/bin/env python3
"""Hardened reference oracle: scrubs GIT_* from the git subprocess environment.

Demonstrates the smallest sound behavior against GIT_DIR poisoning:
every git invocation runs with GIT_*-stripped env, plus a toplevel identity
assertion on --repo (mirrors the frozen counter's fixture-root check).
Reference only; NOT a candidate implementation.
"""
import argparse
import os
import subprocess
import sys


def scrubbed_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_CONFIG_GLOBAL'] = '/dev/null'
    env['GIT_CONFIG_NOSYSTEM'] = '1'
    return env


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()
    env = scrubbed_env()

    def git(*args):
        return subprocess.run(['git', '-C', a.repo, *args],
                              capture_output=True, text=True, env=env)

    top = git('rev-parse', '--show-toplevel')
    want = os.path.realpath(a.repo)
    got = os.path.realpath(top.stdout.strip()) if top.returncode == 0 else None
    if not top.returncode and got != want:
        # repo resolved to a different toplevel (worktree/gitfile); accept only
        # if the absolute git dir matches repo/.git
        gd = git('rev-parse', '--absolute-git-dir')
        if gd.returncode or os.path.realpath(gd.stdout.strip()) != os.path.join(want, '.git'):
            print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
            return 2

    trusted = git('rev-parse', '--verify', a.trusted + '^{commit}')
    if trusted.returncode:
        print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
        return 2
    candidate = git('rev-parse', '--verify', a.candidate + '^{commit}')
    if candidate.returncode:
        print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
        return 2
    trusted = trusted.stdout.strip()
    candidate = candidate.stdout.strip()

    for path in a.path:
        t = git('show', f'{trusted}:{path}')
        if t.returncode or not t.stdout:
            print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
            return 2
        c = git('show', f'{candidate}:{path}')
        if c.returncode:
            print('EXECUTOR_SOURCE_DRIFT', file=sys.stderr)
            return 1
        if t.stdout != c.stdout:
            print('EXECUTOR_SOURCE_DRIFT', file=sys.stderr)
            return 1
    print('EXECUTOR_SOURCE_BOUND')
    return 0


if __name__ == '__main__':
    sys.exit(main())
