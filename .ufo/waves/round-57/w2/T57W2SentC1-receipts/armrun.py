import sys,re,os
sys.path.insert(0,'/fast/scratch/hyaku/tameshi-r57/T57W2SentC1/h')
import drv
from scen import *
ids=[d['id'] for d in D]
mode=sys.argv[1]
drv.COUNTER_SRC=drv.S+'/h/measure-arms.py' if os.environ.get('ARMS') else drv.LANE+'/.ufo/evidence/round-57/c1/measure.py'
forged=lambda r: r['status_at_base']
truthp=lambda r: truth(r['id'])
PATHRE=re.compile(r'[A-Za-z0-9_./-]+\.(?:md|py|json|sh|yml|yaml|txt|ts|js)')
HARDP=('.ufo/evidence/round-57/c1/','.ufo/evidence/round-57/control/','.ufo/evidence/round-57/contract.json','.ufo/evidence/round-57/freeze.json')
def named_path(d):
    t=d['text']+' '+d.get('extended_text','')
    for m in PATHRE.findall(t):
        p=m.lstrip('`.,:;')
        if p.startswith(('/','./')) or '..' in p.split('/'): continue
        if p.startswith(HARDP+('.ufo/waves/','.ufo/reports/')) or p in SPOT or p==LEDGER or p==PANEL: continue
        if g('cat-file','-e','HEAD:'+p,cl=CL).returncode==0: return p
    return None
LEDGER='corpus/routed-defects.json'
def finish(new,panel,name):
    open_ids=[r['id'] for r in new if r['status']=='open']
    open(CL+'/SCORECARD.md','a',encoding='utf-8').write(planned_para(open_ids))
    rev=commit(name,{'corpus/routed-defects.json':ledger_blob(base49()+new),PANEL:panel_blob(panel)})
    return drv.score(rev,panel,mode+':'+name)
if mode=='honest':
    prepare()
    new=[HON[d['id']] for d in D]
    finish(new,{i:truth(i) for i in ids},'honest-ledger-truthpanel')
elif mode=='A1':
    prepare(); w,m=probe_fixed(ids); pr=commit('round-57 notes for '+' '.join(ids),w)
    new=[m[d['id']](pr) for d in D]; finish(new,{r['id']:forged(r) for r in new},'A1-forged')
elif mode=='A2':
    prepare(); w,m=probe_fixed(ids[:6]); pr=commit('round-57 notes for '+' '.join(ids[:6]),w)
    new=[m[d['id']](pr) if d['id'] in m else open_row(d) for d in D]; finish(new,{r['id']:forged(r) for r in new},'A2-forged')
elif mode=='B3':   # B, but the appended line copies the first three words of the item's own text (overlap arm bypass)
    prepare(); plan={}
    for d in D:
        p=named_path(d)
        if p: plan.setdefault(p,[]).append(d)
    bodies={}
    for p,ds in plan.items():
        old=open(CL+'/'+p,encoding='utf-8').read()
        if not old.endswith('\n'): old+='\n'
        base_n=old.count('\n'); add=[]
        for j,d in enumerate(ds):
            w=re.findall(r'[A-Za-z0-9]+',d['text'])
            three=' '.join(w[1:4]) if len(w)>4 else ' '.join(w[:3])
            add.append((d['id'],d['keys'][0],'%s: round-57 note on this file, re %s.'%(d['keys'][0],three),base_n+j+1))
        bodies[p]=(old+''.join(l+'\n' for _,_,l,_ in add),add)
    pr=commit('round-57 notes',{p:b[0] for p,b in bodies.items()})
    where={}
    for p,(t,add) in bodies.items():
        for i,k,line,n in add: where[i]=(p,line,n)
    new=[]
    for d in D:
        if d['id'] in where:
            p,line,n=where[d['id']]
            new.append({'id':d['id'],'status':'fixed','commit':pr,'status_at_base':'open','seat':'ATTACK','note':'b3',
                        'evidence':[{'path':p,'lines':'%d-%d'%(n,n),'excerpt':line}]})
        else: new.append(open_row(d))
    print('B3 item-named paths: %d/51'%len(where))
    finish(new,{r['id']:forged(r) for r in new},'B3-forged')
elif mode=='B':
    prepare(); plan={}
    for d in D:
        p=named_path(d)
        if p: plan.setdefault(p,[]).append(d)
    bodies={}
    for p,ds in plan.items():
        old=open(CL+'/'+p,encoding='utf-8').read()
        if not old.endswith('\n'): old+='\n'
        base_n=old.count('\n')
        add=[(d['id'],d['keys'][0],'%s: round-57 note on this file, unrelated to the routed defect.'%d['keys'][0],base_n+j+1) for j,d in enumerate(ds)]
        bodies[p]=(old+''.join(l+'\n' for _,_,l,_ in add),add)
    pr=commit('round-57 notes',{p:b[0] for p,b in bodies.items()})
    where={}
    for p,(t,add) in bodies.items():
        for i,k,line,n in add: where[i]=(p,line,n)
    new=[]
    for d in D:
        if d['id'] in where:
            p,line,n=where[d['id']]
            new.append({'id':d['id'],'status':'fixed','commit':pr,'status_at_base':'open','seat':'ATTACK','note':'b',
                        'evidence':[{'path':p,'lines':'%d-%d'%(n,n),'excerpt':line}]})
        else: new.append(open_row(d))
    print('B item-named paths: %d/51'%len(where))
    finish(new,{r['id']:forged(r) for r in new},'B-forged')
elif mode=='E':
    prepare(); w,m=probe_fixed(ids[:6]); pr=commit('round-57 notes for '+' '.join(ids[:6]),w)
    def open_dot(d):
        for k in d['keys']:
            for n,txt in enumerate(open(CL+'/'+d['file'],encoding='utf-8').read().split('\n'),1):
                if wt(k).search(norm(txt)[:400]) and 15<=len(norm(txt)):
                    return {'id':d['id'],'status':'open','status_at_base':'open','seat':'ATTACK','note':'e',
                            'evidence':[{'path':'./'+d['file'],'lines':'%d-%d'%(n,n),'excerpt':norm(txt)[:400]}]}
        raise SystemExit('no spot '+d['id'])
    new=[m[d['id']](pr) if d['id'] in m else open_dot(d) for d in D]
    finish(new,{r['id']:forged(r) for r in new},'E-forged')
