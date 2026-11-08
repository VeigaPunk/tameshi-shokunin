#!/usr/bin/env python3
"""battery-bind — re-derive the round-96 battery verdict from committed receipts.

Round 96's 50-state battery printed `C1_CONTROLS states=50 matched=50
mismatches=0 missing=0` and wrote its summary to `C1-summary.txt` in the
driver's `--outdir`; that summary was never committed, so the closure could
not re-derive the line (spot-check D-a) and had to accept a seat's re-grade.
This reader produces the same verdict from the 50 committed receipts and the
committed driver's own expectations, in seconds, without re-running a state.

What it reads, all at `--rev` from the object store (never the worktree):

  * the 50 receipts `<receipts>/<state>.out`;
  * the frozen counter `<counter>` (its sha256 is the `counter=self` digest);
  * the committed driver `<driver>` (its `states()` and `grade()` are the
    oracle; `EXPECT_EXTRA` carries the four states the driver builds itself).

A state whose receipt blob is absent, that carries no `counter_sha=<64 hex>`
line, or whose `counter_sha` differs from the counter blob's sha256 while the
receipt does not name a `mutant=D<nn>` row, is `missing`. A receipt whose
`exit=` differs from the expectation, fails the driver's own `grade()`
conjunct/`__pass`/`__setup` check, is `mismatched`.

Usage:
  python3 -I .ufo/evidence/round-97/c1/battery-bind.py --lane LANE --rev REV \
      [--driver PATH] [--counter PATH] [--receipts DIR] [--selftest]

Exit: 0 every state matched; 1 any mismatched/missing; 2 setup refusal
(driver or counter blob absent at rev, driver digest not the pinned one,
driver import failure, scratch root unusable); 64 usage.
"""
import argparse
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

ROUND_DRIVER = ".ufo/evidence/round-96/c1/controls-v96.py"
ROUND_COUNTER = ".ufo/evidence/round-96/c1/measure-v96.py"
ROUND_RECEIPTS = ".ufo/evidence/round-96/pre-freeze/controls"
SHA_RE = re.compile(r"[0-9a-f]{64}")
GIT = "/usr/bin/git"
SELF_LINE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)


def sealed_env(scratch_home=None):
    home = scratch_home or os.path.join(
        os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "tameshi-r97", "battery-home")
    tmp = os.path.join(home, "tmp")
    os.makedirs(tmp, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "HOME": home, "TMPDIR": tmp,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(lane, args, env, text=False):
    return subprocess.run([GIT, "-C", lane] + args, capture_output=True, text=text, env=env)


def die(msg):
    print("BATTERY_SETUP " + msg)
    return 2


def blob_at(lane, rev, path, env):
    r = git(lane, ["cat-file", "blob", "%s:%s" % (rev, path)], env)
    if r.returncode != 0:
        return None
    return r.stdout


def parse_exit(body):
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("exit="):
            try:
                return int(s.split("=", 1)[1])
            except ValueError:
                return -1
    return -1


def parse_counter_sha(body):
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("counter_sha="):
            return s.split("=", 1)[1].strip()
    return None


def load_driver(driver_bytes, tag):
    path = os.path.join(tag, "controls-under-test.py")
    with open(path, "wb") as f:
        f.write(driver_bytes)
    spec = importlib.util.spec_from_file_location("controls_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def checkout_lane_at(lane, rev, dest, env):
    """Materialize the lane tree at `rev` into dest (read-only archive; the lane
    repo is never written)."""
    os.makedirs(dest, exist_ok=True)
    p = subprocess.Popen([GIT, "-C", lane, "archive", rev], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=env)
    import tarfile
    with tarfile.open(fileobj=p.stdout, mode="r|") as tf:
        tf.extractall(dest)
    err = p.stderr.read()
    rc = p.wait()
    if rc != 0:
        raise RuntimeError("git archive failed: " + err.decode("utf-8", "replace")[:200])


def bind(lane, rev, driver_path, counter_path, receipts_path, driver_sha_pin, tag):
    env = sealed_env()
    driver_blob = blob_at(lane, rev, driver_path, env)
    if driver_blob is None:
        return die("driver-absent-at-rev"), None
    if driver_sha_pin and hashlib.sha256(driver_blob).hexdigest() != driver_sha_pin:
        return die("driver-sha-mismatch"), None
    counter_blob = blob_at(lane, rev, counter_path, env)
    if counter_blob is None:
        return die("counter-absent-at-rev"), None
    counter_sha = hashlib.sha256(counter_blob).hexdigest()
    lane_at_rev = os.path.join(tag, "lane-at-rev")
    checkout_lane_at(lane, rev, lane_at_rev, env)
    try:
        drv = load_driver(driver_blob, tag)
        expectations = {n: c["expect"] for n, c in drv.states(lane_at_rev).items()}
        expectations.update(drv.EXPECT_EXTRA)
    except Exception as exc:  # noqa: BLE001 - any import/state failure is setup
        return die("driver-unusable:" + str(exc)[:160]), None
    matched = mismatched = missing = 0
    bad = []
    for name in sorted(expectations):
        body_b = blob_at(lane, rev, "%s/%s.out" % (receipts_path.rstrip("/"), name), env)
        if body_b is None:
            missing += 1
            bad.append(name + ":MISSING(receipt-absent-at-rev)")
            continue
        body = body_b.decode("utf-8", "replace")
        got_sha = parse_counter_sha(body)
        if got_sha is None or not SHA_RE.fullmatch(got_sha):
            missing += 1
            bad.append(name + ":MISSING(no-counter-sha)")
            continue
        is_mutant = re.search(r"^mutant=D[0-9]+", body, re.M) is not None
        if not is_mutant and got_sha != counter_sha:
            mismatched += 1
            bad.append(name + ":MISMATCH(counter-sha)")
            continue
        code = parse_exit(body)
        ok = drv.grade(name, code, body, expectations[name])
        if ok:
            matched += 1
        else:
            mismatched += 1
            bad.append(name + ":MISMATCH(exit=%d)" % code)
    for line in bad:
        print("BATTERY_ROW " + line)
    print("BATTERY states=%d matched=%d mismatched=%d missing=%d" % (
        len(expectations), matched, mismatched, missing))
    return (0 if not bad else 1), len(expectations)


def selftest():
    """Fixture battery: a real git repo, four states, expectations the reader
    must reproduce; each planted cheat must move the verdict."""
    base = tempfile.mkdtemp(dir=os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
                                              "tameshi-r97"), prefix="battery-selftest-")
    env = sealed_env(os.path.join(base, "home"))
    repo = os.path.join(base, "lane")
    os.makedirs(repo)
    git(repo, ["init", "-q"], env)
    driver = ("EXPECT_EXTRA = {'extra-pass': (0, {'__pass': True})}\n"
              "def states(lane):\n"
              "    return {'a': {'expect': (1, {'k': False})},\n"
              "            'b': {'expect': (2, {'__setup': 'boom'})}}\n"
              "def grade(name, code, out, want):\n"
              "    if code != want[0]:\n"
              "        return False\n"
              "    if '__pass' in want[1]:\n"
              "        return 'PASS=true' in out\n"
              "    if '__setup' in want[1]:\n"
              "        return ('C1_SETUP ' + want[1]['__setup']) in out\n"
              "    conj = {}\n"
              "    for line in out.split('\\n'):\n"
              "        if line.startswith('C1_CONJUNCTS '):\n"
              "            for kv in line.split()[1:]:\n"
              "                k, v = kv.split('=', 1)\n"
              "                conj[k] = (v == 'true')\n"
              "    return all(conj.get(k) == v for k, v in want[1].items())\n")
    counter = "#!/usr/bin/env python3\n# fixture counter\n"
    with open(os.path.join(repo, "driver.py"), "w") as f:
        f.write(driver)
    with open(os.path.join(repo, "counter.py"), "w") as f:
        f.write(counter)
    csha = hashlib.sha256(counter.encode()).hexdigest()
    os.makedirs(os.path.join(repo, "r"))
    bodies = {"a": "counter_sha=%s\nexit=1\nC1_CONJUNCTS k=false\n" % csha,
              "b": "counter_sha=%s\nexit=2\nC1_SETUP boom\n" % csha,
              "extra-pass": "counter_sha=%s\nexit=0\nPASS=true\n" % csha}
    for name, body in bodies.items():
        with open(os.path.join(repo, "r", name + ".out"), "w") as f:
            f.write(body)
    git(repo, ["add", "-A"], env)
    git(repo, ["-c", "user.name=st", "-c", "user.email=st@invalid", "commit", "-qm", "clean"], env)
    rev = git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()

    def run(**kw):
        return bind(repo, rev, "driver.py", "counter.py", "r",
                    kw.pop("pin", None), kw.pop("tag", base))

    passed = total = 0
    rc, _ = run(tag=os.path.join(base, "t0"))
    ok = rc == 0
    print("SELFTEST clean %s rc=%d" % ("PASS" if ok else "FAIL", rc))
    passed += ok; total += 1
    # cheat: worktree-only receipt (never committed)
    with open(os.path.join(repo, "r", "ghost.out"), "w") as f:
        f.write(bodies["a"])
    rc, _ = run(tag=os.path.join(base, "t1"))
    ok = rc == 0  # ghost is not in the expectation set -> ignored
    print("SELFTEST worktree-extra-ignored %s rc=%d" % ("PASS" if ok else "FAIL", rc))
    passed += ok; total += 1
    os.remove(os.path.join(repo, "r", "ghost.out"))
    # cheat: deleted receipt at rev -> missing
    os.remove(os.path.join(repo, "r", "b.out"))
    with open(os.path.join(repo, "r", "b.out"), "w") as f:
        f.write(bodies["b"])
    git(repo, ["rm", "-q", "--cached", "r/b.out"], env)
    git(repo, ["-c", "user.name=st", "-c", "user.email=st@invalid", "commit", "-qm", "drop b"], env)
    rev2 = git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()
    out = bind(repo, rev2, "driver.py", "counter.py", "r", None, os.path.join(base, "t2"))
    ok = out[0] == 1
    print("SELFTEST missing-receipt %s rc=%d" % ("PASS" if ok else "FAIL", out[0]))
    passed += ok; total += 1
    # cheat: wrong counter_sha on a non-mutant receipt -> mismatched
    with open(os.path.join(repo, "r", "b.out"), "w") as f:
        f.write("counter_sha=%s\nexit=2\nC1_SETUP boom\n" % ("0" * 64))
    git(repo, ["add", "-A"], env)
    git(repo, ["-c", "user.name=st", "-c", "user.email=st@invalid", "commit", "-qm", "sha cheat"], env)
    rev3 = git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()
    out = bind(repo, rev3, "driver.py", "counter.py", "r", None, os.path.join(base, "t3"))
    ok = out[0] == 1
    print("SELFTEST counter-sha-cheat %s rc=%d" % ("PASS" if ok else "FAIL", out[0]))
    passed += ok; total += 1
    # cheat: wrong exit -> mismatched
    with open(os.path.join(repo, "r", "b.out"), "w") as f:
        f.write("counter_sha=%s\nexit=0\nC1_SETUP boom\n" % csha)
    git(repo, ["add", "-A"], env)
    git(repo, ["-c", "user.name=st", "-c", "user.email=st@invalid", "commit", "-qm", "exit cheat"], env)
    rev4 = git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()
    out = bind(repo, rev4, "driver.py", "counter.py", "r", None, os.path.join(base, "t4"))
    ok = out[0] == 1
    print("SELFTEST exit-cheat %s rc=%d" % ("PASS" if ok else "FAIL", out[0]))
    passed += ok; total += 1
    # cheat: flipped conjunct -> mismatched
    with open(os.path.join(repo, "r", "b.out"), "w") as f:
        f.write(bodies["b"])
    with open(os.path.join(repo, "r", "a.out"), "w") as f:
        f.write("counter_sha=%s\nexit=1\nC1_CONJUNCTS k=true\n" % csha)
    git(repo, ["add", "-A"], env)
    git(repo, ["-c", "user.name=st", "-c", "user.email=st@invalid", "commit", "-qm", "conj cheat"], env)
    rev5 = git(repo, ["rev-parse", "HEAD"], env).stdout.decode().strip()
    out = bind(repo, rev5, "driver.py", "counter.py", "r", None, os.path.join(base, "t5"))
    ok = out[0] == 1
    print("SELFTEST conj-cheat %s rc=%d" % ("PASS" if ok else "FAIL", out[0]))
    passed += ok; total += 1
    # driver digest pin mismatch -> setup exit 2
    out = bind(repo, rev5, "driver.py", "counter.py", "r", "0" * 64, os.path.join(base, "t6"))
    ok = out[0] == 2
    print("SELFTEST driver-sha-mismatch %s rc=%d" % ("PASS" if ok else "FAIL", out[0]))
    passed += ok; total += 1
    print("BATTERY_SELFTEST: %d/%d pass" % (passed, total))
    import shutil
    shutil.rmtree(base, ignore_errors=True)
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane")
    ap.add_argument("--rev")
    ap.add_argument("--driver", default=ROUND_DRIVER)
    ap.add_argument("--counter", default=ROUND_COUNTER)
    ap.add_argument("--receipts", default=ROUND_RECEIPTS)
    ap.add_argument("--driver-sha", default=None)
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
    tag = tempfile.mkdtemp(dir=os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
                                            "tameshi-r97"), prefix="battery-bind-")
    try:
        rc, _ = bind(os.path.realpath(a.lane), a.rev, a.driver, a.counter, a.receipts,
                     a.driver_sha, tag)
    finally:
        import shutil
        shutil.rmtree(tag, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
