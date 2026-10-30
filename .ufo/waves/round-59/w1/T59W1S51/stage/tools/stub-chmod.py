#!/usr/bin/env python3
"""Cleanup-failure probe stub: makes one fixture dir non-removable.

On the first fixture of fixture-0 (space path equal cell) it chmods the
fixture's tools/ dir to 0o555 so shutil.rmtree(work/fixture-0) in the
counter's finally-block raises PermissionError. All other invocations
behave conformingly. Probe only.
"""
import argparse
import os
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

if a.path == ['tools/space name.py'] and a.candidate == a.trusted:
    tools = os.path.join(a.repo, 'tools')
    if os.path.isdir(tools):
        os.chmod(tools, 0o555)
        print(f'PROBE chmod 0o555 {tools}', file=sys.stderr, flush=True)


def git(*args):
    return subprocess.run(['git', '-C', a.repo, *args],
                          capture_output=True, text=True)


drift = False
for rev in (a.trusted, a.candidate):
    if git('rev-parse', '--verify', rev + '^{commit}').returncode:
        print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
        sys.exit(2)
for path in a.path:
    r = git('ls-tree', a.candidate, '--', path)
    t = git('ls-tree', a.trusted, '--', path)
    if not r.stdout.strip() or not t.stdout.strip():
        print('EXECUTOR_SOURCE_DRIFT', file=sys.stderr)
        drift = True
        continue
    rf, tf = r.stdout.strip().split(), t.stdout.strip().split()
    if rf[1] != 'blob' or rf[0] not in ('100644', '100755') or rf[2] != tf[2]:
        print('EXECUTOR_SOURCE_DRIFT', file=sys.stderr)
        drift = True
if drift:
    sys.exit(1)
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
