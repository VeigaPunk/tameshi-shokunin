import hashlib, json, os, pathlib, subprocess
S=pathlib.Path('/fast/scratch/hyaku/tameshi-r58/T58W2Read13')
C=S/'clone'
records=[]
def run(args):
 p=subprocess.run(args,cwd=C,env={**os.environ,'TMPDIR':str(S)},text=True,capture_output=True)
 r={'command':subprocess.list2cmdline(args),'cwd':str(C),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}; records.append(r)
 print(json.dumps(r)); return p
run(['git','-C',str(C),'rev-parse','HEAD'])
run(['git','-C',str(C),'diff','2a32aa8228d5f86a85c81a923a3148bf792a9538','8063d0a551fc5b3cb5a2d397da7353af53444534','--','SKILL.md','tools/context-capture.py'])
tool=str(C/'tools/context-capture.py'); receipt=C/'.ufo/evidence/round-14/context-receipt.json'; neg=C/'.ufo/evidence/round-14/context-missing-env.json'
for name in ['.ufo/evidence/round-14/capture-context.py','.ufo/evidence/round-14/context-receipt.json','.ufo/evidence/round-14/context-missing-env.json']:
 run(['sha256sum',str(C/name)])
run(['python3',tool,'--check','--json'])
run(['python3',tool,'--selftest'])
expected={'schema':'tameshi-context-expected-v1','receipt_sha256':hashlib.sha256(neg.read_bytes()).hexdigest(),'id':'missing_injected_environment','exit':1}
(S/'expected.json').write_text(json.dumps(expected))
run(['python3',tool,'--check','--receipt',str(neg),'--expected',str(S/'expected.json'),'--json'])
for name,data in [('duplicate',b'{"schema":1,"schema":2}'),('wrongtype',b'[]'),('nonutf8',b'\xff'),('edited',receipt.read_bytes()+b' '),('absent',None)]:
 path=S/(name+'.json')
 if data is not None: path.write_bytes(data)
 expected={'schema':'tameshi-context-expected-v1','receipt_sha256':hashlib.sha256(data or b'').hexdigest(),'id':'context_consistent','exit':0}
 if name=='edited': expected['receipt_sha256']=hashlib.sha256(receipt.read_bytes()).hexdigest()
 (S/'expected.json').write_text(json.dumps(expected))
 run(['python3',tool,'--check','--receipt',str(path),'--expected',str(S/'expected.json'),'--json'])
run(['python3',tool,'--check','--unknown'])
for name in ['.ufo/evidence/round-14/capture-context.py','.ufo/evidence/round-14/context-receipt.json','.ufo/evidence/round-14/context-missing-env.json']:
 run(['sha256sum',str(C/name)])
r=json.loads((C/'.ufo/evidence/round-15/verification-3.json').read_text())
print('retained verification:',json.dumps({'checks':len(r['checks']),'failed_checks':r.get('failed_checks'),'all_checks_passed':all(x['passed'] for x in r['checks'])}))
(S/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
