#!/usr/bin/env python3
"""Attack (a): embed the class tokens in manifest string fields the tool never prints.

Grades the tool's real stdout with the battery's own grading functions (loaded
from the frozen battery blob) to show whether any count moves.
"""
import hashlib
import importlib.util
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
CLONE = os.path.join(WORK, "clone")
TOOL = os.path.join(S, "src", "guard-inertia.py")
BATTERY = os.path.join(S, "src", "guard-refusals.py")
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
CLASSES = ["edit-no-op", "edit-ambiguous", "state-unbuildable",
           "limit-mechanism-missing", "manifest-sha-mismatch", "manifest-empty"]


def env_for(home):
    os.makedirs(home, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "HOME": home, "TMPDIR": home, "HYAKU_SCRATCH": home,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def run(argv, env):
    p = subprocess.run(argv, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def load_battery():
    spec = importlib.util.spec_from_file_location("battery", BATTERY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def commit(clone, msg):
    env = env_for(WORK)
    subprocess.run([GIT, "-C", clone, "add", "-A"], capture_output=True, env=env)
    subprocess.run([GIT, "-C", clone, "-c", "user.name=r98r2", "-c", "user.email=r98r2@invalid",
                    "commit", "-qm", msg], capture_output=True, env=env)
    return subprocess.run([GIT, "-C", clone, "rev-parse", "HEAD"],
                          capture_output=True, text=True, env=env).stdout.strip()


def main():
    bat = load_battery()
    env = env_for(WORK)
    subprocess.run([GIT, "-C", CLONE, "reset", "-q", "--hard", REV], capture_output=True, env=env)
    base = json.loads(open(os.path.join(CLONE, MANIFEST), "rb").read())

    for variant in ("ambiguous-with-notes", "positive-with-notes"):
        subprocess.run([GIT, "-C", CLONE, "reset", "-q", "--hard", REV], capture_output=True, env=env)
        man = json.loads(json.dumps(base))
        if variant == "ambiguous-with-notes":
            man["rows"][0]["edit"]["old"] = "DISPOSITION"
        man["note"] = "GUARD_SETUP edit-no-op GUARD_SETUP state-unbuildable GUARD_SETUP manifest-empty"
        man["rows"][0]["note"] = "GUARD_SETUP edit-no-op:rev-hex GUARD_SETUP state-unbuildable:rev-hex"
        bytes_ = (json.dumps(man, indent=1) + "\n").encode()
        open(os.path.join(CLONE, MANIFEST), "wb").write(bytes_)
        frev = commit(CLONE, "note " + variant)
        fsha = hashlib.sha256(bytes_).hexdigest()
        scratch = os.path.join(WORK, "scratch")
        shutil.rmtree(scratch, ignore_errors=True)
        rc, out, err = run([sys.executable, "-I", TOOL, "--lane", CLONE, "--rev", frev,
                            "--manifest-sha", fsha], env_for(scratch))
        print("=== VARIANT %s rev=%s rc=%d" % (variant, frev[:12], rc))
        for line in out.splitlines():
            print("    OUT| " + line)
        for name in CLASSES:
            print("    GRADE %-24s class_token_ok=%s" % (name, bat.class_token_ok(name, out, rc)))
        print("    GRADE positive_ok=%s" % bat.positive_ok(out, rc))
        print("    NOTE_IN_STDOUT=%s" % ("GUARD_SETUP" in out.replace("\n", " ") and "note" in out.lower()))
    subprocess.run([GIT, "-C", CLONE, "reset", "-q", "--hard", REV], capture_output=True, env=env)


if __name__ == "__main__":
    main()
