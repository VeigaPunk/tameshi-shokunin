#!/usr/bin/env python3
"""measure.py — round-87 frozen counter for `tools/design-blob-audit.py`.

Successor of the round-86 counter (`.ufo/evidence/round-86/measure.py`, killed
by its own kill rule at attempt 3: two counterfeits, `T86E2-att3b-cheat.py`
and `T86CN1-oracle-worktree.py`, each reach `passed=8/8`; lesson
`corpus/lessons/round-86.md` M3). The round-86 counter is NOT amended; this file
is a new freeze that closes the four routed classes and nothing else:

* OPAQUE LABELS. Fixture roots and receipt file names are per-run random
  tokens with no class substring. A root-label oracle has no class to read.
* FIXTURE WORKTREE OFF THE CANDIDATE. After the candidate commit, the fixture
  worktree is checked out at the RECEIPT revision, so the on-disk bytes differ
  from the candidate tree in every mixed-case tool. A worktree-reading oracle
  therefore cannot agree with the candidate-tree expectation.
* EXACT OUTPUT AND STDERR. Stdout must equal the expected complete anchored
  output byte for byte (no `rstrip` tolerance). Exit-2 cases must print empty
  stdout and a stderr line beginning `design-blob-audit: setup refusal`;
  exit 0/1 cases must print empty stderr.
* PINNED GIT. Every git call in this process and every child tool call uses
  the git resolved ONCE from /usr/bin:/bin (never the caller's PATH), and the
  child environment's PATH is pinned to those directories.

Certification: `python3 -I .ufo/evidence/round-87/measure.py --repo LANE
--rev REV --work EMPTY_DIR`. Predicate (the same sentence appears in
`plans/round-87.plan.md` and in the receipt):

    C1_R87 rev=<rev> passed=8/8 C1_R87_PASS=true

Controls are run with `--tool CONTROL.py` (never for certification). A control
must print `C1_R87_PASS=false`; a control printing `passed=8/8` kills the claim.

Stdlib only. Git is read-only against the lane repo and write-only inside the
fixture created under --work (which must be empty; it is also TMPDIR for every
child). Exit: 0 pass, 1 not all cases pass, 2 setup refusal.
"""

import argparse
import hashlib
import json
import os
import random
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

CASES = ['carried', 'mixed', 'malformed-sha', 'incomplete-marker',
         'mixed-headers', 'zero-population', 'absolute-root',
         'unresolvable-candidate']
TRUSTED_DIRS = ('/usr/bin', '/bin')
GIT_TIMEOUT = 60
IDENTITY = ('-c', 'user.name=tameshi-fixture',
            '-c', 'user.email=tameshi@shokunin.local',
            '-c', 'commit.gpgsign=false')
DESIGN_MARKER = '# measured_bytes: worktree (uncommitted at design_base)'
REGULAR = ('100644', '100755')
REFUSAL_PREFIX = 'design-blob-audit: setup refusal'


def trusted_git():
    path = shutil.which('git', path=os.pathsep.join(TRUSTED_DIRS))
    if not path:
        raise SystemExit('measure: git not found in trusted dirs')
    return path


GIT = None


def child_env(work):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(PATH=os.pathsep.join(TRUSTED_DIRS), TMPDIR=str(work),
               GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_NO_REPLACE_OBJECTS='1', PYTHONDONTWRITEBYTECODE='1')
    return env


def main():
    global GIT
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--work', required=True,
                   help='empty scratch directory (required; TMPDIR for children)')
    p.add_argument('--tool', help='control executable; never for certification')
    a = p.parse_args()
    GIT = trusted_git()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        sys.stderr.write('measure: --work must be empty\n')
        return 2
    env = child_env(work)
    nonce = secrets.token_hex(8)

    def git_run(*args, cwd=None):
        return subprocess.run([GIT] + list(args), cwd=cwd,
                              capture_output=True, text=True, env=env,
                              timeout=GIT_TIMEOUT)

    def git(repo, *args):
        r = git_run('-C', str(repo), *args)
        if r.returncode:
            raise RuntimeError('fixture git %s failed: %s'
                               % (args[0], r.stderr.strip()[:200]))
        return r.stdout.strip()

    try:
        rev = git_run('-C', a.repo, 'rev-parse', '--verify',
                      a.rev + '^{commit}').stdout.strip()
        if not rev:
            print('C1_R87 rev=%s passed=0/%d C1_R87_PASS=false reason=rev-unresolvable'
                  % (a.rev, len(CASES)))
            return 1
        if a.tool:
            tool_bytes = Path(a.tool).read_bytes()
        else:
            shown = git_run('-C', a.repo, 'show', rev + ':tools/design-blob-audit.py')
            if shown.returncode:
                print('C1_R87 rev=%s passed=0/%d C1_R87_PASS=false reason=tool-absent'
                      % (rev, len(CASES)))
                return 1
            tool_bytes = shown.stdout.encode('utf-8')
        results = []
        repo = work / 'fixture'
        repo.mkdir()
        git(repo, 'init', '-q')
        if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo.resolve():
            raise RuntimeError('fixture root mismatch')
        tool = work / 'tool-under-test.py'
        tool.write_bytes(tool_bytes)

        def put(rel, data):
            f = repo / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))

        def commit(label):
            git(repo, *IDENTITY, 'add', '-A')
            git(repo, *IDENTITY, 'commit', '-q', '--allow-empty', '-m',
                'fixture-%s-%s' % (label, nonce))
            return git(repo, 'rev-parse', 'HEAD')

        def tok():
            return secrets.token_hex(5)

        # ---- base: the tool blobs the receipts declare --------------------
        tools = {}
        for _ in range(4):
            rel = 'tools/t-%s.py' % tok()
            body = 'print("fixture %s")\n' % tok()
            put(rel, body)
            tools[len(tools)] = (rel, hashlib.sha256(body.encode()).hexdigest())
        base = commit('base')

        def receipt(root, tool_rel, sha, base_rev=None, marker=True,
                    extra=(), sha_text=None):
            lines = ['# receipt: %s' % tok(),
                     '# design_base: %s' % (base_rev or base),
                     '# design_tool: %s' % tool_rel,
                     '# design_tool_sha256: %s'
                     % (sha_text if sha_text is not None else sha)]
            if marker:
                lines.append(DESIGN_MARKER)
            lines.extend(extra)
            name = '%s/%s.txt' % (root, tok())
            put(name, '\n'.join(lines) + '\n')
            return name

        roots = {c: 'pop/%s' % tok() for c in CASES}
        ok_root = roots['carried']
        mx_root = roots['mixed']
        rf_sha = roots['malformed-sha']
        rf_inc = roots['incomplete-marker']
        rf_mix = roots['mixed-headers']
        zp_root = roots['zero-population']

        ok_receipts = {}
        for idx in (0, 1, 2):
            tool_rel, sha = tools[idx]
            ok_receipts[receipt(ok_root, tool_rel, sha)] = (tool_rel, sha)
        mx_receipts = {}
        mx_receipts[receipt(mx_root, tools[0][0], tools[0][1])] = tools[0]
        mx_receipts[receipt(mx_root, tools[1][0], tools[1][1])] = tools[1]
        gone = 'tools/g-%s.py' % tok()
        mx_receipts[receipt(mx_root, gone, tools[2][1])] = (gone, tools[2][1])
        link = 'tools/l-%s.py' % tok()
        mx_receipts[receipt(mx_root, link, tools[3][1])] = (link, tools[3][1])
        receipt(rf_sha, tools[0][0], tools[0][1], sha_text='deadbeef')
        receipt(rf_inc, tools[0][0], tools[0][1], marker=False)
        receipt(rf_mix, tools[0][0], tools[0][1], extra=('# measured_rev: %s' % base,))
        put('%s/%s.txt' % (zp_root, tok()),
            '# measured_rev: %s\n# tool: %s\n# tool_sha256: %s\n# measured_bytes_rev: %s\n'
            % (base, tools[0][0], tools[0][1], base))
        receipt_rev = commit('receipts')

        # ---- candidate: differ / remove / replace by symlink -------------
        put(tools[1][0], 'print("changed %s")\n' % tok())
        git(repo, 'rm', '-q', '--', tools[2][0])
        (repo / tools[3][0]).unlink()
        (repo / tools[3][0]).symlink_to('elsewhere-%s.py' % tok())
        (repo / link).symlink_to('target-%s.py' % tok())
        cand = commit('candidate')

        # ---- fixture worktree forced OFF the candidate tree ---------------
        git(repo, 'checkout', '-q', '--detach', receipt_rev)
        if git(repo, 'rev-parse', 'HEAD') == cand:
            raise RuntimeError('worktree not forced off candidate')

        # ---- data-derived expectations from committed objects only -------
        trees = {}

        def tree_for(rev_):
            if rev_ not in trees:
                entries = {}
                for line in git(repo, 'ls-tree', '-r', rev_).splitlines():
                    meta, path = line.split('\t', 1)
                    mode, otype, oid = meta.split()
                    entries[path] = (mode, otype, oid)
                trees[rev_] = entries
            return trees[rev_]

        def expected(receipts, cand_rev):
            tree = tree_for(cand_rev)
            rows, carried = [], 0
            for path in sorted(receipts):
                tool_rel, declared = receipts[path]
                entry = tree.get(tool_rel)
                if entry is None:
                    state = 'absent'
                elif entry[0] not in REGULAR or entry[1] != 'blob':
                    state = 'nonregular'
                else:
                    blob = subprocess.run([GIT, '-C', str(repo), 'cat-file', 'blob',
                                           entry[2]], capture_output=True, env=env,
                                          timeout=GIT_TIMEOUT)
                    if blob.returncode:
                        raise RuntimeError('fixture blob unreadable')
                    state = ('carried' if hashlib.sha256(blob.stdout).hexdigest()
                             == declared else 'different')
                carried += state == 'carried'
                rows.append('DESIGN_BLOB_ROW %s state=%s' % (path, state))
            rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=%d'
                        % (len(receipts), carried, len(receipts) - carried))
            return '\n'.join(rows)

        exp = {
            'carried': (0, expected(ok_receipts, base), ok_root, base),
            'mixed': (1, expected(mx_receipts, cand), mx_root, cand),
            'malformed-sha': (2, '', rf_sha, base),
            'incomplete-marker': (2, '', rf_inc, base),
            'mixed-headers': (2, '', rf_mix, base),
            'zero-population': (2, '', zp_root, base),
            'absolute-root': (2, '', str(repo), base),
            'unresolvable-candidate': (2, '', ok_root, '0' * 40),
        }
        order = random.SystemRandom().sample(CASES, len(CASES))
        for cls in order:
            want_exit, want_out, root, cand_rev = exp[cls]
            proc = subprocess.run([sys.executable, '-I', str(tool),
                                   '--repo', str(repo), '--receipt-rev', receipt_rev,
                                   '--root', root, '--candidate-rev', cand_rev],
                                  capture_output=True, text=True, env=env,
                                  timeout=GIT_TIMEOUT, cwd=str(work))
            want_stdout = want_out + ('\n' if want_out else '')
            if want_exit == 2:
                want_err_ok = proc.stderr.startswith(REFUSAL_PREFIX)
            else:
                want_err_ok = proc.stderr == ''
            ok = (proc.returncode == want_exit and proc.stdout == want_stdout
                  and want_err_ok)
            results.append({'case': cls, 'expected_exit': want_exit,
                            'exit': proc.returncode, 'stdout_match': proc.stdout == want_stdout,
                            'stderr_ok': want_err_ok, 'ok': ok,
                            'stderr': proc.stderr.strip()[:160]})
        passed = sum(1 for r in results if r['ok'])
        print(json.dumps({'order': order, 'results': results}, indent=1))
        print('C1_R87 rev=%s passed=%d/%d C1_R87_PASS=%s'
              % (rev, passed, len(CASES), str(passed == len(CASES)).lower()))
        return 0 if passed == len(CASES) else 1
    except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
        sys.stderr.write('measure: setup refusal %s\n' % exc)
        return 2
    finally:
        for f in list(work.iterdir()):
            if f.is_dir() and not f.is_symlink():
                shutil.rmtree(f, ignore_errors=True)
            else:
                f.unlink()


if __name__ == '__main__':
    sys.exit(main())
