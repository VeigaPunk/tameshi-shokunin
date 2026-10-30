#!/usr/bin/env python3
"""Independent fixture builder for seat T59W1S11, cell path='tools/space name.py'.
Mirrors frozen measure.py fixture construction exactly (all six versions), then
runs the independent oracle against each. Receipts written under --out."""
import argparse, json, os, subprocess, sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    work = Path(a.work).resolve()
    out = Path(a.out).resolve()
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))
    path = 'tools/space name.py'

    def run(argv, **kw):
        return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)
    def git(repo, *args):
        r = run(['git', '-C', str(repo), *args])
        if r.returncode:
            raise RuntimeError(f'git {args}: {r.stderr}')
        return r.stdout.strip()

    repo = work / 'fixture-space'
    repo.mkdir()
    git(repo, 'init', '-q')
    toplevel = Path(git(repo, 'rev-parse', '--show-toplevel')).resolve()
    assert toplevel == repo, f'fixture root mismatch: {toplevel} != {repo}'

    f = repo / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', path)

    def commit():
        git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        return git(repo, 'rev-parse', 'HEAD')

    versions = {'equal': commit()}
    # object evidence at trusted
    trusted_meta = {
        'rev': versions['equal'],
        'cat_file_t': git(repo, 'cat-file', '-t', f'{versions["equal"]}:{path}'),
        'ls_tree': git(repo, 'ls-tree', versions['equal'], '--', path),
        'show': git(repo, 'show', f'{versions["equal"]}:{path}'),
    }
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', path)
    versions['changed'] = commit()
    changed_show = git(repo, 'show', f'{versions["changed"]}:{path}')
    f.unlink()
    git(repo, 'add', '-u')
    versions['missing'] = commit()
    missing_lstree = git(repo, 'ls-tree', versions['missing'], '--', path)
    f.write_text('print("real executor")\n')
    (repo / 'unrelated.txt').write_text('unrelated change\n')
    git(repo, 'add', '--', path, 'unrelated.txt')
    versions['unrelated'] = commit()
    unrelated_show = git(repo, 'show', f'{versions["unrelated"]}:{path}')
    versions['unresolvable'] = '0' * 40
    # evidence: candidate does not resolve
    probe = run(['git', '-C', str(repo), 'rev-parse', '--verify', versions['unresolvable'] + '^{commit}'])
    unresolvable_probe = {'argv': ['git', '-C', str(repo), 'rev-parse', '--verify', versions['unresolvable'] + '^{commit}'],
                          'returncode': probe.returncode, 'stdout': probe.stdout, 'stderr': probe.stderr}
    f.unlink()
    f.symlink_to('elsewhere.py')
    git(repo, 'add', '--', path)
    versions['symlink'] = commit()
    symlink_lstree = git(repo, 'ls-tree', versions['symlink'], '--', path)

    # independent oracle: classify (repo, trusted, candidate, path) from first principles
    def oracle(repo, trusted, candidate, path):
        # candidate must resolve to a commit
        r = run(['git', '-C', str(repo), 'rev-parse', '--verify', candidate + '^{commit}'])
        if r.returncode != 0:
            return 2, 'EXECUTOR_SOURCE_UNAVAILABLE'
        # declared path must exist as a regular file blob at candidate and equal trusted blob
        t = run(['git', '-C', str(repo), 'cat-file', '-t', f'{candidate}:{path}'])
        if t.returncode != 0 or t.stdout.strip() != 'blob':
            return 1, 'EXECUTOR_SOURCE_DRIFT'
        tb = run(['git', '-C', str(repo), 'show', f'{trusted}:{path}'])
        cb = run(['git', '-C', str(repo), 'show', f'{candidate}:{path}'])
        if tb.returncode != 0 or cb.returncode != 0 or tb.stdout != cb.stdout:
            return 1, 'EXECUTOR_SOURCE_DRIFT'
        return 0, 'EXECUTOR_SOURCE_BOUND'

    expected = {'equal': (0, 'EXECUTOR_SOURCE_BOUND'), 'changed': (1, 'EXECUTOR_SOURCE_DRIFT'),
                'missing': (1, 'EXECUTOR_SOURCE_DRIFT'), 'unrelated': (0, 'EXECUTOR_SOURCE_BOUND'),
                'unresolvable': (2, 'EXECUTOR_SOURCE_UNAVAILABLE'), 'symlink': (1, 'EXECUTOR_SOURCE_DRIFT')}
    oracle_results = {}
    for cls, cand in versions.items():
        rc, tok = oracle(repo, versions['equal'], cand, path)
        oracle_results[cls] = {'candidate': cand, 'oracle_exit': rc, 'oracle_token': tok,
                               'expected_exit': expected[cls][0], 'expected_token': expected[cls][1],
                               'match': (rc, tok) == expected[cls]}

    receipt = {
        'path': path,
        'repo': str(repo),
        'toplevel_assert': str(toplevel),
        'versions': versions,
        'trusted_meta': trusted_meta,
        'changed_show': changed_show,
        'missing_ls_tree': missing_lstree,
        'unrelated_show': unrelated_show,
        'unresolvable_probe': unresolvable_probe,
        'symlink_ls_tree': symlink_lstree,
        'oracle_results': oracle_results,
    }
    (out / 'fixture-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=1))
    print(json.dumps(receipt, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    sys.exit(main())
