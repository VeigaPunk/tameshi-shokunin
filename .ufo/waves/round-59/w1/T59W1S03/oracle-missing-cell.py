#!/usr/bin/env python3
"""T59W1S03 independent oracle -- round59 cell tools/runner.py x 'missing'.

Computes the contract-required (exit_code, token) for one
  --repo REPO --trusted COMMIT --candidate COMMIT --path PATH
invocation by direct git object inspection (rev-parse / ls-tree only).
Independent of tools/executor-source-pin.py; used to cross-check the
frozen counter's expected mapping for this single cell.

Contract (evidence/round-59/contract.json exit_map):
  0 EXECUTOR_SOURCE_BOUND         all declared regular executable-source blobs equal trusted blobs
  1 EXECUTOR_SOURCE_DRIFT         declared source differs or is missing/nonregular at candidate
  2 EXECUTOR_SOURCE_UNAVAILABLE   bad args, invalid trusted commit/source or unresolvable candidate
"""
import argparse
import json
import subprocess
import sys

TOK = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT', 2: 'EXECUTOR_SOURCE_UNAVAILABLE'}
REGULAR_MODES = {'100644', '100755'}


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args],
                          capture_output=True, text=True,
                          env={'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1',
                               'PATH': '/usr/bin:/bin'})


def entry(repo, rev, path):
    """Return (mode, type, blob) or None for the path entry at rev."""
    r = git(repo, 'ls-tree', rev, '--', path)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    meta, _ = r.stdout.rstrip('\n').split('\t', 1)
    mode, typ, blob = meta.split()
    return {'mode': mode, 'type': typ, 'blob': blob}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    a = p.parse_args()

    facts = {'path': a.path}
    rt = git(a.repo, 'rev-parse', '--verify', a.trusted + '^{commit}')
    rc = git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}')
    facts['trusted_commit_resolves'] = rt.returncode == 0
    facts['candidate_commit_resolves'] = rc.returncode == 0

    t = entry(a.repo, a.trusted, a.path) if facts['trusted_commit_resolves'] else None
    c = entry(a.repo, a.candidate, a.path) if facts['candidate_commit_resolves'] else None
    facts['trusted_entry'] = t
    facts['candidate_entry'] = c

    if not facts['candidate_commit_resolves'] or not facts['trusted_commit_resolves']:
        verdict = 2
    elif t is None or t['type'] != 'blob' or t['mode'] not in REGULAR_MODES:
        verdict = 2
    elif c is None or c['type'] != 'blob':
        verdict = 1
    elif c['blob'] != t['blob']:
        verdict = 1
    else:
        verdict = 0

    print(json.dumps({'facts': facts,
                      'expected_exit': verdict,
                      'expected_token': TOK[verdict]}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
