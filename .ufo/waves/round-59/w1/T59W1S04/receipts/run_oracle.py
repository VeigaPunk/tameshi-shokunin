#!/usr/bin/env python3
"""Run oracle against the original fixture (all classes on tools/runner.py)
and independently recompute git blob hashes from raw content."""
import hashlib
import json
import subprocess
import sys

BASE = "/fast/scratch/hyaku/tameshi-r59/T59W1S04"
REPO = f"{BASE}/fixture"
ORACLE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-59/w1/T59W1S04/stage/oracle_cell_runner_unrelated.py"

env = {}
with open(f"{BASE}/versions.env") as f:
    for line in f:
        k, _, v = line.strip().partition("=")
        env[k] = v

PATH = "tools/runner.py"
expected = {"equal": 0, "unrelated": 0, "unresolvable": 2,
            "changed": 1, "missing": 1, "symlink": 1}
token = {0: "EXECUTOR_SOURCE_BOUND", 1: "EXECUTOR_SOURCE_DRIFT",
         2: "EXECUTOR_SOURCE_UNAVAILABLE"}

results = []
for cls in ["equal", "unrelated", "changed", "missing", "symlink", "unresolvable"]:
    cand = env["TRUSTED"] if cls == "equal" else env[cls.upper()]
    out = subprocess.run(
        [sys.executable, "-I", ORACLE, "--repo", REPO, "--trusted", env["TRUSTED"],
         "--candidate", cand, "--path", PATH],
        capture_output=True, text=True)
    exp = expected[cls]
    ok = out.returncode == exp and token[exp] in (out.stdout + out.stderr)
    results.append({"class": cls, "expected_exit": exp,
                    "observed_exit": out.returncode,
                    "output": (out.stdout + out.stderr).strip(), "ok": ok})

print(json.dumps(results, indent=1))

# Independent blob hash recomputation (pure sha1, no git)
def githash(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

real = githash(b'print("real executor")\n')
forged = githash(b'print("forged success")\n')
link = githash(b"elsewhere.py")
print("RECOMPUTED real executor blob:", real, "(git said 74e4df76f9a60662749e2aaf076f67e311f66cdb)")
print("RECOMPUTED forged success blob:", forged, "(git said fbd2ab209ba4a77846c0898c79d4b579331975b7)")
print("RECOMPUTED symlink target blob:", link, "(git said a66620d9fcdca1d09c541464669234d720772947)")
print("ALL_ORACLE_OK:", all(r["ok"] for r in results))
