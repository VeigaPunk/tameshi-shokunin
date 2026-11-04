#!/usr/bin/env python3
"""Per-surface reconnaissance for wave-reconcile future rows (R73 scout T73W1S06).

Read-only: git plumbing only (cat-file/ls-tree/log/rev-parse).
Prints artifact facts + every seat/report-count claim span in each round report.
"""
import hashlib
import json
import os
import re
import subprocess
from collections import Counter

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
NAMED = ['reviewer', 'critic', 'mutation-tester', 'labrat']
ROUNDS = list(range(60, 74))


def git(root, *args):
    p = subprocess.run(['git', '-C', root] + list(args),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None


def blob(root, rev, path):
    return git(root, 'cat-file', 'blob', '%s:%s' % (rev, path))


def listing(root, rev, path):
    out = git(root, 'ls-tree', '-r', '--name-only', rev, '--', path)
    if out is None:
        return None
    return [l for l in out.decode('utf-8', 'replace').splitlines() if l]


def last_commit(root, path):
    out = git(root, 'log', '-1', '--format=%H|%ad|%s', '--date=short', '--', path)
    return out.decode().strip() if out else None


def seat_reports(root, rev, wave_dir):
    files = listing(root, rev, wave_dir)
    if files is None:
        return None, []
    prefix = wave_dir.rstrip('/') + '/'
    top = [p for p in files if p.startswith(prefix)
           and '/' not in p[len(prefix):] and p.endswith('.md')]
    return len(top), sorted(top)


def wave_facts(round_no):
    base = '.ufo/waves/round-%d' % round_no
    files = listing(LANE, 'HEAD', base)
    if files is None:
        return {'present': False}
    top = sorted({p.split('/')[3] for p in files
                  if p.count('/') >= 4 and re.fullmatch(r'w\d+[a-z0-9]*',
                                                        p.split('/')[3])})
    out = {'present': True, 'top_files': [p[len(base) + 1:] for p in files
                                          if p.count('/') == 3],
           'wave_dirs': top, 'waves': []}
    for d in top:
        wd = '%s/%s' % (base, d)
        rpath = '%s/%s-results.json' % (base, d)
        w = {'wave': d, 'dir': wd, 'results_path': rpath}
        rraw = blob(LANE, 'HEAD', rpath)
        if rraw is None:
            w['results'] = None
        else:
            w['results'] = True
            lc = last_commit(LANE, rpath)
            w['results_rev'] = lc.split('|')[0]
            w['results_date'] = lc.split('|')[1]
            w['results_subject'] = lc.split('|')[2]
            w['results_sha256'] = hashlib.sha256(rraw).hexdigest()[:16]
            doc = json.loads(rraw.decode('utf-8'))
            w['seats'] = doc.get('seats')
            w['len_results'] = len(doc.get('results') or [])
            w['agent_multiset'] = dict(Counter(r.get('agent')
                                               for r in doc.get('results') or []))
            w['other_keys'] = sorted(set(doc) - {'lane', 'round', 'wave', 'seats',
                                                 'results'})
            w['settled'] = doc.get('settled')
            w['dead_or_never_spawned'] = doc.get('dead_or_never_spawned')
            w['empty_output_records'] = sum(
                1 for r in doc.get('results') or []
                if r.get('note') or not (r.get('output') or '').strip())
            cnt, names = seat_reports(LANE, w['results_rev'], wd)
            w['seat_reports_at_results_rev'] = cnt
            w['seat_report_names'] = names
            cnt_h, names_h = seat_reports(LANE, 'HEAD', wd)
            w['seat_reports_at_HEAD'] = cnt_h
            w['listing_same_at_HEAD'] = (names == names_h)
            w['results_blob_same_at_HEAD'] = (blob(LANE, 'HEAD', rpath) == rraw)
            w['results_blob_same_at_base'] = (blob(LANE, 'a3dd3574', rpath) == rraw)
            counted = sum(c for a, c in w['agent_multiset'].items()
                          if a in NAMED)
            tot = w['len_results']
            w['attack_named_count'] = counted
            w['attack_pct'] = (100.0 * counted / tot) if tot else 0.0
        # spec candidates: <base>/spec.json, <base>/spec-<d>.json, <base>/<d>-spec.json
        for cand in ('%s/spec.json' % base, '%s/spec-%s.json' % (base, d),
                     '%s/%s-spec.json' % (base, d)):
            sraw = blob(LANE, 'HEAD', cand)
            if sraw is None:
                continue
            lc = last_commit(LANE, cand)
            sdoc = json.loads(sraw.decode('utf-8'))
            items = sdoc.get('items') or []
            w['spec_path'] = cand
            w['spec_rev'] = lc.split('|')[0]
            w['spec_date'] = lc.split('|')[1]
            w['spec_sha256'] = hashlib.sha256(sraw).hexdigest()[:16]
            w['spec_keys'] = sorted(sdoc)
            w['spec_items'] = len(items)
            w['spec_roles'] = dict(Counter(i.get('role') for i in items))
            w['spec_blob_same_at_base'] = (blob(LANE, 'a3dd3574', cand) == sraw)
            break
        out['waves'].append(w)
    return out


CLAIM_PATTERNS = [
    (r'(?<![0-9])\d+\s+seat reports?\b', 'N seat reports'),
    (r'(?<![0-9])\d+\s*/\s*\d+\s+seats?\b', 'N/M seats'),
    (r'(?<![0-9])\d+\s+seats?\b', 'N seats'),
    (r'(?<![0-9])\d+\s+reports?\b', 'N reports'),
    (r'seats?\s*[:=]\s*\d+', 'seats=N'),
    (r'reports?\s*[:=]\s*\d+', 'reports=N'),
    (r'settled\s+\d+\s*/\s*\d+', 'settled N/M'),
    (r'\b\d+\s+settled\b', 'N settled'),
    (r'\b\d+\s+of\s+\d+\s+seats?\b', 'N of M seats'),
    (r'\b\d+\s+(?:cap-cancelled|returned|reports?)\b', 'N returned/reports'),
]


def claims(text):
    hits = []
    for pat, label in CLAIM_PATTERNS:
        for m in re.finditer(pat, text):
            hits.append((m.start(), m.end(), m.group(0), label))
    seen = set()
    out = []
    for h in sorted(hits):
        if (h[0], h[2]) in seen:
            continue
        seen.add((h[0], h[2]))
        out.append(h)
    return out


def main():
    facts = []
    for r in ROUNDS:
        rep_path = '.ufo/reports/round-%d/tameshi.md' % r
        lc = last_commit(FLEET, rep_path)
        rec = {'round': r, 'report_path': rep_path}
        if lc:
            rev = lc.split('|')[0]
            raw = blob(FLEET, rev, rep_path)
            rec.update(rev=rev, date=lc.split('|')[1], subject=lc.split('|')[2][:60],
                       bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()[:16])
            rec['claims'] = claims(raw.decode('utf-8'))
            rec['text'] = raw.decode('utf-8')
        else:
            rec['absent'] = True
        rec['wave'] = wave_facts(r)
        facts.append(rec)

    print('=== ARTIFACT FACTS ===')
    for f in facts:
        print('# round-%d' % f['round'])
        if f.get('absent'):
            print('  report: ABSENT')
        else:
            print('  report=%s rev=%s date=%s bytes=%d sha=%s'
                  % (f['report_path'], f['rev'], f['date'], f['bytes'],
                     f['sha256']))
        w = f['wave']
        if not w['present']:
            print('  wave: NO .ufo/waves/round-%d AT HEAD' % f['round'])
        else:
            print('  wave top-files=%s dirs=%s' % (w['top_files'], w['wave_dirs']))
            for x in w['waves']:
                if x.get('results') is None:
                    print('    wave=%s results=%s ABSENT'
                          % (x['wave'], x['results_path']))
                else:
                    print('    wave=%s results=%s rev=%s(%s) sha=%s'
                          % (x['wave'], x['results_path'], x['results_rev'],
                             x['results_date'], x['results_sha256']))
                    print('      seats=%r len(results)=%d extra_keys=%s'
                          % (x['seats'], x['len_results'], x['other_keys']))
                    print('      agent_multiset=%s'
                          % json.dumps(x['agent_multiset'], sort_keys=True))
                    print('      settled=%r dead_or_never_spawned=%r note_or_empty=%d'
                          % (x['settled'], x['dead_or_never_spawned'],
                             x['empty_output_records']))
                    print('      seat_reports@rev=%d (HEAD=%d same_listing=%s) names=%s'
                          % (x['seat_reports_at_results_rev'],
                             x['seat_reports_at_HEAD'],
                             x['listing_same_at_HEAD'], x['seat_report_names']))
                    print('      results_blob same@HEAD=%s same@base=%s'
                          % (x['results_blob_same_at_HEAD'],
                             x['results_blob_same_at_base']))
                    print('      attack named=%s counted=%d/%d=%.1f%%'
                          % (NAMED, x['attack_named_count'], x['len_results'],
                             x['attack_pct']))
                if 'spec_path' in x:
                    print('    spec=%s rev=%s(%s) sha=%s items=%d'
                          % (x['spec_path'], x['spec_rev'], x['spec_date'],
                             x['spec_sha256'], x['spec_items']))
                    print('      spec_roles=%s same@base=%s'
                          % (json.dumps(x['spec_roles'], sort_keys=True),
                             x['spec_blob_same_at_base']))
                else:
                    print('    spec: ABSENT for wave %s' % x['wave'])
        print()

    print('=== CLAIM SPANS (byte offsets in the report blob) ===')
    for f in facts:
        print('--- round-%d %s' % (f['round'], f.get('rev', 'report-absent')))
        for s, e, tok, label in f.get('claims', []):
            ctx = f['text'][max(0, s - 60):e + 60].replace('\r', '').replace('\n', '\\n')
            print('  [%d:%d] %-22r %-18s %r' % (s, e, tok, label, ctx))
        print()

    for f in facts:
        f.pop('text', None)
        f['claims'] = f.get('claims', [])
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(facts, open(os.path.join(here, 'facts.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
