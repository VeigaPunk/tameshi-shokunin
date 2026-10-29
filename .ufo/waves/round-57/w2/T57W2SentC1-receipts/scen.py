import sys,json,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import drv
from drv import D,HON,CL,g,norm,ack_in,wt,base49,ledger_blob,panel_blob,planned_para,PANEL,commit,prepare
SPOT={x['file'] for x in D}
DD={d['id']:d for d in D}
def keyline(d):
    for k in d['keys']:
        line='%s: round-57 probe note for %s, see the routed entry.'%(k,d['id'])
        if not ack_in(line) and wt(k).search(line) and 15<=len(norm(line))<=400: return k,line
    raise SystemExit('no key '+d['id'])
def lane_keyed(d):
    for k in d['keys']:
        r=g('grep','-rIn','-F','--',k,cl=CL)
        for ln in r.stdout.decode('utf-8','replace').split('\n'):
            p,_,rest=ln.partition(':'); num,_,txt=rest.partition(':')
            if not num.isdigit(): continue
            if p.startswith(('.ufo/waves/','.ufo/reports/','.ufo/evidence/round-57/','corpus/routed-defects.json')) or p in SPOT: continue
            if ack_in(txt) or not wt(k).search(txt): continue
            if 15<=len(norm(txt))<=400: return p,int(num),norm(txt)
    raise SystemExit('no lane key '+d['id'])
def open_row(d,sab='open'):
    p,n,ex=lane_keyed(d)
    return {'id':d['id'],'status':'open','status_at_base':sab,'seat':'ATTACK','note':'forged open',
            'evidence':[{'path':p,'lines':'%d-%d'%(n,n),'excerpt':ex}]}
def truth(i): return HON[i]['status_at_base']
def probe_fixed(ids):
    """one new file, its lines are the excerpts; the caller's commit names ids. Returns (writes, row-maker)."""
    lines=[keyline(DD[i])[1] for i in ids]
    text='\n'.join(lines)+'\n'
    makers={}
    for i in ids:
        ln=keyline(DD[i])[1]; n=lines.index(ln)+1
        makers[i]=(lambda pr,i=i,ln=ln,n=n: {'id':i,'status':'fixed','commit':pr,'status_at_base':'open','seat':'ATTACK',
                    'note':'probe','evidence':[{'path':'corpus/r57-probe.txt','lines':'%d-%d'%(n,n),'excerpt':ln}]})
    return {'corpus/r57-probe.txt':text}, makers
def run(name, ids_fixed, panel_fn, probe_msg=None, planned_prose='', open_sab='open', extra_writes=None, fixed_maker=None):
    prepare()
    writes,makers=({},{})
    pr=None
    if ids_fixed:
        writes,makers=probe_fixed(ids_fixed) if fixed_maker is None else fixed_maker
        pr=commit(probe_msg or 'round-57 probe notes',writes)
    new=[]
    for d in D:
        if d['id'] in makers: new.append(makers[d['id']](pr))
        else: new.append(open_row(d,sab=open_sab))
    open_ids=[r['id'] for r in new if r['status']=='open']
    sc=open(CL+'/SCORECARD.md',encoding='utf-8').read()+planned_para(open_ids,extra=planned_prose)
    open(CL+'/SCORECARD.md','w',encoding='utf-8').write(sc)
    panel={r['id']:panel_fn(r) for r in new}
    rev=commit(name,{'corpus/routed-defects.json':ledger_blob(base49()+new),PANEL:panel_blob(panel)})
    return drv.score(rev,panel,name)
