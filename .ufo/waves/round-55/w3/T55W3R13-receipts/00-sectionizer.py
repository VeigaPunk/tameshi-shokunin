import importlib.util, subprocess, hashlib, json
REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
HEAD = '### Round-17 gate/probe registry \u2014 re-pin and monitor'
spec = importlib.util.spec_from_file_location('r18measure', REPO + '/.ufo/evidence/round-18/measure.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
raw = subprocess.run(['git','-C',REPO,'show',REV+':SKILL.md'], capture_output=True).stdout
hits = [s for s in mod.sectionize(raw) if s['heading'] == HEAD]
assert len(hits) == 1, hits
s = hits[0]
lines = raw.decode('utf-8','surrogateescape').split('\n')
body = lines[s['start']-1:s['end']-1]
while body and body[-1].strip() == '':
    body.pop()
print(json.dumps({'heading': s['heading'], 'start': s['start'], 'end': s['end'],
                  'sha256': s['sha256'],
                  'sha256_recomputed': hashlib.sha256('\n'.join(body).encode('utf-8','surrogateescape')).hexdigest(),
                  'n_lines': len(body)}, ensure_ascii=False, indent=2))
print('---- SECTION TEXT ----')
print('\n'.join(body))
