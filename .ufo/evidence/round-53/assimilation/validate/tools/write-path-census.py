#!/usr/bin/env python3
"""write-path-census.py — F4 expected-value write-path census (tameshi round 39).

Counts, under a frozen pattern list, write sites in the lane's own gate tools
and classifies an expected-value write as unflagged when the file names no
explicit update flag. The behavioural fixture actually writes an expected file
only when update is true.

This is not a full lexer and not a claim that every write in every language
is seen. Shell redirects and writes whose path is not on the same line as the
call are outside the frozen patterns.

Exit codes: 0 pass · 1 fail · 2 usage.
"""
import argparse
import hashlib
import os
import re
import sys
import tempfile

GATES = (
    'bash-witness-study.py',
    'command-binding.py',
    'context-capture.py',
    'env-diff.py',
    'evidence-disposition.py',
    'golden-verdict.py',
    'mte-interop.py',
    'mutate-and-run.sh',
    'pin-disposition.py',
    'receipt-measure.py',
    'receipt-window.py',
    'registry-check.py',
    'registry-replay.py',
    'repeat-control.py',
    'tally-audit.py',
    'tally-audit-v2.py',
    'tally-audit-v3.py',
    'trace-inputs.py',
    'wave-accounting.py',
    'wave-route-mix.py',
    'witness-metadata.py',
)

WRITE_RE = re.compile(
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
)
EXPECTED_RE = re.compile(
    r"""['"][^'"]*(?:\.expected\b|expected\.txt|golden|snapshot)[^'"]*['"]"""
)
SCRATCH_RE = re.compile(r'/tmp/|tempfile|TemporaryDirectory|NamedTemporaryFile|\bscratch\b')
FLAG_RE = re.compile(r'--update_goldens|--update-goldens|--update\b|update_goldens')

PLANTED = {
    'unflagged': 'open("case.expected", "w")\n',
    'flagged': 'if "--update_goldens" in argv:\n    open("case.expected", "w")\n',
    'scratch': 'open("/tmp/census-scratch.txt", "w")\n',
}


def classify_text(text):
    flagged = FLAG_RE.search(text) is not None
    write_sites = 0
    unflagged = 0
    for line in text.splitlines():
        if WRITE_RE.search(line) is None:
            continue
        write_sites += 1
        if EXPECTED_RE.search(line) and SCRATCH_RE.search(line) is None and not flagged:
            unflagged += 1
    return write_sites, unflagged


def update_expected(path, value, update):
    """Write an expected-value file only when update is true."""
    if not update:
        return False  # FLAG_GATE
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(value)
    return True


def selftest():
    failed = []
    got = {name: classify_text(body)[1] for name, body in PLANTED.items()}
    expect = {'unflagged': 1, 'flagged': 0, 'scratch': 0}
    for name, want in expect.items():
        if got[name] != want:
            failed.append('planted %s: want unflagged=%d got %d' % (name, want, got[name]))
    with tempfile.TemporaryDirectory(prefix='write-path-census-') as tmp:
        path = os.path.join(tmp, 'case.expected')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write('old\n')
        wrote = update_expected(path, 'new\n', False)
        with open(path, encoding='utf-8') as fh:
            unchanged = fh.read() == 'old\n'
        if wrote or not unchanged:
            failed.append('no-flag path wrote or changed the expected file')
        wrote = update_expected(path, 'new\n', True)
        with open(path, encoding='utf-8') as fh:
            changed = fh.read() == 'new\n'
        if not wrote or not changed:
            failed.append('update flag did not write the expected file')
    fixture_wrote = 0 if any('update flag' in item or 'no-flag' in item for item in failed) else 1
    print(
        'WRITE_CENSUS_SELFTEST: planted_unflagged=%d planted_flagged=%d planted_scratch=%d fixture_wrote=%d noflag_unchanged=%d'
        % (got['unflagged'], got['flagged'], got['scratch'], fixture_wrote, 1 if fixture_wrote else 0)
    )
    for item in failed:
        print('FAIL %s' % item)
    return 0 if not failed else 1


def census(root):
    missing = []
    write_sites = 0
    unflagged = 0
    rows = []
    for name in GATES:
        path = os.path.join(root, 'tools', name)
        if not os.path.isfile(path):
            missing.append(name)
            continue
        with open(path, encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
        sites, bare = classify_text(text)
        write_sites += sites
        unflagged += bare
        rows.append((name, sites, bare, digest))
    classified = len(GATES) - len(missing)
    print(
        'WRITE_CENSUS: gates=%d/%d live_write_sites=%d live_unflagged=%d missing=%d'
        % (classified, len(GATES), write_sites, unflagged, len(missing))
    )
    for name, sites, bare, digest in rows:
        print('GATE %s write_sites=%d unflagged=%d sha256=%s' % (name, sites, bare, digest))
    for name in missing:
        print('MISSING %s' % name)
    return 0 if not missing else 1


def main():
    ap = argparse.ArgumentParser(description='F4 write-path census')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--census', metavar='ROOT', help='lane root whose tools/ is classified')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.census:
        return census(args.census)
    ap.print_usage(sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
