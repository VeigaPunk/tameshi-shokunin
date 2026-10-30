import hashlib, importlib.util, json, pathlib, subprocess, sys
lane, clone, rev = sys.argv[1:]
spec = importlib.util.spec_from_file_location('frozen18', lane+'/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw = subprocess.check_output(['git','-C',lane,'show',rev+':SKILL.md'])
sec = next(s for s in m.sectionize(raw) if s['heading']=='## Effective expectation reconciliation — round 14')
print('SECTION',sec['start'],sec['end'],sec['sha256'])
root=pathlib.Path(clone)
paths=['corpus/lessons/round-13-verifier-spotcheck.md','corpus/knowledge/incremental-pin-disposition.md','.ufo/evidence/round-13/expected.json','.ufo/evidence/round-14/dispositions-before.json','.ufo/evidence/round-14/dispositions.json','.ufo/evidence/round-14/verification-final.json','.ufo/evidence/round-14/verification.json','.ufo/evidence/round-14/capture-context.py','tools/context-capture.py','.ufo/evidence/round-18/dispositions.json']
for path in paths: print('POINTER',path,(root/path).is_file())
x=json.loads((root/paths[2]).read_bytes())
print('COUNTS',len(x['expected_checks']),len(x['inputs']))
print('STALE',[p for p,h in x['inputs'].items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h])
a=json.loads((root/paths[3]).read_bytes()); b=json.loads((root/paths[4]).read_bytes())
print('DELTA_TOP_KEYS',[k for k in set(a)|set(b) if a.get(k)!=b.get(k)])
print('DELTA_ROWS',[(i,u,v) for i,(u,v) in enumerate(zip(a['rows'],b['rows'])) if u!=v])
for f in ['verification.json','verification-final.json']:
 d=json.loads((root/'.ufo/evidence/round-14'/f).read_bytes())
 print('RETAINED',f,'measured_commit',d['measured_commit'])
 for c in d['checks']:
  print(c['name'],'exit',c['exit'],'last_stdout_line',c['stdout'].rstrip().splitlines()[-1])
for code in ['S003','S049']:
 rows=[r for r in (root/'corpus/SOURCES.md').read_text().splitlines() if r.startswith('| '+code+' |')]
 print('SOURCE',code,'rows',len(rows))
