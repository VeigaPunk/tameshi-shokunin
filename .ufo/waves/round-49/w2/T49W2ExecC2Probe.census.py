#!/usr/bin/env python3
"""Seat T49W2ExecC2Probe: blind-spot census over the seed-4949 dump.

For each survivor mutant of my probe, measure whether the case stream can even reach its region:
input sizes, dash codepoints, registry rows without a document, two registry rows sharing a
document, and the shape of every map document.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import collections

S = '/fast/scratch/hyaku/tameshi-r49/T49W2ExecC2Probe'
GUARD = os.path.join(S, 'cand', 'tools/staged-id-guard.py')
DUMP = os.path.join(S, 'w', 's4949', 'dump.jsonl')
ROW = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL = re.compile(r'https?://[^\s|,;]+')
PROSE = re.compile(r'\s+[\u2014\u2013]\s+')

cases = [json.loads(ln) for ln in open(DUMP, encoding='utf-8') if ln.strip()]
work = tempfile.mkdtemp(prefix='census-', dir=os.path.join(S, 'w'))
stat = collections.Counter()
maxreg = maxstg = maxmap = 0
for c in cases:
    maxreg = max(maxreg, len(c['registry']))
    maxstg = max(maxstg, len(c['staged']))
    maxmap = max(maxmap, len(json.dumps(c['map'])))
    blob = c['registry'] + c['staged']
    if '\u2013' in blob:
        stat['cases_with_en_dash'] += 1
    if '\u2014' in blob:
        stat['cases_with_em_dash'] += 1
    # registry rows: document key by the docstring rule (url, else path-like head)
    docs = []
    rows = 0
    for line in c['registry'].splitlines():
        m = ROW.match(line)
        if not m:
            continue
        rows += 1
        cells = [x.strip() for x in line.strip().strip('|').split('|')]
        found = URL.search(' '.join(cells[1:6]))
        if found:
            docs.append(found.group(0).rstrip('.,;)]'))
            continue
        head = PROSE.split(cells[1] if len(cells) > 1 else '')[0].strip()
        openable = '/' in head or (' ' not in head and re.search(r'\.[A-Za-z0-9]{2,6}$', head))
        docs.append(head if len(head) > 8 and openable else '')
    if rows and any(not d for d in docs):
        stat['cases_with_undocumented_registry_row'] += 1
    norm = [re.sub(r'^https?://', '', d.strip().lower()) for d in docs if d]
    norm = [re.sub(r'^www\.', '', x).rstrip('/') for x in norm]
    if len(norm) != len(set(norm)):
        stat['cases_with_two_registry_rows_sharing_a_document'] += 1
    if c['map'] is not None:
        stat['map_cases'] += 1
        if not isinstance(c['map'], dict):
            stat['map_not_a_dict'] += 1
    d = tempfile.mkdtemp(dir=work)
    rp, sp = os.path.join(d, 'r.md'), os.path.join(d, 's.md')
    open(rp, 'w', encoding='utf-8', newline='').write(c['registry'])
    open(sp, 'w', encoding='utf-8', newline='').write(c['staged'])
    argv = [sys.executable, '-I', GUARD, '--registry', rp, '--staged', sp]
    if c['map'] is not None:
        mp = os.path.join(d, 'm.json')
        open(mp, 'w', encoding='utf-8').write(json.dumps(c['map']))
        argv += ['--map', mp]
    argv.append('--json')
    r = subprocess.run(argv, capture_output=True, cwd=d, timeout=60)
    try:
        js = json.loads(r.stdout)
    except ValueError:
        js = {}
    if isinstance(js, dict) and js.get('registry_rows'):
        stat['cases_with_registry_rows'] += 1
        if js.get('registry_docs') != js.get('registry_rows'):
            stat['cases_where_registry_docs_differs_from_rows'] += 1

print('cases: %d (seed 4949)' % len(cases))
print('largest registry bytes: %d   largest staged bytes: %d   largest map json: %d' %
      (maxreg, maxstg, maxmap))
print('cases with a registry row carrying no document: %d'
      % stat['cases_with_undocumented_registry_row'])
print('cases with two registry rows sharing a document: %d'
      % stat['cases_with_two_registry_rows_sharing_a_document'])
print('cases with registry_docs != registry_rows (of %d with rows): %d'
      % (stat['cases_with_registry_rows'], stat['cases_where_registry_docs_differs_from_rows']))
print('cases with U+2014 em dash: %d   with U+2013 en dash: %d'
      % (stat['cases_with_em_dash'], stat['cases_with_en_dash']))
print('map cases: %d   of which non-dict: %d' % (stat['map_cases'], stat['map_not_a_dict']))
