import json,subprocess,re,posixpath,collections
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
import subprocess as _sp
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
D=json.load(open(LANE+'/.ufo/evidence/round-57/c1/defects.json'))['defects']
DD={d['id']:d for d in D}
H={r['id']:r for r in json.load(open(LANE+'/corpus/routed-defects.json'))['defects'] if r['id'] in DD}
fixed=[i for i in H if H[i]['status']=='fixed']; opn=[i for i in H if H[i]['status']=='open']
SPOT={d['file'] for d in D}
def g(*a): return _sp.run(['git','-C',LANE]+list(a),capture_output=True)
def exists_at(rev,p): return g('cat-file','-e','%s:%s'%(rev,p)).returncode==0
def canon(p): import posixpath; return posixpath.normpath(p)
def ev_paths(i): return [e['path'] for e in H[i]['evidence']]
x5=None

def parent(c):
    r=g('rev-list','--parents','-n','1',c).stdout.decode().split(); return r[1] if len(r)>1 else None
def commit_of(i): return H[i]['commit']
def x3a(i):  # reject if every evidence path is CREATED by the fixing commit (absent at its parent)
    c=commit_of(i); par=parent(c)
    return all(not exists_at(par,canon(p)) for p in ev_paths(i)) if par else False
def x3b(i):  # reject if every evidence path is absent at routed_at (created after routing)
    ra=DD[i]['routed_at']
    return all(not exists_at(ra,canon(p)) for p in ev_paths(i))
def msg_names(i):
    m=g('log','-1','--format=%B',commit_of(i)).stdout.decode()
    return re.search(r'(?<![\w.])'+re.escape(i)+r'(?!\d)',m) is not None
def x3c(i):  # x3a but a named message exempts (what the attacker gets for free)
    return x3a(i) and not msg_names(i)
print('honest fixed rows: %d'%len(fixed))
for name,fn in [('X3a every evidence path created by fixing commit',x3a),('X3b every evidence path absent at routed_at',x3b),
                ('X3c X3a unless commit message names id',x3c)]:
    bad=[i for i in fixed if fn(i)]
    print('%-50s rejects=%2d/34  %s'%(name,len(bad),' '.join(bad)))
print('commit names id in message (honest fixed):', sum(msg_names(i) for i in fixed),'/34')
print('rows per fixing commit (honest):', collections.Counter(commit_of(i)[:8] for i in fixed).most_common(5))
bad=[i for i in opn if x5 is not None and x5(i)]
print('X5 backticked-literal arm applied to OPEN rows: rejects=%d/15 %s'%(len(bad),' '.join(bad)))
