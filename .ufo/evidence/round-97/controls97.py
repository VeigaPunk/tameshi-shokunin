#!/usr/bin/env python3
"""Round-97 pre-freeze controls: the failing-before no-work control and the
forgery controls for both claims, executed and written as receipts before the
claims freeze (Amendment 59/60 prerequisite).

C1 (battery binder): nowork (no committed tool prints BATTERY states= at the
base), positive at the instrument rev, and five forgeries — a receipt deleted
from the index, a working-tree-only receipt, a counter_sha edit, an exit edit,
a conjunct flip — plus a driver-digest mismatch and the shipped selftest.
C2 (guard-inertia): nowork (no committed tool prints GUARD_INERTIA at the base),
positive at the instrument rev, the shipped selftest, a flipped-expectation
manifest (must survive and exit 1) and a no-op edit manifest (must refuse).

Usage: python3 -I .ufo/evidence/round-97/controls97.py --lane LANE --base BASE \
         --rev INSTRUMENTS_REV --work EMPTY_DIR --outdir DIR
Exit: 0 every receipt carries its pre-registered verdict; 1 otherwise.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

GIT = "/usr/bin/git"


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def sh(argv, cwd=None, check=True):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=sealed_env())
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(argv), p.stderr))
    return p


def git(repo, *args, check=True):
    return sh([GIT, "-C", repo] + list(args), check=check)


def clone_at(lane, rev, dest):
    git(dest.rsplit("/", 1)[0] if False else lane, "clone", "-q", "--shared", lane, dest)
    git(dest, "checkout", "-q", "--detach", rev)
    git(dest, "config", "user.name", "r97-control")
    git(dest, "config", "user.email", "r97-control@invalid")
    return dest


def commit(repo, msg, add=True):
    if add:
        git(repo, "add", "-A")
    git(repo, "commit", "-qm", msg)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def write(outdir, name, body, code):
    path = os.path.join(outdir, name + ".out")
    with open(path, "w", encoding="utf-8") as f:
        f.write(body if body.endswith("\n") else body + "\n")
        f.write("rc=%d\n" % code)
    return name, code, body


def run(argv, env=None):
    p = subprocess.run(argv, capture_output=True, text=True, env=env or sealed_env())
    return p.returncode, p.stdout + p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    os.makedirs(a.outdir, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    if os.listdir(a.work):
        raise SystemExit("work-not-empty")
    T = os.path.join(lane, ".ufo/evidence/round-97")
    receipts = []
    env = sealed_env()
    env["HYAKU_SCRATCH"] = a.work

    def add(name, code, body, want_code):
        receipts.append((name, code, body, want_code))

    # ---- C1 nowork: nothing at the base prints the line -------------------
    g = sh([GIT, "-C", lane, "grep", "-c", "BATTERY states=", a.base], check=False)
    add("c1-nowork-bind-absent", g.returncode,
        "git grep BATTERY-states at base %s: rc=%d out=%r" % (a.base, g.returncode, g.stdout.strip()), 1)
    _cf = git(lane, "cat-file", "-e", "8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b:"
               ".ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt", check=False)
    add("c1-nowork-summary-absent", _cf.returncode,
        "git cat-file -e %s:.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt: rc=%d"
        % ("8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b", _cf.returncode), 128)

    # ---- C1 positive at the instrument rev --------------------------------
    binder = os.path.join(T, "c1/battery-bind.py")
    code, out = run([sys.executable, "-I", binder, "--lane", lane, "--rev", a.rev])
    add("c1-positive", code, out, 0)
    code, out = run([sys.executable, "-I", binder, "--selftest"])
    add("c1-selftest", code, out, 0)

    # ---- C1 forgeries: one shared clone at the instrument rev -------------
    st = clone_at(lane, a.rev, os.path.join(a.work, "c1-forge"))
    c = ".ufo/evidence/round-96/pre-freeze/controls/pos-real.out"
    orig = open(os.path.join(st, c), encoding="utf-8").read()
    # (a) deleted from the index, left in the working tree -> missing
    os.remove(os.path.join(st, c))
    with open(os.path.join(st, c), "w", encoding="utf-8") as f:
        f.write(orig)
    git(st, "rm", "-q", "--cached", c)
    r = commit(st, "drop pos-real from index", add=False)
    code, out = run([sys.executable, "-I", binder, "--lane", st, "--rev", r])
    add("c1-forge-worktree-only", code, out, 1)
    # (b) counter_sha edit -> mismatched
    git(st, "reset", "-q", "--hard", r)
    txt = open(os.path.join(st, c), encoding="utf-8").read()
    ntxt = re.sub(r"counter_sha=[0-9a-f]{64}", "counter_sha=" + "0" * 64, txt, count=1)
    assert ntxt != txt
    open(os.path.join(st, c), "w", encoding="utf-8").write(ntxt)
    r = commit(st, "counter-sha edit")
    code, out = run([sys.executable, "-I", binder, "--lane", st, "--rev", r])
    add("c1-forge-counter-sha", code, out, 1)
    # (c) exit edit -> mismatched
    git(st, "reset", "-q", "--hard", r)
    body = open(os.path.join(st, c), encoding="utf-8").read()
    open(os.path.join(st, c), "w", encoding="utf-8").write(
        re.sub(r"exit=\d+", "exit=7", body, count=1))
    r = commit(st, "exit edit")
    code, out = run([sys.executable, "-I", binder, "--lane", st, "--rev", r])
    add("c1-forge-exit", code, out, 1)
    # (d) conjunct flip -> mismatched
    git(st, "reset", "-q", "--hard", r)
    body = open(os.path.join(st, c), encoding="utf-8").read()
    assert "C1_R96_PASS=true" in body
    open(os.path.join(st, c), "w", encoding="utf-8").write(
        body.replace("C1_R96_PASS=true", "C1_R96_PASS=false", 1))
    r = commit(st, "pass-payload edit")
    code, out = run([sys.executable, "-I", binder, "--lane", st, "--rev", r])
    add("c1-forge-payload", code, out, 1)
    # (e) driver digest mismatch at the real lane (pin not equal)
    code, out = run([sys.executable, "-I", binder, "--lane", lane, "--rev", a.rev,
                     "--driver-sha", "0" * 64])
    add("c1-forge-driver-sha", code, out, 2)

    # ---- C2 nowork + positive + controls ---------------------------------
    g = sh([GIT, "-C", lane, "grep", "-c", "GUARD_INERTIA", a.base], check=False)
    add("c2-nowork-absent", 0,
        "git grep GUARD_INERTIA at base %s: rc=%d out=%r" % (a.base, g.returncode, g.stdout.strip()), 0)
    tool = os.path.join(T, "c2/guard-inertia.py")
    man_sha = hashlib.sha256(open(os.path.join(T, "c2/guard-inertia.json"), "rb").read()).hexdigest()
    code, out = run([sys.executable, "-I", tool, "--lane", lane, "--rev", a.rev,
                     "--manifest-sha", man_sha])
    add("c2-positive", code, out, 0)
    code, out = run([sys.executable, "-I", tool, "--selftest"])
    add("c2-selftest", code, out, 0)
    man = json.load(open(os.path.join(T, "c2/guard-inertia.json"), encoding="utf-8"))
    st2 = clone_at(lane, a.rev, os.path.join(a.work, "c2-forge"))
    mp = ".ufo/evidence/round-97/c2/guard-inertia.json"
    # (a) a killed row declared limit -> survived, exit 1
    flipped = json.loads(json.dumps(man))
    # flip a measured `limit` row to `killed`: its two runs are identical, so the
    # observation must contradict the pre-registered expectation (survived, exit 1).
    _lim = [r for r in flipped["rows"] if r["expect"] == "limit"][0]
    _lim["expect"] = "killed"
    _lim.pop("limit_mechanism", None)
    flipped_b = (json.dumps(flipped, indent=1) + "\n").encode()
    open(os.path.join(st2, mp), "wb").write(flipped_b)
    r = commit(st2, "flip expectation")
    code, out = run([sys.executable, "-I", tool, "--lane", st2, "--rev", r,
                     "--manifest-sha", hashlib.sha256(flipped_b).hexdigest()])
    add("c2-forge-flipped-expect", code, out, 1)
    # (b) a no-op edit -> GUARD_SETUP edit-no-op, exit 2
    git(st2, "reset", "-q", "--hard", r)
    noop = json.loads(json.dumps(man))
    noop["rows"][0]["edit"]["new"] = noop["rows"][0]["edit"]["old"]
    noop_b = (json.dumps(noop, indent=1) + "\n").encode()
    open(os.path.join(st2, mp), "wb").write(noop_b)
    r = commit(st2, "no-op edit")
    code, out = run([sys.executable, "-I", tool, "--lane", st2, "--rev", r,
                     "--manifest-sha", hashlib.sha256(noop_b).hexdigest()])
    add("c2-forge-noop", code, out, 2)
    # (c) a substituted manifest under the pinned digest -> manifest-sha-mismatch
    git(st2, "reset", "-q", "--hard", r)
    subst = json.loads(json.dumps(man))
    subst["rows"][0]["edit"]["old"] = "DISPOSITION rows="
    subst["rows"][0]["edit"]["new"] = "DISPOSITION rowz="
    open(os.path.join(st2, mp), "w", encoding="utf-8").write(json.dumps(subst, indent=1) + "\n")
    r = commit(st2, "substituted manifest")
    code, out = run([sys.executable, "-I", tool, "--lane", st2, "--rev", r,
                     "--manifest-sha", man_sha])
    add("c2-forge-manifest-subst", code, out, 2)
    # (d) an empty manifest -> manifest-empty
    git(st2, "reset", "-q", "--hard", r)
    open(os.path.join(st2, mp), "w", encoding="utf-8").write(json.dumps({"rows": {}}, indent=1) + "\n")
    r = commit(st2, "empty manifest")
    code, out = run([sys.executable, "-I", tool, "--lane", st2, "--rev", r,
                     "--manifest-sha", hashlib.sha256(
                         json.dumps({"rows": {}}, indent=1).encode() + b"\n").hexdigest()])
    add("c2-forge-manifest-empty", code, out, 2)

    bad = 0
    for name, code, body, want in receipts:
        write(a.outdir, name, body, code)
        ok = code == want
        if not ok:
            bad += 1
        print("%s %s rc=%d want=%d" % (name, "MATCH" if ok else "MISMATCH", code, want))
    print("CONTROLS97 states=%d matched=%d mismatched=%d" % (
        len(receipts), len(receipts) - bad, bad))
    shutil.rmtree(st, ignore_errors=True)
    shutil.rmtree(st2, ignore_errors=True)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
