import pathlib,subprocess,hashlib,json,importlib.util
r=pathlib.Path("/fast/scratch/hyaku/tameshi-r58/T58W2Read16/clone")
paths=[".ufo/evidence/round-18/defect-probes.py","tools/registry-check.py","tools/evidence-disposition.py","tools/bash-witness-study.py","tools/trace-inputs.py",".ufo/evidence/round-17/coldread/trace-inputs.py",".ufo/evidence/round-18/measure.py",".ufo/evidence/round-18/coldread/assemble.py",".ufo/evidence/round-18/coldread/ledger.json",".ufo/evidence/round-19/measure.py",".ufo/evidence/round-19/contract.json",".ufo/evidence/round-19/before.json",".ufo/evidence/round-19/coldread/measure.py",".ufo/evidence/round-19/coldread/ledger.json","corpus/lessons/round-19.md",".ufo/waves/round-18/w2/SentinelKillCode.md"]
for p in paths: print("POINTER",p,(r/p).is_file())
a=r/".ufo/evidence/round-17/coldread/trace-inputs.py"; b=r/"tools/trace-inputs.py"
print("historical-versus-promoted-byte-identical",a.read_bytes()==b.read_bytes())
base=subprocess.check_output(["git","-C",str(r),"show","2a32aa8228d5f86a85c81a923a3148bf792a9538:.ufo/evidence/round-17/coldread/trace-inputs.py"])
print("historical-unchanged-since-base",base==a.read_bytes())
for n,line in enumerate((r/"tools/mutate-and-run.sh").read_text().splitlines(),1):
 if n in (616,617): print(n,line)
d=json.loads((r/".ufo/evidence/round-18/dispositions.json").read_text()); print("historical_inputs",d["historical_inputs"]["tools/bash-witness-study.py"])
for p in ("corpus/SOURCES.md","corpus/QUALITY.md"):
 if (r/p).exists():
  for line in (r/p).read_text().splitlines():
   if "S049" in line or any("QUALITY"+str(i) in line for i in (37,38,39)): print(p,line)
