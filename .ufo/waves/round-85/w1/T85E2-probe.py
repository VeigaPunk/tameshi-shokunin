#!/usr/bin/env python3
"""Advisory R85 supplemental CLI probes; never changes the frozen counter.

Use --repo REPO --rev COMMIT for a committed instrument, or --instrument FILE
for a lane-authored proposal. --work must name an absent private scratch path.
A positive preflight prevents an always-reject instrument passing the probes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--rev')
    source.add_argument('--instrument', type=Path)
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--work', required=True, type=Path)
    args = parser.parse_args()
    if args.rev and args.repo is None:
        parser.error('--rev requires --repo')
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1',
               GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')

    def run(argv):
        return subprocess.run(argv, cwd=work, env=env, capture_output=True)

    def checked(argv):
        result = run(argv)
        if result.returncode:
            raise RuntimeError(json.dumps({'argv': list(map(str, argv)),
                                           'exit': result.returncode,
                                           'stderr': result.stderr.decode(errors='replace')}))
        return result.stdout.decode().strip()

    try:
        tool = work / 'instrument.py'
        if args.rev:
            result = run(['git', '-C', str(args.repo.resolve()), 'cat-file', 'blob',
                          args.rev + ':tools/design-blob-audit.py'])
            if result.returncode:
                raise RuntimeError('instrument unavailable at requested revision: ' +
                                   result.stderr.decode(errors='replace'))
            tool.write_bytes(result.stdout)
        else:
            tool.write_bytes(args.instrument.resolve().read_bytes())
        fixture = work / 'fixture'
        fixture.mkdir()
        checked(['git', '-C', str(fixture), 'init', '-q'])

        def git(*argv):
            # Reassert ownership before every fixture operation, including mutations.
            top = checked(['git', '-C', str(fixture), 'rev-parse', '--show-toplevel'])
            if Path(top).resolve() != fixture:
                raise RuntimeError('fixture top-level mismatch')
            return checked(['git', '-C', str(fixture), *argv])

        git('config', 'commit.gpgsign', 'false')
        (fixture / 'tools').mkdir()
        content = b'print(1)\n'
        (fixture / 'tools/toy.py').write_bytes(content)
        git('add', 'tools/toy.py')
        git('commit', '-qm', 'fixture candidate')
        base = git('rev-parse', 'HEAD')
        digest = hashlib.sha256(content).hexdigest()

        def receipt(path='tools/toy.py', sha=digest):
            return ('# design_base: ' + base + '\n# design_tool: ' + path +
                    '\n# design_tool_sha256: ' + sha +
                    '\n# measured_bytes: worktree (uncommitted at design_base)\n')

        for name in ['valid', 'late', 'escape']:
            (fixture / name).mkdir()
        (fixture / 'valid/receipt.txt').write_text(receipt())
        (fixture / 'late/a-valid.txt').write_text(receipt())
        (fixture / 'late/z-malformed.txt').write_text(receipt(sha='bad'))
        (fixture / 'escape/receipt.txt').write_text(receipt(path='../tools/toy.py'))
        git('add', 'valid', 'late', 'escape')
        git('commit', '-qm', 'fixture supplemental receipts')
        receipt_rev = git('rev-parse', 'HEAD')

        def probe(name, root, revision, expected):
            argv = [sys.executable, '-I', str(tool), '--repo', str(fixture),
                    '--receipt-rev', revision, '--root', root, '--candidate-rev', base]
            result = run(argv)
            out = result.stdout.decode(errors='replace')
            ok = result.returncode == expected
            if expected == 2:
                ok = ok and not result.stdout
            else:
                ok = ok and 'state=carried' in out and (
                    'DESIGN_BLOB: receipts=1 carried=1 orphan=0' in out)
            print(json.dumps({'case': name, 'argv': argv, 'exit': result.returncode,
                              'expected': expected, 'ok': ok, 'stdout': out,
                              'stderr': result.stderr.decode(errors='replace')}))
            return ok

        if not probe('positive-preflight', 'valid', receipt_rev, 0):
            print('SUPPLEMENTAL_PREFLIGHT: failed; no supplemental capability credit')
            return 1
        results = [probe('late-malformed-valid-sibling', 'late', receipt_rev, 2),
                   probe('path-escape', 'escape', receipt_rev, 2),
                   probe('missing-receipt-rev', 'valid', '0' * 40, 2)]
        passed = sum(results)
        print('SUPPLEMENTAL_PROBE: cases=3 passed=%d mismatches=%d' % (passed, 3 - passed))
        return 0 if all(results) else 1
    except (OSError, RuntimeError) as error:
        print('SUPPLEMENTAL_ERROR: ' + str(error), file=sys.stderr)
        return 2
    finally:
        shutil.rmtree(work)


if __name__ == '__main__':
    sys.exit(main())
