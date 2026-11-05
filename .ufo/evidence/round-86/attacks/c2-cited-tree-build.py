import json, subprocess, sys
sys.path.insert(0, 'tools')
import importlib.util
spec = importlib.util.spec_from_file_location('cap', 'tools/capability-census.py')
cap = importlib.util.module_from_spec(spec); spec.loader.exec_module(cap)
rev = 'd10a9c66d6181cddcad52cdbffd672beb886ff6c'
text = subprocess.run(['git','show',rev+':SCORECARD.md'],capture_output=True,text=True).stdout
rows = cap.parse_rows(text)
cands = ['tools','.ufo','.ufo/evidence','corpus','.ufo/evidence/round-21','.ufo/evidence/round-73']
def kind(p):
    r = subprocess.run(['git','cat-file','-t',rev+':'+p],capture_output=True,text=True)
    return r.stdout.strip() if r.returncode==0 else None
out=[]
for r in rows:
    pick=None
    for c in cands:
        if kind(c)=='tree' and cap.is_cited(r['text'], c):
            pick=c; break
    out.append({'capability': r['name'], 'disposition':'historical', 'receipt':{'path':pick or 'tools','rev':rev}})
json.dump({'schema':'tameshi-capability-census-v1','note':'L1 independent A1c: every row historical, pinned to a CITED ancestor directory (tree)','rows':out}, open('/fast/scratch/hyaku/tameshi-r86/l1/a1c/manifest.json','w'), indent=1)
print('rows',len(out),'distinct pins',sorted({o['receipt']['path'] for o in out}))
