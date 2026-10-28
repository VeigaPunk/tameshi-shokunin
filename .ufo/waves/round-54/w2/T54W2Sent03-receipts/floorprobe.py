#!/usr/bin/env python3
"""Rename the re-key directory after the FLOOR commit and claim read_rev = floor.

Nothing else changes: every entry's sha256 is still the section's sha at C1, and
every reader report claims cand = the floor. The floor commit is an ancestor of
C1, so the ancestry guard passes; no arm recomputes any section at c0.
"""
import json, os, shutil, subprocess, sys
S = '/fast/scratch/hyaku/tameshi-r54/T54W2Sent03'
C1 = '99c3bc88d704566197783f66b211ee0a830e0330'
FLOOR = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
D = S + '/fixtures/floor'
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
def git(a, check=True):
    return subprocess.run(['git', '-C', D] + a, env=env, capture_output=True, check=check)
if os.path.exists(D): shutil.rmtree(D)
subprocess.run(['git','clone','--shared','--quiet',S+'/fixtures/positive',D],env=env,check=True)
assert git(['rev-parse','--show-toplevel']).stdout.decode().strip() == D
old = '.ufo/evidence/round-21/coldread/rekey-r54-' + C1[:12]
new = '.ufo/evidence/round-21/coldread/rekey-r54-' + FLOOR[:12]
os.makedirs(os.path.join(D,new,'traces'), exist_ok=True)
namemap = {}
for n in sorted(os.listdir(os.path.join(D,old,'traces'))):
    shutil.copyfile(os.path.join(D,old,'traces',n), os.path.join(D,new,'traces',n))
    namemap[old+'/traces/'+n] = new+'/traces/'+n
shutil.rmtree(os.path.join(D,old))
ledger = json.loads(git(['show','HEAD:'+LEDGER]).stdout.decode('utf-8','surrogateescape'))
for e in ledger['entries']:
    tr = e.get('traces') or []
    if any(isinstance(t,str) and t.startswith(old+'/') for t in tr):
        e['traces'] = [namemap[t] for t in tr]
        e['read_rev'] = FLOOR
for n in os.listdir(os.path.join(D,'.ufo/waves/round-54/w1')):
    if not n.endswith('.json'): continue
    p = os.path.join(D,'.ufo/waves/round-54/w1',n)
    d = json.load(open(p)); d['cand'] = FLOOR
    json.dump(d, open(p,'w'), indent=1); open(p,'a').write('\n')
with open(os.path.join(D,LEDGER),'w') as fh:
    json.dump(ledger, fh, indent=1, ensure_ascii=False); fh.write('\n')
git(['add','-A'])
git(['-c','user.name=fixture','-c','user.email=fixture@invalid','commit','--quiet','-m','probe: floor'])
print('FLOORPROBE dir=%s head=%s rekey_dir=%s read_rev=%s'
      % (D, git(['rev-parse','HEAD']).stdout.decode().strip(), new, FLOOR))
