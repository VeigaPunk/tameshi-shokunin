import json,os,re,subprocess,sys
C0='9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
P='.ufo/waves/round-55/w1/'
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET='/home/vgpnk/Projects/shokunin'
os.chdir(LANE)
# full tree incl dirs at C0
out=subprocess.check_output(['git','ls-tree','-r','-d','--name-only',C0]).decode().split()
files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C0]).decode().split())
dirs=set(out)
disp=json.loads(subprocess.check_output(['git','show',C0+':.ufo/waves/round-55/w1-dispatch.json']))
names=set(disp['registry']['members'])
md=[f for f in files if f.startswith(P) and f.count('/')==4 and f.endswith('.md')]
tokre=re.compile(r'`([^`\n]{2,240})`')
claimre=re.compile(r'\b(wrote|written|write|created|create|restored|restore|landed|land|applied|apply|produced|produce|appended|append|committed|saved|saved to|staged|generated)\b', re.I)
def norm(t):
    t=t.strip().strip('`').strip()
    t=re.sub(r':[0-9][0-9,\-]*$','',t)           # :12  :12-14  :7,9
    t=re.sub(r'@[0-9a-f]{7,40}$','',t)           # @rev
    return t
def variants(t):
    v=set()
    # brace expansion
    m=re.match(r'^(.*)\{([^{}]+)\}(.*)$',t)
    if m:
        for alt in m.group(2).split(','):
            v|=variants(m.group(1)+alt+m.group(3))
        return v
    if t.startswith(LANE+'/'): t=t[len(LANE)+1:]
    if t.startswith(FLEET+'/'): t='FLEET:'+t[len(FLEET)+1:]
    if t.startswith('./'): t=t[2:]
    v.add(t)
    if '/' not in t and t.endswith(('.md','.json','.txt','.py','.stdout','.sh')):
        v.add(P+t); v.add(P+'T55W1ExecReKeyDryBind-receipts/'+t)
    return v
def exists(t):
    if not t: return None
    if '*' in t or '…' in t or '<' in t or t.endswith('/'): return True  # glob/placeholder/dir-shape: not a concrete missing file
    if t.startswith('FLEET:'):
        p=os.path.join(FLEET,t[len('FLEET:'):])
        return os.path.exists(p)
    if t in files or t in dirs: return True
    # fleet-root relative for .ufo paths outside the lane
    if t.startswith('.ufo/') and not t.startswith('.ufo/waves/round-55'):
        p=os.path.join(FLEET,t)
        if os.path.exists(p): return True
    return False
rows=[]
for f in sorted(md):
    seat=os.path.basename(f)[:-3]
    text=subprocess.check_output(['git','show',C0+':'+f]).decode('utf-8','replace')
    for ln,line in enumerate(text.splitlines(),1):
        if not claimre.search(line): continue
        for raw in tokre.findall(line):
            t=norm(raw)
            if not t or ' ' in t: continue
            if not re.match(r'^(\.?/?\.ufo|tools|corpus|scripts|SKILL\.md|SCORECARD\.md|LOG\.md|MANIFEST\.json|consign|/home/vgpnk|tameshi|\.scratch)',t): continue
            if '/fast/scratch' in t or t.startswith('~') or '/tmp/' in t: continue
            vs=variants(t)
            ok=any(exists(v) for v in vs)
            if not ok: rows.append((seat,ln,t))
print('CLAIM-LINE PATH TOKENS MISSING AT C0:',len(rows))
for seat,ln,t in rows: print(f'{seat}:{ln}: {t}')
