#!/usr/bin/env python3
"""Test the two C2 limit mechanisms against the checker code."""
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
TOOL = os.path.join(LANE, ".ufo/evidence/round-97/c2/guard-inertia.py")
CHECKER = os.path.join(LANE, ".ufo/evidence/round-96/conjunct-disposition-v96.py")
SCRATCH = "/fast/scratch/hyaku/tameshi-r97/R97C1"
os.environ["HYAKU_SCRATCH"] = SCRATCH

spec = importlib.util.spec_from_file_location("guard_inertia", TOOL)
gi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gi)

checker = open(CHECKER, "rb").read()
env = gi.sealed_env()

print("== verify-quiet: git rev-parse forms on an unresolvable 40-hex ==")
REV = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
for label, argv in (
        ("with --verify --quiet", ["rev-parse", "--verify", "--quiet", "--end-of-options", REV + "^{commit}"]),
        ("without them", ["rev-parse", "--end-of-options", REV + "^{commit}"]),
        ("bare rev-parse (manifest edit rev-unresolvable)", ["rev-parse", REV])):
    p = subprocess.run(["/usr/bin/git", "-C", LANE] + argv, capture_output=True, text=True, env=env)
    print("%-46s rc=%d stdout=%r stderr=%r" % (label, p.returncode, p.stdout, p.stderr.strip()[:100]))

print("\n== git-absolute: one edit vs the same edit plus the PATH pin removed ==")
base = os.path.join(SCRATCH, "limit-mech")
import shutil
shutil.rmtree(base, ignore_errors=True)
os.makedirs(base)
repo, rev, extra, env_over = gi.build_state("hostile-path", base, env)
shim = os.path.join(base, "shim")
print("fixture repo=%s rev=%s env_over=%r" % (repo, rev, env_over))

variants = {"pristine": checker}
one = checker.replace(b'GIT = "/usr/bin/git"', b'GIT = "git"', 1)
assert one != checker
variants["one-edit"] = one
pin_old = b'"PATH": "/usr/local/bin:/usr/bin:/bin"'
pin_new = ('"PATH": "%s:/usr/local/bin:/usr/bin:/bin"' % shim).encode()
print("PATH-pin anchor count in checker: %d" % checker.count(pin_old))
two = one.replace(pin_old, pin_new, 1)
assert two != one
variants["two-edit (GIT bare + PATH pin moved under the shim)"] = two

for name, blob in variants.items():
    path = os.path.join(base, "checker-%s.py" % name.split()[0])
    with open(path, "wb") as f:
        f.write(blob)
    code, out = gi.run_checker(path, repo, rev, extra, env_over)
    print("--- %s exit=%d" % (name, code))
    for line in out.splitlines()[:3]:
        print("    " + line)
