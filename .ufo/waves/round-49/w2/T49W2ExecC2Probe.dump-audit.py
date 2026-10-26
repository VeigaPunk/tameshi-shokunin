#!/usr/bin/env python3
"""Seat T49W2ExecC2Probe: independent audit of the seed-4949 dump.

Re-runs the pristine pinned guard over every dumped case (the generator's own dump, unmodified),
classifies each case with an INDEPENDENT classifier written here (not the generator's, not the
counter's), and tallies which documented guard surfaces the case stream actually exercises.
"""
import collections
import json
import os
import re
import subprocess
import sys
import tempfile

S = '/fast/scratch/hyaku/tameshi-r49/T49W2ExecC2Probe'
GUARD = os.path.join(S, 'cand', 'tools/staged-id-guard.py')
DUMP = os.path.join(S, 'w', 's4949', 'dump.jsonl')
ROW = re.compile(r'^( *)\|\s*(S\d{3,})\s*\|')
SHA = ('registry_sha256', 'staged_sha256')

cases = [json.loads(ln) for ln in open(DUMP, encoding='utf-8') if ln.strip()]
print('dump cases: %d' % len(cases))

cls = collections.Counter()
fields = collections.defaultdict(collections.Counter)
reasons = collections.Counter()
exits = collections.Counter()

work = tempfile.mkdtemp(prefix='audit-', dir=os.path.join(S, 'w'))
for c in cases:
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
        js = None
    exits[r.returncode] += 1

    # ---- independent classification, from case bytes + observed exit only
    found = set()
    for line in c['registry'].splitlines() + c['staged'].splitlines():
        m = ROW.match(line)
        if not m:
            continue
        ind = len(m.group(1))
        if 1 <= ind <= 3:
            found.add('indent_1_3')
        if ind >= 4:
            found.add('indent_4_plus')
        if ind <= 3 and len(m.group(2)) >= 5:
            found.add('id_4_plus_digits')
    if c['map'] is None:
        if r.returncode in (0, 1) and isinstance(js, dict):
            found.add('collision' if js.get('collision_count', 0) else 'no_collision')
            if js.get('held'):
                found.add('held')
            if js.get('unmapped'):
                found.add('unmapped')
            if js.get('cascade'):
                found.add('cascade')
        if r.returncode == 2:
            found.add('refusal')
    else:
        found.add('map')
        if r.returncode == 1:
            found.add('map_inadmissible')
        if r.returncode == 2:
            found.add('refusal')
    registry_forms = {}
    for u in re.findall(r'https?://[^\s|,;]+', c['registry']):
        u = u.rstrip('.,;)]')
        registry_forms.setdefault(re.sub(r'^www\.', '', re.sub(r'^https?://', '', u.strip().lower())).rstrip('/'), set()).add(u)
    for u in re.findall(r'https?://[^\s|,;]+', c['staged']):
        u = u.rstrip('.,;)]')
        key = re.sub(r'^www\.', '', re.sub(r'^https?://', '', u.strip().lower())).rstrip('/')
        if key in registry_forms and any(o != u for o in registry_forms[key]):
            found.add('url_form_variant')
            break
    for f in found:
        cls[f] += 1

    if isinstance(js, dict):
        for k, v in js.items():
            if k in SHA:
                fields[k]['present'] += 1
                continue
            if v in (0, '', [], {}, None):
                continue
            if k == 'verdict':
                fields[k][v] += 1
            elif k == 'extractor':
                fields[k][v] += 1
            else:
                fields[k]['non-empty'] += 1
        for reason in js.get('map_reasons') or []:
            text = reason if isinstance(reason, str) else repr(reason)
            for tag, pat in (('injective', 'not injective'), ('carry', 'does not carry'),
                             ('registry', 'collide with registry'),
                             ('staged', 'still staged ids'), ('floor', 'below the safe floor'),
                             ('cover', 'does not cover'), ('self', 'on itself'),
                             ('undocumented', 'undocumented row'), ('held', 'held document off')):
                if pat in text:
                    reasons['map:' + tag] += 1
                    break
            else:
                reasons['map:other:%s' % text[:40]] += 1
    elif r.returncode == 2:
        try:
            reason = json.loads(r.stdout).get('reason', '')
        except ValueError:
            reason = ''
        for tag, pat in (('malformed-row', 'malformed row'), ('duplicate-id', 'duplicate id'),
                         ('not-json', 'not JSON'), ('no-map-object', 'no "map" object'),
                         ('key-not-sid', 'key is not an S-id'),
                         ('target-not-sid', 'target is not an S-id'),
                         ('dup-key', 'repeats the key'),
                         ('not-utf8', 'not valid UTF-8'), ('oversized', 'larger than'),
                         ('non-regular', 'not a regular file'), ('cannot-stat', 'cannot stat')):
            if pat in reason:
                reasons['setup:' + tag] += 1
                break
        else:
            reasons['setup:other:%s' % reason[:50]] += 1

print('\n--- independent class counts (CLASS_MIN contract floor = 10) ---')
for name in ('indent_1_3', 'indent_4_plus', 'id_4_plus_digits', 'collision', 'no_collision',
             'held', 'unmapped', 'cascade', 'refusal', 'url_form_variant', 'map',
             'map_inadmissible'):
    print('%-20s %4d%s' % (name, cls[name], '' if cls[name] >= 10 else '  SHORT'))
print('\n--- guard exits observed ---')
for k in sorted(exits):
    print('exit %s: %d' % (k, exits[k]))
print('\n--- JSON fields carrying a non-empty value (sha: presence only) ---')
for k in sorted(fields):
    print('%-18s %s' % (k, dict(fields[k])))
print('\n--- refusal vocabularies exercised ---')
for k in sorted(reasons):
    print('%-28s %d' % (k, reasons[k]))
print('\nurl_form_variant cases (my own url tally skipped; generator reported it)')
