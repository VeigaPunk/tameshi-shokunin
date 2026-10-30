#!/usr/bin/env python3
"""Timeout-flaw probe stub: hangs on the first fixture only.

Detects first-fixture via (path == tools/runner.py and candidate == trusted).
All other invocations delegate to conforming behavior so the counter reaches
the hang point quickly and then would continue if not for the 30 s timeout.
"""
import subprocess
import sys
import time

if '--path' in sys.argv:
    paths = [sys.argv[i + 1] for i, x in enumerate(sys.argv) if x == '--path']
    cand = sys.argv[sys.argv.index('--candidate') + 1]
    trusted = subprocess.run(
        ['git', '-C', sys.argv[sys.argv.index('--repo') + 1],
         'rev-parse', 'HEAD~4'], capture_output=True, text=True).stdout.strip()
    if paths == ['tools/runner.py'] and cand == trusted:
        print('HANGING probe: sleeping 60 s', file=sys.stderr, flush=True)
        time.sleep(60)
        sys.exit(0)

# conforming behavior for non-target invocations
import argparse
p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()


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
