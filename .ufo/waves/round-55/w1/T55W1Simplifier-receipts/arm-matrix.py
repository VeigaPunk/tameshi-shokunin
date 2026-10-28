#!/usr/bin/env python3
"""Arm-liveness matrix for the frozen round-55 C2 counter (NOT lane code).

Loads the counter from the lane at its frozen path, replaces ONLY the two
subprocess executors (`run`, `trace`) with a scripted responder, and calls the
frozen `main()` unmodified. Every arm predicate, every denominator, the `total`
arithmetic and the verdict line are the frozen code's own.

A scenario that the counter reports PASS=false while all observations are
perfect is a counter defect, not a tool defect.

Usage: arm-matrix.py LANE COUNTER REV FIXTURE_LANE
  LANE         the lane whose frozen counter is loaded (read only)
  COUNTER      path of c2/measure.py inside LANE
  REV          revision the counter checks out (must contain conforming docs)
  FIXTURE_LANE repo the counter clones from (a scratch clone carrying REV)
"""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
from pathlib import Path

MARKER = "could-not-evaluate: cannot create clone scratch under the scratch root"
CLASS_LINE = ("cannot create clone scratch under the scratch root: TMPDIR is not a "
              "usable directory: '%s' (could-not-evaluate)")

TOOL_LABEL = {
    "tools/env-diff.py": "env-diff",
    "tools/repeat-control.py": "repeat-control",
    "tools/registry-check.py": "registry-check",
    "tools/bash-witness-study.py": "bash-witness-study",
    "tools/pin-disposition.py": "pin-disposition",
    "tools/evidence-disposition.py": "evidence-disposition",
    "tools/context-capture.py": "context-capture",
}


def label_of(argv):
    tool = argv[1]
    rest = argv[2:]
    base = TOOL_LABEL[tool]
    if tool == "tools/env-diff.py":
        return base + (" --contract" if "--contract" in rest else " --selftest")
    if tool == "tools/registry-check.py":
        return base + (" --rev" if "--rev" in rest else " --selftest")
    if tool == "tools/repeat-control.py":
        return base + (" --snapshot" if "--snapshot" in rest else " --selftest")
    if tool == "tools/bash-witness-study.py":
        return base + (" count" if "count" in rest else " selftest")
    if tool == "tools/pin-disposition.py":
        return base + (" --read" if "--manifest" in rest else " --selftest")
    if tool == "tools/evidence-disposition.py":
        return base + (" --json" if "--dispositions" in rest else " --selftest")
    return base + (" --check" if "--check" in rest else " --selftest")


def arm_of(env):
    t = env.get("TMPDIR")
    if t is None:
        return "unset"
    if t == "":
        return "empty"
    return "usable" if os.path.isdir(t) else "unusable"


def load(measure_path):
    spec = importlib.util.spec_from_file_location("c2frozen_%d" % id(measure_path),
                                                 str(measure_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_scenario(mod, fixture_lane, rev, work, overrides, trace_mode):
    """overrides: {(label, arm): (rc, stdout, stderr)}; trace_mode: empty|tmp|missing."""
    real_modes = mod.modes(Path("/tmp/x"), Path("/tmp/y"))
    allocating = {m[0] for m in real_modes if m[3]}

    def stub_run(argv, cwd, env):
        label, arm = label_of(argv), arm_of(env)
        if (label, arm) in overrides:
            return overrides[(label, arm)]
        if arm == "unusable":
            if label in allocating:
                return (2, "", "%s: could-not-evaluate: %s"
                        % (label.split()[0], CLASS_LINE % env["TMPDIR"]))
            return (0, "", "")
        return (0, "", "")

    def stub_trace(argv, cwd, env, log):
        if trace_mode == "missing":
            return 0
        log = Path(log)
        log.parent.mkdir(parents=True, exist_ok=True)
        if trace_mode == "tmp":
            log.write_text('1234  mkdir("/tmp/leaked-census-dir", 0700) = 0\n')
        else:
            log.write_text('1234  mkdir("%s/ok", 0700) = 0\n' % env.get("TMPDIR", "/x"))
        return 0

    mod.run = stub_run
    mod.trace = stub_trace
    argv = ["measure.py", "--lane", str(fixture_lane), "--rev", rev,
            "--work", str(work)]
    old = sys.argv
    sys.argv = argv
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = mod.main()
    finally:
        sys.argv = old
    out = buf.getvalue()
    verdict = [l for l in out.splitlines() if l.startswith("C2_R55: ")][-1]
    receipts = json.loads((Path(work) / "c2-receipts.json").read_text())
    return rc, verdict, receipts


def main():
    lane, counter, rev, fixture_lane = sys.argv[1:5]
    scenarios = [
        ("S0 all-perfect (best case)", {}, "empty"),
        ("S1 grammar rc=3 with the line", {("registry-check --selftest", "unusable"): (3, "", "")}, "empty"),
        ("S2 grammar line on stdout", {("context-capture --selftest", "unusable"): (2, "x: " + CLASS_LINE % "/nope", "")}, "empty"),
        ("S3 grammar + Traceback token", {("pin-disposition --selftest", "unusable"): (2, "", "Traceback (most recent call last):\npin-disposition.py: could-not-evaluate: " + CLASS_LINE % "/nope")}, "empty"),
        ("S4 grammar + RuntimeError token", {("bash-witness-study selftest", "unusable"): (2, "", "witness: could-not-evaluate: " + CLASS_LINE % "/nope" + "\nRuntimeError: x")}, "empty"),
        ("S5 grammar line TWICE (one line?)", {("repeat-control --selftest", "unusable"): (2, "", "repeat-control: could-not-evaluate: " + CLASS_LINE % "/nope" + "\nrepeat-control: could-not-evaluate: " + CLASS_LINE % "/nope")}, "empty"),
        ("S6 grammar + stray second stderr line", {("env-diff --contract", "unusable"): (2, "", "env-diff: could-not-evaluate: " + CLASS_LINE % "/nope" + "\ninfo: continuing")}, "empty"),
        ("S12 conforming line with a %r double-quoted value", {("pin-disposition --selftest", "unusable"): (2, "", "pin-disposition.py: could-not-evaluate: " + CLASS_LINE % repr("/tmp/it's here"))}, "empty"),
        ("S7 lazy mode allocates (rc=2)", {("pin-disposition --read", "unusable"): (2, "", "")}, "empty"),
        ("S8 empty-arm treats '' as unusable", {("env-diff --selftest", "empty"): (2, "", "")}, "empty"),
        ("S9 usable-arm regression (rc=1)", {("registry-check --selftest", "usable"): (1, "", "")}, "empty"),
        ("S10 /tmp mkdir in the census", {}, "tmp"),
        ("S11 strace log missing", {}, "missing"),
    ]
    print("counter:", counter)
    print("rev:", rev)
    print()
    for name, overrides, tm in scenarios:
        work = Path(tempfile.mkdtemp(dir="/fast/scratch/hyaku/tameshi-r55/T55W1Simplifier/arms"))
        mod = load(counter)
        rc, verdict, receipts = run_scenario(mod, fixture_lane, rev, work, overrides, tm)
        print("=== %s" % name)
        print("    rc=%s %s" % (rc, verdict))
        if receipts["bad"]:
            print("    bad-keys=%s" % sorted(receipts["bad"]))
    # Doc-arm mutants run against a second fixture clone with docs broken.
    print()


if __name__ == "__main__":
    main()
