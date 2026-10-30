#!/usr/bin/env python3
"""Minimal independent oracle for ONE round-59 cell: path 'tools/日本語.py', class 'symlink'.

Computes the expected (exit, token) verdict for a candidate revision directly from
git object data, per contract exit_map:
  0 EXECUTOR_SOURCE_BOUND     all declared regular executable-source blobs equal trusted blobs
  1 EXECUTOR_SOURCE_DRIFT     a declared source differs or is missing/nonregular at candidate
  2 EXECUTOR_SOURCE_UNAVAILABLE  bad args, invalid trusted commit/source, unresolvable candidate

Oracle rules (derived independently from the contract JSON, not from measure.py):
  trusted commit unresolvable              -> 2 UNAVAILABLE
  trusted path entry missing/nonregular    -> 2 UNAVAILABLE  (invalid trusted source)
  candidate commit unresolvable            -> 2 UNAVAILABLE
  candidate path entry missing             -> 1 DRIFT
  candidate path entry nonregular (not a regular blob: symlink 120000,
      tree 040000, gitlink 160000, ...)     -> 1 DRIFT
  blob content differs from trusted blob   -> 1 DRIFT
  otherwise                                -> 0 BOUND
Usage: oracle.py --repo REPO --trusted COMMIT --candidate COMMIT --path PATH
Prints one line: ORACLE verdict=<token> exit=<n> reason=<why>
"""
import argparse
import subprocess
import sys

REGULAR_MODES = {'100644', '100755'}

def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def entry(repo, commit, path):
    """Return (mode, type, oid) or None for path at commit; (None,'bad',None) if commit bad."""
    rc, out, _ = git(repo, 'rev-parse', '--verify', '--quiet', commit + '^{commit}')
    if rc != 0:
        return (None, 'bad-commit', None)
    rc, out, _ = git(repo, 'ls-tree', commit, '--', path)
    if rc != 0 or not out:
        return (None, None, None)  # commit valid, path absent
    meta, _name = out.split('\t', 1)
    mode, typ, oid = meta.split()
    return (mode, typ, oid)

def blob(repo, oid):
    rc, out, _ = git(repo, 'cat-file', '-p', oid)
    return out if rc == 0 else None

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    a = p.parse_args()
    t = entry(a.repo, a.trusted, a.path)
    if t is None or t[1] == 'bad-commit':
        print(f'ORACLE verdict=EXECUTOR_SOURCE_UNAVAILABLE exit=2 reason=trusted-commit-unresolvable')
        return 2
    if t[0] not in REGULAR_MODES or t[1] != 'blob':
        print(f'ORACLE verdict=EXECUTOR_SOURCE_UNAVAILABLE exit=2 reason=trusted-source-not-regular mode={t[0]} type={t[1]}')
        return 2
    c = entry(a.repo, a.candidate, a.path)
    if c[1] == 'bad-commit':
        print(f'ORACLE verdict=EXECUTOR_SOURCE_UNAVAILABLE exit=2 reason=candidate-unresolvable')
        return 2
    if c[0] is None:
        print(f'ORACLE verdict=EXECUTOR_SOURCE_DRIFT exit=1 reason=path-missing-at-candidate')
        return 1
    if c[0] not in REGULAR_MODES or c[1] != 'blob':
        print(f'ORACLE verdict=EXECUTOR_SOURCE_DRIFT exit=1 reason=nonregular-at-candidate mode={c[0]} type={c[1]} oid={c[2]}')
        return 1
    if blob(a.repo, t[2]) != blob(a.repo, c[2]):
        print(f'ORACLE verdict=EXECUTOR_SOURCE_DRIFT exit=1 reason=blob-content-differs trusted_oid={t[2]} candidate_oid={c[2]}')
        return 1
    print(f'ORACLE verdict=EXECUTOR_SOURCE_BOUND exit=0 reason=blobs-equal oid={t[2]}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
