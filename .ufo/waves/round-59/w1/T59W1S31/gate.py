"""Synthetic CLI control for a duplicate-list mutation; not a candidate implementation."""
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
    return subprocess.run(['git', '-C', a.repo, *args], capture_output=True, text=True)

def stop(code, token):
    print(token)
    sys.exit(code)

def commit(rev):
    r = git('rev-parse', '--verify', '--end-of-options', rev + '^{commit}')
    if r.returncode:
        stop(2, 'EXECUTOR_SOURCE_UNAVAILABLE')
    return r.stdout.strip()

def blob(rev, path):
    r = git('ls-tree', '-z', rev, '--', path)
    entries = r.stdout.rstrip('\0').split('\0') if r.stdout else []
    for entry in entries:
        metadata, name = entry.split('\t', 1)
        mode, kind, oid = metadata.split()
        if name == path and kind == 'blob' and mode in ('100644', '100755'):
            return oid
    return None

trusted = commit(a.trusted)
candidate = commit(a.candidate)
seen = set()
for path in a.path:
    if path in seen:
        continue
    seen.add(path)
    before = blob(trusted, path)
    if before is None:
        stop(2, 'EXECUTOR_SOURCE_UNAVAILABLE')
    if blob(candidate, path) != before:
        stop(1, 'EXECUTOR_SOURCE_DRIFT')
stop(0, 'EXECUTOR_SOURCE_BOUND')
