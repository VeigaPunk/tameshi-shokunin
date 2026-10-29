import importlib.util, json, os, subprocess, hashlib, copy
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; S=os.environ['S']; W=os.environ['W']; R=os.environ['R']
spec=importlib.util.spec_from_file_location('m50', LANE+'/.ufo/evidence/round-50/c1/measure.py'); m50=importlib.util.module_from_spec(spec); spec.loader.exec_module(m50)
clone=S+'/clone'; SPOT='corpus/lessons/round-54-verifier-spotcheck.md'
rows=json.load(open(W+'/rows.json'))
spot_sha=hashlib.sha256(subprocess.run(['git','-C',LANE,'show','5e3569969b532310d2b8a3d130901757a3df356b:'+SPOT],capture_output=True).stdout).hexdigest()
env=dict(os.environ,GIT_AUTHOR_NAME='fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',GIT_COMMITTER_NAME='fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid')
def run(name, mutate):
    rs=copy.deepcopy(rows); mutate(rs)
    doc={'schema':'tameshi-routed-defects-v1','round':54,'note':'neg','defects':[{k:v for k,v in r.items() if k not in('keys','verdict_basis')} for r in rs]}
    open(clone+'/corpus/routed-defects.json','w').write(json.dumps(doc,ensure_ascii=False)+'\n')
    subprocess.run(['git','-C',clone,'add','corpus/routed-defects.json'],check=True)
    subprocess.run(['git','-C',clone,'commit','-q','--allow-empty','-m','neg '+name],check=True,env=env)
    rev=subprocess.run(['git','-C',clone,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    defects=[{'id':r['id'],'file':SPOT,'file_sha256':spot_sha,'routed_at':'650987a0d6fc285b37f0f9e63a3aae864af9cd5a','keys':r['keys']} for r in rs]
    out=[]
    _,c,st,t,_=m50.measure(clone,rev,defects,True,0,12,explain=lambda *a: out.append(' '.join(map(str,a))),this_round_floor=0)
    return f"NEG {name}: total={t} counts={ {k:v for k,v in c.items() if v} } explain={out}"
res=[
 run('R54.6 commit=ff2a821 (predates routing)', lambda rs: rs[1].update(commit='ff2a821'+'0'*0 if False else subprocess.run(['git','-C',clone,'rev-parse','ff2a821'],capture_output=True,text=True).stdout.strip())),
 run('R54.5 excerpt w1=29 (wrong count)', lambda rs: rs[0]['evidence'][0].update(excerpt=rs[0]['evidence'][0]['excerpt'].replace('w1=28','w1=29'))),
 run('R54.7 keys without a matching excerpt', lambda rs: rs[2].update(keys=['nonexistent-key-zz'])),
]
txt='\n'.join(res)+'\n'; open(R+'/negative-controls.txt','w').write(txt); print(txt)
