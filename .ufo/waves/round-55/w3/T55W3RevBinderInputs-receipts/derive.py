#!/usr/bin/env python3
"""Independently derive the round-55 lost-section set at C0 and compare it with
.ufo/evidence/round-55/c1/lost-headings-at-c0.json.

Usage: derive.py CLONE LANE C0 BASE

CLONE is a --shared clone of LANE (read-only use: git show / cat-file only).
The credit predicate replicated is the round-18/round-21 one: a section is
credited iff >=1 ledger entry carrying its section sha passes the class gate,
has commands_executed_count > 0 and has every recorded input (minus
IGNORED_INPUTS) verify as a blob of that sha256 at C0.
"""
import collections
import hashlib
import importlib.util
import json
import subprocess
import sys

CLONE, LANE, C0, BASE = sys.argv[1:5]
R18 = LANE + '/.ufo/evidence/round-18/measure.py'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
IGN = frozenset(('SKILL.md', '.ufo/evidence/round-17/coldread/ledger.json',
                 '.ufo/evidence/round-18/coldread/ledger.json', LEDGER))
FAIL = frozenset(('gap-blocking', 'wrong-expectation', 'not-executed'))
REC = frozenset(('verified-record', 'gap-minor'))
EXEC = frozenset(('executed-ok', 'gap-minor'))


def show(rev, path):
    return subprocess.run(['git', '-C', CLONE, 'show', '%s:%s' % (rev, path)],
                          capture_output=True).stdout


def tree_sha256(rev, paths):
    """path -> sha256(content at REV), one cat-file --batch."""
    out = subprocess.run(['git', '-C', CLONE, 'cat-file', '--batch'],
                         input=('\n'.join('%s:%s' % (rev, p) for p in paths) + '\n').encode(),
                         capture_output=True).stdout
    result, i = {}, 0
    for p in paths:
        nl = out.index(b'\n', i)
        parts = out[i:nl].decode().split()
        if len(parts) < 3:
            i = nl + 1
            continue
        size = int(parts[2])
        result[p] = hashlib.sha256(out[nl + 1:nl + 1 + size]).hexdigest()
        i = nl + 1 + size + 1
    return result


def entry_reason(entry, sha):
    verdict, cls = entry.get('verdict'), entry.get('class')
    if verdict in FAIL:
        return 'verdict'
    if cls == 'record' and verdict not in REC:
        return 'verdict-class'
    if cls == 'instruction' and verdict not in EXEC:
        return 'verdict-class'
    if cls not in ('record', 'instruction'):
        return 'class'
    count = entry.get('commands_executed_count', 0)
    if type(count) is not int or count <= 0:
        return 'commands'
    view = {p: s for p, s in (entry.get('inputs') or {}).items() if p not in IGN}
    if not view:
        return 'inputs-unrecorded'
    drift = sorted(p for p, s in view.items() if sha.get(p) != s)
    return 'input-drift:%s' % ','.join(drift) if drift else None


spec = importlib.util.spec_from_file_location('r18', R18)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sections = mod.sectionize(show(C0, 'SKILL.md'))
entries = json.loads(show(C0, LEDGER))['entries']
paths = [r.split(b'\t', 1)[1].decode()
         for r in subprocess.run(['git', '-C', CLONE, 'ls-tree', '-r', '-z', C0],
                                 capture_output=True).stdout.split(b'\0') if r]
sha = tree_sha256(C0, paths)
by_sha = collections.defaultdict(list)
for e in entries:
    if isinstance(e, dict) and isinstance(e.get('sha256'), str):
        by_sha[e['sha256']].append(e)

changed = set(subprocess.run(['git', '-C', CLONE, 'diff', '--name-only', BASE, C0],
                             capture_output=True).stdout.decode().split())
lost = []
print('sections=%d tree=%d entries=%d' % (len(sections), len(paths), len(entries)))
for sec in sections:
    matches = by_sha.get(sec['sha256'], [])
    reasons = [entry_reason(e, sha) for e in matches]
    if any(r is None for r in reasons):
        continue
    drift = sorted({p for e in matches for p in (e.get('inputs') or {})
                    if p not in IGN and sha.get(p) != e['inputs'][p]})
    lost.append(sec['heading'])
    cause = [p for p in drift if p in changed]
    print('LOST start=%d heading=%s drift=%d round_cause=%s'
          % (sec['start'], sec['heading'], len(drift), ','.join(cause) or '-'))
print('CREDITED=%d LOST=%d' % (len(sections) - len(lost), len(lost)))
declared = json.loads(open(LANE + '/.ufo/evidence/round-55/c1/lost-headings-at-c0.json').read())
print('DECLARED=%d SET_EQUAL=%s' % (len(declared), sorted(declared) == sorted(lost)))
