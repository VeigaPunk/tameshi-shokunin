#!/usr/bin/env python3
"""Read-only recipe replay; all generated data below explicit --work (TMPDIR honored)."""
import argparse, ast, hashlib, json, os, pathlib, shutil, subprocess, time
p=argparse.ArgumentParser(); p.add_argument('--skill',required=True); p.add_argument('--target',required=True); p.add_argument('--work',required=True); p.add_argument('--kind',choices=['js','bash'],required=True); p.add_argument('--check',action='store_true'); p.add_argument('--run',action='store_true'); a=p.parse_args()
w=pathlib.Path(a.work); w.mkdir(parents=True,exist_ok=True); (w/'evidence').mkdir(exist_ok=True)
target=pathlib.Path(a.target); ext='mjs' if a.kind=='js' else 'sh'; pristine=w/('pristine.'+ext)
if not pristine.exists(): shutil.copy2(target,pristine)
data=pristine.read_text(); skill=pathlib.Path(a.skill).read_text(); var='MANIFEST' if a.kind=='js' else 'SPECS'; start=skill.index(var+' = ['); end=skill.index('\n```',start); manifest=ast.literal_eval(ast.parse(skill[start:end]).body[0].value)
for did,site,old,new in manifest:
    count=data.count(old); line=data[:data.index(old)].count('\n')+1 if count else None
    print(f'{did} count={count} first-line={line} expect={"survived" if did in ("D2","D10","B5","B10") else "killed"}')
    assert count==1 and new!=old
print('CHECK: all unique')
if a.check: raise SystemExit(0)
assert a.run
before=(hashlib.sha256(target.read_bytes()).hexdigest(),target.stat().st_size,target.stat().st_mtime_ns)
env=os.environ.copy(); env['TMPDIR']=env.get('TMPDIR',str(w)); env['THE_JANITOR_BIN']=str(w/'handler-deliberately-absent'); results=[]
for did,site,old,new in [('CONTROL','',None,None)]+manifest:
    mutant=pristine if old is None else w/('mutant-'+did+'.'+ext)
    if old is not None:
        mutant.write_text(data.replace(old,new,1)); assert hashlib.sha256(mutant.read_bytes()).digest()!=hashlib.sha256(pristine.read_bytes()).digest()
    cmd=['node' if a.kind=='js' else 'bash',str(mutant),'--selftest']; t=time.monotonic(); r=subprocess.run(cmd,cwd=w,env=env,capture_output=True,text=True,timeout=300 if a.kind=='js' else 280)
    output=r.stdout+r.stderr; (w/'evidence'/(did+'.selftest.txt')).write_text(output)
    summary=[x for x in output.splitlines() if 'SELFTEST:' in x or 'VERDICT:' in x]; fails=[x for x in output.splitlines() if 'bad-case' in x or x.lstrip().startswith('FAIL') or x.lstrip().startswith('not ok')]
    enumerated=('/43' in output) if a.kind=='js' else (sum(x.startswith(('ok-case','bad-case','skip-case')) for x in output.splitlines())==16)
    green=r.returncode==0 and ('VERDICT: PASS' in output if a.kind=='js' else 'SELFTEST: PASS (16 cases)' in output)
    verdict='survived' if green else ('killed' if enumerated else 'inconclusive')
    row={'id':did,'command':cmd,'exit':r.returncode,'summary':summary,'verdict':verdict,'duration_s':round(time.monotonic()-t,3),'sha256':hashlib.sha256(mutant.read_bytes()).hexdigest(),'fails':fails,'enumerated':enumerated}; results.append(row)
    (w/'evidence'/(did+'.meta.json')).write_text(json.dumps(row,indent=2)); print(json.dumps(row))
    if did=='CONTROL': assert green,'red control: no denominator'
    assert enumerated
assert before==(hashlib.sha256(target.read_bytes()).hexdigest(),target.stat().st_size,target.stat().st_mtime_ns)
assert pristine.read_bytes()==target.read_bytes(); print('RESTORE: sha256/size/mtime unchanged; pristine cmp-identical')
print('RESULT: killed=%d survived=%d inconclusive=%d'%tuple(sum(r['verdict']==v for r in results[1:]) for v in ('killed','survived','inconclusive')))
(w/'evidence'/'results.json').write_text(json.dumps(results,indent=2))
