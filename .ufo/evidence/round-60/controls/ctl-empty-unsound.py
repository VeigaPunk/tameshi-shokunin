#!/usr/bin/env python3
"""Control: empty-blob-unsound strawman (round-59 attack T59W1S39 family).

Short-circuits to BOUND as soon as any declared path's trusted blob is the
empty blob (sha1 e69de29...), never comparing the remaining paths. The
round-60 counter declares tools/empty-fixture.txt (empty blob) in every cell,
so this strawman accepts the changed/missing/symlink/corrupt cells too and
fails: certification requires C1_R60_PASS=false.
"""
import argparse
import os
import subprocess
import sys

EMPTY_BLOB_SHA1 = 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'
REGULAR = frozenset({'100644', '100755'})


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
        print('EXECUTOR_SOURCE_UNAVAILABLE: unresolvable revision',
              file=sys.stderr)
        return 2
    for path in a.paths:
        rt = git('rev-parse', '%s:%s' % (t, path))
        if rt.returncode:
            continue
        t_oid = rt.stdout.decode('ascii').strip()
        if t_oid == EMPTY_BLOB_SHA1:
            print('EXECUTOR_SOURCE_BOUND: empty trusted blob short-circuit')
            return 0
    # No empty blob involved: naive per-path oid equality.
    for path in a.paths:
        rt = git('rev-parse', '%s:%s' % (t, path))
        rc = git('ls-tree', '-z', c, '--', path)
        if rt.returncode or rc.returncode:
            print('EXECUTOR_SOURCE_DRIFT: %r unreadable' % path)
            return 1
        recs = [r for r in rc.stdout.split(b'\x00') if r]
        if not recs:
            print('EXECUTOR_SOURCE_DRIFT: %r missing' % path)
            return 1
        fields = recs[0].split(b' ', 2)[0:1]
        meta, _, name = recs[0].partition(b'\t')
        f = meta.split(b' ')
        if name.decode('utf-8', 'surrogateescape') != path:
            print('EXECUTOR_SOURCE_DRIFT: %r missing' % path)
            return 1
        if f[1].decode() != 'blob' or f[0].decode() not in REGULAR:
            print('EXECUTOR_SOURCE_DRIFT: %r nonregular' % path)
            return 1
        if f[2].decode() != rt.stdout.decode('ascii').strip():
            print('EXECUTOR_SOURCE_DRIFT: %r differs' % path)
            return 1
    print('EXECUTOR_SOURCE_BOUND: all declared paths equal')
    return 0


if __name__ == '__main__':
    sys.exit(main())
