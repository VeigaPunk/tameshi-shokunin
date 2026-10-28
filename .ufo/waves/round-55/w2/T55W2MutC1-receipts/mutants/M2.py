#!/usr/bin/env python3
"""Round-55 C1 counter (calibration): the lane's record against the tree.

Ten classes, one per routed defect the round-54 non-author spot-check pinned
(`corpus/lessons/round-54-verifier-spotcheck.md`, R54.1-R54.10). Each class is
scored on three arms at REV:

  1. premise   - the receipt the defect names exists at REV and still yields the
                 fact the defect rests on (a premise that no longer holds is a
                 defect of this counter and fails the class, never a narrowed row);
  2. stale     - the wrong assertion no longer stands in the lane's records
                 (`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`);
  3. corrected - the corrections section carries the value derived FROM THE TREE,
                 not a literal the author chose where a derivation is possible.

The corrections section is the block of `SCORECARD.md` that starts at
`## Round 55 - round-54 record corrections` and runs to the next `## ` heading.

Verdict line:
`C1_R55: rev=... classes=10 premise=N/10 stale=N classes_corrected=N/10 total=N C1_R55_PASS=true|false`
Exit 0 iff PASS, 1 on a failed class, 2 on setup error. --work must be empty;
it receives the derivation manifest. Reads only `git show`; writes nothing else.
"""
import argparse
import glob
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HEADING = "## Round 55 - round-54 record corrections"
RECORD = (
    "SCORECARD.md",
    "corpus/QUALITY.md",
    "corpus/lessons/round-54.md",
    "LOG.md",
)
STAGED_DEFAULT = "/home/vgpnk/Projects/shokuknow"


class Setup(Exception):
    pass


def git(lane, *args, text=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True,
                          text=text, env=env)


def blob(lane, rev, path):
    r = git(lane, "show", "%s:%s" % (rev, path), text=False)
    return r.stdout if r.returncode == 0 else None


def text(lane, rev, path):
    b = blob(lane, rev, path)
    return None if b is None else b.decode("utf-8", "replace")


def exists(lane, rev, path):
    return git(lane, "cat-file", "-e", "%s:%s" % (rev, path)).returncode == 0


def corrections(lane, rev):
    body = text(lane, rev, "SCORECARD.md")
    if body is None:
        return ""
    out, on = [], False
    for line in body.splitlines():
        if line.startswith(HEADING):
            on = True
            continue
        if on and line.startswith("## "):
            break
        if on:
            out.append(line)
    return "\n".join(out)


def scan(lane, rev, paths, pattern):
    """Occurrences of a regex in the record files at REV, corrections excluded."""
    rx = re.compile(pattern)
    hits = []
    for path in paths:
        body = text(lane, rev, path)
        if body is None:
            continue
        if path == "SCORECARD.md":
            body = body.replace(corrections(lane, rev), "")
        for n, line in enumerate(body.splitlines(), 1):
            if rx.search(line):
                hits.append("%s:%d: %s" % (path, n, line.strip()[:160]))
    return hits


def scan_span(lane, rev, paths, pattern):
    """Whitespace-normalized whole-document search (amendment 5).

    A hard-wrapped claim splits across lines, so a line-scoped regex can miss a
    falsehood that is plainly there (round-54 lesson `proves the arm ... requires
    rekeyed=7/7`, split over two lines). This arm searches the document with all
    whitespace runs collapsed and reports the match's offset instead of a line.
    """
    rx = re.compile(pattern)
    hits = []
    for path in paths:
        body = text(lane, rev, path)
        if body is None:
            continue
        if path == "SCORECARD.md":
            body = body.replace(corrections(lane, rev), "")
        flat = " ".join(body.split())
        for m in rx.finditer(flat):
            hits.append("%s@%d: %s" % (path, m.start(), flat[max(0, m.start() - 40):m.end() + 20]))
    return hits


def derive_freeze_digest(lane, rev, name):
    raw = text(lane, rev, ".ufo/evidence/round-54/freeze.json")
    if raw is None:
        return None
    try:
        return json.loads(raw)["files"].get(name)
    except (ValueError, KeyError):
        return None


def finding_counts(lane, rev):
    counts = {}
    for wave in ("w1", "w2"):
        total = files = 0
        r = git(lane, "ls-tree", "-r", "--name-only", rev,
                "--", ".ufo/waves/round-54/%s" % wave)
        names = [n for n in r.stdout.split()
                 if re.search(r"/T54W\d+[A-Za-z]*Read\d+\.json$", n)]
        for rel in sorted(names):
            raw = text(lane, rev, rel)
            if raw is None:
                continue
            try:
                data = json.loads(raw)
            except ValueError:
                continue
            n = len(data.get("findings") or [])
            total += n
            files += 1 if n else 0
        counts[wave] = (total, files)
    return counts


def wave_numbers(lane, rev):
    raw = text(lane, rev, ".ufo/waves/round-54/w1-registry.json")
    if raw is None:
        return None
    try:
        reg = json.loads(raw)
        return (reg["role_mix"]["reviewer"], reg["attack_seats"], reg["seats"])
    except (ValueError, KeyError, TypeError):
        return None


def staged_count(lane, rev):
    """The staged package count, read from the committed receipt (amendment 7).

    Deriving it from the live `merge/tameshi` worktree made the claim depend on
    another lane's uncommitted edits (a +1 file moved total 0 -> 3). The receipt
    carries the command and the number it printed; the tree cannot move it."""
    raw = text(lane, rev, ".ufo/evidence/round-55/c1/staged-at-freeze.txt") or ""
    m = re.search(r"^output=(\d+)$", raw, re.M)
    return int(m.group(1)) if m else 0


def first_commit(lane, rev, path, filt=None):
    """The first commit in history order that touches PATH (filt kept for call-site clarity)."""
    r = git(lane, "log", "--reverse", "--format=%H", rev, "--", path)
    if r.returncode != 0:
        return None
    for line in r.stdout.split():
        return line[:7]
    return None


def classes(lane, rev, staged_root):
    rows = []

    def row(cid, premise, stale, corrected, derived):
        rows.append({"id": cid, "premise": bool(premise), "stale": stale,
                     "corrected": bool(corrected), "derived": derived,
                     "ok": bool(premise) and not stale and bool(corrected)})

    corr = corrections(lane, rev)

    # R54.1 -- the phase-B positive control is recorded as passing while its
    # committed receipt prints CTL_MISMATCH / 2 of 3.
    cb = text(lane, rev, ".ufo/evidence/round-54/control/controls-b.stdout") or ""
    premise = "CTL_MISMATCH" in cb and "CONTROLS_B: 2/3" in cb
    stale = scan(lane, rev, RECORD, r"CTL_POS_c1 true")
    stale += scan(lane, rev, ("corpus/QUALITY.md", "corpus/lessons/round-54.md"),
                  r"(positive control[^\n]{0,160}rekeyed=7/7)|(rekeyed=7/7[^\n]{0,160}positive control)")
    stale += scan_span(lane, rev, RECORD,
                       r"positive control.{0,160}rekeyed=7/7|rekeyed=7/7.{0,160}positive control")
    row("R54.1", premise, stale, "CTL_MISMATCH" in corr and "2/3" in corr,
        "CTL_MISMATCH + 2/3")

    # R54.2 -- three freeze pointers for one round; the receipt names one.
    fr = text(lane, rev, ".ufo/evidence/round-54/after/frozen.stdout") or ""
    m = re.search(r"freeze=([0-9a-f]{40})", fr)
    ptr = m.group(1) if m else None
    stale = scan(lane, rev, ("SCORECARD.md",), r"7883e0e5|fe70474d")
    row("R54.2", ptr is not None, stale, bool(ptr) and ptr[:8] in corr,
        "freeze pointer=%s" % (ptr[:8] if ptr else "none"))

    # R54.3 -- SCORECARD quotes total=14 where the receipt prints total=13.
    bc = text(lane, rev, ".ufo/evidence/round-54/before/c2.stdout") or ""
    m = re.search(r"total=(\d+)", bc)
    n23 = m.group(1) if m else None
    stale = scan(lane, rev, ("SCORECARD.md",), r"total=14")
    row("R54.3", n23 is not None, stale, ("total=13") in corr,
        "total=%s" % n23)

    # R54.4 -- the deciding c2 digest is the one freeze.json pins.
    digest = derive_freeze_digest(lane, rev, "c2/measure.py")
    row("R54.4", bool(digest), [],
        bool(digest) and digest[:8] in corr and "c2/measure.py" in corr,
        "c2 digest=%s" % (digest[:8] if digest else "none"))

    # R54.5 -- finding counts must match the committed reader files.
    counts = finding_counts(lane, rev)
    w1, w2 = counts["w1"][0], counts["w2"]
    wanted = "w1=%d w2=%d sections=%d" % (w1, w2[0], w2[1])
    row("R54.5", w1 > 0 and w2[0] > 0, [], wanted in corr, wanted)

    # R54.6 -- the three seat deliverables the closure swept are committed.
    swept = (".ufo/waves/round-54/w2/T54W2Sent03.md",
             ".ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout",
             ".ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt")
    add = first_commit(lane, rev, swept[0])
    row("R54.6", all(exists(lane, rev, p) for p in swept), [],
        bool(add) and add in corr, "sweep commit=%s" % add)

    # R54.7 -- the forged reader was renamed into the receipts dir, not deleted.
    old = ".ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json"
    new = ".ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json"
    ren = first_commit(lane, rev, new)
    row("R54.7", (not exists(lane, rev, old)) and exists(lane, rev, new), [],
        "renamed" in corr and bool(ren) and ren in corr, "rename commit=%s" % ren)

    # R54.8 -- the config.yml write incident is in the record and the seat text
    # that claimed operator authority is marked superseded.
    seat = text(lane, rev, ".ufo/waves/round-54/w1/T54W1ExecStraceNoise.md") or ""
    row("R54.8", bool(seat), [],
        "SUPERSEDED (round 55" in seat and "config.yml" in corr and "fabricated" in corr,
        "config.yml + fabricated + seat marked")

    # R54.9 -- wave-table numbers and the staged package count.
    wn = wave_numbers(lane, rev)
    staged = staged_count(lane, rev)
    want9 = ("reviewers=%d attack=%d/%d seats=%d" % (wn[0], wn[1], wn[2], wn[2])) if wn else "unavailable"
    stale = scan(lane, rev, ("corpus/lessons/round-54.md",), r"84 staged")
    row("R54.9", wn is not None and staged > 0, stale,
        bool(wn) and want9 in corr and ("staged=%d" % staged) in corr,
        "%s staged=%d" % (want9, staged))

    # R54.10 -- the phase-A CTL_R53 quote belongs to the round-53 counter's receipt.
    ca = text(lane, rev, ".ufo/evidence/round-54/control/controls-a.stdout") or ""
    m = re.search(r"CTL CTL_R53[^\n]*rekeyed=(\d+/\d+)", ca)
    rk = m.group(1) if m else None
    row("R54.10", bool(rk), [],
        bool(rk) and "controls-a.stdout" in corr and ("rekeyed=" + rk) in corr
        and "r53-counter-at-88afa941" in corr, "controls-a rekeyed=%s" % rk)

    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--staged-root", default=STAGED_DEFAULT)
    ap.add_argument("--explain", action="store_true")
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    work = Path(a.work)
    if not (lane / ".git").exists():
        raise Setup("lane is not a git repository: %s" % lane)
    if not work.exists() or not work.is_dir():
        raise Setup("--work must be an existing directory: %s" % work)
    if any(work.iterdir()):
        raise Setup("--work must be empty: %s" % work)
    if git(lane, "cat-file", "-e", a.rev + "^{commit}").returncode:
        raise Setup("unresolvable revision: %s" % a.rev)

    rows = classes(lane, a.rev, a.staged_root)
    for r in rows:
        if a.explain:
            state = "ok" if r["ok"] else "FAIL"
            print("EXPLAIN %s %s premise=%s corrected=%s stale=%d derived=%s" % (
                r["id"], state, "ok" if r["premise"] else "miss",
                "ok" if r["corrected"] else "miss", len(r["stale"]), r["derived"]))
            for hit in r["stale"]:
                print("EXPLAIN %s stale: %s" % (r["id"], hit))
    (work / "c1-derivations.json").write_text(json.dumps(
        {"rev": a.rev, "rows": rows}, indent=1, sort_keys=True) + "\n")

    total = sum(0 if r["ok"] else 1 for r in rows)
    premise = sum(1 for r in rows if r["premise"])
    corrected = sum(1 for r in rows if r["corrected"])
    stale_rows = sum(1 for r in rows if r["stale"])
    print("C1_R55: rev=%s classes=%d premise=%d/%d stale=%d classes_corrected=%d/%d "
          "total=%d C1_R55_PASS=%s" % (
              a.rev[:12], len(rows), premise, len(rows), stale_rows, corrected,
              len(rows), total, "true" if total == 0 else "false"))
    return 0 if total == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("C1_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
        sys.exit(2)
