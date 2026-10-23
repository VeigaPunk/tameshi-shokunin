#!/usr/bin/env python3
"""Round 29 C1 counter v2 (calibration repair), re-frozen before data after the control wave.

Supersedes c1-measure.py (v1): seat CriticC1Design (.ufo/waves/round-29/ctl/CriticC1Design.md)
found that v1 ran the round-27 counter, and through it the monitor, from the
measured checkout's working tree, so the executable identity was not pinned. v2 runs
the monitor chain from bytes pinned at base 367ec0f1 (round-21 selector and round-18
implementation, sha256 below), packaged in a scratch directory and run by absolute
path; the measured clone and REV are passed only as data. The round-27 counter's
arithmetic is reproduced here unchanged (lines 42-54 of that file). No data seat ran
before v2.

Usage: c1-measure-v2.py --repo LANE_CLONE [--rev REV]

Predicate C1_R29_V2_PASS (same sentence in contract-amendment-2.json): PASS iff the
pinned strict cold-read monitor at REV reports covered == total, restraint == 8 and
box3_mismatch == 0 with no override, AND the cold-read ledger at REV keeps the 371
base entries and every non-entry key equal as data (canonical JSON), AND every
ledger entry appended after base index 370 is bound to round-29 seat evidence: each
of its `reports` exists at REV under `.ufo/waves/round-29/`, holds a ```json block
whose `seat` is one of the entry's `seats`, whose `read_rev` equals the entry's
`read_rev`, and whose sections name the entry's `start` and `heading` with the
entry's `verdict`, and each of its `seats` is a member of a committed
`.ufo/waves/round-29/*/swarm-registry.json` at REV.

Prints `C1_R29_V2: covered=C/T restraint=R box3_mismatch=M appended=K bound=B prefix_equal=0|1 rev=REV`
then `PREDICATE: C1_R29_V2_PASS=true|false`. Exit 0 iff PASS; 1 otherwise; 2 when REV
cannot be resolved, a pinned monitor byte differs, or the monitor output is unusable.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = '367ec0f1d79cb9b67d724f2962e7554a0841b1fc'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
WAVES = '.ufo/waves/round-29/'
MONITOR_SHA = {
    '.ufo/evidence/round-21/coldread/measure.py': '657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb',
    '.ufo/evidence/round-18/measure.py': '7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37',
}


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)


def show(repo, rev, path):
    p = git(repo, 'show', '%s:%s' % (rev, path))
    return p.stdout if p.returncode == 0 else None


def canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


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
        print('C1_R29_V2: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()

    pkg = tempfile.mkdtemp(prefix='c1v2r29-')
    try:
        for path, sha in MONITOR_SHA.items():
            raw = show(repo, BASE, path)
            if raw is None or hashlib.sha256(raw).hexdigest() != sha:
                print('C1_R29_V2: pinned monitor byte mismatch for %s' % path, file=sys.stderr)
                return 2
            dst = os.path.join(pkg, path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'wb') as f:
                f.write(raw)
        p = subprocess.run([sys.executable, os.path.join(pkg, '.ufo/evidence/round-21/coldread/measure.py'),
                            '--repo', repo, '--rev', rev], capture_output=True, text=True, cwd=pkg)
    finally:
        shutil.rmtree(pkg, ignore_errors=True)
    try:
        m = json.loads(p.stdout)
        c = m['coldread']
        covered, total, restraint = int(c['sections_covered']), int(c['sections_total']), int(m['calibration_restraint_score'])
    except (ValueError, KeyError, TypeError):
        print('C1_R29_V2: monitor output unusable (exit %d): %s' % (p.returncode, p.stderr[:300]), file=sys.stderr)
        return 2
    if m.get('overrides_used') or m.get('trace_gate') != 'strict' or m.get('revision') != rev:
        print('C1_R29_V2: monitor not strict at rev, or override used', file=sys.stderr)
        return 2
    shonen = m.get('shonen', {})
    marked = shonen.get('box3_marked') and shonen.get('box3_ledger_link')
    mismatch = int(bool(marked) and not c.get('box3_full_page'))
    for h in c.get('uncovered_headings', []):
        print('  uncovered: %s' % h)

    base_ledger = json.loads(show(repo, BASE, LEDGER))
    raw = show(repo, rev, LEDGER)
    ledger = json.loads(raw) if raw else {'entries': []}
    n0 = len(base_ledger['entries'])
    others = lambda d: {k: v for k, v in d.items() if k != 'entries'}
    prefix_equal = int(canon(ledger.get('entries', [])[:n0]) == canon(base_ledger['entries'])
                       and canon(others(ledger)) == canon(others(base_ledger)))
    appended = ledger.get('entries', [])[n0:]

    members = set()
    ls = git(repo, 'ls-tree', '-r', '--name-only', rev, '--', WAVES)
    for path in ls.stdout.decode().split('\n'):
        if path.endswith('/swarm-registry.json'):
            try:
                members |= set(json.loads(show(repo, rev, path)).get('members', {}))
            except (ValueError, TypeError, AttributeError):
                pass

    bound = 0
    for e in appended:
        seats = set(e.get('seats') or [])
        reports = e.get('reports') or []
        ok = bool(seats) and bool(reports) and seats <= members
        for rp in reports:
            if not ok:
                break
            body = show(repo, rev, rp) if rp.startswith(WAVES) else None
            if body is None:
                ok = False
                break
            hit = False
            for blk in json_blocks(body.decode('utf-8', 'replace')):
                try:
                    d = json.loads(blk)
                except ValueError:
                    continue
                if (isinstance(d, dict) and d.get('seat') in seats and d.get('read_rev') == e.get('read_rev')
                        and any(isinstance(s, dict) and s.get('start') == e.get('start')
                                and s.get('heading') == e.get('heading') and s.get('verdict') == e.get('verdict')
                                for s in d.get('sections', []))):
                    hit = True
            ok = ok and hit
        bound += int(ok)

    print('C1_R29_V2: covered=%d/%d restraint=%d box3_mismatch=%d appended=%d bound=%d prefix_equal=%d rev=%s'
          % (covered, total, restraint, mismatch, len(appended), bound, prefix_equal, rev))
    passed = (covered == total and restraint == 8 and mismatch == 0 and prefix_equal == 1
              and bound == len(appended))
    print('PREDICATE: C1_R29_V2_PASS=%s' % ('true' if passed else 'false'))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
