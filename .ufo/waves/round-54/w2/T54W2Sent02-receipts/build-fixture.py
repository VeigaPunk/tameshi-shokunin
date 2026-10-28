#!/usr/bin/env python3
"""Sentinel T54W2Sent02 fixture builder: hand-bind a round-54 re-key at C1.

Everything is written inside the CLONE passed as argv[1]; the lane is only read
(via the --shared clone).  Usage:

    build-fixture.py CLONE C0_HEX40

It appends, for every SKILL.md section at C1 that the committed ledger does not
credit, one entry whose `sha256` is the section sha and whose inputs/traces are
hand-bound under .ufo/evidence/round-21/coldread/rekey-r54-<c0[:12]>/ , and it
commits the wave reader report that pins each frozen heading at c0.

It prints a JSON summary of what it wrote; it does not run any counter.
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
R18 = '.ufo/evidence/round-18/measure.py'
REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-%s'
WAVE = '.ufo/waves/round-54/w1'
INPUT = 'corpus/SOURCES.md'
FROZEN = json.loads(Path(sys.argv[3]).read_text('utf-8')) if len(sys.argv) > 3 else None


def git(*args, cwd=None, check=True):
    r = subprocess.run(['git', '-C', cwd or CLONE] + list(args), env=ENV,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit('git %s failed: %s' % (' '.join(args), r.stderr.strip()))
    return r


def blob(rev, path):
    r = git('cat-file', 'blob', '%s:%s' % (rev, path), check=False)
    return r.stdout.encode() if r.returncode == 0 else None


CLONE = sys.argv[1]
C0 = sys.argv[2]
TOP = git('rev-parse', '--show-toplevel').stdout.strip()
assert os.path.realpath(TOP) == os.path.realpath(CLONE), (TOP, CLONE)
HEAD = git('rev-parse', 'HEAD').stdout.strip()
assert HEAD == C0, ('clone must be checked out at C1 %s, got %s' % (C0, HEAD))

spec = importlib.util.spec_from_file_location('r18fix', os.path.join(CLONE, R18))
r18 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r18)

skill_raw = blob(HEAD, 'SKILL.md')
sections = r18.sectionize(skill_raw)
ledger_path = os.path.join(CLONE, LEDGER)
ledger = json.loads(Path(ledger_path).read_text('utf-8'))
entries = ledger['entries']

input_sha = hashlib.sha256(blob(HEAD, INPUT)).hexdigest()

# which sections are currently uncredited?
before = r18.coldread(CLONE, HEAD, skill_raw,
                      Path(ledger_path).read_bytes(), strict=True)
uncredited = sorted(s['heading'] for s in before['sections'] if not s['credited'])
assert len(before['sections']) == 64, len(before['sections'])
print('uncredited-at-C1=%d' % len(uncredited))

rel = REKEY % C0[:12]
trace_dir = os.path.join(CLONE, rel, 'traces')
os.makedirs(trace_dir, exist_ok=True)
added, added_headings = [], []
for n, sec in enumerate(sections, 1):
    if sec['heading'] not in uncredited:
        continue
    trace_rel = '%s/traces/section-%02d.json' % (rel, n)
    trace_abs = os.path.join(CLONE, trace_rel)
    receipt = {'schema': 'tameshi-trace-inputs-v1',
               'inputs': {INPUT: input_sha}}
    Path(trace_abs).write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n', 'utf-8')
    entry = {
        'heading': sec['heading'],
        'start': sec['start'],
        'sha256': sec['sha256'],
        'skill_sha256': hashlib.sha256(skill_raw).hexdigest(),
        'class': 'instruction',
        'verdict': 'executed-ok',
        'commands_executed_count': 1,
        'wrong_expectations': 0,
        'blocking_gaps': 0,
        'read_rev': C0,
        'inputs': {INPUT: input_sha},
        'traces': [trace_rel],
    }
    added.append(entry)
    added_headings.append(sec['heading'])
ledger['entries'] = entries + added
Path(ledger_path).write_text(json.dumps(ledger, indent=1, sort_keys=True) + '\n', 'utf-8')

# reader reports pinning the frozen headings at c0, over the C1 section bytes
os.makedirs(os.path.join(CLONE, WAVE), exist_ok=True)
by_heading = {s['heading']: s for s in sections}
pinned = []
for i, h in enumerate(FROZEN, 1):
    sec = by_heading.get(h)
    assert sec is not None, 'frozen heading absent at C1: %r' % h
    doc = {'heading': h, 'cand': C0, 'section_sha256': sec['sha256'],
           'findings': []}
    Path(os.path.join(CLONE, WAVE, 'T54W1Read%02d.json' % i)).write_text(
        json.dumps(doc, indent=1, sort_keys=True) + '\n', 'utf-8')
    pinned.append({'file': 'T54W1Read%02d.json' % i, 'heading': h,
                   'section_sha256': sec['sha256']})

git('add', '-A')
git('-c', 'user.name=sentinel', '-c', 'user.email=sentinel@example.invalid',
    'commit', '--quiet', '-m', 'T54W2Sent02 fixture: hand-bind rekey-r54 at C1')
print(json.dumps({'fixture_rev': git('rev-parse', 'HEAD').stdout.strip(),
                  'c0': C0, 'rekey_dir': rel,
                  'input': INPUT, 'input_sha': input_sha,
                  'entries_added': len(added),
                  'uncredited_before': len(uncredited),
                  'headings_added': added_headings,
                  'readers': pinned}, indent=1))
