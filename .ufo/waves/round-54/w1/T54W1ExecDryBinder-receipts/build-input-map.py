#!/usr/bin/env python3
"""Round-54 w1 dry-run binder: for each C0-lost heading, union the prior ledger
entries' lane-relative input paths and classify them at C0."""
import hashlib
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
BASE = 'd33053f7552db4bd290c99a36979760f544c41ad'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
UNSTABLE = ('LOG.md', 'SCORECARD.md')


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return e


def git(*args):
    return subprocess.run(['git', '-C', LANE] + list(args), env=env(),
                          capture_output=True, check=False)


def blob(rev, path):
    r = git('show', '%s:%s' % (rev, path))
    return r.stdout if r.returncode == 0 else None


def main():
    headings = json.load(open(os.path.join(
        LANE, '.ufo/evidence/round-54/c1/lost-headings-at-c0.json')))

    raw = blob(C0, LEDGER)
    if raw is None:
        print('E: ledger missing at C0')
        return 2
    ledger = json.loads(raw.decode('utf-8', 'surrogateescape'))
    entries = [e for e in (ledger.get('entries') or []) if isinstance(e, dict)]

    r54 = set()
    for line in git('diff', '--name-only', '%s..%s' % (BASE, C0)) \
            .stdout.decode().splitlines():
        if line.strip():
            r54.add(line.strip())
    for line in git('diff', '--name-only').stdout.decode().splitlines():
        if line.strip():
            r54.add(line.strip())

    out = []
    counts = []
    for h in headings:
        prior = [e for e in entries if e.get('heading') == h]
        paths = []
        seen = set()
        for e in prior:
            for p in sorted((e.get('inputs') or {})):
                if p not in seen:
                    seen.add(p)
                    paths.append(p)
        inputs, dropped, unstable = {}, [], []
        for p in paths:
            data = blob(C0, p)
            if data is None:
                dropped.append(p)
                continue
            inputs[p] = hashlib.sha256(data).hexdigest()
            base = os.path.basename(p)
            if p in UNSTABLE or base in UNSTABLE or p in r54:
                unstable.append(p)
        row = {'heading': h, 'inputs': inputs, 'dropped': dropped,
               'unstable': unstable}
        out.append(row)
        counts.append((h, len(prior)))

    dest = os.path.join(LANE, '.ufo/waves/round-54/w1/T54W1ExecDryBinder-input-map.json')
    with open(dest, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=False)
        fh.write('\n')
    print('wrote', dest, 'headings=%d' % len(out))
    for o, (h, nprior) in zip(out, counts):
        print('%-72s prior=%d inputs=%d dropped=%d unstable=%d %s'
              % (o['heading'][:72], nprior, len(o['inputs']),
                 len(o['dropped']), len(o['unstable']),
                 'EMPTY' if not o['inputs'] else
                 ('ALL-UNSTABLE' if len(o['unstable']) == len(o['inputs']) else '')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
