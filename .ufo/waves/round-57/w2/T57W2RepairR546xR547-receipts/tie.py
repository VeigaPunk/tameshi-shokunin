import subprocess, re, json
B='5e3569969b532310d2b8a3d130901757a3df356b'; R='650987a0d6fc285b37f0f9e63a3aae864af9cd5a'
def g(*a): return subprocess.run(['git','-C','.']+list(a),capture_output=True).stdout.decode('utf-8','replace')
text={'R54.6':"**R54.6 — uncommitted round work at closure.** `T54W2Sent03.md` (the seat report whose arm-3 blind spots the round routes) plus the two receipts it cites (`c1committed-positive.stdout`, `rejection-attribution.txt`) were untracked at closure; the deciding run's own `after/clean-tree-after.txt` records them as `??`, i.e. the tree was dirty *during* the measurement the gate calls clean. Every other w2 seat report is committed. The closure swept these three files byte-identical under lane identity (durability commit, named below); the lane must not leave seat deliverables uncommitted again.",
 'R54.7':"**R54.7 — forged-file disposition is imprecise.** `077d431` swept `.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json` into history; `7fa9a5e` **renames** it (`R100`) to `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json`, where it still sits in the tree as the incident receipt. The report says \"the deletion lands in `7fa9a5e0`\" — say \"renamed into the receipts dir\". It never credited and cannot: the path fails arm 4's `/T54W\\d+.*Read.*\\.json$/` and its `section_sha256` (`b90c1f79…`) is not the genuine reader's (`61736dce…`) nor any section at `c0`."}
keys={'R54.6':['T54W2Sent03','c1committed-positive.stdout','rejection-attribution.txt','clean-tree-after.txt'],
      'R54.7':['forged-reader.json','T54W2Sent01','7fa9a5e','R100','section_sha256']}
commits=g('rev-list','--reverse',f'{R}..{B}').split()
for rid in keys:
    tokens=re.findall(r'[\w.\-/]+',text[rid])
    print('==',rid,'basename-in-text tie candidates:')
    for c in commits:
        files=set(g('diff-tree','--no-commit-id','--name-only','-r','--root','-m',c).split('\n'))-{''}
        msg=g('log','-1','--format=%B',c)
        names=re.search(r'(?<![\w.])'+re.escape(rid)+r'(?!\d)',msg) is not None
        for p in files:
            if p.startswith('.ufo/waves/') or p.startswith('.ufo/reports/'):
                if not any(p.endswith(k) for k in keys[rid]): continue
            tie = names or p in text[rid] or p.split('/')[-1] in text[rid]
            if not tie: continue
            print(f'  {c[:7]} names={names} {p}')
