#!/usr/bin/env python3
r"""tools/arm-liveness.py — every declared red arm of a frozen counter must
have a committed input that moves its tally (round 66; adopts the operator's
considerthese 2026-10-28 proposal 2, counter-arm liveness check, scoped to
the receipt-family instruments — the scope and the flip are disclosed in
`tools/arm-liveness.json`).

Why: two landed failures were arms that could never fire on real history —
the r53 rekey arm (`rekey-dir-count=0` at every revision) and the r65 bind
sweep's candidates scope, which read `findings=0` on the genuinely defective
`7d7f9ca8..87e95597` range (r65 lesson mistakes 5; the defect was found by
inspection, not by any standing check). A passing control set did not reveal
either. This checker makes the proposal mechanical: a manifest row PINS one
committed input per arm — instrument bytes at a pinned revision, the input
(range, rev, doc), the tally field, its do-nothing baseline value and the
expected move — and the checker RE-EXECUTES the row: the instrument is
extracted from git objects at the row's pinned revision (never a worktree),
run with `python -I` against the committed input, and the row is ARM_LIVE
only when the exit matches, the parsed tally is >= the row's expect_min AND
strictly greater than the row's baseline (the arm's tally moved). A row whose
input cannot move its arm is ARM_DEAD: the declared red arm is dead.

Manifest (`tools/arm-liveness.json`, schema `tameshi-arm-liveness-v1`):
  rows[]: id, instrument (repo path), instrument_rev (40-hex; the revision
  whose BYTES are run — pin the revision you verified against, not "tip"),
  args (argv tail; the literal `{repo}` is replaced by the lane repo path),
  tally (the summary field name, e.g. `findings`), expect_min (int),
  baseline (int, the do-nothing value), expect_exit (int), arm (one line
  naming the red arm and its committed input).

Verdict lines:
  ARM_LIVE <id> tally=<tally>=<n> exit=<e>
  ARM_DEAD <id> tally=<tally>=<n|unparsed> exit=<e> expect=<field>...
  ARM_LIVENESS: rows=N live=L dead=D
Exit map: 0 = every row live; 1 = at least one row dead; 2 = usage/setup or
a manifest with zero rows (fail-closed: an empty manifest proves nothing).

The standing manifest's three rows are the receipt-family red arms with
real-history committed inputs (the r64 empty-commit discrimination, the
quoted-line records-ahead-of-receipts demonstration, the receipt-exists
records-ahead-of-receipts demonstration at the r64 declaration revision).
Their instrument revisions are pinned at the round-65 tip, so the rows stay
reproducible regardless of later tool edits. The round-66 receipts
demonstrate the dead-arm detector itself: a scratch manifest row pinning the
FROZEN bind tool over the r65 pre-correction range expects findings>=1 and
reads ARM_DEAD (findings=0) — the r65 blind spot, caught mechanically — and
the same row re-pinned to the round-66 tool reads ARM_LIVE.

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only, commits two toy counters (`toy-live.py` prints
`findings=3`, exits 1; `toy-dead.py` prints `findings=0`, exits 0) and checks
four arms:
  1. live — a manifest whose row pins toy-live.py expecting findings>=1
     reads ARM_LIVE, exit 0;
  2. dead — a manifest whose row pins toy-dead.py with the same expectation
     reads ARM_DEAD naming the row, exit 1;
  3. vacuous guard — a manifest with zero rows exits 2;
  4. usage — missing flags exit 2.
"""

import argparse
import json
import os
import re
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


def check_row(repo, row, out):
    if not isinstance(row, dict) or not all(
            row.get(k) is not None for k in ("id", "instrument",
                                             "instrument_rev", "args",
                                             "tally")):
        out.write("ARM_DEAD malformed-row -> no id/instrument/rev/args/tally\n")
        return False
    rid = row["id"]
    blob = run_git(repo, "show", "%s:%s" % (row["instrument_rev"],
                                            row["instrument"]))
    d = tempfile.mkdtemp(prefix="armlive-")
    inst = os.path.join(d, os.path.basename(row["instrument"]))
    with open(inst, "wb") as f:
        f.write(blob)
    argv = [sys.executable, "-I", inst]
    argv += [a.replace("{repo}", str(repo)) for a in row["args"]]
    p = subprocess.run(argv, capture_output=True, cwd=str(repo))
    text = p.stdout.decode(errors="replace")
    m = None
    for m in re.finditer(re.escape(row["tally"]) + r"=(\d+)", text):
        pass
    count = int(m.group(1)) if m else None
    live = (p.returncode == int(row.get("expect_exit", 0))
            and count is not None
            and count >= int(row.get("expect_min", 0))
            and count > int(row.get("baseline", 0)))
    if live:
        out.write("ARM_LIVE %s tally=%s=%d exit=%d\n"
                  % (rid, row["tally"], count, p.returncode))
    else:
        out.write("ARM_DEAD %s tally=%s=%s exit=%d expect=%s>=%s>baseline=%s "
                  "exit=%s\n"
                  % (rid, row["tally"],
                     "unparsed" if count is None else str(count),
                     p.returncode, row["tally"], row.get("expect_min"),
                     row.get("baseline"), row.get("expect_exit")))
    return live


def sweep(repo, manifest_path, out=sys.stdout):
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    rows = man.get("rows")
    if not rows:
        out.write("ARM_LIVENESS error=empty-manifest rows=0\n")
        return 2
    live = 0
    dead = 0
    for row in rows:
        if check_row(repo, row, out):
            live += 1
        else:
            dead += 1
    out.write("ARM_LIVENESS: rows=%d live=%d dead=%d\n"
              % (len(rows), live, dead))
    return 1 if dead else 0


def _env():
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
    return e


TOY_LIVE = ("import sys\n"
            "print('toy summary findings=3')\n"
            "sys.exit(1)\n")
TOY_DEAD = ("import sys\n"
            "print('toy summary findings=0')\n"
            "sys.exit(0)\n")


def selftest(out=sys.stdout):
    ok = 0
    total = 4
    import io
    d = tempfile.mkdtemp(prefix="armlive-selftest-")
    try:
        fx = os.path.join(d, "fx")
        os.makedirs(fx)
        run_git(fx, "init", "-q", ".")
        for k, v in (("user.email", "fx@fx"), ("user.name", "fx")):
            run_git(fx, "config", k, v)
        b1 = run_git(fx, "hash-object", "-w", "--stdin",
                     inp=TOY_LIVE.encode()).decode().strip()
        b2 = run_git(fx, "hash-object", "-w", "--stdin",
                     inp=TOY_DEAD.encode()).decode().strip()
        tree = run_git(fx, "mktree",
                       inp="100644 blob %s\ttoy-live.py\n"
                           "100644 blob %s\ttoy-dead.py\n" % (b1, b2)
                       ).decode().strip()
        env = _env()
        r = subprocess.run(["git", "-C", fx, "commit-tree", tree, "-m", "toys"],
                           capture_output=True, env=env, input=b"x")
        rev = r.stdout.decode().strip()
        run_git(fx, "update-ref", "refs/heads/master", rev)

        def manifest(name, rows):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"schema": "tameshi-arm-liveness-v1",
                           "rows": rows}, f)
            return p

        def row(inst, tid):
            return {"id": tid, "instrument": inst, "instrument_rev": rev,
                    "args": [], "tally": "findings", "expect_min": 1,
                    "baseline": 0, "expect_exit": 1}

        # arm 1: live row -> exit 0
        buf = io.StringIO()
        rc = sweep(fx, manifest("m1.json", [row("toy-live.py", "L1")]),
                   out=buf)
        if rc == 0 and "ARM_LIVE L1" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM1 live-row: PASS\n")
        else:
            out.write("SELFTEST_ARM1 live-row: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 2: dead row -> exit 1, named
        buf = io.StringIO()
        rc = sweep(fx, manifest("m2.json", [row("toy-dead.py", "D1")]),
                   out=buf)
        t = buf.getvalue()
        if rc == 1 and "ARM_DEAD D1" in t:
            ok += 1
            out.write("SELFTEST_ARM2 dead-row: PASS\n")
        else:
            out.write("SELFTEST_ARM2 dead-row: FAIL rc=%r\n%s\n"
                      % (rc, t))
        # arm 3: vacuous manifest -> exit 2
        buf = io.StringIO()
        rc = sweep(fx, manifest("m3.json", []), out=buf)
        if rc == 2 and "error=empty-manifest" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM3 vacuous-guard: PASS\n")
        else:
            out.write("SELFTEST_ARM3 vacuous-guard: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 4: usage — missing flags exit 2
        r = subprocess.run([sys.executable, os.path.abspath(__file__)],
                           capture_output=True)
        if r.returncode == 2:
            ok += 1
            out.write("SELFTEST_ARM4 usage: PASS\n")
        else:
            out.write("SELFTEST_ARM4 usage: FAIL rc=%r\n" % r.returncode)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    out.write("ARM_LIVENESS_SELFTEST: %d/%d pass\n" % (ok, total))
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
        sys.stderr.write("ARM_LIVENESS error=usage "
                         "--repo --manifest required (or --selftest)\n")
        return 2
    try:
        return sweep(str(Path(a.repo).resolve()), a.manifest)
    except (RuntimeError, OSError, ValueError) as e:
        sys.stderr.write("ARM_LIVENESS error=setup %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
