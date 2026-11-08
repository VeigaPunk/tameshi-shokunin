#!/usr/bin/env python3
"""R94M1 — mutation study of the C1 verdict-content reader.

READ-ONLY on the lane. Everything writable lives under $R94M1_SCRATCH
(default /fast/scratch/hyaku/tameshi-r94/R94M1/study).

What it does, per defect line in R94M1-defects.txt (pre-registered):
  1. clone the lane at REV (--shared) into scratch, materialize the battery
     state with the frozen driver's own states() definitions, commit inside the
     clone only (identity ctl <ctl@fixture.invalid>);
  2. run the PRISTINE counter (extracted from REV's object store) on that state
     and grade it with the battery's own expectation (baseline);
  3. write the single-edit mutant, recompute SELF_SHA256 for the mutated bytes
     (prep=pin) or leave it stale (prep=nopin, the self-pin probe), run it on
     the same state, grade it the same way;
  4. restore the exact pristine bytes into the mutant path, verify the sha256,
     and re-run the restored bytes on the same state;
  5. classify KILLED / SURVIVED / INCONCLUSIVE.

Detector = the battery's own pre-registered expectation for the exposing state
(controls-v94.py states()["<state>"]["expect"], or EXPECT_EXTRA for the two
setup controls). That expectation is what the frozen pre-freeze receipt records
for the honest counter, i.e. "the state refuses this note in this way".

E25 (gate identity) is probed against an INERT foreign gate fixture repo, not
against the battery's gate-foreign state: the battery's chosen foreign gate is
scripts/shokunin-watchdog.sh, a live fleet driver, and the battery's own control
never reaches materialize() because the identity check refuses first. A mutant
that removes the check WOULD execute it, so the probe points spec.gate.repo at
a scratch fixture repo holding a do-nothing `selftest` script with a different
sha256. The rule under test (GATE_COMMIT/GATE_SHA256 anchor) and the battery
expectation (exit 2, token gate-identity-mismatch) are unchanged.

Usage: python3 -I R94M1-driver.py [--jobs N] [--only ID ...] [--keep]
Exit 0 when every defect produced a verdict.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "7084358c732ebe1334c2eb9a352c3ed96b547f7c"
COUNTER_PATH = ".ufo/evidence/round-94/c1/measure-v94.py"
COUNTER_SHA = "a22563b0c2b4a2b43922cec3d1ab3fa511110e035b9edfdfdc6eaebb97023010"
CONTROLS = LANE + "/.ufo/evidence/round-94/c1/controls-v94.py"
W1 = LANE + "/.ufo/waves/round-94/w1"
SPEC_FILE = W1 + "/R94M1-defects.txt"
SCRATCH = os.environ.get("R94M1_SCRATCH", "/fast/scratch/hyaku/tameshi-r94/R94M1/study")
TREE_PATHS = ["corpus/knowledge/mutation-case-fleet-sources-census.md", "corpus/README.md",
              "corpus/SOURCES.md", "corpus/lessons/round-94.md",
              ".ufo/evidence/round-94/c1/census-mutants.json",
              ".ufo/evidence/round-94/c1/pins.json",
              ".ufo/evidence/round-94/c1/measure-v94.py"]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as f:
        return sha_bytes(f.read())


# The battery's gate-foreign state names scripts/shokunin-watchdog.sh, a live
# fleet driver. The battery expectation for gate identity is a setup refusal
# that fires before materialize(); only a mutant WITHOUT the anchor reaches the
# foreign gate. E25 is therefore probed against an inert foreign gate fixture
# (see the module docstring); the battery state name is kept in the receipt.
STATE_OVERRIDE = {"E25": "gate-foreign-inert"}


def load_controls():
    s = importlib.util.spec_from_file_location("ctl94", CONTROLS)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def sealed_git_out(args):
    p = subprocess.run(["git"] + args, capture_output=True,
                       env={"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8",
                            "LC_ALL": "C.UTF-8", "GIT_NO_REPLACE_OBJECTS": "1",
                            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"})
    if p.returncode != 0:
        raise SystemExit("git failed: %s\n%s" % (" ".join(args), p.stderr.decode()))
    return p.stdout


def read_spec():
    out = []
    with open(SPEC_FILE, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            d = json.loads(line)
            if "old" in d:
                d.setdefault("edits", [{"old": d["old"], "new": d["new"]}])
            d["line"] = ln
            out.append(d)
    ids = [d["id"] for d in out]
    assert len(ids) == len(set(ids)), "duplicate defect id"
    assert len(out) >= 16, "spec too short: %d" % len(out)
    return out


def extract_revtree(dest):
    """Committed bytes at REV for the files states() reads (never the work tree)."""
    os.makedirs(dest, exist_ok=True)
    arch = sealed_git_out(["-C", LANE, "archive", "--format=tar", REV, "--"] + TREE_PATHS)
    subprocess.run(["tar", "-x", "-C", dest], input=arch, check=True)
    missing = [p for p in TREE_PATHS if not os.path.exists(os.path.join(dest, p))]
    assert not missing, missing
    return dest


def build_inert_gate_repo(dest):
    """A foreign gate whose `selftest` does nothing (E25 probe only)."""
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(os.path.join(dest, "scripts", "fixtures", "sources-census", "root", "c-shokunin"),
                exist_ok=True)
    with open(os.path.join(dest, "scripts", "inert-gate.sh"), "w") as f:
        f.write("#!/usr/bin/env bash\n# inert foreign gate for the R94M1 gate-identity probe\n"
                "case \"${1:-}\" in selftest) echo \"selftest ok\"; exit 0;;\n"
                "validate) echo \"inert validate\"; exit 0;;\n*) exit 0;; esac\n")
    with open(os.path.join(dest, "scripts", "fixtures", "sources-census", "root", "c-shokunin",
                           ".keep"), "w") as f:
        f.write("inert\n")
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run(["git", "init", "-q", dest], check=True, env=env)
    top = subprocess.run(["git", "-C", dest, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, env=env).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "fixture toplevel mismatch"
    subprocess.run(["git", "-C", dest, "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", dest, "-c", "user.name=ctl", "-c",
                    "user.email=ctl@fixture.invalid", "commit", "-q", "-m",
                    "inert foreign gate"], check=True, env=env)
    commit = subprocess.run(["git", "-C", dest, "rev-parse", "HEAD"], capture_output=True,
                            text=True, env=env).stdout.strip()
    gate_sha = sha_file(os.path.join(dest, "scripts", "inert-gate.sh"))
    return commit, gate_sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    for sub in ("states", "mutants", "work", "receipts", "revtree"):
        os.makedirs(os.path.join(SCRATCH, sub), exist_ok=True)
    ctl = load_controls()
    defects = read_spec()
    for d in defects:
        d["battery_state"] = d["state"]
        d["state"] = STATE_OVERRIDE.get(d["id"], d["state"])
    if a.only:
        defects = [d for d in defects if d["id"] in a.only]
    pristine = sealed_git_out(["-C", LANE, "cat-file", "blob", REV + ":" + COUNTER_PATH])
    assert sha_bytes(pristine) == COUNTER_SHA, "instrument digest mismatch: " + sha_bytes(pristine)
    pristine_text = pristine.decode()
    pristine_path = os.path.join(SCRATCH, "pristine-counter.py")
    with open(pristine_path, "wb") as f:
        f.write(pristine)
    # anchor validation before any run
    for d in defects:
        for e in d["edits"]:
            n = pristine_text.count(e["old"])
            assert n == 1, "%s anchor occurs %d times: %r" % (d["id"], n, e["old"][:50])
        assert d["prep"] in ("pin", "nopin"), d["id"]
    revtree = extract_revtree(os.path.join(SCRATCH, "revtree"))
    C = ctl.states(revtree)
    for d in defects:
        if d["state"] not in C and d["state"] != "gate-foreign-inert":
            raise SystemExit("unknown state " + d["state"])
    inert_commit, inert_sha = build_inert_gate_repo(os.path.join(SCRATCH, "inert-gate"))

    # ---------------------------------------------------------------- states
    def build_state(name):
        dest = os.path.join(SCRATCH, "states", name)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        repo = ctl.clone_at(LANE, REV, dest)
        if name == "gate-foreign-inert":
            # Spec repointed at the inert foreign gate; everything else is the
            # battery's gate-foreign state (same battery expectation).
            spec = dict(C["gate-foreign"])
            spec["files"] = {".ufo/evidence/round-94/c1/census-mutants.json":
                             spec_edit_gate(revtree, inert_commit, inert_sha)}
        else:
            spec = C[name]
        ctl.materialize_state(repo, spec)
        ctl.sh("git", "-C", repo, "add", "-A")
        ctl.sh("git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
               "commit", "-q", "--allow-empty", "-m", "r94m1 state " + name)
        top = ctl.sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
        assert os.path.realpath(top) == os.path.realpath(repo), "state toplevel mismatch"
        return repo, ctl.sh("git", "-C", repo, "rev-parse", "HEAD").strip()

    def spec_edit_gate(tree, commit, sha):
        p = os.path.join(tree, ".ufo/evidence/round-94/c1/census-mutants.json")
        s = json.load(open(p, encoding="utf-8"))
        s["gate"].update(repo=os.path.join(SCRATCH, "inert-gate"), commit=commit,
                         path="scripts/inert-gate.sh", sha256=sha)
        return json.dumps(s, indent=1, ensure_ascii=False) + "\n"

    def want(d):
        if d["prep"] == "nopin":
            return ctl.EXPECT_EXTRA["selfpin-edit"]
        if d["state"] == "gate-foreign-inert":
            return (2, {"__setup": "gate-identity-mismatch"})
        return C[d["state"]]["expect"]

    states_needed = sorted({d["state"] for d in defects})
    built = {}
    with ThreadPoolExecutor(max_workers=min(6, len(states_needed))) as ex:
        futs = {n: ex.submit(build_state, n) for n in states_needed}
        for n, f in futs.items():
            built[n] = f.result()
    print("STATES " + " ".join("%s=%s" % (n, built[n][1][:10]) for n in states_needed))

    def run_counter(counter, repo, rev):
        work = tempfile.mkdtemp(dir=os.path.join(SCRATCH, "work"), prefix="w-")
        try:
            p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                                "--work", work], capture_output=True, text=True,
                               timeout=1800, stdin=subprocess.DEVNULL)
            return p.returncode, p.stdout + p.stderr
        finally:
            shutil.rmtree(work, ignore_errors=True)

    # ---------------------------------------------------------------- baselines
    base_keys = sorted({(d["state"], d["prep"]) for d in defects})
    baselines = {}

    def baseline(key):
        state, prep = key
        repo, rev = built[state]
        if prep == "nopin":
            bp = os.path.join(SCRATCH, "mutants", "baseline-nopin.py")
            with open(bp, "w") as f:
                f.write(pristine_text)
            with open(bp, "a") as f:
                f.write("\n# post-freeze edit (never committed)\n")
        else:
            bp = pristine_path
        rc, out = run_counter(bp, repo, rev)
        d = next(x for x in defects if x["state"] == state and x["prep"] == prep)
        ok = ctl.grade(d["id"], rc, out, want(d))
        return key, dict(exit=rc, sha=sha_file(bp), out=out, sha_out=sha_bytes(out.encode()),
                         ok=ok, conj=ctl.conj_of(out))

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for key, r in ex.map(baseline, base_keys):
            baselines[key] = r
    for k, r in sorted(baselines.items()):
        print("BASELINE %s/%s exit=%d grade=%s" % (k[0], k[1], r["exit"],
                                                  "MATCH" if r["ok"] else "MISMATCH"))

    # ---------------------------------------------------------------- probes
    def probe(d):
        did = d["id"]
        state, prep = d["state"], d["prep"]
        repo, rev = built[state]
        mpath = os.path.join(SCRATCH, "mutants", did + ".py")
        text = pristine_text
        for e in d["edits"]:
            text = text.replace(e["old"], e["new"], 1)
        assert text != pristine_text, did
        with open(mpath, "w") as f:
            f.write(text)
        if prep == "pin":
            ctl.recompute_pin(mpath)
        else:
            with open(mpath, "a") as f:
                f.write("\n# post-freeze edit (never committed)\n")
        msha = sha_file(mpath)
        rc, out = run_counter(mpath, repo, rev)
        ok = ctl.grade(did, rc, out, want(d))
        # restore exact pristine bytes, then re-run them on the same state
        with open(mpath, "wb") as f:
            f.write(pristine)
        rsha = sha_file(mpath)
        if prep == "pin":
            rc2, out2 = run_counter(pristine_path, repo, rev)
        else:
            bp = os.path.join(SCRATCH, "mutants", "baseline-nopin.py")
            rc2, out2 = run_counter(bp, repo, rev)
        bl = baselines[(state, prep)]
        restored_same = (sha_bytes(out2.encode()) == bl["sha_out"] and rc2 == bl["exit"])
        base_conj = bl["conj"]
        mconj = ctl.conj_of(out)
        moved = {k: [base_conj.get(k), mconj.get(k)] for k in sorted(set(base_conj) | set(mconj))
                 if base_conj.get(k) != mconj.get(k)}
        if not bl["ok"]:
            verdict = "INCONCLUSIVE"
            reason = "baseline does not satisfy the battery expectation"
        elif ok:
            verdict = "SURVIVED"
            reason = "mutant still satisfies exit=%d + graded conjuncts" % want(d)[0]
        else:
            verdict = "KILLED"
            if rc != want(d)[0]:
                reason = "exit %d != expected %d" % (rc, want(d)[0])
            else:
                reason = "conjunct moved: " + ", ".join("%s=%s->%s" % (k, v[0], v[1])
                                                        for k, v in moved.items())
            setup = [l for l in out.split("\n") if l.startswith("C1_SETUP ")]
            if setup:
                reason += " [" + setup[0] + "]"
        body = ("defect=%s rule=%s state=%s battery_state=%s prep=%s\n"
                "instrument_sha=%s\nmutant_sha=%s\nrestored_sha=%s pristine_sha=%s\n"
                "baseline_exit=%d baseline_grade=%s baseline_sha_out=%s\n"
                "mutant_exit=%d mutant_grade=%s\nrestored_exit=%d restored_matches_baseline=%s\n"
                "expect=%r\nexpect_text=%s\nmoved_conjuncts=%r\nverdict=%s reason=%s\n"
                "--- baseline output ---\n%s\n--- mutant output ---\n%s\n"
                "--- restored output ---\n%s\n") % (
                    did, d["rule"], state, d.get("battery_state"), prep, COUNTER_SHA, msha, rsha, sha_bytes(pristine),
                    bl["exit"], "MATCH" if bl["ok"] else "MISMATCH", bl["sha_out"],
                    rc, "MATCH" if ok else "MISMATCH", rc2, restored_same, want(d), d["expect"],
                    moved, verdict, reason, bl["out"], out, out2)
        with open(os.path.join(SCRATCH, "receipts", did + ".out"), "w") as f:
            f.write(body)
        return dict(id=did, rule=d["rule"], state=state, prep=prep, expect=d["expect"],
                    baseline_exit=bl["exit"], baseline_ok=bl["ok"], mutant_exit=rc,
                    mutant_ok=ok, moved=moved, verdict=verdict, reason=reason,
                    mutant_sha=msha, restored_sha=rsha, restored_same=restored_same,
                    conj=mconj, base_conj=base_conj)

    results = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for r in ex.map(probe, defects):
            results.append(r)
            print("PROBE %s %s exit=%d %s" % (r["id"], r["verdict"], r["mutant_exit"],
                                              r["reason"][:100]))
    results.sort(key=lambda r: ([x["id"] for x in defects].index(r["id"])))
    killed = sum(r["verdict"] == "KILLED" for r in results)
    survived = sum(r["verdict"] == "SURVIVED" for r in results)
    incon = sum(r["verdict"] == "INCONCLUSIVE" for r in results)
    print("C1_MUTATION_SUMMARY defects=%d killed=%d survived=%d inconclusive=%d" % (
        len(results), killed, survived, incon))
    print("SURVIVORS " + " ".join(r["id"] for r in results if r["verdict"] == "SURVIVED"))
    print("INCONCLUSIVE " + " ".join(r["id"] for r in results if r["verdict"] == "INCONCLUSIVE"))
    with open(os.path.join(W1, "R94M1-results.json"), "w") as f:
        json.dump(dict(instrument=COUNTER_SHA, rev=REV, defects=results), f, indent=1, sort_keys=True)
        f.write("\n")
    shutil.copytree(os.path.join(SCRATCH, "receipts"), os.path.join(W1, "R94M1-receipts"),
                    dirs_exist_ok=True)
    if not a.keep:
        for name in os.listdir(os.path.join(SCRATCH, "states")):
            shutil.rmtree(os.path.join(SCRATCH, "states", name), ignore_errors=True)
        shutil.rmtree(os.path.join(SCRATCH, "inert-gate"), ignore_errors=True)
    return 0 if incon == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
