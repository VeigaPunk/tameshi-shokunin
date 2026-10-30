#!/usr/bin/env python3
"""T59W1S35 probe P5: mini-gate vs commit-level replace refs + four counter path spellings."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S35/lab3')
GIT = shutil.which('git')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_TEMPLATE_DIR='/nonexistent-template', PYTHONDONTWRITEBYTECODE='1')

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

shutil.rmtree(LAB, ignore_errors=True)
LAB.mkdir(parents=True)
repo = LAB / 'p5'
repo.mkdir()
git(repo, 'init', '-q')
top = subprocess.run([GIT, '-C', str(repo), 'rev-parse', '--show-toplevel'],
                     capture_output=True, text=True, env=ENV)
assert Path(top.stdout.strip()).resolve() == repo.resolve(), 'fixture root mismatch'

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
for p in PATHS:
    f = repo / p
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f'print("real executor {p}")\n')
    git(repo, 'add', '--', p)
trusted = commit(repo, 'trusted')
for p in PATHS:
    f = repo / p
    f.write_text(f'print("forged {p}")\n')
    git(repo, 'add', '--', p)
forged = commit(repo, 'forged')
git(repo, 'replace', forged, trusted)  # commit-level replace: candidate commit OID now reads as trusted

BASE = [GIT, '--no-replace-objects', '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false']

def entry(repo, rev, path):
    e = run([*BASE, '-C', str(repo), 'ls-tree', rev, '--', path])
    parts = e['out'].split(None, 3)
    return (parts[0], parts[2]) if len(parts) >= 3 else None

def gate(repo, trusted, candidate, paths):
    r = run([*BASE, '-C', str(repo), 'rev-parse', '--verify', f'{candidate}^{{commit}}'])
    if r['rc'] != 0:
        return 2, 'EXECUTOR_SOURCE_UNAVAILABLE'
    for p in paths:
        if entry(repo, candidate, p) != entry(repo, trusted, p) or entry(repo, candidate, p) is None:
            return 1, 'EXECUTOR_SOURCE_DRIFT'
    return 0, 'EXECUTOR_SOURCE_BOUND'

cases = []
# 1) commit-level replace, vulnerable shape (no --no-replace-objects) vs hardened shape
def gate_noreplace_off(candidate, path):
    e = run([GIT, '-C', str(repo), 'ls-tree', candidate, '--', path])
    parts = e['out'].split(None, 3)
    return (parts[0], parts[2]) if len(parts) >= 3 else None

vuln = all(gate_noreplace_off(forged, p) == entry(repo, trusted, p) for p in PATHS)
rc_h, tok_h = gate(repo, trusted, forged, PATHS)
rc_eq, tok_eq = gate(repo, trusted, trusted, PATHS)
rc_un, tok_un = gate(repo, trusted, '0' * 40, PATHS)
cases.append({'case': 'commit-replace-vulnerable-ls-tree-shows-trusted-oids', 'all_paths_show_trusted': vuln})
cases.append({'case': 'commit-replace-hardened-gate', 'rc': rc_h, 'token': tok_h, 'expected_rc': 1})
cases.append({'case': 'equal-hardened-gate', 'rc': rc_eq, 'token': tok_eq, 'expected_rc': 0})
cases.append({'case': 'unresolvable-hardened-gate', 'rc': rc_un, 'token': tok_un, 'expected_rc': 2})

# 2) per-path spelling check under hardened gate: candidate equal to trusted except exactly one path
for p in PATHS:
    r2 = LAB / ('p5-' + str(PATHS.index(p)))
    r2.mkdir()
    git(r2, 'init', '-q')
    for q in PATHS:
        f = r2 / q
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f'print("real executor {q}")\n')
        git(r2, 'add', '--', q)
    t2 = commit(r2, 'trusted')
    f = r2 / p
    f.write_text(f'print("forged {p}")\n')
    git(r2, 'add', '--', p)
    mixed = commit(r2, f'mixed {p}')
    rc, tok = gate(r2, t2, mixed, PATHS)
    cases.append({'case': f'mixed-drift-{p}', 'rc': rc, 'token': tok, 'expected_rc': 1})
    # equal case for this repo too
    rc0, tok0 = gate(r2, t2, t2, PATHS)
    cases.append({'case': f'equal-{p}-repo', 'rc': rc0, 'token': tok0, 'expected_rc': 0})

print(json.dumps({
    'meta': {'git_version': run([GIT, '--version'])['out'].strip()},
    'trusted': trusted, 'forged': forged,
    'gate_argv_prefix': BASE,
    'cases': cases,
}, ensure_ascii=False, indent=1))
