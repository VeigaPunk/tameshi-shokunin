#!/usr/bin/env python3
"""Scratch reference candidate for tools/executor-source-pin.py (T59W1S37 probe).

Implements the contract interface with sound --path handling:
- argparse errors (option-like PATH values) -> exit 2 + EXECUTOR_SOURCE_UNAVAILABLE token
- PATH validated as repo-relative POSIX literal (no absolute, no '', '.', '..')
- PATH always passed to git as pathspec ':(literal)<path>' after '--'
- trusted source must be a single regular blob (100644/100755); else exit 2
- candidate commit unresolvable -> exit 2; path missing/nonregular at candidate -> exit 1
- path echo is repr()-quoted (single-line tokens; no raw path interpolation)
"""
import argparse
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True)


def prepare(path):
    """Return True iff path is a usable repo-relative POSIX literal path."""
    if not path:
        return False
    if path.startswith('/') or '\\' in path:
        return False
    segments = path.split('/')
    if any(seg in ('', '.', '..') for seg in segments):
        return False
    return True


def bind(raw):
    """MUTATION POINT — single trust boundary for caller-supplied --path values.

    MUTANT: return raw unchanged (trust caller-supplied path string verbatim).
    """
    return raw


def lookup(repo, rev, bound):
    """Return blob sha iff rev:bound resolves to exactly one regular blob, else None.

    bound is the value returned by bind(); None means caller-supplied path rejected.
    """
    if bound is None:
        return None
    r = git(repo, 'ls-tree', '-z', rev, '--', bound)
    if r.returncode or not r.stdout:
        return None
    entries = [e for e in r.stdout.split(b'\x00') if e]
    if len(entries) != 1:
        return None
    meta = entries[0].split(b'\t', 1)[0].decode()
    mode, typ, sha = meta.split(' ')
    if typ != 'blob' or mode not in ('100644', '100755'):
        return None
    return sha


def die(msg, code):
    tok = 'EXECUTOR_SOURCE_DRIFT' if code == 1 else 'EXECUTOR_SOURCE_UNAVAILABLE'
    sys.stderr.write(tok + ': ' + msg + '\n')
    return code


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    try:
        a = p.parse_args()
    except SystemExit:
        sys.stderr.write('EXECUTOR_SOURCE_UNAVAILABLE: bad arguments\n')
        return 2

    bounds = []
    for path in a.path:
        bound = bind(path)
        if bound is None:
            return die(f'path={path!r} not a repo-relative literal path', 2)
        bounds.append(bound)

    r = git(a.repo, 'rev-parse', '--verify', '--quiet', a.trusted + '^{commit}')
    if r.returncode:
        return die(f'trusted={a.trusted!r} not a commit', 2)
    r = git(a.repo, 'rev-parse', '--verify', '--quiet', a.candidate + '^{commit}')
    if r.returncode:
        return die(f'candidate={a.candidate!r} unresolvable', 2)

    for orig, bound in zip(a.path, bounds):
        tsha = lookup(a.repo, a.trusted, bound)
        if tsha is None:
            return die(f'trusted source path={orig!r} not a regular blob', 2)
        csha = lookup(a.repo, a.candidate, bound)
        if csha is None:
            return die(f'path={orig!r} missing or nonregular at candidate', 1)
        tblob = git(a.repo, 'cat-file', 'blob', tsha)
        cblob = git(a.repo, 'cat-file', 'blob', csha)
        if tblob.stdout != cblob.stdout:
            return die(f'path={orig!r} blob differs at candidate', 1)
    print('EXECUTOR_SOURCE_BOUND: all declared paths equal')
    return 0


if __name__ == '__main__':
    sys.exit(main())
