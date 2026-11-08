#!/usr/bin/env python3
"""T91E1 independent reproduction of R91-C1 verdicts (kill rule C1-(b)).

Outside the sealed counter: materializes a pristine copy of the pinned gate
(scripts/sources-census.sh @ f47ad6ba...) plus its fixtures under scratch,
verifies the pristine selftest, applies each census-mutant's exact old->new
edit with its own code (assert old occurs exactly once), runs the gate's own
`selftest` in the ordinary shell environment (no env -i), twice per mutant,
records rc + SURVIVED/killed arm lines, derives the verdict (rc==0 ->
SURVIVED else KILLED, unstable if the two runs differ), compares against the
CTL1b control receipt's C1_ROW lines, then runs the sealed counter once at
the freeze rev and prints its full stdout.

Stdlib only. Read-only git on the fleet/lane repos (archive/show/rev-parse);
all writes under SCRATCH (default /fast/scratch/hyaku/tameshi-r91/T91E1).
Usage: T91E1_SCRATCH=/fast/scratch/hyaku/tameshi-r91/T91E1 python3 T91E1-repro.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

FLEET = "/home/vgpnk/Projects/shokunin"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
FLEET_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
GATE_PATH = "scripts/sources-census.sh"
GATE_SHA = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
SPEC_PATH = os.path.join(LANE, ".ufo/evidence/round-91/c1/census-mutants.json")
CTL_PATH = os.path.join(
    LANE, ".ufo/evidence/round-91/pre-freeze/controls/CTL1b-nowork-A.out"
)
COUNTER = os.path.join(LANE, ".ufo/evidence/round-91/c1/measure-v91.py")
FREEZE_REV = "50e59d59a5b0fffffe7a0e99da9a39397f2f94fc"
SCRATCH = os.environ.get(
    "T91E1_SCRATCH", "/fast/scratch/hyaku/tameshi-r91/T91E1"
)
SELFTEST_TIMEOUT = 180

failures = []


def note_fail(msg):
    failures.append(msg)
    print("FAIL " + msg, flush=True)


def run_selftest(gate, depth=1):
    """Run the gate's own selftest in the ordinary shell environment."""
    env = dict(os.environ)  # ordinary environment; never env -i
    try:
        p = subprocess.run(
            ["bash", gate, "selftest"],
            cwd=os.path.dirname(gate),
            capture_output=True,
            timeout=SELFTEST_TIMEOUT,
            env=env,
        )
        return p.returncode, p.stdout.decode("utf-8", errors="replace"), (
            p.stderr.decode("utf-8", errors="replace")
        )
    except subprocess.TimeoutExpired:
        return None, "", "timeout"


def arm_lines(out):
    lines = out.split("\n")
    surv = [l.split("\t", 1)[1].split(" (")[0] for l in lines if l.startswith("SURVIVED\t")]
    killed_n = sum(1 for l in lines if l.startswith("killed\t"))
    return surv, killed_n


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    tmp = os.path.join(SCRATCH, "tmp")
    os.makedirs(tmp, exist_ok=True)
    os.environ["TMPDIR"] = tmp

    # --- preconditions: freeze rev exists; spec + controls readable; pin ok
    v = subprocess.run(
        ["git", "-C", LANE, "rev-parse", "--verify", FREEZE_REV],
        capture_output=True,
    )
    if v.returncode != 0:
        note_fail("freeze-rev-not-found:" + FREEZE_REV)
        return 2
    spec_bytes = open(SPEC_PATH, "rb").read()
    spec = json.loads(spec_bytes)
    mutants = spec["mutants"]
    if spec["gate"]["commit"] != FLEET_COMMIT or spec["gate"]["path"] != GATE_PATH:
        note_fail("spec-gate-mismatch")
    print("SPEC sha256=" + hashlib.sha256(spec_bytes).hexdigest())
    print("SPEC n_mutants=%d" % len(mutants))

    expected = {}
    for line in open(CTL_PATH).read().split("\n"):
        if line.startswith("C1_ROW "):
            toks = line.split(" ")[1:]
            parts = {"id": toks[0]}
            parts.update(kv.split("=", 1) for kv in toks[1:])
            expected[parts["id"]] = parts
    if len(expected) != len(mutants):
        note_fail("controls-rows=%d" % len(expected))

    # --- materialize pristine copy exactly per seat spec (read-only git) ---
    g = os.path.join(SCRATCH, "g")
    if os.path.isdir(g):
        shutil.rmtree(g)
    os.makedirs(os.path.join(g, "scripts"), exist_ok=True)
    pipe = (
        "git -C %s archive --format=tar %s scripts/fixtures/sources-census | "
        "tar -x -C %s" % (FLEET, FLEET_COMMIT, g)
    )
    r = subprocess.run(["bash", "-c", pipe])
    if r.returncode != 0:
        note_fail("archive-extract-rc=%d" % r.returncode)
    show = subprocess.run(
        ["git", "-C", FLEET, "show", "%s:%s" % (FLEET_COMMIT, GATE_PATH)],
        capture_output=True,
    )
    if show.returncode != 0:
        note_fail("show-rc=%d" % show.returncode)
        return 1
    gate_p = os.path.join(g, GATE_PATH)
    with open(gate_p, "wb") as f:
        f.write(show.stdout)
    os.chmod(gate_p, 0o755)
    gate_bytes = show.stdout
    if hashlib.sha256(gate_bytes).hexdigest() != GATE_SHA:
        note_fail("gate-sha-mismatch")
    else:
        print("GATE sha256=" + GATE_SHA + " (matches spec pin)")
    gate_text = gate_bytes.decode("utf-8")
    if not os.path.isdir(os.path.join(g, "scripts/fixtures/sources-census")):
        note_fail("fixtures-absent")
    print("FIXTURES present")

    # --- pristine selftest twice: exit 0 and 'selftest ok' ---
    for i in (1, 2):
        rc, out, err = run_selftest(gate_p)
        ok = rc == 0 and "selftest ok" in out
        print("PRISTINE run%d rc=%s selftest_ok=%s" % (i, rc, ok))
        if not ok:
            note_fail("pristine-not-green run%d rc=%s" % (i, rc))

    # --- per-mutant independent reproduction ---
    results = []
    for m in mutants:
        mid, old, new = m["id"], m["old"], m["new"]
        cnt = gate_text.count(old)
        if cnt != 1:
            note_fail("%s old-count=%d" % (mid, cnt))
        if new == old:
            note_fail("%s noop" % mid)
        md = os.path.join(SCRATCH, "m-" + mid)
        if os.path.isdir(md):
            shutil.rmtree(md)
        shutil.copytree(g, md)
        mgp = os.path.join(md, GATE_PATH)
        mtext = gate_text.replace(old, new, 1)
        with open(mgp, "wb") as f:
            f.write(mtext.encode("utf-8"))
        os.chmod(mgp, 0o755)
        n = subprocess.run(["bash", "-n", mgp], capture_output=True)
        if n.returncode != 0:
            note_fail("%s bash-n-rc=%d" % (mid, n.returncode))
        runs = []
        for _ in range(2):
            rc, out, err = run_selftest(mgp)
            surv, killed_n = arm_lines(out)
            verdict = (
                "INCONCLUSIVE" if rc is None else ("SURVIVED" if rc == 0 else "KILLED")
            )
            runs.append(
                dict(rc=rc, out=out, err=err, surv=surv, killed_n=killed_n,
                     verdict=verdict)
            )
        derived = (
            runs[0]["verdict"]
            if runs[0]["verdict"] == runs[1]["verdict"]
            else "UNSTABLE"
        )
        exp = expected.get(mid, {})
        match = derived == exp.get("note") == exp.get("derived")
        print(
            "MUTANT %s rc1=%s rc2=%s derived=%s expected_derived=%s expected_note=%s match=%s"
            % (
                mid,
                runs[0]["rc"],
                runs[1]["rc"],
                derived,
                exp.get("derived"),
                exp.get("note"),
                match,
            )
        )
        for i, r in enumerate(runs, 1):
            print(
                "  run%d SURVIVED_arms=%s killed_arms=%d tail=%s"
                % (
                    i,
                    ",".join(r["surv"]) if r["surv"] else "(none)",
                    r["killed_n"],
                    ("selftest ok" if "selftest ok" in r["out"] else "selftest FAILED"),
                )
            )
        if derived != exp.get("note"):
            note_fail("%s differs: mine=%s note=%s" % (mid, derived, exp.get("note")))
        results.append((m, runs, derived, exp))

    # --- sealed counter, once, at the freeze rev (full stdout pasted) ---
    work = os.path.join(SCRATCH, "counter-work")
    os.makedirs(work, exist_ok=True)
    if os.listdir(work):
        note_fail("counter-work-not-empty")
    print("=== COUNTER-BEGIN ===")
    c = subprocess.run(
        [sys.executable, "-I", COUNTER, "--repo", LANE, "--rev", FREEZE_REV,
         "--work", work],
        capture_output=True,
        timeout=1800,
    )
    sys.stdout.write("=== COUNTER-BEGIN ===\n")
    sys.stdout.write(c.stdout.decode("utf-8", errors="replace"))
    sys.stdout.write("=== COUNTER-END rc=%d ===\n" % c.returncode)
    if c.stderr:
        sys.stdout.write("=== COUNTER-STDERR ===\n")
        sys.stdout.write(c.stderr.decode("utf-8", errors="replace"))

    print("=== SUMMARY ===")
    ndiff = sum(1 for (_, _, d, e) in results if d != e.get("note"))
    print("PROVISIONAL n=%d verdict_differs=%d" % (len(results), ndiff))
    print("PROVISIONAL " + ("reproducible" if ndiff == 0 else "differs"))
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  " + f)
    return 0 if (ndiff == 0 and not failures) else 1


if __name__ == "__main__":
    sys.exit(main())
