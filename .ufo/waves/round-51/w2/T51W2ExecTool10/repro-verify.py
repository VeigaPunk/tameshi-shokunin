#!/usr/bin/env python3
"""T51W2ExecTool10 consolidated verification for the C3 pin-disposition row."""
import json
import os
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool10"
CLONE = os.path.join(S, "clone")
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CAND = "6d8c11e378aa90b12650808e1b79270742935f15"
TOOL = "tools/pin-disposition.py"
MANIFEST = ".ufo/evidence/round-13/pin-manifest.json"

env = dict(os.environ)
env["TMPDIR"] = os.path.join(S, "tmp")
os.makedirs(env["TMPDIR"], exist_ok=True)

out = []


def emit(k, v):
    out.append("%-46s %s" % (k, v))
    print("%-46s %s" % (k, v))


def run(argv, label, cwd=CLONE, e=None):
    t0 = time.time()
    r = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                       capture_output=True, env=e or env)
    dt = time.time() - t0
    lines = [l for l in r.stdout.decode(errors="replace").split("\n") if l.strip()]
    last = lines[-1].strip() if lines else ""
    err = r.stderr.decode(errors="replace").strip().split("\n")
    emit(label, "exit=%d wall=%.3fs last=%r%s" % (
        r.returncode, dt, last[:70],
        (" ERR:" + err[-1][:90]) if err and err[0] else ""))
    return r.returncode, last, r.stdout, r.stderr


# 1. row's exact backticked self-test command
run(["python3", TOOL, "--selftest"], "1 row self-test (exact backtick cmd)")
# 2. usage probe
run(["python3", TOOL, "--r51-no-such-flag"], "2 usage probe --r51-no-such-flag")
# 3. entry command against the real fleet root
rc, last, sout, serr = run(
    ["python3", TOOL, "--manifest", MANIFEST, "--root", "/home/vgpnk/Projects/shokunin"],
    "3 entry cmd vs real fleet root")
try:
    d = json.loads(sout)
    emit("3b entry counts (exit-0 with drift?)", json.dumps(d["counts"]))
    emit("3c exit-0 means 'clean'? legs changed",
         "%d changed / %d unchanged" % (d["counts"]["changed"], d["counts"]["unchanged"]))
except Exception as exc:
    emit("3b entry counts", "unparsed %s" % exc)

# 4. run-mode exit-1 path outside the selftest (uncaught exception)
deep = os.path.join(S, "deep2.json")
if not os.path.exists(deep):
    open(deep, "w").write("[" * 100000 + "]" * 100000)
rc, last, sout, serr = run(["python3", TOOL, "--manifest", deep, "--root", "/tmp"],
                           "4 run mode, 100k-deep JSON manifest")
emit("4b is that a selftest FAIL?", "NO: run mode, manifest path")
emit("4c traceback present?", "yes" if b"Traceback" in serr else "no")

# 5. verdict map coverage: every code the tool can exit with
codes = {}
for label, argv in [
    ("selftest", ["python3", TOOL, "--selftest"]),
    ("usage", ["python3", TOOL, "--r51-no-such-flag"]),
    ("help", ["python3", TOOL, "--help"]),
    ("no args", ["python3", TOOL]),
    ("selftest+arg", ["python3", TOOL, "--selftest", "--root", "x"]),
    ("missing manifest", ["python3", TOOL, "--manifest", "/nonexistent.json", "--root", "/tmp"]),
    ("root not a dir", ["python3", TOOL, "--manifest", MANIFEST, "--root", deep]),
    ("7-leg manifest", ["python3", TOOL, "--manifest", os.path.join(S, "sevenlegs.json"),
                        "--root", "/home/vgpnk/Projects/shokunin"]),
    ("run-mode crash", ["python3", TOOL, "--manifest", deep, "--root", "/tmp"]),
]:
    rc, last, sout, serr = run(argv, "5 code probe: %s" % label)
    codes[label] = rc
emit("5b observed exit codes", json.dumps(codes))

# 6. selftest with git unavailable -> COULD_NOT_EVALUATE
emptybin = os.path.join(S, "emptybin")
os.makedirs(emptybin, exist_ok=True)
e2 = dict(env)
e2["PATH"] = emptybin
run([sys.executable, TOOL, "--selftest"], "6 selftest with git off PATH", e=e2)

# 7. pinned value load-bearing
mut = os.path.join(S, "mutated-manifest.json")
d = json.load(open(os.path.join(CLONE, MANIFEST)))
d["legs"][0]["expected_sha256"] = "0" * 64
json.dump(d, open(mut, "w"))
rc, last, sout, serr = run(["python3", TOOL, "--manifest", mut,
                            "--root", "/home/vgpnk/Projects/shokunin"],
                           "7 entry cmd w/ mutated pinned sha")
try:
    d = json.loads(sout)
    emit("7b pinned value is load-bearing",
         "leg0 content_status=%s pinned.status=%s" % (
             d["legs"][0]["content_status"], d["legs"][0]["pinned"]["status"]))
except Exception as exc:
    emit("7b pinned value", "unparsed %s" % exc)

# 8. residue after a clean PASS run
import glob
for p in glob.glob("/tmp/tameshi-r13-pin-disposition-selftest.*"):
    subprocess.run(["rm", "-rf", p])
run(["python3", TOOL, "--selftest"], "8 clean PASS run")
res = glob.glob("/tmp/tameshi-r13-pin-disposition-selftest.*")
emit("8b residue after PASS (row claims removed)",
     "count=%d %s" % (len(res), res))

# 9. sibling repos untouched by the entry command
def sig(repo):
    r = subprocess.run(["git", "-C", repo, "status", "--porcelain"],
                       capture_output=True)
    return r.stdout.decode(errors="replace").strip()


before = {r: sig(os.path.join("/home/vgpnk/Projects/shokunin", r))
          for r in ("kumitate-shokunin", "kagi-shokunin", "tsukuroi-shokunin", "mado-shokunin")}
run(["python3", TOOL, "--manifest", MANIFEST, "--root", "/home/vgpnk/Projects/shokunin"],
   "9 entry cmd again (sibling write check)")
after = {r: sig(os.path.join("/home/vgpnk/Projects/shokunin", r)) for r in before}
emit("9b sibling repo status unchanged",
     str(before == after))

with open(os.path.join(S, "verify-results.txt"), "w") as h:
    h.write("\n".join(out) + "\n")
