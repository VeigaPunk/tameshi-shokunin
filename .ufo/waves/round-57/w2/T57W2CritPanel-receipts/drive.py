import importlib.util, json, glob, hashlib, subprocess, os, sys
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S=os.environ['HYAKU_SCRATCH']+'/tameshi-r57/T57W2CritPanel'
B='5e3569969b532310d2b8a3d130901757a3df356b'
C=S+'/clone'
spec=importlib.util.spec_from_file_location('m57', L+'/.ufo/evidence/round-57/c1/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
defects_doc=json.load(open(L+'/.ufo/evidence/round-57/c1/defects.json'))
defects=defects_doc['defects']
base_doc=json.loads(subprocess.run(['git','-C',L,'show',B+':corpus/routed-defects.json'],capture_output=True,check=True).stdout)
base_rows=base_doc['defects']
triage={}
for f in glob.glob(L+'/.ufo/waves/round-57/w1/T57W1ScribeItems*/rows.json'):
    for r in json.load(open(f)): triage[r['id']]=r
derived=json.load(open(S+'/derived.json'))['sab']
ids=[d['id'] for d in defects]
PRE_FIXED=[i for i in ids if triage[i]['status']=='fixed' and derived[i]=='fixed']
def honest_row(i):
    t=triage[i]; r={'id':i,'status':t['status'],'status_at_base':derived[i],'evidence':t['evidence']}
    if t['status']=='fixed': r['commit']=t['commit']
    if t['status']=='declined': r['reason']=t['verdict_basis']
    return r
def ledger(relabel):
    rows=[]
    planned=[]
    for i in ids:
        r=honest_row(i)
        if i in relabel:
            r={'id':i,'status':'open','status_at_base':'open','evidence':triage[i]['evidence']}
        if r['status']=='open': planned.append(i)
        rows.append(r)
    return rows, planned
def git(*a, inp=None):
    return subprocess.run(['git','-C',C]+list(a),capture_output=True,check=True,input=inp,
        env=dict(os.environ,GIT_AUTHOR_NAME='fx',GIT_AUTHOR_EMAIL='fx@example.invalid',GIT_COMMITTER_NAME='fx',GIT_COMMITTER_EMAIL='fx@example.invalid'))
def make_rev(name, rows, planned, verdicts):
    git('checkout','-q','--detach',B)
    doc=dict(base_doc); doc['defects']=base_rows+rows
    os.makedirs(C+'/corpus',exist_ok=True)
    open(C+'/corpus/routed-defects.json','w').write(json.dumps(doc,indent=1))
    os.makedirs(C+'/.ufo/evidence/round-57/c1',exist_ok=True)
    open(C+'/.ufo/evidence/round-57/c1/defects.json','w').write(open(L+'/.ufo/evidence/round-57/c1/defects.json').read())
    pj=json.dumps({'verdicts':verdicts},indent=1)
    open(C+'/.ufo/evidence/round-57/c1/panel.json','w').write(pj)
    with open(C+'/SCORECARD.md','a') as fh:
        fh.write('\n**Planned (round 58):** '+', '.join(planned)+'.\n')
    git('add','-A'); git('commit','-q','-m',name)
    rev=git('rev-parse','HEAD').stdout.decode().strip()
    return rev, hashlib.sha256(pj.encode()).hexdigest()
def score(name, rows, planned, verdicts, base_is_rev=None):
    rev,pin=make_rev(name, rows, planned, verdicts)
    notes=[]
    res=m.measure(C, rev, defects, True, 0, 999, 0, B, 49, m.EXPECTED_SPOTS, explain=lambda *a: notes.append(' '.join(str(x) for x in a)), panel_pin=pin, panel_allowed=5)
    c=res['counts']
    pd=[n for n in notes if n.startswith('panel-disagree')]
    other=[n for n in notes if not n.startswith('panel-disagree')]
    return {'name':name,'rev':rev[:12],'total':res['total'],'counts':{k:v for k,v in c.items() if v},
            'stat':res['stat'],'panel_disagree':len(pd),'panel_over':c['panel_over'],
            'arm_faults_excl_panel': sum(v for k,v in c.items() if k not in('panel_over','panel_pin') and v),
            'notes_head': other[:6], 'panel_ids': [p.split()[-1] for p in pd]}
truth=dict(derived)
rev_answer={i:triage[i]['status'] for i in ids}
all_open={i:'open' for i in ids}
all_fixed={i:'fixed' for i in ids}
rows_h,pl_h=ledger(set())
out=[]
out.append(score('honest_vs_truth', rows_h, pl_h, truth))
out.append(score('honest_vs_allopen', rows_h, pl_h, all_open))
out.append(score('honest_vs_allfixed', rows_h, pl_h, all_fixed))
out.append(score('honest_vs_revanswer', rows_h, pl_h, rev_answer))
r5,p5=ledger(set(PRE_FIXED[:5]))
out.append(score('relabel5_vs_truth', r5, p5, truth))
out.append(score('relabel5_vs_allopen', r5, p5, all_open))
r27,p27=ledger(set(PRE_FIXED))
out.append(score('relabel27_vs_truth', r27, p27, truth))
out.append(score('relabel27_vs_allopen', r27, p27, all_open))
rall,pall=ledger(set(ids))
out.append(score('relabelall_vs_allopen', rall, pall, all_open))
out.append(score('relabelall_vs_truth', rall, pall, truth))
json.dump({'pre_fixed':PRE_FIXED,'results':out},open(S+'/panel-sim.json','w'),indent=1)
for o in out:
    print(o['name'].ljust(26), 'total=%d'%o['total'], 'panel_disagree=%d'%o['panel_disagree'], 'panel_over=%d'%o['panel_over'], 'fixed=%d open=%d declined=%d'%(o['stat']['fixed'],o['stat']['open'],o['stat']['declined']), 'nonpanel_faults=%d'%o['arm_faults_excl_panel'], o['counts'] if o['arm_faults_excl_panel'] else '')
