#!/usr/bin/env python3
"""T59W1S09 minimal independent oracle for ONE cell:
path 'tools/space name.py' x class 'missing' (fixture-1).

Computes the contract verdict from git plumbing facts only (list argv, no
shell), per contract.json exit_map:
  0 EXECUTOR_SOURCE_BOUND      all declared regular executable-source blobs equal trusted blobs
  1 EXECUTOR_SOURCE_DRIFT      declared source differs or is missing/nonregular at candidate
  2 EXECUTOR_SOURCE_UNAVAILABLE bad args, invalid trusted commit/source or unresolvable candidate

Usage: oracle_cell.py --repo REPO --trusted COMMIT --candidate COMMIT --path PATH
Emits one JSON line to stdout and exits with the verdict code.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', required=True)
a, unknown = p.parse_known_args()

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1')

def git(*args):
    return subprocess.run(['git', '-C', a.repo, *args], capture_output=True,
                          text=True, env=env, timeout=30)

def fail(code, token, reason, **kw):
    print(json.dumps({'exit': code, 'token': token, 'reason': reason, **kw}))
    sys.exit(code)

if unknown or not (a.repo and a.trusted and a.candidate and a.path):
    fail(2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'bad-arguments', argv=sys.argv[1:])

def resolve_commit(rev):
    r = git('rev-parse', '--verify', rev + '^{commit}')
    return r.stdout.strip() if r.returncode == 0 else None

trusted_c = resolve_commit(a.trusted)
if trusted_c is None:
    fail(2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'trusted-unresolvable', trusted=a.trusted)
candidate_c = resolve_commit(a.candidate)
if candidate_c is None:
    fail(2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'candidate-unresolvable', candidate=a.candidate)

def entry(rev):
    """Return (mode, type, sha) for path at rev, or None if absent."""
    r = git('ls-tree', rev, '--', a.path)
    if r.returncode != 0:
        return ('ERR', 'ERR', None)
    lines = [l for l in r.stdout.splitlines() if l]
    if not lines:
        return None
    meta, _name = lines[0].split('\t', 1)
    mode, typ, sha = meta.split()
    return (mode, typ, sha)

t = entry(trusted_c)
if t is None or t[0] == 'ERR' or t[1] != 'blob':
    fail(2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'trusted-source-not-regular-blob',
         trusted_entry=t)
c = entry(candidate_c)
if c is None:
    fail(1, 'EXECUTOR_SOURCE_DRIFT', 'candidate-source-missing',
         trusted_entry=t, candidate_entry=None)
if c[0] == 'ERR':
    fail(2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'candidate-lookup-error', candidate_entry=c)
if c[1] != 'blob':
    fail(1, 'EXECUTOR_SOURCE_DRIFT', 'candidate-source-nonregular',
         trusted_entry=t, candidate_entry=c)
if c[2] != t[2]:
    fail(1, 'EXECUTOR_SOURCE_DRIFT', 'candidate-source-differs',
         trusted_entry=t, candidate_entry=c)
print(json.dumps({'exit': 0, 'token': 'EXECUTOR_SOURCE_BOUND', 'reason': 'blobs-equal',
                  'trusted_entry': t, 'candidate_entry': c,
                  'blob_sha': hashlib.sha256(f'{t[1]} {t[2]}\x00'.encode()).hexdigest()[:12]}))
sys.exit(0)
