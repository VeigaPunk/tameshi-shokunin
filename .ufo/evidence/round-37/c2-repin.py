#!/usr/bin/env python3
"""Re-attest the frozen r36 predicate against the r37 tally-audit tool pin."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PIN_PATH = ".ufo/evidence/round-37/counter-pin.json"
COUNTER_PATH = ".ufo/evidence/round-36/c1/c1-measure-v2.py"
TOOL_PATH = "tools/tally-audit-v3.py"
SEALED_PATH = ".ufo/evidence/round-35/c1/sealed"


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
    return env


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], env=git_env(), capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    env = git_env()
    rev_result = git(lane, "rev-parse", "--verify", a.rev)
    if rev_result.returncode:
        print("C2_R37_REPIN: SETUP rev_unresolved=%s" % a.rev)
        return 2
    rev = rev_result.stdout.decode().strip()
    pin_result = git(lane, "show", "%s:%s" % (rev, PIN_PATH))
    counter_result = git(lane, "show", "%s:%s" % (rev, COUNTER_PATH))
    tool_result = git(lane, "show", "%s:%s" % (rev, TOOL_PATH))
    if pin_result.returncode or counter_result.returncode or tool_result.returncode:
        print("C2_R37_REPIN: SETUP pinned_input_missing")
        return 2
    pin = json.loads(pin_result.stdout.decode("utf-8"))
    counter_sha = hashlib.sha256(counter_result.stdout).hexdigest()
    tool_sha = hashlib.sha256(tool_result.stdout).hexdigest()
    pins_ok = (counter_sha == pin["counter_sha256"] and tool_sha == pin["tool_sha256"])
    if not pins_ok:
        print("C2_R37_REPIN: SETUP pin_mismatch counter=%s tool=%s" % (counter_sha, tool_sha))
        return 2

    with tempfile.TemporaryDirectory(prefix="tameshi-r37-repin-", dir="/tmp") as tmp:
        work = os.path.join(tmp, "work")
        os.mkdir(work)
        p = subprocess.run([
            sys.executable,
            os.path.join(lane, COUNTER_PATH),
            "--lane", lane,
            "--rev", rev,
            "--work", work,
            "--sealed", SEALED_PATH,
            "--tool", TOOL_PATH,
        ], cwd=lane, env=env, capture_output=True, timeout=1800)
    output = p.stdout.decode("utf-8", "replace")
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    required = ("C1_R36V2_CONTROL_PASS=true", "pub_kill=6/6", "pub_accept=3/3",
                "pub_slots=9", "pub_distinct=9", "ho_kill=4/4", "ho_accept=3/3",
                "ho_invalid=0", "rev=" + rev)
    ok = p.returncode == 0 and all(token in output for token in required)
    print("C2_R37_REPIN: counter_sha256=%s tool_sha256=%s frozen_predicate_replayed=%d rev=%s C2_R37_REPIN_PASS=%s"
          % (counter_sha, tool_sha, int(ok), rev, "true" if ok else "false"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
