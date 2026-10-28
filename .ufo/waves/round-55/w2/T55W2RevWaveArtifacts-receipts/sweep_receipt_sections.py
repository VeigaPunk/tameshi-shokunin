import json,os,re,subprocess
C0='9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'; P='.ufo/waves/round-55/w1/'
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; os.chdir(LANE)
files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C0]).decode().split())
md={os.path.basename(f)[:-3]:f for f in files if f.startswith(P) and f.count('/')==4 and f.endswith('.md')}
tok=re.compile(r'`([^`\n]{2,160})`')
hdr=re.compile(r'^#{1,6}\s')
recsec=re.compile(r'^#{1,6}.*(receipt|artefact|artifact|deliverab|output)',re.I)
missing=[]; total=0; seats_with=0
for seat,f in sorted(md.items()):
    text=subprocess.check_output(['git','show',C0+':'+f]).decode('utf-8','replace').splitlines()
    own={x[len(P+seat+'-receipts/'):] for x in files if x.startswith(P+seat+'-receipts/')}
    insec=False; has=False
    for ln,line in enumerate(text,1):
        if hdr.match(line): insec=bool(recsec.match(line))
        if not insec: continue
        for raw in tok.findall(line):
            t=raw.strip()
            if '/' in t or ' ' in t or t.endswith('/') or '*' in t or '…' in t or '<' in t or '{' in t: continue
            if not re.search(r'\.(txt|stdout|stderr|json|diff|patch|py|out|sha256|exit|rc|log|html|sh|md|sha|csv|tsv|pem)$',t): continue
            total+=1
            if t in own or t==seat+'.md' or t==seat+'.json': has=True; continue
            missing.append((seat,ln,t))
    if has: seats_with+=1
print('deliverable-section tokens checked:',total,'seats with a receipts/deliverables section:',seats_with)
print('citations that do not resolve to the seat own receipts dir:',len(missing))
for m in missing: print(f'{m[0]}:{m[1]}: {m[2]}')
