#!/usr/bin/env python3
"""Contract probe model only; not an observed candidate implementation."""
import argparse
import subprocess
import sys
p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()
def git(*args):
    return subprocess.run(['git', '-C', a.repo, *args], capture_output=True)
def stop(code):
    print({0:'EXECUTOR_SOURCE_BOUND',1:'EXECUTOR_SOURCE_DRIFT',2:'EXECUTOR_SOURCE_UNAVAILABLE'}[code])
    sys.exit(code)
def commit(rev):
    r = git('rev-parse', '--verify', '--end-of-options', rev+'^{commit}')
    if r.returncode: stop(2)
    return r.stdout.decode().strip()
def entry(rev, path):
    r = git('ls-tree', '-z', rev, '--', ':(literal)'+path)
    if r.returncode or not r.stdout: return None
    meta, name = r.stdout.rstrip(b'\0').split(b'\t', 1)
    mode, kind, oid = meta.split()
    return mode, kind, oid
trusted = commit(a.trusted)
candidate = commit(a.candidate)
for path in a.path:
    t = entry(trusted, path)
    if t is None or t[0] not in (b'100644', b'100755') or t[1] != b'blob':
        stop(2)
    c = entry(candidate, path)
    if c is None or c[0] not in (b'100644', b'100755') or c[1] != b'blob' or t[2] != c[2]:
        stop(1)
stop(0)
