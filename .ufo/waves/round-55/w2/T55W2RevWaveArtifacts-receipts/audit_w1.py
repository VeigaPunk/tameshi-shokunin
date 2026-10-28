import json,os,subprocess
C0='9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'; P='.ufo/waves/round-55/w1/'
os.chdir('/fast/scratch/hyaku/tameshi-r55/T55W2RevWaveArtifacts/lane')
disp=json.loads(subprocess.check_output(['git','show',C0+':.ufo/waves/round-55/w1-dispatch.json']))
names=list(disp['registry']['members'])
files=subprocess.check_output(['git','ls-tree','-r','--name-only',C0,'--',P]).decode().split()
root=[f[len(P):] for f in files if f.count('/')==4]
mds=[r for r in root if r.endswith('.md')]; jss=[r for r in root if r.endswith('.json')]
recs={f.split('/')[4][:-len('-receipts')] for f in files if f.startswith(P) and f.count('/')>4 and f.split('/')[4].endswith('-receipts')}
seatmd={m[:-3] for m in mds}&set(names); seatjs={j[:-5] for j in jss}&set(names)
print('dispatch counts          :',disp['counts'])
print('w1 files at C0           :',len(files))
print('root .md files           :',len(mds),' seat-named:',len(seatmd))
print('root .json files         :',len(jss),' seat-named:',len(seatjs))
print('non-seat root .md        :',sorted({m[:-3] for m in mds}-set(names)))
print('non-seat root .json      :',sorted({j[:-5] for j in jss}-set(names)))
print('receipt dirs             :',len(recs),' all dispatched:',recs<=set(names))
print()
print('seats md+json            :',len(seatmd&seatjs))
print('seats md only            :',sorted(seatmd-seatjs))
print('seats json only          :',sorted(seatjs-seatmd))
print('seats receipts only      :',sorted(recs-seatmd-seatjs))
print('seats with nothing       :',sorted(set(names)-seatmd-seatjs-recs))
print('md present total         :',len(seatmd),'/',len(names))
print('json present total       :',len(seatjs),'/',len(names))
print('any artifact total       :',len(seatmd|seatjs|recs),'/',len(names))
