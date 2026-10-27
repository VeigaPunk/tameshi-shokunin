import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool10"
CLONE = os.path.join(S, "clone")
env = dict(os.environ)
env["TMPDIR"] = os.path.join(S, "tmp")

base = open(os.path.join(CLONE, ".ufo/evidence/round-13/pin-manifest.json")).read()
needle = '"schema": "pin-manifest-v1"'
repl = '"schema": "pin-manifest-v1", "note": ' + ("9" * 5000) + ","
p = os.path.join(S, "bigint2.json")
open(p, "w").write(base.replace(needle, repl, 1))
print("wrote", p, "size", os.path.getsize(p))

r = subprocess.run(
    [sys.executable, "tools/pin-disposition.py", "--manifest", p,
     "--root", "/home/vgpnk/Projects/shokunin"],
    cwd=CLONE, stdin=subprocess.DEVNULL, capture_output=True, env=env)
print("EXIT =", r.returncode)
err = r.stderr.decode(errors="replace").strip().split("\n")
print("stderr last 3:")
for l in err[-3:]:
    print("   ", l[:130])
print("stdout bytes:", len(r.stdout))

src = open(os.path.join(S, "pin-disposition.cand.py")).read()
i = src.find("except json.JSONDecodeError")
print("--- read_manifest except context ---")
print(src[i - 300:i + 200])
