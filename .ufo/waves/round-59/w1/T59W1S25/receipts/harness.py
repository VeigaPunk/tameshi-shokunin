#!/usr/bin/env python3
"""T59W1S25 adversarial harness: 'trusted revision invalid' attack surface.

Builds Git fixtures with primitives only, then runs a bounded matrix of
invalid/edge trusted revisions against a gate tool copy. Emits JSON receipts.
Never touches anything outside its scratch root (given as argv[1]).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

SCRATCH = Path(sys.argv[1]).resolve()
FIX = SCRATCH / 'fixtures'
UNAV = 'EXECUTOR_SOURCE_UNAVAILABLE'
DRIFT = 'EXECUTOR_SOURCE_DRIFT'
BOUND = 'EXECUTOR_SOURCE_BOUND'


def sh(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                          timeout=30)


def git(repo, *args):
    r = sh(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError('git %s: %s' % (args, r.stderr))
    return r.stdout.strip()


def commit_all(repo, msg):
    git(repo, '-c', 'user.name=fixture', '-c', 'user.email=f@e.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', msg)
    return git(repo, 'rev-parse', 'HEAD')


def build_fixtures():
    if FIX.exists():
        subprocess.run(['rm', '-rf', str(FIX)], check=True)
    FIX.mkdir(parents=True)
    repo = FIX / 'fx'
    repo.mkdir()
    git(repo, 'init', '-q')
    top = git(repo, 'rev-parse', '--show-toplevel')
    assert Path(top).resolve() == repo.resolve(), 'fixture root mismatch: %s' % top
    f = repo / 'tools' / 'runner.py'
    f.parent.mkdir(parents=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    trusted = commit_all(repo, 'trusted real')
    versions = {'trusted': trusted,
                'tree': git(repo, 'rev-parse', 'HEAD^{tree}'),
                'blob': git(repo, 'rev-parse', 'HEAD:tools/runner.py')}
    git(repo, 'tag', '-a', 'v1', '-m', 'annotated trusted', trusted)
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    versions['changed'] = commit_all(repo, 'changed')
    f.unlink()
    git(repo, 'add', '-u')
    versions['nofile'] = commit_all(repo, 'trusted source absent')
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    commit_all(repo, 'restore')
    f.unlink()
    f.symlink_to('elsewhere.py')
    git(repo, 'add', '--', 'tools/runner.py')
    versions['syn'] = commit_all(repo, 'trusted source symlink')
    git(repo, 'rm', '--cached', '-q', '--', 'tools/runner.py')
    f.unlink()
    git(repo, 'update-index', '--add', '--cacheinfo',
        '160000,1234567890123456789012345678901234567890,tools/runner.py')
    versions['gitlink'] = commit_all(repo, 'trusted source gitlink')
    repo2 = FIX / 'fx2'
    repo2.mkdir()
    git(repo2, 'init', '-q')
    assert Path(git(repo2, 'rev-parse', '--show-toplevel')).resolve() == repo2.resolve()
    (repo2 / 'other.txt').write_text('other repo\n')
    git(repo2, 'add', '--', 'other.txt')
    versions['foreign'] = commit_all(repo2, 'foreign repo commit')
    return str(repo), versions


def run_tool(tool, repo, trusted, candidate, path='tools/runner.py'):
    r = sh([sys.executable, '-I', str(tool), '--repo', repo,
            '--trusted', trusted, '--candidate', candidate, '--path', path])
    return {'rc': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}


def main():
    tool = Path(sys.argv[2]).resolve()
    repo, v = build_fixtures()
    Z = '0' * 40
    # (label, trusted, candidate, expected_rc or None=observe, expected_token or None)
    cases = [
        ('garbage', 'not-a-revision', v['trusted'], 2, UNAV),
        ('empty', '', v['trusted'], 2, UNAV),
        ('zeros40', Z, v['trusted'], 2, UNAV),
        ('tree-hash', v['tree'], v['trusted'], 2, UNAV),
        ('blob-hash', v['blob'], v['trusted'], 2, UNAV),
        ('abbrev7', v['trusted'][:7], v['trusted'], None, None),
        ('uppercase', v['trusted'].upper(), v['trusted'], 2, UNAV),
        ('trailing-newline', v['trusted'] + '\n', v['trusted'], 2, UNAV),
        ('leading-space', ' ' + v['trusted'], v['trusted'], 2, UNAV),
        ('head-ref', 'HEAD', v['trusted'], None, BOUND),
        ('annotated-tag', 'v1', v['trusted'], None, BOUND),
        ('trusted-src-absent', v['nofile'], v['trusted'], 2, UNAV),
        ('trusted-src-symlink', v['syn'], v['trusted'], 2, UNAV),
        ('trusted-src-gitlink', v['gitlink'], v['trusted'], 2, UNAV),
        ('foreign-repo-sha', v['foreign'], v['trusted'], 2, UNAV),
        ('option-like-h', '-h', v['trusted'], 2, UNAV),
        ('option-like-long', '--exec=evil', v['trusted'], 2, UNAV),
        ('long-1000', 'A' * 1000, v['trusted'], 2, UNAV),
        ('tilde-beyond', 'HEAD~50', v['trusted'], 2, UNAV),
        ('cand-zeros-control', v['trusted'], Z, 2, UNAV),
        ('both-invalid', Z, Z, 2, UNAV),
        ('repo-missing', v['trusted'], v['trusted'], 2, UNAV),
    ]
    out = {'tool': str(tool), 'repo': repo, 'versions': v, 'cases': []}
    for label, tr, cand, erc, etok in cases:
        rrepo = '/nonexistent-xyz' if label == 'repo-missing' else repo
        r = run_tool(tool, rrepo, tr, cand)
        combined = r['stdout'] + r['stderr']
        if erc is None:
            verdict = 'observe'
        else:
            verdict = 'ok' if (r['rc'] == erc and etok in combined) else 'VIOLATION'
        out['cases'].append({'label': label, 'trusted': tr[:80],
                             'expected_rc': erc, 'expected_token': etok,
                             'rc': r['rc'], 'stdout': r['stdout'][:400],
                             'stderr': r['stderr'][:400], 'verdict': verdict})
    viol = [c for c in out['cases'] if c['verdict'] == 'VIOLATION']
    out['violations'] = len(viol)
    dest = SCRATCH / 'receipts' / ('attack-%s.json' % Path(tool).stem)
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print('tool=%s violations=%d receipt=%s' % (tool, len(viol), dest))
    for c in out['cases']:
        print('  %-22s rc=%-3s exp=%-4s %s' % (c['label'], c['rc'],
              c['expected_rc'], c['verdict']))


if __name__ == '__main__':
    main()
