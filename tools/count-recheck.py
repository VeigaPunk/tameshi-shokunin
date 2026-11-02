#!/usr/bin/env python3
r"""tools/count-recheck.py — a record's printed counting figure must still be
the count its named command produces at the revision the record names
(round 70; the standing detector for the printed-count drift class).

Why: the r69 non-author closure routed three numeric record defects, all the
same class — a figure printed in a correction narrative that the printed
command itself refutes at the revision the same sentence names ("reads 4 at
both the r67 tip and the r68 tip" — measured 0 at both r67-tip candidates;
"20 receipt files" — 19 added; "19 rehearsal receipts" — 18 present). The
fix routed to this round was procedural: re-run the printed command at the
named revision BEFORE printing the count. This checker makes that procedure
standing: a manifest row pins (the record bytes at a revision, the exact
record span that carries the figure, the printed integer, the counting
command of record) and the row verifies only when the measured count matches
the expectation. A `drift` row is the standing red arm: the drift is
MEASURED on every sweep, never assumed, and stays measured until a
superseding record carries corrected figures (append-only, the r69
corrections precedent).

Counting command of record: `git grep -c [-E] <pattern> <rev> -- <path>`
(SOURCES S301: the command's own contract — "Instead of showing every
matched line, show the number of lines that match."). Measured behavior on
this host, disclosed: zero matches print NOTHING and exit 1 — the checker
reads empty stdout with exit 1 as the count 0 (a valid measurement, never an
error); the blob is read from git objects at the named revision (never a
worktree); any other exit or a non-integer count field is a row ERROR.

Manifest (`tools/count-recheck.json`, schema `tameshi-count-recheck-v1`):
  rows[]: id, record (repo path), record_rev (40-hex; pin the revision whose
  bytes you verified against, never "tip"), span (the exact substring of the
  record that carries the figure), printed (the integer the record prints),
  command {rev, path, pattern, regex}, expect ("match" | "drift"), note.

Row measurement:
  1. span binding — the span must be a byte substring of the record at
     record_rev, and the printed integer must occur in the span as a
     delimited decimal token; otherwise the row is an ERROR (unexpected).
  2. count — run the command; parse the integer after the last colon of the
     final stdout line; empty stdout with exit 1 reads 0.
  3. verdict — "match" if measured == printed, else "drift"; a row is met
     when its verdict equals its expect (a drift row with expect=drift is
     the arm firing, not failing).
Verdict lines:
  COUNT_ROW <id> expect=<e> printed=<p> measured=<m> ok
  COUNT_ROW <id> expect=<e> printed=<p> measured=<m> MISMATCH
  COUNT_ROW <id> expect=<e> printed=<p> measured=<m> ERROR reason=<r>
  COUNT_RECHECK: rows=N met=M unexpected=U
Exit map: 0 = every row met its expectation; 1 = at least one row
unexpected or errored; 2 = usage, a zero-row manifest (fail-closed: an
empty manifest proves nothing), or an unresolvable record revision/path —
resolved for ALL rows up front, before any row effect.

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only (hash-object / mktree / commit-tree / update-ref;
the index is never touched) and checks six arms:
  1. match-met — the printed figure equals the recount: ok, exit 0
  2. drift-met — the printed figure differs and expect=drift (the red arm
     fires): ok
  3. mismatch-caught — expect=match but the recount differs: MISMATCH,
     exit 1
  4. span-absent — the pinned span is not in the record bytes: ERROR,
     exit 1
  5. unresolvable — a record revision absent from the repo: exit 2
  6. vacuous guard — a zero-row manifest: exit 2; missing flags: exit 2
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
from pathlib import Path

REQUIRED = ("id", "record", "record_rev", "span", "printed", "command",
            "expect", "note")
CMD_REQUIRED = ("rev", "path", "pattern", "regex")


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


def count_command(repo, cmd):
    """Run the counting command of record; return (count, error)."""
    argv = ["git", "-C", str(repo), "grep", "-c"]
    if cmd.get("regex"):
        argv.append("-E")
    argv += [cmd["pattern"], cmd["rev"], "--", cmd["path"]]
    r = subprocess.run(argv, capture_output=True)
    if r.returncode == 0:
        lines = [l for l in r.stdout.decode("utf-8", "replace").splitlines()
                 if l.strip()]
        if not lines:
            return None, "empty-stdout-exit0"
        last = lines[-1]
        field = last.rsplit(":", 1)[-1].strip()
        if not field.isdigit():
            return None, "count-not-integer:%s" % field[:40]
        return int(field), None
    if r.returncode == 1 and not r.stdout.strip():
        # zero matches: git grep -c prints nothing and exits 1 (measured,
        # disclosed in the module docstring) — the count is 0.
        return 0, None
    return None, "git-grep-exit=%d %s" % (
        r.returncode, r.stderr.decode(errors="replace").strip()[:120])


def sweep(repo, manifest_path, out=sys.stdout):
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    rows = man.get("rows")
    if not rows:
        out.write("COUNT_RECHECK error=empty-manifest rows=0\n")
        return 2
    for row in rows:
        missing = [k for k in REQUIRED if row.get(k) is None]
        if missing:
            raise RuntimeError("row malformed: missing %s" % ",".join(missing))
        cmiss = [k for k in CMD_REQUIRED if row["command"].get(k) is None]
        if cmiss:
            raise RuntimeError("row %s command malformed: missing %s"
                               % (row["id"], ",".join(cmiss)))
    if not all(row.get("expect") in ("match", "drift") for row in rows):
        raise RuntimeError("row expect must be match|drift")
    # resolve every record blob up front: an unresolvable record is setup,
    # exit 2 before any row effect.
    records = {}
    for row in rows:
        records[row["id"]] = run_git(
            repo, "show", "%s:%s" % (row["record_rev"], row["record"])
        ).stdout.decode("utf-8", "surrogateescape")
    met = 0
    unexpected = 0
    for row in rows:
        rid = row["id"]
        text = records[rid]
        span = row["span"]
        printed = row["printed"]
        if span not in text:
            unexpected += 1
            out.write("COUNT_ROW %s expect=%s printed=%s measured=- ERROR "
                      "reason=span-absent\n" % (rid, row["expect"], printed))
            continue
        if not re.search(r"(?<!\d)%d(?!\d)" % printed, span):
            unexpected += 1
            out.write("COUNT_ROW %s expect=%s printed=%s measured=- ERROR "
                      "reason=printed-token-absent-in-span\n"
                      % (rid, row["expect"], printed))
            continue
        measured, err = count_command(repo, row["command"])
        if err is not None:
            unexpected += 1
            out.write("COUNT_ROW %s expect=%s printed=%s measured=- ERROR "
                      "reason=%s\n" % (rid, row["expect"], printed, err))
            continue
        verdict = "match" if measured == printed else "drift"
        ok = (verdict == row["expect"])
        if ok:
            met += 1
        else:
            unexpected += 1
        out.write("COUNT_ROW %s expect=%s printed=%s measured=%d %s\n"
                  % (rid, row["expect"], printed, measured,
                     "ok" if ok else "MISMATCH"))
    out.write("COUNT_RECHECK: rows=%d met=%d unexpected=%d\n"
              % (len(rows), met, unexpected))
    return 1 if unexpected else 0


def _env():
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
    return e


def build_fixture(d):
    """Fixture repo: one commit carrying a record file and a data blob.
    Returns (repo, rev)."""
    fx = os.path.join(d, "fx")
    os.makedirs(fx)
    run_git(fx, "init", "-q", ".")
    for k, v in (("user.email", "fx@fx"), ("user.name", "fx")):
        run_git(fx, "config", k, v)
    data = run_git(fx, "hash-object", "-w", "--stdin",
                   inp="alpha\nbeta\ngamma\n").stdout.decode().strip()
    record = run_git(fx, "hash-object", "-w", "--stdin",
                     inp="The audit found 3 gates committed this round.\n"
                         "An earlier draft said 2 gates committed.\n"
                     ).stdout.decode().strip()
    tree = run_git(fx, "mktree",
                   inp="100644 blob %s\tdata.txt\n"
                       "100644 blob %s\trecord.md\n" % (data, record)
                   ).stdout.decode().strip()
    r = subprocess.run(["git", "-C", fx, "commit-tree", tree,
                        "-m", "toy audit"], capture_output=True,
                       env=_env(), input=b"x")
    rev = r.stdout.decode().strip()
    run_git(fx, "update-ref", "refs/heads/master", rev)
    return fx, rev


def selftest(out=sys.stdout):
    ok = 0
    total = 6
    d = tempfile.mkdtemp(prefix="count-recheck-selftest-")
    try:
        fx, rev = build_fixture(d)

        def manifest(name, rows):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"schema": "tameshi-count-recheck-v1",
                           "rows": rows}, f)
            return p

        def row(rid, span, printed, expect, rrev=None, pattern="gate"):
            return {"id": rid, "record": "record.md", "record_rev":
                    rrev or rev, "span": span, "printed": printed,
                    "command": {"rev": rev, "path": "data.txt",
                                "pattern": pattern, "regex": False},
                    "expect": expect, "note": "toy"}

        # arm 1: match met — the recount equals the printed figure -> exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m1.json", [
            row("C1", "found 3 gates", 3, "match", pattern="a")]), out=buf)
        if rc == 0 and "COUNT_ROW C1 expect=match printed=3 measured=3 ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM1 match-met: PASS\n")
        else:
            out.write("SELFTEST_ARM1 match-met: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 2: drift met (red arm fires) — the record's stale draft figure
        # (printed 2) against the recount 3, expect=drift -> ok, exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m2.json", [
            row("C2", "said 2 gates", 2, "drift", pattern="a")]), out=buf)
        if rc == 0 and "COUNT_ROW C2 expect=drift printed=2 measured=3 ok" \
                in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM2 drift-met: PASS\n")
        else:
            out.write("SELFTEST_ARM2 drift-met: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 3: mismatch caught — the same stale figure, expect=match
        buf = io.StringIO()
        rc = sweep(fx, manifest("m3.json", [
            row("C3", "said 2 gates", 2, "match", pattern="a")]), out=buf)
        if rc == 1 and "COUNT_ROW C3 expect=match printed=2 measured=3 " \
                "MISMATCH" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM3 mismatch-caught: PASS\n")
        else:
            out.write("SELFTEST_ARM3 mismatch-caught: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 4: span absent from the record bytes -> row ERROR, exit 1
        buf = io.StringIO()
        rc = sweep(fx, manifest("m4.json", [
            row("C4", "found 9 gates", 9, "match", pattern="a")]), out=buf)
        if rc == 1 and "ERROR reason=span-absent" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM4 span-absent: PASS\n")
        else:
            out.write("SELFTEST_ARM4 span-absent: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 5: unresolvable record revision -> setup exit 2
        buf = io.StringIO()
        try:
            rc = sweep(fx, manifest("m5.json", [
                row("C5", "found 2 gates", 2, "match", rrev="0" * 40,
                    pattern="a")]), out=buf)
        except RuntimeError:
            rc = 2
        if rc == 2:
            ok += 1
            out.write("SELFTEST_ARM5 unresolvable: PASS\n")
        else:
            out.write("SELFTEST_ARM5 unresolvable: FAIL rc=%r %r\n"
                      % (rc, buf.getvalue()[:200]))
        # arm 6: vacuous manifest exit 2 + usage exit 2
        buf = io.StringIO()
        rc = sweep(fx, manifest("m6.json", []), out=buf)
        arm6a = (rc == 2 and "error=empty-manifest" in buf.getvalue())
        r = subprocess.run([sys.executable, os.path.abspath(__file__)],
                           capture_output=True)
        arm6b = (r.returncode == 2)
        if arm6a and arm6b:
            ok += 1
            out.write("SELFTEST_ARM6 vacuous-usage: PASS\n")
        else:
            out.write("SELFTEST_ARM6 vacuous-usage: FAIL arm6a=%r rc=%r %r "
                      "arm6b_rc=%r\n" % (arm6a, rc, buf.getvalue()[:200],
                                         r.returncode))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    out.write("COUNT_RECHECK_SELFTEST: %d/%d pass\n" % (ok, total))
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
        sys.stderr.write("COUNT_RECHECK error=usage\n")
        return 2
    try:
        return sweep(a.repo, a.manifest)
    except (RuntimeError, subprocess.CalledProcessError) as e:
        sys.stderr.write("COUNT_RECHECK error=setup %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
