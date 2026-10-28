#!/usr/bin/env python3
"""Round-55 C1 mutation scoreboard (final).

Counter byteset: FROZEN sha256 5e8f50d1... (freeze.json amendment 7 digest,
= .ufo/evidence/round-55/c1/measure.py at C0 9cf0146).

Kill rule: a mutant is KILLED only if it deviates from the correct expectation
on a tree where the PRISTINE counter matched that expectation. On a blind-spot
tree (where pristine itself deviates) a mutant's coincidence is not evidence.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

S = Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1")
M = S / "mutants"
R = S / "receipts-c0"

# (label, lane, expected PASS, expected token, why)
TREES = [
    ("base", "clone", False, "total=10", "frozen base: ten classes mismatch (premise 9/10)"),
    ("C0", "current", True, "total=0", "the tree that reaches total=0 (C0 9cf0146)"),
    ("dirty", "dirtyC0", False, None,
     "C0 record content laid in the frozen rev's worktree uncommitted: REV vs worktree read"),
    ("noprem", "nopremiseC0", False, None, "C0 minus R54.1's premise receipt"),
    ("corronly", "corronly2", False, None,
     "corrections section + staged receipt present, in-place fixes reverted"),
    ("tailsec", "tailsec2", False, None,
     "a later `## ` section quotes stale tokens: exercises the corrections trim"),
    ("m1", "m1tree2", False, None, "`CTL_POS_c1 true` outside corrections"),
    ("m2", "m2tree2", True, "total=0", "receipt and section both say total=15"),
    ("m7", "m7tree2", False, None, "corrections say w1=99"),
    ("m9", "m9tree2", True, "total=0", "later commit touches the swept seat file"),
    ("m10", "m10tree2", True, "total=0", "freeze.json pins cafebabe, section follows"),
    ("m12", "m12tree2", True, "total=0", "staged receipt says 3, section follows"),
    ("m13", "m13tree2", True, "total=0", "frozen.stdout names deadbee1, section follows"),
    ("m14", "m14tree2", False, None, "hard-wrapped `positive control ... rekeyed=7/7`"),
    ("m15", "m15tree2", False, None, "`CTL_POS_c1 true` in LOG.md only"),
    ("m16", "m16tree2", False, None, "SUPERSEDED block removed from the seat file"),
    # --- false-negative probes: a CORRECT counter must also FAIL these
    ("f1", "f1b2", False, None, "third wrong pointer 097985c1 outside corrections"),
    ("f2", "f2b2", False, None, "wrong total=16 (not the literal 14) outside corrections"),
    ("f3", "f3b2", False, None, "lower-case ctl_pos_c1 true"),
    ("p7", "p7b", False, None, "stale c2 digest 49280fe5 outside corrections"),
    ("p9", "p9b", False, None, "wrong staged count 86 (regex literal is 84)"),
    ("p5", "p5b", False, None, "old finding counts outside corrections"),
    ("p10", "p10b", False, None, "rekeyed=0/30 quote outside corrections"),
    ("p8", "p8b", False, None, "corrections drop the word fabricated"),
]


def rev(lane):
    return subprocess.run(["git", "-C", str(S / lane), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def run(script, lane, rv, work):
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    cmd = [sys.executable, str(script), "--lane", str(S / lane), "--rev", rv,
           "--work", str(work), "--explain"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr, " ".join(cmd)


def verdict(out):
    for line in out.splitlines():
        if line.startswith("C1_R55: "):
            return line
    return ""


R.mkdir(parents=True, exist_ok=True)
scripts = [("pristine", M / "frozen-current-5e8f50d1.py")] \
    + sorted((p.stem, p) for p in M.glob("N[0-9]*.py"))
order = [t[0] for t in TREES]

report = {}
for tag, path in scripts:
    res = {}
    for label, lane, want_pass, wanttok, _why in TREES:
        rv = rev(lane)
        rc, out, err, cmd = run(path, lane, rv, S / ("wc0-%s-%s" % (tag, label)))
        v = verdict(out)
        ap = "C1_R55_PASS=true" in v
        ok = (ap == want_pass and rc == (0 if want_pass else 1)
              and (wanttok is None or wanttok in v))
        res[label] = {"rc": rc, "pass": ap, "as_expected": ok, "verdict": v,
                      "fails": [ln.split()[1] for ln in out.splitlines()
                                if ln.startswith("EXPLAIN ") and " FAIL " in ln]}
        (R / ("%s@%s.stdout" % (tag, label))).write_text(
            "$ %s\n[rc=%d]\n%s%s" % (cmd, rc, out, ("STDERR:\n" + err) if err else ""))
    report[tag] = res

# trees where pristine printed what a correct counter must print
sound = [k for k in order if report["pristine"][k]["as_expected"]]
blind = [k for k in order if not report["pristine"][k]["as_expected"]]

lines = ["| counter | " + " | ".join(order) + " | verdict |",
         "|---" * (len(order) + 2) + "|",
         "| (expected) | " + " | ".join("P" if t[2] else "F" for t in TREES)
         + " | baseline |"]
rows = []
for tag in [t[0] for t in scripts]:
    res = report[tag]
    cells = ["%s/%d%s" % ("P" if res[k]["pass"] else "F", res[k]["rc"],
                          "" if k in sound else "*") for k in order]
    dev_sound = [k for k in sound if not res[k]["as_expected"]]
    if tag == "pristine":
        vs = "BASELINE-OK" if not blind else "BASELINE-BLIND:" + ",".join(blind)
        verdict_s = vs
    else:
        verdict_s = ("KILLED@" + ",".join(dev_sound)) if dev_sound else "SURVIVED"
    lines.append("| %s | %s | %s |" % (tag, " | ".join(cells), verdict_s))
    rows.append({"mutant": tag, "verdict": verdict_s,
                 "deviates_on_sound": dev_sound,
                 "coincides_on_blind": [k for k in blind if res[k]["as_expected"]],
                 "cells": {k: res[k]["pass"] for k in order},
                 "rc": {k: res[k]["rc"] for k in order},
                 "fails": {k: res[k]["fails"] for k in order},
                 "sha256": hashlib.sha256(path_of.read_bytes()).hexdigest()
                 if (path_of := M / ("frozen-current-5e8f50d1.py" if tag == "pristine"
                                     else tag + ".py")).exists() else None})

# verdict ordering per the required tally
tally = {"KILLED": 0, "SURVIVED": 0}
for r in rows:
    if r["mutant"] != "pristine":
        tally[r["verdict"].split("@")[0]] += 1

md = ["# Round-55 C1 counter mutation matrix (counter sha256 5e8f50d1...)", "",
      "`*` marks a tree where the PRISTINE counter already deviates from the correct",
      "expectation: a mutant that happens to match there is coincidence, not a kill.",
      "", "sound trees: %s" % ", ".join(sound), "",
      "blind trees: %s" % (", ".join(blind) or "none"), ""]
md += lines
md += ["", "killed=%d survived=%d" % (tally["KILLED"], tally["SURVIVED"])]
(S / "matrix-c0.md").write_text("\n".join(md) + "\n")
(S / "matrix-c0.json").write_text(json.dumps(
    {"counter_sha256": hashlib.sha256((M / "frozen-current-5e8f50d1.py").read_bytes()).hexdigest(),
     "sound_trees": sound, "blind_trees": blind,
     "trees": [{"label": t[0], "lane": t[1], "rev": rev(t[1]), "expected_pass": t[2],
                "expected_token": t[3], "why": t[4]} for t in TREES],
     "tally": tally, "rows": rows}, indent=1) + "\n")
print("\n".join(md))
