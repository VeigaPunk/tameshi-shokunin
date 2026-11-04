#!/usr/bin/env python3
"""tools/additivity-range.py — declared-claim additivity sweep over a commit
range (round 74; closes the round-73 closure's routed defects 1-2).

What it answers: *does a round's append-only / content-preservation claim hold
on EVERY commit of the round's range, not only on the pair of revisions a
receipt happened to ship?* The round-73 range rewrote `LOG.md` CRLF->LF at
`862e8844` and `corpus/QUALITY.md` at `21a7332f`; `tools/additivity-receipt.py`
measures one `(base, tip, file)` pair per call and judges on the CR-normalized
comparison by default, so the `LOG.md` pair prints `raw_old_only=3484` with
`norm_cr_old_only=0` and exits **0** — a receipt that reads clean while the
rewrite is real, and no receipt covers the other commits at all.

Two row kinds, one explicit claim class per row:

  commits   every commit in `range` that changes `file` is measured at
            `first-parent -> commit`; the row holds when no commit violates its
            claim class and names the worst commit otherwise.
  pair      one `base -> tip` measurement (the range-total view a closure
            prints).

Claim classes (the predicate each row declares, not a label chosen after data):

  append-only-raw       judged on `raw_old_only`: no existing line removed or
                        altered on the committed bytes. A CRLF rewrite is a
                        violation here even when the content is identical.
  append-only-content   judged on `norm_cr_old_only` (CRLF/CR -> LF first): the
                        weaker "content preserved" claim, which by construction
                        cannot see a line-ending rewrite.

`expect: hold|violated` per row, so a standing red row MEASURES the mismatch on
every sweep instead of assuming it away (the wave-reconcile precedent).

Binding rules:

  * bytes come from git objects (`git cat-file blob <rev>:<path>`), never from
    a worktree; an absent base blob means the file was added (nothing removed,
    `hold`), an absent tip blob means deleted (`violated` with every line
    counted);
  * `verbatim_prefix` (CR-stripped, empty-dropped base content is a prefix of
    the tip content) is printed for every row but not judged;
  * a zero-row manifest, an unresolvable revision, an unknown claim class or an
    unknown row kind is a setup refusal (exit 2) before any row effect;
  * `TMPDIR`, when set, is the scratch root: set-but-unusable is
    could-not-evaluate exit 2, never a silent `/tmp` fallback (the round-53
    scratch-root contract).

Exit: 0 every row measured its expected status; 1 at least one did not; 2 setup.

Usage:

  python3 -I tools/additivity-range.py --selftest
  python3 -I tools/additivity-range.py --repo . --manifest tools/additivity-range.json
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCHEMA = "tameshi-additivity-range-v1"
ROW_SCHEMA = "tameshi-additivity-range-row-v1"
CLAIMS = ("append-only-raw", "append-only-content")
KINDS = ("commits", "pair")
REV_RE = re.compile(r"[0-9a-f]{6,40}")


class SetupError(Exception):
    pass


def die(msg):
    raise SetupError(msg)


def scrub_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=scrub_env())
    if proc.returncode != 0:
        die("git-%s:%s" % (args[0],
                           proc.stderr.decode("utf-8", "replace").strip()[:200]))
    return proc.stdout


def rev_ok(repo, rev):
    if not isinstance(rev, str) or not REV_RE.fullmatch(rev):
        die("rev-unresolvable:%r" % (rev,))
    try:
        git(repo, "rev-parse", "--verify", "%s^{commit}" % rev)
    except SetupError:
        die("rev-unresolvable:%s" % rev)
    return rev


def blob(repo, rev, path):
    """Committed bytes, or None when the path does not exist at that rev."""
    proc = subprocess.run(["git", "-C", repo, "cat-file", "-e",
                           "%s:%s" % (rev, path)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=scrub_env())
    if proc.returncode != 0:
        return None
    return git(repo, "cat-file", "blob", "%s:%s" % (rev, path))


def line_set(raw, strip_cr):
    if strip_cr:
        raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return set(raw.split(b"\n")) - {b""}


def content_lines(raw):
    lines = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n").split(b"\n")
    return [l for l in lines if l != b""]


def prefix_ok(old_raw, new_raw):
    old, new = content_lines(old_raw), content_lines(new_raw)
    return len(old) <= len(new) and new[:len(old)] == old


def measure(repo, base, tip, path):
    old_raw, new_raw = blob(repo, base, path), blob(repo, tip, path)
    out = {"base": base[:12], "tip": tip[:12], "path": path}
    if old_raw is None and new_raw is None:
        out.update(added=True, removed=False, base_sha256=None, tip_sha256=None,
                   raw_old_only=0, raw_new_only=0, norm_cr_old_only=0,
                   norm_cr_new_only=0, verbatim_prefix=True,
                   eol_rewrite_disclosed=False)
        return out
    if old_raw is None:                     # added: nothing removed
        out.update(added=True, removed=False)
        old_raw = b""
    else:
        out.update(added=False)
    if new_raw is None:                     # deleted: every line removed
        out.update(removed=True)
        new_raw = b""
    else:
        out.update(removed=False)
    out["base_sha256"] = hashlib.sha256(old_raw).hexdigest()
    out["tip_sha256"] = hashlib.sha256(new_raw).hexdigest()
    for name, strip in (("raw", False), ("norm_cr", True)):
        o, n = line_set(old_raw, strip), line_set(new_raw, strip)
        out[name + "_old_only"] = len(o - n)
        out[name + "_new_only"] = len(n - o)
    out["verbatim_prefix"] = prefix_ok(old_raw, new_raw)
    out["eol_rewrite_disclosed"] = (
        out["raw_old_only"] != out["norm_cr_old_only"]
        or out["raw_new_only"] != out["norm_cr_new_only"])
    return out


def judged(m, claim):
    if claim == "append-only-raw":
        return m["raw_old_only"]
    if claim == "append-only-content":
        return m["norm_cr_old_only"]
    die("claim-unknown:%s" % (claim,))


def first_parent(repo, rev):
    raw = git(repo, "rev-list", "--parents", "-n", "1", rev).decode().split()
    if len(raw) < 2:
        die("root-commit-has-no-parent:%s" % rev)
    return raw[1]


def changed(repo, parent, rev, path):
    """True when the file's blob differs between parent and rev."""
    def at(r):
        p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify",
                            "--quiet", "%s:%s" % (r, path)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=scrub_env())
        return p.stdout.strip() if p.returncode == 0 else b""
    return at(parent) != at(rev)


def walk_commits(repo, base, tip, path):
    out = []
    revs = git(repo, "rev-list", "--reverse", "--first-parent",
               "%s..%s" % (base, tip)).decode().split()
    for rev in revs:
        parent = first_parent(repo, rev)
        if not changed(repo, parent, rev, path):
            continue
        m = measure(repo, parent, rev, path)
        m["commit"] = rev[:12]
        out.append(m)
    return revs, out


def row_measure(repo, row):  # returns (measured, worst_measurement, walked)
    path = row.get("file")
    if not isinstance(path, str) or not path:
        die("row-file-absent:%s" % (row.get("id"),))
    kind, claim = row.get("kind"), row.get("claim")
    if kind not in KINDS:
        die("row-kind-unknown:%s" % (row.get("id"),))
    if claim not in CLAIMS:
        die("row-claim-unknown:%s" % (row.get("id"),))
    if kind == "pair":
        base = rev_ok(repo, row.get("base"))
        tip = rev_ok(repo, row.get("tip"))
        m = measure(repo, base, tip, path)
        m["commit"] = tip[:12]
        measured = "violated" if judged(m, claim) > 0 else "hold"
        return measured, m, 1
    rng = row.get("range")
    if (not isinstance(rng, list) or len(rng) != 2):
        die("row-range-malformed:%s" % (row.get("id"),))
    base = rev_ok(repo, rng[0])
    tip = rev_ok(repo, rng[1])
    revs, rows = walk_commits(repo, base, tip, path)
    if not revs:
        die("range-empty:%s" % (row.get("id"),))
    worst = None
    for m in rows:
        if judged(m, claim) > 0 and (worst is None
                                     or judged(m, claim) > judged(worst, claim)):
            worst = m
    measured = "violated" if worst is not None else "hold"
    return measured, (worst or (rows[-1] if rows else None)), len(rows)


def detail_of(measured, m, n_walked, n_changed):
    if m is None:
        return "walked=%d changed=0 (file untouched in range)" % n_walked
    return ("walked=%d changed=%d worst=%s raw_old_only=%d raw_new_only=%d "
            "norm_cr_old_only=%d norm_cr_new_only=%d verbatim_prefix=%s "
            "eol_rewrite_disclosed=%s removed=%s"
            % (n_walked, n_changed, m.get("commit"), m["raw_old_only"],
               m["raw_new_only"], m["norm_cr_old_only"],
               m["norm_cr_new_only"], str(m["verbatim_prefix"]).lower(),
               str(m["eol_rewrite_disclosed"]).lower(), str(m["removed"]).lower()))


def sweep(manifest, repo, quiet=False):
    rows = manifest.get("rows") if isinstance(manifest, dict) else None
    if not isinstance(rows, list) or not rows:
        die("zero-rows")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            die("row-malformed")
        if row["id"] in seen:
            die("row-id-duplicate:%s" % row["id"])
        seen.add(row["id"])
        if row.get("expect") not in ("hold", "violated"):
            die("row-expect-invalid:%s" % row["id"])
        if row.get("kind") not in KINDS:
            die("row-kind-unknown:%s" % row["id"])
        if row.get("claim") not in CLAIMS:
            die("row-claim-unknown:%s" % row["id"])
    out, unexpected = [], 0
    for row in rows:
        measured, m, n = row_measure(repo, row)
        ok = measured == row["expect"]
        if not ok:
            unexpected += 1
        out.append({"id": row["id"], "file": row["file"], "kind": row["kind"],
                    "claim": row["claim"], "expect": row["expect"],
                    "measured": measured, "ok": ok,
                    "detail": detail_of(measured, m, n, n),
                    "raw_old_only": (m or {}).get("raw_old_only", 0),
                    "norm_cr_old_only": (m or {}).get("norm_cr_old_only", 0)})
        if not quiet:
            print("ADDRANGE_ROW %s file=%s kind=%s claim=%s expect=%s "
                  "measured=%s %s | %s"
                  % (row["id"], row["file"], row["kind"], row["claim"],
                     row["expect"], measured, "ok" if ok else "MISMATCH",
                     out[-1]["detail"]))
    met = len(out) - unexpected
    if not quiet:
        print("ADDRANGE: rows=%d met=%d unexpected=%d"
              % (len(out), met, unexpected))
        # derived populations beside the tally: a stub that echoes each row's
        # `expect` cannot print sums it never measured (the r73 S07 carry).
        print("ADDRANGE_TOTALS raw_old_only=%d norm_cr_old_only=%d"
              % (sum(r["raw_old_only"] for r in out),
                 sum(r["norm_cr_old_only"] for r in out)))
    return out, unexpected


# --- selftest -------------------------------------------------------------
def scratch_root():
    tmp = os.environ.get("TMPDIR")
    if tmp:
        if not os.path.isdir(tmp):
            print("additivity-range: could-not-evaluate: cannot create clone "
                  "scratch under the scratch root: TMPDIR is not a usable "
                  "directory: '%s' (could-not-evaluate)" % tmp, file=sys.stderr)
            raise SystemExit(2)
        return tempfile.mkdtemp(prefix="additivity-range-selftest-", dir=tmp)
    return tempfile.mkdtemp(prefix="additivity-range-selftest-")


def selftest():
    work = scratch_root()
    env = scrub_env()
    env.update(GIT_AUTHOR_NAME="selftest", GIT_COMMITTER_NAME="selftest",
               GIT_AUTHOR_EMAIL="selftest@local",
               GIT_COMMITTER_EMAIL="selftest@local")
    results = []

    def arm(name, want_exit, fn):
        try:
            got_exit, lines = fn()
        except SetupError:
            got_exit, lines = 2, []
        ok = got_exit == want_exit
        results.append((name, ok, got_exit, want_exit, lines[:1]))

    try:
        subprocess.run(["git", "init", "-q", work], capture_output=True, env=env)
        top = subprocess.run(["git", "-C", work, "rev-parse", "--show-toplevel"],
                             capture_output=True).stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(work):
            die("fixture-top-level-mismatch")

        def commit(msg):
            subprocess.run(["git", "-C", work, "add", "-A"], capture_output=True,
                           env=env)
            subprocess.run(["git", "-C", work, "commit", "-q", "-m", msg],
                           capture_output=True, env=env)
            return subprocess.run(["git", "-C", work, "rev-parse", "HEAD"],
                                  capture_output=True).stdout.decode().strip()

        path = os.path.join(work, "REC.md")
        body = ("\r\n".join("line-%02d" % i for i in range(1, 21)) + "\r\n")
        with open(path, "wb") as fh:
            fh.write(body.encode("ascii"))
        base = commit("base: 20 CRLF lines")
        with open(path, "ab") as fh:
            fh.write(b"appended-a\r\nappended-b\r\n")
        clean = commit("clean append")
        # the r73 defect shape: existing LF lines rewritten to CRLF, then append
        subprocess.run(["git", "-C", work, "reset", "-q", "--hard", base],
                       capture_output=True, env=env)
        raw = open(path, "rb").read()
        parts = raw.split(b"\r\n")
        rewritten = (b"\n".join(parts[:10]) + b"\n" + b"\r\n".join(parts[10:])
                     + b"appended-c\r\n")
        with open(path, "wb") as fh:
            fh.write(rewritten)
        rewrite = commit("append with LF->CRLF rewrite of the tail")

        def run(rows):
            return sweep({"rows": rows}, work, quiet=True)

        def row(**kw):
            base_row = {"id": "fixture-row", "file": "REC.md",
                        "kind": "commits", "claim": "append-only-raw",
                        "expect": "hold", "range": [base, clean]}
            base_row.update(kw)
            return base_row

        def pair(claim, base_rev, tip_rev, expect):
            return {"id": "fixture-pair", "file": "REC.md", "kind": "pair",
                    "claim": claim, "expect": expect, "base": base_rev,
                    "tip": tip_rev}

        def exit_of(fn):
            try:
                out, unexpected = fn()
                return (0 if unexpected == 0 else 1), out
            except SetupError as exc:
                return 2, [str(exc)]

        arm("arm1-clean-append-holds", 0,
            lambda: exit_of(lambda: run([row(range=[base, clean])])))
        arm("arm2-eol-rewrite-violates-raw", 0,
            lambda: exit_of(lambda: run([row(range=[base, rewrite],
                                              expect="violated")])))
        arm("arm3-content-class-cannot-see-rewrite", 0,
            lambda: exit_of(lambda: run([row(range=[base, rewrite],
                                              claim="append-only-content",
                                              expect="hold")])))
        arm("arm4-flipped-expect-measures-mismatch", 1,
            lambda: exit_of(lambda: run([row(range=[base, rewrite],
                                              expect="hold")])))
        arm("arm5-pair-kind-range-total", 0,
            lambda: exit_of(lambda: run([pair("append-only-raw", base,
                                              rewrite, "violated")])))
        arm("arm6-zero-rows-refused", 2,
            lambda: exit_of(lambda: run([])))
        arm("arm7-unresolvable-rev-refused", 2,
            lambda: exit_of(lambda: run([row(range=["f" * 40, clean])])))
        arm("arm8-unknown-claim-refused", 2,
            lambda: exit_of(lambda: run([row(claim="append-only-vibes")])))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    passed = 0
    for name, ok, got, want, sample in results:
        print("SELFTEST %-42s %s (got=%s want=%s)%s"
              % (name, "ok" if ok else "FAIL", got, want,
                 (" | " + sample) if (not ok and sample) else ""))
        if ok:
            passed += 1
    print("ADDITIVITY_RANGE_SELFTEST: %d/%d pass" % (passed, len(results)))
    return 0 if passed == len(results) == 8 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".")
    ap.add_argument("--manifest", default="tools/additivity-range.json")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        try:
            return selftest()
        except SetupError as exc:
            print("ADDITIVITY_RANGE error=selftest-setup:%s" % exc,
                  file=sys.stderr)
            return 2
    try:
        try:
            with open(a.manifest, "rb") as fh:
                manifest = json.loads(fh.read().decode("utf-8"))
        except OSError as exc:
            die("manifest-unreadable:%s:%s" % (a.manifest, exc))
        except ValueError as exc:
            die("manifest-unparsable:%s:%s" % (a.manifest, exc))
        rows, unexpected = sweep(manifest, a.repo)
        if a.json_out:
            with open(a.json_out, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"schema": SCHEMA, "rows": rows,
                                     "unexpected": unexpected},
                                    indent=1, ensure_ascii=True) + "\n")
        return 0 if unexpected == 0 else 1
    except SetupError as exc:
        print("ADDITIVITY_RANGE error=setup:%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
