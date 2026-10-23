#!/usr/bin/env python3
"""Round 33 C2 counter (freshness: S055 doctest-row drift repair), frozen before any data run.

Claim C2 (contract .ufo/evidence/round-33/contract.json): corpus/SOURCES.md at REV carries a row
(id > S099) whose teaches cell opens `supersedes S055 -`, naming a VERSIONED python docs URL
(docs.python.org/3.<n>/..., never the moving /3/ alias); the fetched bytes of that URL, taken this
round, are committed at .ufo/evidence/round-33/c2/doctest-snapshot.html and their sha256 equals
(1) the digest recorded in the round-33 lesson Gate at REV and (2) the digest frozen in this
counter; and the snapshot contains the quoted module-introduction sentence the row teaches. This
turns the S055 digest drift (re-opened round 31, carried through round 32) into a pinned,
re-derivable record: re-derivation runs over committed bytes, no live fetch. Label: C2_R33_PASS.

Kill rule (frozen): the first full run at the measurement revision decides; false is a miss.
The live re-open itself is evidenced by the round-33 lesson Gate (URL, access date, bytes, sha256,
<=25-word quote); this counter verifies the committed record coheres.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
QUOTE = b'The doctest module searches for pieces of text that look like interactive Python sessions'
SNAPSHOT = '.ufo/evidence/round-33/c2/doctest-snapshot.html'
LESSON = 'corpus/lessons/round-33.md'
EXPECTED_SHA = '217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899'  # pinned at freeze; see contract.json ("snapshot_sha")


def git(lane, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_OPTIONAL_LOCKS'] = '0'
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True, env=env)


def show(lane, rev, path):
    r = git(lane, 'show', '%s:%s' % (rev, path))
    return r.stdout if r.returncode == 0 else None


def parse_row(line):
    cells = [c.strip() for c in line.split('|')]
    return cells  # cells[1] = id, cells[3] = url cell, cells[8] = teaches (0-based with empties)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    a = ap.parse_args()

    sources = show(a.lane, a.rev, 'corpus/SOURCES.md')
    row_id = url = teaches = None
    if sources:
        for line in sources.decode('utf-8', 'replace').splitlines():
            m = re.match(r'^\|\s*(S[0-9]{3,})\s*\|', line)
            if not m:
                continue
            cells = [c.strip() for c in line.split('|')]
            # cells: ['', id, source-url-cell, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by, '']
            t = cells[7] if len(cells) > 8 else ''
            if re.match(r'^supersedes S055(\s|[—–-])', t) and int(m.group(1)[1:]) > 99:
                row_id = m.group(1)
                url = cells[2]
                teaches = t
                break
    versioned = bool(url and re.search(r'docs\.python\.org/3\.[0-9]+/', url))
    snap = show(a.lane, a.rev, SNAPSHOT)
    snap_sha_ok = EXPECTED_SHA is not None and snap is not None and \
        hashlib.sha256(snap).hexdigest() == EXPECTED_SHA
    quote_ok = bool(snap and QUOTE in snap)
    lesson = show(a.lane, a.rev, LESSON) or b''
    gate_sha_ok = False
    if snap is not None:
        lesson_text = lesson.decode('utf-8', 'replace')
        gm = re.search(r'^## Gate\b(.*?)(?=^## |\Z)', lesson_text, re.M | re.S)
        block = gm.group(1) if gm else ''
        digests = re.findall(r'sha256[ :=]+`?([0-9a-f]{64})`?', block)
        gate_sha_ok = (hashlib.sha256(snap).hexdigest() in digests
                       and 'https://docs.python.org/3.15/library/doctest.html' in block)
    ok = bool(row_id and versioned and snap_sha_ok and quote_ok and gate_sha_ok)
    print('C2_R33: row=%s versioned_url=%d snapshot_sha_ok=%d gate_sha_ok=%d quote_ok=%d C2_R33_PASS=%s'
          % (row_id or 'none', int(versioned), int(snap_sha_ok), int(gate_sha_ok), int(quote_ok),
             'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
