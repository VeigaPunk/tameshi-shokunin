#!/usr/bin/env python3
# Attack-side extractor: rounds 50-56 routed items, list items AND bold-led paragraphs.
import json, re, subprocess, sys, hashlib
LANE = sys.argv[1]; REV = sys.argv[2]
GENERIC = {'SKILL.md','SCORECARD.md','LOG.md','SHONEN.md','README.md','QUALITY.md','SOURCES.md','corpus/SOURCES.md','corpus/QUALITY.md','corpus/README.md','[~]','--selftest','measure.py'}
ITEM_RE = re.compile(r'^(?:(\d+)\.|-)\s+(.*)$')
BOLD_RE = re.compile(r'^\*\*R(\d+)\.(\d+)')
PATH_RE = re.compile(r'(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|json|mjs|stdout|spec|jsonl))\b')
SID_RE = re.compile(r'\bS\d{3}\b')
def git(*a): return subprocess.run(['git','-C',LANE]+list(a),check=True,capture_output=True).stdout
def blocks(text):
    lines=text.split('\n'); out=[]; inside=False; cur=None; start=None
    for no,line in enumerate(lines,1):
        if line.startswith('## '):
            inside = 'rout' in line.lower(); cur=None; continue
        if not inside: continue
        if not line.strip(): cur=None; continue
        m=ITEM_RE.match(line)
        if m:
            cur={'line':no,'text':m.group(2).strip(),'kind':'list'}; out.append(cur); continue
        if line.startswith('**R') or (cur is None and line.startswith('**')):
            cur={'line':no,'text':line.strip(),'kind':'bold'}; out.append(cur); continue
        if cur is not None and line.startswith((' ','\t')):
            cur['text']+=' '+line.strip()
        elif cur is not None and cur['kind']=='bold':
            cur['text']+=' '+line.strip()
    return out
def keys_of(text):
    keys=[s.strip() for s in re.findall(r'`([^`\n]+)`',text)]
    keys=[k for k in keys if k and k not in GENERIC and len(k)>=4]
    keys+=[p for p in PATH_RE.findall(text) if p not in GENERIC]
    keys+=SID_RE.findall(text)
    seen=[];[seen.append(k) for k in keys if k not in seen]
    return seen
out=[]
for r in range(50,57):
    path='corpus/lessons/round-%d-verifier-spotcheck.md'%r
    blob=git('show','%s:%s'%(REV,path)).decode()
    routed_at=git('log','--diff-filter=A','--format=%H',REV,'--',path).decode().split()[-1]
    items=blocks(blob); n_unl=0; seen={}; pos=0
    for it in items:
        m=BOLD_RE.match(it['text']); pos+=1
        if m and int(m.group(1))==r:
            did='R%d.%s'%(r,m.group(2))
        else:
            did='R%d.%d'%(r,pos)   # absolute 1-based position in the routed list (the id rule as written collides)
        if did in seen:
            seen[did]['text']+=' '+it['text']; continue
        rec={'id':did,'round':r,'file':path,'line':it['line'],'routed_at':routed_at,'file_sha256':hashlib.sha256(blob.encode()).hexdigest(),'text':it['text'],'keys':keys_of(it['text']),'kind':it['kind']}
        seen[did]=rec; out.append(rec)
print(json.dumps({'count':len(out),'defects':out},ensure_ascii=False,indent=1))
