#!/usr/bin/env python3
"""R95SN1: I04 corrected -- a refs/replace in the FLEET repo (the gate repo the
counter executes from), using a clone of the fleet root."""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
FLEET_SRC = "/home/vgpnk/Projects/shokunin"
COUNTER = S + "/snap/measure-v95.py"
SEAL = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null"}
RESULTS = []


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None, check=False, shell=False):
    if shell:
        p = subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True)
    else:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, p.stderr))
    return p


def clone(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", src, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def run_counter(lane, rev, work, counter=COUNTER, timeout=500):
    cmd = [sys.executable, "-I", counter, "--repo", lane, "--rev", rev, "--work", work]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"


def fresh_work(name):
    w = os.path.join(S, "wk1", name)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    return w


def j04_fleet_replace_ref():
    base = os.path.join(S, "atkB")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    lane = clone(LANE_SRC, os.path.join(base, "lane"))
    fl = clone(FLEET_SRC, os.path.join(base, "fleet"))
    spec_p = os.path.join(lane, ".ufo/evidence/round-95/c1/census-mutants.json")
    spec = json.load(open(spec_p))
    gc, gp = spec["gate"]["commit"], spec["gate"]["path"]
    have = sh(["git", "-C", fl, "cat-file", "blob", gc + ":" + gp], env=SEAL)
    assert have.returncode == 0, "fleet clone lacks the gate blob"
    real = sh(["git", "-C", fl, "rev-parse", gc + ":" + gp], env=SEAL).stdout.strip()
    evil = sh("git -C %s hash-object -w --stdin <<'EOF'\n#!/bin/sh\nexit 0\nEOF" % fl,
              shell=True, env=SEAL).stdout.strip()
    sh(["git", "-C", fl, "replace", real, evil], env=SEAL)
    listing = sh(["git", "-C", fl, "replace", "-l"], env=SEAL).stdout.strip()
    # repoint the spec at the clone
    spec["gate"]["repo"] = fl
    json.dump(spec, open(spec_p, "w"), indent=1)
    sh(["git", "-C", lane, "add", "-A"], env=SEAL)
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", "gate repo repointed"], env=SEAL)
    rc, out = run_counter(lane, "HEAD", fresh_work("j04"))
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS", "C1_SUMMARY"))]
    ok = "replace-refs-present:fleet" in out
    rec("J04", "refs/replace on the GATE blob inside the FLEET repo the counter executes from "
               "(fleet clone carries %s)" % listing[:20],
        "exit=%s out=%r" % (rc, got[:3]),
        "exit 2, C1_SETUP replace-refs-present:fleet (the counter checks the fleet repo too)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def j05_control_no_replace():
    """control: the same fixture WITHOUT the replace ref must proceed."""
    base = os.path.join(S, "atkC")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    lane = clone(LANE_SRC, os.path.join(base, "lane"))
    fl = clone(FLEET_SRC, os.path.join(base, "fleet"))
    spec_p = os.path.join(lane, ".ufo/evidence/round-95/c1/census-mutants.json")
    spec = json.load(open(spec_p))
    spec["gate"]["repo"] = fl
    json.dump(spec, open(spec_p, "w"), indent=1)
    sh(["git", "-C", lane, "add", "-A"], env=SEAL)
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", "gate repo repointed"], env=SEAL)
    rc, out = run_counter(lane, "HEAD", fresh_work("j05"))
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS", "C1_SUMMARY"))]
    rec("J05", "control: the same fleet-clone fixture WITHOUT a replace ref must proceed "
               "past the fleet replace check",
        "exit=%s out=%r" % (rc, got[:3]),
        "without a replace ref the counter must NOT print replace-refs-present:fleet",
        "INFO", "observed")


def main():
    os.makedirs(os.path.join(S, "atkB"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [j04_fleet_replace_ref, j05_control_no_replace]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-40s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-fleet-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
