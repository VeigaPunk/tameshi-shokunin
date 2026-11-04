#!/usr/bin/env python3
"""Frozen R85-C1 counter; eight independently generated public CLI cases."""
import argparse, hashlib, os, pathlib, shutil, subprocess, sys
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); p.add_argument('--rev',required=True); p.add_argument('--work',required=True); p.add_argument('--control',choices=['accept'])
a=p.parse_args(); work=pathlib.Path(a.work); work.mkdir(parents=True,exist_ok=True)
if any(work.iterdir()): sys.exit('work must be empty')
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_AUTHOR_NAME='fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',GIT_COMMITTER_NAME='fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid')
def run(argv,**kw): return subprocess.run(argv,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kw)
def git(root,*args):
 r=run(['git','-C',str(root),*args]);
 if r.returncode: raise RuntimeError(r.stderr.decode())
 return r.stdout.decode().strip()
try:
 tool=work/'instrument.py'
 extracted=run(['git','-C',a.repo,'cat-file','blob',a.rev+':tools/design-blob-audit.py'])
 available=extracted.returncode==0
 tool.write_bytes(b"print('DESIGN_BLOB: receipts=1 carried=1 orphan=0')\n" if a.control else extracted.stdout)
 root=work/'fixture'; root.mkdir(); git(root,'init','-q'); git(root,'config','commit.gpgsign','false')
 assert pathlib.Path(git(root,'rev-parse','--show-toplevel')).resolve()==root.resolve()
 (root/'tools').mkdir(); (root/'tools/toy.py').write_bytes(b'print(1)\n'); git(root,'add','tools'); git(root,'commit','-qm','fixture regular'); base=git(root,'rev-parse','HEAD'); sha=hashlib.sha256(b'print(1)\n').hexdigest()
 (root/'link').symlink_to('tools/toy.py'); git(root,'add','link'); git(root,'commit','-qm','fixture symlink'); cand=git(root,'rev-parse','HEAD')
 def receipt(path='tools/toy.py',digest=sha): return '# design_base: '+base+'\n# design_tool: '+path+'\n# design_tool_sha256: '+digest+'\n# measured_bytes: worktree (uncommitted at design_base)\n'
 definitions=[('carried',receipt(),0,'state=carried'),('different',receipt(digest='0'*64),1,'state=different'),('absent',receipt(path='missing.py'),1,'state=absent'),('symlink',receipt(path='link'),1,'state=nonregular'),('malformed',receipt(digest='bad'),2,''),('ghost',receipt(),2,''),('mixed',receipt()+'# measured_rev: '+base+'\n# tool: tools/toy.py\n# tool_sha256: '+sha+'\n',2,''),('zero','plain text\n',2,'')]
 passed=0
 for name,text,code,token in definitions:
  d=root/name; d.mkdir(); (d/'receipt.txt').write_text(text); git(root,'add',name); git(root,'commit','-qm','fixture '+name); rr=git(root,'rev-parse','HEAD')
  args=[sys.executable,'-I',str(tool),'--repo',str(root),'--receipt-rev',rr,'--root',name,'--candidate-rev',('0'*40 if name=='ghost' else cand)]
  r=run(args); out=r.stdout.decode(errors='replace'); ok=(available or bool(a.control)) and r.returncode==code and (not out if code==2 else token in out and 'DESIGN_BLOB: receipts=1 carried='+('1 orphan=0' if code==0 else '0 orphan=1') in out)
  passed+=bool(ok); print('CASE %s exit=%d expected=%d ok=%s stdout=%r stderr=%r'%(name,r.returncode,code,str(bool(ok)).lower(),out,r.stderr.decode(errors='replace')))
 print('DESIGN_CAPABILITY: cases=8 passed=%d mismatches=%d R85_C1_PASS=%s'%(passed,8-passed,str(passed==8).lower()))
 sys.exit(0 if passed==8 else 1)
finally:
 shutil.rmtree(work)
