import json,subprocess,re,os,sys,hashlib,shutil,importlib.util
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S='/fast/scratch/hyaku/tameshi-r57/T57W2SentC1'; ATK=S+'/a'; CL=ATK+'/clone'
C0='ca75c2674645ab6bdadeecb8584007c74342bfa9'; BASE='5e3569969b532310d2b8a3d130901757a3df356b'
DEF_SHA='bef2293ba3db863b03247e9867b11aa2501aa54af0b098ce0f974817f485dee9'
PANEL='.ufo/evidence/round-57/c1/panel.json'
COUNTER_SRC=LANE+'/.ufo/evidence/round-57/c1/measure.py'
ACK=('planned','carried','still open','not worked','stay open','stays open','remain open','remains open','routed to round','not fixed','unfixed','not landed')
def sh(*a): return subprocess.run(list(a),capture_output=True)
def g(*a,cl=None,check=False):
    r=subprocess.run(['git','-C',cl or CL]+list(a),capture_output=True)
    if check and r.returncode: raise RuntimeError(' '.join(a)+': '+r.stderr.decode())
    return r
def norm(t): return ' '.join(t.split())
def ack_in(s): return any(w in s.lower() for w in ACK)
def wt(k): return re.compile(r'(?<![\w-])'+re.escape(k)+r'(?![\w-])',re.I)
D=json.load(open(LANE+'/.ufo/evidence/round-57/c1/defects.json'))['defects']
HON={r['id']:r for r in json.load(open(LANE+'/corpus/routed-defects.json'))['defects']}
BASE_ROWS=json.loads(g('show','%s:corpus/routed-defects.json'%BASE,cl=LANE).stdout.decode())['defects']
def prepare():
    if os.path.exists(ATK): shutil.rmtree(ATK)
    os.makedirs(ATK)
    r=sh('git','clone','--shared','--quiet',LANE,CL); assert r.returncode==0, r.stderr
    g('checkout','--detach',C0,check=True)
    top=g('rev-parse','--show-toplevel',check=True).stdout.decode().strip()
    assert os.path.realpath(top)==os.path.realpath(CL), top
    shutil.copytree(LANE+'/.ufo/evidence/round-57',CL+'/.ufo/evidence/round-57',dirs_exist_ok=True)
    shutil.copy(LANE+'/SCORECARD.md',CL+'/SCORECARD.md')
    commit('harness: instrument copy as in dry-c1.sh',{})
def commit(msg,writes,append=None):
    for p,t in writes.items():
        full=os.path.join(CL,p); os.makedirs(os.path.dirname(full),exist_ok=True)
        open(full,'w',encoding='utf-8').write(t)
    for p,t in (append or {}).items():
        full=os.path.join(CL,p); os.makedirs(os.path.dirname(full),exist_ok=True)
        open(full,'a',encoding='utf-8').write(t)
    g('add','-A',check=True)
    r=subprocess.run(['git','-C',CL,'-c','user.name=fixture','-c','user.email=fixture@example.invalid','commit','-q','--allow-empty','-m',msg],capture_output=True)
    assert r.returncode==0, r.stderr
    return g('rev-parse','HEAD',check=True).stdout.decode().strip()
def base49(): return json.loads(json.dumps(BASE_ROWS))
def ledger_blob(rows): return json.dumps({'schema':'tameshi-routed-defects-v1','round':57,'defects':rows},indent=1,ensure_ascii=False)+'\n'
def panel_blob(v): return json.dumps({'schema':'tameshi-c1-blind-panel-v1','base':BASE,'verdicts':v},indent=1,ensure_ascii=False)+'\n'
def planned_para(ids,rnd=58,extra=''): return '\n**Planned (round %d):** %s.%s\n'%(rnd,', '.join(ids),extra)
def load_counter(panel_sha):
    src=COUNTER_SRC
    txt=open(src,encoding='utf-8').read()
    txt2=re.sub(r"PANEL_SHA256 = '[^']*'","PANEL_SHA256 = %r"%panel_sha,txt); assert txt2!=txt
    p=S+'/h/measure-pinned.py'; open(p,'w',encoding='utf-8').write(txt2)
    spec=importlib.util.spec_from_file_location('mp',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
def score(rev,panel,label,tail=int(os.environ.get('TAIL','12'))):
    pb=panel_blob(panel)
    m=load_counter(hashlib.sha256(pb.encode()).hexdigest())
    blob=g('show','%s:.ufo/evidence/round-57/c1/defects.json'%rev,check=True).stdout
    pin_ok=hashlib.sha256(blob).hexdigest()==DEF_SHA
    defects=json.loads(blob.decode())['defects']
    out=[]
    note=lambda *x: out.append('EXPLAIN '+' '.join(str(v) for v in x))
    res=m.measure(CL,rev,defects,pin_ok,explain=note,panel_pin=m.PANEL_SHA256)
    print('=== %s'%label)
    for l in (out+[m.terms_line(res),m.verdict(res)])[-tail:]: print(l)
    return res
