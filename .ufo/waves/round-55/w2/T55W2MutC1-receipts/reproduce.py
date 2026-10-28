#!/usr/bin/env python3
"""T55W2MutC1 - mutation matrix for the round-55 frozen C1 counter (calibration).

Seven single-edit mutants of `.ufo/evidence/round-55/c1/measure.py` at C0, each
scored twice: at C0 itself (does the certified run distinguish the mutant?) and
against a defect fixture that reintroduces the record defect the mutated check
guards (does the mutant let that defect through?).

Usage:
  python3 reproduce.py --lane <lane repo> --rev <C0> --scratch <dir> --receipts <dir>

Clones live under --scratch (git clone --shared, never the lane); every git call
names -C <dir> and each fixture asserts `rev-parse --show-toplevel` == its dir
before committing. Only mutant sources, fixture patches, run stdout and the
matrix are written under --receipts.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEADING = "## Round 55 - round-54 record corrections"
SCORECARD = "SCORECARD.md"
LESSONS = "corpus/lessons/round-54.md"
C2_BEFORE = ".ufo/evidence/round-54/before/c2.stdout"
CONTROLS_B = ".ufo/evidence/round-54/control/controls-b.stdout"
READER_NEW = ".ufo/waves/round-54/w2/T54W2Read99.json"

# ---------------------------------------------------------------- mutants ---
# (id, target guard, old, new). Each old string must occur exactly once at C0.
MUTANTS = [
    (
        "M1",
        "drop the R54.3 stale scan (total=14 no longer searched)",
        '    stale = scan(lane, rev, ("SCORECARD.md",), r"total=14")\n',
        "    stale = []  # MUTANT M1: R54.3 stale scan dropped\n",
    ),
    (
        "M2",
        "replace the R54.3 tree-derived value with the literal total=13",
        '    row("R54.3", n23 is not None, stale, bool(n23) and ("total=%s" % n23) in corr,\n',
        '    row("R54.3", n23 is not None, stale, ("total=13") in corr,\n',
    ),
    (
        "M3",
        "treat premise=false as ok (drop premise from the row verdict)",
        '                     "ok": bool(premise) and not stale and bool(corrected)})\n',
        '                     "ok": not stale and bool(corrected)})  # MUTANT M3: premise ignored\n',
    ),
    (
        "M4",
        "read the corrections section without trimming at the next `## ` heading",
        '        if on and line.startswith("## "):\n            break\n',
        '        if on and False:  # MUTANT M4: no trim at the next heading\n            break\n',
    ),
    (
        "M5",
        "count reader files from the lane working tree instead of git at REV",
        '        r = git(lane, "ls-tree", "-r", "--name-only", rev,\n'
        '                "--", ".ufo/waves/round-54/%s" % wave)\n'
        '        names = [n for n in r.stdout.split()\n'
        '                 if re.search(r"/T54W\\d+[A-Za-z]*Read\\d+\\.json$", n)]\n',
        '        root = Path(lane) / ".ufo" / "waves" / "round-54" / wave\n'
        '        names = [str(p.relative_to(lane)) for p in sorted(root.rglob("*.json"))\n'
        '                 if re.search(r"/T54W\\d+[A-Za-z]*Read\\d+\\.json$",\n'
        '                              "/" + str(p.relative_to(lane)))]\n',
    ),
    (
        "M6",
        "make the span scan case-insensitive (re.IGNORECASE on the whole pattern)",
        '    rx = re.compile(pattern)\n'
        '    hits = []\n'
        '    for path in paths:\n'
        '        body = text(lane, rev, path)\n'
        '        if body is None:\n'
        '            continue\n'
        '        if path == "SCORECARD.md":\n'
        '            body = body.replace(corrections(lane, rev), "")\n'
        '        flat = " ".join(body.split())\n',
        '    rx = re.compile(pattern, re.IGNORECASE)  # MUTANT M6: case-insensitive span\n'
        '    hits = []\n'
        '    for path in paths:\n'
        '        body = text(lane, rev, path)\n'
        '        if body is None:\n'
        '            continue\n'
        '        if path == "SCORECARD.md":\n'
        '            body = body.replace(corrections(lane, rev), "")\n'
        '        flat = " ".join(body.split())\n',
    ),
    (
        "M7",
        "drop the R54.1 span arm, keep the line-scoped scan",
        '    stale += scan_span(lane, rev, RECORD,\n'
        '                       r"positive control.{0,160}rekeyed=7/7|rekeyed=7/7.{0,160}positive control")\n',
        "    # MUTANT M7: span arm dropped (line-scoped scan retained)\n",
    ),
    (
        "M8",
        "drop the R54.1 line-scoped record arm, keep the span arm (expected equivalent)",
        '    stale += scan(lane, rev, ("corpus/QUALITY.md", "corpus/lessons/round-54.md"),\n'
        '                  r"(positive control[^\\n]{0,160}rekeyed=7/7)|(rekeyed=7/7[^\\n]{0,160}positive control)")\n',
        "    # MUTANT M8: R54.1 line-scoped record arm dropped; the span arm remains\n",
    ),
]


# ------------------------------------------------------------------ helpers ---
def run(cmd, cwd=None, check=False):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("FAILED %s\n%s\n%s" % (" ".join(cmd), r.stdout, r.stderr))
    return r


def git(d, *args, check=False):
    return run(["git", "-C", str(d), *args], check=check)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def assert_toplevel(d):
    r = git(d, "rev-parse", "--show-toplevel", check=True)
    top = Path(r.stdout.strip()).resolve()
    if top != Path(d).resolve():
        raise SystemExit("toplevel %s != fixture %s" % (top, d))


def clone_at(lane, dest, rev):
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    run(["git", "clone", "--shared", "--no-checkout", str(lane), str(dest)], check=True)
    git(dest, "checkout", "-f", rev, check=True)
    got = git(dest, "rev-parse", "HEAD", check=True).stdout.strip()
    if got != rev:
        raise SystemExit("clone %s head %s != %s" % (dest, got, rev))
    return dest


def commit_all(d, msg):
    assert_toplevel(d)
    git(d, "add", "-A", check=True)
    git(d, "-c", "user.name=T55W2MutC1", "-c", "user.email=mut@example.invalid",
        "commit", "-q", "-m", msg, check=True)
    return git(d, "rev-parse", "HEAD", check=True).stdout.strip()


def edit(path, old, new, count=1):
    body = Path(path).read_text()
    n = body.count(old)
    if n != count:
        raise SystemExit("%s: anchor occurs %d times (want %d): %r" % (path, n, count, old[:60]))
    Path(path).write_text(body.replace(old, new))


# ---------------------------------------------------------------- fixtures ---
def fixture_d1(d):
    """A stale `total=14` re-enters SCORECARD outside the corrections section."""
    p = Path(d) / SCORECARD
    lines = p.read_text().splitlines(keepends=True)
    idx = next(i for i, l in enumerate(lines) if l.startswith(HEADING))
    lines.insert(idx, "C2 claim row (round-54): total=14\n\n")
    p.write_text("".join(lines))


def fixture_d2(d):
    """The receipt's total moves (13 -> 15): the correction is no longer tree-derived."""
    edit(Path(d) / C2_BEFORE, "total=13 C2_R54_PASS=false", "total=15 C2_R54_PASS=false")


def fixture_d3(d):
    """The phase-B receipt no longer prints CTL_MISMATCH: R54.1's premise dies."""
    edit(Path(d) / CONTROLS_B,
         "CTL_MISMATCH CTL_POS_c1 expected=true actual=false",
         "CTL_MATCH CTL_POS_c1 expected=true actual=true")


def fixture_d4(d):
    """A later `## ` section carries a stale token: the corrections must stop at it."""
    with open(Path(d) / SCORECARD, "a") as fh:
        fh.write("\n## Round 56 - placeholder section (fixture)\n\n"
                 "The C2 claim row quotes total=14.\n")


def fixture_d5(d):
    """A reader file is committed, then removed from the worktree only."""
    p = Path(d) / READER_NEW
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"heading": "fixture", "cand": "0" * 40,
                             "section_sha256": "0" * 64,
                             "findings": [{"quote": "q", "why": "w"}]}) + "\n")
    rev = commit_all(d, "fixture D5: extra committed reader file")
    p.unlink()  # worktree now disagrees with the commit
    return rev


def fixture_d6(d):
    """A capitalised restatement of the R54.1 falsehood (case-only variant)."""
    with open(Path(d) / LESSONS, "a") as fh:
        fh.write("\nPositive Control prints Rekeyed=7/7 on its arm.\n")


def fixture_d7(d):
    """The R54.1 falsehood hard-wrapped across two lines: only the span arm sees it."""
    with open(Path(d) / LESSONS, "a") as fh:
        fh.write("\nThe positive control\nprints rekeyed=7/7 on its arm.\n")


FIXTURES = [
    ("D1", "R54.3 stale scan", "total=14 re-enters SCORECARD outside corrections", fixture_d1),
    ("D2", "R54.3 derivation", "the deciding receipt prints total=15", fixture_d2),
    ("D3", "R54.1 premise", "controls-b.stdout loses CTL_MISMATCH", fixture_d3),
    ("D4", "corrections trim", "a later section carries total=14", fixture_d4),
    ("D5", "R54.5 reader counts", "committed extra reader removed from the worktree", fixture_d5),
    ("D6", "span case", "capitalised Positive Control / Rekeyed=7/7 claim", fixture_d6),
    ("D7", "span arm", "the same falsehood hard-wrapped over two lines", fixture_d7),
]


# -------------------------------------------------------------------- runs ---
def score(counter, lane, rev, work, out_path):
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    r = run([sys.executable, str(counter), "--lane", str(lane), "--rev", rev,
             "--work", str(work), "--explain"])
    out_path.write_text(r.stdout + r.stderr)
    rows = {}
    verdict = None
    for line in r.stdout.splitlines():
        parts = line.split()
        if len(parts) > 2 and parts[0] == "EXPLAIN" and parts[2] in ("ok", "FAIL"):
            rows[parts[1]] = parts[2]
        if line.startswith("C1_R55:"):
            verdict = line
    return {"rc": r.returncode, "rows": rows, "verdict": verdict,
            "stdout": r.stdout, "stderr": r.stderr}


def sig(s):
    return (s["rc"], tuple(sorted(s["rows"].items())))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--receipts", required=True)
    a = ap.parse_args()

    lane = Path(a.lane).resolve()
    rev = a.rev
    scratch = Path(a.scratch)
    receipts = Path(a.receipts)
    (receipts / "mutants").mkdir(parents=True, exist_ok=True)
    (receipts / "fixtures").mkdir(parents=True, exist_ok=True)
    (receipts / "runs").mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)

    src = git(lane, "show", "%s:.ufo/evidence/round-55/c1/measure.py" % rev, check=True).stdout
    pristine = receipts / "mutants" / "M0-pristine.py"
    pristine.write_text(src)
    print("PRISTINE sha256=%s" % sha256_bytes(src.encode()))

    # 1. single-edit mutants
    mut_paths = {}
    for mid, why, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            raise SystemExit("%s: anchor occurs %d times at C0" % (mid, n))
        body = src.replace(old, new)
        p = receipts / "mutants" / ("%s.py" % mid)
        p.write_text(body)
        mut_paths[mid] = p
        print("MUTANT %s sha256=%s bytes_delta=%+d why=%s" % (
            mid, sha256_bytes(body.encode()), len(body.encode()) - len(src.encode()), why))
        run([sys.executable, "-m", "py_compile", str(p)], check=True)

    # 2. pristine clone at C0 + fixtures
    base = clone_at(lane, scratch / "base", rev)
    fixtures = {}
    for fid, guard, desc, fn in FIXTURES:
        d = clone_at(lane, scratch / ("fx-" + fid), rev)
        new_rev = fn(d)
        if new_rev is None:
            new_rev = commit_all(d, "fixture %s: %s" % (fid, desc))
        patch = git(d, "diff", rev, new_rev).stdout
        (receipts / "fixtures" / ("%s.patch" % fid)).write_text(patch)
        fixtures[fid] = (d, new_rev)
        print("FIXTURE %s rev=%s files=%d" % (fid, new_rev[:12], patch.count("diff --git")))

    scenarios = [("C0", base, rev)] + [(fid, fixtures[fid][0], fixtures[fid][1])
                                      for fid, _, _, _ in FIXTURES]
    counters = [("M0", pristine)] + [(mid, mut_paths[mid]) for mid, _, _, _ in MUTANTS]

    # 3. full matrix
    matrix = {}
    for sid, lane_dir, srev in scenarios:
        for cid, cpath in counters:
            key = "%s/%s" % (sid, cid)
            work = scratch / "work" / ("%s_%s" % (sid, cid))
            res = score(cpath, lane_dir, srev, work, receipts / "runs" / ("%s__%s.stdout" % (sid, cid)))
            matrix[key] = res
            print("%-8s %-3s rc=%d %s" % (sid, cid, res["rc"],
                                          res["verdict"] or (res["stderr"].strip().splitlines() or [""])[0]))

    # 4. verdicts
    report = {"rev": rev, "pristine_sha256": sha256_bytes(src.encode()), "mutants": {}, "fixtures": {}}
    matrix_ok = {sid for sid, _, _ in scenarios}
    for mid, why, _, _ in MUTANTS:
        killed_by = []
        target = {"M1": "D1", "M2": "D2", "M3": "D3", "M4": "D4",
                  "M5": "D5", "M6": "D6", "M7": "D7"}.get(mid, "none")
        for sid, _, _ in scenarios:
            if sig(matrix["%s/%s" % (sid, mid)]) != sig(matrix["%s/M0" % sid]):
                killed_by.append(sid)
        at_c0 = "distinguished" if "C0" in killed_by else "equivalent"
        report["mutants"][mid] = {
            "why": why, "target_fixture": target, "at_c0": at_c0,
            "killed_by": killed_by,
            "verdict": "KILLED" if killed_by else "SURVIVED",
            "target_pristine": matrix["%s/M0" % target]["verdict"] if target in matrix_ok else "-",
            "target_mutant": matrix["%s/%s" % (target, mid)]["verdict"] if target in matrix_ok else "-",
        }
        m = report["mutants"][mid]
        print("VERDICT %s %s at_c0=%s killed_by=%s target=%s pristine=[%s] mutant=[%s]" % (
            mid, m["verdict"], at_c0, ",".join(killed_by) or "none", target,
            m["target_pristine"], m["target_mutant"]))
    for sid, guard, desc, _ in [("C0", "certified rev", "no defect", None)] + FIXTURES:
        report["fixtures"][sid] = {
            "guard": guard, "defect": desc,
            "pristine": matrix["%s/M0" % sid]["verdict"],
            "pristine_failed_rows": [k for k, v in matrix["%s/M0" % sid]["rows"].items() if v == "FAIL"],
            "mutants_that_pass": [mid for mid, _, _, _ in MUTANTS
                                  if matrix["%s/%s" % (sid, mid)]["verdict"]
                                  and matrix["%s/%s" % (sid, mid)]["rc"] == 0],
        }
        f = report["fixtures"][sid]
        print("FIXTURE-SCORE %s pristine_failed=%s mutants_that_pass=%s" % (
            sid, f["pristine_failed_rows"], f["mutants_that_pass"]))
    (receipts / "matrix.json").write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print("MATRIX written to %s" % (receipts / "matrix.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
