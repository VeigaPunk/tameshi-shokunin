#!/usr/bin/env python3
"""Score the committed base plus the frozen instruments; no claimed content is applied."""
import json,os,pathlib,shutil,subprocess
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin');S=pathlib.Path('/fast/scratch/hyaku/tameshi-r58/l1-before');B='2a32aa8228d5f86a85c81a923a3148bf792a9538';E='.ufo/evidence/round-58';O=L/E/'before';O.mkdir(exist_ok=True)
S.mkdir(parents=True,exist_ok=True);env=dict(os.environ,TMPDIR=str(S),GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1')
def git(*a):return subprocess.run(['git',*a],capture_output=True,text=True,env=env,check=True)
try:
 C=S/'clone';git('clone','--shared','-q',str(L),str(C));git('-C',str(C),'checkout','--detach','-q',B)
 assert pathlib.Path(git('-C',str(C),'rev-parse','--show-toplevel').stdout.strip())==C
 for k in ['c1','c2']:shutil.copytree(L/E/k,C/E/k,dirs_exist_ok=True)
 git('-C',str(C),'add',E);git('-C',str(C),'-c','user.name=fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','BASE plus frozen round-58 instruments only')
 rev=git('-C',str(C),'rev-parse','HEAD').stdout.strip()
 for k in ['c1','c2']:
  args=['python3','-I',str(C/E/k/'measure.py'),'--lane',str(C),'--rev',rev,'--work',str(S/('work-'+k)),'--explain']
  r=subprocess.run(args,capture_output=True,text=True,env=env)
  # Receipt makes clone-only identity explicit; never relabel it as a lane measurement.
  (O/(k+'.stdout')).write_text(r.stdout.replace(' rev=', ' clone_rev='));(O/(k+'.stderr')).write_text(r.stderr);(O/(k+'.exit')).write_text(str(r.returncode)+'\n')
  print(k,r.returncode,r.stdout.splitlines()[-1] if r.stdout else r.stderr)
 (O/'invocation.json').write_text(json.dumps({'base':B,'overlay':'only c1 and c2 frozen instruments; no ledger or registry patch','clone_rev':rev,'commands':'python3 -I COUNTER --lane CLONE --rev CLONE_REV --work EMPTY_DIR --explain'},indent=1)+'\n')
finally:shutil.rmtree(S,ignore_errors=True)
