#!/usr/bin/env python3
r"""tools/anchor-drift-sweep.py — a held source row's anchor heading must
still be the heading the row's own pinned snapshot carries (round 69; the
standing detector for the r68 closure's routed defect 2: the S299 anchor
cell said "§Directory deletion operations" where the shutil page's — snapshot
and live agree — section heading is "Directory and files operations"; the
drift was caught by the non-author closure reading the page, not by any
standing check).

Why: `corpus/SOURCES.md` anchors locate a quote by exact section heading
(CORPUS.md contract v1); the rows pin committed snapshots precisely because
docs pages drift (the r33/r40/r41 docs-clock lesson) — but nothing checked
that the anchor NAME still matches the snapshot the row pins. A heading
rename on the page silently breaks the anchor's locatability while every
sweep stays green. This checker binds anchor name to snapshot bytes the way
figure-attribution (r68) binds record figure to receipt bytes: a manifest
row pins (the snapshot path at a revision, the exact heading string the row
anchors, expect present|absent) and the row verifies only when the measured
presence matches the expectation. An `expect=absent` row is the standing
red arm: the drift is MEASURED on every sweep, never assumed, and stays
measured until a superseding row carries the corrected heading.

Manifest (`tools/anchor-drift-sweep.json`, schema
`tameshi-anchor-drift-v1`):
  rows[]: id, snapshot (repo path), snapshot_rev (40-hex; pin the revision
  whose bytes you verified against, never "tip"), heading (the exact
  heading string the anchor cell names), expect ("present" | "absent"),
  note (one line naming the row and its history).

Row measurement:
  present — the snapshot's heading set (h1-h6) contains the heading string
            after normalization (HTML entities decoded, tags stripped,
            whitespace runs collapsed, a trailing paragraph mark '¶'
            dropped)
  absent  — it does not
A row is met when measured == expect; unexpected rows name themselves.

Verdict lines:
  ANCHOR_ROW <id> expect=<e> measured=<m> ok
  ANCHOR_ROW <id> expect=<e> measured=<m> MISMATCH
  ANCHOR_DRIFT: rows=N met=M unexpected=U
Exit map: 0 = every row met its expectation; 1 = at least one row
mismatched (the declared red arm reads measured=absent with expect=absent
and is MET — the arm fired, not failed); 2 = usage/setup (an unresolvable
snapshot revision or path, before any row effect) or a manifest with zero
rows (fail-closed: an empty manifest proves nothing).

Snapshot bytes are read from git objects at the pinned revision (never a
worktree). Headings are parsed with html.parser.HTMLParser (SOURCES S300:
the parser "calls handler methods when start tags, end tags, text, comments,
and other markup elements are encountered" — the subclass overrides
handle_starttag/handle_endtag/handle_data to collect h1-h6 text).

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only, commits one toy snapshot with two headings (one
carrying extra whitespace and a trailing paragraph mark), and checks five
arms:
  1. present — expect=present, heading in the snapshot: ok, exit 0
  2. absent-met — expect=absent, heading not in the snapshot: ok
  3. mismatch-caught — expect=present, heading not in the snapshot:
     MISMATCH, exit 1
  4. unresolvable — a snapshot revision absent from the repo: exit 2
  5. vacuous guard — a manifest with zero rows: exit 2, and missing flags:
     exit 2 (usage)
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
REQUIRED = ("id", "snapshot", "snapshot_rev", "heading", "expect", "note")
PARA_MARK = "¶"


def run_git(repo, *args, inp=None, check=True):
    if isinstance(inp, str):
        inp = inp.encode()
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       input=inp)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (
            " ".join(args[:3]),
            r.stderr.decode(errors="replace").strip()[:300]))
    return r.stdout


class HeadingGrabber(HTMLParser):
    """Collect the text of every h1-h6 element (SOURCES S300: subclass
    HTMLParser and override the handler methods). Nested inline tags inside
    a heading contribute their text; an unterminated heading contributes
    nothing (disclosed simplification)."""

    def __init__(self):
        # convert_charrefs=True: entity references arrive as text (S300)
        HTMLParser.__init__(self, convert_charrefs=True)
        self._open = []
        self._buf = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        if tag in HEADING_TAGS:
            self._open.append(tag)
            self._buf.append([])

    def handle_endtag(self, tag):
        if tag in HEADING_TAGS and self._open and self._open[-1] == tag:
            self._open.pop()
            self.headings.append("".join(self._buf.pop()))

    def handle_data(self, data):
        if self._open:
            self._buf[-1].append(data)


def normalize(text):
    t = re.sub(r"\s+", " ", text).strip()
    if t.endswith(PARA_MARK):
        t = t[:-len(PARA_MARK)].rstrip()
    return t


def snapshot_headings(blob):
    p = HeadingGrabber()
    p.feed(blob.decode("utf-8", "replace"))
    p.close()
    return {normalize(h) for h in p.headings if normalize(h)}


def resolve_snapshots(repo, rows):
    """Read every snapshot blob up front; any unresolvable input is setup,
    exit 2 — nothing is certified from an unreadable input."""
    out = {}
    for row in rows:
        key = (row["id"], "snapshot")
        out[key] = run_git(repo, "show", "%s:%s" % (row["snapshot_rev"],
                                                    row["snapshot"]))
    return out


def sweep(repo, manifest_path, out=sys.stdout):
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    rows = man.get("rows")
    if not rows:
        out.write("ANCHOR_DRIFT error=empty-manifest rows=0\n")
        return 2
    for row in rows:
        missing = [k for k in REQUIRED if row.get(k) is None]
        if missing:
            raise RuntimeError("row malformed: missing %s" % ",".join(missing))
    if not all(row.get("expect") in ("present", "absent") for row in rows):
        raise RuntimeError("row expect must be present|absent")
    blobs = resolve_snapshots(repo, rows)
    met = 0
    unexpected = 0
    for row in rows:
        rid = row["id"]
        headings = snapshot_headings(blobs[(rid, "snapshot")])
        heading = normalize(row["heading"])
        measured = "present" if heading in headings else "absent"
        ok = (measured == row["expect"])
        if ok:
            met += 1
        else:
            unexpected += 1
        out.write("ANCHOR_ROW %s expect=%s measured=%s %s\n"
                  % (rid, row["expect"], measured,
                     "ok" if ok else "MISMATCH"))
    out.write("ANCHOR_DRIFT: rows=%d met=%d unexpected=%d\n"
              % (len(rows), met, unexpected))
    return 1 if unexpected else 0


def _env():
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
    return e


TOY_SNAPSHOT = (
    "<html><head><title>toy</title></head><body>\n"
    "<h1>Toy &amp; Page \u00b6</h1>\n"
    "<h2>  Alpha\n  Heading </h2>\n"
    "<p>body text</p>\n"
    "</body></html>\n")


def selftest(out=sys.stdout):
    ok = 0
    total = 5
    d = tempfile.mkdtemp(prefix="anchor-drift-selftest-")
    try:
        fx = os.path.join(d, "fx")
        os.makedirs(fx)
        run_git(fx, "init", "-q", ".")
        for k, v in (("user.email", "fx@fx"), ("user.name", "fx")):
            run_git(fx, "config", k, v)
        blob = run_git(fx, "hash-object", "-w", "--stdin",
                       inp=TOY_SNAPSHOT).decode().strip()
        tree = run_git(fx, "mktree",
                       inp="100644 blob %s\tsnap.html\n" % blob).decode().strip()
        r = subprocess.run(["git", "-C", fx, "commit-tree", tree,
                            "-m", "toy snapshot"],
                           capture_output=True, env=_env(), input=b"x")
        rev = r.stdout.decode().strip()
        run_git(fx, "update-ref", "refs/heads/master", rev)

        def manifest(name, rows):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"schema": "tameshi-anchor-drift-v1", "rows": rows}, f)
            return p

        def row(rid, heading, expect, srev=None):
            return {"id": rid, "snapshot": "snap.html", "snapshot_rev":
                    srev or rev, "heading": heading, "expect": expect,
                    "note": "toy"}

        # arm 1: present expectation met (entity decode + whitespace
        # collapse through the heading) -> exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m1.json", [
            row("A1", "Alpha Heading", "present")]), out=buf)
        if rc == 0 and "ANCHOR_ROW A1 expect=present measured=present ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM1 present: PASS\n")
        else:
            out.write("SELFTEST_ARM1 present: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 2: absent expectation met (the red arm fires) -> exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m2.json", [
            row("A2", "Gamma Missing", "absent")]), out=buf)
        if rc == 0 and "ANCHOR_ROW A2 expect=absent measured=absent ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM2 absent-met: PASS\n")
        else:
            out.write("SELFTEST_ARM2 absent-met: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 3: mismatch caught (expect present, heading not there) -> exit 1
        buf = io.StringIO()
        rc = sweep(fx, manifest("m3.json", [
            row("A3", "Gamma Missing", "present")]), out=buf)
        if rc == 1 and "ANCHOR_ROW A3 expect=present measured=absent " \
                "MISMATCH" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM3 mismatch-caught: PASS\n")
        else:
            out.write("SELFTEST_ARM3 mismatch-caught: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 4: unresolvable snapshot revision -> setup exit 2
        buf = io.StringIO()
        try:
            rc = sweep(fx, manifest("m4.json", [
                row("A4", "Alpha Heading", "present", srev="0" * 40)]),
                out=buf)
        except RuntimeError:
            rc = 2
        if rc == 2:
            ok += 1
            out.write("SELFTEST_ARM4 unresolvable: PASS\n")
        else:
            out.write("SELFTEST_ARM4 unresolvable: FAIL rc=%r %r %r\n"
                      % (rc, buf.getvalue()[:200]))
        # arm 5: vacuous manifest exit 2 + usage exit 2
        buf = io.StringIO()
        rc = sweep(fx, manifest("m5.json", []), out=buf)
        arm5a = (rc == 2 and "error=empty-manifest" in buf.getvalue())
        r = subprocess.run([sys.executable, os.path.abspath(__file__)],
                           capture_output=True)
        arm5b = (r.returncode == 2)
        if arm5a and arm5b:
            ok += 1
            out.write("SELFTEST_ARM5 vacuous-usage: PASS\n")
        else:
            out.write("SELFTEST_ARM5 vacuous-usage: FAIL arm5a=%r rc=%r %r "
                      "arm5b_rc=%r\n" % (arm5a, rc, buf.getvalue()[:200],
                                         r.returncode))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    out.write("ANCHOR_DRIFT_SELFTEST: %d/%d pass\n" % (ok, total))
    return 0 if ok == total else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--manifest")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.repo or not a.manifest:
        ap.print_usage(sys.stderr)
        sys.stderr.write("ANCHOR_DRIFT error=usage\n")
        return 2
    try:
        return sweep(a.repo, a.manifest)
    except (RuntimeError, subprocess.CalledProcessError) as e:
        sys.stderr.write("ANCHOR_DRIFT error=setup %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
