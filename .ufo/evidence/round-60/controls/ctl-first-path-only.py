#!/usr/bin/env python3
"""Control: first-path-only strawman (round-59 mistake 2 family).

Implements the same regular-blob equality logic as the real gate but inspects
ONLY the first declared --path and ignores the rest. The round-60 counter
invokes the tool once per class with ALL five declared paths and puts the
symlink cell on paths[1] and the corrupt cell on paths[3], so this strawman
answers BOUND on both and fails: certification requires C1_R60_PASS=false.
"""
import argparse
import os
import subprocess
import sys

REGULAR = frozenset({'100644', '100755'})
TOKENS = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT',
          2: 'EXECUTOR_SOURCE_UNAVAILABLE'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', dest='paths', required=True)
    a = p.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}

    def git(*args):
        return subprocess.run(['git', '-C', a.repo] + list(args),
                              capture_output=True, env=env, timeout=25)

    def resolve(rev):
        r = git('rev-parse', '--verify', '--quiet', '--end-of-options',
                rev + '^{commit}')
        if r.returncode:
            return None
        out = r.stdout.decode('ascii', 'strict').strip()
        return out if len(out) == 40 else None

    t = resolve(a.trusted)
    c = resolve(a.candidate)
    if not t or not c:
        print(TOKENS[2] + ': unresolvable revision', file=sys.stderr)
        return 2
    first = a.paths[0]
    r = git('--no-replace-objects', '--literal-pathspecs', 'ls-tree', '-z',
            c, '--', first)
    if r.returncode:
        print(TOKENS[2] + ': ls-tree failed', file=sys.stderr)
        return 2
    rec = None
    for record in r.stdout.split(b'\x00'):
        if not record:
            continue
        meta, sep, name = record.partition(b'\t')
        if not sep:
            continue
        fields = meta.split(b' ')
        if len(fields) != 3:
            continue
        if name.decode('utf-8', 'surrogateescape') != first:
            continue
        rec = (fields[0].decode('ascii'), fields[1].decode('ascii'),
               fields[2].decode('ascii'))
    if rec is None:
        print('EXECUTOR_SOURCE_DRIFT: %r missing at candidate' % first)
        return 1
    mode, kind, oid = rec
    if kind != 'blob' or mode not in REGULAR:
        print('EXECUTOR_SOURCE_DRIFT: %r nonregular' % first)
        return 1
    rt = git('rev-parse', '%s:%s' % (t, first))
    if rt.returncode:
        print(TOKENS[2] + ': trusted read failed', file=sys.stderr)
        return 2
    if oid == rt.stdout.decode('ascii').strip():
        print('EXECUTOR_SOURCE_BOUND: first path equal')
        return 0
    print('EXECUTOR_SOURCE_DRIFT: first path differs')
    return 1


if __name__ == '__main__':
    sys.exit(main())
