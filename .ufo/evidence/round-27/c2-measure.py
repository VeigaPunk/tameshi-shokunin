#!/usr/bin/env python3
"""Round 27 C2 counter (frontier F8, oracle anchoring), frozen at pre-registration.

Usage: c2-measure.py --repo LANE_CLONE [--rev REV] [--kumitate DIR]

Reads committed bytes at REV (default HEAD) of the lane clone only, plus the pinned
kumitate blob. Counts the round-26 cite-check suite-hole survivors that are
classified against an independently anchored expectation. A survivor counts as
classified only when all of these hold at REV:
  1. `.ufo/evidence/round-27/f8/anchors.json` names it with an expectation and at
     least one anchor; every `contract` anchor quote occurs on its named line of the
     pinned blob (whitespace-normalised), and every `external` anchor cites a
     SOURCES.md row with status `mined` and opened 2026-10-22 whose row text
     contains the quote (whitespace-normalised);
  2. `.ufo/evidence/round-27/f8/receipt.json` has a result for it whose
     `probe_sha256` equals sha256 of `.ufo/evidence/round-27/f8/anchor-probe.py` at
     REV and whose `anchors_sha256` equals sha256 of anchors.json at REV (the
     receipt is bound to the bytes that produced it), with a `class` set and both
     `*_meets_anchor` fields present;
  3. the entry `corpus/knowledge/oracle-anchored-survivors.md` exists with a
     `ground: F8` line and a `source:` line naming S012, and the S012 row is
     `mined` with the entry path in its `used-by` cell. (Amendment 1, before any
     after-measurement: the frozen text required S012's `opened` cell to read
     2026-10-22, but CORPUS.md SOURCES contract rule 2 lets only status, recheck
     and used-by change in place; the re-open is recorded in the round-27 lesson
     Gate instead.)
Prints `C2_F8: survivors=4 classified=N anchored_holes=M` and one line per
survivor. Exit 0 iff classified == 4; 1 otherwise; 2 on usage.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys

IDS = ('S_OOR_EDGE', 'S_STRICT', 'S_USAGE', 'S_PIN_INCLUDES')
OPENED = '2026-10-22'
F8 = '.ufo/evidence/round-27/f8/'
ENTRY = 'corpus/knowledge/oracle-anchored-survivors.md'


def show(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def source_rows(text):
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.split('|')]
        if len(cells) > 11 and re.fullmatch(r'S\d{3}', cells[1]):
            rows[cells[1]] = {'line': line, 'status': cells[8], 'opened': cells[9], 'used_by': cells[11]}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', default='HEAD')
    ap.add_argument('--kumitate', default='/home/vgpnk/Projects/shokunin/kumitate-shokunin')
    a = ap.parse_args()
    rev = subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', a.rev + '^{commit}'],
                         capture_output=True, text=True)
    if rev.returncode:
        print('C2_F8: cannot resolve rev', file=sys.stderr)
        return 2
    rev = rev.stdout.strip()
    sources = show(a.repo, rev, 'corpus/SOURCES.md')
    rows = source_rows(sources.decode('utf-8')) if sources else {}
    anchors_b = show(a.repo, rev, F8 + 'anchors.json')
    receipt_b = show(a.repo, rev, F8 + 'receipt.json')
    probe_b = show(a.repo, rev, F8 + 'anchor-probe.py')
    entry_b = show(a.repo, rev, ENTRY)

    s012 = rows.get('S012', {})
    entry_ok = bool(entry_b) and bool(re.search(r'(?m)^ground: F8\b', entry_b.decode('utf-8'))) \
        and bool(re.search(r'(?m)^source:.*\bS012\b', entry_b.decode('utf-8'))) \
        and s012.get('status') == 'mined' and ENTRY in s012.get('used_by', '')
    anchors = json.loads(anchors_b) if anchors_b else {'survivors': []}
    receipt = json.loads(receipt_b) if receipt_b else {'results': []}
    bound = bool(receipt_b and probe_b and anchors_b) \
        and receipt.get('probe_sha256') == hashlib.sha256(probe_b).hexdigest() \
        and receipt.get('anchors_sha256') == hashlib.sha256(anchors_b).hexdigest()
    blob = None
    if anchors_b:
        blob = subprocess.run(['git', '-C', a.kumitate, 'show', '%s:%s' % (anchors['rev'], anchors['path'])],
                              capture_output=True).stdout
        if hashlib.sha256(blob).hexdigest() != anchors.get('blob_sha256'):
            blob = None
    blob_lines = blob.decode('utf-8').splitlines() if blob else []
    by_id = {s['id']: s for s in anchors.get('survivors', [])}
    res_by_id = {r['id']: r for r in receipt.get('results', [])}
    classified = holes = 0
    for sid in IDS:
        why = []
        s = by_id.get(sid)
        if not s or not s.get('anchors') or 'expect' not in s:
            why.append('no anchored expectation')
        else:
            for an in s['anchors']:
                if an['kind'] == 'contract':
                    ln = an.get('line', 0)
                    if not (0 < ln <= len(blob_lines) and norm(an['quote']) in norm(blob_lines[ln - 1])):
                        why.append('contract quote not on line %s' % ln)
                elif an['kind'] == 'external':
                    row = rows.get(an.get('source'), {})
                    if not (row.get('status') == 'mined' and row.get('opened') == OPENED
                            and norm(an['quote']) in norm(row.get('line', ''))):
                        why.append('external %s not a mined row opened %s carrying the quote' % (an.get('source'), OPENED))
                elif an['kind'] != 'arithmetic':
                    why.append('unknown anchor kind')
        r = res_by_id.get(sid)
        if not bound:
            why.append('receipt not bound to probe and anchors bytes')
        elif not r or 'class' not in r or 'pristine_meets_anchor' not in r or 'mutant_meets_anchor' not in r:
            why.append('no executed result')
        if not entry_ok:
            why.append('F8 entry or mined S012 missing')
        if why:
            print('  %s: UNCLASSIFIED (%s)' % (sid, '; '.join(why)))
            continue
        classified += 1
        holes += r['class'] == 'anchored-hole'
        print('  %s: %s pristine_meets=%s mutant_meets=%s' % (sid, r['class'], r['pristine_meets_anchor'], r['mutant_meets_anchor']))
    print('C2_F8: survivors=%d classified=%d anchored_holes=%d rev=%s' % (len(IDS), classified, holes, rev))
    return 0 if classified == len(IDS) else 1


if __name__ == '__main__':
    raise SystemExit(main())
