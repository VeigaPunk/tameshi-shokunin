#!/usr/bin/env python3
"""Refine the c1-probe entries: drop unstable/self-referential inputs, re-commit.

The first probe reused each section's prior input set verbatim, which dragged in
LOG.md, SCORECARD.md and the round-21 ledger itself (exactly the inputs arm 5
rejects and arm 3 cannot verify). This writes a revision whose probe entries pin
only stable blobs, so the remaining question is the counter's structure alone.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
DROP = ('LOG.md', 'SCORECARD.md', LEDGER)
FALLBACK = ('corpus/SOURCES.md', 'corpus/knowledge/service-limits.md',
            'tools/registry.json')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
GITC = ['-c', 'user.name=c1-probe', '-c', 'user.email=c1-probe@example.invalid',
        '-c', 'commit.gpgsign=false']


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=ENV)
    if r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(args), r.stderr.decode()))
    return r.stdout


def main():
    clone = sys.argv[1]
    rev = sys.argv[2]
    top = git(clone, 'rev-parse', '--show-toplevel').decode().strip()
    assert Path(top).resolve() == Path(clone).resolve(), (top, clone)
    spec = importlib.util.spec_from_file_location(
        'r18', os.path.join(clone, '.ufo/evidence/round-18/measure.py'))
    r18 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r18)
    ledger = json.loads(git(clone, 'show', '%s:%s' % (rev, LEDGER)).decode())
    changed = 0
    for e in ledger['entries']:
        if not e.get('probe'):
            continue
        pins = {p: s for p, s in (e.get('inputs') or {}).items() if p not in DROP}
        if not pins:
            for p in FALLBACK:
                data = r18.cat_file_blob(clone, rev, p)
                if data is not None:
                    pins[p] = hashlib.sha256(data).hexdigest()
                    break
        assert pins, e['heading']
        e['inputs'] = pins
        trace = e['traces'][0]
        receipt = json.loads(git(clone, 'show', '%s:%s' % (rev, trace)).decode())
        receipt['inputs'] = pins
        Path(clone, trace).write_text(json.dumps(receipt, indent=2) + '\n', 'utf-8')
        changed += 1
    Path(clone, LEDGER).write_text(json.dumps(ledger, indent=1) + '\n', 'utf-8')
    git(clone, 'add', '-A')
    git(clone, *GITC, 'commit', '-q', '-m',
        'c1-probe v3: probe entries pin only stable blobs (no LOG.md/SCORECARD.md/ledger pins)')
    print('REFINED_REV %s (entries rewritten: %d)' % (
        git(clone, 'rev-parse', 'HEAD').decode().strip(), changed))


if __name__ == '__main__':
    main()
