import os, subprocess, json
from pathlib import Path
ROOT=Path('/fast/scratch/hyaku/tameshi-r59/T59W1S57')
os.environ['TMPDIR']=str(ROOT)
repo=ROOT/'fixture'; repo.mkdir()
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_COUNT='0')
records=[]
def run(args, override=None):
 e=env.copy();e.update(override or {})
 p=subprocess.run(args,env=e,capture_output=True,text=True,timeout=15)
 records.append(dict(command=args,env_override=override,exit=p.returncode,stdout=p.stdout,stderr=p.stderr))
 return p
run(['git','-C',str(repo),'init','-q'])
assert run(['git','-C',str(repo),'rev-parse','--show-toplevel']).stdout.strip()==str(repo)
def git(*a):return run(['git','-C',str(repo),*a])
def commit():
 git('add','--all');git('-c','user.name=fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','fixture')
 return git('rev-parse','HEAD').stdout.strip()
(repo/'tools').mkdir();(repo/'tools/runner.py').write_text('print("trusted")\n');(repo/'-runner.py').write_text('minus\n')
trusted=commit(); (repo/'tools/runner.py').write_text('print("changed")\n');changed=commit()
git('replace',changed,trusted)
git('ls-tree','-z',changed,'--','tools/runner.py')
run(['git','--no-replace-objects','-C',str(repo),'ls-tree','-z',changed,'--','tools/runner.py'])
git('tag','ambiguous',trusted);git('branch','ambiguous',changed);git('rev-parse','--verify','--end-of-options','ambiguous^{commit}')
git('rev-parse','--verify','--end-of-options','--help^{commit}')
git('--literal-pathspecs','ls-tree','-z',trusted,'--','-runner.py')
git('config','filter.boundary.clean','/nonexistent-t59w1s57-filter')
git('config','filter.boundary.smudge','/nonexistent-t59w1s57-filter')
git('config','filter.boundary.required','true')
(repo/'.gitattributes').write_text('tools/runner.py filter=boundary\n')
git('cat-file','blob',trusted+':tools/runner.py')
run(['git','-C',str(repo),'rev-parse','--show-toplevel'],{'GIT_DIR':str(ROOT/'nonexistent')})
(ROOT/'fixture-info.json').write_text(json.dumps(dict(repo=str(repo),trusted=trusted,changed=changed)))
print(json.dumps(records,indent=2))
