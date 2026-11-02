#!/usr/bin/env python3
r"""tools/pointer-recheck.py — a record's cited line pointer must still point
at the content the record claims, at the revisions the record names
(round 71; the standing detector for the stale-line-pointer class).

Why: the class is real routed history. The r48 non-author closure routed it
("The lesson Gate cites corpus/SOURCES.md:140-141 for S267 and S268; the rows
are at 142-143", round-48 spotcheck defect 5) and the lesson's own erratum
carries the correction; considerthese 2026-10-28 proposal 5 asked for exactly
this standing sweep ("re-resolve every line or page pointer added in the
window against the current bytes ... and list the drifted ones"); the r16
PROVINCE append's "the seven-leg list now sits at `:85-91`" measures stale at
the r71 base (the ten-leg ledger sits at 88-97). Until now no instrument
measured the class: pointers drifted while the quoted-line, count-recheck,
figure-attribution and anchor-drift instruments covered their neighboring
classes (quotes, printed counts, single figures, page headings).

Mechanism: a manifest row pins (the record bytes at a revision, the exact
cited pointer token as it occurs in the record, the target path at a
revision, the 1-indexed inclusive line span the token cites, and the needle —
the content the record claims the span carries). The span is extracted from
git objects at the pinned revision (never a worktree) with the pointer-recheck
engine of record `git cat-file blob <rev>:<path> | sed -n 'START,ENDp'` —
GNU sed's documented address-range semantics (SOURCES S302: §4.4 Range
Addresses, "An address range matches lines starting from where the first
address matches, and continues until the second address matches (inclusively)";
its §4.3 numeric-address form grounds single-line spans). The stages run as
argv lists (no shell — the r70 mistake-2 discipline). sed is load-bearing:
if it cannot be spawned the run is setup exit 2 (could-not-evaluate), never a
silent fallback. Needles match as UTF-8 bytes of the span bytes; a needle that
stays inside one line is terminator-agnostic (CRLF and LF blobs alike).

Row measurement:
  1. pointer binding — the token must occur in the record bytes at
     record_rev; otherwise the row is an ERROR (unexpected). A row whose
     defect does not exist in the record bytes is refused, not passed (the
     r70 mistake-1 practice one level up).
  2. span — sed prints the span bytes at target_rev; a span past the last
     line prints nothing (measured on this host), which reads as a miss.
  3. verdict — "hit" if the needle occurs in the span bytes, else "miss";
     a row is met when its verdict equals its expect (an expect=miss row is
     the standing red arm: the drift is MEASURED on every sweep, never
     assumed, and stays measured until a superseding record carries the
     correction — the r48/r69/r70 append-only precedent).
Verdict lines:
  POINTER_ROW <id> expect=<e> measured=<m> ok
  POINTER_ROW <id> expect=<e> measured=<m> MISMATCH
  POINTER_ROW <id> expect=<e> measured=- ERROR reason=<r>
  POINTER_RECHECK: rows=N met=M unexpected=U
Exit map: 0 = every row met its expectation; 1 = at least one row
unexpected or errored; 2 = usage, a zero-row manifest (fail-closed: an
empty manifest proves nothing), malformed rows, an unresolvable record or
target revision/path, or a sed that cannot be spawned — all resolved for
ALL rows up front, before any row effect.

Manifest (`tools/pointer-recheck.json`, schema `tameshi-pointer-recheck-v1`):
  rows[]: id, record (repo path), record_rev (40-hex; pin the revision whose
  bytes you verified against, never "tip"), pointer (the exact cited token),
  target (repo path), target_rev (40-hex), start, end (1-indexed inclusive),
  needle, expect ("hit" | "miss"), note.

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only (hash-object / mktree / commit-tree / update-ref;
the index is never touched) and checks seven arms:
  1. hit-met — the needle is in the span: ok, exit 0
  2. miss-met — the fixture's stale-pointer shape, expect=miss (the red arm
     fires): ok
  3. mismatch-caught — expect=hit but the needle is absent: MISMATCH, exit 1
  4. pointer-absent — the pinned token is not in the record bytes: ERROR,
     exit 1
  5. crlf-span — a CRLF blob with a mid-line needle: the span bytes keep
     their carriage returns and the needle still hits (terminator-agnostic
     by construction, measured here)
  6. unresolvable — a record revision absent from the repo: exit 2
  7. vacuous guard — a zero-row manifest: exit 2; missing flags: exit 2
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

REQUIRED = ("id", "record", "record_rev", "pointer", "target", "target_rev",
            "start", "end", "needle", "expect", "note")


def run_git(repo, *args, inp=None, check=True):
    if isinstance(inp, str):
        inp = inp.encode()
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       input=inp)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (
            " ".join(args[:3]),
            r.stderr.decode(errors="replace").strip()[:300]))
    return r


def sed_span(blob_bytes, start, end):
    """Engine of record: sed -n 'START,ENDp' over the blob bytes (S302).

    argv stages only, no shell. sed is load-bearing: a sed that cannot be
    spawned is a setup failure (could-not-evaluate), never a silent fallback.
    A span past the last line prints nothing (measured, disclosed).
    """
    try:
        r = subprocess.run(["sed", "-n", "%d,%dp" % (start, end)],
                           capture_output=True, input=blob_bytes)
    except FileNotFoundError:
        raise RuntimeError("sed-not-spawnable: the pointer-recheck engine of "
                           "record is could-not-evaluate on this host")
    if r.returncode != 0:
        raise RuntimeError("sed exit=%d %s" % (
            r.returncode, r.stderr.decode(errors="replace").strip()[:120]))
    return r.stdout


def sweep(repo, manifest_path, out=sys.stdout):
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    rows = man.get("rows")
    if not rows:
        out.write("POINTER_RECHECK error=empty-manifest rows=0\n")
        return 2
    for row in rows:
        missing = [k for k in REQUIRED if row.get(k) is None]
        if missing:
            raise RuntimeError("row malformed: missing %s" % ",".join(missing))
        if row["expect"] not in ("hit", "miss"):
            raise RuntimeError("row %s expect must be hit|miss" % row["id"])
        for k in ("start", "end"):
            if not isinstance(row[k], int) or isinstance(row[k], bool) \
                    or row[k] < 1:
                raise RuntimeError("row %s %s must be a positive integer"
                                   % (row["id"], k))
        if row["start"] > row["end"]:
            raise RuntimeError("row %s start>end" % row["id"])
    # resolve every record and target blob up front: an unresolvable record
    # or target is setup, exit 2 before any row effect.
    records = {}
    blobs = {}
    for row in rows:
        records[row["id"]] = run_git(
            repo, "show", "%s:%s" % (row["record_rev"], row["record"])
        ).stdout.decode("utf-8", "surrogateescape")
        blobs[row["id"]] = run_git(
            repo, "show", "%s:%s" % (row["target_rev"], row["target"])
        ).stdout
    met = 0
    unexpected = 0
    for row in rows:
        rid = row["id"]
        if row["pointer"] not in records[rid]:
            unexpected += 1
            out.write("POINTER_ROW %s expect=%s measured=- ERROR "
                      "reason=pointer-absent-in-record\n" % (rid, row["expect"]))
            continue
        span = sed_span(blobs[rid], row["start"], row["end"])
        needle = row["needle"].encode("utf-8")
        measured = "hit" if needle in span else "miss"
        ok = (measured == row["expect"])
        if ok:
            met += 1
        else:
            unexpected += 1
        out.write("POINTER_ROW %s expect=%s measured=%s %s\n"
                  % (rid, row["expect"], measured,
                     "ok" if ok else "MISMATCH"))
    out.write("POINTER_RECHECK: rows=%d met=%d unexpected=%d\n"
              % (len(rows), met, unexpected))
    return 1 if unexpected else 0


def _env():
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
    return e


def build_fixture(d):
    """Fixture repo: one commit carrying a record file and two data blobs
    (LF and CRLF). Returns (repo, rev)."""
    fx = os.path.join(d, "fx")
    os.makedirs(fx)
    run_git(fx, "init", "-q", ".")
    for k, v in (("user.email", "fx@fx"), ("user.name", "fx")):
        run_git(fx, "config", k, v)
    lf_data = run_git(fx, "hash-object", "-w", "--stdin",
                      inp="alpha one\nalpha two\nbeta three\ngamma four\n"
                      ).stdout.decode().strip()
    crlf_data = run_git(fx, "hash-object", "-w", "--stdin",
                        inp=b"win line one\r\nwin line two\r\nwin line three\r\n"
                        ).stdout.decode().strip()
    record = run_git(fx, "hash-object", "-w", "--stdin",
                     inp="The audit list sits at data.md:3-4 per the note.\n"
                         "An earlier draft cited data.md:2-2 for the beta line.\n"
                         "The win table sits at win.md:2-2 in the CRLF blob.\n"
                     ).stdout.decode().strip()
    tree = run_git(fx, "mktree",
                   inp="100644 blob %s\tdata.md\n"
                       "100644 blob %s\twin.md\n"
                       "100644 blob %s\trecord.md\n"
                       % (lf_data, crlf_data, record)).stdout.decode().strip()
    r = subprocess.run(["git", "-C", fx, "commit-tree", tree,
                        "-m", "toy pointer audit"], capture_output=True,
                       env=_env(), input=b"x")
    rev = r.stdout.decode().strip()
    run_git(fx, "update-ref", "refs/heads/master", rev)
    return fx, rev


def selftest(out=sys.stdout):
    ok = 0
    total = 7
    d = tempfile.mkdtemp(prefix="pointer-recheck-selftest-")
    try:
        fx, rev = build_fixture(d)

        def manifest(name, rows):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"schema": "tameshi-pointer-recheck-v1",
                           "rows": rows}, f)
            return p

        def row(rid, pointer, start, end, needle, expect, target="data.md",
                trev=None):
            return {"id": rid, "record": "record.md", "record_rev": rev,
                    "pointer": pointer, "target": target,
                    "target_rev": trev or rev, "start": start, "end": end,
                    "needle": needle, "expect": expect, "note": "toy"}

        # arm 1: hit met — the needle is in the span -> ok, exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m1.json", [
            row("P1", "data.md:3-4", 3, 4, "beta three", "hit")]), out=buf)
        if rc == 0 and "POINTER_ROW P1 expect=hit measured=hit ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM1 hit-met: PASS\n")
        else:
            out.write("SELFTEST_ARM1 hit-met: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 2: miss met (red arm fires) — the record's stale draft pointer
        # (line 2 carries "alpha two", not the beta line), expect=miss -> ok
        buf = io.StringIO()
        rc = sweep(fx, manifest("m2.json", [
            row("P2", "data.md:2-2", 2, 2, "beta three", "miss")]), out=buf)
        if rc == 0 and "POINTER_ROW P2 expect=miss measured=miss ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM2 miss-met: PASS\n")
        else:
            out.write("SELFTEST_ARM2 miss-met: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 3: mismatch caught — the same stale pointer, expect=hit
        buf = io.StringIO()
        rc = sweep(fx, manifest("m3.json", [
            row("P3", "data.md:2-2", 2, 2, "beta three", "hit")]), out=buf)
        if rc == 1 and "POINTER_ROW P3 expect=hit measured=miss " \
                "MISMATCH" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM3 mismatch-caught: PASS\n")
        else:
            out.write("SELFTEST_ARM3 mismatch-caught: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 4: pointer absent from the record bytes -> row ERROR, exit 1
        buf = io.StringIO()
        rc = sweep(fx, manifest("m4.json", [
            row("P4", "data.md:9-9", 2, 2, "beta three", "miss")]), out=buf)
        if rc == 1 and "ERROR reason=pointer-absent-in-record" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM4 pointer-absent: PASS\n")
        else:
            out.write("SELFTEST_ARM4 pointer-absent: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 5: CRLF blob, mid-line needle — the span keeps its carriage
        # returns and the needle still hits (terminator-agnostic, measured)
        buf = io.StringIO()
        rc = sweep(fx, manifest("m5.json", [
            row("P5", "win.md:2-2", 2, 2, "line two", "hit",
                target="win.md")]), out=buf)
        if rc == 0 and "POINTER_ROW P5 expect=hit measured=hit ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM5 crlf-span: PASS\n")
        else:
            out.write("SELFTEST_ARM5 crlf-span: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 6: unresolvable record revision -> setup exit 2
        buf = io.StringIO()
        try:
            rc = sweep(fx, manifest("m6.json", [
                row("P6", "data.md:3-4", 3, 4, "beta three", "hit",
                    trev="0" * 40)]), out=buf)
        except RuntimeError:
            rc = 2
        if rc == 2:
            ok += 1
            out.write("SELFTEST_ARM6 unresolvable: PASS\n")
        else:
            out.write("SELFTEST_ARM6 unresolvable: FAIL rc=%r %r\n"
                      % (rc, buf.getvalue()[:200]))
        # arm 7: vacuous manifest exit 2 + usage exit 2
        buf = io.StringIO()
        rc = sweep(fx, manifest("m7.json", []), out=buf)
        arm7a = (rc == 2 and "error=empty-manifest" in buf.getvalue())
        r = subprocess.run([sys.executable, os.path.abspath(__file__)],
                           capture_output=True)
        arm7b = (r.returncode == 2)
        if arm7a and arm7b:
            ok += 1
            out.write("SELFTEST_ARM7 vacuous-usage: PASS\n")
        else:
            out.write("SELFTEST_ARM7 vacuous-usage: FAIL arm7a=%r rc=%r %r "
                      "arm7b_rc=%r\n" % (arm7a, rc, buf.getvalue()[:200],
                                         r.returncode))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    out.write("POINTER_RECHECK_SELFTEST: %d/%d pass\n" % (ok, total))
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
        sys.stderr.write("POINTER_RECHECK error=usage\n")
        return 2
    try:
        return sweep(a.repo, a.manifest)
    except (RuntimeError, subprocess.CalledProcessError) as e:
        sys.stderr.write("POINTER_RECHECK error=setup %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
