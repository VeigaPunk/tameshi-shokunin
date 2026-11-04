#!/usr/bin/env python3
"""Whole-table sweep for R75-C2 (seat T75W1E3): every `SELFTEST:` and `rows=`
token in SCORECARD's `## Capabilities` table, compared against the lane
instrument that prints it.

Read-only.  Runs each instrument with cwd = the lane repo and captures stdout.
`--doc` selects the SCORECARD file (default: the lane's); the instruments
themselves always measure the lane at its own committed objects, so the doc is
the only variable (used to sweep a patched copy without touching the lane).

Output: one `SWEEP_ROW` per spec, `SWEEP_TOKEN` coverage lines, stale rows not
in the plan's seven reported as `SWEEP_EXTRA_STALE`, then `SWEEP_SUMMARY`.
Exit 0 when every covered token matches its instrument, 1 otherwise.
"""
import argparse
import os
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'

# The plan's seven stale live figures (R75-C2).  Everything else that is stale
# is an extra finding and is printed as SWEEP_EXTRA_STALE.
PLAN_SEVEN_PAIRS = {
    ('commit-message receipt binding sweep', 'selftest'),
    ('quoted-line receipt backability', 'selftest'),
    ('counter-arm liveness check', 'selftest'),
    ('counter-arm liveness check', 'rows'),
    ('anchor-drift sweep', 'rows'),
    ('line-pointer recheck', 'rows'),
    ('round-range additivity sweep', 'rows'),
}

# (capability, token kind, token regex, instrument argv or None for a
#  non-instrument citation).  argc covers EVERY SELFTEST:/rows= token the
# capability table carries; coverage is asserted below.
SPECS = [
    ('mutation sweep runner', 'selftest',
     r'MUTATE_SELFTEST: \d+/\d+ pass',
     ['bash', 'tools/mutate-and-run.sh', '--selftest']),
    ('receipt-existence sweep', 'selftest',
     r'RECEIPT_EXISTS_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', 'tools/receipt-exists.py', '--selftest']),
    ('commit-message receipt binding sweep', 'selftest',
     r'RECEIPT_COMMIT_BIND_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', 'tools/receipt-commit-bind.py', '--selftest']),
    ('quoted-line receipt backability', 'selftest',
     r'QUOTED_LINE_EXISTS_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', 'tools/quoted-line-exists.py', '--selftest']),
    ('counter-arm liveness check', 'selftest',
     r'ARM_LIVENESS_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', 'tools/arm-liveness.py', '--selftest']),
    ('counter-arm liveness check', 'rows',
     r'rows=\d+ live=\d+ dead=\d+',
     ['python3', '-I', 'tools/arm-liveness.py', '--repo', '.',
      '--manifest', 'tools/arm-liveness.json']),
    ('figure-attribution check', 'selftest',
     r'FIGURE_ATTRIBUTION_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', '-X', 'utf8', 'tools/figure-attribution.py', '--selftest']),
    ('figure-attribution check', 'rows',
     r'FIGURE_ATTRIBUTION: rows=\d+ met=\d+ unexpected=\d+',
     ['python3', '-I', '-X', 'utf8', 'tools/figure-attribution.py', '--repo', '.',
      '--manifest', 'tools/figure-attribution.json']),
    ('anchor-drift sweep', 'selftest',
     r'ANCHOR_DRIFT_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', '-X', 'utf8', 'tools/anchor-drift-sweep.py', '--selftest']),
    ('anchor-drift sweep', 'rows',
     r'ANCHOR_DRIFT: rows=\d+ met=\d+ unexpected=\d+',
     ['python3', '-I', '-X', 'utf8', 'tools/anchor-drift-sweep.py', '--repo', '.',
      '--manifest', 'tools/anchor-drift-sweep.json']),
    ('printed-count recheck', 'selftest',
     r'COUNT_RECHECK_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', '-X', 'utf8', 'tools/count-recheck.py', '--selftest']),
    ('printed-count recheck', 'rows',
     r'COUNT_RECHECK: rows=\d+ met=\d+ unexpected=\d+',
     ['python3', '-I', '-X', 'utf8', 'tools/count-recheck.py', '--repo', '.',
      '--manifest', 'tools/count-recheck.json']),
    ('line-pointer recheck', 'selftest',
     r'POINTER_RECHECK_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', '-X', 'utf8', 'tools/pointer-recheck.py', '--selftest']),
    ('line-pointer recheck', 'rows',
     r'POINTER_RECHECK: rows=\d+ met=\d+ unexpected=\d+',
     ['python3', '-I', '-X', 'utf8', 'tools/pointer-recheck.py', '--repo', '.',
      '--manifest', 'tools/pointer-recheck.json']),
    ('rekey-cost forecast', 'selftest',
     r'REKEY_COST_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', 'tools/rekey-cost.py', '--selftest']),
    ('wave-record reconciliation', 'selftest',
     r'WAVE_RECONCILE_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', '-X', 'utf8', 'tools/wave-reconcile.py', '--selftest']),
    ('wave-record reconciliation', 'rows',
     r'WAVE_RECONCILE: rows=\d+ met=\d+ unexpected=\d+',
     ['python3', '-I', '-X', 'utf8', 'tools/wave-reconcile.py', '--repo', '.',
      '--extra-root', 'fleet=/home/vgpnk/Projects/shokunin',
      '--manifest', 'tools/wave-reconcile.json']),
    ('round-range additivity sweep', 'rows',
     r'ADDRANGE: rows=\d+ met=\d+ unexpected=\d+',
     ['python3', '-I', 'tools/additivity-range.py', '--repo', '.',
      '--manifest', 'tools/additivity-range.json']),
    ('round-range additivity sweep', 'selftest',
     r'ADDITIVITY_RANGE_SELFTEST: \d+/\d+ pass',
     ['python3', '-I', 'tools/additivity-range.py', '--selftest']),
]

# Tokens that are cited in a capability row but are NOT produced by the row's
# instrument (a seat receipt quoted alongside).  They are excluded from the
# comparison, named, and never counted as match or stale.
NONINSTRUMENT = [
    ('wave-record reconciliation', 'rows=6', 'ORACLE_CMP rows=6 equal=6',
     'independent oracle receipt by seat T73W1S01, not this instrument'),
]


def capability_rows(doc_text):
    lines = doc_text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == '## Capabilities')
    except StopIteration:
        raise SystemExit('setup: no ## Capabilities section')
    rows = {}
    for ln in lines[start + 1:]:
        if ln.startswith('## '):
            break
        if ln.startswith('|') and not ln.startswith('|---'):
            cells = [c.strip() for c in ln.strip('|').split('|')]
            if len(cells) >= 3 and cells[0] != 'Capability':
                rows[cells[0]] = ln
    return rows


def run(argv, cache, tmpdir):
    key = tuple(argv)
    if key not in cache:
        env = dict(os.environ)
        env['TMPDIR'] = tmpdir
        p = subprocess.run(argv, cwd=LANE, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=env)
        cache[key] = (p.returncode, p.stdout.decode('utf-8', 'replace'))
    return cache[key]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', default=os.path.join(LANE, 'SCORECARD.md'))
    ap.add_argument('--tmpdir', default=os.environ.get('TMPDIR', '/tmp'))
    a = ap.parse_args()

    doc_text = open(a.doc, encoding='utf-8').read()
    rows = capability_rows(doc_text)
    cache = {}
    match = stale = 0
    stale_rows = []
    print('SWEEP_DOC %s' % a.doc)
    for cap, kind, pat, argv in SPECS:
        line = rows.get(cap)
        if line is None:
            print('SWEEP_SETUP capability=%r absent' % cap)
            return 2
        m1 = re.search(pat, line)
        quoted = m1.group(0) if m1 else None
        rc, out = run(argv, cache, a.tmpdir)
        m2 = re.search(pat, out)
        measured = m2.group(0) if m2 else None
        state = 'match' if quoted is not None and quoted == measured else 'stale'
        print('SWEEP_ROW cap=%-38s kind=%-8s quoted=%-52s measured=%-52s rc=%d %s'
              % (cap, kind, quoted, measured, rc, state))
        if state == 'match':
            match += 1
        else:
            stale += 1
            stale_rows.append((cap, kind, quoted, measured))

    # coverage: every SELFTEST:/rows= token in the table must be accounted for
    # by a SPECS entry (or a named NONINSTRUMENT citation).  Count token shapes
    # per row and compare with the declared spec counts, so a token no spec
    # regex reaches cannot pass unnoticed.
    declared = {}
    for cap, kind, _pat, _argv in SPECS:
        d = declared.setdefault(cap, [0, 0])
        d[0 if kind == 'selftest' else 1] += 1
    for cap, _token, _cite, _why in NONINSTRUMENT:
        declared.setdefault(cap, [0, 0])[1] += 1
    uncovered = 0
    for cap in declared:
        line = rows.get(cap, '')
        n_selftest = len(re.findall(r'[A-Z][A-Z0-9_]*SELFTEST:', line))
        n_rows = len(re.findall(r'rows=', line))
        want_selftest, want_rows = declared[cap]
        if (n_selftest, n_rows) != (want_selftest, want_rows):
            print('SWEEP_UNCOVERED cap=%r selftest_tokens=%d/%d rows_tokens=%d/%d'
                  % (cap, n_selftest, want_selftest, n_rows, want_rows))
            uncovered += 1
    for cap, token, cite, why in NONINSTRUMENT:
        print('SWEEP_NONINSTRUMENT cap=%r token=%r cite=%r why=%s'
              % (cap, token, cite, why))
    for cap, kind, quoted, measured in stale_rows:
        tag = 'PLAN7' if (cap, kind) in PLAN_SEVEN_PAIRS else 'EXTRA'
        print('SWEEP_STALE cap=%r kind=%s quoted=%r measured=%r class=%s'
              % (cap, kind, quoted, measured, tag))
    print('SWEEP_SUMMARY specs=%d match=%d stale=%d uncovered=%d'
          % (len(SPECS), match, stale, uncovered))
    return 0 if stale == 0 and uncovered == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
