#!/usr/bin/env python3
"""R94R2 freeze-conformance + C2 manifest row-by-row audit (read-only).
Reads: plan, round-94 claims, counter/driver blobs at 7084358c, receipts dir,
conjunct-disposition.json. Prints a table; exit 0 always (report is the file)."""
import hashlib, json, re, subprocess, pathlib, sys
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "7084358c732ebe1334c2eb9a352c3ed96b547f7c"
EXP_COUNTER = "a22563b0c2b4a2b43922cec3d1ab3fa511110e035b9edfdfdc6eaebb97023010"
EXP_DRIVER = "9a0870c2e33b8634dcd9dbd28adbec3fe5178ba76cce9a94a16e9e063b4c6ecf"
def blob(rev, path):
    return subprocess.run(["git","-C",LANE,"cat-file","blob",rev+":"+path], capture_output=True).stdout
def sha(b): return hashlib.sha256(b).hexdigest()
print("counter sha:", sha(blob(REV,".ufo/evidence/round-94/c1/measure-v94.py")), "==expected", sha(blob(REV,".ufo/evidence/round-94/c1/measure-v94.py"))==EXP_COUNTER)
print("driver sha:", sha(blob(REV,".ufo/evidence/round-94/c1/controls-v94.py")), "==expected", sha(blob(REV,".ufo/evidence/round-94/c1/controls-v94.py"))==EXP_DRIVER)
# conjunct keys from counter --conjuncts
counter = pathlib.Path("/fast/scratch/hyaku/tameshi-r94/R94R2/measure-v94.py")
out = subprocess.run(["python3","-I",str(counter),"--conjuncts"],capture_output=True,text=True).stdout.strip()
keys = out.split()[1:20]
print("conjunct keys:", keys)
man = json.load(open(LANE+"/.ufo/evidence/round-94/conjunct-disposition.json"))
rows = man["rows"]
print("manifest keys:", sorted(rows))
print("missing:", [k for k in keys if k not in rows], "extra:", [k for k in rows if k not in keys])
base = pathlib.Path(LANE+"/.ufo/evidence/round-94/pre-freeze/controls")
for k,v in rows.items():
    st = v.get("state")
    if not st:
        print(f"{k:15s} UNFALS len={len(v.get('unfalsifiable',''))} 64hex={bool(re.search(r'[0-9a-f]{64}',v.get('unfalsifiable','')))}")
        continue
    p = base/f"{st}.out"
    t = p.read_text() if p.exists() else ""
    if v.get("mode")=="setup-refusal":
        print(f"{k:15s} state={st:18s} setup token found:", ("C1_SETUP "+v["token"] in t))
    else:
        m = re.search(r'C1_CONJUNCTS (.+)', t)
        d = dict(kv.split("=",1) for kv in m.group(1).split()) if m else {}
        print(f"{k:15s} state={st:18s} conj={d.get(k)} moves={d.get(k)=='false'}")
