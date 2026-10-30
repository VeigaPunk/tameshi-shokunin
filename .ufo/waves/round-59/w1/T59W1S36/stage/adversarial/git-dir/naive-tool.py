#!/usr/bin/env python3
"""NAIVE reference oracle for the executor-source-pin CLI contract.

Deliberately unsanitized: passes the ambient environment through to every git
subprocess. Used ONLY to demonstrate the GIT_DIR-poisoning surface in scratch.
This is NOT a candidate implementation of tools/executor-source-pin.py.
"""
import argparse
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    def git(*args):
        return subprocess.run(['git', '-C', a.repo, *args],
                              capture_output=True, text=True)

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
