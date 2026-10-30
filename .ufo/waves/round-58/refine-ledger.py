#!/usr/bin/env python3
"""Select substantive located evidence, not incidental key matches, in the candidate.
This is an integration record; unresolved proof chains remain visible to the counter.
"""
import json,pathlib,re
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin');p=L/'.ufo/waves/round-58/ledger-candidate.json';d=json.loads(p.read_text());by={r['id']:r for r in d['defects']}
def setev(i,path,needle,before=0,after=0):
 lines=(L/path).read_text().splitlines();hits=[n for n,s in enumerate(lines) if needle in s]
 if len(hits)!=1:print('AMBIGUOUS',i,needle,len(hits));return
 n=hits[0];a=max(0,n-before);b=min(len(lines),n+after+1);ex=' '.join(s.strip() for s in lines[a:b]);
 if len(ex)>400:print('LONG',i,len(ex));return
 e={'path':path,'lines':f'{a+1}-{b}','excerpt':ex};by[i]['evidence']=[e]
# Substantive correction sentences; no headings/shebangs as purported repairs.
setev('R50.2','SKILL.md','| pbt staged-id generator |')
setev('R50.3','corpus/README.md','| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held')
setev('R51.1','tools/registry.json','"MTE_INTEROP: PASS legs_conforming=10/10"')
# Row key can match its path; include a second name cell to tie to the mte item.
if 'R51.1' in by:
 lines=(L/'tools/registry.json').read_text().splitlines();n=next(n for n,s in enumerate(lines) if '"name": "mte-interop-check"' in s)
 by['R51.1']['evidence'].append({'path':'tools/registry.json','lines':f'{n+1}-{n+1}','excerpt':lines[n].strip()})
setev('R51.5','corpus/lessons/round-58.md','At kagi revision `c49023b773b69de983f0e6eb7e5867ceb5c2c634`')
setev('R51.6','corpus/lessons/round-58.md','R51.6 — rejected candidates and reasons')
setev('R52.4','.ufo/evidence/round-52/integrate/build-readers.py','Usage: build-readers.py')
setev('R53.4','corpus/lessons/round-58.md','R53.4: the earlier')
setev('R54.1','SCORECARD.md','Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`',0,1)
setev('R54.2','SCORECARD.md','Corrected: one pointer, `077d431e`',0,1)
setev('R54.3','SCORECARD.md','Old: `total=14` in the C2 claim row. Corrected: `total=13`.',0,1)
setev('R54.4','SCORECARD.md','Old: `49280fe5` for `c2/measure.py`. Corrected: `8528ee85`',0,1)
setev('R54.7','SCORECARD.md','Corrected: the file was **renamed**',0,2)
setev('R54.10','SCORECARD.md',"Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7`",0,1)
setev('R55.1','corpus/lessons/round-58.md','At measured revision `4c04c1d3`')
setev('R55.3','SCORECARD.md','Standing axis table at the round end:',0,1)
setev('R56.3','corpus/knowledge/receipt-revision-binding.md','The frontmatter `recheck:` line still names the freeze-era',0,3)
setev('R56.4','.ufo/evidence/round-57/coldread-referent-r56.md','- Referent: commit',0,1)
setev('R56.5','.ufo/evidence/round-57/controls.sh','# ONE GENERATION. Controls are RECOMPUTED',0,3)
p.write_text(json.dumps(d,ensure_ascii=False,indent=1)+'\n')
print('refined candidate written')
