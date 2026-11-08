#!/usr/bin/env python3
"""C1 oracle-trust test: a hand-written receipt that was never produced by the
counter, committed in a scratch clone, still counts matched."""
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tameshi-r97/R97C1"
CLONE = os.path.join(SCRATCH, "c1-forge-handwritten")
BINDER = os.path.join(LANE, ".ufo/evidence/round-97/c1/battery-bind.py")
DRIVER_SHA = "88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
RECEIPT = ".ufo/evidence/round-96/pre-freeze/controls/pos-real.out"

env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "HOME": os.path.join(SCRATCH, "home"), "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_NO_REPLACE_OBJECTS": "1"}
os.makedirs(env["HOME"], exist_ok=True)
GIT = "/usr/bin/git"


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, env=env, **kw)


if os.path.exists(CLONE):
    import shutil
    shutil.rmtree(CLONE)
r = run([GIT, "clone", "-q", "--shared", LANE, CLONE])
assert r.returncode == 0, r.stderr
top = run([GIT, "-C", CLONE, "rev-parse", "--show-toplevel"]).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(CLONE), (top, CLONE)
print("clone toplevel asserted: %s" % top)

body = open(os.path.join(CLONE, RECEIPT), "r", encoding="utf-8").read()
import re
sha = re.search(r"^counter_sha=([0-9a-f]{64})$", body, re.M).group(1)
# hand-written payload: never produced by measure-v96.py; the declared
# expectation only requires exit=0 and the PASS=true token.
forged = ("counter_sha=%s\nexit=0\nC1_R96_PASS=true\n"
          "hand-written by the critic; never executed measure-v96.py\n" % sha)
with open(os.path.join(CLONE, RECEIPT), "w", encoding="utf-8") as f:
    f.write(forged)
run([GIT, "-C", CLONE, "config", "user.name", "critic"])
run([GIT, "-C", CLONE, "config", "user.email", "critic@invalid"])
run([GIT, "-C", CLONE, "add", "-A"])
r = run([GIT, "-C", CLONE, "-c", "user.name=critic", "-c", "user.email=critic@invalid",
         "commit", "-qm", "hand-written receipt"])
assert r.returncode == 0, r.stderr
rev = run([GIT, "-C", CLONE, "rev-parse", "HEAD"]).stdout.strip()
print("rev=%s" % rev)
print("forged receipt body:\n%s" % forged)
r = run([sys.executable, "-I", BINDER, "--lane", CLONE, "--rev", rev,
         "--driver-sha", DRIVER_SHA])
print("binder rc=%d" % r.returncode)
print(r.stdout)
print(r.stderr)
sys.exit(0)
