#!/usr/bin/env python3
"""T90E1 independent reproduction of the round-90 C1 census mutation verdicts.

Kill rule C1-(b): reproduce, OUTSIDE the frozen counter, the 12 mutant verdicts of
.ufo/evidence/round-90/c1/census-mutants.json against the fleet gate
scripts/sources-census.sh @ f47ad6ba8d306f8125597401cb2ce45c1297a593, measured
under the gate's own `selftest` mode.

Method (independent of measure.py; no shared code path):
  1. Materialize a pristine copy D/scripts/sources-census.sh + D/scripts/fixtures/
     sources-census from the fleet git objects.
  2. Assert the copy's sha256 equals the spec pin and that pristine `selftest`
     exits 0 printing `selftest ok` (twice).
  3. For each mutant, on its own fresh copy of D: assert the spec `old` string
     occurs EXACTLY once, replace it once with `new`, run `selftest` twice in the
     ordinary environment (only TMPDIR is pointed at the seat scratch), record rc
     and every line whose first field is SURVIVED. rc 0 = SURVIVED, else KILLED.
  4. Compare with the C1_ROW lines of pre-freeze control CTL1b-nowork-A.out.
  5. Run the frozen counter once at the freeze rev 3485ceb0 and print its stdout.

Usage:
  python3 T90E1-repro.py --scratch /fast/scratch/hyaku/tameshi-r90/T90E1 \
      [--lane /home/vgpnk/Projects/shokunin/tameshi-shokunin] \
      [--fleet /home/vgpnk/Projects/shokunin] \
      [--ctl .ufo/evidence/round-90/pre-freeze/controls/CTL1b-nowork-A.out] \
      [--freeze 3485ceb08df394edf5fbe26bd09b03985a04fba1] \
      [--skip-counter]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

FLEET_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
GATE_REL = "scripts/sources-census.sh"
FIX_REL = "scripts/fixtures/sources-census"
SPEC_REL = ".ufo/evidence/round-90/c1/census-mutants.json"
MEASURE_REL = ".ufo/evidence/round-90/c1/measure.py"
TIMEOUT = 200


def run(argv, cwd, tmpdir, timeout=TIMEOUT, stdin_devnull=True):
    env = dict(os.environ)
    env["TMPDIR"] = tmpdir
    return subprocess.run(
        argv, cwd=cwd, env=env, capture_output=True, text=True,
        timeout=timeout, stdin=subprocess.DEVNULL if stdin_devnull else None)


def selftest(copy_dir, tmpdir):
    return run(["bash", os.path.join(copy_dir, GATE_REL), "selftest"],
               os.path.dirname(os.path.join(copy_dir, GATE_REL)), tmpdir)


def survived_arms(stdout):
    arms = []
    for line in stdout.splitlines():
        parts = re.split(r"\t+", line, maxsplit=1)
        if len(parts) == 2 and parts[0] == "SURVIVED":
            arms.append(parts[1])
    return arms


def materialize(dest, fleet):
    gate_dir = os.path.join(dest, "scripts")
    os.makedirs(gate_dir, exist_ok=True)
    arch = subprocess.run(
        ["git", "-C", fleet, "archive", "--format=tar", FLEET_COMMIT, FIX_REL],
        capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", dest], input=arch, check=True)
    gate_bytes = subprocess.run(
        ["git", "-C", fleet, "show", FLEET_COMMIT + ":" + GATE_REL],
        capture_output=True, check=True).stdout
    gate_path = os.path.join(dest, GATE_REL)
    with open(gate_path, "wb") as f:
        f.write(gate_bytes)
    os.chmod(gate_path, 0o755)
    return gate_bytes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/tameshi-shokunin")
    ap.add_argument("--fleet", default="/home/vgpnk/Projects/shokunin")
    ap.add_argument("--ctl", default=".ufo/evidence/round-90/pre-freeze/controls/CTL1b-nowork-A.out")
    ap.add_argument("--freeze", default="3485ceb08df394edf5fbe26bd09b03985a04fba1")
    ap.add_argument("--skip-counter", action="store_true")
    ap.add_argument("--log", default="")
    a = ap.parse_args()

    scratch = os.path.realpath(a.scratch)
    os.makedirs(scratch, exist_ok=True)
    tmpdir = os.path.join(scratch, "tmp")
    os.makedirs(tmpdir, exist_ok=True)
    d0 = os.path.join(scratch, "g")
    if os.path.exists(d0):
        shutil.rmtree(d0)

    out = []

    def say(s=""):
        out.append(s)
        print(s, flush=True)

    say("T90E1 independent reproduction (outside measure.py)")
    fleet_commit = subprocess.run(
        ["git", "-C", a.fleet, "rev-parse", FLEET_COMMIT + "^{commit}"],
        capture_output=True, text=True, check=True).stdout.strip()
    say("fleet_commit=" + fleet_commit)

    gate_bytes = materialize(d0, a.fleet)
    copied = open(os.path.join(d0, GATE_REL), "rb").read()
    sha = hashlib.sha256(copied).hexdigest()
    spec = json.load(open(os.path.join(a.lane, SPEC_REL)))
    pin_sha = spec["gate"]["sha256"]
    say("pristine_sha256=%s pin_match=%s" % (sha, sha == pin_sha))
    if sha != pin_sha:
        say("FATAL: pristine gate sha256 does not match the spec pin")
        return 2

    for i in (1, 2):
        p = selftest(d0, tmpdir)
        ok = "selftest ok" in p.stdout
        say("PRISTINE run%d rc=%d selftest_ok=%s" % (i, p.returncode, ok))
        if p.returncode != 0 or not ok:
            say("FATAL: pristine selftest not green")
            say(p.stdout)
            say(p.stderr)
            return 2

    rows = []
    for m in spec["mutants"]:
        mid = m["id"]
        md = os.path.join(scratch, "m-" + mid)
        if os.path.exists(md):
            shutil.rmtree(md)
        shutil.copytree(d0, md, symlinks=True)
        gp = os.path.join(md, GATE_REL)
        text = open(gp, encoding="utf-8").read()
        count = text.count(m["old"])
        if count != 1:
            say("MUT %s INVALID old_occurrences=%d" % (mid, count))
            rows.append(dict(id=mid, rc="invalid", arms=[], verdict="INVALID",
                             old_count=count, sha="", stderr=""))
            continue
        mtext = text.replace(m["old"], m["new"], 1)
        with open(gp, "w", encoding="utf-8") as f:
            f.write(mtext)
        msha = hashlib.sha256(open(gp, "rb").read()).hexdigest()
        rcs = []
        arms = []
        errs = []
        for i in (1, 2):
            p = selftest(md, tmpdir)
            rcs.append(p.returncode)
            arms.append(survived_arms(p.stdout))
            if p.stderr.strip():
                errs.append(p.stderr.strip())
            say("MUT %s run%d rc=%d survived_arms=%s" % (
                mid, i, p.returncode, "|".join(survived_arms(p.stdout)) or "-"))
        verdict = "SURVIVED" if all(r == 0 for r in rcs) else "KILLED"
        if len(set(rcs)) > 1:
            verdict = "UNSTABLE"
        merged_arms = sorted({arm for group in arms for arm in group})
        rows.append(dict(id=mid, rc=rcs, arms=merged_arms, verdict=verdict,
                         old_count=count, sha=msha, stderr=" ".join(errs)[:400]))
        shutil.rmtree(md, ignore_errors=True)

    # counter receipt comparison (pre-freeze CTL1b)
    ctl = {}
    ctl_path = os.path.join(a.lane, a.ctl)
    for line in open(ctl_path, encoding="utf-8").read().splitlines():
        mm = re.match(r"^C1_ROW (C\d\d) derived=(\w+)", line)
        if mm:
            ctl[mm.group(1)] = mm.group(2)
    say()
    say("COUNTER_RECEIPT " + a.ctl)
    say("counter_rows=%d" % len(ctl))
    disagree = []
    for r in rows:
        cv = ctl.get(r["id"], "-")
        agree = "yes" if cv == r["verdict"] else "NO"
        if agree == "NO":
            disagree.append(r["id"])
        r["counter"] = cv
        r["agree"] = agree
    say("agree=%d/%d disagree=%s" % (len(rows) - len(disagree), len(rows),
                                      ",".join(disagree) or "none"))

    # markdown table
    say()
    say("| id | rc run1/run2 | selftest arm(s) printed SURVIVED | my verdict | counter verdict | agree? |")
    say("|---|---|---|---|---|---|")
    for r in rows:
        rc = "%s/%s" % tuple(r["rc"]) if isinstance(r["rc"], list) else r["rc"]
        arms = ", ".join("`%s`" % x for x in r["arms"]) if r["arms"] else "—"
        say("| %s | %s | %s | %s | %s | %s |" % (
            r["id"], rc, arms, r["verdict"], r["counter"], r["agree"]))

    freeze_ok = True
    freeze_stdout = ""
    if not a.skip_counter:
        work = os.path.join(scratch, "counter-work")
        if os.path.exists(work):
            shutil.rmtree(work)
        os.makedirs(work)
        measure = os.path.join(a.lane, MEASURE_REL)
        say()
        say("FREEZE_COUNTER_CMD python3 -I %s --repo %s --rev %s --work %s" % (
            measure, a.lane, a.freeze, work))
        p = run(["python3", "-I", measure, "--repo", a.lane, "--rev", a.freeze,
                 "--work", work], a.lane, tmpdir, timeout=600)
        freeze_stdout = p.stdout + p.stderr
        say(freeze_stdout.rstrip("\n"))
        say("FREEZE_COUNTER_EXIT=%d" % p.returncode)
        rows_freeze = {}
        for line in p.stdout.splitlines():
            mm = re.match(r"^C1_ROW (C\d\d) derived=(\w+)", line)
            if mm:
                rows_freeze[mm.group(1)] = mm.group(2)
        bad = [r["id"] for r in rows if rows_freeze.get(r["id"]) != r["verdict"]]
        freeze_ok = not bad
        say("FREEZE_VS_INDEPENDENT disagree=%s" % (",".join(bad) or "none"))
        shutil.rmtree(work, ignore_errors=True)

    say()
    if disagree:
        say("VERDICT: disagree:" + ",".join(disagree))
    else:
        say("VERDICT: reproduced-%d/%d" % (len(rows), len(rows)))
    if not freeze_ok:
        say("NOTE: freeze counter rows also compared; independent vs freeze disagree above")

    if a.log:
        with open(a.log, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
    return 0 if not disagree and freeze_ok else 1


if __name__ == "__main__":
    sys.exit(main())
