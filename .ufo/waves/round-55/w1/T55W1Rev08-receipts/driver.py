#!/usr/bin/env python3
"""T55W1Rev08: fixture driver for R54.4 / R54.10 correction byte-accuracy.

Each fixture is a `git clone --shared` of the lane at base, then the fixture's
SCORECARD.md gets a `## Round 55 - round-54 record corrections` block, a commit
is made IN THE FIXTURE (toplevel asserted equal to the fixture), and the frozen
round-55 c1 counter is run against the fixture.
"""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
S = "/fast/scratch/hyaku/tameshi-r55/T55W1Rev08"
BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
HEADING = "## Round 55 - round-54 record corrections"


def sh(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def blocks():
    """The two entries verbatim from the L1's live corrections section."""
    body = open(os.path.join(LANE, "SCORECARD.md"), encoding="utf-8").read().splitlines()
    out = {}
    cur, buf = None, []
    for line in body:
        if line.startswith("**ER-R54-"):
            if cur:
                out[cur] = "\n".join(buf).rstrip() + "\n"
            cur = line[2:line.index(" ")]
            buf = [line]
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).rstrip() + "\n"
    return out


def fixture(name, section, receipt_dir):
    d = os.path.join(S, name)
    shutil.rmtree(d, ignore_errors=True)
    r = sh("git", "clone", "--shared", LANE, d)
    assert r.returncode == 0, r.stderr
    r = sh("git", "-C", d, "checkout", "--detach", BASE)
    assert r.returncode == 0, r.stderr
    top = sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    with open(os.path.join(d, "SCORECARD.md"), "a", encoding="utf-8") as fh:
        fh.write("\n" + section)
    r = sh("git", "-C", d, "add", "SCORECARD.md")
    assert r.returncode == 0, r.stderr
    r = sh("git", "-C", d, "-c", "user.name=fixture", "-c",
           "user.email=fixture@local", "commit", "-q", "-m", name)
    assert r.returncode == 0, r.stderr
    rev = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    work = os.path.join(d, "_work")
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, os.path.join(LANE, ".ufo/evidence/round-55/c1/measure.py"),
           "--lane", d, "--rev", rev, "--work", work, "--explain"]
    run = sh(*cmd)
    text = run.stdout + run.stderr
    with open(os.path.join(receipt_dir, name + ".stdout"), "w", encoding="utf-8") as fh:
        fh.write("$ " + " ".join(cmd) + "\n" + text + "rc=%d\n" % run.returncode)
    keep = [ln for ln in text.splitlines()
            if ln.startswith(("EXPLAIN R54.4 ", "EXPLAIN R54.10 ", "C1_R55:"))]
    print("### %s rev=%s rc=%d" % (name, rev[:12], run.returncode))
    for ln in keep:
        print("   " + ln)
    return {ln.split()[1]: ("ok" in ln.split()[2]) for ln in keep if ln.startswith("EXPLAIN")}


def main():
    R = os.path.join(S, "receipts")
    os.makedirs(R, exist_ok=True)
    b = blocks()
    res = {}

    positive = HEADING + "\n\n" + b["ER-R54-4"] + "\n" + b["ER-R54-10"]
    res["pos"] = fixture("fix-pos", positive, R)

    neg4 = positive.replace("`8528ee85`", "`49280fe5`")
    assert "8528ee85" not in neg4
    res["neg4"] = fixture("fix-neg4", neg4, R)

    neg10 = b["ER-R54-10"].replace("prints `rekeyed=0/7`", "prints `rekeyed=0/30`")
    assert "rekeyed=0/7" not in neg10
    res["neg10"] = fixture("fix-neg10", HEADING + "\n\n" + b["ER-R54-4"] + "\n" + neg10, R)

    soup = HEADING + "\n\n" + (
        "**ER-R54-4 - soup.**\n"
        "`c2/measure.py` is the counter and is pinned at `8528ee85`.\n\n"
        "**ER-R54-10 - soup.**\n"
        "`controls-a.stdout` prints `rekeyed=0/7` for `CTL_0_c1`; the round-53\n"
        "counter `r53-counter-at-88afa941.stdout` prints `rekeyed=30/30`.\n")
    res["soup"] = fixture("fix-soup", soup, R)

    with open(os.path.join(R, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps(res, sort_keys=True))


if __name__ == "__main__":
    main()
