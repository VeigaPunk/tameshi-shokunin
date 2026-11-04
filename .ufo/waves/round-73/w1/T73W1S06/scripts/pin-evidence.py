#!/usr/bin/env python3
"""Pinned-rev re-derivation of the recon table numbers (read-only git plumbing)."""
import hashlib
import json
import subprocess
from collections import Counter

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
NAMED = ['reviewer', 'critic', 'mutation-tester', 'labrat']
PINS = {
    60: {'results_rev': 'e13e0324e048377d7ca5d296294f6f4089240aa0',
         'report_rev': '9f39c5fcb9400667ffb2846dd2183ef9cd5dfe82',
         'wave_dir': '.ufo/waves/round-60/w1',
         'results': '.ufo/waves/round-60/w1-results.json',
         'spec': '.ufo/waves/round-60/spec-w1.json'},
    72: {'results_rev': 'a3dd35742eee608d1205843dacebc461b4242b9e',
         'report_rev': '3664a6d30051410c3d2bb8c32926d13e284a5118',
         'wave_dir': '.ufo/waves/round-72/w1',
         'results': '.ufo/waves/round-72/w1-results.json',
         'spec': '.ufo/waves/round-72/w1-spec.json'},
    73: {'results_rev': '17cd19396b36d4c15f1bce1bbdb7c42346f1df76',
         'report_rev': None,
         'wave_dir': '.ufo/waves/round-73/w1',
         'results': '.ufo/waves/round-73/w1-results.json',
         'spec': '.ufo/waves/round-73/w1-spec.json'},
}


def g(root, *a):
    p = subprocess.run(['git', '-C', root] + list(a),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None


def blob(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'cat-file', 'blob', '%s:%s' % (rev, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout if p.returncode == 0 else None


def listing(root, rev, path):
    out = g(root, 'ls-tree', '-r', '--name-only', rev, '--', path)
    return [l for l in out.decode().splitlines() if l] if out is not None else None


for r, pin in PINS.items():
    print('## round-%d (lane pin %s)' % (r, pin['results_rev'][:12]))
    raw = blob(LANE, pin['results_rev'], pin['results'])
    if raw is None:
        print('  results: ABSENT at pin -> row setup error exit 2')
    else:
        doc = json.loads(raw.decode())
        ms = Counter(x['agent'] for x in doc['results'])
        files = listing(LANE, pin['results_rev'], pin['wave_dir'])
        pre = pin['wave_dir'] + '/'
        md = [p for p in files if p.startswith(pre)
              and '/' not in p[len(pre):] and p.endswith('.md')]
        atk = sum(v for k, v in ms.items() if k in NAMED)
        print('  results sha256=%s' % hashlib.sha256(raw).hexdigest()[:16])
        print('  seats=%d len(results)=%d agent_multiset=%s'
              % (doc['seats'], len(doc['results']),
                 json.dumps(dict(sorted(ms.items())))))
        print('  committed top-level seat reports=%d %s'
              % (len(md), [p.rsplit('/', 1)[-1] for p in sorted(md)]))
        print('  attack named-set=%s counted=%d/%d=%.1f%%'
              % (NAMED, atk, len(doc['results']),
                 100.0 * atk / len(doc['results'])))
        print('  results blob identical at lane HEAD=%s'
              % (blob(LANE, 'HEAD', pin['results']) == raw))
    sraw = blob(LANE, pin['results_rev'], pin['spec'])
    if sraw is None:
        print('  spec: ABSENT at pin')
    else:
        sdoc = json.loads(sraw.decode())
        items = sdoc.get('items') or []
        roles = Counter(i.get('role') for i in items)
        print('  spec %s sha256=%s items=%d roles=%s'
              % (pin['spec'], hashlib.sha256(sraw).hexdigest()[:16], len(items),
                 json.dumps(dict(sorted(roles.items())))))
    if pin['report_rev']:
        rraw = blob(FLEET, pin['report_rev'], '.ufo/reports/round-%d/tameshi.md' % r)
        print('  fleet report rev=%s bytes=%d sha256=%s'
              % (pin['report_rev'][:12], len(rraw),
                 hashlib.sha256(rraw).hexdigest()[:16]))
    else:
        print('  fleet report: ABSENT (no .ufo/reports/round-%d/tameshi.md)' % r)
    print()

print('lane HEAD now =', g(LANE, 'rev-parse', 'HEAD').decode().strip())
print('fleet HEAD now =', g(FLEET, 'rev-parse', 'HEAD').decode().strip())
