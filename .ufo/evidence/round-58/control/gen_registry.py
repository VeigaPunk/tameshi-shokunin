#!/usr/bin/env python3
"""Round-58 C2 control registry generator (used by .ufo/evidence/round-58/controls.sh).

Usage: gen_registry.py --clone DIR --base BASE --rev REV --mode skip|fab|mut
  DIR is a scratch clone checked out at REV. The script removes every registry row that runs
  `tools/receipt-revision-gate.py` without `--selftest` (the selftest row stays), writes three
  fixture rows and, where the mode needs them, fixture receipts under
  `.ufo/evidence/round-58/control/ctl-fixtures/` inside DIR, and prints one JSON stats line. It
  runs git only for `diff --name-only`. Nothing outside DIR is touched.

Fixtures are built here, never read from a committed receipt: `accept` names REV (certified REV,
exit 0), `drift` names BASE with a --paths file listing one path that differs BASE..REV (exit 3,
RECEIPT_REV_CONTENT_DRIFT), `absent` carries no `rev=` token (exit 3, RECEIPT_REV_ABSENT), and
the unresolvable row certifies a revision that exists nowhere (exit 2).

  skip  the three rows hold the right commands but their `expect.exit` is rotated (accept
        expects 2, drift expects 0, unresolvable expects 3): the declared exits are still
        {0,2,3}, the executed rows all differ (held 0/3).
  fab   the receipts the accept and drift rows name were never written: accept expects 0 and
        drift expects 3 + RECEIPT_REV_CONTENT_DRIFT, the gate answers RECEIPT_MISSING; the
        unresolvable row exits 2 before it reads a receipt, so exactly one row holds.
  mut   every row holds on the clean gate and none of the rows runs the drift branch
        (accept 0 / absent 3 / unresolvable 2), so mutants M1 (accept-on-drift) and M2 (wrong
        drift code) cannot turn a row red; M3 (exit 0 on unresolvable) is killed by the exit-2
        row, because any valid exit-2 row runs that branch - the control targets 1/3, not 0/3.
"""
import argparse
import json
import os
import subprocess
import sys

REGISTRY = 'tools/registry.json'
GATE = 'tools/receipt-revision-gate.py'
FIX = '.ufo/evidence/round-58/control/ctl-fixtures'
BOGUS = '0123456789abcdef0123456789abcdef01234567'


def changed_path(clone, base, rev):
    out = subprocess.run(['git', '-C', clone, 'diff', '--name-only', base, rev],
                         capture_output=True, check=True).stdout.decode().splitlines()
    out = [p for p in out if p]
    for p in out:
        if not p.startswith('.ufo/'):
            return p
    if out:   # only reachable in a dry run, where REV adds instruments and nothing else
        return out[0]
    raise SystemExit('gen_registry: no path differs BASE..REV; the drift fixture needs one')


def row(name, argv, exit_code, rev, contains=None):
    expect = {'exit': exit_code}
    if contains:
        expect['stdout_contains'] = contains
    return {'name': name, 'kind': 'gate', 'argv': argv, 'expect': expect, 'timeout_s': 60,
            'source': '%s@%s:1-31' % (GATE, rev), 'status': 'active', 'tags': ['ctl-r57']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', required=True)
    ap.add_argument('--base', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--mode', required=True, choices=('skip', 'fab', 'mut'))
    a = ap.parse_args()
    clone = os.path.abspath(a.clone)
    rev, base = a.rev, a.base
    reg_path = os.path.join(clone, REGISTRY)
    with open(reg_path, 'r', encoding='utf-8') as fh:
        reg = json.load(fh)
    before = len(reg['rows'])
    reg['rows'] = [r for r in reg['rows']
                   if not (GATE in r.get('argv', []) and '--selftest' not in r.get('argv', []))]
    removed = before - len(reg['rows'])
    fx = os.path.join(clone, FIX)
    os.makedirs(fx, exist_ok=True)
    drifted = changed_path(clone, base, rev)
    with open(os.path.join(fx, 'paths.txt'), 'w', encoding='utf-8') as fh:
        fh.write(drifted + '\n')
    receipts = {'accept': 'CTL accept rev=%s\n' % rev,
                'drift': 'CTL drift rev=%s\n' % base,
                'absent': 'CTL absent no revision token here\n'}
    if a.mode == 'fab':
        receipts = {'absent': receipts['absent']}
    for name, body in receipts.items():
        with open(os.path.join(fx, name + '.stdout'), 'w', encoding='utf-8') as fh:
            fh.write(body)

    def argv(receipt, certified=rev, paths=False, role='verdict'):
        out = ['python3', GATE, '--lane', '.', '--certified', certified]
        if paths:
            out += ['--paths', FIX + '/paths.txt']
        return out + ['--receipt', '%s/%s.stdout:%s' % (FIX, receipt, role)]

    unres = argv('accept', certified=BOGUS)
    if a.mode == 'skip':
        new = [row('ctl-r57-gate-accept', argv('accept'), 2, rev),
               row('ctl-r57-gate-drift', argv('drift', paths=True), 0, rev,
                   ['RECEIPT_REV_CONTENT_DRIFT']),
               row('ctl-r57-gate-unresolvable', unres, 3, rev, ['RECEIPT_REV_UNRESOLVABLE'])]
    elif a.mode == 'fab':
        new = [row('ctl-r57-gate-accept', argv('accept'), 0, rev),
               row('ctl-r57-gate-drift', argv('drift', paths=True), 3, rev,
                   ['RECEIPT_REV_CONTENT_DRIFT']),
               row('ctl-r57-gate-unresolvable', unres, 2, rev, ['RECEIPT_REV_UNRESOLVABLE'])]
    else:
        new = [row('ctl-r57-gate-accept', argv('accept'), 0, rev),
               row('ctl-r57-gate-absent', argv('absent'), 3, rev, ['RECEIPT_REV_ABSENT']),
               row('ctl-r57-gate-unresolvable', unres, 2, rev, ['RECEIPT_REV_UNRESOLVABLE'])]
    reg['rows'].extend(new)
    with open(reg_path, 'w', encoding='utf-8') as fh:
        json.dump(reg, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print(json.dumps({'mode': a.mode, 'gate_rows_removed': removed, 'rows_added': len(new),
                      'drift_path': drifted}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
