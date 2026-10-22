#!/usr/bin/env python3
"""Round 29 C1 counter (calibration repair, routed item 1 of round-28 spot-check), frozen before data.

Usage: c1-measure.py --repo LANE_CLONE [--rev REV]

Predicate C1_R29_PASS (same sentence in contract.json): PASS iff the frozen
round-27 counter `.ufo/evidence/round-27/c1-measure.py` exits 0 at REV
(covered == total, restraint == 8, box3_mismatch == 0), AND the cold-read
ledger at REV keeps the 371 base entries equal as data, AND every ledger entry
appended after base index 370 is bound to round-29 seat evidence: each of its
`reports` exists at REV under `.ufo/waves/round-29/`, holds a ```json block
whose `seat` is one of the entry's `seats` and whose sections name the entry's
`start` and `heading`, and each of its `seats` is a member of a committed
`.ufo/waves/round-29/*/swarm-registry.json` at REV.

Prints `C1_R29: monitor_exit=E covered=C/T restraint=R box3_mismatch=M appended=K bound=B prefix_equal=0|1 rev=REV`
then `PREDICATE: C1_R29_PASS=true|false`. Exit 0 iff PASS; 1 otherwise; 2 when
REV cannot be resolved or the round-27 counter cannot run (exit 2 there).
"""
import argparse
import json
import os
import re
import subprocess
import sys

BASE = '367ec0f1d79cb9b67d724f2962e7554a0841b1fc'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
R27 = '.ufo/evidence/round-27/c1-measure.py'
WAVES = '.ufo/waves/round-29/'


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)


def show(repo, rev, path):
    p = git(repo, 'show', '%s:%s' % (rev, path))
    return p.stdout if p.returncode == 0 else None


def json_blocks(text):
    return re.findall(r'```json\s*\n(.*?)\n```', text, re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', default='HEAD')
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    r = git(repo, 'rev-parse', '--verify', '--quiet', a.rev + '^{commit}')
    if r.returncode:
        print('C1_R29: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    # The round-27 counter is run from REV's own bytes when present, else from base bytes.
    counter = show(repo, rev, R27) or show(repo, BASE, R27)
    tmp = subprocess.run(['mktemp', '-d', '/tmp/c1r29-XXXX'], capture_output=True, text=True).stdout.strip()
    cpath = os.path.join(tmp, 'c1-measure-r27.py')
    with open(cpath, 'wb') as f:
        f.write(counter)
    p = subprocess.run([sys.executable, cpath, '--repo', repo, '--rev', rev], capture_output=True, text=True, cwd=repo)
    subprocess.run(['rm', '-rf', tmp])
    sys.stdout.write(p.stdout)
    if p.returncode == 2:
        print('C1_R29: round-27 counter exit 2: %s' % p.stderr[:300], file=sys.stderr)
        return 2
    m = re.search(r'covered=(\d+)/(\d+) restraint=(\d+) box3_mismatch=(\d)', p.stdout)
    covered, total, restraint, mismatch = (m.groups() if m else ('?', '?', '?', '?'))

    base_ledger = json.loads(show(repo, BASE, LEDGER))
    raw = show(repo, rev, LEDGER)
    ledger = json.loads(raw) if raw else {'entries': []}
    n0 = len(base_ledger['entries'])
    prefix_equal = int(ledger['entries'][:n0] == base_ledger['entries'])
    appended = ledger['entries'][n0:]

    members = set()
    ls = git(repo, 'ls-tree', '-r', '--name-only', rev, '--', WAVES)
    for path in ls.stdout.decode().split('\n'):
        if path.endswith('/swarm-registry.json'):
            try:
                members |= set(json.loads(show(repo, rev, path)).get('members', {}))
            except (ValueError, TypeError):
                pass

    bound = 0
    for e in appended:
        seats = set(e.get('seats') or [])
        reports = e.get('reports') or []
        ok = bool(seats) and bool(reports) and seats <= members
        for rp in reports:
            if not ok:
                break
            if not rp.startswith(WAVES):
                ok = False
                break
            body = show(repo, rev, rp)
            if body is None:
                ok = False
                break
            hit = False
            for blk in json_blocks(body.decode('utf-8', 'replace')):
                try:
                    d = json.loads(blk)
                except ValueError:
                    continue
                if d.get('seat') in seats and any(s.get('start') == e.get('start') and s.get('heading') == e.get('heading')
                                                  for s in d.get('sections', [])):
                    hit = True
            ok = ok and hit
        bound += int(ok)

    print('C1_R29: monitor_exit=%d covered=%s/%s restraint=%s box3_mismatch=%s appended=%d bound=%d prefix_equal=%d rev=%s'
          % (p.returncode, covered, total, restraint, mismatch, len(appended), bound, prefix_equal, rev))
    passed = p.returncode == 0 and prefix_equal == 1 and bound == len(appended)
    print('PREDICATE: C1_R29_PASS=%s' % ('true' if passed else 'false'))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
