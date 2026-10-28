#!/usr/bin/env python3
"""Recompute the round-12 section sha at one revision, two documented ways.

Primary value: the frozen round-18 sectionizer's sectionize() -- the function the
cold-read credit rule hashes sections with.  Secondary: the seat assignment's prose
cut (this heading -> the next heading of the same or higher level), recorded so the
difference between the two readings is auditable instead of hidden.  No hashing
scheme is invented here.
"""
import hashlib
import importlib.util
import subprocess

REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
MEASURE = REPO + '/.ufo/evidence/round-18/measure.py'
HEADING = '## Repeated controls and gate registry \u2014 round 12'
NEXT_SAME_OR_HIGHER = '## Pin disposition and provenance correction \u2014 round 13'

spec = importlib.util.spec_from_file_location('r18measure', MEASURE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

raw = subprocess.run(['git', '-C', REPO, 'cat-file', 'blob', REV + ':SKILL.md'],
                     capture_output=True, check=True).stdout
hits = [s for s in mod.sectionize(raw) if s['heading'] == HEADING]
assert len(hits) == 1, hits
print('sectionize (primary, ledger mechanism):', hits[0])

lines = raw.decode('utf-8', 'surrogateescape').split('\n')
i = lines.index(HEADING)
j = lines.index(NEXT_SAME_OR_HIGHER)
body = lines[i:j]
while body and body[-1].strip() == '':
    body.pop()
print('prose cut  lines %d-%d (next same-or-higher heading at %d)  sha256=%s' % (
    i + 1, i + len(body), j + 1,
    hashlib.sha256('\n'.join(body).encode('utf-8', 'surrogateescape')).hexdigest()))
print('sectionize lines %d-%d  sha256=%s' % (
    hits[0]['start'], hits[0]['end'] - 1, hits[0]['sha256']))
