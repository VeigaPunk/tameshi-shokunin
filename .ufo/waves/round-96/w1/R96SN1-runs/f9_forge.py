#!/usr/bin/env python3
"""R96SN1 F9 attack: forge a receipt whose counter_sha= is copied from the
honest counter blob while the body is forged. Does the v96 checker accept it?

Method: clone the lane at the freeze rev, commit a hand-written receipt
carrying the honest counter blob's sha256 (publicly computable from the
object store) plus a forged C1_CONJUNCTS body. No counter run, no driver.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r96/R96SN1"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "be6c22b6d8a94f07eee6b0fa79edab7df228c0b0"
COUNTER = ".ufo/evidence/round-96/c1/measure-v96.py"
RECEIPTS = ".ufo/evidence/round-96/pre-freeze/controls"
MANIFEST = ".ufo/evidence/round-96/conjunct-disposition.json"

ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LC_ALL": "C.UTF-8",
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(repo, *a):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True, env=ENV)
    return p.returncode, p.stdout, p.stderr


def main():
    work = os.path.join(S, "f9")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    dest = os.path.join(work, "repo")
    top = os.path.realpath(S)
    rc, out, err = git(dest, "clone")
    # clone explicitly
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, dest],
                   check=True, env=ENV)
    assert os.path.realpath(dest) == os.path.realpath(dest)
    subprocess.run(["git", "-C", dest, "checkout", "-q", "--detach", REV],
                   check=True, env=ENV)

    # honest counter blob sha at REV (public: it is in the object store)
    rc, cb, err = git(dest, "cat-file", "blob", REV + ":" + COUNTER)
    assert rc == 0, err
    honest_sha = hashlib.sha256(cb).hexdigest()
    print("honest counter blob sha256 =", honest_sha)

    # the manifest's rows -> which states are needed
    rc, mb, err = git(dest, "cat-file", "blob", REV + ":" + MANIFEST)
    rows = json.loads(mb)["rows"]
    needed = {}
    for k, v in rows.items():
        if "unfalsifiable" in v:
            continue
        needed.setdefault(v["state"], []).append((k, v))

    rdir = os.path.join(dest, RECEIPTS)
    os.makedirs(rdir, exist_ok=True)
    for state, entries in needed.items():
        conj = []
        for k, v in entries:
            if v["mode"] == "setup-refusal":
                body = "exit=2\nC1_SETUP " + v["token"] + "\n"
                conj.append(("setup", body))
            else:
                conj.append(("conjunct-false", k))
        # Forge: claim EVERY conjunct it is responsible for is false.
        lines = ["counter_sha=" + honest_sha, "exit=1"]
        cj = []
        for kind, payload in conj:
            if kind == "setup":
                lines.append(payload.strip())
            else:
                cj.append(payload + "=false")
        if cj:
            lines.append("C1_CONJUNCTS " + " ".join(cj))
        lines.append("C1_R96_PASS=false")
        with open(os.path.join(rdir, state + ".out"), "w") as f:
            f.write("\n".join(lines) + "\n")
    print("wrote %d forged receipts" % len(needed))

    subprocess.run(["git", "-C", dest, "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", dest, "-c", "user.name=forge",
                    "-c", "user.email=forge@invalid", "commit", "-q", "-m",
                    "forged receipts (counter_sha copied from honest blob)"],
                   check=True, env=ENV)
    newrev = subprocess.run(["git", "-C", dest, "rev-parse", "HEAD"],
                            capture_output=True, text=True, env=ENV).stdout.strip()
    print("forged rev =", newrev)

    chk = os.path.join(dest, ".ufo/evidence/round-96/conjunct-disposition-v96.py")
    p = subprocess.run([sys.executable, "-I", chk, "--lane", dest, "--rev", newrev,
                        "--min-falsifiable", "17", "--counter", COUNTER],
                       capture_output=True, text=True)
    print("=== checker output ===")
    print(p.stdout)
    print("stderr:", p.stderr[-500:])
    print("CHECKER EXIT =", p.returncode)
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
