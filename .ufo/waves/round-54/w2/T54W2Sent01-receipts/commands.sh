#!/bin/bash
# T54W2Sent01 fixture: forge a reader report; frozen C1 counter at a scratch clone.
# Host lane is read-only throughout; every git mutation names a clone under $S.
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r54/T54W2Sent01
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
COUNTER=$LANE/.ufo/evidence/round-54/c1/measure.py     # sha256 d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812
C1=99c3bc88d704566197783f66b211ee0a830e0330
CL=$S/clone
[ -d "$CL" ] || git clone --shared --quiet "$LANE" "$CL"
git -C "$CL" checkout --detach --quiet "$C1"
test "$(git -C "$CL" rev-parse --show-toplevel)" = "$CL" || exit 9

# 1. 23 clean reader reports at C1 (heading/cand/sha from reader-section.py) + binder
mkdir -p "$CL/.ufo/waves/round-54/w1"
python3 - "$CL" "$C1" "$LANE" <<'PY'
import json,subprocess,sys
cl,c1,lane=sys.argv[1:4]
heads=sorted(set(json.load(open(lane+'/.ufo/evidence/round-54/c1/lost-headings-at-c0.json')))
             |set(json.load(open(lane+'/.ufo/evidence/round-54/c1/lost-headings-at-base.json'))))
for i,h in enumerate(heads,1):
    d=json.loads(subprocess.run(['python3',lane+'/.ufo/waves/round-54/reader-section.py',lane,c1,h],
                                capture_output=True,text=True,check=True).stdout)
    p='%s/.ufo/waves/round-54/w1/T54W2Read%02d.json'%(cl,i)
    json.dump({'heading':h,'cand':c1,'section_sha256':d['section_sha256'],'findings':[]},open(p,'w'))
    open(p[:-5]+'.md','w').write('# %s\n'%h)
PY
cp "$LANE/.ufo/evidence/round-54/c1/lost-headings-at-c0.json" "$CL/.ufo/evidence/round-54/c1/"
OUT="$CL/.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704"; mkdir -p "$OUT"
python3 "$LANE/.ufo/evidence/round-54/integrate/binder.py" "$CL" "$C1" "$C1" "$OUT"   # 23 REKEY, 0 SKIP
git -C "$CL" add -A && git -C "$CL" -c user.email=f@invalid -c user.name=f commit -qm "fixture: binder pass"
# ledger-only state: the current counter refuses it (F1)
mkdir -p "$S/workX"; python3 "$COUNTER" --lane "$CL" --rev HEAD --work "$S/workX" --explain

# 2. hand-bind: drop the self-referential round-21 ledger input from the Mutation-sweep entry+trace
python3 - "$CL" <<'PY'
import json,sys
cl=sys.argv[1]; led='.ufo/evidence/round-21/coldread/ledger.json'
pref='.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/'
p=cl+'/'+led; d=json.load(open(p))
for e in d['entries']:
    if e.get('heading','').startswith('## Mutation-sweep') and any(t.startswith(pref) for t in e.get('traces') or []):
        e['inputs'].pop(led,None)
        e.get('external_inputs',{}).pop('tameshi@99c3bc88d704:'+led,None)
open(p,'w').write(json.dumps(d,indent=1,ensure_ascii=False)+'\n')
t=cl+'/'+pref+'traces/section-04.json'; tr=json.load(open(t)); tr['inputs'].pop(led,None)
open(t,'w').write(json.dumps(tr,indent=1,ensure_ascii=False)+'\n')
PY
git -C "$CL" add -A && git -C "$CL" -c user.email=f@invalid -c user.name=f commit -qm "fixture: hand-bound entry credits"
mkdir -p "$S/workA"; python3 "$COUNTER" --lane "$CL" --rev HEAD --work "$S/workA" --explain   # PASS=true

# 3. forge: guessed sha, correct heading/cand; plant in the scanned wave dir; counter stays false
python3 - "$LANE/.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json" <<'PY'
import hashlib,json,sys
json.dump({'heading':'## Standing rules','cand':'99c3bc88d704566197783f66b211ee0a830e0330',
           'section_sha256':hashlib.sha256(b'forged-r54-sent01: never read the section bytes').hexdigest(),
           'findings':[]},open(sys.argv[1],'w'))
PY
cp "$LANE/.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json" "$CL/.ufo/waves/round-54/w2/T54W2Read07.json"
rm -f "$CL/.ufo/waves/round-54/w1/T54W2Read07.json"
git -C "$CL" add -A && git -C "$CL" -c user.email=f@invalid -c user.name=f commit -qm "fixture: forged report under w2"
mkdir -p "$S/workE"; python3 "$COUNTER" --lane "$CL" --rev HEAD --work "$S/workE" --explain   # readers=6/7 PASS=false
# control: genuine bytes under the same w2 path -> readers=7/7 PASS=true
cp "$S/genuine-read07.json" "$CL/.ufo/waves/round-54/w2/T54W2Read07.json"
git -C "$CL" add -A && git -C "$CL" -c user.email=f@invalid -c user.name=f commit -qm "fixture: genuine bytes under w2"
mkdir -p "$S/workF"; python3 "$COUNTER" --lane "$CL" --rev HEAD --work "$S/workF" --explain   # PASS=true
