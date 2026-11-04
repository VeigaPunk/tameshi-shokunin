#!/usr/bin/env bash
# Reproducible dead-seat fixture for the wave-reconcile row kinds.
# Creates a throwaway git repo (git init + one commit, all under $BASE), runs
# the committed reconciler against it, and prints the row lines.
#
#   bash deadseat-fixture.sh [base-dir]
#
# Wave A: 12 dispatched spawn seats, 12 result records, ONE dead (T07: output
#   null + note), 11 committed seat .md files, report claims "12 seats, 11
#   reports", attack floor 30.
# Wave B: the same dispatch (12 tasks), but a hand-trimmed results artifact
#   (11 records, seats=11) and an 11-role spec; report claims "11 seats, 11
#   reports".
set -euo pipefail
BASE=${1:-/fast/scratch/hyaku/tameshi-r73/T73W1S12}
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
mkdir -p "$BASE"
D=$(mktemp -d "$BASE/fx.XXXXXX")
git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "GUARD-FAIL: $D" >&2; exit 1; }

python3 -I -X utf8 - "$D" <<'PY'
import json, os, sys
D = sys.argv[1]
roles = ['executor','executor','executor','scribe','scribe','scout',
         'reviewer','critic','mutation-tester','sentinel','revenger','reviewer']
names = ['T%02d' % i for i in range(1, 13)]
os.makedirs(os.path.join(D, 'waveA')); os.makedirs(os.path.join(D, 'waveB'))
res = {'lane':'fx','round':1,'wave':'A','seats':12,'results':[]}
for n, r in zip(names, roles):
    if n == 'T07':
        res['results'].append({'name':n,'agent':r,'output':None,
            'note':'seat died before delivering output; no report file'})
    else:
        res['results'].append({'name':n,'agent':r,'output':'SETTLED %s' % n,'note':None})
json.dump(res, open(os.path.join(D,'waveA','results.json'),'w'), indent=1)
json.dump({'wave':'A','items':[{'name':n,'role':r} for n,r in zip(names,roles)]},
          open(os.path.join(D,'waveA','spec.json'),'w'), indent=1)
for n in names:
    if n != 'T07':
        open(os.path.join(D,'waveA',n+'.md'),'w').write('# %s\n' % n)
open(os.path.join(D,'report.md'),'w').write(
    '- **The wave**: 12 seats, 11 reports; one seat died.\n')
plan = ('- Wave A: 12 seats \u2014 3 executor, 2 scribe, 1 scout, 2 reviewer,\n'
        '  1 critic, 1 mutation-tester, 1 sentinel, 1 revenger.')
open(os.path.join(D,'plan.md'),'w').write(plan + '\n')
tasks = [{'name':n,'agent':r,'task':'fixture'} for n,r in zip(names,roles)]
json.dump({'schema':'ufo-swarm-wave-dispatch-v1','wave':'A',
           'counts':{'spawn':12,'resume':0,'total':12},
           'taskCall':{'context':'x','tasks':tasks},'resumeSends':[]},
          open(os.path.join(D,'dispatch.json'),'w'), indent=1)
rolesB = roles[:11]; namesB = names[:11]
json.dump({'lane':'fx','round':1,'wave':'B','seats':11,
           'results':[{'name':n,'agent':r,'output':'ok','note':None}
                      for n,r in zip(namesB,rolesB)]},
          open(os.path.join(D,'waveB','results.json'),'w'), indent=1)
json.dump({'wave':'B','items':[{'name':n,'role':r} for n,r in zip(namesB,rolesB)]},
          open(os.path.join(D,'waveB','spec.json'),'w'), indent=1)
for n in namesB:
    open(os.path.join(D,'waveB',n+'.md'),'w').write('# %s\n' % n)
open(os.path.join(D,'reportB.md'),'w').write(
    '- **The wave**: 11 seats, 11 reports.\n')
PY

git -C "$D" add -A
git -C "$D" -c user.email=fx@example.invalid -c user.name=fx commit -qm 'fixture'
REV=$(git -C "$D" rev-parse HEAD)
echo "FIXTURE_REV=$REV"
echo "FIXTURE_DIR=$D"

python3 -I -X utf8 - "$D" "$REV" <<'PY'
import json, sys
D, REV = sys.argv[1], sys.argv[2]
def wave(d): return {'dir':d,'results':d+'/results.json','rev':REV}
spanA = ('- Wave A: 12 seats \u2014 3 executor, 2 scribe, 1 scout, 2 reviewer,\n'
         '  1 critic, 1 mutation-tester, 1 sentinel, 1 revenger.')
rolesA = {'executor':3,'scribe':2,'scout':1,'reviewer':2,'critic':1,
          'mutation-tester':1,'sentinel':1,'revenger':1}
rows = [
 {'id':'A-seats','kind':'seats','expect':'meet',
  'record':{'path':'report.md','rev':REV,'root':'lane','span':'12 seats, 11 reports','printed':12},
  'wave':wave('waveA')},
 {'id':'A-seatreports-11','kind':'seat_reports','expect':'meet',
  'record':{'path':'report.md','rev':REV,'root':'lane','span':'12 seats, 11 reports','printed':11},
  'wave':wave('waveA')},
 {'id':'A-seatreports-12','kind':'seat_reports','expect':'drift',
  'record':{'path':'report.md','rev':REV,'root':'lane','span':'12 seats, 11 reports','printed':12},
  'wave':wave('waveA')},
 {'id':'A-roles-spec','kind':'roles','expect':'meet',
  'record':{'path':'waveA/spec.json','rev':REV,'root':'lane','span':'"T01"'},
  'wave':wave('waveA'),
  'declaration':{'form':'spec-items','path':'waveA/spec.json','rev':REV,'root':'lane'}},
 {'id':'A-roles-plan','kind':'roles','expect':'meet',
  'record':{'path':'plan.md','rev':REV,'root':'lane','span':spanA},
  'wave':wave('waveA'),
  'declaration':{'form':'text-tokens','path':'plan.md','rev':REV,'root':'lane','span':spanA,'roles':rolesA}},
 {'id':'A-attack-floor30','kind':'attack_share','expect':'meet',
  'record':{'path':'report.md','rev':REV,'root':'lane','span':'12 seats, 11 reports'},
  'wave':wave('waveA'),'named':['reviewer','critic','mutation-tester'],'floor_pct':30},
 {'id':'B-seats','kind':'seats','expect':'meet',
  'record':{'path':'reportB.md','rev':REV,'root':'lane','span':'11 seats, 11 reports','printed':11},
  'wave':wave('waveB')},
 {'id':'B-roles-spec','kind':'roles','expect':'meet',
  'record':{'path':'waveB/spec.json','rev':REV,'root':'lane','span':'"T01"'},
  'wave':wave('waveB'),
  'declaration':{'form':'spec-items','path':'waveB/spec.json','rev':REV,'root':'lane'}},
 {'id':'B-attack-floor25','kind':'attack_share','expect':'meet',
  'record':{'path':'reportB.md','rev':REV,'root':'lane','span':'11 seats, 11 reports'},
  'wave':wave('waveB'),'named':['reviewer','critic','mutation-tester'],'floor_pct':25},
]
json.dump({'schema':'tameshi-wave-reconcile-v1','rows':rows},
          open(D+'/manifest.json','w'), indent=1)
PY

cd "$LANE"
python3 -I -X utf8 tools/wave-reconcile.py --repo "$D" --manifest "$D/manifest.json"
