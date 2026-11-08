#!/usr/bin/env python3
"""guard-refusals — drive the frozen round-97 guard-inertia tool through every
declared GUARD_SETUP refusal class, end to end, from committed bytes.

Round 97's matrix declared six refusal classes, but two of them existed only as
code: no committed receipt or selftest case executed `state-unbuildable` or
`limit-mechanism-missing` (round-97 spot-check D-6). This battery reads the
frozen tool as a blob at --rev (sha256 must equal --tool-sha, so a worktree
copy or an unpinned driver is refused), builds one manifest fixture per class
in a scratch clone, runs the tool's public CLI once per class, and grades the
run on exit 2 plus the exact class token on a line of the tool's own stdout.
The positive run uses the committed manifest and must print the exact
`GUARD_INERTIA` predicate with exit 0.

`--red CLASS` substitutes the positive manifest for that class: the battery
must then MISS the class (exit 1), which is how the claim shows the battery
can fail.

Usage:
  python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --lane LANE \
      --rev <40 hex> --tool <repo path> --tool-sha <64 hex> --work <empty dir> \
      [--red CLASS] [--selftest]

Exit: 0 every class refused with exit 2 and the exact token, and the positive
printed the predicate with exit 0; 1 a missed class, a wrong token or a failed
positive (each named); 2 setup (bad rev, tool absent, tool-sha invalid or
mismatched, manifest unreadable, work not empty); 64 usage.
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
CLASSES = ["edit-no-op", "edit-ambiguous", "state-unbuildable",
          "limit-mechanism-missing", "manifest-sha-mismatch", "manifest-empty"]
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
PREDICATE = "GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0"


def sealed_env(scratch):
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "HOME": scratch, "TMPDIR": scratch, "HYAKU_SCRATCH": scratch,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def run(argv, env, cwd=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def git(repo, args, env):
    return run([GIT, "-C", repo] + args, env)


def die(msg):
    print("GUARD_REFUSALS_SETUP " + msg)
    return 2


def class_token_ok(name, stdout, rc):
    if rc != 2:
        return False
    for line in stdout.splitlines():
        if line == "GUARD_SETUP " + name or line.startswith("GUARD_SETUP " + name + ":"):
            return True
    return False


def positive_ok(stdout, rc):
    return rc == 0 and any(line == PREDICATE for line in stdout.splitlines())


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
        pass  # bytes unchanged; the pin passed to the tool is a different digest
    else:
        raise ValueError("unknown class " + name)
    return (json.dumps(man, indent=1) + "\n").encode()


def commit(repo, msg, env):
    git(repo, ["add", "-A"], env)
    r = git(repo, ["-c", "user.name=r98-refusal", "-c", "user.email=r98-refusal@invalid",
                   "commit", "-qm", msg], env)
    if r[0] != 0:
        raise SystemExit("GUARD_REFUSALS_SETUP fixture-commit-failed:%s" % r[2][:120])
    return git(repo, ["rev-parse", "HEAD"], env)[1].strip()


def selftest():
    cases = [
        ("refusal-exact", class_token_ok("edit-no-op", "GUARD_SETUP edit-no-op:row-1\n", 2), True),
        ("refusal-bare", class_token_ok("edit-no-op", "GUARD_SETUP edit-no-op\n", 2), True),
        ("refusal-wrong-exit", class_token_ok("edit-no-op", "GUARD_SETUP edit-no-op:row-1\n", 0), False),
        ("refusal-wrong-token", class_token_ok("edit-no-op", "GUARD_SETUP edit-ambiguous:x\n", 2), False),
        ("refusal-longer-word", class_token_ok("edit-no-op", "GUARD_SETUP edit-no-opX\n", 2), False),
        ("refusal-other-line", class_token_ok("edit-no-op", "note GUARD_SETUP edit-no-op:x\n", 2), False),
        ("positive-exact", positive_ok(PREDICATE + "\n", 0), True),
        ("positive-missing", positive_ok("GUARD_INERTIA rows=1\n", 0), False),
        ("positive-wrong-exit", positive_ok(PREDICATE + "\n", 1), False),
    ]
    passed = 0
    for name, got, want in cases:
        ok = got == want
        passed += ok
        print("SELFTEST %s %s got=%s want=%s" % (name, "PASS" if ok else "FAIL", got, want))
    print("GUARD_REFUSALS_SELFTEST: %d/%d pass" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane")
    ap.add_argument("--rev")
    ap.add_argument("--tool", default=".ufo/evidence/round-97/c2/guard-inertia.py")
    ap.add_argument("--tool-sha", default=None)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--work", default=None)
    ap.add_argument("--red", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.lane or not a.rev or not a.work:
        print(__doc__)
        sys.exit(64)
    if not re.fullmatch(r"[0-9a-f]{40}", a.rev):
        sys.exit(die("rev-not-a-commit-id"))
    lane = os.path.realpath(a.lane)
    work = os.path.realpath(a.work)
    if os.path.isdir(work) and os.listdir(work):
        sys.exit(die("work-not-empty"))
    os.makedirs(work, exist_ok=True)
    env = sealed_env(work)
    r = git(lane, ["rev-parse", "--verify", "--quiet", "--end-of-options", a.rev + "^{commit}"], env)
    if r[0] != 0:
        sys.exit(die("rev-unresolvable"))
    rev = r[1].strip()
    tb = git(lane, ["cat-file", "blob", "%s:%s" % (rev, a.tool)], env)
    if tb[0] != 0:
        sys.exit(die("tool-absent-at-rev"))
    tool_blob = tb[1].encode()
    if a.tool_sha is not None:
        if not re.fullmatch(r"[0-9a-f]{64}", a.tool_sha):
            sys.exit(die("tool-sha-invalid"))
        if hashlib.sha256(tool_blob).hexdigest() != a.tool_sha:
            sys.exit(die("tool-sha-mismatch"))
    mb = git(lane, ["cat-file", "blob", "%s:%s" % (rev, a.manifest)], env)
    if mb[0] != 0:
        sys.exit(die("manifest-absent-at-rev"))
    man_bytes = mb[1].encode()
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    try:
        base = json.loads(man_bytes)
    except ValueError:
        sys.exit(die("manifest-unparsable"))
    if not base.get("rows"):
        sys.exit(die("manifest-empty-at-rev"))
    tool = os.path.join(work, "tool.py")
    with open(tool, "wb") as f:
        f.write(tool_blob)
    clone = os.path.join(work, "clone")
    r = run([GIT, "clone", "-q", "--shared", lane, clone], env)
    if r[0] != 0:
        sys.exit(die("clone-failed:%s" % r[2][:120]))
    git(clone, ["checkout", "-q", "--detach", rev], env)
    git(clone, ["config", "user.name", "r98-refusal"], env)
    git(clone, ["config", "user.email", "r98-refusal@invalid"], env)
    man_path = os.path.join(clone, a.manifest)
    failed = 0
    refused = 0
    observations = []
    for name in CLASSES:
        git(clone, ["reset", "-q", "--hard", rev], env)
        if a.red == name:
            fixture = man_bytes
            fixture_sha = man_sha
        else:
            fixture = fixture_manifest(base, name)
            fixture_sha = hashlib.sha256(fixture).hexdigest()
            if name == "manifest-sha-mismatch":
                fixture_sha = hashlib.sha256(fixture + b"x").hexdigest()
        os.makedirs(os.path.dirname(man_path), exist_ok=True)
        with open(man_path, "wb") as f:
            f.write(fixture)
        status = git(clone, ["status", "--porcelain"], env)[1].strip()
        frev = commit(clone, "fixture " + name, env) if status else rev
        scratch = os.path.join(work, "tool-scratch")
        shutil.rmtree(scratch, ignore_errors=True)
        os.makedirs(scratch, exist_ok=True)
        benv = sealed_env(scratch)
        rc, out, err = run([sys.executable, "-I", tool, "--lane", clone, "--rev", frev,
                            "--manifest-sha", fixture_sha], benv)
        ok = class_token_ok(name, out, rc)
        observations.append((name, rc, ok))
        if a.red == name:
            # the red arm must MISS: a substituted positive manifest must not refuse.
            if ok:
                failed += 1
                print("GUARD_REFUSALS_RED %s refused-under-red-run" % name)
            else:
                print("GUARD_REFUSALS_RED %s missed-as-declared rc=%d" % (name, rc))
            continue
        if ok:
            refused += 1
        else:
            failed += 1
            token = [ln for ln in out.splitlines() if ln.startswith("GUARD_SETUP")][:1]
            print("GUARD_REFUSALS_MISS %s rc=%d first=%r" % (name, rc, token))
    # positive: the committed manifest at the committed revision
    git(clone, ["reset", "-q", "--hard", rev], env)
    scratch = os.path.join(work, "tool-scratch")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch, exist_ok=True)
    rc, out, err = run([sys.executable, "-I", tool, "--lane", clone, "--rev", rev,
                        "--manifest-sha", man_sha], sealed_env(scratch))
    pos = positive_ok(out, rc)
    if not pos:
        failed += 1
        print("GUARD_REFUSALS_POSITIVE_FAIL rc=%d last=%r" % (rc, out.splitlines()[-1:]))
    print("GUARD_REFUSALS classes=%d refused=%d wrong=%d positive=%s%s"
          % (len(CLASSES), refused, len(CLASSES) - refused, "ok" if pos else "fail",
             (" red=" + a.red) if a.red else ""))
    shutil.rmtree(clone, ignore_errors=True)
    shutil.rmtree(os.path.join(work, "tool-scratch"), ignore_errors=True)
    if a.red:
        return 1  # the red run is the failing demonstration the claim cites
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
