import os, re, sys, runpy
os.environ.setdefault('S', os.environ['S'])
import importlib.util
FIX = os.environ['S'] + '/fix'
spec = importlib.util.spec_from_file_location('m50', FIX + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
orig = m.planned_ids
def widened(lane, rev):
    blob = m.show(lane, rev, 'SCORECARD.md').decode()
    para = blob.split('**Planned (round')[-1]
    return set(re.findall(r'\bR\d{2}\.\d+\b', para))
m.planned_ids = widened
rev = subprocess.run(['git','-C',FIX,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip() if False else __import__('subprocess').run(['git','-C',FIX,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
import json, hashlib, subprocess
W = os.environ['W']; BASE='5e3569969b532310d2b8a3d130901757a3df356b'; ROUTED='c1d49d76be4028df2a68322e7117ff3aafaccd5c'; SPOT='corpus/lessons/round-52-verifier-spotcheck.md'
rows = json.load(open(W+'/rows.json'))
sha = hashlib.sha256(subprocess.run(['git','-C',FIX,'show',BASE+':'+SPOT],capture_output=True).stdout).hexdigest()
defects=[{'id':r['id'],'file':SPOT,'file_sha256':sha,'routed_at':ROUTED,'keys':r['keys']} for r in rows]
rv, counts, stat, total, n = m.measure(FIX, rev, defects, True, fixed_floor=0, declined_cap=99, this_round_floor=0, base=BASE)
print('with R5x-widened planned regex: total=%d counts=%s stat=%s' % (total, {k:v for k,v in counts.items() if v}, stat))
