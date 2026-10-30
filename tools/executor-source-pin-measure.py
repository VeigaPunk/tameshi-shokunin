#!/usr/bin/env python3
"""executor-source-pin-measure: discriminating counter for the executor-source-pin gate.

Round-60 installed successor of the round-59 frozen counter
(`.ufo/evidence/round-59/measure.py`) and its staged candidate
(`.ufo/evidence/round-59/successor/measure-nonce.py`, never frozen). Differences
that close the round-59 routed defects:

* ONE tool invocation per class cell with ALL declared --path values (round-59
  mistake 2: the frozen counter's one-path-per-call shape admitted a
  first-path-only strawman scoring 24/24).
* Per-run nonce fixture contents and commit messages (round-59 mistake 1:
  constant fixtures admitted a fingerprint cheat scoring 24/24).
* Shuffled class order per run (defeats sequence cheats by call index).
* An empty-blob declared path (round-59 attack T59W1S39: the 24 fixtures had no
  empty-blob cell; an empty-blob-unsound tool scored 24/24).
* An exec-bit boundary cell (round-59 spot-check defect 4: the boundary is
  decided -- blob equality is the contract, mode is not bound beyond
  regular-ness -- and the decision is now a tested cell, expected exit 0).
* A corrupt-blob cell expecting EXECUTOR_SOURCE_UNAVAILABLE exit 2 (round-59
  spot-check defect 7: a blob-read plumbing failure maps to exit 2 in tool v2;
  the unfixed v1 tool scores 7/8 with only this cell failing).

PASS label: C1_R60 (the same sentence as plans/round-60.plan.md and
.ufo/evidence/round-60/contract.json).

Stdlib only; git is invoked read-only against the lane repo and write-only
inside the scratch fixture it creates under --work (which must be empty and is
honoured as the scratch root; TMPDIR is passed through to child calls).
"""

import argparse
import json
import os
from pathlib import Path
import random
import secrets
import shutil
import subprocess
import sys

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py',
         'tools/-runner.py', 'tools/empty-fixture.txt']
# The symlink cell targets PATHS[1]; the corrupt cell targets PATHS[3] -- both
# AFTER the first declared path, so a first-path-only strawman fails both.
SYMLINK_PATH = PATHS[1]
CORRUPT_PATH = PATHS[3]

CLASSES = ['equal', 'unrelated', 'execbit', 'changed', 'missing',
           'symlink', 'corrupt', 'unresolvable']
EXPECTED = {'equal': 0, 'unrelated': 0, 'execbit': 0, 'changed': 1,
            'missing': 1, 'symlink': 1, 'corrupt': 2, 'unresolvable': 2}
TOKENS = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT',
          2: 'EXECUTOR_SOURCE_UNAVAILABLE'}

GIT_TIMEOUT = 30


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lane', required=True)
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
    nonce = secrets.token_hex(8)
    nonce2 = secrets.token_hex(8)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))

    def run(argv, **kw):
        return subprocess.run(argv, capture_output=True, text=True, env=env,
                              timeout=GIT_TIMEOUT, **kw)

    def git(repo, *args, text=True):
        return subprocess.run(['git', '-C', str(repo)] + list(args),
                              capture_output=True, text=text, env=env,
                              timeout=GIT_TIMEOUT)

    def git_ok(repo, *args):
        r = git(repo, *args)
        if r.returncode:
            raise RuntimeError('fixture git %s failed: %s' % (args[0], r.stderr))
        return r.stdout.strip()

    def commit_fixture(repo, label):
        git_ok(repo, '-c', 'user.name=fixture', '-c',
               'user.email=fixture@example.invalid', '-c',
               'commit.gpgsign=false', 'commit', '-qm',
               'fixture-%s-%s' % (label, nonce))
        return git_ok(repo, 'rev-parse', 'HEAD')

    rev = git_ok(a.lane, 'rev-parse', '--verify', a.rev + '^{commit}')
    if not a.tool:
        r = run(['git', '-C', a.lane, 'show',
                 rev + ':tools/executor-source-pin.py'])
        if r.returncode:
            print('C1_R60 rev=%s passed=0/%d C1_R60_PASS=false '
                  'reason=tool-absent' % (rev, len(CLASSES)))
            return 1

    results = []
    try:
        tool = Path(a.tool).resolve() if a.tool else work / 'tool.py'
        if not a.tool:
            tool.write_text(r.stdout)
        repo = work / 'fixture'
        repo.mkdir()
        git_ok(repo, 'init', '-q')
        toplevel = Path(git_ok(repo, 'rev-parse', '--show-toplevel')).resolve()
        if toplevel != repo.resolve():
            raise RuntimeError('fixture root mismatch')

        def reset_trusted():
            git_ok(repo, 'reset', '-q', '--hard', trusted)
            git_ok(repo, 'clean', '-qfdx')

        # Trusted commit: the four nonce paths carry nonce bytes, the fifth is
        # the empty blob.
        for ix, path in enumerate(PATHS):
            f = repo / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text('' if ix == len(PATHS) - 1
                         else 'print("trusted %s %s")\n' % (path, nonce))
            git_ok(repo, 'add', '--', path)
        trusted = commit_fixture(repo, 'trusted')

        def candidate(name, mutate):
            reset_trusted()
            mutate()
            git_ok(repo, 'add', '-A')
            return commit_fixture(repo, name)

        versions = {'equal': trusted}

        def m_unrelated():
            (repo / 'unrelated.txt').write_text('unrelated %s\n' % nonce)
        versions['unrelated'] = candidate('unrelated', m_unrelated)

        def m_execbit():
            for ix, path in enumerate(PATHS[:-1]):
                mode = (repo / path).stat().st_mode
                new = (mode | 0o111) if ix % 2 == 0 else (mode & ~0o111)
                os.chmod(repo / path, new)
        versions['execbit'] = candidate('execbit', m_execbit)

        def m_changed():
            for ix, path in enumerate(PATHS):
                f = repo / path
                f.write_text('' if ix == len(PATHS) - 1
                             else 'print("changed %s %s")\n' % (path, nonce2))
        versions['changed'] = candidate('changed', m_changed)

        def m_missing():
            for path in PATHS:
                git_ok(repo, 'rm', '-q', '--', path)
        versions['missing'] = candidate('missing', m_missing)

        def m_symlink():
            f = repo / SYMLINK_PATH
            f.unlink()
            f.symlink_to('elsewhere.py')
        versions['symlink'] = candidate('symlink', m_symlink)

        def m_corrupt():
            f = repo / CORRUPT_PATH
            f.write_text('print("corrupt %s %s")\n' % (CORRUPT_PATH, nonce2))
        versions['corrupt'] = candidate('corrupt', m_corrupt)
        # Delete the candidate blob object for CORRUPT_PATH so a raw
        # `git cat-file blob` of it fails at plumbing level.
        oid = git_ok(repo, 'rev-parse', '%s:%s' % (versions['corrupt'],
                                                   CORRUPT_PATH))
        obj = repo / '.git' / 'objects' / oid[:2] / oid[2:]
        if not obj.exists():
            raise RuntimeError('corrupt cell: object %s is not loose' % oid)
        obj.unlink()
        probe = git(repo, 'cat-file', 'blob', oid)
        if probe.returncode == 0:
            raise RuntimeError('corrupt cell: object still readable')

        versions['unresolvable'] = '0' * 40

        order = random.sample(CLASSES, len(CLASSES))
        for cls in order:
            out = run([sys.executable, '-I', str(tool),
                       '--repo', str(repo),
                       '--trusted', trusted,
                       '--candidate', versions[cls]]
                      + sum((['--path', pth] for pth in PATHS), []))
            expected = EXPECTED[cls]
            token = TOKENS[expected]
            ok = (out.returncode == expected
                  and token in (out.stdout + out.stderr))
            results.append({'class': cls, 'expected': expected,
                            'exit': out.returncode,
                            'stdout': out.stdout.strip()[:400],
                            'stderr': out.stderr.strip()[:400], 'ok': ok})
        passed = sum(1 for x in results if x['ok'])
        print(json.dumps({'nonce': nonce, 'order': order,
                          'results': results}, ensure_ascii=False, indent=1))
        print('C1_R60 rev=%s passed=%d/%d C1_R60_PASS=%s'
              % (rev, passed, len(CLASSES), str(passed == len(CLASSES)).lower()))
        return 0 if passed == len(CLASSES) else 1
    finally:
        for f in list(work.iterdir()):
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()


if __name__ == '__main__':
    sys.exit(main())
