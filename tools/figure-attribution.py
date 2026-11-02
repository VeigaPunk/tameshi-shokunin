#!/usr/bin/env python3
r"""tools/figure-attribution.py — a record figure pinned to a named receipt
must live in THAT receipt's committed bytes (round 68; the named successor of
the r67 instrument boundary — the figure-misattribution class,
`corpus/lessons/round-67.md`: the r66 stale selftest cells were byte-backed
only through the rehearsal receipt's preserved pre-correction bytes while the
live receipt named for them reads seven-of-seven).

Why: quoted-line-exists (r65) checks a record's verdict-shaped quotes against
receipts the record cites — set-membership backing. It cannot see
misattribution: a figure that exists somewhere in the cited set but not in the
receipt the record names for it passes the set check (the r66 stale cells
passed every sweep for exactly that reason; the correction needed a human,
SCORECARD R67 correction 1). This checker binds figure to receipt: a manifest
row pins (doc bytes at a revision, the exact figure line, ONE receipt path at
a revision) and the row verifies only when the figure line is a byte
substring of BOTH the doc and the NAMED receipt. A row whose expectation is
`misattributed` is the standing red arm: the figure is in the doc but not in
the named receipt, measured on every sweep, never assumed. The
anywhere-in-cited-set relaxation is the cheat family this instrument refuses
by construction — a set-matcher passes the red pair (the round-68 control
receipt demonstrates it) because the figure IS in the round's other receipt.

Manifest (`tools/figure-attribution.json`, schema
`tameshi-figure-attribution-v1`):
  rows[]: id, doc (repo path), doc_rev (40-hex), figure (the exact line the
  record asserts), receipt (repo path), receipt_rev (40-hex),
  expect ("attributed" | "misattributed"), arm (one line naming the record
  pair and its history).

Row measurement:
  figure-absent   — the doc bytes do not contain the figure (the record does
                    not even say it); never ok for either expectation
  attributed      — the doc contains the figure AND the named receipt's
                    bytes contain it
  misattributed   — the doc contains the figure AND the named receipt's
                    bytes do not
A row is met when measured == expect; unexpected rows name themselves.

Verdict lines:
  FIGURE_ROW <id> expect=<e> measured=<m> ok
  FIGURE_ROW <id> expect=<e> measured=<m> MISMATCH
  FIGURE_ATTRIBUTION: rows=N met=M unexpected=U
Exit map: 0 = every row met its expectation; 1 = at least one row mismatched
(the declared red arm reads measured=misattributed with expect=misattributed
and is MET — the arm fired, not failed); 2 = usage/setup (an unresolvable
doc/receipt revision or path, before any row effect) or a manifest with zero
rows (fail-closed: an empty manifest proves nothing).

Doc and receipt bytes are read from git objects at the pinned revisions
(never a worktree). Unresolvable revisions or paths are setup, exit 2 —
nothing is certified from an unreadable input.

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only, commits two toy docs and two toy receipts, and
checks seven arms:
  1. attributed — expect=attributed, receipt carries the figure: ok, exit 0
  2. misattributed-met — expect=misattributed, receipt lacks it: ok
  3. mismatch-caught — expect=attributed, receipt lacks it: MISMATCH, exit 1
  4. figure-absent — the doc does not contain the figure: MISMATCH
  5. unresolvable — a receipt revision absent from the repo: exit 2
  6. vacuous guard — a manifest with zero rows: exit 2
  7. usage — missing flags: exit 2
"""

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


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


def blob_bytes(repo, rev, path):
    return run_git(repo, "show", "%s:%s" % (rev, path))


REQUIRED = ("id", "doc", "doc_rev", "figure", "receipt", "receipt_rev",
            "expect", "arm")


def resolve_inputs(repo, rows):
    """Read every doc/receipt blob up front; any unresolvable input is
    setup, exit 2 — nothing is certified from an unreadable input."""
    out = {}
    for row in rows:
        rid = row.get("id", "<no-id>")
        for kind, rev, path in (("doc", row.get("doc_rev"), row.get("doc")),
                                ("receipt", row.get("receipt_rev"),
                                 row.get("receipt"))):
            key = (rid, kind)
            if rev is None or path is None:
                raise RuntimeError("row %s: %s revision/path missing" % (rid, kind))
            out[key] = blob_bytes(repo, rev, path)
    return out


def sweep(repo, manifest_path, out=sys.stdout):
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    rows = man.get("rows")
    if not rows:
        out.write("FIGURE_ATTRIBUTION error=empty-manifest rows=0\n")
        return 2
    for row in rows:
        missing = [k for k in REQUIRED if row.get(k) is None]
        if missing:
            raise RuntimeError("row malformed: missing %s" % ",".join(missing))
    if not all(row.get("expect") in ("attributed", "misattributed")
               for row in rows):
        raise RuntimeError("row expect must be attributed|misattributed")
    blobs = resolve_inputs(repo, rows)
    met = 0
    unexpected = 0
    for row in rows:
        rid = row["id"]
        doc = blobs[(rid, "doc")]
        receipt = blobs[(rid, "receipt")]
        figure = row["figure"].encode("utf-8")
        in_doc = figure in doc
        in_receipt = figure in receipt
        if not in_doc:
            measured = "figure-absent"
        elif in_receipt:
            measured = "attributed"
        else:
            measured = "misattributed"
        ok = (measured == row["expect"])
        if ok:
            met += 1
        else:
            unexpected += 1
        out.write("FIGURE_ROW %s expect=%s measured=%s %s\n"
                  % (rid, row["expect"], measured,
                     "ok" if ok else "MISMATCH"))
    out.write("FIGURE_ATTRIBUTION: rows=%d met=%d unexpected=%d\n"
              % (len(rows), met, unexpected))
    return 1 if unexpected else 0


def _env():
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
    return e


TOY_DOC = ("record: the toy suite reads FIGURE_TOY: 4/4 pass\n"
           "and cites the toy receipt\n")
TOY_DOC_NOFIG = ("record: nothing asserted here\n")
TOY_RECEIPT_GOOD = ("FIXTURE: toy control\n"
                    "FIGURE_TOY: 4/4 pass\n")
TOY_RECEIPT_BAD = ("FIXTURE: toy control (other rev)\n"
                   "FIGURE_TOY: 5/5 pass\n")


def selftest(out=sys.stdout):
    ok = 0
    total = 7
    d = tempfile.mkdtemp(prefix="figattr-selftest-")
    this = os.path.abspath(__file__)
    try:
        fx = os.path.join(d, "fx")
        os.makedirs(fx)
        run_git(fx, "init", "-q", ".")
        for k, v in (("user.email", "fx@fx"), ("user.name", "fx")):
            run_git(fx, "config", k, v)
        blobs = {}
        for name, text in (("toy-doc.md", TOY_DOC),
                           ("toy-doc2.md", TOY_DOC_NOFIG),
                           ("toy-receipt-good.txt", TOY_RECEIPT_GOOD),
                           ("toy-receipt-bad.txt", TOY_RECEIPT_BAD)):
            blobs[name] = run_git(fx, "hash-object", "-w", "--stdin",
                                  inp=text.encode()).decode().strip()
        tree = run_git(fx, "mktree", inp="".join(
            "100644 blob %s\t%s\n" % (sha, name)
            for name, sha in sorted(blobs.items()))).decode().strip()
        r = subprocess.run(["git", "-C", fx, "commit-tree", tree, "-m", "toys"],
                           capture_output=True, env=_env(), input=b"x")
        rev = r.stdout.decode().strip()
        run_git(fx, "update-ref", "refs/heads/master", rev)

        def manifest(name, rows):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"schema": "tameshi-figure-attribution-v1",
                           "rows": rows}, f)
            return p

        def row(rid, doc, receipt, expect, figure="FIGURE_TOY: 4/4 pass"):
            return {"id": rid, "doc": doc, "doc_rev": rev,
                    "figure": figure, "receipt": receipt,
                    "receipt_rev": rev, "expect": expect, "arm": "toy"}

        # arm 1: attributed expectation met -> exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m1.json", [
            row("A1", "toy-doc.md", "toy-receipt-good.txt", "attributed")],
        ), out=buf)
        if rc == 0 and "FIGURE_ROW A1 expect=attributed measured=attributed ok" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM1 attributed: PASS\n")
        else:
            out.write("SELFTEST_ARM1 attributed: FAIL rc=%r\n%s\n" % (rc, buf.getvalue()))
        # arm 2: misattributed expectation met (the red arm fires) -> exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m2.json", [
            row("A2", "toy-doc.md", "toy-receipt-bad.txt", "misattributed")],
        ), out=buf)
        if rc == 0 and "FIGURE_ROW A2 expect=misattributed measured=misattributed ok" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM2 misattributed-met: PASS\n")
        else:
            out.write("SELFTEST_ARM2 misattributed-met: FAIL rc=%r\n%s\n" % (rc, buf.getvalue()))
        # arm 3: mismatch caught (expect attributed, receipt lacks it) -> exit 1
        buf = io.StringIO()
        rc = sweep(fx, manifest("m3.json", [
            row("A3", "toy-doc.md", "toy-receipt-bad.txt", "attributed")],
        ), out=buf)
        if rc == 1 and "FIGURE_ROW A3 expect=attributed measured=misattributed MISMATCH" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM3 mismatch-caught: PASS\n")
        else:
            out.write("SELFTEST_ARM3 mismatch-caught: FAIL rc=%r\n%s\n" % (rc, buf.getvalue()))
        # arm 4: figure absent from the doc -> MISMATCH
        buf = io.StringIO()
        rc = sweep(fx, manifest("m4.json", [
            row("A4", "toy-doc2.md", "toy-receipt-good.txt", "attributed")],
        ), out=buf)
        if rc == 1 and "measured=figure-absent MISMATCH" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM4 figure-absent: PASS\n")
        else:
            out.write("SELFTEST_ARM4 figure-absent: FAIL rc=%r\n%s\n" % (rc, buf.getvalue()))
        # arm 5: unresolvable receipt revision -> setup exit 2
        buf = io.StringIO()
        bad_row = row("A5", "toy-doc.md", "toy-receipt-good.txt", "attributed")
        bad_row["receipt_rev"] = "0" * 40
        try:
            rc = sweep(fx, manifest("m5.json", [bad_row]), out=buf)
        except RuntimeError:
            rc = 2
        if rc == 2:
            ok += 1
            out.write("SELFTEST_ARM5 unresolvable: PASS\n")
        else:
            out.write("SELFTEST_ARM5 unresolvable: FAIL rc=%r\n%s\n" % (rc, buf.getvalue()))
        # arm 6: vacuous manifest -> exit 2
        buf = io.StringIO()
        rc = sweep(fx, manifest("m6.json", []), out=buf)
        if rc == 2 and "error=empty-manifest" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM6 vacuous-guard: PASS\n")
        else:
            out.write("SELFTEST_ARM6 vacuous-guard: FAIL rc=%r\n%s\n" % (rc, buf.getvalue()))
        # arm 7: usage — missing flags exit 2
        r = subprocess.run([sys.executable, this],
                           capture_output=True)
        if r.returncode == 2:
            ok += 1
            out.write("SELFTEST_ARM7 usage: PASS\n")
        else:
            out.write("SELFTEST_ARM7 usage: FAIL rc=%r\n" % r.returncode)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    out.write("FIGURE_ATTRIBUTION_SELFTEST: %d/%d pass\n" % (ok, total))
    return 0 if ok == total else 1


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--manifest")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.repo and a.manifest):
        ap.print_usage(sys.stderr)
        sys.stderr.write("FIGURE_ATTRIBUTION error=usage "
                         "--repo --manifest required (or --selftest)\n")
        return 2
    try:
        return sweep(str(Path(a.repo).resolve()), a.manifest)
    except (RuntimeError, OSError, ValueError) as e:
        sys.stderr.write("FIGURE_ATTRIBUTION error=setup %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
