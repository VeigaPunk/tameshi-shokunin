#!/usr/bin/env python3
"""T90R1 defect probe for the frozen C1 counter (measure.py @ 3485ceb0).

Each variant is a scratch clone of the lane (git clone --shared), checked out at the
pre-freeze commit 33dd6e47 (no note), with ONE committed change on top of an honest
fixture (note = derived verdicts, S999 source row, README row), then the frozen counter
is run on that clone at its HEAD. Variants are designed to answer:

  V0-pos         honest fixture                                  -> expect PASS=true (sanity)
  V1-dup-row     extra row for C02 with TWO verdict cells        -> ? (silent skip at measure.py:222-224)
  V2-outside     S999 row only under a non-Registry `## Notes`   -> ? (source scan at measure.py:238-241)
  V3-fence       README row removed; the coverage line sits in a fenced code block -> ? (measure.py:244-245)
  V4-replace     committed note has C02=KILLED (wrong); a local refs/replace swaps the blob for the
                 honest note; run once inheriting env, once with GIT_NO_REPLACE_OBJECTS=1
                                                                   -> ? (measure.py:125-126, 234)

All reads of the lane are from committed objects at A_REV (git show), never the working tree.
Writes: only under --work (scratch). The lane and fleet trees are never written.

Usage: python3 -I probe_defects.py --work EMPTY_DIR --measure /path/to/measure.py
"""
import argparse, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
A_REV = "33dd6e474ec3660f72c3c1e1c30105269807fe12"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
DERIVED = {"C01": "KILLED", "C02": "SURVIVED", "C03": "SURVIVED", "C04": "KILLED", "C05": "KILLED",
           "C06": "SURVIVED", "C07": "KILLED", "C08": "SURVIVED", "C09": "SURVIVED", "C10": "SURVIVED",
           "C11": "KILLED", "C12": "SURVIVED"}


def gi(*a, env=None, cwd=None):
    p = subprocess.run(["git", *a], capture_output=True, text=True, env=env, cwd=cwd)
    if p.returncode != 0:
        raise SystemExit("git failed %s: %s" % (a, p.stderr))
    return p.stdout


def show(path):
    return gi("-C", LANE, "show", "%s:%s" % (A_REV, path))


def note(rows, measured="5/12"):
    out = ["source: S999 fixture row (positive control only)", "", "# fixture note", "",
           "measured: %s killed" % measured, "", "| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in rows.items():
        out.append("| %s | fixture arm | %s | differs |" % (k, v))
    return "\n".join(out) + "\n"


def s999_row():
    return ("| S999 | Fixture — https://fixture.invalid/r90 | docs | B | fixture | §1 | positive-control fixture row "
            "| mined | 2026-11-06 | 90d | %s |" % NOTE)


def pos_sources():
    src = show("corpus/SOURCES.md")
    lines = src.split("\n")
    idx = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| S\d{3}", l))
    lines.insert(idx + 1, s999_row())
    return "\n".join(lines)


def pos_readme():
    return show("corpus/README.md") + "\n| `knowledge/mutation-case-fleet-sources-census.md` | fixture row | S999 |\n"


def run_variant(name, files, post, env_extra, work, measure):
    d = os.path.join(work, "v-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    repo = os.path.join(d, "repo")
    gi("clone", "-q", "--shared", "--no-checkout", LANE, repo)
    top = gi("-C", repo, "rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(repo), "toplevel mismatch %s" % name
    gi("-C", repo, "checkout", "-q", "--detach", A_REV)
    for p, text in files.items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(text)
    gi("-C", repo, "add", "-A")
    gi("-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid", "commit", "-q", "-m", "probe " + name)
    rev = gi("-C", repo, "rev-parse", "HEAD").strip()
    for cmd in post:  # e.g. replace refs, applied inside the scratch clone only
        gi(*[c.replace("{REPO}", repo) for c in cmd])
    wk = os.path.join(d, "work")
    os.makedirs(wk)
    env = dict(os.environ)
    env.update(env_extra)
    p = subprocess.run([sys.executable, "-I", measure, "--repo", repo, "--rev", "HEAD", "--work", wk],
                       capture_output=True, text=True, env=env)
    keep = [l for l in p.stdout.split("\n") if l.startswith(("C1_CONJ", "C1_R90", "C1_SETUP", "C1_SUMMARY"))]
    return name, rev, p.returncode, keep, p.stdout + p.stderr[-400:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--measure", required=True)
    a = ap.parse_args()
    work = os.path.realpath(a.work)
    assert os.path.isdir(work) and not os.listdir(work)
    measure = os.path.realpath(a.measure)

    base_note_rows = dict(DERIVED)
    readme = pos_readme()
    sources = pos_sources()
    variants = []

    variants.append(("V0-pos", {NOTE: note(base_note_rows), "corpus/SOURCES.md": sources, "corpus/README.md": readme}, [], {}))

    dup = note(base_note_rows) + "| C02 | fixture arm | KILLED | SURVIVED |\n"
    variants.append(("V1-dup-row", {NOTE: dup, "corpus/SOURCES.md": sources, "corpus/README.md": readme}, [], {}))

    no_reg = show("corpus/SOURCES.md").rstrip("\n") + "\n\n## Notes\n\n" + s999_row() + "\n"
    variants.append(("V2-outside", {NOTE: note(base_note_rows), "corpus/SOURCES.md": no_reg, "corpus/README.md": readme}, [], {}))

    readme_fence = show("corpus/README.md").rstrip("\n") + "\n\n```\n| `knowledge/mutation-case-fleet-sources-census.md` | in a code fence | S999 |\n```\n"
    variants.append(("V3-fence", {NOTE: note(base_note_rows), "corpus/SOURCES.md": sources, "corpus/README.md": readme_fence}, [], {}))

    wrong_rows = dict(base_note_rows, C02="KILLED")
    variants.append(("V4-replace-env", {NOTE: note(wrong_rows), "corpus/SOURCES.md": sources, "corpus/README.md": readme},
                     "REPLACE", {}))
    variants.append(("V4-replace-sealed", {NOTE: note(wrong_rows), "corpus/SOURCES.md": sources, "corpus/README.md": readme},
                     "REPLACE", {"GIT_NO_REPLACE_OBJECTS": "1"}))

    results = []
    with ThreadPoolExecutor(3) as ex:
        futs = []
        for v in variants:
            name, files, post, env_extra = v
            if post == "REPLACE":
                futs.append(ex.submit(run_replace, name, files, env_extra, work, measure, honest=note(base_note_rows)))
            else:
                futs.append(ex.submit(run_variant, name, files, post, env_extra, work, measure))
        for f in futs:
            results.append(f.result())
    for name, rev, rc, keep, tail in results:
        print("PROBE_VARIANT %s rev=%s exit=%d" % (name, rev, rc))
        for l in keep:
            print("PROBE_LINE %s %s" % (name, l))


def run_replace(name, files, env_extra, work, measure, honest):
    """Commit the wrong note, then make a local replace ref: wrong-note blob -> honest-note blob."""
    d = os.path.join(work, "v-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    repo = os.path.join(d, "repo")
    gi("clone", "-q", "--shared", "--no-checkout", LANE, repo)
    assert os.path.realpath(gi("-C", repo, "rev-parse", "--show-toplevel").strip()) == os.path.realpath(repo)
    gi("-C", repo, "checkout", "-q", "--detach", A_REV)
    for p, text in files.items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(text)
    gi("-C", repo, "add", "-A")
    gi("-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid", "commit", "-q", "-m", "probe " + name)
    rev = gi("-C", repo, "rev-parse", "HEAD").strip()
    wrong_blob = gi("-C", repo, "rev-parse", "HEAD:" + NOTE).strip()
    honest_path = os.path.join(d, "honest-note.md")
    with open(honest_path, "w", encoding="utf-8") as f:
        f.write(honest)
    honest_blob = subprocess.run(["git", "-C", repo, "hash-object", "-w", honest_path],
                                 capture_output=True, text=True, check=True).stdout.strip()
    gi("-C", repo, "replace", wrong_blob, honest_blob)
    wk = os.path.join(d, "work")
    os.makedirs(wk)
    env = dict(os.environ)
    env.update(env_extra)
    p = subprocess.run([sys.executable, "-I", measure, "--repo", repo, "--rev", "HEAD", "--work", wk],
                       capture_output=True, text=True, env=env)
    keep = [l for l in p.stdout.split("\n") if l.startswith(("C1_CONJ", "C1_R90", "C1_SETUP", "C1_SUMMARY"))]
    print("PROBE_REPLACE %s wrong=%s honest=%s replace_list=%s" % (
        name, wrong_blob[:12], honest_blob[:12], gi("-C", repo, "replace", "-l").strip().replace("\n", " ")))
    return name, rev, p.returncode, keep, p.stdout


if __name__ == "__main__":
    main()
