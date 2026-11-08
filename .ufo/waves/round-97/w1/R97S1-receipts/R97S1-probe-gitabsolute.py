#!/usr/bin/env python3
"""Probe: does the C2 'git-absolute' limit row's declared limit_mechanism hold?

The manifest row 'git-absolute' declares expect=limit with limit_mechanism
"sealed_env() pins PATH to /usr/local/bin:/usr/bin:/bin, so the bare name
resolves the same /usr/bin/git". The row's state is 'hostile-path', which
build_state() overrides with PATH=<shim>:/usr/local/bin:/usr/bin:/bin.
So: does the bare name 'git' resolve to /usr/bin/git, or to the shim?

Reuses guard-inertia.py's own build_state/run_checker so the fixture is the
one the matrix actually uses.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
TOOL = os.path.join(LANE, ".ufo/evidence/round-97/c2/guard-inertia.py")
CHECKER = ".ufo/evidence/round-96/conjunct-disposition-v96.py"
WORK = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else ".")

os.environ["HYAKU_SCRATCH"] = WORK
sys.path.insert(0, os.path.dirname(TOOL))
import importlib.util
spec = importlib.util.spec_from_file_location("gi", TOOL)
gi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gi)

env = gi.sealed_env()
base = tempfile.mkdtemp(dir=WORK, prefix="probe-gitabs-")
repo, rev, extra, env_over = gi.build_state("hostile-path", base, env)
print("store repo:", repo, "rev:", rev)
print("env_over:", env_over)

shim = os.path.join(base, "shim")
print("shim contents:", os.listdir(shim))
print("shim/git body:", open(os.path.join(shim, "git")).read())

# What does the bare name resolve to under this PATH?
e2 = gi.sealed_env(); e2.update(env_over)
r = subprocess.run(["sh", "-c", "command -v git; git --version"],
                   capture_output=True, text=True, env=e2)
print("PATH resolution under the row's env:")
print(r.stdout.strip())
print("stderr:", r.stderr.strip())

# The pristine and the mutant checker, exactly as the matrix builds them.
blob = subprocess.run(["git", "-C", LANE, "cat-file", "blob",
                        "e72a0c8bde44920554dc81c88c0dbb8dde491977:" + CHECKER],
                       capture_output=True).stdout
old = b'GIT = "/usr/bin/git"'
new = b'GIT = "git"'
assert blob.count(old) == 1, blob.count(old)
mut = blob.replace(old, new, 1)

cp = os.path.join(base, "checker-pristine.py")
mp = os.path.join(base, "checker-mutant.py")
open(cp, "wb").write(blob)
open(mp, "wb").write(mut)

pr = gi.run_checker(cp, repo, rev, extra, env_over)
mu = gi.run_checker(mp, repo, rev, extra, env_over)
print()
print("PRISTINE exit=%d" % pr[0])
print("pristine stdout+stderr:")
print(pr[1])
print("MUTANT   exit=%d" % mu[0])
print("mutant stdout+stderr:")
print(mu[1])
print()
print("outputs byte-identical:", pr[1] == mu[1])
print("exits identical:", pr[0] == mu[0])

# Does the mutant actually reach the shim git? Put a marker in the shim.
marker = os.path.join(base, "shim", "MARKER")
open(marker, "w").write("")
pr2 = gi.run_checker(cp, repo, rev, extra, env_over)
mu2 = gi.run_checker(mp, repo, rev, extra, env_over)
print()
print("re-run pristine exit=%d mutant exit=%d" % (pr2[0], mu2[0]))
print("outputs identical after shim marker:", pr2[1] == mu2[1])
print("pristine text repr:", repr(pr2[1][:400]))
print("mutant   text repr:", repr(mu2[1][:400]))
shutil.rmtree(base, ignore_errors=True)
