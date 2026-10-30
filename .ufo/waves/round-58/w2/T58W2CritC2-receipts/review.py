import concurrent.futures, hashlib, json, os, subprocess, sys, ast
from pathlib import Path
S=Path('/fast/scratch/hyaku/tameshi-r58/T58W2CritC2')
C=S/'clone'
R=Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2CritC2-receipts')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(S),GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1')
rows=[r for r in json.loads((C/'tools/registry.json').read_text())['rows'] if r['kind']=='gate' and r['argv'][1]=='tools/receipt-revision-gate.py']
def run(row):
    cmd=['python3',str(C/'tools/registry-check.py'),'--root',str(C),'--only',row['name'],'--json']
    p=subprocess.run(cmd,cwd=S,env=env,capture_output=True,text=True)
    record={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expect':row['expect']}
    (R/(row['name']+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record),flush=True)
    return record
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    results=list(ex.map(run,rows))
(R/'rows.json').write_text(json.dumps(results,indent=2)+'\n')
# Extract only literal cheat payloads from wave-one artifact; never execute its driver.
source=Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/attack.py').read_text()
mod=ast.parse(source)
payloads={n.targets[0].id:ast.literal_eval(n.value) for n in mod.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('CHEAT_GATE','BENT_RC')}
import importlib.util
mp=C/'.ufo/evidence/round-58/c2/measure.py'
spec=importlib.util.spec_from_file_location('frozen_c2',mp); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# build_lane owns isolated fixture creation, verifies toplevel before commits, uses fixture identity.
parent=S/'forgery'; parent.mkdir()
lane,head=m.build_lane(parent,'lane',payloads['CHEAT_GATE'],payloads['BENT_RC'],mutants_text=(C/m.MUTANTS_PATH).read_text())
cmd=['python3',str(mp),'--lane',lane,'--rev',head,'--work',str(S/'forgery-counter'),'--explain']
p=subprocess.run(cmd,cwd=S,env=env,capture_output=True,text=True)
record={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
print(json.dumps(record),flush=True)
(R/'forgery-counter.json').write_text(json.dumps(record,indent=2)+'\n')
# Same fixture, trusted C0 executor, exposing actual semantic failure.
checks=[]
for name in ('c2-fx-ok','c2-fx-drift','c2-fx-unresolvable'):
    cmd=['python3',str(C/'tools/registry-check.py'),'--root',lane,'--only',name,'--json']
    p=subprocess.run(cmd,cwd=S,env=env,capture_output=True,text=True)
    checks.append({'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
print(json.dumps(checks),flush=True)
(R/'forgery-real-executor.json').write_text(json.dumps(checks,indent=2)+'\n')
