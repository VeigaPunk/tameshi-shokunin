import json, subprocess, collections
LANE="/home/vgpnk/Projects/shokunin/tameshi-shokunin"; BASE="0a2010acd1e92e4e332774050825e21bcfc7e079"
PKG="/home/vgpnk/Projects/shokuknow/merge/tameshi"
def show(c):
    r=subprocess.run(c,capture_output=True,text=True); return r.stdout
print("== R54.9 wave half: .ufo/waves/round-54/w1-registry.json at",BASE,"==")
d=json.loads(show(["git","-C",LANE,"show",BASE+":.ufo/waves/round-54/w1-registry.json"]))
print("role_mix:",json.dumps(d["role_mix"],sort_keys=True))
print("role_mix sum:",sum(d["role_mix"].values()),"| seats:",d["seats"],"| attack_seats:",d["attack_seats"])
print("items (seat names):",len(d["items"]))
print("reviewer+critic+mutation-tester:",d["role_mix"]["reviewer"]+d["role_mix"]["critic"]+d["role_mix"]["mutation-tester"])
print("attack share: %d/%d = %.4f%% -> 27.6%%" % (d["attack_seats"],d["seats"],100*d["attack_seats"]/d["seats"]))
print()
print("== R54.9 staged half: MERGE-REPORT.json entries vs files on disk ==")
m=json.load(open(PKG+"/MERGE-REPORT.json"))
t=[(e.get("target") or e.get("canonical_target")) for e in m["entries"]]
c=collections.Counter(t)
print("entries:",len(m["entries"]),"| distinct targets:",len(c),"| duplicated target:",[k for k,v in c.items() if v>1])
def rel(root,strip):
    out=show(["find",root,"-name","*.md"]).split(); return {p.split(strip,1)[1] for p in out}
k=rel(PKG+"/knowledge",PKG+"/knowledge/"); a=rel(PKG+"/amendments",PKG+"/amendments/")
print("knowledge/*.md:",len(k),"| amendments/*.md:",len(a),"| union:",len(k|a))
print("set(distinct targets) == union:",set(t)==(k|a))
print("knowledge-only file count (what c1/measure.py globs as `staged`):",len(k))
print("staged entry files:",len(k|a),"| minus the named delta-debugging entry:",len(k|a)-1)
print("delta entry in knowledge/:", "corpus/knowledge/delta-debugging-minimization-contract.md" in k)
print()
print("== R54.9 fleet-report claims (bytes) ==")
rep="/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md"
lines=open(rep).read().splitlines()
for n in (8,58,206): print("  %d: %s" % (n,lines[n-1].strip()))
print("  report itemization sum (23+13+4+4+2+12+4+4+4+3+2) =", 23+13+4+4+2+12+4+4+4+3+2)
print("  20/76 = %.4f%% (the report's own count with 4 reviewers)" % (100*20/76))
print()
print("== R54.10: receipts at",BASE,"==")
for f in (".ufo/evidence/round-54/control/controls-a.stdout",".ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout"):
    for ln in show(["git","-C",LANE,"show",BASE+":"+f]).splitlines():
        if "CTL_R53" in ln or ln.startswith("C1_R53"): print(" ",f.split("/")[-1],"::",ln)
print("report bytes :51-52:")
for n in (51,52): print("  %d: %s" % (n,lines[n-1]))
