#!/usr/bin/env python3
"""Read-only C0b section checks; generated state confined to seat scratch/receipts."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
S = Path('/fast/scratch/hyaku/tameshi-r57/T57W3Read03')
CLONE = S / 'clone'
OUT = LANE / '.ufo/waves/round-57/w3/T57W3Read03-receipts'
REV = 'adf87899c70d616140a81185a8f9acbbdfb30392'
HEADING = '## The leg ledger — replay, receipt, and how it is read (round 7, measured)'
ENV = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
ENV['TMPDIR'] = str(S / 'tmp')
Path(ENV['TMPDIR']).mkdir(parents=True, exist_ok=True)

def run(args):
    r = subprocess.run(args, cwd=CLONE, env=ENV, capture_output=True, text=True)
    return {'command': ' '.join(map(str,args)), 'cwd': str(CLONE), 'exit_code': r.returncode, 'output': r.stdout, 'stderr': r.stderr}

def static():
    results = []
    spec = importlib.util.spec_from_file_location('frozen', LANE / '.ufo/evidence/round-18/measure.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    raw = subprocess.check_output(['git','-C',str(LANE),'show',REV+':SKILL.md'], env=ENV)
    sec = next(s for s in m.sectionize(raw) if s['heading']==HEADING)
    results.append({'command': "python3: importlib loads frozen round-18/measure.py; raw=git -C " + str(LANE) + " show " + REV + ":SKILL.md; m.sectionize(raw); select exact heading; print(sec['start'],sec['end'],sec['sha256'])", 'exit_code':0, 'output':f"{sec['start']} {sec['end']} {sec['sha256']}\n"})
    for rev, ranges in [('9f1d3c3', [(72,109),(511,522)]),('4b7c682',[(597,620)])]:
        rec = run(['git','-C',str(CLONE),'show',rev+':tools/mutate-and-run.sh'])
        lines = rec['output'].splitlines()
        rec['output'] = '\n'.join(f'{i}: {lines[i-1]}' for a,b in ranges for i in range(a,b+1))+'\n'
        rec['selection'] = ranges
        results.append(rec)
    ledger = (CLONE/'corpus/knowledge/fleet-kill-rate-ledger.md').read_text()
    rows = [line for line in ledger.splitlines() if re.match(r'^\| [1-6] \|',line)]
    first_six = rows[:6]
    appends = [line for line in ledger.splitlines() if line.startswith('| kumitate `scripts/round-gate.mjs`') or line.startswith('| kumitate `scripts/sources-check.mjs`')]
    results.append({'command': 'python3: count original §1 rows, ER-2 rows, round-16 and round-18 appended measured rows in '+str(CLONE/'corpus/knowledge/fleet-kill-rate-ledger.md'), 'exit_code':0, 'output':json.dumps({'section1_and_ER2_count':len(first_six),'appended_count':len(appends),'total':len(first_six)+len(appends),'rows':first_six+appends},indent=2)})
    paths = ['tools/mutate-and-run.sh','corpus/knowledge/fleet-kill-rate-ledger.md','corpus/knowledge/mutation-case-kumitate-cite-check.md','corpus/knowledge/mutation-case-kagi-drift-pins.md','corpus/README.md','corpus/SOURCES.md']
    results.append({'command':'python3: existence and sha256 of section pointers and drifted context inputs at detached C0b', 'exit_code':0, 'output':json.dumps({p:{'exists':(CLONE/p).is_file(),'sha256':hashlib.sha256((CLONE/p).read_bytes()).hexdigest()} for p in paths},indent=2)})
    (OUT/'static.json').write_text(json.dumps(results,indent=2)+'\n')
    return results

def replay():
    for name in ('kumitate-shokunin','kagi-shokunin','tsukuroi-shokunin','mado-shokunin'):
        target = S/name
        if not target.exists():
            target.symlink_to(LANE.parent/name, target_is_directory=True)
    rec = run(['bash',str(CLONE/'tools/mutate-and-run.sh'),'--regression','--workdir',str(S/'regression')])
    (OUT/'regression.json').write_text(json.dumps(rec,indent=2)+'\n')
    (OUT/'regression.stdout').write_text(rec['output'])
    (OUT/'regression.stderr').write_text(rec['stderr'])
    for leg in (S/'regression').iterdir():
        if not leg.is_dir() or leg.name=='specs':
            continue
        dest=OUT/leg.name
        dest.mkdir(exist_ok=True)
        for name in ('sweep.log','results.tsv','git-show.err'):
            if (leg/name).is_file():
                shutil.copyfile(leg/name,dest/name)
    return rec

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    a=pool.submit(static)
    b=pool.submit(replay)
    for rec in a.result():
        print(json.dumps(rec,ensure_ascii=False))
    print(json.dumps(b.result(),ensure_ascii=False))
