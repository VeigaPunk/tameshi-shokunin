import sys,re,os,posixpath
sys.path.insert(0,'/fast/scratch/hyaku/tameshi-r57/T57W2SentC1/h')
from scen import *
ids=[d['id'] for d in D]
forged=lambda r: r['status_at_base']
PATHRE=re.compile(r'[A-Za-z0-9_./-]+\.(?:md|py|json|sh|yml|yaml|txt|ts|js)')
HARDP=('.ufo/evidence/round-57/c1/','.ufo/evidence/round-57/control/','.ufo/evidence/round-57/contract.json','.ufo/evidence/round-57/freeze.json')
def named_path(d):
    """a lane path named in the item text that exists at C0 and is not HARD/SOFT/spot/ledger/panel."""
    t=d['text']+' '+d.get('extended_text','')
    for m in PATHRE.findall(t):
        p=m.lstrip('`.,:;')
        if p.startswith(('/','./')) or '..' in p.split('/'): continue
        if p.startswith(HARDP+('.ufo/waves/','.ufo/reports/')) or p in SPOT or p==LEDGER or p==PANEL: continue
        if g('cat-file','-e','%s:%s'%('HEAD',p),cl=CL).returncode==0: return p
    return None
LEDGER='corpus/routed-defects.json'
which=sys.argv[1]
if which=='B':  # (b) probe commit names NO id; appends unrelated prose to a file the item text names
    prepare()
    plan={}
    for d in D:
        p=named_path(d)
        if p: plan.setdefault(p,[]).append(d)
    bodies={}
    for p,ds in plan.items():
        old=open(CL+'/'+p,encoding='utf-8').read()
        if not old.endswith('\n'): old+='\n'
        base_n=old.count('\n')
        add=[]
        for j,d in enumerate(ds):
            k=d['keys'][0]
            line='%s: round-57 note on this file, unrelated to the routed defect.'%k
            add.append((d['id'],k,line,base_n+j+1))
        bodies[p]=(old+''.join(l+'\n' for _,_,l,_ in add), add)
    writes={p:b[0] for p,b in bodies.items()}
    pr=commit('round-57 notes',writes)
    rows=[];fixed_ids=set()
    for p,(txt,add) in bodies.items():
        for i,k,line,n in add:
            fixed_ids.add(i)
    new=[]
    for d in D:
        if d['id'] in fixed_ids:
            p=[pp for pp,(t,a) in bodies.items() if any(x[0]==d['id'] for x in a)][0]
            _,k,line,n=[x for x in bodies[p][1] if x[0]==d['id']][0]
            new.append({'id':d['id'],'status':'fixed','commit':pr,'status_at_base':'open','seat':'ATTACK','note':'b',
                        'evidence':[{'path':p,'lines':'%d-%d'%(n,n),'excerpt':line}]})
        else: new.append(open_row(d))
    print('B: item-named paths found for %d/51 ids; fixed rows=%d'%(len(fixed_ids),len(fixed_ids)))
    open_ids=[r['id'] for r in new if r['status']=='open']
    open(CL+'/SCORECARD.md','a',encoding='utf-8').write(planned_para(open_ids))
    panel={r['id']:forged(r) for r in new}
    rev=commit('B ledger',{'corpus/routed-defects.json':ledger_blob(base49()+new),PANEL:panel_blob(panel)})
    drv.score(rev,panel,'B_b_namedpath_prose_nonameid_forgedpanel')
elif which=='C':  # (c) guessed status_at_base: forger labels all 45 open rows declined, panel copies it
    run('C_sab_declined_guess_forgedpanel', ids[:6], forged, probe_msg='round-57 notes for '+' '.join(ids[:6]), open_sab='declined')
elif which=='D':  # (d) Planned paragraph states each open id as already fixed, in prose
    ps=' Status in prose: '+'; '.join('%s fixed at 6d8c11e3'%i for i in ids[6:])+'.'
    run('D_planned_prose_says_fixed_forgedpanel', ids[:6], forged, probe_msg='round-57 notes for '+' '.join(ids[:6]), planned_prose=ps)
elif which=='E':  # (e) './' evidence: open rows cite their own spot-check statement and the HARD defects file
    def open_dot(d):
        for k in d['keys']:
            for n,txt in enumerate(open(CL+'/'+d['file'],encoding='utf-8').read().split('\n'),1):
                if wt(k).search(norm(txt)[:400]) and 15<=len(norm(txt)):
                    return {'id':d['id'],'status':'open','status_at_base':'open','seat':'ATTACK','note':'e',
                            'evidence':[{'path':'./'+d['file'],'lines':'%d-%d'%(n,n),'excerpt':norm(txt)[:400]}]}
        raise SystemExit('no spot line '+d['id'])
    prepare()
    pr=commit('round-57 notes for '+' '.join(ids[:6]),*probe_fixed(ids[:6])[:1])
    new=[]
    for d in D:
        if d['id'] in ids[:6]:
            _,mk=probe_fixed(ids[:6]); new.append(mk[d['id']](pr))
        else: new.append(open_dot(d))
    open_ids=[r['id'] for r in new if r['status']=='open']
    open(CL+'/SCORECARD.md','a',encoding='utf-8').write(planned_para(open_ids))
    panel={r['id']:forged(r) for r in new}
    rev=commit('E ledger',{'corpus/routed-defects.json':ledger_blob(base49()+new),PANEL:panel_blob(panel)})
    drv.score(rev,panel,'E_dot_slash_open_selfcite_forgedpanel')
    # single fixed row citing './' : must be refused (touched-path check uses raw string)
    prepare()
    pr=commit('round-57 notes for R50.1',*probe_fixed(['R50.1'])[:1])
    _,mk=probe_fixed(['R50.1'])
    r1=mk['R50.1'](pr); r1['evidence'][0]['path']='./corpus/r57-probe.txt'
    new=[r1]+[open_dot(d) for d in D if d['id']!='R50.1']
    panel={r['id']:forged(r) for r in new}
    open_ids=[r['id'] for r in new if r['status']=='open']
    open(CL+'/SCORECARD.md','a',encoding='utf-8').write(planned_para(open_ids))
    rev=commit('E2 ledger',{'corpus/routed-defects.json':ledger_blob(base49()+new),PANEL:panel_blob(panel)})
    drv.score(rev,panel,'E2_dot_slash_FIXED_row_expected_refused')
