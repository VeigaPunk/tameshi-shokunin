#!/usr/bin/env python3
"""C2 do-nothing, exact counter form: a committed manifest of non-guard edits
in a scratch clone prints the frozen predicate with the claim's counter flags."""
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tameshi-r97/R97C1"
CLONE = os.path.join(SCRATCH, "c2-clone-trivial")
TOOL = ".ufo/evidence/round-97/c2/guard-inertia.py"
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
CHECKER_SHA = "02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
GIT = "/usr/bin/git"
env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "HOME": os.path.join(SCRATCH, "home"), "HYAKU_SCRATCH": SCRATCH,
       "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_NO_REPLACE_OBJECTS": "1"}
os.makedirs(env["HOME"], exist_ok=True)


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, env=env, **kw)


def fresh_clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    r = run([GIT, "clone", "-q", "--shared", LANE, dest])
    assert r.returncode == 0, r.stderr
    top = run([GIT, "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), (top, dest)
    run([GIT, "-C", dest, "config", "user.name", "critic"])
    run([GIT, "-C", dest, "config", "user.email", "critic@invalid"])


def commit_all(dest, msg):
    run([GIT, "-C", dest, "add", "-A"])
    r = run([GIT, "-C", dest, "-c", "user.name=critic", "-c", "user.email=critic@invalid",
             "commit", "-qm", msg])
    assert r.returncode == 0, r.stderr
    return run([GIT, "-C", dest, "rev-parse", "HEAD"]).stdout.strip()


def rows_trivial():
    rows = []
    for i in range(8):
        rows.append({"id": "trivial-kill-%d" % i,
                     "guard": "NOT A GUARD: an unrelated summary-token print",
                     "edit": {"old": "DISPOSITION rows=", "new": "DISPOSITION rowz="},
                     "state": "clean",
                     "pristine": {"exit": 0, "token": "DISPOSITION rows="},
                     "expect": "killed"})
    for i in range(2):
        rows.append({"id": "trivial-limit-%d" % i,
                     "guard": "NOT A GUARD: an inert byte change",
                     "edit": {"old": "MIN_REASON = 40", "new": "MIN_REASON = 40 "},
                     "state": "clean",
                     "pristine": {"exit": 0, "token": "DISPOSITION rows="},
                     "expect": "limit",
                     "limit_mechanism": "an appended space to an unprinted constant; exit and token identical"})
    return {"rows": rows}


def run_counter(clone, rev, label):
    print("===== %s rev=%s =====" % (label, rev))
    r = run([sys.executable, "-I", os.path.join(clone, TOOL), "--lane", clone, "--rev", rev,
             "--checker-sha", CHECKER_SHA])
    print(r.stdout)
    print(r.stderr)
    print("rc=%d" % r.returncode)
    return r.returncode


# arm 1: the committed manifest replaced by a coherent non-guard manifest
fresh_clone(CLONE)
with open(os.path.join(CLONE, MANIFEST), "w", encoding="utf-8") as f:
    f.write(json.dumps(rows_trivial(), indent=1) + "\n")
rev = commit_all(CLONE, "non-guard manifest")
run_counter(CLONE, rev, "non-guard manifest")

# arm 2: an all-zero/empty manifest
fresh_clone(CLONE)
with open(os.path.join(CLONE, MANIFEST), "w", encoding="utf-8") as f:
    f.write(json.dumps({"rows": []}, indent=1) + "\n")
rev = commit_all(CLONE, "empty manifest")
run_counter(CLONE, rev, "empty manifest")

# arm 3: control — the frozen manifest at the same clone revision style
fresh_clone(CLONE)
rev = run([GIT, "-C", CLONE, "rev-parse", "HEAD"]).stdout.strip()
run_counter(CLONE, rev, "frozen manifest")
sys.exit(0)
