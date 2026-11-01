#!/usr/bin/env python3
"""executor-source-pin-measure-v2: host-portable revision of the round-60
discriminating counter.

Round-60 attempt-2 revision of `tools/executor-source-pin-measure.py` (the
frozen round-60 instrument, whose certification receipts are Linux-host
receipts). The cell set, declared paths, expected exits, invocation shape
(one tool invocation per cell, all --path values), per-run nonce fixtures
and shuffled class order are byte-for-byte the same design as the frozen
instrument; only host-portability plumbing differs:

* fixture bytes are written with explicit UTF-8 (the frozen instrument
  relies on the interpreter's locale encoding, which is cp1252 under
  `-I` on Windows-native CPython and cannot encode the 日本語 fixture
  path content: UnicodeEncodeError, receipt
  `.ufo/evidence/round-60/win-host/red-v1-counter.err`);
* the child tool invocation carries `-X utf8` (a no-op on POSIX, where
  UTF-8 is already the default) so the child's stdio encoding cannot
  depend on the host codepage;
* the exec-bit cell forces the index modes with
  `git update-index --chmod=±x` after `git add -A` (with
  `core.fileMode=false` — the git-for-windows default — a worktree chmod
  alone never reaches the commit, and the candidate commit collapses to
  the trusted tree);
* `reset_trusted` clears the Windows read-only attribute before
  `git reset --hard` (git-for-windows writes loose objects read-only and
  leaves content-unchanged worktree files untouched, so a read-only
  attribute set by one cell leaks into the next);
* the corrupt cell clears the read-only attribute before deleting the
  loose object (os.unlink on a read-only file fails on Windows);
* the fixture cleanup clears the read-only attribute on failure
  (shutil.rmtree hit PermissionError on `.git/objects/**` — the second
  failure in `red-v1-counter.err`).

PASS label: C1_R60V2 (the same predicate as C1_R60; the distinct label
records which instrument revision produced a receipt).

Stdlib only; git is invoked read-only against the lane repo and write-only
inside the scratch fixture it creates under --work (which must be empty and is
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


def write_utf8(path, text):
    """Write fixture bytes as UTF-8 regardless of the host locale codec."""
    path.write_bytes(text.encode('utf-8'))


def _force_remove(func, path, _exc):
    """rmtree/onexc-onerror helper: clear the read-only bit, then retry."""
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass
    try:
        func(path)
    except OSError:
        pass


def rmtree_force(path):
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_force_remove)
    else:
        shutil.rmtree(path, onerror=_force_remove)


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
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))
    try:
        instrument = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        instrument = 'unknown'

    def run(argv, **kw):
        return subprocess.run(argv, capture_output=True, text=True, env=env,
                              encoding='utf-8', timeout=GIT_TIMEOUT, **kw)

    def git(repo, *args, text=True):
        return subprocess.run(['git', '-C', str(repo)] + list(args),
                              capture_output=True, text=text, env=env,
                              encoding='utf-8' if text else None,
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
            print('C1_R60V2 rev=%s passed=0/%d C1_R60V2_PASS=false '
                  'reason=tool-absent' % (rev, len(CLASSES)))
            return 1

    results = []
    try:
        tool = Path(a.tool).resolve() if a.tool else work / 'tool.py'
        if not a.tool:
            tool.write_bytes(r.stdout.encode('utf-8', 'surrogateescape'))
        repo = work / 'fixture'
        repo.mkdir()
        git_ok(repo, 'init', '-q')
        toplevel = Path(git_ok(repo, 'rev-parse', '--show-toplevel')).resolve()
        if toplevel != repo.resolve():
            raise RuntimeError('fixture root mismatch')

        def clear_readonly():
            # git-for-windows leaves content-unchanged worktree files
            # untouched by reset --hard; a read-only attribute set in an
            # earlier cell (the exec-bit cell's `& ~0o111`) would otherwise
            # break unlink/write in later cells. 0644 is the normal state on
            # POSIX too, so this is a no-op there.
            for path in PATHS:
                f = repo / path
                if f.exists() or f.is_symlink():
                    try:
                        os.chmod(f, 0o644)
                    except OSError:
                        pass

        def reset_trusted():
            clear_readonly()
            git_ok(repo, 'reset', '-q', '--hard', trusted)
            git_ok(repo, 'clean', '-qfdx')

        # Trusted commit: the four nonce paths carry nonce bytes, the fifth is
        # the empty blob.
        for ix, path in enumerate(PATHS):
            f = repo / path
            f.parent.mkdir(parents=True, exist_ok=True)
            write_utf8(f, '' if ix == len(PATHS) - 1
                       else 'print("trusted %s %s")\n' % (path, nonce))
            git_ok(repo, 'add', '--', path)
        trusted = commit_fixture(repo, 'trusted')

        def candidate(name, mutate, post_add=None):
            reset_trusted()
            mutate()
            git_ok(repo, 'add', '-A')
            if post_add is not None:
                post_add()
            return commit_fixture(repo, name)

        versions = {'equal': trusted}

        def m_unrelated():
            write_utf8(repo / 'unrelated.txt', 'unrelated %s\n' % nonce)
        versions['unrelated'] = candidate('unrelated', m_unrelated)

        def m_execbit():
            # Worktree chmod: same shape as the frozen instrument. The
            # index-mode force below is the host-portable part: with
            # core.fileMode=false (git-for-windows default) the chmod alone
            # never reaches a commit, and the candidate would collapse to
            # the trusted tree.
            for ix, path in enumerate(PATHS[:-1]):
                mode = (repo / path).stat().st_mode
                new = (mode | 0o111) if ix % 2 == 0 else (mode & ~0o111)
                os.chmod(repo / path, new)
        versions['execbit'] = candidate(
            'execbit', m_execbit,
            post_add=lambda: [git_ok(repo, 'update-index', '--chmod=' +
                                     ('+x' if ix % 2 == 0 else '-x'),
                                     '--', path)
                              for ix, path in enumerate(PATHS[:-1])])

        def m_changed():
            for ix, path in enumerate(PATHS):
                f = repo / path
                write_utf8(f, '' if ix == len(PATHS) - 1
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
            write_utf8(f, 'print("corrupt %s %s")\n' % (CORRUPT_PATH, nonce2))
        versions['corrupt'] = candidate('corrupt', m_corrupt)
        # Delete the candidate blob object for CORRUPT_PATH so a raw
        # `git cat-file blob` of it fails at plumbing level. git-for-windows
        # writes loose objects with the read-only attribute set; clear it or
        # the unlink fails on Windows.
        oid = git_ok(repo, 'rev-parse', '%s:%s' % (versions['corrupt'],
                                                   CORRUPT_PATH))
        obj = repo / '.git' / 'objects' / oid[:2] / oid[2:]
        if not obj.exists():
            raise RuntimeError('corrupt cell: object %s is not loose' % oid)
        try:
            os.chmod(obj, 0o644)
        except OSError:
            pass
        obj.unlink()
        probe = git(repo, 'cat-file', 'blob', oid)
        if probe.returncode == 0:
            raise RuntimeError('corrupt cell: object still readable')

        versions['unresolvable'] = '0' * 40

        order = random.sample(CLASSES, len(CLASSES))
        for cls in order:
            out = run([sys.executable, '-I', '-X', 'utf8', str(tool),
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
        # ensure_ascii=True: the receipt must survive any host stdio codec
        # (the frozen instrument used ensure_ascii=False, which assumes a
        # UTF-8 stdio).
        print(json.dumps({'instrument': instrument, 'nonce': nonce,
                          'order': order,
                          'results': results}, ensure_ascii=True, indent=1))
        print('C1_R60V2 rev=%s passed=%d/%d C1_R60V2_PASS=%s'
              % (rev, passed, len(CLASSES), str(passed == len(CLASSES)).lower()))
        return 0 if passed == len(CLASSES) else 1
    finally:
        for f in list(work.iterdir()):
            if f.is_dir():
                rmtree_force(f)
            else:
                f.unlink()


if __name__ == "__main__":
    sys.exit(main())
