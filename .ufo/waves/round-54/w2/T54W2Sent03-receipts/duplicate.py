#!/usr/bin/env python3
"""Build the "duplicate" probe from the prefix fixture.

Adds a SECOND, correct (read_rev == c0) bound entry for "## Standing rules" next
to the poisoned one, so the directory holds both a wrong and a right entry for
that heading. Tests whether arm 3's per-heading test is existential (any good
entry credits) or universal (every bound entry must be good).
"""
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W2Sent03'
C1 = '99c3bc88d704566197783f66b211ee0a830e0330'
SRC = S + '/fixtures/prefix'
D = S + '/fixtures/duplicate'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-' + C1[:12]

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def git(args, check=True):
    return subprocess.run(['git', '-C', D] + args, env=env, capture_output=True, check=check)


def main():
    if os.path.exists(D):
        shutil.rmtree(D)
    subprocess.run(['git', 'clone', '--shared', '--quiet', SRC, D], env=env, check=True)
    assert git(['rev-parse', '--show-toplevel']).stdout.decode().strip() == D
    head = git(['rev-parse', 'HEAD']).stdout.decode().strip()
    ledger = json.loads(git(['show', head + ':' + LEDGER]).stdout.decode('utf-8', 'surrogateescape'))
    poisoned = [e for e in ledger['entries']
                if e.get('heading') == '## Standing rules'
                and any(isinstance(t, str) and t.startswith(REKEY + '/') for t in (e.get('traces') or []))]
    assert len(poisoned) == 1, poisoned
    bad = poisoned[0]
    assert bad['read_rev'] == C1[:12], bad['read_rev']

    twin = json.loads(json.dumps(bad))
    twin['read_rev'] = C1
    twin_trace = REKEY + '/traces/section-99.json'
    twin['traces'] = [twin_trace]
    twin['seats'] = ['T54W2Sent03 duplicate probe']
    with open(os.path.join(D, twin_trace), 'w') as fh:
        json.dump({'schema': 'tameshi-trace-inputs-v1', 'argv': ['true'], 'cwd': S,
                   'root': D, 'rev': C1, 'exit': 0,
                   'inputs': dict(bad['inputs']), 'external': {},
                   'live_lane_reads': {}, 'untracked': []}, fh, indent=1)
        fh.write('\n')
    ledger['entries'].append(twin)
    with open(os.path.join(D, LEDGER), 'w') as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    git(['add', '-A'])
    git(['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
         'commit', '--quiet', '-m', 'probe: poisoned entry + clean twin'])
    print('DUPLICATE dir=%s head=%s poisoned_read_rev=%s twin_read_rev=%s'
          % (D, git(['rev-parse', 'HEAD']).stdout.decode().strip(),
             bad['read_rev'], twin['read_rev']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
