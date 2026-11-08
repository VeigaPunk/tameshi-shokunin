#!/usr/bin/env python3
"""R95SN1: PATH-resolution and --rev-validation attacks on the C2 checker."""
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CHECKER = S + "/snap/conjunct-disposition-v95.py"
COUNTER_REL = ".ufo/evidence/round-95/c1/measure-v95.py"
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
RESULTS = []


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None, check=False):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, p.stderr))
    return p


def clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", LANE_SRC, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def commit_all(lane, msg):
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", msg])
    return sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()


def stage_instruments(lane):
    shutil.copytree(os.path.join(LANE_SRC, ".ufo/evidence/round-95"),
                    os.path.join(lane, ".ufo/evidence/round-95"), dirs_exist_ok=True)
    shutil.rmtree(os.path.join(lane, ".ufo/evidence/round-95/c1/__pycache__"),
                  ignore_errors=True)


KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
        "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
        "figure", "witnessed", "source", "coverage", "n_min"]


def build(name):
    d = os.path.join(S, "atk7", name)
    lane = clone(d)
    stage_instruments(lane)
    blob = sh(["git", "-C", lane, "cat-file", "blob", "HEAD:" + COUNTER_REL]).stdout
    sha = hashlib.sha256(blob.encode()).hexdigest()
    man = json.load(open(os.path.join(lane, ".ufo/evidence/round-95/conjunct-disposition.json")))
    rd = os.path.join(lane, RECEIPTS_REL)
    os.makedirs(rd, exist_ok=True)
    for k, row in man["rows"].items():
        if "unfalsifiable" in row:
            continue
        st = row["state"]
        if row["mode"] == "setup-refusal":
            body = "counter_sha=%s\nexit=2\nC1_SETUP %s\n" % (sha, row["token"])
        else:
            body = ("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(rd, st + ".out"), "w").write(body)
    rev = commit_all(lane, "base")
    return lane, rev, sha


def f01_path_hijack_git():
    """A hostile `git` earlier in PATH must not be executed by the checker."""
    lane, rev, sha = build("f01")
    fake = os.path.join(S, "atk7", "f01_bin")
    shutil.rmtree(fake, ignore_errors=True)
    os.makedirs(fake)
    g = os.path.join(fake, "git")
    with open(g, "w") as f:
        f.write("#!/bin/sh\n"
                "echo \"HIJACKED-GIT $@\" >&2\n"
                "exit 7\n")
    os.chmod(g, 0o755)
    env = dict(os.environ)
    env["PATH"] = fake + ":" + env["PATH"]
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    hijacked = "HIJACKED-GIT" in out
    rec("F01", "a hostile `git` earlier in PATH is executed by the C2 checker",
        "exit=%d hijacked=%s out=%r" % (p.returncode, hijacked,
                                        [l for l in out.splitlines()][:3]),
        "the checker must resolve git from a pinned PATH (the C1 counter pins "
        "PATH=/usr/local/bin:/usr/bin:/bin); an inherited PATH lets a hostile git "
        "supply the graded bytes",
        "HIGH" if hijacked else "NONE (defended)",
        "VULNERABLE" if hijacked else "defended")


def f02_rev_branch_name():
    """--rev naming a branch instead of a frozen 40-hex commit."""
    lane, rev, sha = build("f02")
    # a branch whose tip differs from the frozen rev
    sh(["git", "-C", lane, "checkout", "-q", "-b", "attacker"])
    rd = os.path.join(lane, RECEIPTS_REL)
    p2 = os.path.join(rd, "renamed-result.out")
    open(p2, "w").write("counter_sha=%s\nexit=1\nC1_CONJUNCTS ids=false\n" % sha)
    commit_all(lane, "forged receipt on a branch")
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", "attacker",
                        "--min-falsifiable", "17"], capture_output=True, text=True)
    out = p.stdout + p.stderr
    rec("F02", "--rev names a movable branch instead of a frozen 40-hex commit",
        "exit=%d out=%r" % (p.returncode, [l for l in out.splitlines() if l.startswith("DISPOSITION ")][:1]),
        "--rev must be pinned to an object id so the audited bytes cannot move under a "
        "ref name; the checker accepts any revspec",
        "MEDIUM", "observed")


def f03_counter_path_env():
    """ambient PATH also reaches the counter subprocess the checker spawns."""
    lane, rev, sha = build("f03")
    fake = os.path.join(S, "atk7", "f03_bin")
    shutil.rmtree(fake, ignore_errors=True)
    os.makedirs(fake)
    g = os.path.join(fake, "git")
    with open(g, "w") as f:
        f.write("#!/bin/sh\nexit 7\n")
    os.chmod(g, 0o755)
    env = dict(os.environ)
    env["PATH"] = fake + ":" + env["PATH"]
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    rec("F03", "ambient PATH reaches the counter subprocess the C2 checker spawns",
        "exit=%d out=%r" % (p.returncode, [l for l in out.splitlines()][:2]),
        "the checker's sealed_env should pin PATH the way the C1 counter's does",
        "MEDIUM", "observed")


def f04_checker_env_keeps_non_git():
    """sealed_env() of the C2 checker: which ambient variables survive?"""
    src = open(CHECKER).read()
    import re as _re
    m = _re.search(r"def sealed_env\(\).*?\n\n", src, _re.S)
    body = m.group(0) if m else ""
    keeps_non_git = "if not k.startswith(\"GIT_\")" in body or "if not k.startswith('GIT_')" in body
    pins_path = "PATH" in body
    rec("F04", "C2 checker sealed_env(): which ambient state survives into its git calls",
        "keeps_non_GIT_ambient=%s pins_PATH=%s body=%r" % (
            keeps_non_git, pins_path, body.strip().split("\n")[-3:]),
        "the counter's sealed_env replaces the whole environment; the checker's keeps "
        "everything except GIT_*, including PATH (which selects the git binary)",
        "MEDIUM" if (keeps_non_git and not pins_path) else "NONE",
        "observed" if (keeps_non_git and not pins_path) else "defended")


def main():
    os.makedirs(os.path.join(S, "atk7"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [f01_path_hijack_git, f02_rev_branch_name, f03_counter_path_env,
               f04_checker_env_keeps_non_git]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-40s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-path-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
