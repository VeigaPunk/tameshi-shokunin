#!/usr/bin/env python3
"""Step 2: sensitivity of X1 threshold, X6 backtick-restatement check, and X5 defeat by re-pointing."""
import importlib.util
import json
import os
import re
import subprocess
import sys

S = os.environ['S']
CL = os.path.join(S, 'clone')
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
ENV = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
spec = importlib.util.spec_from_file_location('measure50', os.path.join(S, 'measure50.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
o = json.load(open(os.path.join(S, 'out.json')))
DEF_LIST = json.loads(m.show(CL, BASE, '.ufo/evidence/round-50/c1/defects.json').decode())['defects']
DEF = {d['id']: d for d in DEF_LIST}
SPOT = {d['file']: d['file_sha256'] for d in DEF_LIST}
REAL = json.loads(m.show(CL, BASE, 'corpus/routed-defects.json').decode())
RR = {r['id']: r for r in REAL['defects']}
STOP = set('that this with from have been were will into only when than also they them their there which '
           'about would could should does doing each being after before under over across other where while '
           'since until both very more most such some'.split())


def toks(s):
    return {t for t in re.findall(r'[a-z][a-z0-9_]{3,}', s.lower()) if t not in STOP}


def G(*a):
    return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, env=ENV).stdout.decode('utf-8', 'replace')


def fresh_items(rid, row, ev_rev):
    d = DEF[rid]
    files = m.touched(CL, row['commit'])
    out = []
    for item in row['evidence']:
        if not isinstance(item, dict) or not m.has_key(item, d['keys']) or item.get('path') not in files:
            continue
        then = m.show(CL, d['routed_at'], item['path'])
        if then is not None and m.norm(item['excerpt']) in m.norm(then.decode('utf-8', 'replace')):
            continue
        a, b = (int(x) for x in item['lines'].split('-'))
        text = m.show(CL, ev_rev, item['path']).decode('utf-8', 'replace').split('\n')
        if any(w in ' '.join(text[a - 1:b]).lower() for w in m.ACK_WORDS):
            continue
        out.append(item)
    return out


def overlap_max(rid, fresh):
    return max([len(toks(i['excerpt']) & toks(DEF[rid]['text'])) for i in fresh] or [0])


def backtick_spans(text):
    return [s.strip().lower() for s in re.findall(r'`([^`\n]{3,})`', text)]


def X6_no_quoted_restatement(rid, fresh):
    """fresh excerpt does not contain a backticked span quoted in the item's own text"""
    spans = backtick_spans(DEF[rid]['text'])
    return not any(any(s in m.norm(i['excerpt']).lower() for s in spans) for i in fresh)


# ---- X1 threshold sensitivity on real fixed rows and forged rows ----
forg_rows = {k: v['row'] for k, v in o['forgery'].items()}
forg_rev = o['rev_forge']
X1_real = {}
for rid, row in RR.items():
    if row['status'] != 'fixed':
        continue
    fr = fresh_items(rid, row, BASE)
    X1_real[rid] = {'overlap': overlap_max(rid, fr), 'X6': X6_no_quoted_restatement(rid, fr), 'fresh_n': len(fr),
                    'spans': backtick_spans(DEF[rid]['text'])}
X1_forg = {}
for name, row in forg_rows.items():
    rid = row['id']
    fr = fresh_items(rid, row, forg_rev)
    X1_forg[name] = {'overlap': overlap_max(rid, fr), 'X6': X6_no_quoted_restatement(rid, fr),
                     'spans': backtick_spans(DEF[rid]['text'])}
thr = {}
for t in (1, 2, 3, 4):
    thr[t] = {'real_false_reject': [k for k, v in X1_real.items() if v['overlap'] < t],
              'forged_caught': [k for k, v in X1_forg.items() if v['overlap'] < t],
              'forged_accepted': [k for k, v in X1_forg.items() if v['overlap'] >= t]}
X6 = {'real_false_reject': [k for k, v in X1_real.items() if not v['X6']],
      'forged_caught': [k for k, v in X1_forg.items() if not v['X6']],
      'forged_accepted': [k for k, v in X1_forg.items() if v['X6']]}

# ---- X5 defeat by re-pointing: find a keyed line present at routed_at AND still at REV (same path) ----
def defeat_candidates(rid, rev):
    d = DEF[rid]
    cache = {}
    found = []
    for key in d['keys']:
        out = G('grep', '-n', '-i', '-F', '-e', key, d['routed_at'])
        for line in out.split('\n'):
            parts = line.split(':', 3)
            if len(parts) < 4:
                continue
            _, path, num, text = parts
            if not num.isdigit():
                continue
            ex = m.norm(text)
            if not (15 <= len(ex) <= 400):
                continue
            item = {'path': path, 'lines': '%s-%s' % (num, num), 'excerpt': text.strip()}
            if m.has_key(item, d['keys']) and m.check_evidence(CL, rev, item, d['keys'], SPOT, cache) is None:
                found.append(item)
                return item
    return None


rejected_flips = [k for k in o['open_checks_flipped_from_fixed'] if not o['open_checks_flipped_from_fixed'][k]]
accepted_flips = [k for k in o['open_checks_flipped_from_fixed'] if o['open_checks_flipped_from_fixed'][k]]
X5_defeat = {}
for rid in rejected_flips:
    item = defeat_candidates(rid, o['rev_open'])
    X5_defeat[rid] = item

print(json.dumps({'X1_thresholds': {str(k): v for k, v in thr.items()},
                  'X1_real_overlap': {k: v['overlap'] for k, v in X1_real.items() if v['overlap'] < 4},
                  'X1_forged_overlap': {k: v['overlap'] for k, v in X1_forg.items()},
                  'X6': X6,
                  'X5_accepted_flips_from_fixed': accepted_flips,
                  'X5_rejected_flips_from_fixed': rejected_flips,
                  'X5_defeat_substitute_found': {k: (v is not None) for k, v in X5_defeat.items()},
                  'X5_defeat_items': X5_defeat}, indent=1, ensure_ascii=False))
json.dump({'X1_real': X1_real, 'X1_forg': X1_forg, 'thr': thr, 'X6': X6, 'X5_accepted_flips_from_fixed': accepted_flips,
           'X5_rejected_flips_from_fixed': rejected_flips, 'X5_defeat': X5_defeat},
          open(os.path.join(S, 'out2.json'), 'w'), indent=1, ensure_ascii=False)
