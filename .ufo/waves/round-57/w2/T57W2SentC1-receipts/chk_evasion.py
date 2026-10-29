"""T57W2SentC1 receipt: in-process check_evidence probes of the leading-./ bypass (report section 2).
Runs against the scratch clone's HEAD (instrument copy present). Usage: chk_evasion.py CLONE_DIR (default: the attack clone)."""
import sys,importlib.util,os,subprocess
CL=sys.argv[1] if len(sys.argv)>1 else '/fast/scratch/hyaku/tameshi-r57/T57W2SentC1/a/clone'
SRC=sys.argv[2] if len(sys.argv)>2 else '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/measure.py'
spec=importlib.util.spec_from_file_location('m',SRC); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def g(*a): return subprocess.run(['git','-C',CL]+list(a),capture_output=True)
rev=g('rev-parse','HEAD').stdout.decode().strip()
import json
defects=json.loads(g('show','%s:.ufo/evidence/round-57/c1/defects.json'%rev).stdout.decode())['defects']
spot={d['file'] for d in defects}
def find(path,needle):
    L=g('show','%s:%s'%(rev,path)).stdout.decode('utf-8','replace').split('\n')
    for i,l in enumerate(L,1):
        if needle in l: return i,' '.join(l.split())
    raise SystemExit('needle not found: %s %s'%(path,needle))
cases=[
 ('.ufo/evidence/round-57/c1/measure.py','PANEL_ALLOWED = 5',['PANEL_ALLOWED']),
 ('./.ufo/evidence/round-57/c1/measure.py','PANEL_ALLOWED = 5',['PANEL_ALLOWED']),
 ('.ufo/evidence/round-57/c1/defects.json','fixture-shrinking-pilot',['S022']),
 ('./.ufo/evidence/round-57/c1/defects.json','fixture-shrinking-pilot',['S022']),
 ('corpus/routed-defects.json','"note"',['S022']),
 ('./corpus/routed-defects.json','"note"',['S022']),
 ('corpus/lessons/round-50-verifier-spotcheck.md','S022 status contradicts',['S022']),
 ('./corpus/lessons/round-50-verifier-spotcheck.md','S022 status contradicts',['S022']),
 ('CORPUS/lessons/round-50-verifier-spotcheck.md','S022 status contradicts',['S022']),
]
for path,needle,keys in cases:
    base=path[2:] if path.startswith('./') else path
    try:
        n,l=find(base if g('cat-file','-e','%s:%s'%(rev,base)).returncode==0 else path,needle)
    except SystemExit:
        n,l=1,needle
    item={'path':path,'lines':'%d-%d'%(n,n),'excerpt':l[:400]}
    why=m.check_evidence(CL,rev,item,keys,spot,{})
    print('%-58s line %-4d %s'%(path,n,'ACCEPTED' if why is None else 'refused: '+why))
