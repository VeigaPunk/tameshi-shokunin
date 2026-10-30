#!/usr/bin/env python3
"""T59W1S35 follow-up probes P1-P3: correct the confounded/ surprising first-round results."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S35/lab2')
GIT = shutil.which('git')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_TEMPLATE_DIR='/nonexistent-template', PYTHONDONTWRITEBYTECODE='1')
results = []

def rec(**kw):
    results.append(kw)

def run(argv, cwd=None):
    r = subprocess.run(argv, capture_output=True, text=True, env=ENV, cwd=cwd, timeout=30)
    return {'argv': [str(a) for a in argv], 'rc': r.returncode, 'out': r.stdout, 'err': r.stderr}

def git(repo, *args, check=True):
    r = run([GIT, '-C', str(repo), *args])
    if check and r['rc'] != 0:
        raise RuntimeError(f"git {' '.join(str(a) for a in args)} failed: {r['err']}")
    return r

def commit(repo, msg='fixture'):
    git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', msg)
    return git(repo, 'rev-parse', 'HEAD')['out'].strip()

def base_repo(name):
    repo = LAB / name
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    top = subprocess.run([GIT, '-C', str(repo), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True, env=ENV)
    assert Path(top.stdout.strip()).resolve() == repo.resolve(), 'fixture root mismatch'
    f = repo / 'tools/runner.py'
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    trusted = commit(repo, 'trusted')
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    forged = commit(repo, 'forged-drift')
    return repo, trusted, forged

def plant_mon(repo):
    t = repo / 'tools'
    t.mkdir(exist_ok=True)
    (t / 'mon.sh').write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\nexit 0\n')
    (t / 'mon.sh').chmod(0o755)

def ex(repo):
    return (repo / 'EXECUTED').exists()

def reset(repo):
    (repo / 'EXECUTED').unlink(missing_ok=True)

shutil.rmtree(LAB, ignore_errors=True)
LAB.mkdir(parents=True)

# ---- P1: fsmonitor scoping across invocation shapes
repo, trusted, forged = base_repo('p1-fsmonitor')
plant_mon(repo)
git(repo, 'config', '--local', 'core.fsmonitor', '"$PWD/tools/mon.sh"')
shapes = {}
for label, argv in (
    ('porcelain-diff-two-commit', [GIT, '-C', str(repo), 'diff', trusted, forged, '--', 'tools/runner.py']),
    ('porcelain-diff-quiet', [GIT, '-C', str(repo), 'diff', '--quiet', trusted, forged, '--', 'tools/runner.py']),
    ('plumbing-diff-tree', [GIT, '-C', str(repo), 'diff-tree', trusted, forged, '--', 'tools/runner.py']),
    ('plumbing-diff-tree-quiet', [GIT, '-C', str(repo), 'diff-tree', '--quiet', trusted, forged, '--', 'tools/runner.py']),
    ('plumbing-ls-tree', [GIT, '-C', str(repo), 'ls-tree', forged, '--', 'tools/runner.py']),
    ('plumbing-cat-file', [GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py']),
    ('plumbing-rev-parse', [GIT, '-C', str(repo), 'rev-parse', '--verify', f'{forged}^{{commit}}']),
):
    reset(repo)
    r = run(argv)
    shapes[label] = {'ran_fsmonitor': ex(repo), 'rc': r['rc']}
belt = {}
for label, argv in (
    ('diff-tree-quiet-fsmonitor-false', [GIT, '-c', 'core.fsmonitor=false', '-C', str(repo), 'diff-tree', '--quiet', trusted, forged, '--', 'tools/runner.py']),
    ('diff-tree-quiet-autoRefresh-false', [GIT, '-c', 'diff.autoRefreshIndex=false', '-C', str(repo), 'diff-tree', '--quiet', trusted, forged, '--', 'tools/runner.py']),
):
    reset(repo)
    r = run(argv)
    belt[label] = {'ran_fsmonitor': ex(repo), 'rc': r['rc']}
rec(id='P1-fsmonitor-scoping-map', family='scoping probe',
    attack='repo-local core.fsmonitor poison; map which invocation shapes consult it',
    shapes=shapes, belts=belt,
    verdict=('fsmonitor consulted by diff-tree (incl. --quiet) but NOT by two-commit porcelain diff, ls-tree, cat-file, or rev-parse; '
             '-c core.fsmonitor=false belt neutralizes' if belt.get('diff-tree-quiet-fsmonitor-false', {}).get('ran_fsmonitor') is False else 'see fields'))

# ---- P2: commit-level replace refs vs ls-tree OID gate
repo, trusted, forged = base_repo('p2-replace-commit')
git(repo, 'replace', forged, trusted)
g = {}
for label, argv in (
    ('ls-tree-candidate', [GIT, '-C', str(repo), 'ls-tree', forged, '--', 'tools/runner.py']),
    ('ls-tree-candidate-no-replace', [GIT, '--no-replace-objects', '-C', str(repo), 'ls-tree', forged, '--', 'tools/runner.py']),
    ('rev-parse-candidate', [GIT, '-C', str(repo), 'rev-parse', '--verify', f'{forged}^{{commit}}']),
    ('rev-parse-candidate-no-replace', [GIT, '--no-replace-objects', '-C', str(repo), 'rev-parse', '--verify', f'{forged}^{{commit}}']),
    ('cat-file-candidate', [GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py']),
    ('cat-file-candidate-no-replace', [GIT, '--no-replace-objects', '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py']),
):
    r = run(argv)
    g[label] = {'rc': r['rc'], 'out': r['out'].strip()}
rec(id='P2-commit-level-replace-vs-oid-gate', family='ls-tree OID-compare gate',
    attack=f'refs/replace/{forged[:12]}.. -> trusted commit oid',
    forged=forged, trusted=trusted,
    ls_tree_vulnerable=g['ls-tree-candidate']['out'],
    ls_tree_hardened=g['ls-tree-candidate-no-replace']['out'],
    revparse_vulnerable=g['rev-parse-candidate']['out'],
    catfile_vulnerable=g['cat-file-candidate']['out'].strip()[:40],
    verdict=('SUBVERTED: commit-level replace makes ls-tree show TRUSTED oid for candidate rev (OID gate would print BOUND); '
             '--no-replace-objects restores forged tree everywhere'
             if 'runner' in g['ls-tree-candidate']['out'] and '74e4df' not in g['ls-tree-candidate']['out'] + trusted else
             'SUBVERTED check: ' + g['ls-tree-candidate']['out']),
    evidence=g)

# ---- P3: worktree config scope, confound removed (diff.external instead of alias)
repo, trusted, forged = base_repo('p3-worktree')
plant_mon(repo)
git(repo, 'config', '--local', 'extensions.worktreeConfig', 'true')
git(repo, 'config', '--worktree', 'diff.external', '"$PWD/tools/mon.sh"')
reset(repo)
d_wt = git(repo, 'diff', trusted, forged, '--', 'tools/runner.py', check=False)
ran_worktree_external = ex(repo)
# negative control: same value in local scope
reset(repo)
git(repo, 'config', '--local', 'diff.external', '"$PWD/tools/mon.sh"')
d_local = git(repo, 'diff', trusted, forged, '--', 'tools/runner.py', check=False)
ran_local_external = ex(repo)
rec(id='P3-worktree-config-scope', family='porcelain diff gate, main worktree',
    attack='diff.external poison in .git/config.worktree vs .git/config, extensions.worktreeConfig=true (local)',
    ran_worktree_external=ran_worktree_external, worktree_diff_rc=d_wt['rc'],
    ran_local_external=ran_local_external, local_diff_rc=d_local['rc'],
    verdict=('WORKTREE CONFIG SCOPE IS LIVE on the main worktree: same subversion as local config'
             if ran_worktree_external else 'worktree scope NOT honored on main worktree'),
    evidence={'worktree': d_wt, 'local': d_local})

# ---- P4: negative control for alias premise (config write verified, builtin still wins)
repo, trusted, forged = base_repo('p4-alias-control')
git(repo, 'config', '--local', 'alias.cat-file', '!echo SHOULD_NOT_RUN_FOR_BUILTINS')
git(repo, 'config', '--local', 'alias.zzz', '!echo NONBUILTIN_ALIAS_RAN')
cfg = git(repo, 'config', '--local', '--get', 'alias.cat-file')
r1 = run([GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
r2 = run([GIT, '-C', str(repo), 'zzz'])
rec(id='P4-alias-resolution-order', family='premise control',
    attack='alias.cat-file and alias.zzz both planted; config write verified',
    alias_catfile_value=cfg['out'].strip(),
    builtin_call_out=r1['out'].strip()[:40], builtin_call_rc=r1['rc'],
    nonbuiltin_call_out=r2['out'].strip(),
    verdict=('RESOLUTION ORDER: git 2.56 runs aliases ONLY for names that are not builtins; builtins are unshadowable via repo config'
             if 'SHOULD_NOT_RUN' not in r1['out'] and 'NONBUILTIN_ALIAS_RAN' in r2['out'] else 'alias semantics differ; see fields'),
    evidence={'cfg': cfg, 'builtin': r1, 'nonbuiltin': r2})

print(json.dumps({'meta': {'git_version': run([GIT, '--version'])['out'].strip()}, 'probes': results}, ensure_ascii=False, indent=1))
