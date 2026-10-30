import hashlib, importlib.util, json, os, pathlib, re, shutil, subprocess
lane=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
clone=pathlib.Path('/fast/scratch/hyaku/tameshi-r57/T57W3Read11/clone')
rev='adf87899c70d616140a81185a8f9acbbdfb30392'
spec=importlib.util.spec_from_file_location('frozen',lane/'.ufo/evidence/round-18/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=subprocess.check_output(['git','-C',str(lane),'show',rev+':SKILL.md'])
sec=next(s for s in m.sectionize(raw) if s['heading']=='### Round-13 gate/probe registry')
print(sec['start'],sec['end'],sec['sha256'])
paths=['tools/pin-disposition.py','tools/witness-metadata.py','.ufo/evidence/round-13/pin-manifest.json','.ufo/evidence/round-13/witness-metadata.json','.ufo/evidence/round-13/expected.json','.ufo/evidence/round-12/BashWitness/summary.json','.ufo/evidence/round-12/BashWitness/declaration.json','.ufo/evidence/round-12/BashWitness/declared.tsv','.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json']
for p in paths:
 assert (clone/p).is_file(),p
 print('POINTER_OK',p)
text=raw.decode()
assert '## Seventh recorded case and full-page cold-read — round 16' in text
print('HEADING_POINTER_OK seventh recorded case')
sources=(clone/'corpus/SOURCES.md').read_text()
for source in ['S047','S048','S266']:
 row=next(line for line in sources.splitlines() if line.startswith('| '+source+' |'))
 print('SOURCE_ROW',row)
pit=(clone/'.ufo/evidence/round-48/freshness/sources/S048.html').read_text()
for line in pit.splitlines():
 if 'priorit' in line.lower() or 'not yet implemented' in line.lower(): print('PIT_SNAPSHOT',line)
summary=json.loads((clone/paths[5]).read_text())
companion=json.loads((clone/paths[3]).read_text())
print('SUMMARY_TOOL',json.dumps(summary['tool'],sort_keys=True))
assert summary['tool']['sha256']==companion['producer']['sha256']
print('CURRENT_PRODUCER_SHA256',hashlib.sha256((clone/'tools/bash-witness-study.py').read_bytes()).hexdigest())
for p in paths[5:]:
 old=subprocess.check_output(['git','-C',str(lane),'show','5e3569969b532310d2b8a3d130901757a3df356b:'+p])
 assert old==(clone/p).read_bytes(),p
 print('BASE_FROZEN_BYTES_UNCHANGED',p,hashlib.sha256(old).hexdigest())
fixture=clone.parent/'without-expected'
fixture.mkdir(exist_ok=True)
for p in [paths[3]]+paths[5:]:
 dest=fixture/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(clone/p,dest)
assert not (fixture/paths[4]).exists()
cmd=['python3',str(clone/'tools/witness-metadata.py'),'--check','--lane-root',str(fixture),'--companion','.ufo/evidence/round-13/witness-metadata.json']
p=subprocess.run(cmd,cwd=str(clone),capture_output=True,text=True)
print('WITHOUT_EXPECTED_COMMAND',json.dumps(cmd));print('EXIT',p.returncode);print(p.stdout,p.stderr)
assert p.returncode==0
print('POINTER_AND_CLAIM_SWEEP_PASS')
