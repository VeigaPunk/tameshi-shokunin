import hashlib, json, subprocess, urllib.request
from html.parser import HTMLParser
from pathlib import Path
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
C='8063d0a551fc5b3cb5a2d397da7353af53444534'
B='2a32aa8228d5f86a85c81a923a3148bf792a9538'
def show(rev,path):
    return subprocess.check_output(['git','-C',L,'show',rev+':'+path],text=True)
def row(text,id):
    return next(x for x in text.splitlines() if x.startswith('| '+id+' |'))
cand=show(C,'corpus/SOURCES.md'); base=show(B,'corpus/SOURCES.md')
r285=row(cand,'S285'); r288=row(cand,'S288'); teaches=r288.split('|')[7].strip()
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data): self.parts.append(data)
req=urllib.request.Request('https://www.atlassian.com/incident-management/handbook/postmortems',headers={'User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req,timeout=60) as response:
    raw=response.read(); status=response.status
Path(__file__).with_name('atlassian-live.html').write_bytes(raw)
p=Parser(); p.feed(raw.decode()); text=' '.join(' '.join(p.parts).split())
sentence='We practice blameless postmortems at Atlassian to ensure we understand and remediate the root cause of every incident with a severity of level 2 or higher.'
checks={
 'http':status,'live_bytes':len(raw),'live_sha256':hashlib.sha256(raw).hexdigest(),
 'sentence':sentence,'live_sentence_found':sentence in text,
 'extract_sentence_found':sentence in ' '.join(show(C,'.ufo/waves/round-58/l1/sources/atlassian-postmortems.txt').split()),
 'S285_unchanged':r285==row(base,'S285'),
 'S288_absent_at_base':'| S288 |' not in base,
 'S288_unique_at_C0':sum(x.startswith('| S288 |') for x in cand.splitlines())==1,
 'supersession_prefix':teaches.startswith('supersedes S285 —'),
 'rejection_carried':'REJECTED:' in teaches and r288.split('|')[8].strip()=='rejected',
 'flip_carried':'flip:' in teaches,
 'explicit_when_needed_sentence_found':"We carry out postmortems for severity 1 and 2 incidents. Otherwise, they're optional." in text}
result=json.dumps(checks,indent=2,ensure_ascii=False)+'\n'
Path(__file__).with_name('source-sweep.json').write_text(result)
print(result,end='')
