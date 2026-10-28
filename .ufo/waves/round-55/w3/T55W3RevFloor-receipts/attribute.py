#!/usr/bin/env python3
"""Attribute every cold-read loss base->C0 to the ledger entry that stopped crediting,
and to the input path(s) that newly drifted. Reads git objects only."""
import hashlib
import importlib.util
import json
import subprocess
import sys

REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '0a2010acd1e92e4e332774050825e21bcfc7e079'
C0 = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
IMPL = REPO + '/.ufo/evidence/round-18/measure.py'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'

spec = importlib.util.spec_from_file_location('r18', IMPL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.DEFAULT_LEDGER_PATH = LEDGER
m.LEDGER_PATH = LEDGER
m.IGNORED_INPUTS = m.IGNORED_INPUTS | frozenset((LEDGER,))

ledger = json.loads(m.blob(REPO, C0, LEDGER))
entries = [e for e in ledger['entries'] if isinstance(e, dict)]
by_sha = {}
for e in entries:
    if isinstance(e.get('sha256'), str):
        by_sha.setdefault(e['sha256'], []).append(e)

changed = set(subprocess.run(['git', '-C', REPO, 'diff', '--name-only', BASE, C0],
                             capture_output=True, text=True).stdout.split())


def sha_at(rev, path):
    data = m.cat_file_blob(REPO, rev, path)
    return None if data is None else hashlib.sha256(data).hexdigest()


base_secs = {s['sha256']: s for s in m.sectionize(m.blob(REPO, BASE, 'SKILL.md'))}
c0_secs = m.sectionize(m.blob(REPO, C0, 'SKILL.md'))

# base credited set from the frozen receipts
base_json = json.load(open(sys.argv[1]))  # noqa
c0_json = json.load(open(sys.argv[2]))
fc = {s['heading'] for s in base_json['coldread']['sections'] if s['credited']}
cc = {s['heading'] for s in c0_json['coldread']['sections'] if s['credited']}
lost = sorted(fc - cc)

out = []
for heading in lost:
    sec = next(s for s in c0_secs if s['heading'] == heading)
    rec = {'heading': heading, 'start': sec['start'], 'sha_at_c0': sec['sha256'],
           'sha_at_base': base_secs.get(sec['sha256'], {}).get('sha256'),
           'section_text_unchanged': sec['sha256'] in base_secs,
           'entries': [], 'newly_drifted': [], 'attributable': None,
           'unattributable_inputs': []}
    matches = by_sha.get(sec['sha256'], [])
    if not matches:
        rec['cause'] = 'no-ledger-entry (section bytes changed -> new sha)'
        # proof: the base section with same heading has a different sha and does have entries
        base_sec = next((s for s in m.sectionize(m.blob(REPO, BASE, 'SKILL.md'))
                         if s['heading'] == heading), None)
        rec['base_sha'] = base_sec['sha256'] if base_sec else None
        rec['base_entries'] = len(by_sha.get(base_sec['sha256'], [])) if base_sec else 0
        out.append(rec)
        continue
    newly = []
    for e in matches:
        rb = m.entry_reason(REPO, BASE, e, True)
        rc = m.entry_reason(REPO, C0, e, True)
        stale_b = m.entry_is_stale(REPO, BASE, e)
        stale_c = m.entry_is_stale(REPO, C0, e)
        row = {'seat': (e.get('seats') or ['?'])[0], 'read_rev': (e.get('read_rev') or '')[:12],
               'base_reason': rb, 'c0_reason': rc, 'stale_base': stale_b, 'stale_c0': stale_c,
               'inputs': sorted((e.get('inputs') or {}))}
        rec['entries'].append(row)
        if rb is None and rc is not None:
            newly.append(row)
    rec['crediting_entries_at_base'] = sum(1 for r in rec['entries'] if r['base_reason'] is None)
    if not newly:
        rec['cause'] = 'no entry credited at base (section was credited by another mechanism?)'
        out.append(rec)
        continue
    drifted = set()
    for row in newly:
        for tok in (row['c0_reason'] or '').split(';'):
            if tok.startswith('input-drift:') or tok.startswith('input-missing:') \
                    or tok.startswith('input-not-blob:'):
                drifted.add(tok.split(':', 1)[1])
    rec['newly_drifted'] = sorted(drifted)
    rec['lost_entries'] = [r['seat'] for r in newly]
    rec['attributable'] = all(p in changed for p in drifted)
    rec['unattributable_inputs'] = sorted(p for p in drifted if p not in changed)
    rec['cause'] = 'input-drift on newly changed file(s)' if rec['attributable'] else 'DRIFT ON UNCHANGED FILE'
    out.append(rec)

json.dump({'base': BASE, 'c0': C0, 'credited_base': len(fc), 'credited_c0': len(cc),
           'lost': len(lost), 'rows': out}, open(sys.argv[3], 'w'), indent=1)
print()

for r in out:
    print('%-72s -> %s' % (r['heading'][:72], r['cause']))
    if r.get('newly_drifted'):
        print('    lost seats %s  newly drifted: %s  attributable=%s'
              % (r['lost_entries'], ','.join(r['newly_drifted']), r['attributable']))
    if r.get('unattributable_inputs'):
        print('    !! UNATTRIBUTABLE: %s' % ','.join(r['unattributable_inputs']))
