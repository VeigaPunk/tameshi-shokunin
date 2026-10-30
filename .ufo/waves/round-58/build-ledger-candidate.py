#!/usr/bin/env python3
"""Reconcile bounded existing evidence into a candidate; never invent an excerpt.
Unresolved rows stay open and name their remaining debt in SCORECARD. This script
only writes a candidate under the round wave directory; L1 reviews before install.
"""
import collections, functools, importlib.util, json, pathlib, re, subprocess
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin'); W=L/'.ufo/waves/round-58/w1'
sp=importlib.util.spec_from_file_location('counter',L/'.ufo/evidence/round-58/c1/measure.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
REV=subprocess.check_output(['git','-C',str(L),'rev-parse','master'],text=True).strip()
@functools.lru_cache(None)
def git(*args):return subprocess.run(['git','-C',str(L),*args],capture_output=True).stdout
@functools.lru_cache(None)
def text(r,p):return git('show',r+':'+p).decode('utf-8','replace')
@functools.lru_cache(None)
def touched(c):return set(git('diff-tree','--no-commit-id','--name-only','-r','--root','-m',c).decode().splitlines())
@functools.lru_cache(None)
def parent(c):return git('rev-list','--parents','-n','1',c).decode().split()[1:2]
def find_evidence(d,paths,commit=None):
 for p in dict.fromkeys(paths):
  if not p or p.startswith(m.HARD) or p==m.LEDGER or p in spots:continue
  if p.startswith(m.SOFT) and not any(p.endswith(k) for k in d['keys']):continue
  if commit:
   if p not in touched(commit):continue
   msg=git('log','-1','--format=%B',commit).decode()
   tied=re.search(r'(?<![\w.])'+re.escape(d['id'])+r'(?!\d)',msg) or commit.startswith(pcommits.get(d['id'],'!')[:40]) or p in d['text'] or pathlib.Path(p).name in d['text']
   if not tied:continue
   before=text(parent(commit)[0],p) if parent(commit) else ''
   routed=text(d['routed_at'],p)
  for n,line in enumerate(text(REV,p).splitlines(),1):
   if len(m.norm(line))<15:continue
   if commit and any(a in line.lower() for a in m.ACK_WORDS):continue
   ex=line.strip()
   if len(m.norm(ex))>400:
    hit=next((re.search(re.escape(k),ex,re.I) for k in d['keys'] if re.search(re.escape(k),ex,re.I)),None)
    if not hit:continue
    ex=ex[max(0,hit.start()-80):max(0,hit.start()-80)+390]
   e={'path':p,'lines':f'{n}-{n}','excerpt':ex}
   if not m.has_key(e,d['keys']):continue
   if commit and (m.norm(ex) in m.norm(before) or m.norm(ex) in m.norm(routed)):continue
   return e
 return None
D=json.loads((L/'.ufo/evidence/round-58/c1/defects.json').read_text())['defects'];spots={d['file'] for d in D}
P=json.loads((L/'.ufo/evidence/round-58/c1/panel.json').read_text());pcommits={i:v.get('commit','') for i,v in P['detail'].items()}
C={r['id']:r for r in json.loads((L/'.ufo/waves/round-57/integrate/candidate-ledger.json').read_text())['defects']};V={}
for p in W.glob('T58W1Verify*.json'):
 for r in json.loads(p.read_text()).get('rows',[]):V[r['id']]=r
repairs={'R51.5':'38e4e3aff7cf0da9032761acd1548e49ba49d9fe','R51.6':'38e4e3aff7cf0da9032761acd1548e49ba49d9fe','R53.2':'7d5ae605eb6f07b91e836fd5afe822db5e00ecd3','R53.4':'7d5ae605eb6f07b91e836fd5afe822db5e00ecd3','R55.1':'7d5ae605eb6f07b91e836fd5afe822db5e00ecd3','R55.4':'6024c8fcc9b01950b9bff11b59cab257eea87333'}
rows=[];unresolved=[]
for d in D:
 i=d['id'];sab=P['verdicts'][i];r={'id':i,'status_at_base':sab}
 paths=[e.get('path') for o in (C.get(i,{}),V.get(i,{})) for e in o.get('evidence',[]) if isinstance(e,dict)]
 if i in repairs:
  c=repairs[i];e=find_evidence(d,['corpus/lessons/round-58.md'],c)
  if e:r.update(status='fixed',commit=c,evidence=[e])
  else:unresolved.append((i,'new-fix-no-excerpt'))
 elif sab=='fixed':
  commits=list(dict.fromkeys(c for c in [pcommits.get(i),C.get(i,{}).get('commit'),V.get(i,{}).get('commit')] if isinstance(c,str) and re.fullmatch('[0-9a-f]{40}',c)))
  for c in commits:
   relevant=paths+[p for p in touched(c) if p.endswith('.md')]
   e=find_evidence(d,relevant,c)
   if e:r.update(status='fixed',commit=c,evidence=[e]);break
  else:unresolved.append((i,'base-fixed-no-durable-chain'))
 if 'status' not in r:
  r['status']='declined' if sab=='declined' else 'open'
  if sab=='fixed':r['status_at_base']='open'
  r['reason']=('The blind panel describes this as declined; preserve the reasoned supersession rather than assert a historical fix.' if sab=='declined' else 'Resolution evidence is incomplete; preserve this routed item for round 59 rather than manufacture a fixed disposition.')
  e=find_evidence(d,paths+['SCORECARD.md','corpus/lessons/round-58.md'])
  r['evidence']=[e] if e else []
 rows.append(r)
base_doc=json.loads(git('show',m.BASE+':corpus/routed-defects.json'));base_doc['round']=58;base_doc['defects']+=rows
out=L/'.ufo/waves/round-58/ledger-candidate.json';out.write_text(json.dumps(base_doc,ensure_ascii=False,indent=1)+'\n')
print('candidate',out,'statuses',collections.Counter(r['status'] for r in rows),'unresolved',unresolved)
for r in rows:
 if not r['evidence']:print('NO_EVIDENCE',r['id'])
print('OPEN',','.join(r['id'] for r in rows if r['status']=='open'))
