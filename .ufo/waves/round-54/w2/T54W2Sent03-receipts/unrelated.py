#!/usr/bin/env python3
"""read_rev abuse: an UNRELATED commit (not an ancestor of the deciding revision).

  unrelated       the "## Standing rules" entry's read_rev is an unrelated commit's
                  sha; the re-key directory stays honest (C1 prefix)
  unrelated_dir   the re-key directory itself is renamed after that unrelated
                  commit and every entry's read_rev follows it (tests the
                  ancestry guard on c0)

Usage: unrelated.py unrelated|unrelated_dir
"""
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W2Sent03'
C1 = '99c3bc88d704566197783f66b211ee0a830e0330'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
HEADING = '## Standing rules'
VARIANT = sys.argv[1]
D = '%s/fixtures/%s' % (S, VARIANT)

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def git(args, check=True):
    return subprocess.run(['git', '-C', D] + args, env=env, capture_output=True, check=check)


def main():
    if os.path.exists(D):
        shutil.rmtree(D)
    subprocess.run(['git', 'clone', '--shared', '--quiet', S + '/fixtures/positive', D],
                   env=env, check=True)
    assert git(['rev-parse', '--show-toplevel']).stdout.decode().strip() == D
    assert git(['rev-parse', 'HEAD']).stdout.decode().strip() != ''

    # an orphan commit: no parent, unrelated to the lane's history
    envc = dict(env, GIT_AUTHOR_NAME='fx', GIT_AUTHOR_EMAIL='fx@invalid',
                GIT_COMMITTER_NAME='fx', GIT_COMMITTER_EMAIL='fx@invalid',
                GIT_AUTHOR_DATE='2026-10-28T00:00:00Z',
                GIT_COMMITTER_DATE='2026-10-28T00:00:00Z')
    tree = git(['write-tree']).stdout.decode().strip()
    orphan = subprocess.run(['git', '-C', D, 'commit-tree', tree, '-m', 'unrelated root'],
                            env=envc, capture_output=True, check=True).stdout.decode().strip()
    anc = subprocess.run(['git', '-C', D, 'merge-base', '--is-ancestor', orphan, C1],
                        capture_output=True, env=env)
    assert anc.returncode != 0, 'orphan must not be an ancestor of C1'

    ledger = json.loads(git(['show', 'HEAD:' + LEDGER]).stdout.decode('utf-8', 'surrogateescape'))
    entries = ledger['entries']
    rekey_c1 = '.ufo/evidence/round-21/coldread/rekey-r54-' + C1[:12]

    if VARIANT == 'unrelated':
        hit = [e for e in entries
               if e.get('heading') == HEADING
               and any(isinstance(t, str) and t.startswith(rekey_c1 + '/')
                       for t in (e.get('traces') or []))]
        assert len(hit) == 1, hit
        hit[0]['read_rev'] = orphan
        detail = {'rekey_dir': 'rekey-r54-' + C1[:12], 'read_rev': orphan}
    else:
        new = '.ufo/evidence/round-21/coldread/rekey-r54-' + orphan[:12]
        os.makedirs(os.path.join(D, new, 'traces'), exist_ok=True)
        namemap = {}
        for name in sorted(os.listdir(os.path.join(D, rekey_c1, 'traces'))):
            shutil.copyfile(os.path.join(D, rekey_c1, 'traces', name),
                            os.path.join(D, new, 'traces', name))
            namemap[rekey_c1 + '/traces/' + name] = new + '/traces/' + name
        shutil.rmtree(os.path.join(D, rekey_c1))
        for e in entries:
            tr = e.get('traces') or []
            if any(isinstance(t, str) and t.startswith(rekey_c1 + '/') for t in tr):
                e['traces'] = [namemap[t] for t in tr]
                e['read_rev'] = orphan
        detail = {'rekey_dir': 'rekey-r54-' + orphan[:12], 'read_rev': orphan}

    with open(os.path.join(D, LEDGER), 'w') as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    git(['add', '-A'])
    git(['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
         'commit', '--quiet', '-m', 'probe: %s' % VARIANT])
    print('UNRELATED %s dir=%s head=%s orphan=%s %s'
          % (VARIANT, D, git(['rev-parse', 'HEAD']).stdout.decode().strip(), orphan,
             json.dumps(detail, sort_keys=True)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
