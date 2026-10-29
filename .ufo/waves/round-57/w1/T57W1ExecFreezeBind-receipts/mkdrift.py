import hashlib, importlib.util, json, subprocess, sys, os
from pathlib import Path
lane, extra_input = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else '')
assert subprocess.run(['git','-C',lane,'rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()==lane
G=['git','-c','user.name=fixture','-c','user.email=fixture@example.invalid','-C',lane]
H='## The mutation bar — nominal vs load-bearing'
p=Path(lane,'SKILL.md'); t=p.read_text().replace('Never quote a case count from source.','Never quote a case count from sources.',1)
p.write_text(t); subprocess.run(G+['commit','-qam','synthetic one-line drift in one SKILL section'],check=True)
c0=subprocess.run(G+['rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
src=subprocess.run(G+['show',c0+':.ufo/evidence/round-18/measure.py'],capture_output=True).stdout
Path(os.environ['S'],'r18.py').write_bytes(src)
spec=importlib.util.spec_from_file_location('r18',os.environ['S']+'/r18.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sec={s['heading']:s for s in m.sectionize(p.read_bytes())}[H]
w=Path(lane,'.ufo/waves/round-57/w3'); w.mkdir(parents=True)
(w/'T57W3SynthRead01.json').write_text(json.dumps({'heading':H,'cand':c0,'section_sha256':sec['sha256'],'findings':[]},indent=1))
(w/'T57W3SynthRead01.md').write_text('synthetic reader\n')
if extra_input:
    ip=Path(lane,extra_input); ip.write_text(ip.read_text()+'\n')
subprocess.run(G+['add','-A','.ufo/waves/round-57',extra_input or '.ufo/waves/round-57'],check=True)
subprocess.run(G+['commit','-qm','synthetic readers'+(' + moved input' if extra_input else '')],check=True)
print(c0, subprocess.run(G+['rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())
