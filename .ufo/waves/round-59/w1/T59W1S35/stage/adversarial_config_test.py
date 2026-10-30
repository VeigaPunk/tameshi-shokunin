#!/usr/bin/env python3
"""T59W1S35 staged CLI test: Git config / repo-metadata poisoning of the
round-59 executor-source-pin gate, exercised through the FROZEN CLI interface:

    python3 TOOL --repo REPO --trusted COMMIT --candidate COMMIT --path PATH [--path PATH ...]

Exit/token map (contract.json):
    0 + EXECUTOR_SOURCE_BOUND        all declared blobs equal trusted blobs
    1 + EXECUTOR_SOURCE_DRIFT        declared source differs / missing / nonregular
    2 + EXECUTOR_SOURCE_UNAVAILABLE  bad args, invalid trusted, unresolvable candidate

This test does NOT claim any candidate implementation exists. It takes the tool
under test via --tool and reports pass/fail per poisoned fixture. It writes only
under --work (must be empty). Usage:

    python3 adversarial_config_test.py --tool TOOL --work EMPTYDIR [--porcelain-selfcheck-only]

Design notes (all blades demonstrated empirically on git 2.56.0, see receipts):
  * textconv: candidate commit carries .gitattributes mapping each declared path
    to a driver; repo-local diff.<drv>.textconv rewrites blob content; subverts
    porcelain diff INCLUDING --quiet (observed rc 0 on forged blobs).
  * diff.external: repo-local (or config.worktree) diff.external diverts human
    porcelain diff to a command exiting 0 (observed rc 0, command executed).
  * replace refs: refs/replace/<candidate> -> trusted commit makes even
    `git ls-tree <candidate>` show TRUSTED oids (subverts OID-compare gates);
    blob-level replace subverts cat-file content gates.
  * fsmonitor/alias/hooks: command-execution blades; fsmonitor fires under
    diff-tree (not ls-tree/cat-file/rev-parse); hooks don't fire for plumbing;
    aliases never shadow builtins (git 2.56) but must stay a non-goal anyway.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
TOKENS = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT', 2: 'EXECUTOR_SOURCE_UNAVAILABLE'}
GIT = shutil.which('git')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool', required=True, help='gate implementation under test (python file)')
    ap.add_argument('--work', required=True, help='empty scratch dir for fixtures')
    a = ap.parse_args()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        ap.error('--work must be empty')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))
    tool = Path(a.tool).resolve()
    results = []

    def run(argv, cwd=None):
        return subprocess.run(argv, capture_output=True, text=True, env=env, cwd=cwd, timeout=30)

    def git(repo, *args, check=True):
        r = run([GIT, '-C', str(repo), *args])
        if check and r.returncode:
            raise RuntimeError(f'git {args}: {r.stderr}')
        return r

    def commit(repo, msg):
        git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', msg)
        return git(repo, 'rev-parse', 'HEAD').stdout.strip()

    def new_repo(name):
        repo = work / name
        repo.mkdir()
        git(repo, 'init', '-q')
        top = run([GIT, '-C', str(repo), 'rev-parse', '--show-toplevel'])
        assert Path(top.stdout.strip()).resolve() == repo.resolve(), 'fixture root mismatch'
        for p in PATHS:
            f = repo / p
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(f'print("real executor {p}")\n')
        git(repo, 'add', '--', *PATHS)
        return repo, commit(repo, 'trusted')

    def forge(repo):
        for p in PATHS:
            (repo / p).write_text(f'print("forged success {p}")\n')
        git(repo, 'add', '--', *PATHS)
        return commit(repo, 'forged')

    def plant_monitor(repo):
        t = repo / 'tools' / '_mon.sh'
        t.write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\necho FAKE-UNIFORM\n')
        t.chmod(0o755)
        return t

    def call_tool(repo, trusted, candidate, paths):
        r = run([sys.executable, '-I', str(tool), '--repo', str(repo),
                 '--trusted', trusted, '--candidate', candidate,
                 *sum((['--path', p] for p in paths), [])])
        return {'rc': r.returncode, 'out': r.stdout, 'err': r.stderr,
                'token_ok': any(TOKENS.get(r.returncode, '') in s for s in (r.stdout, r.stderr))}

    def check(name, repo, trusted, candidate, expect_rc, paths=PATHS, assert_no_exec=False, selfcheck=None):
        res = call_tool(repo, trusted, candidate, paths)
        executed = (repo / 'EXECUTED').exists()
        (repo / 'EXECUTED').unlink(missing_ok=True)
        ok = res['rc'] == expect_rc and res['token_ok'] and (not assert_no_exec or not executed)
        results.append({'fixture': name, 'expected_rc': expect_rc, **res,
                        'attacker_command_executed': executed, 'ok': ok, 'selfcheck': selfcheck})
        return ok

    # ---- fixture 1: textconv poison, fully self-contained adversarial candidate
    repo, trusted = new_repo('f1-textconv')
    plant_monitor(repo)
    git(repo, 'config', '--local', 'diff.pin.textconv', '"$PWD/tools/_mon.sh"')
    (repo / '.gitattributes').write_text(''.join(f'"{p}" diff=pin\n' if ' ' in p else f'{p} diff=pin\n' for p in PATHS))
    git(repo, 'add', '--', '.gitattributes')
    cand = forge(repo)
    sc = run([GIT, '-C', str(repo), 'diff', '--quiet', trusted, cand, '--', *PATHS])
    live = sc.returncode == 0 and (repo / 'EXECUTED').exists()
    (repo / 'EXECUTED').unlink(missing_ok=True)
    check('textconv+gitattributes-candidate', repo, trusted, cand, 1,
          selfcheck={'porcelain_diff_quiet_rc': sc.returncode, 'poison_live': live})

    # ---- fixture 2: diff.external in local config
    repo, trusted = new_repo('f2-extdiff-local')
    plant_monitor(repo)
    git(repo, 'config', '--local', 'diff.external', '"$PWD/tools/_mon.sh"')
    cand = forge(repo)
    sc = run([GIT, '-C', str(repo), 'diff', trusted, cand, '--', *PATHS])
    live2 = sc.returncode == 0 and (repo / 'EXECUTED').exists()
    (repo / 'EXECUTED').unlink(missing_ok=True)
    check('diff-external-local-config', repo, trusted, cand, 1,
          selfcheck={'porcelain_diff_rc': sc.returncode, 'poison_live': live2})

    # ---- fixture 3: diff.external in config.worktree (local enables extension)
    repo, trusted = new_repo('f3-extdiff-worktree')
    plant_monitor(repo)
    git(repo, 'config', '--local', 'extensions.worktreeConfig', 'true')
    git(repo, 'config', '--worktree', 'diff.external', '"$PWD/tools/_mon.sh"')
    cand = forge(repo)
    sc = run([GIT, '-C', str(repo), 'diff', trusted, cand, '--', *PATHS])
    live3 = sc.returncode == 0 and (repo / 'EXECUTED').exists()
    (repo / 'EXECUTED').unlink(missing_ok=True)
    check('diff-external-worktree-config', repo, trusted, cand, 1,
          selfcheck={'porcelain_diff_rc': sc.returncode, 'poison_live': live3})

    # ---- fixture 4: commit-level replace refs
    repo, trusted = new_repo('f4-replace-commit')
    cand = forge(repo)
    git(repo, 'replace', cand, trusted)
    sc = run([GIT, '-C', str(repo), 'ls-tree', cand, '--', PATHS[0]])
    st = run([GIT, '-C', str(repo), 'ls-tree', trusted, '--', PATHS[0]])
    check('replace-refs-commit-level', repo, trusted, cand, 1,
          selfcheck={'vulnerable_ls_tree_first_line': sc.stdout.splitlines()[0] if sc.stdout else '',
                     'poison_live': sc.stdout == st.stdout and sc.stdout != ''})
    git(repo, 'replace', '-d', cand)

    # ---- fixture 5: combined execution blades (fsmonitor + alias + hooks) with drift
    repo, trusted = new_repo('f5-exec-blades')
    plant_monitor(repo)
    cand = forge(repo)  # commit BEFORE fsmonitor poison (it would run/break the commit itself)
    git(repo, 'config', '--local', 'core.fsmonitor', '"$PWD/tools/_mon.sh"')
    git(repo, 'config', '--local', 'alias.cat-file', '!"$PWD/tools/_mon.sh"')
    h = repo / '.git' / 'hooks' / 'post-checkout'
    h.write_text('#!/bin/sh\necho invoked >> "$PWD/EXECUTED"\n')
    h.chmod(0o755)
    check('fsmonitor-alias-hooks-drift', repo, trusted, cand, 1, assert_no_exec=True)

    # ---- controls
    repo, trusted = new_repo('c1-equal')
    check('control-equal', repo, trusted, trusted, 0)
    check('control-unresolvable', repo, trusted, '0' * 40, 2)
    check('control-bad-trusted', repo, '0' * 40, trusted, 2)
    repo, trusted = new_repo('c2-partial-drift')
    (repo / PATHS[1]).write_text('print("forged one path")\n')
    git(repo, 'add', '--', PATHS[1])
    cand = commit(repo, 'partial drift')
    check('control-partial-drift-all-paths', repo, trusted, cand, 1)
    check('control-partial-drift-single-declared-path', repo, trusted, cand, 1, paths=[PATHS[1]])
    check('control-partial-drift-undeclared-path', repo, trusted, cand, 0, paths=[PATHS[0]])

    passed = sum(r['ok'] for r in results)
    print(json.dumps(results, ensure_ascii=False, indent=1))
    print(f'T59W1S35_CLI_TEST passed={passed}/{len(results)} '
          f'T59W1S35_CLI_TEST_PASS={str(passed == len(results)).lower()}')
    return 0 if passed == len(results) else 1

if __name__ == '__main__':
    sys.exit(main())
