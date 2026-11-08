#!/usr/bin/env python3
"""guard-inertia — measure whether each declared guard edit in the round-96
checker is observable, on a fixture store, without re-running a 185 s battery state.

Round 96's own wave left the "are the guards inert?" probe unmeasured (spot-check
D-b: R96L1 delivered nothing). This tool makes that probe runnable: for every row
in the committed manifest it copies the checker blob extracted from `--rev`, applies
exactly one exact-string edit (refusing a no-op, an ambiguous or a missing anchor),
runs the pristine and the mutant checker against a fresh fixture store at the row's
state, and classifies the row:

  * `killed` — the pristine run refuses as the row declares and the mutant run's
    verdict differs (exit differs, or the declared token disappears);
  * `limit`  — the two runs are identical and the row names the measured mechanism
    that makes this edit alone observationally equivalent;
  * `survived` — anything else, including a row whose observation contradicts its
    pre-registered `expect`.

A row's outcome must equal its frozen `expect`; one contradiction ends the run
with exit 1. The tool never executes a battery state: every store is a four-file
fixture committed in a scratch git repo.

Usage:
  python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane LANE --rev REV \
      [--checker PATH] [--manifest PATH] [--checker-sha SHA] [--selftest]

Exit: 0 every row observed its expectation and none survived; 1 a survived row
or an unmet row; 2 setup (checker/manifest absent at rev, digest mismatch,
ambiguous or no-op edit, scratch unusable); 64 usage.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

GIT = "/usr/bin/git"
CHECKER = ".ufo/evidence/round-96/conjunct-disposition-v96.py"
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
SCRATCH_ROOT = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")


def sealed_env():
    home = os.path.join(SCRATCH_ROOT, "tameshi-r97", "guard-home")
    tmp = os.path.join(home, "tmp")
    os.makedirs(tmp, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "HOME": home, "TMPDIR": tmp,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(repo, args, env):
    return subprocess.run([GIT, "-C", repo] + args, capture_output=True, env=env)


def die(msg):
    print("GUARD_SETUP " + msg)
    return 2


def blob_at(lane, rev, path, env):
    r = git(lane, ["cat-file", "blob", "%s:%s" % (rev, path)], env)
    return None if r.returncode != 0 else r.stdout


def setup_store(base, env, *, manifest=None, receipts=None, prefix="store"):
    """A minimal lane: counter, manifest, claims digest, receipts; one commit."""
    repo = os.path.join(base, prefix)
    os.makedirs(os.path.join(repo, ".ufo/evidence/round-96/c1"), exist_ok=True)
    os.makedirs(os.path.join(repo, ".ufo/evidence/round-96/pre-freeze/controls"), exist_ok=True)
    os.makedirs(os.path.join(repo, ".ufo/waves/round-96"), exist_ok=True)
    counter = ("#!/usr/bin/env python3\nimport sys\n"
               "if '--conjuncts' in sys.argv:\n"
               "    print('C1_CONJUNCT_KEYS alpha beta gamma')\n"
               "    sys.exit(0)\n"
               "print('C1_R96_PASS=false')\nsys.exit(1)\n")
    cpath = os.path.join(repo, ".ufo/evidence/round-96/c1/measure-v96.py")
    with open(cpath, "w") as f:
        f.write(counter)
    csha = hashlib.sha256(counter.encode()).hexdigest()
    rows = manifest if manifest is not None else {
        "alpha": {"state": "pos", "mode": "conjunct-false"},
        "beta": {"state": "pos2", "mode": "conjunct-false"},
        "gamma": {"unfalsifiable": "the sealed pin at state pos forbids a committed falsifier for gamma"},
    }
    mbytes = json.dumps({"rows": rows}, indent=1).encode() + b"\n"
    with open(os.path.join(repo, ".ufo/evidence/round-96/conjunct-disposition.json"), "wb") as f:
        f.write(mbytes)
    with open(os.path.join(repo, ".ufo/waves/round-96/claims.json"), "w") as f:
        json.dump({"claims": {"C1": {"manifest_sha256": hashlib.sha256(mbytes).hexdigest()}}}, f)
    rcpts = receipts if receipts is not None else {
        "pos": "counter_sha=%s\nexit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n" % csha,
        "pos2": "counter_sha=%s\nexit=1\nC1_CONJUNCTS alpha=true beta=false gamma=true\n" % csha,
    }
    for name, body in rcpts.items():
        with open(os.path.join(repo, ".ufo/evidence/round-96/pre-freeze/controls/%s.out" % name), "w") as f:
            f.write(body)
    git(repo, ["init", "-q"], env)
    git(repo, ["add", "-A"], env)
    r = git(repo, ["-c", "user.name=guard-fixture", "-c", "user.email=guard@invalid",
                   "commit", "-qm", "fixture"], env)
    if r.returncode != 0:
        raise RuntimeError("fixture commit failed: " + r.stderr.decode("utf-8", "replace")[:200])
    git(repo, ["branch", "-M", "master"], env)
    rev = git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()
    return repo, rev, csha


def rewrite_receipt(repo, env, name, body):
    with open(os.path.join(repo, ".ufo/evidence/round-96/pre-freeze/controls/%s.out" % name), "w") as f:
        f.write(body)
    git(repo, ["add", "-A"], env)
    r = git(repo, ["-c", "user.name=guard-fixture", "-c", "user.email=guard@invalid",
                   "commit", "-qm", "state edit " + name], env)
    if r.returncode != 0:
        raise RuntimeError("state commit failed: " + r.stderr.decode("utf-8", "replace")[:200])
    return git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()


def build_state(name, base, env):
    """Returns (repo, rev, extra_args, env_overrides)."""
    if name == "clean":
        repo, rev, _ = setup_store(base, env)
        return repo, rev, [], {}
    if name == "replace-refs":
        repo, rev, _ = setup_store(base, env)
        alt = git(repo, ["-c", "user.name=guard-fixture", "-c", "user.email=guard@invalid",
                        "commit-tree", rev + "^{tree}", "-p", rev, "-m", "alt"], env)
        altid = alt.stdout.decode().strip()
        if not altid:
            raise RuntimeError("commit-tree failed: " + alt.stderr.decode()[:200])
        r = git(repo, ["replace", rev, altid], env)
        if r.returncode != 0:
            raise RuntimeError("replace failed: " + r.stderr.decode()[:200])
        return repo, rev, [], {}
    if name == "counter-sha":
        repo, rev, csha = setup_store(base, env)
        rev = rewrite_receipt(repo, env, "pos",
                              "counter_sha=%s\nexit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n" % ("0" * 64))
        return repo, rev, [], {}
    if name == "receipt-absent":
        repo, rev, _ = setup_store(base, env, manifest={
            "alpha": {"state": "ghost", "mode": "conjunct-false"},
            "beta": {"state": "pos2", "mode": "conjunct-false"},
            "gamma": {"unfalsifiable": "the sealed pin at state pos2 forbids a committed falsifier for gamma"}})
        return repo, rev, [], {}
    if name == "no-flip":
        repo, rev, csha = setup_store(base, env)
        rev = rewrite_receipt(repo, env, "pos",
                              "counter_sha=%s\nexit=1\nC1_CONJUNCTS alpha=true beta=true gamma=true\n" % csha)
        return repo, rev, [], {}
    if name == "unknown-key":
        m = {"alpha": {"state": "pos", "mode": "conjunct-false"},
             "beta": {"state": "pos2", "mode": "conjunct-false"},
             "gamma": {"unfalsifiable": "the sealed pin at state pos forbids a committed falsifier for gamma"},
             "delta": {"state": "pos", "mode": "conjunct-false"}}
        repo, rev, _ = setup_store(base, env, manifest=m)
        return repo, rev, [], {}
    if name == "min-falsifiable":
        repo, rev, _ = setup_store(base, env)
        return repo, rev, ["--min-falsifiable", "4"], {}
    if name == "hostile-path":
        repo, rev, _ = setup_store(base, env)
        shim = os.path.join(base, "shim")
        os.makedirs(shim, exist_ok=True)
        p = os.path.join(shim, "git")
        with open(p, "w") as f:
            f.write("#!/bin/sh\nexit 99\n")
        os.chmod(p, 0o755)
        return repo, rev, [], {"PATH": shim + ":/usr/local/bin:/usr/bin:/bin"}
    raise RuntimeError("unknown state: " + name)


def run_checker(checker_path, repo, rev, extra_args, env_override):
    env = sealed_env()
    env.update(env_override)
    r = subprocess.run([sys.executable, "-I", checker_path, "--lane", repo, "--rev", rev]
                       + extra_args, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def classify(row, pristine, mutant):
    """pristine/mutant = (exit, text). Returns observed class."""
    pe, pt = pristine
    me, mt = mutant
    pr = row.get("pristine", {})
    if pe != pr.get("exit") or (pr.get("token") and pr["token"] not in pt):
        return "pristine-unmet"
    differs = (me != pe) or bool(pr.get("token") and pr["token"] not in mt)
    if row["expect"] == "killed":
        return "killed" if differs else "survived"
    if row["expect"] == "limit":
        return "limit" if not differs else "survived"
    return "survived"


def run_matrix(checker_bytes, manifest, tag):
    os.makedirs(tag, exist_ok=True)
    env = sealed_env()
    cpath = os.path.join(tag, "checker-pristine.py")
    with open(cpath, "wb") as f:
        f.write(checker_bytes)
    results = []
    for i, row in enumerate(manifest["rows"]):
        base = os.path.join(tag, "row%02d-%s" % (i, row["id"]))
        os.makedirs(base, exist_ok=True)
        if row["expect"] == "limit" and len(str(row.get("limit_mechanism", "")).strip()) < 40:
            raise SystemExit(_setup_text("limit-mechanism-missing:" + row["id"]))
        old, new = row["edit"]["old"], row["edit"]["new"]
        count = checker_bytes.count(old.encode())
        if count != 1:
            raise SystemExit(_setup_text("edit-ambiguous:%s:%d" % (row["id"], count)))
        if old == new:
            raise SystemExit(_setup_text("edit-no-op:" + row["id"]))
        mb = checker_bytes.replace(old.encode(), new.encode(), 1)
        mpath = os.path.join(tag, "checker-%s.py" % row["id"])
        with open(mpath, "wb") as f:
            f.write(mb)
        try:
            repo, rev, extra, env_over = build_state(row["state"], base, env)
        except Exception as exc:  # noqa: BLE001 - an unbuildable state is setup
            raise SystemExit(_setup_text("state-unbuildable:%s:%s" % (row["id"], str(exc)[:120])))
        rev = row.get("rev") or rev
        pristine = run_checker(cpath, repo, rev, extra, env_over)
        mutant = run_checker(mpath, repo, rev, extra, env_over)
        cls = classify(row, pristine, mutant)
        results.append((row["id"], row["expect"], cls, pristine, mutant))
        print("GUARD_ROW %s expect=%s observed=%s pristine=exit=%d%s mutant=exit=%d%s" % (
            row["id"], row["expect"], cls, pristine[0],
            ("/" + row["pristine"]["token"]) if row["pristine"].get("token") else "",
            mutant[0],
            ("/" + row["pristine"]["token"]) if row["pristine"].get("token") and row["pristine"]["token"] in mutant[1] else ""))
    killed = sum(1 for r in results if r[2] == "killed")
    limits = sum(1 for r in results if r[2] == "limit")
    survived = sum(1 for r in results if r[2] not in ("killed", "limit"))
    unmet = sum(1 for r in results if r[2] != r[1])
    print("GUARD_INERTIA rows=%d killed=%d limits=%d survived=%d unmet=%d" % (
        len(results), killed, limits, survived, unmet))
    return 0 if survived == 0 and unmet == 0 else 1


def _setup_text(msg):
    return "GUARD_SETUP " + msg


def selftest():
    os.makedirs(os.path.join(SCRATCH_ROOT, "tameshi-r97"), exist_ok=True)
    base = tempfile.mkdtemp(dir=os.path.join(SCRATCH_ROOT, "tameshi-r97"), prefix="guard-selftest-")
    checker = ("import sys\nGUARD = 'x'\nif len(sys.argv) > 1 and sys.argv[1] == 'boom':\n"
               "    print('REFUSED boom')\n    sys.exit(2)\nprint('OK')\nsys.exit(0)\n")
    passed = total = 0

    def cls_arm(name, row, pristine, mutant, want):
        nonlocal passed, total
        got = classify(row, pristine, mutant)
        ok = got == want
        print("SELFTEST %s %s got=%s want=%s" % (name, "PASS" if ok else "FAIL", got, want))
        passed += ok
        total += 1

    cls_arm("kill-real", {"expect": "killed", "pristine": {"exit": 2, "token": "REFUSED boom"}},
            (2, "REFUSED boom"), (0, "OK"), "killed")
    cls_arm("limit-real", {"expect": "limit", "pristine": {"exit": 2, "token": "REFUSED boom"}},
            (2, "REFUSED boom"), (2, "REFUSED boom"), "limit")
    cls_arm("kill-lie", {"expect": "killed", "pristine": {"exit": 2, "token": "REFUSED boom"}},
            (2, "REFUSED boom"), (2, "REFUSED boom"), "survived")
    cls_arm("limit-lie", {"expect": "limit", "pristine": {"exit": 2, "token": "REFUSED boom"}},
            (2, "REFUSED boom"), (0, "OK"), "survived")
    cls_arm("pristine-unmet", {"expect": "killed", "pristine": {"exit": 2, "token": "REFUSED boom"}},
            (0, "OK"), (0, "OK"), "pristine-unmet")

    def anchor_arm(name, row, want_prefix):
        nonlocal passed, total
        try:
            run_matrix(checker.encode(), {"rows": [row]}, os.path.join(base, "t-" + name))
            got = "no-refusal"
        except SystemExit as exc:
            got = str(exc.code)
        ok = got == want_prefix or (want_prefix.endswith(":") and got.startswith(want_prefix))
        print("SELFTEST %s %s got=%s want=%s" % (name, "PASS" if ok else "FAIL", got, want_prefix))
        passed += ok
        total += 1

    anchor_arm("noop-anchor", {"id": "noop", "expect": "killed", "state": "clean",
                               "edit": {"old": "GUARD = 'x'", "new": "GUARD = 'x'"},
                               "pristine": {"exit": 2}}, "GUARD_SETUP edit-no-op:noop")
    anchor_arm("ambiguous-anchor", {"id": "amb", "expect": "killed", "state": "clean",
                                   "edit": {"old": "x", "new": "y"},
                                   "pristine": {"exit": 2}}, "GUARD_SETUP edit-ambiguous:amb:")
    print("GUARD_INERTIA_SELFTEST: %d/%d pass" % (passed, total))
    shutil.rmtree(base, ignore_errors=True)
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane")
    ap.add_argument("--rev")
    ap.add_argument("--checker", default=CHECKER)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--checker-sha", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.lane:
        print(__doc__)
        sys.exit(64)
    if not a.rev or not re.fullmatch(r"[0-9a-f]{40}", a.rev):
        sys.exit(die("rev-not-a-commit-id"))
    env = sealed_env()
    r = git(a.lane, ["rev-parse", "--verify", "--quiet", "--end-of-options",
                     a.rev + "^{commit}"], env)
    if r.returncode != 0:
        sys.exit(die("rev-unresolvable"))
    a.rev = r.stdout.decode().strip()
    checker = blob_at(a.lane, a.rev, a.checker, env)
    if checker is None:
        sys.exit(die("checker-absent-at-rev"))
    if a.checker_sha and hashlib.sha256(checker).hexdigest() != a.checker_sha:
        sys.exit(die("checker-sha-mismatch"))
    manifest_b = blob_at(a.lane, a.rev, a.manifest, env)
    if manifest_b is None:
        sys.exit(die("manifest-absent-at-rev"))
    try:
        manifest = json.loads(manifest_b)
    except Exception:
        sys.exit(die("manifest-unparsable"))
    os.makedirs(os.path.join(SCRATCH_ROOT, "tameshi-r97"), exist_ok=True)
    tag = tempfile.mkdtemp(dir=os.path.join(SCRATCH_ROOT, "tameshi-r97"), prefix="guard-inertia-")
    try:
        rc = run_matrix(checker, manifest, tag)
    except SystemExit as exc:
        if isinstance(exc.code, str) and exc.code.startswith("GUARD_SETUP "):
            print(exc.code)
            sys.exit(2)
        raise
    finally:
        shutil.rmtree(tag, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
