#!/usr/bin/env python3
"""C1 wording test: the claim says a counter_sha= edit prints a nonzero
mismatched count; the binder's code exempts receipts carrying `mutant=Dnn`."""
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tameshi-r97/R97C1"
CLONE = os.path.join(SCRATCH, "c1-forge-mutant-sha")
BINDER = os.path.join(LANE, ".ufo/evidence/round-97/c1/battery-bind.py")
DRIVER_SHA = "88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
RECEIPT = ".ufo/evidence/round-96/pre-freeze/controls/D01.out"
GIT = "/usr/bin/git"
env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "HOME": os.path.join(SCRATCH, "home"), "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_NO_REPLACE_OBJECTS": "1"}
os.makedirs(env["HOME"], exist_ok=True)


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env, **kw)


if os.path.exists(CLONE):
    shutil.rmtree(CLONE)
r = run([GIT, "clone", "-q", "--shared", LANE, CLONE])
assert r.returncode == 0, r.stderr
top = run([GIT, "-C", CLONE, "rev-parse", "--show-toplevel"]).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(CLONE), (top, CLONE)
print("clone toplevel asserted: %s" % top)

path = os.path.join(CLONE, RECEIPT)
body = open(path, encoding="utf-8").read()
print("original first three lines:\n%s" % "\n".join(body.splitlines()[:3]))
new = re.sub(r"^counter_sha=[0-9a-f]{64}$", "counter_sha=" + "0" * 64, body, count=1, flags=re.M)
assert new != body
open(path, "w", encoding="utf-8").write(new)
run([GIT, "-C", CLONE, "add", "-A"])
r = run([GIT, "-C", CLONE, "-c", "user.name=critic", "-c", "user.email=critic@invalid",
         "commit", "-qm", "mutant receipt counter_sha edit"])
assert r.returncode == 0, r.stderr
rev = run([GIT, "-C", CLONE, "rev-parse", "HEAD"]).stdout.strip()
print("=== binder on the edited mutant receipt (rev %s) ===" % rev)
r = run([sys.executable, "-I", BINDER, "--lane", CLONE, "--rev", rev, "--driver-sha", DRIVER_SHA])
print(r.stdout)
print("rc=%d" % r.returncode)
sys.exit(0)
