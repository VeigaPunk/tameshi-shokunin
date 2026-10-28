import importlib.util, json, os, re, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
HEADS=json.loads((LANE/'.ufo/evidence/round-56/c1/lost-headings-at-base.json').read_text())
ENV={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1')
CLONE=Path(sys.argv[1]); WORK=Path(sys.argv[2])
def git(*a):
    r=subprocess.run(['git','-C',str(CLONE)]+list(a),env=ENV,capture_output=True,text=True)
    if r.returncode: raise SystemExit('git %s: %s'%(' '.join(a),r.stderr))
    return r.stdout
def commit(m):
    git('add','-Af'); git('-c','user.name=w','-c','user.email=w@x.invalid','commit','-q','-m',m)
    return git('rev-parse','HEAD').strip()
def show(rev,p):
    r=subprocess.run(['git','-C',str(CLONE),'show','%s:%s'%(rev,p)],env=ENV,capture_output=True)
    return r.stdout if r.returncode==0 else None
def secs(rev):
    p=WORK/('r18-%s.py'%rev[:12]); p.write_bytes(show(rev,'.ufo/evidence/round-18/measure.py'))
    sp=importlib.util.spec_from_file_location('r'+rev[:12],str(p)); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return {s['heading']:s for s in m.sectionize(show(rev,'SKILL.md'))}
def slug(h): return re.sub(r'[^A-Za-z0-9]+','-',h.strip('# ')).strip('-')[:40]
def reports(cand,S,rot=None):
    d=CLONE/'.ufo/waves/round-56/w2'
    if d.exists():
        for p in d.iterdir(): p.unlink()
    d.mkdir(parents=True,exist_ok=True)
    for i,h in enumerate(HEADS):
        s=S[h]; cmd="git -C . show %s:SKILL.md | sed -n '%d,%dp'"%(cand,s['start'],s['end'])
        sh=S[HEADS[(i+1)%len(HEADS)]]['sha256'] if (rot and h in rot) else s['sha256']
        stem='T56W2Read-%02d-%s'%(i,slug(h))
        (d/(stem+'.json')).write_text(json.dumps({'heading':h,'cand':cand,'section_sha256':sh,
            'findings':['read'],'commands':[cmd]},indent=1)+'\n')
        (d/(stem+'.md')).write_text('# %s\n\n    %s\n'%(h,cmd))
base=git('rev-parse','HEAD').strip()
S=secs(base)
rekey=CLONE/('.ufo/evidence/round-21/coldread/rekey-r56-'+base[:12]+'/traces')
rekey.mkdir(parents=True,exist_ok=True); (rekey/'readers.json').write_text('{}\n')
reports(base,S); good=commit('reports+rekey (all valid)')
def c1(rev,tag):
    w=WORK/tag; w.mkdir(parents=True,exist_ok=True)
    r=subprocess.run([sys.executable,str(LANE/'.ufo/evidence/round-56/c1/measure.py'),
        '--lane',str(CLONE),'--rev',rev,'--work',str(w),'--explain'],capture_output=True,text=True)
    print('--- C1 %s rev=%s rc=%d'%(tag,rev[:12],r.returncode))
    for l in (r.stdout+r.stderr).splitlines():
        if l.startswith('EXPLAIN arm') or l.startswith('C1_R56'):
            print(l)
c1(good,'c1-good')
reports(base,S,rot={'## Standing rules'}); bad=commit('one rotated hash')
c1(bad,'c1-bad')
