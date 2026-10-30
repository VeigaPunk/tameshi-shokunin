#!/usr/bin/env python3
"""MOCK sound shape (receipt aid, NOT a candidate implementation):
ls-tree (mode, oid) tuple compare, --no-replace-objects, belts. Must PASS
T59W1S35's adversarial_config_test."""
import argparse
import shutil
import subprocess
import sys

GIT = shutil.which('git')
BASE = [GIT, '--no-replace-objects', '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false']

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

def run(args):
    return subprocess.run(BASE + args, capture_output=True, text=True)

for rev in (a.trusted, a.candidate):
    if run(['-C', a.repo, 'rev-parse', '--verify', rev + '^{commit}']).returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
        sys.exit(2)

def entry(rev, path):
    r = run(['-C', a.repo, 'ls-tree', rev, '--', path])
    if r.returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
        sys.exit(2)
    parts = r.stdout.split(None, 3)
    return (parts[0], parts[2]) if len(parts) >= 3 else None

for path in a.path:
    if entry(a.trusted, path) != entry(a.candidate, path) or entry(a.candidate, path) is None:
        print('EXECUTOR_SOURCE_DRIFT', file=sys.stderr)
        sys.exit(1)
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
