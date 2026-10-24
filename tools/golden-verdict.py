#!/usr/bin/env python3
"""golden-verdict.py — three-outcome golden-comparison verdicts (tameshi round 38).

A golden comparison has three outcomes, not two: POSIX `diff` exits 0 when no
differences were found, 1 when differences were found, and greater than 1 when
an error occurred (S105 — The Open Group Base Specifications Issue 7,
§EXIT STATUS). The path that writes the expected value is a flagged path: the
write sits behind an explicit update flag (S106 — google/golden, `Compare`).

Modes:
  --selftest           run the three frozen behavioural cases; exit 0 iff 3/3 pass
  --check-entry PATH   check a knowledge entry declares the three outcome classes
  --classify-exit N    print the outcome class for a diff exit code

Exit codes: 0 pass · 1 fail · 2 usage.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

OUTCOMES = ('match', 'differ', 'error')


def classify_exit(rc):
    """Map a diff exit code to one of the three golden-verdict outcome classes."""
    if rc == 0:
        return 'match'
    if rc == 1:
        return 'differ'
    return 'error'


def compare(golden, actual, diff_bin='diff'):
    """Compare a golden file with an actual file; return (outcome, detail)."""
    if not os.path.isfile(golden):
        return 'error', 'golden file absent: %s' % golden
    proc = subprocess.run([diff_bin, '-u', golden, actual], capture_output=True)
    return classify_exit(proc.returncode), 'diff exit %d' % proc.returncode


def selftest():
    """Three frozen cases: identical, differing, and a comparison that cannot be made."""
    cases = []
    with tempfile.TemporaryDirectory(prefix='golden-verdict-') as tmp:
        golden = os.path.join(tmp, 'expected.txt')
        same = os.path.join(tmp, 'same.txt')
        other = os.path.join(tmp, 'other.txt')
        absent = os.path.join(tmp, 'absent.txt')
        with open(golden, 'w', encoding='utf-8') as fh:
            fh.write('alpha\nbeta\n')
        with open(same, 'w', encoding='utf-8') as fh:
            fh.write('alpha\nbeta\n')
        with open(other, 'w', encoding='utf-8') as fh:
            fh.write('alpha\ngamma\n')
        cases.append(('match', compare(golden, same)))
        cases.append(('differ', compare(golden, other)))
        cases.append(('error', compare(golden, absent)))

    failed = []
    for want, (got, detail) in cases:
        if got != want:
            failed.append('case %s: expected %s, observed %s (%s)' % (want, want, got, detail))
    print('GOLDEN_VERDICT_SELFTEST: %d/3 pass' % (3 - len(failed)))
    for line in failed:
        print('FAIL %s' % line)
    return 0 if not failed else 1


def check_entry(path):
    """A golden-verdict knowledge entry must declare the three classes and the flagged write path."""
    try:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
    except OSError as exc:
        print('GOLDEN_VERDICT_ENTRY: unreadable %s (%s)' % (path, exc))
        return 1

    missing = [o for o in OUTCOMES
               if not re.search(r'^\|\s*`?%s`?\s*\|' % re.escape(o), text, re.I | re.M)]
    update_rule = bool(re.search(r'update.{0,40}flag|flag.{0,40}update', text, re.I))
    print('GOLDEN_VERDICT_ENTRY: classes=%d/3 update_rule=%s path=%s'
          % (3 - len(missing), 'present' if update_rule else 'absent', path))
    for o in missing:
        print('MISSING outcome class: %s' % o)
    if not update_rule:
        print('MISSING explicit update-flag rule')
    return 0 if not missing and update_rule else 1


def main():
    ap = argparse.ArgumentParser(description='golden-comparison three-outcome verdicts')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--check-entry', metavar='PATH')
    ap.add_argument('--classify-exit', metavar='N', type=int)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.check_entry:
        return check_entry(a.check_entry)
    if a.classify_exit is not None:
        print(classify_exit(a.classify_exit))
        return 0
    ap.print_usage(sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
