#!/usr/bin/env python3
"""Round-55 lab probe: do the five counter-lazy modes stay lazy under real work?

Hypothesis: the five modes c2/measure.py calls lazy never call
strict_scratch_root(), even when their inputs make them work hardest.

Detector (per mode):
  * exit code equals the class the tool's own usage documents for that workload,
    under BOTH a usable and an unusable TMPDIR;
  * no frozen scratch-root grammar line and no RuntimeError/Traceback token in
    stdout or stderr under the unusable TMPDIR;
  * strace -f census: zero mkdir/mkdirat (and zero O_CREAT openat) under
    /tmp or the unusable TMPDIR.

Positive control: each tool's selftest under the same unusable TMPDIR must
refuse with exit 2 and the frozen grammar (proves the environment is really
unusable and the refusal path is armed).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

GRAMMAR = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.-]*(\.py)?: could-not-evaluate: cannot create clone "
    r"scratch under the scratch root: TMPDIR is not a usable directory: "
    r"'[^']*' \(could-not-evaluate\)$")
MARK = "cannot create clone scratch under the scratch root"
TIMEOUT = 900


def env(tmpdir, home):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    if tmpdir is None:
        e.pop("TMPDIR", None)
    else:
        e["TMPDIR"] = str(tmpdir)
    e["HOME"] = str(home)
    e.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
    return e


def run(argv, cwd, e):
    p = subprocess.run(argv, cwd=str(cwd), env=e, capture_output=True,
                       text=True, timeout=TIMEOUT)
    return p.returncode, p.stdout, p.stderr


def traced(argv, cwd, e, log):
    p = subprocess.run(
        ["strace", "-f", "-e", "trace=mkdir,mkdirat,openat", "-o", str(log), *argv],
        cwd=str(cwd), env=e, capture_output=True, text=True, timeout=TIMEOUT)
    return p.returncode


def census(log, bogus):
    text = log.read_text(errors="replace").splitlines() if log.exists() else []
    mkdir_lines = [l for l in text if re.search(r"\bmk(dir|dirat)\(", l)]
    scratch = [l for l in mkdir_lines if bogus in l or '"/tmp' in l]
    creat = [l for l in text if "openat(" in l and "O_CREAT" in l
             and (bogus in l or '"/tmp' in l)]
    return {"mkdir_total": len(mkdir_lines), "mkdir_scratch": scratch,
            "openat_creat_scratch": creat}


def modes(work):
    """(id, argv, expected rc, workload note).  Bench cwd is the clone."""
    w = str(work)
    return [
        ("pin-disposition --manifest",
         ["python3", "tools/pin-disposition.py", "--manifest",
          w + "/pin-manifest-mismatch.json", "--root",
          "/home/vgpnk/Projects/shokunin"], 0,
         "six real legs observed, every pin digest wrong, one pinned commit absent"),
        ("context-capture --check --receipt/--expected (mismatch)",
         ["python3", "tools/context-capture.py", "--check", "--receipt",
          ".ufo/evidence/round-14/context-receipt.json", "--expected",
          w + "/context-expected-exit1.json", "--json"], 1,
         "full re-derivation of the 29 KB receipt, then a pinned verdict mismatch"),
        ("context-capture --check --receipt/--expected (tampered)",
         ["python3", "tools/context-capture.py", "--check", "--receipt",
          ".ufo/evidence/round-14/context-receipt.json", "--expected",
          w + "/context-expected-tampered.json", "--json"], 2,
         "full receipt hashing, then a digest refusal"),
        ("context-capture --check (frozen receipt)",
         ["python3", "tools/context-capture.py", "--check", "--json"], 0,
         "frozen receipt re-derivation against the built-in digest/id/exit pin"),
        ("evidence-disposition --root . --dispositions (heavy, clean)",
         ["python3", "tools/evidence-disposition.py", "--root", ".",
          "--dispositions", ".ufo/evidence/round-18/dispositions.json", "--json"], 0,
         "four pins hashed, git historical inputs resolved, 13 checks replayed"),
        ("evidence-disposition --root ed-lane (failing)",
         ["python3", "tools/evidence-disposition.py", "--root",
          w + "/ed-lane", "--dispositions",
          w + "/ed-lane/.ufo/evidence/x/dispositions.json", "--json"], 1,
         "pinned fixture hashed and replayed, then a genuine failed row"),
        ("repeat-control --snapshot (mismatch)",
         ["python3", "tools/repeat-control.py", "--snapshot",
          ".ufo/evidence/round-12/ControlGate/mismatch"], 1,
         "three saved observations re-hashed and re-classified"),
        ("bash-witness-study count (tampered counts)",
         ["python3", "tools/bash-witness-study.py", "count",
          "--evidence", w + "/bashwitness"], 1,
         "ten saved rows and their raw logs re-derived, then a count mismatch"),
    ]


def controls():
    return [
        ("control:repeat-control --selftest",
         ["python3", "tools/repeat-control.py", "--selftest"]),
        ("control:context-capture --selftest",
         ["python3", "tools/context-capture.py", "--selftest"]),
        ("control:pin-disposition --selftest",
         ["python3", "tools/pin-disposition.py", "--selftest"]),
        ("control:evidence-disposition --selftest",
         ["python3", "tools/evidence-disposition.py", "--selftest"]),
        ("control:bash-witness-study selftest",
         ["python3", "tools/bash-witness-study.py", "selftest"]),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None,
                    help="substring filter on mode names (mutant arms)")
    a = ap.parse_args()
    clone, work, out = Path(a.clone), Path(a.work), Path(a.out)
    home = out / "home"
    home.mkdir(parents=True, exist_ok=True)
    usable = out / "tmp-usable"
    usable.mkdir(exist_ok=True)
    bogus = out / "no-such-tmpdir"
    if bogus.exists():
        raise SystemExit("bogus TMPDIR must not exist: %s" % bogus)

    results = {"label": a.label, "clone": str(clone),
               "tool_sha256": {p.name: __import__("hashlib").sha256(p.read_bytes()).hexdigest()
                               for p in sorted((clone / "tools").glob("*"))
                               if p.is_file()}, "modes": {}, "controls": {}}

    # Positive control: prove the unusable TMPDIR really refuses scratch.
    for name, argv in controls():
        rc, so, se = run(argv, clone, env(bogus, home))
        lines = [l for l in se.splitlines() if GRAMMAR.match(l)]
        results["controls"][name] = {
            "rc": rc, "grammar_lines": lines,
            "stderr": se.strip().splitlines()[:3],
            "stdout": so.strip().splitlines()[:3],
            "class_ok": rc == 2 and len(lines) == 1,
        }

    for name, argv, expected, note in modes(work):
        if a.only and a.only not in name:
            continue
        rec = {"argv": argv, "expected_rc": expected, "note": note}
        for arm, tmpdir in (("usable", usable), ("unusable", bogus)):
            e = env(tmpdir, home)
            rc, so, se = run(argv, clone, e)
            log = out / ("strace-%s-%s.log" % (re.sub(r"[^a-z0-9]+", "-",
                                                     name.lower()).strip("-"), arm))
            traced(argv, clone, e, log)
            rec[arm] = {
                "rc": rc, "stdout": so, "stderr": se,
                "scratch_marker": MARK in so + se,
                "grammar": [l for l in (so + se).splitlines() if GRAMMAR.match(l)],
                "runtime_error": "RuntimeError" in so + se,
                "traceback": "Traceback (most recent call last)" in so + se,
                "census": census(log, str(bogus)),
            }
        u, us = rec["unusable"], rec["usable"]
        rec["verdict"] = (
            "lazy-holds" if (
                u["rc"] == expected == us["rc"]
                and not u["scratch_marker"] and not u["grammar"]
                and not u["runtime_error"] and not u["traceback"]
                and not u["census"]["mkdir_scratch"]
                and not u["census"]["openat_creat_scratch"]
                # no scratch allocation anywhere in either arm: all seven
                # workloads are read-only modes, so mkdir itself is the signal
                and u["census"]["mkdir_total"] == 0
                and us["census"]["mkdir_total"] == 0)
            else "FALSIFIED")
        results["modes"][name] = rec

    out.mkdir(parents=True, exist_ok=True)
    (out / ("results-%s.json" % a.label)).write_text(
        json.dumps(results, indent=1) + "\n")
    for name, rec in results["modes"].items():
        u = rec["unusable"]
        print("%-58s rc=%s/%s expected=%s mkdir_scratch=%d creat_scratch=%d %s" % (
            name, u["rc"], rec["usable"]["rc"], rec["expected_rc"],
            len(u["census"]["mkdir_scratch"]), len(u["census"]["openat_creat_scratch"]),
            rec["verdict"]))
    for name, rec in results["controls"].items():
        print("%-58s rc=%s grammar=%d %s" % (
            name, rec["rc"], len(rec["grammar_lines"]),
            "ok" if rec["class_ok"] else "FAIL"))
    return 0 if all(r["verdict"] == "lazy-holds" for r in results["modes"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
