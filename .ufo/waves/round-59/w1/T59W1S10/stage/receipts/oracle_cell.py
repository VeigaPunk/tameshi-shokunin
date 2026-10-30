#!/usr/bin/env python3
"""Independent oracle for round-59 cell: path='tools/space name.py', class='unrelated'.

Replicates the frozen measure.py fixture construction for this single cell
(states: equal / changed / unrelated) and independently derives the expected
verdict from raw git plumbing (object type, mode, blob content hash).

Oracle verdict rule (independent re-derivation from contract.json exit_map):
  0 EXECUTOR_SOURCE_BOUND   candidate entry for declared path exists, is a
                            regular file (mode 100644/100755, type blob),
                            and its blob equals the trusted blob.
  1 EXECUTOR_SOURCE_DRIFT   candidate entry missing, nonregular (symlink
                            mode 120000, gitlink 160000, dir), or blob
                            differs from trusted.
  2 EXECUTOR_SOURCE_UNAVAILABLE  trusted/candidate commit unresolvable, or
                            trusted entry absent/nonregular (invalid source).
"""
import argparse, json, os, subprocess, sys, shutil

PATH = 'tools/space name.py'  # contains a literal space
REAL = 'print("real executor")\n'
FORGED = 'print("forged success")\n'

BASE_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
BASE_ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
                PYTHONDONTWRITEBYTECODE='1')

def run(argv, cwd=None):
    return subprocess.run(argv, capture_output=True, text=True, env=BASE_ENV, timeout=30, cwd=cwd)

def git(repo, *args, check=True):
    r = run(['git', '-C', str(repo), *args])
    if check and r.returncode:
        raise RuntimeError(f'git {args}: {r.stderr}')
    return r.stdout.strip()

def commit(repo):
    git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
    return git(repo, 'rev-parse', 'HEAD')

def build_fixture(root):
    """Byte-faithful port of measure.py construction for this one path."""
    root = os.path.abspath(root)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    assert subprocess.run(['git', 'init', '-q', root], env=BASE_ENV).returncode == 0
    assert os.path.realpath(git(root, 'rev-parse', '--show-toplevel')) == os.path.realpath(root)
    f = os.path.join(root, PATH)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    versions = {}
    with open(f, 'w') as fh: fh.write(REAL)
    git(root, 'add', '--', PATH)
    versions['equal'] = commit(root)
    trusted = versions['equal']
    with open(f, 'w') as fh: fh.write(FORGED)
    git(root, 'add', '--', PATH)
    versions['changed'] = commit(root)
    # 'unrelated': rewrite identical source content + add unrelated.txt.
    with open(f, 'w') as fh: fh.write(REAL)
    with open(os.path.join(root, 'unrelated.txt'), 'w') as fh: fh.write('unrelated change\n')
    git(root, 'add', '--', PATH, 'unrelated.txt')
    versions['unrelated'] = commit(root)
    return trusted, versions

def ls_entry(repo, rev, path):
    out = git(repo, 'ls-tree', rev, '--', path, check=False)
    if not out:
        return None
    mode, typ, rest = out.split(None, 2)
    h, p = rest.split('\t', 1)
    return {'mode': mode, 'type': typ, 'oid': h, 'path': p}

def oracle(repo, trusted, candidate, path):
    """Independent verdict from plumbing only. Returns (exit, token, detail)."""
    for rev in (trusted, candidate):
        r = run(['git', '-C', repo, 'rev-parse', '--verify', f'{rev}^{{commit}}'])
        if r.returncode:
            return 2, 'EXECUTOR_SOURCE_UNAVAILABLE', f'unresolvable commit {rev}'
    t = ls_entry(repo, trusted, path)
    if t is None or t['type'] != 'blob' or t['mode'] not in ('100644', '100755'):
        return 2, 'EXECUTOR_SOURCE_UNAVAILABLE', f'trusted entry bad: {t}'
    c = ls_entry(repo, candidate, path)
    if c is None:
        return 1, 'EXECUTOR_SOURCE_DRIFT', 'missing at candidate'
    if c['type'] != 'blob' or c['mode'] not in ('100644', '100755'):
        return 1, 'EXECUTOR_SOURCE_DRIFT', f'nonregular at candidate: {c}'
    if (c['mode'], c['oid']) != (t['mode'], t['oid']):
        return 1, 'EXECUTOR_SOURCE_DRIFT', f"blob differs trusted={t['oid']} candidate={c['oid']}"
    return 0, 'EXECUTOR_SOURCE_BOUND', f"mode={c['mode']} type={c['type']} oid={c['oid']}"

def content_check(repo, oid):
    return git(repo, 'cat-file', '-p', oid)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixture', default='fixture')
    a = ap.parse_args()
    results = []
    trusted, versions = build_fixture(a.fixture)
    for cls in ('equal', 'changed', 'unrelated'):
        exit_code, token, detail = oracle(a.fixture, trusted, versions[cls], PATH)
        # frozen measure.py expectations for this cell
        expected = 0 if cls in ('equal', 'unrelated') else 1
        exp_tok = 'EXECUTOR_SOURCE_BOUND' if expected == 0 else 'EXECUTOR_SOURCE_DRIFT'
        results.append({
            'cell': {'path': PATH, 'class': cls},
            'trusted': trusted, 'candidate': versions[cls],
            'oracle_exit': exit_code, 'oracle_token': token, 'oracle_detail': detail,
            'frozen_expected_exit': expected, 'frozen_expected_token': exp_tok,
            'match': exit_code == expected and token == exp_tok,
        })
    # source-object type/mode/content evidence at trusted and each candidate
    entries = {}
    for cls, rev in [('trusted(equal)', trusted)] + list(versions.items()):
        entries[cls] = ls_entry(a.fixture, rev, PATH)
        if entries[cls]:
            entries[cls]['content'] = content_check(a.fixture, entries[cls]['oid'])
    print(json.dumps({'trusted': trusted, 'versions': versions,
                      'results': results, 'entries': entries}, indent=1))
    ok = all(r['match'] for r in results)
    print(f'ORACLE_CELL path={PATH!r} states={len(results)} match={str(ok).lower()}')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
