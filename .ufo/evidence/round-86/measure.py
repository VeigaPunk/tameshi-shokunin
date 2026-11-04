#!/usr/bin/env python3
"""measure.py — round-86 frozen counter for the design-receipt audit capability.

Successor of the round-85 frozen counter (`.ufo/evidence/round-85/measure.py`),
which certified `tools/design-blob-audit.py` at 8/8 while a no-git basename
oracle reached the same 8/8 (round-85 closure routed defect 1; QUALITY
criterion 111). This counter closes exactly that gap and nothing else:

* per-run nonce fixture paths, bytes and commit messages — a fingerprint cheat
  that recognises round-85's constant fixture text has nothing to recognise;
* shuffled case order per run — a sequence cheat keyed by invocation index
  cannot line up with the expected per-case exits;
* expected rows are DATA-DERIVED: for every design receipt the counter reads
  the candidate tree and the candidate blob itself and computes the expected
  state (carried/different/absent/nonregular) plus the expected summary from
  that read, never from a hand-written token list;
* the comparison is the COMPLETE anchored output: the exact stdout lines, in
  sorted receipt-path order, each carrying the `DESIGN_BLOB_ROW <path>
  state=<state>` prefix, and the exact `DESIGN_BLOB: receipts=N carried=C
  orphan=O` summary; exit-2 cases must carry no stdout at all. A counterfeit
  that prints only a summary, or that reads the `--root` label instead of the
  candidate objects, cannot match.

The instrument contract is the one `tools/design-blob-audit.py` declares:
`--repo REPO --receipt-rev REV --root RELATIVE_DIR --candidate-rev REV`.

PASS label: `C1_R86` — the same sentence in `plans/round-86.plan.md` and in
the round-86 SCORECARD record.

Stdlib only; git is invoked read-only against the lane repo and write-only
inside the scratch fixture created under --work (which must be empty and is
honoured as the scratch root; TMPDIR is passed through to child calls).
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import secrets
import shutil
import subprocess
import sys

CASES = ['carried', 'mixed', 'malformed-sha', 'incomplete-marker',
         'mixed-headers', 'zero-population', 'absolute-root',
         'unresolvable-candidate']
GIT_TIMEOUT = 60
IDENTITY = ('-c', 'user.name=tameshi-fixture',
            '-c', 'user.email=tameshi@shokunin.local',
            '-c', 'commit.gpgsign=false')
DESIGN_MARKER = '# measured_bytes: worktree (uncommitted at design_base)'


def lane_env(extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1')
    if extra:
        env.update(extra)
    return env


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--work', required=True,
                   help='empty scratch directory for fixtures (required)')
    p.add_argument('--tool', help='control executable override; '
                                  'never used for certification')
    a = p.parse_args()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        p.error('--work must be empty')
    nonce = secrets.token_hex(6)
    nonce2 = secrets.token_hex(6)
    env = lane_env({'TMPDIR': str(work)})

    def run(argv):
        return subprocess.run(argv, capture_output=True, text=True, env=env,
                              timeout=GIT_TIMEOUT)

    def git(repo, *args):
        r = subprocess.run(['git', '-C', str(repo)] + list(args),
                           capture_output=True, text=True, env=env,
                           timeout=GIT_TIMEOUT)
        if r.returncode:
            raise RuntimeError('fixture git %s failed: %s'
                               % (args[0], r.stderr.strip()[:200]))
        return r.stdout.strip()

    rev = git(a.repo, 'rev-parse', '--verify', a.rev + '^{commit}')
    if not a.tool:
        r = run(['git', '-C', a.repo, 'show',
                 rev + ':tools/design-blob-audit.py'])
        if r.returncode:
            print('C1_R86 rev=%s passed=0/%d C1_R86_PASS=false '
                  'reason=tool-absent' % (rev, len(CASES)))
            return 1

    results = []
    try:
        tool = Path(a.tool).resolve() if a.tool else work / 'tool.py'
        if not a.tool:
            tool.write_text(r.stdout)
        repo = work / 'fixture'
        repo.mkdir()
        git(repo, 'init', '-q')
        if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo.resolve():
            raise RuntimeError('fixture root mismatch')

        def put(rel, data):
            f = repo / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(data if isinstance(data, bytes)
                          else data.encode('utf-8'))

        def commit(label):
            git(repo, *IDENTITY, 'add', '-A')
            git(repo, *IDENTITY, 'commit', '-q', '-m',
                'fixture-%s-%s' % (label, nonce))
            return git(repo, 'rev-parse', 'HEAD')

        # ---- base commit: the tool blobs the receipts declare ------------
        tools = {}
        for tag in ('a', 'b', 'c', 'd'):
            rel = 'tools/tool-%s-%s.py' % (tag, nonce)
            body = 'print("fixture %s %s")\n' % (tag, nonce)
            put(rel, body)
            tools[tag] = (rel, hashlib.sha256(body.encode()).hexdigest())
        base = commit('base')

        def receipt(root, name, tool_rel, sha, base_rev=None, marker=True,
                    extra=(), sha_text=None):
            lines = ['# receipt: %s %s' % (name, nonce),
                     '# design_base: %s' % (base_rev or base),
                     '# design_tool: %s' % tool_rel,
                     '# design_tool_sha256: %s'
                     % (sha_text if sha_text is not None else sha)]
            if marker:
                lines.append(DESIGN_MARKER)
            lines.extend(extra)
            put('%s/%s.txt' % (root, name), '\n'.join(lines) + '\n')

        ok_root = 'pop/ok-%s' % nonce
        mx_root = 'pop/mx-%s' % nonce
        rf_root = 'pop/rf-%s' % nonce
        zp_root = 'pop/zp-%s' % nonce

        # carried population: three receipts, all tools carried by base
        for i, tag in enumerate(('a', 'b', 'c')):
            receipt(ok_root, 'rc%d-%s' % (i, nonce2), tools[tag][0],
                    tools[tag][1])
        # mixed population: carried + different + absent + nonregular
        receipt(mx_root, 'ma-%s' % nonce2, tools['a'][0], tools['a'][1])
        receipt(mx_root, 'mb-%s' % nonce2, tools['b'][0], tools['b'][1])
        receipt(mx_root, 'mc-%s' % nonce2, 'tools/gone-%s.py' % nonce,
                tools['c'][1])
        receipt(mx_root, 'md-%s' % nonce2, 'tools/link-%s.py' % nonce,
                tools['d'][1])
        # refusal populations: one bad receipt each, in its own root
        receipt(rf_root + '-sha', 'rs-%s' % nonce2, tools['a'][0],
                tools['a'][1], sha_text='deadbeef')
        receipt(rf_root + '-inc', 'ri-%s' % nonce2, tools['a'][0],
                tools['a'][1], marker=False)
        receipt(rf_root + '-mix', 'rm-%s' % nonce2, tools['a'][0],
                tools['a'][1], extra=('# measured_rev: %s' % base,))
        # zero population: a normal receipt only
        put('%s/normal-%s.txt' % (zp_root, nonce2),
            '# measured_rev: %s\n# tool: tools/tool-a-%s.py\n'
            '# tool_sha256: %s\n# measured_bytes_rev: %s\n'
            % (base, nonce, tools['a'][1], base))
        receipt_rev = commit('receipts')

        # ---- candidate commit: differ / remove / replace by symlink ------
        put(tools['b'][0], 'print("changed %s")\n' % nonce2)
        git(repo, 'rm', '-q', '--', tools['c'][0])
        (repo / tools['d'][0]).unlink()
        (repo / tools['d'][0]).symlink_to('elsewhere-%s.py' % nonce)
        (repo / ('tools/link-%s.py' % nonce)).symlink_to('target-%s.py' % nonce)
        cand = commit('candidate')

        # ---- data-derived expectations ----------------------------------
        trees = {}

        def tree_for(rev):
            if rev not in trees:
                entries = {}
                for line in git(repo, 'ls-tree', '-r', rev).splitlines():
                    meta, path = line.split('\t', 1)
                    mode, otype, oid = meta.split()
                    entries[path] = (mode, otype, oid)
                trees[rev] = entries
            return trees[rev]
        REGULAR = ('100644', '100755')

        def expected_rows(root, receipt_revs, cand_rev):
            tree = tree_for(cand_rev)
            rows = []
            carried = 0
            for path in sorted(receipt_revs):
                tool_rel, declared = receipt_revs[path]
                entry = tree.get(tool_rel)
                if entry is None:
                    state = 'absent'
                elif entry[0] not in REGULAR or entry[1] != 'blob':
                    state = 'nonregular'
                else:
                    blob = subprocess.run(
                        ['git', '-C', str(repo), 'cat-file', 'blob',
                         entry[2]], capture_output=True, env=env,
                        timeout=GIT_TIMEOUT)
                    if blob.returncode:
                        raise RuntimeError('fixture blob unreadable')
                    state = ('carried' if hashlib.sha256(blob.stdout).hexdigest()
                             == declared else 'different')
                carried += state == 'carried'
                rows.append('DESIGN_BLOB_ROW %s state=%s' % (path, state))
            rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=%d'
                        % (len(receipt_revs), carried,
                           len(receipt_revs) - carried))
            return '\n'.join(rows)

        ok_receipts = {'%s/rc%d-%s.txt' % (ok_root, i, nonce2): tools[t]
                       for i, t in enumerate(('a', 'b', 'c'))}
        mx_receipts = {
            '%s/ma-%s.txt' % (mx_root, nonce2): tools['a'],
            '%s/mb-%s.txt' % (mx_root, nonce2): tools['b'],
            '%s/mc-%s.txt' % (mx_root, nonce2):
                ('tools/gone-%s.py' % nonce, tools['c'][1]),
            '%s/md-%s.txt' % (mx_root, nonce2):
                ('tools/link-%s.py' % nonce, tools['d'][1]),
        }
        expectations = {
            'carried': (0, expected_rows(ok_root, ok_receipts, base)),
            'mixed': (1, expected_rows(mx_root, mx_receipts, cand)),
            'malformed-sha': (2, ''),
            'incomplete-marker': (2, ''),
            'mixed-headers': (2, ''),
            'zero-population': (2, ''),
            'absolute-root': (2, ''),
            'unresolvable-candidate': (2, ''),
        }
        argv = {
            'carried': [ok_root, base],
            'mixed': [mx_root, cand],
            'malformed-sha': [rf_root + '-sha', base],
            'incomplete-marker': [rf_root + '-inc', base],
            'mixed-headers': [rf_root + '-mix', base],
            'zero-population': [zp_root, base],
            'absolute-root': [str(repo), base],
            'unresolvable-candidate': [ok_root, '0' * 40],
        }

        order = random.sample(CASES, len(CASES))
        for cls in order:
            root, cand_rev = argv[cls]
            out = run([sys.executable, '-I', str(tool),
                       '--repo', str(repo),
                       '--receipt-rev', receipt_rev,
                       '--root', root,
                       '--candidate-rev', cand_rev])
            want_exit, want_out = expectations[cls]
            got_out = out.stdout.rstrip('\n')
            ok = (out.returncode == want_exit and got_out == want_out)
            results.append({'case': cls, 'expected_exit': want_exit,
                            'exit': out.returncode,
                            'expected_stdout': want_out[:600],
                            'stdout': got_out[:600],
                            'stderr': out.stderr.strip()[:300], 'ok': ok})
        passed = sum(1 for x in results if x['ok'])
        print(json.dumps({'nonce': nonce, 'order': order,
                          'results': results}, ensure_ascii=False, indent=1))
        print('C1_R86 rev=%s passed=%d/%d C1_R86_PASS=%s'
              % (rev, passed, len(CASES),
                 str(passed == len(CASES)).lower()))
        return 0 if passed == len(CASES) else 1
    finally:
        for f in list(work.iterdir()):
            if f.is_dir() and not f.is_symlink():
                shutil.rmtree(f)
            else:
                f.unlink()


if __name__ == '__main__':
    sys.exit(main())
