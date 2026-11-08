#!/usr/bin/env python3
"""T91SC1 — probe for the round-91 case-note amendment (read-only on the lane).

Builds a SCRATCH fixture clone of the lane, applies the three amendment edits
exactly as the L1 would, and runs the two FROZEN round-91 counters against the
fixture. Also runs the "before" state (lane HEAD) so the amendment is shown to
be load-bearing. Nothing in the lane repo is written; the fixture is deleted on
exit.

  python3 -I T91SC1-amendment-probe.py

Usage: T91SC1-amendment-probe.py [--keep]
Output: stdout (tee'd by the caller to T91SC1-amendment-probe.out)
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCRATCH = "/fast/scratch/hyaku/tameshi-r91/T91SC1"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
REG = "corpus/SOURCES.md"
R90 = "corpus/lessons/round-90.md"

# --- the amendment, part 1: the replacement `source:` line -------------------
# The frozen counter takes cited = re.findall(r"\bS(\d{3,})\b", src[0]) over the
# SINGLE line that starts with "source:" (len(src) must be 1).  The old line
# cites S316/S317/S001; S318 is appended in the same clause style, before the
# trailing "S001 ... ; fleet ..." clauses.  The quote is the L1's own snapshot
# (.ufo/evidence/round-91/sources/git-env.txt:1413-1415), 18 words.
S318_CLAUSE = (
    "; S318 git(1), `GIT_NO_REPLACE_OBJECTS` (docs, tier A, mined, opened 2026-11-08)"
    " — https://git-scm.com/docs/git,"
    " `.ufo/evidence/round-91/sources/git-env.txt:1413-1415`:"
    " \"Setting and exporting this environment variable tells Git to ignore replacement"
    " refs and do not replace Git objects.\""
    " (grounds the sealed counter's `GIT_NO_REPLACE_OBJECTS=1` read path)"
)

# --- the amendment, part 3 companion: the S318 registry row ------------------
S318_ROW = (
    "| S318 | git(1) — Git Documentation (git-scm.com; Git 2.56.0) — https://git-scm.com/docs/git"
    " | docs | A"
    " | git's own statement that GIT_NO_REPLACE_OBJECTS makes git ignore replacement refs"
    " and not replace Git objects"
    " | ENVIRONMENT VARIABLES, the GIT_NO_REPLACE_OBJECTS entry (tag-stripped snapshot"
    " line 1413-1415) @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 02:04:29 GMT)"
    " | \"Setting and exporting this environment variable tells Git to ignore replacement"
    " refs and do not replace Git objects.\" (18 words) — the sealing ground for the"
    " round-91 counter: with GIT_NO_REPLACE_OBJECTS=1 every git read ignores replacement"
    " refs, so a `git replace` ref cannot swap the bytes a counter reads"
    " | mined | 2026-11-08 | 365d"
    " | corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-91.md |"
)

# Fixture stand-in for corpus/lessons/round-91.md (the L1 writes the real one;
# this exists only so the fixture's used-by path resolves and the gate's E11
# check on the S318 row is exercised honestly).
R91_STUB = """# Round 91 (fixture stand-in — the L1 writes the real lesson)

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S318 git(1), GIT_NO_REPLACE_OBJECTS | admit (A, `mined`) | https://git-scm.com/docs/git, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 02:04:29 GMT` (`.ufo/evidence/round-91/sources/git-env.html`, text `git-env.txt`) | "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." (18 words, `git-env.txt:1413-1415`): the sealing ground for the round-91 counter's `GIT_NO_REPLACE_OBJECTS=1` read path. Cited by the case note. |
"""


def run(argv, cwd=None, env=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def say(*a):
    print(*a)
    sys.stdout.flush()


def git_out(repo, *a):
    rc, out, err = run(["git", "-C", repo] + list(a))
    if rc != 0:
        raise SystemExit("git failed: %s: %s" % (" ".join(a), err.strip()[:200]))
    return out


def note_source_line(text):
    lines = [l for l in text.split("\n") if l.startswith("source:")]
    if len(lines) != 1:
        raise SystemExit("expected exactly one source: line, found %d" % len(lines))
    return lines[0]


def build_fixture(dest):
    """A scratch clone of the lane with the three amendment edits applied."""
    rc, out, err = run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, dest])
    if rc != 0:
        raise SystemExit("clone failed: " + err.strip()[:200])
    top = git_out(dest, "rev-parse", "--show-toplevel").strip()
    if top != os.path.realpath(dest):
        raise SystemExit("toplevel mismatch: %s != %s" % (top, dest))
    git_out(dest, "checkout", "-q", "--detach", "HEAD")

    # (2) the admission-status appendix, byte-for-byte from the frozen fix
    # generator (fixes-v91.py --variant pos) — the L1 lands exactly these bytes.
    rc, out, err = run(["python3", "-I",
                        os.path.join(LANE, ".ufo/evidence/round-91/c2/fixes-v91.py"),
                        "--target", dest])
    if rc != 0:
        raise SystemExit("fixes-v91 failed: " + err.strip()[:200])
    say("  fixes-v91.py --target <fixture>: " + out.strip())

    # (1) the replacement `source:` line — a REPLACEMENT of note line 1, never
    # an addition: the counter reads src[0] only when exactly one line starts
    # with "source:".
    npath = os.path.join(dest, NOTE)
    with open(npath, encoding="utf-8") as f:
        nt = f.read()
    old = note_source_line(nt)
    marker = "; S001 Stryker mutant states"
    if marker not in old:
        raise SystemExit("source: line layout changed; marker not found")
    new = old.replace(marker, S318_CLAUSE + marker, 1)
    if new.count("source:") != 1 or not new.startswith("source:"):
        raise SystemExit("replacement source: line is malformed")
    nt = nt.replace(old, new, 1)
    with open(npath, "w", encoding="utf-8") as f:
        f.write(nt)
    say("  source: line replaced (old %d B -> new %d B); appended marker section present: %s"
        % (len(old), len(new), "## Admission status (appended round 91)" in nt))

    # (3) companion: the S318 registry row in corpus/SOURCES.md.
    rpath = os.path.join(dest, REG)
    with open(rpath, encoding="utf-8") as f:
        src = f.read()
    lines = src.split("\n")
    idx = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| S\d{3}", l))
    lines.insert(idx + 1, S318_ROW)
    with open(rpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    say("  S318 registry row inserted after line %d" % (idx + 1))

    with open(os.path.join(dest, "corpus/lessons/round-91.md"), "w", encoding="utf-8") as f:
        f.write(R91_STUB)

    # commit inside the fixture only
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "ctl"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "ctl@fixture.invalid"
    rc, out, err = run(["git", "-C", dest, "add", "-A"], env=env)
    if rc != 0:
        raise SystemExit("git add failed: " + err.strip()[:200])
    rc, out, err = run(["git", "-C", dest, "commit", "-q", "-m",
                        "fixture: round-91 case-note amendment"], env=env)
    if rc != 0:
        raise SystemExit("git commit failed: " + err.strip()[:200])
    rev = git_out(dest, "rev-parse", "HEAD").strip()
    say("  fixture commit: " + rev)
    return rev


def counter_c1(repo, rev, work):
    cmd = ["python3", "-I", os.path.join(LANE, ".ufo/evidence/round-91/c1/measure-v91.py"),
           "--repo", repo, "--rev", rev, "--work", work]
    rc, out, err = run(cmd)
    return rc, out, err


def counter_c2(repo, rev, work):
    cmd = ["bash", os.path.join(LANE, ".ufo/evidence/round-91/c2/measure-c2-v91.sh"),
           repo, rev, work]
    rc, out, err = run(cmd)
    return rc, out, err


def parse_note_report(note_path):
    """Run the FROZEN parser (measure-v91.py:parse_note) over a note file."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "mv", os.path.join(LANE, ".ufo/evidence/round-91/c1/measure-v91.py"))
    mv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mv)
    with open(note_path, encoding="utf-8") as f:
        nt = f.read()
    rows, amb = mv.parse_note(nt)
    src = [l for l in nt.split("\n") if l.startswith("source:")]
    heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", nt, re.M)
    return rows, amb, src, heads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    os.makedirs(SCRATCH, exist_ok=True)
    work_root = os.path.join(SCRATCH, "probe")
    shutil.rmtree(work_root, ignore_errors=True)
    os.makedirs(work_root)

    say("== replace-ref check (the sealed counters refuse a non-empty replace list) ==")
    for r in (LANE, FLEET):
        rc, out, _ = run(["git", "-C", r, "replace", "-l"])
        say("  %s: git replace -l -> rc=%d out=%r" % (r, rc, out.strip()))

    say("\n== BEFORE: lane HEAD, no amendment ==")
    w = os.path.join(work_root, "before-c1")
    os.makedirs(w)
    rc, out, err = counter_c1(LANE, "HEAD", w)
    say("  exit=%d" % rc)
    for l in out.split("\n"):
        if l.startswith(("C1_SUMMARY", "C1_CONJUNCTS", "C1_R91_PASS", "C1_SETUP")):
            say("  " + l)

    say("\n== fixture: lane + the round-91 amendment ==")
    fx = os.path.join(work_root, "fixture")
    rev = build_fixture(fx)

    rows, amb, src, heads = parse_note_report(os.path.join(fx, NOTE))
    say("  frozen parse_note over the amended note: rows=%d ambiguous=%s" % (len(rows), amb))
    say("  header-named verdict cells: %s" % ", ".join("%s=%s" % (k, rows[k]) for k in sorted(rows)))
    say("  lines starting with 'source:': %d ; measured heads: %s" % (len(src), heads))

    say("\n== AFTER: the sealed counter over the amended fixture ==")
    w = os.path.join(work_root, "after-c1")
    os.makedirs(w)
    rc, out, err = counter_c1(fx, rev, w)
    say("  exit=%d" % rc)
    for l in out.split("\n"):
        if l.startswith(("C1_SUMMARY", "C1_CONJUNCTS", "C1_R91_PASS", "C1_SETUP")):
            say("  " + l)
    if rc not in (0, 1):
        say("  stderr: " + err.strip()[:400])

    say("\n== AFTER: the C2 calibration counter over the amended fixture ==")
    w = os.path.join(work_root, "after-c2")
    os.makedirs(w)
    rc, out, err = counter_c2(fx, rev, w)
    say("  exit=%d" % rc)
    for l in out.split("\n"):
        if l.startswith(("DEFECT_BIND", "C2_SUMMARY", "C2_R91_PASS", "C2_SETUP", "argv=", "toolpin=")):
            say("  " + l)
    if rc not in (0, 1):
        say("  stderr: " + err.strip()[:400])

    say("\n== NEGATIVE CONTROL: a second copy of the verdict table appended to the note ==")
    # The frozen parser marks a repeated id ambiguous (ids=false -> the counter
    # refuses).  A header-named parser therefore reads exactly ONE verdict
    # table per note; the amendment must never append a second one.
    dup = os.path.join(work_root, "dup")
    shutil.copytree(fx, dup, symlinks=True)
    with open(os.path.join(dup, NOTE), encoding="utf-8") as f:
        nt = f.read()
    rows_txt = [l for l in nt.split("\n") if re.match(r"^\|\s*C\d\d\s*\|", l)]
    hdr = [l for l in nt.split("\n") if l.lstrip().startswith("|") and "verdict" in l.lower()][0]
    nt = nt + "\n## Duplicate verdict table (negative control)\n\n" + hdr + "\n" + "\n".join(rows_txt) + "\n"
    with open(os.path.join(dup, NOTE), "w", encoding="utf-8") as f:
        f.write(nt)
    drows, damb, dsrc, dheads = parse_note_report(os.path.join(dup, NOTE))
    say("  frozen parse_note over the duplicated note: rows=%d ambiguous=%s"
        % (len(drows), damb))
    say("  -> ids conjunct would be FALSE (ambiguous ids refuse the state)")

    say("\n== gate check on the amended fixture registry (E/W codes for the S318 row) ==")
    gate = os.path.join(SCRATCH, "gate.sh")
    rc, out, err = run(["bash", gate, "validate", "--today", "2026-11-08",
                         "--file", os.path.join(fx, REG)])
    say("  exit=%d" % rc)
    for l in out.split("\n"):
        if l.strip():
            say("  " + l)

    if not a.keep:
        shutil.rmtree(work_root, ignore_errors=True)
        say("\nscratch fixture removed")
    else:
        say("\nscratch fixture kept at " + work_root)


if __name__ == "__main__":
    main()
