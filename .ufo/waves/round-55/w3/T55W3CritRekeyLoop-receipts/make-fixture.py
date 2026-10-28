import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
LANE=Path(sys.argv[1]); C0=sys.argv[2]
E='.ufo/evidence/round-55'
def show(rev,path):
    return subprocess.run(['git','-C',str(LANE),'show','%s:%s'%(rev,path)],capture_output=True,check=True).stdout
r18=LANE/'.ufo/evidence/round-18/measure.py'
spec=importlib.util.spec_from_file_location('r18', str(r18)); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
secs=m.sectionize(show(C0,'SKILL.md'))
heads=sorted(set(json.loads((LANE/E/'c1/lost-headings-at-c0.json').read_text())))
by={s['heading']:s for s in secs}
out=[]
w3=LANE/'.ufo/waves/round-55/w3'
for n,h in enumerate(heads,1):
    sha=by[h]['sha256']
    (w3/('FAKEREAD%02d.json'%n)).write_text(json.dumps({
        'heading':h,'cand':C0,'section_sha256':sha,'findings':[]},indent=1)+'\n')
    (w3/('FAKEREAD%02d.md'%n)).write_text(
        '# FAKEREAD%02d\n\nThis seat did not open `SKILL.md`, did not run a command and did not read the section.\n'
        'The sha above was produced by scripts/make-fixture.py from `git show %s:SKILL.md`.\n'
        'No artifact was opened. findings is empty because nothing was read.\n'%(n,C0[:12]))
    out.append((n,h,sha))
print('wrote',len(out),'reader pairs')
print(json.dumps(out[:2],indent=1))
