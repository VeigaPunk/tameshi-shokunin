#!/usr/bin/env python3
"""Independent minimal oracle for round-59 cell: path 'tools/日本語.py', class 'equal'.

Reimplements the contract's expectation from first principles using only git
plumbing (ls-tree / cat-file), independent of tools/executor-source-pin.py.

Contract mapping (frozen round-59 contract.json):
  exit 0 + EXECUTOR_SOURCE_BOUND      : declared regular executable-source blobs equal trusted blobs
  exit 1 + EXECUTOR_SOURCE_DRIFT      : a declared source differs or is missing/nonregular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE: bad args, invalid trusted commit/source or unresolvable candidate

Oracle reports observed object facts and the verdict a conforming gate MUST
emit for those facts; --expect equal|changed makes it assert the fixture
encodes the assumed class.
"""
import argparse
import json
import subprocess
import sys

def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def resolve_commit(repo, rev):
    rc, out, err = git(repo, 'rev-parse', '--verify', f'{rev}^{{commit}}')
    return (out.strip(), None) if rc == 0 else (None, err.strip())

def tree_entry(repo, commit, path):
    rc, out, err = git(repo, 'ls-tree', commit, '--', path)
    if rc != 0 or not out.strip():
        return None
    # format: "<mode> <type> <oid>\t<path>"
    meta, _, name = out.rstrip('\n').partition('\t')
    mode, typ, oid = meta.split()
    return {'mode': mode, 'type': typ, 'oid': oid, 'name': name}

def blob_bytes(repo, oid):
    rc, out, err = git(repo, 'cat-file', 'blob', oid)
    return out.encode() if rc == 0 else None

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    p.add_argument('--expect', choices=['equal', 'changed'], default=None,
                   help='counter class the fixture must encode; mapped to contract verdict')
    a = p.parse_args()
    # counter class name -> contract verdict category (contract exit_map)
    expect_verdict = {'equal': 'equal', 'changed': 'drift'}.get(a.expect) if a.expect else None

    trusted, terr = resolve_commit(a.repo, a.trusted)
    candidate, cerr = resolve_commit(a.repo, a.candidate)
    facts = {'path': a.path, 'trusted_rev': a.trusted, 'candidate_rev': a.candidate}

    if trusted is None:
        facts.update(verdict='unavailable', expected_exit=2,
                     expected_token='EXECUTOR_SOURCE_UNAVAILABLE', reason=f'trusted unresolvable: {terr}')
        print(json.dumps(facts, ensure_ascii=False, indent=1)); return 0
    if candidate is None:
        facts.update(verdict='unavailable', expected_exit=2,
                     expected_token='EXECUTOR_SOURCE_UNAVAILABLE', reason=f'candidate unresolvable: {cerr}')
        print(json.dumps(facts, ensure_ascii=False, indent=1)); return 0

    te = tree_entry(a.repo, trusted, a.path)
    ce = tree_entry(a.repo, candidate, a.path)
    facts['trusted_entry'] = te
    facts['candidate_entry'] = ce

    fixture_ok = True
    notes = []
    if te is None or te['type'] != 'blob' or te['mode'] != '100644':
        fixture_ok = False
        notes.append('trusted entry is not a regular 100644 blob as fixture design assumes')
    else:
        content = blob_bytes(a.repo, te['oid'])
        facts['trusted_content_sha256_input'] = content.decode(errors='replace')
        if content != b'print("real executor")\n':
            fixture_ok = False
            notes.append('trusted blob content deviates from frozen measure.py fixture content')

    if ce is not None and ce['type'] == 'blob':
        cc = blob_bytes(a.repo, ce['oid'])
        facts['candidate_content_sha256_input'] = cc.decode(errors='replace')

    if ce is None or ce['type'] != 'blob':
        verdict, exit_code, token = 'drift', 1, 'EXECUTOR_SOURCE_DRIFT'
        notes.append('candidate entry missing or non-blob -> drift per contract')
    elif te is None:
        verdict, exit_code, token = 'drift', 1, 'EXECUTOR_SOURCE_DRIFT'
        notes.append('trusted source missing -> cannot bind -> drift per contract')
    elif (ce['mode'], ce['type'], ce['oid']) == (te['mode'], te['type'], te['oid']):
        verdict, exit_code, token = 'equal', 0, 'EXECUTOR_SOURCE_BOUND'
        notes.append('mode/type/oid identical across trusted and candidate -> bound')
    else:
        verdict, exit_code, token = 'drift', 1, 'EXECUTOR_SOURCE_DRIFT'
        notes.append('mode/type/oid differ across trusted and candidate -> drift')

    facts.update(verdict=verdict, expected_exit=exit_code, expected_token=token,
                 fixture_assumption_ok=fixture_ok, notes=notes)
    if a.expect:
        facts['expect'] = a.expect
        facts['expect_verdict'] = expect_verdict
        facts['expect_met'] = (expect_verdict == verdict)
    print(json.dumps(facts, ensure_ascii=False, indent=1))
    if expect_verdict and expect_verdict != verdict:
        return 1
    return 0 if fixture_ok else 1

if __name__ == '__main__':
    sys.exit(main())
