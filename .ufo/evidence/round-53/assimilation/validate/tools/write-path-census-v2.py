#!/usr/bin/env python3
"""F4 write-form census v2.

Sees two write forms the round-39 pattern misses: a string literal
expected.json on a .write_bytes call, and os.replace / os.rename.
Does not edit tools/write-path-census.py. The v1 pin stays put.

Exit codes: 0 pass · 1 selftest fail · 2 usage.
"""
import argparse
import json
import os
import re
import sys

WRITE_RE = re.compile(
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
    r"""|os\.replace\s*\("""
    r"""|os\.rename\s*\("""
)
EXPECTED_RE = re.compile(
    r"""['"][^'"]*(?:\.expected\b|expected\.txt|expected\.json|golden|snapshot)[^'"]*['"]"""
)
SCRATCH_RE = re.compile(r'/tmp/|tempfile|TemporaryDirectory|NamedTemporaryFile|\bscratch\b')
FLAG_RE = re.compile(r'--update_goldens|--update-goldens|--update\b|update_goldens')

FIXTURE_REL = '.ufo/evidence/round-40/census/fixtures.json'


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


def load_fixtures(path):
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    return data


def selftest(fixture_path):
    failed = []
    planted = load_fixtures(fixture_path)
    expect = {
        'bytes_unflagged': 1,
        'replace_unflagged': 1,
        'bytes_flagged': 0,
        'replace_flagged': 0,
        'scratch_replace': 0,
    }
    got = {}
    for name, want in expect.items():
        body = planted.get(name)
        if not isinstance(body, str):
            failed.append('missing fixture %s' % name)
            got[name] = -1
            continue
        _sites, unflagged = classify_text(body)
        got[name] = unflagged
        if unflagged != want:
            failed.append('planted %s: want unflagged=%d got %d' % (name, want, unflagged))
    print(
        'WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=%d replace_unflagged=%d bytes_flagged=%d replace_flagged=%d scratch_replace=%d'
        % (
            got.get('bytes_unflagged', -1),
            got.get('replace_unflagged', -1),
            got.get('bytes_flagged', -1),
            got.get('replace_flagged', -1),
            got.get('scratch_replace', -1),
        )
    )
    for item in failed:
        print('FAIL %s' % item)
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(description='F4 write-form census v2')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--fixtures', default=None, help='fixture JSON path')
    args = ap.parse_args()
    if args.selftest:
        path = args.fixtures
        if path is None:
            here = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(os.path.dirname(here), FIXTURE_REL)
        return selftest(path)
    ap.print_usage(sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
