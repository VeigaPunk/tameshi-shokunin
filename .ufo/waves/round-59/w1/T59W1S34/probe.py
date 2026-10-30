import hashlib, json, os, pathlib, shutil, subprocess, sys
S=pathlib.Path('/fast/scratch/hyaku/tameshi-r59/T59W1S34')
O=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-59/w1/T59W1S34')
R=S/'repo'; R.mkdir()
os.environ['TMPDIR']=str(S)
os.environ['GIT_CONFIG_GLOBAL']='/dev/null'; os.environ['GIT_CONFIG_NOSYSTEM']='1'
def run(cmd, **kw):
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=90,**kw)
    return {'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def git(*args, input=None):
    r=run(['git','-C',str(R),*args],input=input)
    if r['exit']: raise RuntimeError(r)
    return r['stdout'].strip()
r=run(['git','-C',str(R),'init','-q']); assert r['exit']==0
assert git('rev-parse','--show-toplevel')==str(R)
# Each write below has an asserted explicit scratch repository root.
def tree(mode, oid):
    return git('mktree',input=f'{mode} blob {oid}\trunner.py\n')
def commit(t):
    return git('-c','user.name=fixture','-c','user.email=fixture@example.invalid','commit-tree',t,input='fixture\n')
blob=git('hash-object','-w','--stdin',input='target.py')
trusted=commit(tree('120000',blob))
candidate=commit(tree('100644',blob))
# Control lane revision need not contain a candidate tool: --tool is explicitly a control.
rev=candidate
measure=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-59/measure.py')
shutil.copyfile(measure,S/'measure.py')
model=S/'model.py'; pristine=model.read_bytes()
def sha(b): return hashlib.sha256(b).hexdigest()
results={'axes':['contract correctness','counter discrimination','exact restoration'],'model_only':True,'trusted':trusted,'candidate':candidate,'blob':blob,'tree_entries':{'trusted':git('ls-tree',trusted),'candidate':git('ls-tree',candidate)},'runs':[]}
try:
    for phase in ['pristine','mutated','restored']:
        if phase=='mutated':
            b=pristine.replace(b"t is None or t[0] not in (b'100644', b'100755') or t[1] != b'blob'",b"t is None or t[1] != b'blob'")
            assert b!=pristine
            model.write_bytes(b)
        if phase=='restored': model.write_bytes(pristine)
        shutil.copyfile(model,O/(phase+'-model.py'))
        work=S/('counter-'+phase)
        counter=run([sys.executable,'-I',str(S/'measure.py'),'--lane',str(R),'--rev',rev,'--work',str(work),'--tool',str(model)])
        attack=run([sys.executable,'-I',str(model),'--repo',str(R),'--trusted',trusted,'--candidate',candidate,'--path','runner.py'])
        results['runs'].append({'phase':phase,'sha256':sha(model.read_bytes()),'counter':counter,'trusted_symlink_attack':attack})
finally:
    model.write_bytes(pristine)
    results['restored_sha256']=sha(model.read_bytes())
    results['restored_exact']=model.read_bytes()==pristine
    (O/'receipts.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'runs':[{'phase':x['phase'],'sha256':x['sha256'],'counter_exit':x['counter']['exit'],'counter_summary':x['counter']['stdout'].splitlines()[-1],'attack':x['trusted_symlink_attack']} for x in results['runs']],'restored_exact':results['restored_exact']},indent=2))
