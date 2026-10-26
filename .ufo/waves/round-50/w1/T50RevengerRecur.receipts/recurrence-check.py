#!/usr/bin/env python3
"""recurrence-check.py — proposed QUALITY criterion 100's check.

A routed-defect class with a second occurrence is closed only by a check whose
falsifier receipt postdates the last occurrence. Refuses (exit 1) a class with
>= 2 ledger rows that has no gate, no committed falsifier receipt at REV, or a
falsifier receipt older than the class's last occurrence.
"""
import argparse, json, subprocess, sys

def git(lane, *a):
    return subprocess.run(['git', '-C', lane] + list(a), capture_output=True, text=True)

def blob_exists(lane, rev, path):
    return git(lane, 'cat-file', '-e', '%s:%s' % (rev, path)).returncode == 0

def ancestor(lane, a, b):
    """True if a is an ancestor of (or equal to) b."""
    r = git(lane, 'merge-base', '--is-ancestor', a, b)
    return r.returncode == 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--ledger', default='corpus/routed-defects.json')
    ap.add_argument('--classes', required=True)
    a = ap.parse_args()
    ledger = json.loads(git(a.lane, 'show', '%s:%s' % (a.rev, a.ledger)).stdout or '{}')
    classes = json.load(open(a.classes))
    rows = ledger.get('defects', ledger.get('rows', []))
    by_class = {}
    for r in rows:
        c = r.get('class')
        if c:
            by_class.setdefault(c, []).append(r)
    fails = []
    for c, rs in sorted(by_class.items()):
        if len(rs) < 2:
            continue
        spec = classes.get(c) or {}
        gate = spec.get('gate')
        receipt = spec.get('falsifier_receipt')
        occ = spec.get('last_occurrence_commit')
        if not gate:
            fails.append('%s rows=%d no-gate' % (c, len(rs)))
            continue
        if not receipt or not blob_exists(a.lane, a.rev, receipt):
            fails.append('%s rows=%d gate=%s receipt-missing' % (c, len(rs), gate))
            continue
        if occ and not ancestor(a.lane, occ, a.rev):
            fails.append('%s rows=%d occurrence-not-in-tree' % (c, len(rs)))
            continue
        rc = git(a.lane, 'log', '-1', '--format=%H', a.rev, '--', receipt).stdout.strip()
        if occ and rc and ancestor(a.lane, rc, occ) and rc != occ:
            fails.append('%s rows=%d gate=%s receipt-older-than-occurrence' % (c, len(rs), gate))
    for f in fails:
        print('RECURRENCE FAIL ' + f)
    print('RECURRENCE_CHECK classes=%d multi=%d fails=%d' % (
        len(by_class), sum(1 for v in by_class.values() if len(v) >= 2), len(fails)))
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
