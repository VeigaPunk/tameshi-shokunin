#!/bin/bash
# C2 counterexample battery: the real SCORECARD.md + tools/capability-census.json
# + tools/selfstate-freshness.json committed into a fixture repo, then the
# census's binding is attacked one variable at a time. Every command echoed.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=55d5a5c6002a048337cc511e1712df87b961d364
D=$1
rm -rf "$D"; mkdir -p "$D"; cd "$D" || exit 1
git init -q .
test "$(git rev-parse --show-toplevel)" = "$D" || { echo "TOPLEVEL_MISMATCH"; exit 1; }
git -C "$LANE" show $REV:SCORECARD.md > SCORECARD.md
mkdir -p tools
cp "$LANE/tools/capability-census.json" "$LANE/tools/selfstate-freshness.json" \
   "$LANE/tools/capability-census.py" tools/
python3 - <<'EOF'
import json, os
m=json.load(open('tools/capability-census.json'))
for r in m['rows']:
    if r['disposition']=='historical':
        p=r['receipt']['path']
        os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
        if not os.path.isdir(p): open(p,'w').write('fixture receipt\n')
EOF
git add -A >/dev/null && git -c user.name=f -c user.email=f@invalid \
  -c commit.gpgsign=false commit -qm fixture-r0
R0=$(git rev-parse HEAD)
python3 - "$R0" <<'EOF'
import json,sys
m=json.load(open('tools/capability-census.json'))
for r in m['rows']:
    if r['disposition']=='historical': r['receipt']['rev']=sys.argv[1]
json.dump(m,open('tools/capability-census.json','w'),indent=1)
EOF
git add -A >/dev/null && git -c user.name=f -c user.email=f@invalid \
  -c commit.gpgsign=false commit -qm fixture-r1
R1=$(git rev-parse HEAD)
cp tools/capability-census.json "$D/../manifest-R1.json"

echo "### F0 baseline: real doc + real manifest + real selfstate at R1"
echo "\$ python3 -I -X utf8 tools/capability-census.py --repo . --rev $R1"
python3 -I -X utf8 tools/capability-census.py --repo . --rev "$R1" | tail -1
echo "exit=${PIPESTATUS[0]}"

echo
echo "### F1 historical pins resolve to DIRECTORIES the row does not describe"
python3 - <<'EOF'
import json
p='tools/capability-census.json'; m=json.load(open(p))
for r in m['rows']:
    if r['capability']=='six-leg regression ledger': r['receipt']['path']='tools/'
    if r['capability']=='sources-registry': r['receipt']['path']='.ufo/evidence/kaika-round-1'
json.dump(m,open(p,'w'),indent=1)
EOF
echo "\$ python3 -I -X utf8 tools/capability-census.py --repo . --rev $R1   # uncommitted manifest"
python3 -I -X utf8 tools/capability-census.py --repo . --rev "$R1" \
  | grep -E "six-leg regression ledger|sources-registry|CAP_CENSUS"
echo "exit=${PIPESTATUS[0]}"

echo
echo "### F2 a committed live row whose claimed figure is FALSE still binds"
cp ../manifest-R1.json tools/capability-census.json
python3 - <<'EOF'
s=open('SCORECARD.md').read()
assert 'REGISTRY_BIND_SELFTEST: 13/13 pass' in s
open('SCORECARD.md','w').write(
    s.replace('REGISTRY_BIND_SELFTEST: 13/13 pass','REGISTRY_BIND_SELFTEST: 0/13 pass'))
EOF
git add -A >/dev/null && git -c user.name=f -c user.email=f@invalid \
  -c commit.gpgsign=false commit -qm fixture-r2-false-figure
R2=$(git rev-parse HEAD)
echo "committed false figure count at R2: $(git show "$R2:SCORECARD.md" | grep -c 'REGISTRY_BIND_SELFTEST: 0/13 pass')"
echo "\$ python3 -I -X utf8 tools/capability-census.py --repo . --rev $R2"
python3 -I -X utf8 tools/capability-census.py --repo . --rev "$R2" \
  | grep -E "registry-home figure binding|CAP_CENSUS"
echo "exit=${PIPESTATUS[0]}"

echo
echo "### F3 an UNCOMMITTED selfstate row binds a live row at a rev that lacks it"
python3 - <<'EOF'
import json
p='tools/selfstate-freshness.json'; d=json.load(open(p))
d['rows'].append({'id':'forged-live','mode':'capability',
                  'capability':'standing-pin audit','expect':'match'})
json.dump(d,open(p,'w'),indent=1)
m=json.load(open('tools/capability-census.json'))
for r in m['rows']:
    if r['capability']=='standing-pin audit': r['selfstate_row']='forged-live'
json.dump(m,open('tools/capability-census.json','w'),indent=1)
EOF
echo "committed selfstate at R1 carries forged-live: $(git show "$R1:tools/selfstate-freshness.json" | grep -c forged-live)"
echo "\$ python3 -I -X utf8 tools/capability-census.py --repo . --rev $R1"
python3 -I -X utf8 tools/capability-census.py --repo . --rev "$R1" \
  | grep -E "standing-pin audit|CAP_CENSUS"
echo "exit=${PIPESTATUS[0]}"

echo
echo "### F4 a live row bound to a selfstate row DECLARED expect=stale still binds"
python3 - <<'EOF'
import json
p='tools/selfstate-freshness.json'; d=json.load(open(p))
d['rows'].append({'id':'declared-stale-live','mode':'capability',
                  'capability':'standing-pin audit','expect':'stale'})
json.dump(d,open(p,'w'),indent=1)
m=json.load(open('tools/capability-census.json'))
for r in m['rows']:
    if r['capability']=='standing-pin audit': r['selfstate_row']='declared-stale-live'
json.dump(m,open('tools/capability-census.json','w'),indent=1)
EOF
echo "\$ python3 -I -X utf8 tools/capability-census.py --repo . --rev $R1"
python3 -I -X utf8 tools/capability-census.py --repo . --rev "$R1" \
  | grep -E "standing-pin audit|CAP_CENSUS"
echo "exit=${PIPESTATUS[0]}"

echo
echo "### F5 negative control: de-citing a historical row IS refused"
cp ../manifest-R1.json tools/capability-census.json
python3 - <<'EOF'
import json
p='tools/selfstate-freshness.json'; d=json.load(open(p))
d['rows']=[r for r in d['rows'] if r.get('id') not in ('forged-live','declared-stale-live')]
json.dump(d,open(p,'w'),indent=1)
s=open('SCORECARD.md').read()
open('SCORECARD.md','w').write(
    s.replace('`bash tools/mutate-and-run.sh --regression`','bash tools/mutate-and-run.sh --regression'))
EOF
git add -A >/dev/null && git -c user.name=f -c user.email=f@invalid \
  -c commit.gpgsign=false commit -qm fixture-r3-decited
R3=$(git rev-parse HEAD)
echo "\$ python3 -I -X utf8 tools/capability-census.py --repo . --rev $R3"
python3 -I -X utf8 tools/capability-census.py --repo . --rev "$R3" \
  | grep -E "six-leg regression ledger|CAP_CENSUS"
echo "exit=${PIPESTATUS[0]}"
