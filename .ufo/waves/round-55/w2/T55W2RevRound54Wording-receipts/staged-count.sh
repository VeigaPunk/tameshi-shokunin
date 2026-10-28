#!/bin/bash
# staged-count reconciliation for the round-54 lesson's Rejects bullet.
set -u
PKG=/home/vgpnk/Projects/shokuknow/merge/tameshi
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
python3 - "$PKG" <<'PY'
import json, os, sys, collections
pkg = sys.argv[1]
d = json.load(open(os.path.join(pkg, 'MERGE-REPORT.json')))
e = d['entries']
print('MERGE-REPORT.json: entries =', len(e), '| accepted(rows) =', d['accepted'], '| refused(rows) =', d['refused'], '| first_id =', d['first_id'])
print('entry kinds =', dict(collections.Counter(x['kind'] for x in e)))
files = []
for r, _, fs in os.walk(os.path.join(pkg, 'knowledge')):
    files += [f for f in fs if f.endswith('.md')]
print('*.md under merge/tameshi/knowledge (recursive) =', len(files))
print('*.md under merge/tameshi (recursive, all) =', sum(1 for r, _, fs in os.walk(pkg) for f in fs if f.endswith('.md')))
names = set(files)
print('round-53 adopted entry on disk (change-aware-resweep-cadence.md):', 'change-aware-resweep-cadence.md' in names)
print('round-54 named-rejected entry on disk (delta-debugging-minimization-contract.md):', 'delta-debugging-minimization-contract.md' in names)
am = [x for x in e if x['kind'] == 'amendment']
print('amendment entries =', len(am), '| any amendment target present among knowledge/ files?',
      any(os.path.basename(x['target']) in names for x in am))
print('folded-into-canonical entries =', sum(1 for x in e if x['kind'] == 'folded-into-canonical'))
print()
print('arithmetic, three candidate denominators:')
print('  track A (entries):        86 entries, round 53 adopted 1 -> 85 unadopted; minus the 1 named in round 54 = 84  <- pre-edit text')
print('  track B (knowledge files): %d .md files; minus the 1 named in round 54 = %d  <- post-edit text' % (len(files), len(files) - 1))
print('  track C (all .md):        %d .md files total (adds MERGE-REPORT.md, SOURCES.append.md, 4 amendment payloads)' %
      sum(1 for r, _, fs in os.walk(pkg) for f in fs if f.endswith('.md')))
PY
echo
echo '--- the two sentences the number has to agree with ---'
git -C "$LANE" show "$C0:corpus/lessons/round-53.md" | sed -n '54p'
git -C "$LANE" show "$C0:SCORECARD.md" | sed -n '2534,2536p'
git -C "$LANE" show "$C0:corpus/lessons/round-54.md" | sed -n '50,52p'
echo
echo '--- ER-R54-9, the correction that moved the number ---'
git -C "$LANE" show "$C0:SCORECARD.md" | sed -n '/ER-R54-9/,/^$/p'
