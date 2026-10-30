#!/usr/bin/env python3
"""R55.3 sweep: provenance of the adjudicated row (commit, freshness, tie) + the monitor measurement."""
import hashlib
import json
import re
import subprocess

CLONE = '/fast/scratch/hyaku/tameshi-r57/TameshiR57x'  # placeholder, overwritten below
CLONE = '/fast/scratch/hyaku/tameshi-r57/T57W3RowR551xR553/clone'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
C0B = 'adf87899c70d616140a81185a8f9acbbdfb30392'
MASTER = '2c51affd37e15cd7cd258d76ba0f5f73ff235924'
ROUTED = 'fa48c06c3669355fd80e8722eb733c1d6dfdd2f8'
COMMIT = 'c1dd23b3f83f5dff676c4a4482498e87345375ef'
TRACE = '.ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/traces/section-18.json'
ACK_WORDS = ('planned', 'carried', 'still open', 'not worked', 'stay open', 'stays open', 'remain open',
             'remains open', 'routed to round', 'not fixed', 'unfixed', 'not landed')
defects = json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/defects.json'))
D = {d['id']: d for d in defects['defects']}


def git(*args):
    p = subprocess.run(['git', '-C', CLONE] + list(args), capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def show(rev, path):
    rc, out, _ = git('show', '%s:%s' % (rev, path))
    return out if rc == 0 else None


print('### R55.3 sweep (scratch clone %s)' % CLONE)
print('\n## 1. the item and its keys (frozen .ufo/evidence/round-57/c1/defects.json)')
print('keys:', D['R55.3']['keys'])
print('text:', D['R55.3']['text'])
print('routed_at:', D['R55.3']['routed_at'])

print('\n## 2. the blind panel verdict and its commit (lane .ufo/evidence/round-57/c1/panel.json)')
panel = json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/panel.json'))
print('verdicts[R55.3] =', panel['verdicts'].get('R55.3'))
print('detail[R55.3]   =', json.dumps(panel.get('detail', {}).get('R55.3')))
print('panel sha256    =', hashlib.sha256(open(
    '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/panel.json', 'rb').read()).hexdigest())

print('\n## 3. commit provenance of the row\'s commit %s' % COMMIT)
rc, out, _ = git('log', '-1', '--format=%H%n%s%n%b', COMMIT)
print('commit message:\n' + out.rstrip())
print('is ancestor of BASE  :', git('merge-base', '--is-ancestor', COMMIT, BASE)[0] == 0)
print('is ancestor of C0b   :', git('merge-base', '--is-ancestor', COMMIT, C0B)[0] == 0)
print('is ancestor of routed:', git('merge-base', '--is-ancestor', COMMIT, ROUTED)[0] == 0)
rc, out, _ = git('diff-tree', '--no-commit-id', '--name-only', '-r', '--root', '-m', COMMIT)
touched = [x for x in out.split('\n') if x]
print('touches the evidence path:', TRACE in touched)
print('touched files (%d):' % len(touched))
for t in touched:
    print('   ', t)

print('\n## 4. freshness: the excerpted file is new in that commit')
for rev in (ROUTED, COMMIT + '^', BASE, C0B, MASTER):
    print('%-42s %s' % (rev, 'PRESENT' if show(rev, TRACE) else 'ABSENT'))

print('\n## 5. the excerpt, verbatim and normalised, with the key and ACK scan')
lines = show(MASTER, TRACE).split('\n')
span = lines[16:19]
norm = ' '.join('\n'.join(span).split())
print('cited lines 17-19:')
for l in span:
    print('   |' + l)
print('normalised:', repr(norm))
for k in D['R55.3']['keys']:
    hit = re.search(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', norm, re.IGNORECASE)
    print('key %-10r whole-token hit: %s' % (k, bool(hit)))
print('ACK words in the cited span:', [w for w in ACK_WORDS if w in norm.lower()] or 'none')
print('excerpt length:', len(norm), '(counter admits 15..400)')

print('\n## 6. tie arm: can any commit tie without the panel pin?')
rc, out, _ = git('log', '--all', '--format=%H %s')
hits = [l for l in out.split('\n') if re.search(r'(?<![\w.])R55\.3(?!\d)', l)]
print('commits whose message names R55.3:', len(hits), hits[:5])
item_text = D['R55.3']['text']
rc, out, _ = git('ls-tree', '-r', '--name-only', MASTER)
names = [x for x in out.split('\n') if x]
hits = [p for p in names if p.rsplit('/', 1)[-1] and p.rsplit('/', 1)[-1] in item_text]
print('tracked files whose basename occurs in the item text:', len(hits), hits[:5])
print('=> the only tie arm left is amendment 2\'s panel_tie (the panel named this commit)')

print('\n## 7. the frozen round-21 monitor, measured by this seat')
for tag, f in (('base 5e35699', 'monitor-base.json'), ('C0b  adf87899', 'monitor-c0b.json')):
    p = '/fast/scratch/hyaku/tameshi-r57/T57W3RowR551xR553/' + f
    try:
        d = json.load(open(p))
    except Exception as exc:                                   # pragma: no cover
        print(tag, 'unavailable:', exc)
        continue
    cr = d.get('coldread', {})
    print('%-12s calibration_restraint_score=%s box3_full_page=%s sections_covered=%s credited=%s' % (
        tag, d.get('calibration_restraint_score'), cr.get('box3_full_page'),
        cr.get('sections_covered'), cr.get('sections_credited')))
