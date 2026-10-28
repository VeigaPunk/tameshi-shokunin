import importlib.util, subprocess, sys, json

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
spec = importlib.util.spec_from_file_location('m18', LANE + '/.ufo/evidence/round-18/measure.py')
m18 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m18)
raw = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', REV + ':SKILL.md'],
                     capture_output=True, check=True).stdout
secs = m18.sectionize(raw)
for s in secs:
    if s['heading'].strip() == '## Standing rules':
        print(json.dumps({k: s[k] for k in ('start', 'end', 'heading', 'sha256')}))
