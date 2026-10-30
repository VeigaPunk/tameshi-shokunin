#!/usr/bin/env python3
"""Capture one declared controls generation and split its two labelled phases.
Usage: capture-controls.py REV. Refuses to overwrite an existing generation.
"""
import hashlib,json,os,pathlib,re,subprocess,sys
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin');E=L/'.ufo/evidence/round-58';O=E/'control';REV=sys.argv[1]
if (O/'controls-generation.stdout').exists():raise SystemExit('control generation already captured; no silent reroll')
env=dict(os.environ,HYAKU_SCRATCH='/fast/scratch/hyaku')
r=subprocess.run(['bash',str(E/'controls.sh'),str(L),'2a32aa8228d5f86a85c81a923a3148bf792a9538',REV,str(O)],capture_output=True,text=True,env=env)
(O/'controls-generation.stdout').write_text(r.stdout);(O/'controls-generation.stderr').write_text(r.stderr)
cut=r.stdout.find('# phase B:')
parts={'a':r.stdout[:cut] if cut>=0 else r.stdout,'b':r.stdout[cut:] if cut>=0 else ''}
ok=True
for ab,t in parts.items():
 (O/f'controls-{ab}.stdout').write_text(t)
 mt=re.search(r'^CONTROLS_'+ab.upper()+r': (\d+)/(\d+) as pre-registered$',t,re.M)
 passed=bool(mt and mt[1]==mt[2] and not re.search('CTL_(?:ARM_)?MISMATCH',t))
 code=0 if passed else 1;ok&=passed
 (O/f'controls-{ab}.exit').write_text(str(code)+'\n')
 (O/f'controls-{ab}.stdout.sha256').write_text(hashlib.sha256(t.encode()).hexdigest()+'\n')
 print(ab,'exit',code,mt[0] if mt else 'tally absent')
(O/'controls-generation.json').write_text(json.dumps({'rev':REV,'wrapper_exit':r.returncode,'phases_pass':ok},indent=1)+'\n')
raise SystemExit(0 if ok and r.returncode==0 else 1)
