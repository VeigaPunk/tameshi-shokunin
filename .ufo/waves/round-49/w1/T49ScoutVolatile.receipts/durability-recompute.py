import importlib.util,json,subprocess,sys,hashlib
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; B='8ca67421111fa354b47b803358391d0b07fc6db9'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('m18',L+'/.ufo/evidence/round-18/measure.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
LED='.ufo/evidence/round-21/coldread/ledger.json'
m.IGNORED_INPUTS=m.IGNORED_INPUTS|frozenset((LED,))
git=lambda *a:subprocess.run(['git','-C',L,*a],capture_output=True,check=True).stdout
skill=git('show',B+':SKILL.md'); led=json.loads(git('show',B+':'+LED))
VOL=['LOG.md','SCORECARD.md','corpus/SOURCES.md','corpus/QUALITY.md','corpus/README.md']
secs=m.sectionize(skill)
by={}
for e in led['entries']: by.setdefault(e.get('sha256'),[]).append(e)
out=[]
for s in secs:
    rows=[]
    for e in by.get(s['sha256'],[]):
        r=m.entry_reason(L,B,e,True)
        view=m.inputs_view(e)
        rows.append(dict(credits=r is None,reason=r,inputs=sorted(view or {}),vol=[v for v in VOL if v in (view or {})],
          stale=m.entry_is_stale(L,B,e),failing=m.entry_failure(e) is not None,cls=e.get('class'),rr=e.get('read_rev','')[:8],ntr=len(e.get('traces',[]))))
    cred=[r for r in rows if r['credits']]
    out.append(dict(start=s['start'],heading=s['heading'],n=len(rows),credited_entries=len(cred),
      covered=bool(cred) and not any(r['failing'] and not r['stale'] for r in rows),
      durable=[r for r in cred if not r['vol']].__len__(),
      volatile_only=bool(cred) and all(r['vol'] for r in cred),
      cred=cred))
json.dump(out,open(sys.argv[1],'w'),indent=1)
print('ignored',sorted(m.IGNORED_INPUTS))
cov=[o for o in out if o['covered']]
print('covered',len(cov),'of',len(out))
print('covered with zero volatile-free crediting entry:',[ (o['start'],o['heading']) for o in cov if o['durable']==0])
print('covered sections whose every crediting entry lists a record file (volatile_only):',sum(o['volatile_only'] for o in cov))
print('covered with some crediting entry listing a record file:',sum(any(r['vol'] for r in o['cred']) for o in cov))
for o in out:
    if not o['covered']: print('UNCOVERED',o['start'],o['heading'][:60],o['n'],o['credited_entries'],o['durable'])
