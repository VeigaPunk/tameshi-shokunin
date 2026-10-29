"""Candidate extra arms, evaluated on the HONEST ledger (current working tree) and the honest defects set.
Read-only: git objects of the lane only. Prints per-arm false-rejects on the honest fixed rows (34) and open rows (15)."""
import json,subprocess,re,posixpath,os,collections
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; BASE='5e3569969b532310d2b8a3d130901757a3df356b'
D=json.load(open(LANE+'/.ufo/evidence/round-57/c1/defects.json'))['defects']
DD={d['id']:d for d in D}
H={r['id']:r for r in json.load(open(LANE+'/corpus/routed-defects.json'))['defects'] if r['id'] in DD}
SPOT={d['file'] for d in D}; LEDGER='corpus/routed-defects.json'; PANEL='.ufo/evidence/round-57/c1/panel.json'
HARD=('.ufo/evidence/round-57/c1/','.ufo/evidence/round-57/control/','.ufo/evidence/round-57/contract.json','.ufo/evidence/round-57/freeze.json')
def g(*a): return subprocess.run(['git','-C',LANE]+list(a),capture_output=True)
def exists_at(rev,p): return g('cat-file','-e','%s:%s'%(rev,p)).returncode==0
def canon(p): return posixpath.normpath(p)
fixed=[i for i in H if H[i]['status']=='fixed']; opn=[i for i in H if H[i]['status']=='open']; dec=[i for i in H if H[i]['status']=='declined']
print('honest: fixed=%d open=%d declined=%d'%(len(fixed),len(opn),len(dec)))
res=collections.OrderedDict()
def arm(name,fn,pool):
    bad=[i for i in pool if fn(i)]
    res[name]=(len(bad),bad)
ev_paths=lambda i:[e['path'] for e in H[i]['evidence']]
# X1 canonical path form
arm('X1 reject non-canonical paths (./, //, ..)', lambda i: any(p!=canon(p) or p.startswith('./') for p in ev_paths(i)), fixed)
arm('X1 (open rows)', lambda i: any(p!=canon(p) or p.startswith('./') for p in ev_paths(i)), opn)
# X2 reject self-citation of ledger / spot-check / panel / HARD after canonicalisation
arm('X2 canonical self-cite + HARD exclusion', lambda i: any((canon(p)==LEDGER or canon(p) in SPOT or canon(p)==PANEL or canon(p).startswith(HARD)) for p in ev_paths(i)), fixed)
arm('X2 (open rows)', lambda i: any((canon(p)==LEDGER or canon(p) in SPOT or canon(p)==PANEL or canon(p).startswith(HARD)) for p in ev_paths(i)), opn)
# X3 at least one fixing evidence path must exist at routed_at (not a file created after routing)
def x3(i):
    ra=DD[i]['routed_at']
    return not any(exists_at(ra,canon(p)) for p in ev_paths(i))
arm('X3 need an evidence path that existed at routed_at', x3, fixed)
# X4 fixing evidence path must be named by item text (drop the commit-message-names-id OR)
def x4(i):
    t=DD[i]['text']+' '+DD[i].get('extended_text','')
    return not any(p in t or posixpath.basename(p) in t for p in ev_paths(i))
arm('X4 evidence path must be named by item text (drop names-id OR)', x4, fixed)
# X5 excerpt must carry a backticked literal of the item text (not just a key)
def lits(i):
    t=DD[i]['text']+' '+DD[i].get('extended_text','')
    return [m for m in re.findall(r'`([^`]{3,})`',t)]
def x5(i):
    L=lits(i)
    if not L: return False  # no literal to demand: item not judged by this arm
    return not any(any(l in e['excerpt'] for l in L) for e in H[i]['evidence'])
arm('X5 excerpt must contain a backticked literal of item text', x5, fixed)
# X6 at least two distinct evidence items per fixed row
arm('X6 >=2 evidence items per fixed row', lambda i: len(H[i]['evidence'])<2, fixed)
# X7 open cap (count) : honest open rows = len(opn); a cap of 17 rejects nothing on fixed rows
print('X7 open cap 17: honest open=%d -> over cap by %d; fixed rows rejected: 0'%(len(opn),max(0,len(opn)-17)))
for k,(n,bad) in res.items():
    print('%-62s rejects=%2d/%d  %s'%(k,n,len(fixed) if 'open rows' not in k else len(opn), ' '.join(bad[:12])))
