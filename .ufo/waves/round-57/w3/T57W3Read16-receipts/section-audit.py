import importlib.util, subprocess, pathlib, hashlib, json
lane='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
root=pathlib.Path('/fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone')
rev='adf87899c70d616140a81185a8f9acbbdfb30392'
spec=importlib.util.spec_from_file_location('frozen',lane+'/.ufo/evidence/round-18/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=subprocess.check_output(['git','-C',lane,'show',rev+':SKILL.md'])
sec=next(s for s in m.sectionize(raw) if s['heading']=='### Round-18 gate/probe registry — routed-defect closure')
print(sec['start'],sec['end'],sec['sha256'])
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==rev
paths=['.ufo/evidence/round-18/defect-probes.py','tools/registry-check.py','tools/registry.json','tools/evidence-disposition.py','tools/bash-witness-study.py','tools/trace-inputs.py','.ufo/evidence/round-17/coldread/trace-inputs.py','.ufo/evidence/round-18/measure.py','.ufo/evidence/round-18/coldread/assemble.py','.ufo/evidence/round-18/coldread/ledger.json','.ufo/evidence/round-18/dispositions.json','.ufo/waves/round-18/w2/SentinelKillCode.md','.ufo/evidence/round-19/measure.py','.ufo/evidence/round-19/coldread/measure.py','.ufo/evidence/round-19/coldread/ledger.json','.ufo/evidence/round-19/contract.json','.ufo/evidence/round-19/before.json','.ufo/evidence/round-19/source-baseline.txt','.ufo/evidence/round-19/source-round18-final.txt','corpus/lessons/round-19.md','corpus/QUALITY.md','corpus/SOURCES.md']
for path in paths:
    assert (root/path).is_file(), path
    print('POINTER OK',path,hashlib.sha256((root/path).read_bytes()).hexdigest())
runner=(root/'tools/mutate-and-run.sh').read_text().splitlines()
assert runner[615].startswith('PIN_BASH=275d8294') and runner[616].startswith('REV_BASH=fecee874')
print('PIN LINES OK',616,runner[615],617,runner[616])
disposition=json.loads((root/'.ufo/evidence/round-18/dispositions.json').read_text())
assert '4acc607dfd79f19d508bd50cdd06b77269fccd1d' in json.dumps(disposition)
assert (root/'tools/trace-inputs.py').read_bytes()!=(root/'.ufo/evidence/round-17/coldread/trace-inputs.py').read_bytes()
print('PROMOTED TRACE DIFFERS FROM HISTORICAL COPY: OK')
for token,path in [('37.','corpus/QUALITY.md'),('38.','corpus/QUALITY.md'),('39.','corpus/QUALITY.md'),('| S049 |','corpus/SOURCES.md')]:
    assert token in (root/path).read_text(); print('ANCHOR OK',path,token)
print('ALL POINTER AND IDENTITY CHECKS PASS')
