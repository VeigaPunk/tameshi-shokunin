#!/usr/bin/env python3
"""Deterministic SCORECARD capability-figure repair applier (R75-C2, seat T75W1E3).

Reads scard-repairs.json (beside this script unless --manifest is given) and
applies each `old` -> `new` replacement to a SCORECARD document.  A row is
applied only when ALL of these hold, so a drifted or partially patched document
is refused instead of half-rewritten:

  * the named capability row exists in the `## Capabilities` table;
  * the `old` substring occurs exactly once inside that row;
  * the `old` substring occurs exactly once in the whole document
    (document-unique: no line-scope needed to disambiguate);
  * the `new` substring does not occur anywhere yet.

Usage
  apply-repairs.py --check [DOC]   print every row and the counts it measured,
                                   write nothing (exit 0 iff all seven would
                                   apply cleanly)
  apply-repairs.py [DOC]           apply all seven atomically, then re-read the
                                   written file and re-verify each row

DOC defaults to ./SCORECARD.md.  Exit codes: 0 ok, 1 refusal or mismatch,
2 setup (unreadable manifest/doc or bad manifest shape).
"""
import argparse
import json
import os
import sys
import tempfile

REQUIRED_KEYS = ('capability', 'old', 'new')


def capability_rows(doc_text):
    lines = doc_text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines)
                     if ln.strip() == '## Capabilities')
    except StopIteration:
        return None
    rows = {}
    for ln in lines[start + 1:]:
        if ln.startswith('## '):
            break
        if ln.startswith('|') and not ln.startswith('|---'):
            cells = [c.strip() for c in ln.strip('|').split('|')]
            if len(cells) >= 3 and cells[0] != 'Capability':
                rows[cells[0]] = ln
    return rows


def line_of(text, needle):
    idx = text.find(needle)
    return None if idx < 0 else text.count('\n', 0, idx) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('doc', nargs='?', default='SCORECARD.md')
    ap.add_argument('--manifest',
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         'scard-repairs.json'))
    ap.add_argument('--check', action='store_true',
                    help='print the plan and measured counts; write nothing')
    a = ap.parse_args()

    try:
        with open(a.manifest, encoding='utf-8') as f:
            manifest = json.load(f)
        repairs = manifest['repairs']
    except (OSError, ValueError, KeyError) as e:
        print('SETUP manifest=%r unusable: %s' % (a.manifest, e))
        return 2
    for r in repairs:
        missing = [k for k in REQUIRED_KEYS if not isinstance(r.get(k), str) or not r[k]]
        if missing:
            print('SETUP row=%r missing/invalid keys %s' % (r.get('capability'), missing))
            return 2

    try:
        with open(a.doc, encoding='utf-8', newline='') as f:
            text = f.read()
    except OSError as e:
        print('SETUP doc=%r unreadable: %s' % (a.doc, e))
        return 2
    rows = capability_rows(text)
    if rows is None:
        print('SETUP doc=%r has no ## Capabilities section' % a.doc)
        return 2

    plan = []
    problems = 0
    for r in repairs:
        cap, old, new = r['capability'], r['old'], r['new']
        row = rows.get(cap)
        row_old = row.count(old) if row is not None else 0
        doc_old = text.count(old)
        doc_new = text.count(new)
        ok = row is not None and row_old == 1 and doc_old == 1 and doc_new == 0
        print('CHECK cap=%-38s line=%-4s row_old=%d doc_old=%d new_pre=%d %s'
              % (cap, line_of(text, old), row_old, doc_old, doc_new,
                 'ok' if ok else 'REFUSED'))
        if ok:
            plan.append((cap, old, new))
        else:
            problems += 1

    if problems:
        print('APPLY_REFUSED rows=%d doc=%s (nothing written)' % (problems, a.doc))
        return 1
    if a.check:
        print('CHECK_OK rows=%d doc=%s (nothing written)' % (len(plan), a.doc))
        return 0

    new_text = text
    for i, (cap, old, new) in enumerate(plan, 1):
        if new_text.count(old) != 1 or new_text.count(new) != 0:
            print('APPLY_REFUSED row=%d cap=%r precondition lost mid-batch' % (i, cap))
            return 1
        new_text = new_text.replace(old, new, 1)
        if new_text.count(old) != 0 or new_text.count(new) != 1:
            print('APPLY_REFUSED row=%d cap=%r replacement did not land once' % (i, cap))
            return 1

    fd, tmp = tempfile.mkstemp(prefix='.apply-repairs.', dir=os.path.dirname(os.path.abspath(a.doc)))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
            f.write(new_text)
        os.replace(tmp, a.doc)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        print('APPLY_REFUSED write doc=%r failed: %s' % (a.doc, e))
        return 1

    with open(a.doc, encoding='utf-8', newline='') as f:
        written = f.read()
    verified = 0
    for cap, old, new in plan:
        if written.count(old) == 0 and written.count(new) == 1:
            verified += 1
        else:
            print('VERIFY_FAIL cap=%r old_count=%d new_count=%d'
                  % (cap, written.count(old), written.count(new)))
    print('APPLIED rows=%d doc=%s' % (len(plan), a.doc))
    print('VERIFY rows=%d/%d old_absent_new_once=%s'
          % (verified, len(plan), 'ok' if verified == len(plan) else 'FAIL'))
    return 0 if verified == len(plan) else 1


if __name__ == '__main__':
    sys.exit(main())
