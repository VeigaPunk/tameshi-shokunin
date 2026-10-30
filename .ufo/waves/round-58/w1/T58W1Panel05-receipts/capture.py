import os, pathlib, subprocess, concurrent.futures, json
C='/fast/scratch/hyaku/tameshi-r58/T58W1Panel05/clone'
R=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel05-receipts')
BASE='2a32aa8228d5f86a85c81a923a3148bf792a9538'
def run(name,args,env=None):
 p=subprocess.run(args,cwd=C,env=env,capture_output=True,text=True)
 text='$ '+ ' '.join(args)+'\nexit='+str(p.returncode)+'\nstdout:\n'+p.stdout+'stderr:\n'+p.stderr
 (R/(name+'.txt')).write_text(text)
 print(name+': '+text)
 return p
jobs=[]
def git(name,*args): jobs.append((name,['git','-C',C,*args],None))
git('base','rev-parse','HEAD')
git('r533-control-tree','ls-tree','-r',BASE,'--',C+'/.ufo/evidence/round-53/control')
git('r533-control-tally','show',BASE+':.ufo/evidence/round-53/control/controls.stdout')
git('r534-original','show',BASE+':.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/c2-counter-repaired.stdout')
git('r534-object','rev-parse','--verify','9c6ef7bc80c0^{commit}')
git('r535-original','show',BASE+':.ufo/evidence/round-53/verify-freeze.stdout')
git('r535-freeze-history','log','--format=%H %s','--',C+'/.ufo/evidence/round-53/verify-freeze.stdout')
git('r536-initial-fix','show','59c38109bf119d0e9d4f878644a82babc937bc1e','--',*[C+'/tools/'+f+'.py' for f in ['bash-witness-study','env-diff','evidence-disposition','pin-disposition']])
git('r536-completion','show','99c3bc88d704566197783f66b211ee0a830e0330','--',C+'/tools/env-diff.py')
git('r536-ancestor','merge-base','--is-ancestor','99c3bc88d704566197783f66b211ee0a830e0330',BASE)
for tool,args in [('bash-witness-study',['selftest']),('env-diff',['--selftest']),('evidence-disposition',['--selftest']),('pin-disposition',['--selftest'])]:
 env=dict(os.environ,TMPDIR='/fast/scratch/hyaku/tameshi-r58/T58W1Panel05/DOES_NOT_EXIST',PYTHONDONTWRITEBYTECODE='1')
 jobs.append(('r536-probe-'+tool,['python3',C+'/tools/'+tool+'.py',*args],env))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 list(ex.map(lambda a:run(*a),jobs))
