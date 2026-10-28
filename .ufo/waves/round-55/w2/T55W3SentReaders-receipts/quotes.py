import importlib.util, subprocess, json, os, re
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
C0='9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
spec=importlib.util.spec_from_file_location('m18',LANE+'/.ufo/evidence/round-18/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=subprocess.run(['git','-C',LANE,'cat-file','blob',C0+':SKILL.md'],capture_output=True,check=True).stdout
text=raw.decode('utf-8','surrogateescape').split('\n')
secs=m.sectionize(raw)
def body(s): return '\n'.join(text[s['start']-1:s['end']])
by={s['heading']:s for s in secs}
for d in ('w3','w2'):
    p=f'{LANE}/.ufo/waves/round-55/{d}'
    for f in sorted(os.listdir(p)):
        if re.fullmatch(r'T55W3R\d\d\.json',f):
            j=json.load(open(f'{p}/{f}'))
            b=body(by[j['heading']])
            print(f'== {d}/{f} findings={len(j["findings"])}')
            for k,x in enumerate(j['findings']):
                q=x['quote']
                present = q in b
                print(f'   [{k}] quote_present_in_section={present} quote={q[:110]!r}')
