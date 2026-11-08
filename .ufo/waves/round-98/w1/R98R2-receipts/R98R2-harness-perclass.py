#!/usr/bin/env python3
"""Independent per-class replay of the C2 fixtures against the frozen tool blob.

Mirrors guard-refusals.py's fixture mutations and invocation, but prints every
line of the tool's stdout per class plus its exit, so each class's declared
branch is visible instead of folded into one summary line.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

GIT = "/usr/bin/git"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "764aca97e513d650949999362cd4b0f5f0e566a5"
S = "/fast/scratch/hyaku/tameshi-r98/R98R2"
WORK = os.path.join(S, "pc-work")
TOOL = os.path.join(S, "src", "guard-inertia.py")
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
CLASSES = ["edit-no-op", "edit-ambiguous", "state-unbuildable",
           "limit-mechanism-missing", "manifest-sha-mismatch", "manifest-empty"]


def env_for(home):
    os.makedirs(home, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "HOME": home, "TMPDIR": home, "HYAKU_SCRATCH": home,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def run(argv, env, cwd=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def git(repo, args, env):
    return run([GIT, "-C", repo] + args, env)


def fixture_manifest(base, name):
    man = json.loads(json.dumps(base))
    rows = man["rows"]
    if name == "edit-no-op":
        rows[0]["edit"]["new"] = rows[0]["edit"]["old"]
    elif name == "edit-ambiguous":
        rows[0]["edit"]["old"] = "DISPOSITION"
    elif name == "state-unbuildable":
        rows[0]["state"] = "no-such-state-r98"
    elif name == "limit-mechanism-missing":
        rows[0]["expect"] = "limit"
        rows[0]["limit_mechanism"] = "too short"
    elif name == "manifest-empty":
        man = {"rows": {}}
    elif name == "manifest-sha-mismatch":
        pass
    else:
        raise ValueError(name)
    return (json.dumps(man, indent=1) + "\n").encode()


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    env = env_for(WORK)
    clone = os.path.join(WORK, "clone")
    r = run([GIT, "clone", "-q", "--shared", LANE, clone], env)
    assert r[0] == 0, r[2]
    git(clone, ["checkout", "-q", "--detach", REV], env)
    git(clone, ["config", "user.name", "r98r2"], env)
    git(clone, ["config", "user.email", "r98r2@invalid"], env)
    man_path = os.path.join(clone, MANIFEST)
    man_bytes = open(man_path, "rb").read()
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    base = json.loads(man_bytes)
    print("MANIFEST sha256=%s rows=%d first_id=%s" % (man_sha, len(base["rows"]), base["rows"][0]["id"]))
    for name in CLASSES:
        git(clone, ["reset", "-q", "--hard", REV], env)
        fixture = fixture_manifest(base, name)
        fsha = hashlib.sha256(fixture).hexdigest()
        if name == "manifest-sha-mismatch":
            fsha = hashlib.sha256(fixture + b"x").hexdigest()
        open(man_path, "wb").write(fixture)
        status = git(clone, ["status", "--porcelain"], env)[1].strip()
        if status:
            git(clone, ["add", "-A"], env)
            git(clone, ["-c", "user.name=r98r2", "-c", "user.email=r98r2@invalid",
                        "commit", "-qm", "fixture " + name], env)
            frev = git(clone, ["rev-parse", "HEAD"], env)[1].strip()
        else:
            frev = REV
        scratch = os.path.join(WORK, "scratch")
        shutil.rmtree(scratch, ignore_errors=True)
        rc, out, err = run([sys.executable, "-I", TOOL, "--lane", clone, "--rev", frev,
                            "--manifest-sha", fsha], env_for(scratch))
        print("=== CLASS %s rev=%s fixture_sha=%s rc=%d" % (name, frev[:12], fsha, rc))
        for line in out.splitlines():
            print("    OUT| " + line)
        if err.strip():
            for line in err.splitlines()[:5]:
                print("    ERR| " + line)
    # positive: committed manifest, committed rev
    git(clone, ["reset", "-q", "--hard", REV], env)
    scratch = os.path.join(WORK, "scratch")
    shutil.rmtree(scratch, ignore_errors=True)
    rc, out, err = run([sys.executable, "-I", TOOL, "--lane", clone, "--rev", REV,
                        "--manifest-sha", man_sha], env_for(scratch))
    print("=== POSITIVE rev=%s rc=%d" % (REV[:12], rc))
    for line in out.splitlines():
        print("    OUT| " + line)


if __name__ == "__main__":
    main()
