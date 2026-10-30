#!/usr/bin/env python3
"""Amendment 1 (L1): install the wave-1 blind panel, set PANEL_SHA256, update freeze+contract.
Run AFTER wave-1 settles and BEFORE any ledger scoring/deciding invocation.
Usage: python3 amend1-panel.py"""
import hashlib, json, os, re, sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
W1 = LANE + '/.ufo/waves/round-58/w1'
E = LANE + '/.ufo/evidence/round-58'
BASE = '2a32aa8228d5f86a85c81a923a3148bf792a9538'

# 1. collect panel seats
seats = sorted(f for f in os.listdir(W1) if re.match(r'T58W1Panel\d+\.json$', f))
if not seats:
    sys.exit('no panel seat files')
verdicts, detail, files = {}, {}, {}
for f in seats:
    blob = open(os.path.join(W1, f), 'rb').read()
    d = json.loads(blob)
    seat = d.get('seat') or f[:-5]
    files[seat] = hashlib.sha256(blob).hexdigest()
    for iid, v in d.get('verdicts', {}).items():
        if iid in verdicts:
            sys.exit('duplicate id across panel seats: %s' % iid)
        verdicts[iid] = v.get('verdict')
        detail[iid] = {'seat': seat, 'commit': v.get('commit') or ''}
ids = sorted(verdicts)
if len(ids) != 51:
    sys.exit('panel covers %d ids, expected 51' % len(ids))

# 2. panel.json (digest over its own new bytes)
panel = {'schema': 'tameshi-c1-panel-v1', 'base': BASE, 'verdicts': verdicts, 'detail': detail, 'files': files,
         'note': 'wave-1 blind panel (T58W1Panel01..11); provenance checked by counter arm A9 against .ufo/waves/round-58/w1/<seat>.json + w1-results.json'}
pbytes = (json.dumps(panel, indent=1, ensure_ascii=False) + '\n').encode('utf-8')
pin = hashlib.sha256(pbytes).hexdigest()
open(os.path.join(E, 'c1/panel.json'), 'wb').write(pbytes)

# 3. measure.py PANEL_SHA256
mp = os.path.join(E, 'c1/measure.py')
s = open(mp, encoding='utf-8').read()
new, n = re.subn(r"PANEL_SHA256 = '[^']*'", "PANEL_SHA256 = '%s'" % pin, s, count=1)
if n != 1:
    sys.exit('PANEL_SHA256 line not found')
open(mp, 'w', encoding='utf-8').write(new)

# 4. contract amendments mirror
amend = [{'n': 1,
          'what': 'set PANEL_SHA256 to the wave-1 blind panel digest (%s…) and installed the panel from the '
                  'T58W1Panel01..11 seat files (verdicts/detail/files); predicate, target, counters and arms '
                  'unchanged; landed before any scoring or deciding invocation' % pin[:12]}]
cpath = os.path.join(E, 'contract.json')
c = json.load(open(cpath))
c['amendments'] = amend
open(cpath, 'w').write(json.dumps(c, indent=1, ensure_ascii=False) + '\n')

# 5. freeze.json: update digests for the changed frozen files + amendments
fpath = os.path.join(E, 'freeze.json')
fr = json.load(open(fpath))
fr['amendments'] = amend
for rel, path in (('c1/panel.json', os.path.join(E, 'c1/panel.json')), ('c1/measure.py', mp)):
    fr['files'][rel] = hashlib.sha256(open(path, 'rb').read()).hexdigest()
open(fpath, 'w').write(json.dumps(fr, indent=1) + '\n')
print('AMEND1 panel ids=%d pin=%s seats=%d' % (len(ids), pin[:12], len(seats)))
print('from collections import Counter; v=%r; print({k: v2 for k, v2 in [("fixed", list(v.values()).count("fixed")), ("open", list(v.values()).count("open")), ("declined", list(v.values()).count("declined"))]})' % verdicts)
