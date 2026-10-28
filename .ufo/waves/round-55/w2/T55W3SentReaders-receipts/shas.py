import importlib.util, subprocess, json, sys
spec=importlib.util.spec_from_file_location('m18','.ufo/evidence/round-18/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rev='9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
raw=subprocess.run(['git','cat-file','blob',rev+':SKILL.md'],capture_output=True,check=True).stdout
secs=m.sectionize(raw)
by={}
for s in secs:
    by.setdefault(s['heading'],[]).append(s)
heads=["## Context gate classification and explicit exit classes — round 15",
"## Effective expectation reconciliation — round 14",
"## Live-tree re-pin and entry-command monitor — round 17",
"## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
"## Pin disposition and provenance correction — round 13",
"## Repeated controls and gate registry — round 12",
"## Standing rules",
"## The leg ledger — replay, receipt, and how it is read (round 7, measured)",
"## The operator's runbook and the six-leg regression (round 10, measured)",
"### Gate/probe registry",
"### Round-13 gate/probe registry",
"### Round-15 gate/probe registry",
"### Round-17 gate/probe registry — re-pin and monitor",
"### Round-18 gate/probe registry — routed-defect closure",
"### Round-21 gate/probe registry — finite environment differential",
"### Round-26 gate/probe registry — report interop",
"### The service's limits — what tameshi refuses to mutation-test",
"### Triggers T1–T3 and the re-pin rule"]
out={}
for h in heads:
    got=by.get(h)
    if not got:
        print('MISSING-IN-SKILL', repr(h)); out[h]=None; continue
    if len(got)>1:
        print('DUPLICATE-IN-SKILL', repr(h), len(got))
    s=got[0]
    out[h]={'sha':s['sha256'],'start':s['start'],'end':s['end']}
    print(f"{s['sha256']}  L{s['start']}-{s['end']}  {h}")
json.dump(out,open('/fast/scratch/hyaku/tameshi-r55/T55W3SentReaders/c0-sections.json','w'),indent=1,ensure_ascii=False)
print('total headings', len(heads), 'resolved', sum(1 for v in out.values() if v))
