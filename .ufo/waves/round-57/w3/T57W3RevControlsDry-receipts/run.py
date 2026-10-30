import os, pathlib, subprocess, shutil, json, hashlib, re
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
R=L/'.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run4'
S=pathlib.Path('/fast/scratch/hyaku/tameshi-r57/T57W3RevControlsDry')
E=pathlib.Path('.ufo/evidence/round-57')
BASE='5e3569969b532310d2b8a3d130901757a3df356b'
os.environ.update(HYAKU_SCRATCH=str(S/'work'),PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1')
R.mkdir(parents=True,exist_ok=True); S.mkdir(parents=True,exist_ok=True)
log=[]
def run(args,label=None):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True,cwd=S)
    log.append({'command': [str(x) for x in args], 'exit':p.returncode, 'stdout':p.stdout,'stderr':p.stderr})
    if label:
        (R/(label+'.stdout')).write_text(p.stdout); (R/(label+'.stderr')).write_text(p.stderr); (R/(label+'.exit')).write_text(str(p.returncode)+'\n')
    (R/'commands.json').write_text(json.dumps(log,indent=2)+'\n')
    return p
def git(c,*a): return run(['git','-C',c,*a])
def guard(c): assert git(c,'rev-parse','--show-toplevel').stdout.strip()==str(c)
def commit(c,msg):
    guard(c); assert git(c,'add','-A').returncode==0
    assert git(c,'-c','user.name=fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm',msg).returncode==0
    return git(c,'rev-parse','HEAD').stdout.strip()
def put(c,p,data):
    f=c/p; f.parent.mkdir(parents=True,exist_ok=True); f.write_text(data)
def jput(c,p,obj): put(c,p,json.dumps(obj,indent=2,sort_keys=True)+'\n')
master=git(L,'rev-parse','master').stdout.strip(); (R/'master.txt').write_text(master+'\n')
c=S/'clone'
assert run(['git','-C',S,'clone','--shared',L,c]).returncode==0
guard(c); assert git(c,'checkout','--detach',master).returncode==0
for p in [pathlib.Path('corpus/routed-defects.json'),pathlib.Path('SCORECARD.md'),E]:
    dest=c/p
    if dest.is_dir(): shutil.rmtree(dest)
    dest.parent.mkdir(parents=True,exist_ok=True)
    if (L/p).is_dir(): shutil.copytree(L/p,dest)
    else: shutil.copy2(L/p,dest)
rows=json.loads((c/'corpus/routed-defects.json').read_text())['defects'][49:]
with (c/'SCORECARD.md').open('a') as f: f.write('\n**Planned (round 58):** '+', '.join(x['id'] for x in rows if x['status']=='open')+'.\n')
# Pin a deliberately synthetic panel, with synthetic provenance accepted by the unchanged arm.
seat='T57W3DrySyntheticPanel'
real_panel=json.loads((c/E/'c1/panel.json').read_text())
verdicts=real_panel['verdicts']
seatdoc={'synthetic':True,'verdicts':{k:{'verdict':v} for k,v in verdicts.items()}}
jput(c,pathlib.Path('.ufo/waves/round-57/w3')/(seat+'.json'),seatdoc)
seatsha=hashlib.sha256((c/'.ufo/waves/round-57/w3'/(seat+'.json')).read_bytes()).hexdigest()
panel={'synthetic':True,'verdicts':verdicts,'detail':{k:dict(real_panel.get('detail',{}).get(k,{}),seat=seat) for k in verdicts},'files':{seat:seatsha}}
jput(c,E/'c1/panel.json',panel)
mp=c/E/'c1/measure.py'; original_counter=mp.read_text()
pin=hashlib.sha256((c/E/'c1/panel.json').read_bytes()).hexdigest()
mp.write_text(re.sub(r'^PANEL_SHA256 = .*$',"PANEL_SHA256 = '%s'"%pin,original_counter,flags=re.M))
freeze=c/E/'freeze.json'
if freeze.exists(): freeze.unlink()
jput(c,pathlib.Path('.ufo/waves/round-57/w3-results.json'),{'results':[{'name':seat}]})
guard(c)
assert git(c,'add','-f','.ufo/waves/round-57/w3/'+seat+'.json','.ufo/waves/round-57/w3-results.json').returncode==0
rev=commit(c,'fixture: current master plus working instruments and synthetic pinned panel')
(R/'assembly.json').write_text(json.dumps({'master':master,'scratch_rev':rev,'synthetic_panel_sha256':pin,'synthetic_status_counts':{v:sum(x==v for x in verdicts.values()) for v in set(verdicts.values())}},indent=2)+'\n')
run(['bash',c/E/'controls.sh',c,BASE,rev,R/'controls'],'controls')
def decide(label,r):
    out=c/('dry-'+label); out.mkdir(exist_ok=True)
    p=run(['bash',c/E/'deciding-run.sh',c,BASE,r,out],label)
    (R/(label+'.outdir.json')).write_text(json.dumps(sorted(x.name for x in out.iterdir()))+'\n')
    return p
decide('missing-freeze',rev)
decide('rev-not-head',master)
# Remove panel pin only: freeze integrity is valid, so observe whether deciding-run explicitly refuses the pin.
mp.write_text(original_counter)
co=json.loads((c/E/'contract.json').read_text())
# A first synthetic freeze carries zero amendments to match its one manifest commit.
co['amendments']=[]; jput(c,E/'contract.json',co)
files={}
for p in co['frozen_paths']:
    if p==str(E/'freeze.json'): continue
    key=p if p.startswith('tools/') else p[len(str(E))+1:]
    files[key]=hashlib.sha256((c/p).read_bytes()).hexdigest()
jput(c,E/'freeze.json',{'schema':'tameshi-freeze-v1','round':57,'base':BASE,'files':files,'amendments':[]})
rev2=commit(c,'fixture: synthetic integrity-valid freeze with pending panel pin')
decide('missing-panel-pin',rev2)
# Counter evidence of the pin failure, independent of deciding-run's missing-receipt gate.
run(['python3',mp,'--lane',c,'--rev',rev2,'--work',S/'pin-counter-work','--explain'],'missing-panel-pin-counter')
shutil.rmtree(S)
print(json.dumps({'master':master,'controls_exit':log[-1]['exit'],'receipts':str(R)}))
