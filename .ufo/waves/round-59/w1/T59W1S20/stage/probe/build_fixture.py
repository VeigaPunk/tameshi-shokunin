#!/usr/bin/env python3
"""Independent fixture builder for cell path='tools/-runner.py', frozen round59 measure.py.

Replicates ONLY the fixture construction the frozen counter performs for this
path (all six class commits), then dumps the object-level facts needed to verify
Git source-object type/mode/content and the expected return/token contract.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

PATH = 'tools/-runner.py'
ROOT = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S20')
REPO = ROOT / 'fixture-cell'

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           TMPDIR=str(ROOT))

def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env,
                          timeout=30, **kw)

def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr}")
    return r.stdout.strip()

def main():
    if REPO.exists():
        subprocess.run(['rm', '-rf', str(REPO)], check=True)
    REPO.mkdir(parents=True)
    git(REPO, 'init', '-q')
    top = git(REPO, 'rev-parse', '--show-toplevel')
    assert Path(top).resolve() == REPO.resolve(), f'fixture root mismatch: {top}'

    f = REPO / PATH
    f.parent.mkdir(parents=True, exist_ok=True)

    f.write_text('print("real executor")\n')
    git(REPO, 'add', '--', PATH)

    def commit():
        git(REPO, '-c', 'user.name=fixture',
            '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        return git(REPO, 'rev-parse', 'HEAD')

    versions = {}
    versions['equal'] = commit()          # == trusted
    trusted = versions['equal']

    f.write_text('print("forged success")\n')
    git(REPO, 'add', '--', PATH)
    versions['changed'] = commit()

    f.unlink()
    git(REPO, 'add', '-u')
    versions['missing'] = commit()

    f.write_text('print("real executor")\n')
    (REPO / 'unrelated.txt').write_text('unrelated change\n')
    git(REPO, 'add', '--', PATH, 'unrelated.txt')
    versions['unrelated'] = commit()

    versions['unresolvable'] = '0' * 40

    f.unlink()
    f.symlink_to('elsewhere.py')
    git(REPO, 'add', '--', PATH)
    versions['symlink'] = commit()

    # Object-level verification for THIS cell's discriminating pair.
    facts = {'path': PATH, 'trusted': trusted, 'versions': versions}
    for label, rev in [('trusted', trusted), ('changed', versions['changed'])]:
        entry = git(REPO, 'ls-tree', rev, '--', PATH)
        mode, typ, blob, _ = entry.split(None, 3)
        facts[label] = {
            'ls_tree': entry,
            'mode': mode,
            'type': typ,
            'blob': blob,
            'cat_file_t': git(REPO, 'cat-file', '-t', blob),
            'cat_file_s': git(REPO, 'cat-file', '-s', blob),
            'content_repr': repr(git(REPO, 'cat-file', '-p', blob)),
        }
    facts['blobs_differ'] = facts['trusted']['blob'] != facts['changed']['blob']
    facts['contents_differ'] = (
        facts['trusted']['content_repr'] != facts['changed']['content_repr'])
    (ROOT / 'fixture-facts.json').write_text(json.dumps(facts, indent=1))
    print(json.dumps(facts, indent=1))
    return 0

if __name__ == '__main__':
    sys.exit(main())
