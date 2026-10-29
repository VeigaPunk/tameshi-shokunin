"""Corrected search: for each id, find a PRE-BASE commit C (ancestor of BASE, not ancestor of routed_at)
that touches a path named by the item text, and an added line that carries a whole-token key,
is absent at C's parent, absent at routed_at, and sits in an ACK-free <=30-line window at HEAD."""
import json,subprocess,re,os,sys,concurrent.futures
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
CL=os.environ['CLONE']; BASE='5e3569969b532310d2b8a3d130901757a3df356b'
D=json.load(open(LANE+'/.ufo/evidence/round-57/c1/defects.json'))['defects']
ACK=('planned','carried','still open','not worked','stay open','stays open','remain open','remains open','routed to round','not fixed','unfixed','unfixed','not landed')
PATHRE=re.compile(r'[A-Za-z0-9_./-]+\.(?:md|py|json|sh|yml|yaml|txt|ts|js)')
def g(*a): return subprocess.run(['git','-C',CL]+list(a),capture_output=True)
def show(rev,path):
    p=g('show','%s:%s'%(rev,path))
    return p.stdout.decode('utf-8','replace') if p.returncode==0 else None
def norm(t): return ' '.join(t.split())
def ack_in(s): return any(w in s.lower() for w in ACK)
def keyhit(text,keys):
    low=norm(text)
    for k in keys:
        if re.search(r'(?<![\w-])'+re.escape(k)+r'(?![\w-])',low,re.I): return k
    return None
def cand_paths(item_text):
    out=[]
    for m in PATHRE.findall(item_text):
        p=m.lstrip('`.,:;')
        if p and p not in out: out.append(p)
    return out
def is_anc(a,b): return g('merge-base','--is-ancestor',a,b).returncode==0
def search(d):
    keys=d['keys']; item_text=d.get('text','')+' '+d.get('extended_text','')
    routed=d['routed_at']; out=[]
    for P in cand_paths(item_text):
        if P.startswith('/') or '..' in P.split('/'): continue
        if show(BASE,P) is None: continue
        for C in g('log','--format=%H',BASE,'--',P).stdout.decode().split():
            if is_anc(C,routed): continue          # must be AFTER routing
            if not is_anc(C,BASE): continue        # must be at/before base
            par=g('rev-list','--parents','-n','1',C).stdout.decode().split()[1:]
            prevtxt=show(par[0],P) if par else None
            then=show(routed,P)
            cur=show('HEAD',P)
            if cur is None: continue
            lines=cur.split('\n')
            dt=g('diff','--unified=0','--no-color',par[0] if par else C,C,'--',P).stdout.decode('utf-8','replace')
            added=[l[1:] for l in dt.split('\n') if l.startswith('+') and not l.startswith('+++')]
            for E in added:
                ne=norm(E)
                if not (15<=len(ne)<=400): continue
                if ack_in(E): continue
                k=keyhit(E,keys)
                if k is None: continue
                if prevtxt is not None and ne in norm(prevtxt): continue
                if then is not None and ne in norm(then): continue
                hits=[i for i,l in enumerate(lines) if ne in norm(l)]
                got=None
                for i in hits:
                    n=len(lines)
                    for a in range(max(0,i-30),i+1):
                        for b in range(i+1,min(n+1,a+31)):
                            span=' '.join(lines[a:b])
                            if ack_in(span): break
                            if ne in norm(span): got=(a+1,b); break
                        if got: break
                    if got: break
                if got:
                    out.append(dict(id=d['id'],commit=C,path=P,lines='%d-%d'%got,excerpt=E.strip(),key=k))
                    break
            if out: break
        if out: break
    return out[:1]
res={}
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
    futs={ex.submit(search,d):d['id'] for d in D}
    for f in concurrent.futures.as_completed(futs):
        try: r=f.result()
        except Exception as e: r=[]; print('ERR',futs[f],repr(e),file=sys.stderr)
        if r: res[r[0]['id']]=r[0]
json.dump(res,open(os.path.dirname(os.path.abspath(__file__))+'/prebase3.json','w'),indent=1)
print('PREBASE EVIDENCE FOUND for %d/%d ids'%(len(res),len(D)))
for d in D:
    r=res.get(d['id'])
    print('%-7s %-4s %s'%(d['id'],'OK' if r else '--',(r['commit'][:10]+' '+r['path']+' '+r['lines']+' key='+str(r['key'])) if r else ''))
