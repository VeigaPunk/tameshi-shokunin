#!/usr/bin/env python3
"""T59W1S35 adversarial lab: Git config poisoning vs the round-59 executor-source-pin gate design.

Scratch-only fixture driver. Every git mutation happens inside LAB (each fixture
verifies `git rev-parse --show-toplevel` == fixture dir before use). The gate is
emulated by plausible implementation families (porcelain diff/show gate, subprocess
plumbing gate); no production path is touched.

Env mirrors the frozen counter (measure.py): all GIT_* stripped,
GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1. Only repo-local config (and
repo-enabled worktree config / repo-carried refs) remains attacker-reachable.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S35/lab')
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

def assert_toplevel(repo):
    top = subprocess.run([GIT, '-C', str(repo), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True, env=ENV)
    assert top.returncode == 0 and Path(top.stdout.strip()).resolve() == repo.resolve(), 'fixture root mismatch'

def base_repo(name):
    repo = LAB / name
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    assert_toplevel(repo)
    f = repo / 'tools/runner.py'
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    trusted = commit(repo, 'trusted')
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', 'tools/runner.py')
    forged = commit(repo, 'forged-drift')
    return repo, trusted, forged

def plant_tools(repo):
    t = repo / 'tools'
    t.mkdir(exist_ok=True)
    (t / 'faketool.sh').write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\necho FAKE-UNIFORM-OUTPUT\n')
    (t / 'always-zero.sh').write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\nexit 0\n')
    (t / 'spoof-cat-file.sh').write_text(
        '#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\n'
        'for a in "$@"; do case "$a" in -s) echo 100; exit 0;; -t) echo blob; exit 0;; esac; done\n'
        'echo "spoofed-blob-content-that-matches-nothing"\n')
    (t / 'real-cat-file.sh').write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\nexit 0\n')
    for s in t.glob('*.sh'):
        s.chmod(0o755)
    h = repo / '.git' / 'hooks'
    h.mkdir(exist_ok=True)
    (h / 'post-checkout').write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\n')
    (h / 'post-checkout').chmod(0o755)

def executed(repo):
    return (repo / 'EXECUTED').exists()

def reset_state(repo):
    (repo / 'EXECUTED').unlink(missing_ok=True)

shutil.rmtree(LAB, ignore_errors=True)
LAB.mkdir(parents=True)
meta = {'git': GIT, 'git_version': run([GIT, '--version'])['out'].strip(),
        'lab': str(LAB), 'counter_env_git_keys': sorted(k for k in ENV if k.startswith('GIT_')),
        'python': sys.version.split()[0]}

# ================================================================ A0: premise probes
repo, trusted, forged = base_repo('a0-premise')
plant_tools(repo)
git(repo, 'config', '--local', 'alias.st', '!echo ALIAS_RAN')
r = git(repo, 'st', check=False)
rec(id='A0a-alias-shadows-builtin', family='premise',
    attack='repo-local [alias] st = !cmd, invoked as `git st`',
    observed=r['out'].strip(), rc=r['rc'],
    verdict='PREMISE CONFIRMED: aliases shadow builtins' if 'ALIAS_RAN' in r['out'] else 'alias did not shadow builtin')
reset_state(repo)
git(repo, 'config', '--local', 'alias.cat-file', '!"$PWD/tools/real-cat-file.sh"')
r = run([GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
rec(id='A0b-alias-shadows-cat-file', family='premise',
    attack="repo-local [alias] cat-file = !cmd, invoked as argv ['git','-C',repo,'cat-file',...] (subprocess family)",
    observed=r['out'].strip(), rc=r['rc'], executed=executed(repo),
    verdict=('PREMISE CONFIRMED: subprocess plumbing family hijackable via repo-local alias, no shell/env needed'
             if executed(repo) else 'alias did NOT intercept subprocess argv cat-file'),
    evidence=r)
reset_state(repo)

# ================================================================ A1: textconv (committed .gitattributes in candidate)
repo, trusted, forged = base_repo('a1-textconv')
plant_tools(repo)
git(repo, 'config', '--local', 'diff.runner.textconv', '"$PWD/tools/faketool.sh"')
# candidate commit carries the driver mapping itself -> fully self-contained adversarial candidate
(repo / '.gitattributes').write_text('tools/runner.py diff=runner\n')
git(repo, 'add', '--', '.gitattributes')
cand = commit(repo, 'forged+gitattributes')
d_human = git(repo, 'diff', trusted, cand, '--', 'tools/runner.py', check=False)
d_quiet = git(repo, 'diff', '--quiet', trusted, cand, '--', 'tools/runner.py', check=False)
subverted = executed(repo) and d_human['rc'] == 0
rec(id='A1-textconv-vs-porcelain-diff', family='porcelain diff gate (git diff T C -- path)',
    attack='candidate commit carries .gitattributes mapping path to driver; repo-local diff.<drv>.textconv rewrites blob content',
    candidate=cand, textconv_executed=executed(repo), human_diff_rc=d_human['rc'],
    human_diff_out=d_human['out'].strip(), quiet_diff_rc=d_quiet['rc'],
    verdict=('SUBVERTED: textconv ran and porcelain diff reports NO difference between trusted and forged blob (rc 0)'
             if subverted else 'not subverted via this invocation shape; see fields'),
    evidence={'human': d_human, 'quiet': d_quiet})
reset_state(repo)

# ================================================================ A2: diff.external
repo, trusted, forged = base_repo('a2-extdiff')
plant_tools(repo)
git(repo, 'config', '--local', 'diff.external', '"$PWD/tools/always-zero.sh"')
d_human = git(repo, 'diff', trusted, forged, '--', 'tools/runner.py', check=False)
d_quiet = git(repo, 'diff', '--quiet', trusted, forged, '--', 'tools/runner.py', check=False)
rec(id='A2-diff-external-vs-porcelain-diff', family='porcelain diff gate',
    attack='repo-local diff.external diverts diff work to attacker command exiting 0',
    external_executed=executed(repo), human_diff_rc=d_human['rc'],
    human_diff_out=d_human['out'].strip(), quiet_diff_rc=d_quiet['rc'],
    verdict=('SUBVERTED: attacker external diff invoked; porcelain diff empty (rc 0) despite real blob drift'
             if executed(repo) and d_human['rc'] == 0 else 'not subverted via this invocation shape'),
    evidence={'human': d_human, 'quiet': d_quiet})
reset_state(repo)

# ================================================================ A3: full alias hijack of the naive plumbing gate
repo, trusted, forged = base_repo('a3-alias-hijack')
plant_tools(repo)
git(repo, 'config', '--local', 'alias.cat-file', '!"$PWD/tools/spoof-cat-file.sh"')
git(repo, 'config', '--local', 'alias.rev-parse', '!echo 0b50e8455ab46f7344149582ee672b83eb5ea7f3')
r_blob = run([GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
r_size = run([GIT, '-C', str(repo), 'cat-file', '-s', f'{forged}:tools/runner.py'])
r_rev = run([GIT, '-C', str(repo), 'rev-parse', '--verify', f'{forged}^{{commit}}'])
rec(id='A3-alias-hijack-plumbing-gate', family="subprocess plumbing gate ([git cat-file blob c:path], [git rev-parse --verify c^{commit}])",
    attack='repo-local [alias] cat-file=!spoof, [alias] rev-parse=!echo <attacker-oid>',
    spoofed_content=(r_blob['out'].strip() == 'spoofed-blob-content-that-matches-nothing'),
    spoofed_size=(r_size['out'].strip() == '100'),
    spoofed_rev=(r_rev['out'].strip() == '0b50e8455ab46f7344149582ee672b83eb5ea7f3'),
    executed=executed(repo),
    verdict=('SUBVERTED: content, size, and commit-resolution channels all attacker-scriptable from repo-local config'
             if executed(repo) and r_blob['out'].strip().startswith('spoofed') else 'not subverted'),
    evidence={'blob': r_blob, 'size': r_size, 'rev': r_rev})
reset_state(repo)

# ================================================================ A4: fsmonitor scoping (porcelain vs plumbing)
repo, trusted, forged = base_repo('a4-fsmonitor')
plant_tools(repo)
git(repo, 'config', '--local', 'core.fsmonitor', '"$PWD/tools/always-zero.sh"')
s = git(repo, 'status', '--porcelain', check=False)
d = git(repo, 'diff', '--quiet', trusted, forged, '--', 'tools/runner.py', check=False)
reset_state(repo)
p = git(repo, 'diff-tree', '--quiet', trusted, forged, '--', 'tools/runner.py', check=False)
rec(id='A4-fsmonitor-scoping', family='scoping probe',
    attack='repo-local core.fsmonitor external command',
    ran_on_status=executed(repo), status_rc=s['rc'],
    note='positive control: status refreshes index; porcelain/plumbing diff scoping probed in A4b',
    evidence={'status': s})
reset_state(repo)
d2 = git(repo, 'diff', trusted, forged, '--', 'tools/runner.py', check=False)
ran_porcelain = executed(repo)
reset_state(repo)
p = git(repo, 'diff-tree', '--quiet', trusted, forged, '--', 'tools/runner.py', check=False)
ran_plumbing = executed(repo)
rec(id='A4b-fsmonitor-porcelain-vs-plumbing', family='scoping probe',
    attack='same core.fsmonitor repo; porcelain `git diff T C` vs plumbing `git diff-tree --quiet T C`',
    ran_on_porcelain_diff=ran_porcelain, porcelain_diff_rc=d2['rc'],
    ran_on_plumbing=ran_plumbing, plumbing_diff_rc=p['rc'],
    verdict=('fsmonitor executes for porcelain diff (index refresh) but NOT for tree-to-tree plumbing'
             if ran_porcelain and not ran_plumbing else 'scoping result differs; see fields'),
    evidence={'porcelain': d2, 'plumbing': p})

# ================================================================ A5: hooks vs plumbing reads
repo, trusted, forged = base_repo('a5-hooks')
plant_tools(repo)
c = git(repo, 'cat-file', 'blob', f'{forged}:tools/runner.py')
l = git(repo, 'ls-tree', forged, '--', 'tools/runner.py')
rec(id='A5-hooks-vs-plumbing', family='subprocess plumbing gate',
    attack='post-checkout hook planted; cat-file + ls-tree reads',
    executed=executed(repo), blob_has_forged=('forged success' in c['out']),
    lstree=l['out'].strip(),
    verdict='IMMUNE: cat-file/ls-tree run no hooks' if not executed(repo) else 'NOT immune',
    evidence={'cat-file': c, 'ls-tree': l})

# ================================================================ A6: worktree config blade (extensions-gated)
repo, trusted, forged = base_repo('a6-worktree')
plant_tools(repo)
git(repo, 'config', '--local', 'extensions.worktreeConfig', 'true')
git(repo, 'config', '--worktree', 'alias.cat-file', '!"$PWD/tools/real-cat-file.sh"')
r = run([GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
rec(id='A6-worktree-config-blade', family='subprocess plumbing gate, main worktree',
    attack='poison only in .git/config.worktree, local config additionally enables extensions.worktreeConfig',
    executed=executed(repo),
    verdict=('WORKTREE CONFIG LIVE: attacker who controls local config can route poison through config.worktree too'
             if executed(repo) else 'worktree blade inert in this layout'),
    evidence=r)
reset_state(repo)

# ================================================================ A7: belt candidates against alias shadowing
repo, trusted, forged = base_repo('a7-belts')
plant_tools(repo)
git(repo, 'config', '--local', 'alias.cat-file', '!"$PWD/tools/spoof-cat-file.sh"')
b1 = run([GIT, '-c', 'alias.cat-file=', '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
reset_state(repo)
b2 = run([GIT, '-c', 'alias.cat-file=cat-file', '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
reset_state(repo)
b3 = run([GIT, '--no-replace-objects', '-c', 'alias.cat-file=', '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
rec(id='A7-alias-neutralization-belts', family='belt probe',
    attack='same alias-poisoned repo; belts: B1 `-c alias.cat-file=`, B2 `-c alias.cat-file=cat-file`, B3 `--no-replace-objects -c alias.cat-file=`',
    B1_rc=b1['rc'], B1_out=b1['out'].strip()[:80], B1_executed=executed(repo),
    B2_rc=b2['rc'], B2_err=b2['err'].strip()[:120],
    B3_out=b3['out'].strip()[:80],
    verdict=('B1 (empty -c override) neutralizes alias: builtin runs, forged content returned'
             if (not executed(repo) or True) and 'forged success' in b1['out'] else 'B1 failed'),
    evidence={'B1': b1, 'B2': b2, 'B3': b3})
reset_state(repo)

# ================================================================ A8: counter env scope verification
r8 = run([GIT, 'config', '--global', '--list', '--show-origin'])
r8b = run([GIT, 'config', '--system', '--list', '--show-origin'])
r8c = git(repo, 'config', '--local', '--list')
rec(id='A8-counter-env-scopes', family='counter (measure.py) environment inventory',
    attack='measure which config scopes remain live under counter-sanitized env',
    global_rc=r8['rc'], global_out=r8['out'].strip(), system_rc=r8b['rc'], system_err=r8b['err'].strip()[:120],
    local_lines=len(r8c['out'].strip().splitlines()),
    verdict=('global neutralized (points at /dev/null), system neutralized -> repo-local config is THE live poisoning scope'
             if not r8['out'].strip() and r8b['rc'] != 0 else 'scope inventory unexpected'),
    evidence={'global': r8, 'system': r8b, 'local_tail': r8c['out'].strip().splitlines()[-8:]})

# ================================================================ A9: adjacent repo-carried poison: replace refs
repo, trusted, forged = base_repo('a9-replace-refs')
plant_tools(repo)
# attacker swaps forged blob -> trusted blob content via refs/replace
tb = git(repo, 'rev-parse', f'{trusted}:tools/runner.py')['out'].strip()
fb = git(repo, 'rev-parse', f'{forged}:tools/runner.py')['out'].strip()
git(repo, 'replace', fb, tb)
vuln = run([GIT, '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
hardened = run([GIT, '--no-replace-objects', '-C', str(repo), 'cat-file', 'blob', f'{forged}:tools/runner.py'])
l = git(repo, 'ls-tree', forged, '--', 'tools/runner.py')
rec(id='A9-replace-refs-adjacent', family='subprocess plumbing gate (cat-file byte compare)',
    attack=f'refs/replace/{fb[:12]}.. -> trusted blob oid; candidate commit untouched',
    trusted_blob=tb, forged_blob=fb,
    vulnerable_read=vuln['out'].strip(), hardened_read=hardened['out'].strip(),
    lstree=l['out'].strip(),
    verdict=('SUBVERTED without --no-replace-objects: forged blob reads as TRUSTED content (byte-compare gate prints BOUND); '
             '`--no-replace-objects` restores real content' if 'real executor' in vuln['out'] and 'forged success' in hardened['out']
             else 'replace-refs behavior differs; see fields'),
    evidence={'vulnerable': vuln, 'hardened': hardened, 'ls-tree': l})

# ================================================================ A10: minimal sound gate emulation under poisoned repo
repo, trusted, forged = base_repo('a10-mini-gate')
plant_tools(repo)
(repo / '.gitattributes').write_text('tools/runner.py diff=runner\n')
git(repo, 'add', '--', '.gitattributes')
cand = commit(repo, 'forged+attributes')
# poison AFTER the last commit: fsmonitor poison also breaks `git commit` itself
# (observed: "warning: Empty last update token" -> commit aborts), a repo-operation DoS blade.
git(repo, 'config', '--local', 'alias.cat-file', '!"$PWD/tools/spoof-cat-file.sh"')
git(repo, 'config', '--local', 'alias.ls-tree', '!echo SPOOFED-LSTREE')
git(repo, 'config', '--local', 'alias.rev-parse', '!echo deadbeef')
git(repo, 'config', '--local', 'diff.external', '"$PWD/tools/always-zero.sh"')
git(repo, 'config', '--local', 'core.fsmonitor', '"$PWD/tools/always-zero.sh"')
git(repo, 'config', '--local', 'diff.runner.textconv', '"$PWD/tools/faketool.sh"')

def mini_gate(repo, trusted, candidate, path):
    """ls-tree OID+mode compare; alias-belt on every builtin used; no replace objects."""
    belt = ['-c', 'alias.rev-parse=', '-c', 'alias.ls-tree=']
    base = [GIT, '--no-replace-objects', *belt]
    r = run([*base, '-C', str(repo), 'rev-parse', '--verify', f'{candidate}^{{commit}}'])
    if r['rc'] != 0:
        return 2, 'EXECUTOR_SOURCE_UNAVAILABLE', r
    def entry(rev):
        e = run([*base, '-C', str(repo), 'ls-tree', rev, '--', path])
        parts = e['out'].split(None, 3)
        return (parts[0], parts[2]) if len(parts) >= 3 else None
    t, cnd = entry(trusted), entry(candidate)
    if t is None or cnd is None or t != cnd:
        return 1, 'EXECUTOR_SOURCE_DRIFT', (t, cnd)
    return 0, 'EXECUTOR_SOURCE_BOUND', (t, cnd)

cases = []
for label, cand_arg in (('equal', trusted), ('forged-drift', cand), ('unresolvable', '0' * 40)):
    rc, token, detail = mini_gate(repo, trusted, cand_arg, 'tools/runner.py')
    cases.append({'case': label, 'rc': rc, 'token': token,
                  'expected': 0 if label == 'equal' else 2 if label == 'unresolvable' else 1,
                  'detail': str(detail)})
all_ok = all(c['rc'] == c['expected'] for c in cases)
rec(id='A10-mini-gate-under-full-poison', family='emulated minimal sound gate (ls-tree oid+mode compare)',
    attack='repo poisoned simultaneously: alias cat-file/ls-tree/rev-parse, diff.external, core.fsmonitor, textconv+gitattributes',
    executed_during_gate=executed(repo), cases=cases,
    verdict=('SOUND UNDER FULL POISON: all three cases exit as spec (0/1/2) with zero attacker command executions'
             if all_ok and not executed(repo) else 'gate misbehaved under poison; see cases'),
    evidence=None)

summary = {
    'meta': meta,
    'axes_named': ['soundness/always-accept-resistance', 'fidelity-to-frozen-counter',
                   'claim-boundary precision', 'operability of proposed CLI test'],
    'demonstrations': results,
}
print(json.dumps(summary, ensure_ascii=False, indent=1))
