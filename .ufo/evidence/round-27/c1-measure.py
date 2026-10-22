#!/usr/bin/env python3
"""Round 27 C1 counter (calibration harm repair), frozen at pre-registration.

Usage: c1-measure.py --repo LANE_CLONE [--rev REV]

Runs the lane's strict cold-read monitor unchanged
(`.ufo/evidence/round-21/coldread/measure.py --repo R --rev REV`, no override flag)
and counts mismatches between the lane's self-assessment and repo state:
SHONEN box 3 is marked `[~]` and cites the cold-read ledger as its durable
evidence; it is a mismatch when the monitor does not credit the full page
(`box3_full_page` false), which also drops the calibration score by 2.
Prints `C1_MONITOR: covered=C/T restraint=R box3_mismatch=0|1 rev=REV`.
Exit 0 iff covered == T, restraint == 8 and box3_mismatch == 0; 1 otherwise;
2 when the monitor cannot run or reports an override.
"""
import argparse
import json
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', default='HEAD')
    a = ap.parse_args()
    a.repo = os.path.abspath(a.repo)
    rev = subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', a.rev + '^{commit}'],
                         capture_output=True, text=True)
    if rev.returncode:
        print('C1_MONITOR: cannot resolve rev', file=sys.stderr)
        return 2
    rev = rev.stdout.strip()
    p = subprocess.run([sys.executable, '.ufo/evidence/round-21/coldread/measure.py', '--repo', a.repo, '--rev', rev],
                       cwd=a.repo, capture_output=True, text=True)
    try:
        m = json.loads(p.stdout)
    except ValueError:
        print('C1_MONITOR: monitor output unreadable (exit %d): %s' % (p.returncode, p.stderr[:300]), file=sys.stderr)
        return 2
    if m.get('overrides_used') or m.get('trace_gate') != 'strict' or m.get('revision') != rev:
        print('C1_MONITOR: monitor not strict at rev, or override used', file=sys.stderr)
        return 2
    c = m['coldread']
    shonen = m.get('shonen', {})
    marked = shonen.get('box3_marked') and shonen.get('box3_ledger_link')
    mismatch = int(bool(marked) and not c.get('box3_full_page'))
    covered, total, restraint = c['sections_covered'], c['sections_total'], m['calibration_restraint_score']
    print('C1_MONITOR: covered=%d/%d restraint=%d box3_mismatch=%d depth_score=%s rev=%s'
          % (covered, total, restraint, mismatch, m.get('depth_score'), rev))
    for h in c.get('uncovered_headings', []):
        print('  uncovered: %s' % h)
    return 0 if covered == total and restraint == 8 and mismatch == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
