#!/usr/bin/env python3
"""Integrate wave-1 C1 fragments into the round-45 ledger (L1 integration step).

Reads /tmp/tameshi-r45-ExecRows*/S###.json fragments and their S###.raw
snapshots, checks that each fragment's `author` equals its seat directory,
gzips each raw snapshot to .ufo/evidence/round-45/freshness/sources/S###.raw.gz
(the raw bytes' sha256 must equal the fragment's raw_sha256), and writes
.ufo/evidence/round-45/freshness/ledger.json sorted by id. It never invents or
edits a quote or a verdict; a fragment that fails these checks is skipped and
listed. Usage: integrate.py --lane LANE [--glob PATTERN]
"""
import argparse
import glob
import gzip
import hashlib
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--lane', required=True)
ap.add_argument('--glob', default='/tmp/tameshi-r45-ExecRows*/S[0-9][0-9][0-9].json')
a = ap.parse_args()
dest = os.path.join(a.lane, '.ufo/evidence/round-45/freshness/sources')
os.makedirs(dest, exist_ok=True)
entries, skipped = {}, []
for frag in sorted(glob.glob(a.glob)):
    seat = os.path.basename(os.path.dirname(frag))[len('tameshi-r45-'):]
    try:
        e = json.load(open(frag, encoding='utf-8'))
    except ValueError as exc:
        skipped.append('%s unparsable %s' % (frag, exc))
        continue
    rid = e.get('id')
    if rid != os.path.basename(frag)[:-5]:
        skipped.append('%s id/file mismatch' % frag)
        continue
    if e.get('author') != seat:
        skipped.append('%s author %r != seat %r' % (frag, e.get('author'), seat))
        continue
    if rid in entries:
        skipped.append('%s duplicate id (kept %s)' % (frag, entries[rid]['author']))
        continue
    raw_path = frag[:-5] + '.raw'
    if e.get('verdict') != 'unreachable':
        if not os.path.isfile(raw_path):
            skipped.append('%s raw snapshot missing' % frag)
            continue
        raw = open(raw_path, 'rb').read()
        if hashlib.sha256(raw).hexdigest() != e.get('raw_sha256'):
            skipped.append('%s raw sha mismatch' % frag)
            continue
        e['snapshot'] = '.ufo/evidence/round-45/freshness/sources/%s.raw.gz' % rid
        with open(os.path.join(a.lane, e['snapshot']), 'wb') as out:
            out.write(gzip.compress(raw, mtime=0))
    entries[rid] = e
ledger = {'round': 45, 'entries': [entries[k] for k in sorted(entries, key=lambda s: int(s[1:]))]}
with open(os.path.join(a.lane, '.ufo/evidence/round-45/freshness/ledger.json'), 'w', encoding='utf-8') as f:
    json.dump(ledger, f, indent=1, ensure_ascii=False)
    f.write('\n')
for s in skipped:
    print('SKIPPED ' + s)
counts = {}
for e in entries.values():
    counts[e.get('verdict')] = counts.get(e.get('verdict'), 0) + 1
print('INTEGRATED entries=%d %s skipped=%d' % (len(entries), json.dumps(counts, sort_keys=True), len(skipped)))
