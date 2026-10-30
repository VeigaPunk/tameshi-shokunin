#!/usr/bin/env python3
"""Minimal independent oracle for ONE frozen cell: path='tools/日本語.py', class='missing'.

Derives the contract-expected (exit, token) verdict for ANY (trusted, candidate)
pair by direct git-object inspection only — never touches the worktree, so it is
immune to the fixture's final on-disk state (HEAD is the symlink commit when
measure.py runs all probes).

Contract exit_map (frozen):
  0 EXECUTOR_SOURCE_BOUND        all declared regular executable-source blobs equal trusted blobs
  1 EXECUTOR_SOURCE_DRIFT        declared source differs OR is missing/nonregular at candidate
  2 EXECUTOR_SOURCE_UNAVAILABLE  bad args, invalid trusted commit/source, unresolvable candidate

Trusted-side absence is folded into UNAVAILABLE ("invalid trusted ... source"),
matching how measure.py always supplies a valid trusted commit.
"""
import subprocess
import sys

def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args],
                       capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout, r.stderr

def resolve_commit(repo, rev):
    rc, out, _ = git(repo, 'rev-parse', '--verify', f'{rev}^{{commit}}')
    return out.strip() if rc == 0 else None

def tree_entry(repo, commit, path):
    """Return (mode, objtype, object_id) for path at commit, or None if absent."""
    rc, out, _ = git(repo, 'ls-tree', commit, '--', path)
    if rc != 0 or not out.strip():
        return None
    meta, _, name = out.rstrip('\n').partition('\t')
    mode, objtype, oid = meta.split()
    return mode, objtype, oid

def oracle(repo, trusted, candidate, path):
    t = resolve_commit(repo, trusted)
    if t is None:
        return 2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'trusted not a commit'
    c = resolve_commit(repo, candidate)
    if c is None:
        return 2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'candidate not a commit'
    te = tree_entry(repo, t, path)
    if te is None or te[1] != 'blob' or te[0] not in ('100644', '100755'):
        return 2, 'EXECUTOR_SOURCE_UNAVAILABLE', 'trusted source missing/nonregular'
    ce = tree_entry(repo, c, path)
    if ce is None:
        return 1, 'EXECUTOR_SOURCE_DRIFT', 'declared source missing at candidate'
    if ce[1] != 'blob' or ce[0] not in ('100644', '100755'):
        return 1, 'EXECUTOR_SOURCE_DRIFT', 'declared source nonregular at candidate'
    if ce[2] == te[2]:
        return 0, 'EXECUTOR_SOURCE_BOUND', 'blob identical to trusted'
    return 1, 'EXECUTOR_SOURCE_DRIFT', 'blob differs from trusted'

def main():
    repo, trusted = sys.argv[1], sys.argv[2]
    versions = [('equal', trusted),
                ('changed', sys.argv[3]), ('missing', sys.argv[4]),
                ('unrelated', sys.argv[5]), ('unresolvable', '0' * 40),
                ('symlink', sys.argv[6])]
    path = sys.argv[7]
    expected = {'equal': 0, 'changed': 1, 'missing': 1,
                'unrelated': 0, 'unresolvable': 2, 'symlink': 1}
    tokens = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT',
              2: 'EXECUTOR_SOURCE_UNAVAILABLE'}
    allok = True
    for cls, cand in versions:
        code, token, why = oracle(repo, trusted, cand, path)
        ok = code == expected[cls] and token == tokens[expected[cls]]
        allok &= ok
        print(f'cell path={path!r} class={cls:<12} candidate={cand[:12]} '
              f'-> exit={code} token={token} why={why!r} expected_match={ok}')
    print(f'OWNED_CELL path={path!r} class=missing verdict=exit 1 + EXECUTOR_SOURCE_DRIFT '
          f'(all six discriminated: {allok})')
    return 0 if allok else 1

if __name__ == '__main__':
    sys.exit(main())
