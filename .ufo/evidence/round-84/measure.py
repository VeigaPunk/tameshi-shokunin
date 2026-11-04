#!/usr/bin/env python3
"""R84 frozen public-CLI counter; does not import the instrument."""
import argparse,json,os,pathlib,subprocess,tempfile,shutil
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--rev',required=True);p.add_argument('--work',required=True);a=p.parse_args()
repo=str(pathlib.Path(a.repo).resolve());work=pathlib.Path(a.work);work.mkdir(parents=True,exist_ok=True)
s=pathlib.Path(tempfile.mkdtemp(prefix='identity-',dir=work))
try:
 rev=subprocess.check_output(['git','-C',repo,'rev-parse',a.rev+'^{commit}'],text=True).strip()
 tool=s/'defect-bind.py';tool.write_bytes(subprocess.check_output(['git','-C',repo,'show',rev+':tools/defect-bind.py']))
 cases=[('array',[]),('object',{}),('null',None),('integer',7),('boolean',True),('empty',''),('internal-newline','x\nDEFECT_BIND: rows=0 closed=0 open=0 unexpected=0'),('trailing-newline','x\n'),('valid','safe-id_1.2')]
 passed=0;invalid_refused=0
 for name,ident in cases:
  man=s/(name+'.json');man.write_text(json.dumps({'schema':'tameshi-defect-bind-v1','rows':[{'id':ident,'kind':'tree-paths','rev':rev,'paths':['SKILL.md']}]}))
  r=subprocess.run(['python3','-I','-X','utf8',str(tool),'--repo',repo,'--manifest',str(man)],capture_output=True,text=True)
  invalid=name!='valid'
  ok=(r.returncode==2 and not r.stdout and 'row-id-alphabet:' in r.stderr and 'Traceback' not in r.stderr) if invalid else (r.returncode==0 and 'DEFECT_BIND: rows=1 closed=1 open=0 unexpected=0' in r.stdout)
  passed+=ok;invalid_refused+=bool(ok and invalid)
  print('CASE',name,'exit='+str(r.returncode),'ok='+str(bool(ok)).lower(),'stdout='+repr(r.stdout),'stderr='+repr(r.stderr))
 print('IDENTITY_CALIBRATION: cases=9 invalid_refused=%d valid_accepted=%d mismatches=%d R84_C1_PASS=%s'%(invalid_refused,passed-invalid_refused,9-passed,str(passed==9).lower()))
 raise SystemExit(0 if passed==9 else 1)
finally:shutil.rmtree(s)
