#!/usr/bin/env python3
"""Probe fixture W: every re-keyed entry bound to a read_rev that is NOT c0.

Coverage stays 64/64 (the entries still credit), readers still match, the row is
untouched: only arm 3's `read_rev == c0` binding is violated, so the pristine
counter reads total=1 and a counter that drops that conjunct reads total=0.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms')
CLONE = S / 'lane'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')


def git(*args, check=True):
    r = subprocess.run(['git', '-C', str(CLONE)] + list(args), env=ENV, capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(args), r.stderr.decode()))
    return r.stdout


def main():
    fx = json.loads((S / 'fixtures.json').read_text())
    z = fx['fixtures']['G_green']
    base = fx['base']
    rekey = fx['rekey_dir'] + '/'
    git('checkout', '--detach', z)
    assert git('rev-parse', '--show-toplevel').decode().strip() == str(CLONE)
    led = json.loads(git('show', '%s:%s' % (z, LEDGER)))
    changed = 0
    for e in led['entries']:
        if isinstance(e, dict) and any(isinstance(t, str) and t.startswith(rekey)
                                       for t in (e.get('traces') or [])):
            if e.get('read_rev') != base:
                e['read_rev'] = base
                changed += 1
    assert changed == 18, 'expected 18 bound entries, changed %d' % changed
    (CLONE / LEDGER).write_text(json.dumps(led, indent=2) + '\n')
    git('add', '--all')
    git('commit', '--quiet', '-m', 'fixture: re-key entries bound to a read_rev that is not c0')
    w = git('rev-parse', 'HEAD').decode().strip()
    fx['fixtures']['W_rekey_binding'] = w
    (S / 'fixtures.json').write_text(json.dumps(fx, indent=2) + '\n')
    print('W', w, 'changed', changed)
    return 0


if __name__ == '__main__':
    sys.exit(main())
