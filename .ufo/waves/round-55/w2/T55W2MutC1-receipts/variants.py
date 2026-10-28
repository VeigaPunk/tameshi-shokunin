#!/usr/bin/env python3
"""T55W2MutC1 phase 2 - drift probes against the frozen C1 stale arms.

Each probe rewrites ONE record token into a plausible drift variant of the same
falsehood (case, spacing, an inserted word) and runs the PRISTINE counter at the
probe revision. A probe that still prints C1_R55_PASS=true is a blind spot in the
frozen counter: the mutant that "survived" there is equivalent to a detector that
already cannot see the defect.

Usage:
  python3 variants.py --lane <lane repo> --rev <C0> --scratch <dir> --receipts <dir>

Clones under --scratch only; writes probes/*.patch, runs/<probe>__M0.stdout and
variants.json under --receipts.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCORECARD = "SCORECARD.md"
LESSONS = "corpus/lessons/round-54.md"
HEADING = "## Round 55 - round-54 record corrections"

# Positive controls: the exact literal the frozen arm searches for, at the same
# insertion point as the matching drift probe. These MUST fail, or the drift
# probes' PASSes say nothing about the arm (the text would simply be unscanned).
CONTROLS = [
    ("K1", "R54.3 exact token", "SCORECARD", "The C2 claim row quotes total=14."),
    ("K2", "R54.1 exact token", "SCORECARD", "The claim row said CTL_POS_c1 true."),
    ("K3", "R54.9 exact token", "LESSONS", "The package counted 84 staged at closure."),
    ("K4", "R54.2 exact token", "SCORECARD", "The freeze pointer fe70474d was quoted."),
    ("K5", "R54.1 exact span", "LESSONS",
     "The positive control prints rekeyed=7/7 on its arm."),
]

PROBES = [
    ("V1", "R54.3 spacing drift", "SCORECARD", "The C2 claim row quotes total = 14."),
    ("V2", "R54.3 case drift", "SCORECARD", "The C2 claim row quotes Total=14."),
    ("V3", "R54.1 tab/space drift", "SCORECARD", "The claim row said CTL_POS_c1  true."),
    ("V4", "R54.9 word insertion", "LESSONS", "The package counted 84 files staged at closure."),
    ("V5", "R54.2 hash case drift", "SCORECARD", "The freeze pointer FE70474D was quoted."),
    ("V6", "R54.1 sentence-start capital", "LESSONS",
     "Positive control prints rekeyed=7/7 on its arm."),
    ("V7", "R54.1 operator spacing", "LESSONS",
     "The positive control requires rekeyed = 7/7 to pass."),
]


def run(cmd, check=False):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("FAILED %s\n%s\n%s" % (" ".join(cmd), r.stdout, r.stderr))
    return r


def git(d, *args, check=False):
    return run(["git", "-C", str(d), *args], check=check)


def assert_toplevel(d):
    top = Path(git(d, "rev-parse", "--show-toplevel", check=True).stdout.strip()).resolve()
    if top != Path(d).resolve():
        raise SystemExit("toplevel %s != probe %s" % (top, d))


def clone_at(lane, dest, rev):
    dest = Path(dest)
    if dest.exists():
        import shutil
        shutil.rmtree(dest)
    run(["git", "clone", "--shared", "--no-checkout", str(lane), str(dest)], check=True)
    git(dest, "checkout", "-f", rev, check=True)
    if git(dest, "rev-parse", "HEAD", check=True).stdout.strip() != rev:
        raise SystemExit("clone head mismatch at %s" % dest)
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--suite", choices=["drift", "control"], default="drift")
    a = ap.parse_args()
    probes = PROBES if a.suite == "drift" else CONTROLS
    lane, rev = Path(a.lane).resolve(), a.rev
    scratch, receipts = Path(a.scratch), Path(a.receipts)
    (receipts / "probes").mkdir(parents=True, exist_ok=True)
    (receipts / "runs").mkdir(parents=True, exist_ok=True)
    counter = receipts / "mutants" / "M0-pristine.py"
    if not counter.exists():
        raise SystemExit("run reproduce.py first: %s missing" % counter)

    out = {}
    for pid, guard, where, text in probes:
        d = clone_at(lane, scratch / ("probe-" + pid), rev)
        p = Path(d) / (SCORECARD if where == "SCORECARD" else LESSONS)
        body = p.read_text()
        if where == "SCORECARD":
            lines = body.splitlines(keepends=True)
            idx = next(i for i, l in enumerate(lines) if l.startswith(HEADING))
            lines.insert(idx, text + "\n\n")
            p.write_text("".join(lines))
        else:
            p.write_text(body + "\n" + text + "\n")
        assert_toplevel(d)
        git(d, "add", "-A", check=True)
        git(d, "-c", "user.name=T55W2MutC1", "-c", "user.email=mut@example.invalid",
            "commit", "-q", "-m", "probe %s: %s" % (pid, guard), check=True)
        prev = git(d, "rev-parse", "HEAD", check=True).stdout.strip()
        (receipts / "probes" / ("%s.patch" % pid)).write_text(git(d, "diff", rev, prev).stdout)
        work = scratch / "work" / ("probe_%s" % pid)
        if work.exists():
            import shutil
            shutil.rmtree(work)
        work.mkdir(parents=True)
        r = run([sys.executable, str(counter), "--lane", str(d), "--rev", prev,
                 "--work", str(work), "--explain"])
        (receipts / "runs" / ("%s__M0.stdout" % pid)).write_text(r.stdout + r.stderr)
        rows = {}
        verdict = None
        for line in r.stdout.splitlines():
            parts = line.split()
            if len(parts) > 2 and parts[0] == "EXPLAIN" and parts[2] in ("ok", "FAIL"):
                rows[parts[1]] = parts[2]
            if line.startswith("C1_R55:"):
                verdict = line
        blind = r.returncode == 0
        out[pid] = {"guard": guard, "text": text, "in": where, "rev": prev,
                    "rc": r.returncode, "verdict": verdict,
                    "failed_rows": [k for k, v in rows.items() if v == "FAIL"],
                    "blind_spot": blind}
        print("%s %-27s in=%-9s rc=%d failed=%s blind_spot=%s" % (
            pid, guard, where, r.returncode, out[pid]["failed_rows"], blind))
    name = "variants.json" if a.suite == "drift" else "variants-control.json"
    (receipts / name).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("blind_spots=%d/%d" % (sum(1 for v in out.values() if v["blind_spot"]), len(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
