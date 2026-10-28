import importlib.util, subprocess, json, glob, os, hashlib, collections, re
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
W3=LANE+'/.ufo/waves/round-55/w3'
W2=LANE+'/.ufo/waves/round-55/w2'
C0='9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
spec=importlib.util.spec_from_file_location('m18',LANE+'/.ufo/evidence/round-18/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=subprocess.run(['git','-C',LANE,'cat-file','blob',C0+':SKILL.md'],capture_output=True,check=True).stdout
secs=m.sectionize(raw)
by={s['heading']:s for s in secs}
sha2head={s['sha256']:s['heading'] for s in secs}
# expected heading per seat from spec
sp=json.load(open(LANE+'/.ufo/waves/round-55/spec-w3.json'))
exp={}
for it in sp['items']:
    n=it['name']
    if n.startswith('T55W3R') and n[7:].isdigit():
        txt=it['item']
        mm=re.match(r'.*?`(#{1,3} [^`]+)`', txt)
        exp[n]=mm.group(1)
rows=[]
seen=collections.defaultdict(list)
for n in sorted(exp):
    cands=[p for p in (f'{W3}/{n}.json', f'{W2}/{n}.json') if os.path.exists(p)]
    if not cands:
        rows.append({'seat':n,'status':'MISSING','expected':exp[n]}); continue
    if len(cands)>1:
        rows.append({'seat':n,'status':'BOTH-LOCATIONS','expected':exp[n],'paths':cands})
    p=cands[0]
    try:
        d=json.load(open(p))
    except Exception as e:
        rows.append({'seat':n,'status':'BAD-JSON:'+str(e),'path':p}); continue
    h=d.get('heading'); sha=d.get('section_sha256'); cand=d.get('cand'); f=d.get('findings')
    got=by.get(h)
    ok_sha = bool(got) and sha==got['sha256']
    ok_cand = cand==C0
    ok_head_exp = h==exp[n]
    ok_f = isinstance(f,list) and all(isinstance(x,dict) and isinstance(x.get('quote'),str) and isinstance(x.get('why'),str) for x in f)
    sha_owner = sha2head.get(sha,'<no-section-matches>')
    seen[h].append(n)
    rows.append({'seat':n,'status':'OK' if (ok_sha and ok_cand and ok_head_exp and ok_f) else 'DEFECT',
                 'path':os.path.relpath(p,LANE),'expected':exp[n],'heading':h,'sha':sha,
                 'c0sha':(got or {}).get('sha256'),'sha_ok':ok_sha,'cand_ok':ok_cand,
                 'heading_matches_assignment':ok_head_exp,'findings_ok':ok_f,'findings_n':len(f) if isinstance(f,list) else None,
                 'sha_owner':sha_owner})
dups={h:v for h,v in seen.items() if len(v)>1}
print(json.dumps({'rows':rows,'dups':dups},indent=1,ensure_ascii=False))
