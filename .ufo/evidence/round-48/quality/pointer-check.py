#!/usr/bin/env python3
"""Round-48 pointer check: every backticked repo path in a record block must exist at REV.

Mined mistake (corpus/lessons/round-48.md `## Mistakes`, prospective-record row): the attempt-1 L1 wrote its
round-48 LOG.md entry and QUALITY 94-96 before the work they describe; the orchestrator salvage commit 15b1521
landed them with pointers to receipts that did not exist yet. This check reads the block of FILE at REV that
starts at the first line containing --start (to the end of the file), takes every backticked token that looks
like a lane path (starts with `.ufo/`, `corpus/`, `tools/`, `SCORECARD.md`, `LOG.md`, or with one of the
round-48 evidence subdirectories, which resolve under .ufo/evidence/round-48/), drops a `:N` / `:N-M` line
suffix, and checks `git cat-file -e REV:path`. Tokens with glob, brace, ellipsis or placeholder characters are
skipped and counted. Prints `MISSING <path>` per absent path and a summary line
`POINTERS: checked=N missing=M skipped=K rev=REV`; exit 1 when missing>0 or checked=0.

Usage: pointer-check.py --lane LANE --rev REV --file PATH --start TEXT
       pointer-check.py --selftest
"""
import argparse
import re
import subprocess
import sys

E48 = '.ufo/evidence/round-48/'
ROOTS = ('.ufo/', 'corpus/', 'tools/', 'SCORECARD.md', 'LOG.md', 'SHONEN.md', 'PROVINCE.md')
SUBS = ('quality/', 'control/', 'calibration/', 'freshness/', 'selftest/', 'after/', 'before/')
TOKEN = re.compile(r'`([^`\s]+)`')
SKIP = re.compile(r'[*?{}<>…|]|\.\.\.|\bN\b|\$')


def candidates(text):
    out, skipped = [], 0
    for tok in TOKEN.findall(text):
        tok = re.sub(r':\d+(?:[-,]\d+)*$', '', tok).rstrip('.,;')
        if tok.startswith(SUBS):
            tok = E48 + tok
        if not tok.startswith(ROOTS):
            continue
        if SKIP.search(tok):
            skipped += 1
            continue
        out.append(tok.rstrip('/'))
    return sorted(set(out)), skipped


def exists(lane, rev, path):
    return subprocess.run(['git', '-C', lane, 'cat-file', '-e', '%s:%s' % (rev, path)],
                          capture_output=True).returncode == 0


def check(text, present):
    paths, skipped = candidates(text)
    missing = [p for p in paths if not present(p)]
    return paths, missing, skipped


def selftest():
    fails = 0
    cases = [
        ('present', 'see `.ufo/evidence/round-48/a.txt:3` and `quality/b.stdout`', {'.ufo/evidence/round-48/a.txt', '.ufo/evidence/round-48/quality/b.stdout'}, 0, 2),
        ('missing', 'receipt `control/c1-controls.stdout`', set(), 1, 1),
        ('skip-glob', '`.ufo/waves/round-48/w1/T48*.md` and `corpus/{a,b}.md`', set(), 0, 0),
        ('not-a-path', '`REGRESSION: PASS` `runs 3`', set(), 0, 0),
    ]
    for name, text, have, want_missing, want_checked in cases:
        paths, missing, _ = check(text, lambda p: p in have)
        ok = len(missing) == want_missing and len(paths) == want_checked
        fails += not ok
        print('%s %s checked=%d missing=%d' % ('PASS' if ok else 'FAIL', name, len(paths), len(missing)))
    print('POINTER_CHECK_SELFTEST: cases=%d failed=%d' % (len(cases), fails))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--file')
    ap.add_argument('--start')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    rev = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', a.rev + '^{commit}'],
                         capture_output=True, text=True, check=True).stdout.strip()
    body = subprocess.run(['git', '-C', a.lane, 'show', '%s:%s' % (rev, a.file)],
                          capture_output=True, text=True, check=True).stdout
    i = body.find(a.start)
    if i < 0:
        print('POINTERS: start text not found in %s at %s' % (a.file, rev))
        return 2
    paths, missing, skipped = check(body[i:], lambda p: exists(a.lane, rev, p))
    for p in missing:
        print('MISSING ' + p)
    print('POINTERS: file=%s checked=%d missing=%d skipped=%d rev=%s' % (a.file, len(paths), len(missing), skipped, rev))
    return 1 if (missing or not paths) else 0


if __name__ == '__main__':
    sys.exit(main())
