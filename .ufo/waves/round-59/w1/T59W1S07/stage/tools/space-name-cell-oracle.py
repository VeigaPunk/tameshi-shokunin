#!/usr/bin/env python3
"""Independent cell oracle: 'tools/space name.py', class equal (round59).

Resolves declared source blobs in Git directly; checks candidate resolvable,
object is a regular blob, and blob id equals trusted blob id.
Exit contract per round-59 contract.json exit_map.
"""
import subprocess
import sys

def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args],
                       capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def main():
    repo = trusted = candidate = None
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--repo':
            repo = argv[i + 1]; i += 2
        elif a == '--trusted':
            trusted = argv[i + 1]; i += 2
        elif a == '--candidate':
            candidate = argv[i + 1]; i += 2
        elif a == '--path':
            i += 2  # cell-fixed path; ignore extra --path
        else:
            print(f'EXECUTOR_SOURCE_UNAVAILABLE unknown-arg {a}')
            return 2
    if not (repo and trusted and candidate):
        print('EXECUTOR_SOURCE_UNAVAILABLE bad-args')
        return 2
    path = 'tools/space name.py'

    rc, _, err = git(repo, 'rev-parse', '--verify', trusted + '^{commit}')
    if rc:
        print('EXECUTOR_SOURCE_UNAVAILABLE bad-trusted')
        return 2
    rc, _, err = git(repo, 'rev-parse', '--verify', candidate + '^{commit}')
    if rc:
        print('EXECUTOR_SOURCE_UNAVAILABLE bad-candidate')
        return 2

    rc, out, _ = git(repo, 'ls-tree', candidate, '--', path)
    if rc or not out:
        print('EXECUTOR_SOURCE_DRIFT missing-or-unreadable')
        return 1
    mode, typ, blob = out.split()[0], out.split()[1], out.split()[2]
    if typ != 'blob' or mode not in ('100644', '100755'):
        print('EXECUTOR_SOURCE_DRIFT nonregular-source')
        return 1
    rc, tout, _ = git(repo, 'ls-tree', trusted, '--', path)
    tblob = tout.split()[2]
    if blob != tblob:
        print('EXECUTOR_SOURCE_DRIFT blob-mismatch')
        return 1
    print('EXECUTOR_SOURCE_BOUND')
    return 0

if __name__ == '__main__':
    sys.exit(main())
