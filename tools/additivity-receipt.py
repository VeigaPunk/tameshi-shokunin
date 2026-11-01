#!/usr/bin/env python3
"""tools/additivity-receipt.py — append-only receipts on committed bytes with
the normalization declared (round 63; closes the r62 routed defect RD5).

The r62 report claimed "LOG.md 0 lines removed (comm -23 -> 0)" while the same
command on the raw committed bytes measures 80 (LOG.md) and 30 (SCORECARD.md):
the work commit rewrote the r61 tail blocks LF->CRLF, and the receipt did not
state any normalization. This instrument is the convention of record:

  1. Receipts are computed on COMMITTED BYTES (git cat-file at pinned revs),
     never on worktree bytes.
  2. Every receipt prints BOTH the raw comparison and the CR-normalized
     comparison, so a line-ending rewrite is disclosed by the receipt itself
     (raw > normalized = a rewrite happened) instead of being silently
     absorbed into a "0".
  3. The verbatim-prefix property (CR-stripped, empty-dropped base content is
     a byte-verbatim prefix of the tip) is checked and printed.
  4. Append-only discipline is judged on the NORMALIZED comparison; a run
     requiring raw additivity too passes --require-raw.

Exit codes: 0 = append-only holds at the judged level; 1 = content lines
removed or altered (append-only violated); 2 = usage/setup error.

Selftest (``--selftest``) builds a throwaway git repo in the system temp dir
and exercises five arms; every arm names the input that moves its outcome:

  ARM-CLEAN-APPEND    append lines to a CRLF file, no rewrite of existing
                      bytes            -> raw=0 norm=0 prefix=true exit 0
  ARM-EOL-REWRITE     the r62 defect shape: append and rewrite the tail
                      blocks LF->CRLF  -> raw>0 norm=0 prefix=true exit 0,
                                          rewrite disclosed (raw != norm)
  ARM-REQUIRE-RAW     the same bytes under --require-raw -> exit 1
  ARM-ALTER           change an existing line's content -> norm>0 exit 1
  ARM-DELETE          delete an existing line            -> norm>0 exit 1
"""
import argparse
import hashlib
import os
import subprocess
import sys
import tempfile

SCHEMA = "tameshi-additivity-receipt-v1"


def die(msg, code=2):
    print("ADDITIVITY-RECEIPT error=%s" % msg, file=sys.stderr)
    sys.exit(code)


def git(repo, *args, inp=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    r = subprocess.run(["git", "-C", str(repo), *args], input=inp,
                       capture_output=True, env=env)
    if r.returncode != 0:
        die("git-%s: %s" % (args[0], r.stderr.decode(errors="replace")[:200]))
    return r.stdout


def blob_bytes(repo, rev, path):
    """Committed bytes at <rev>:<path> via one plumbing read (S294, S289:
    blob bytes are what the commit stores; no eol/text attribute layer is
    applied by cat-file)."""
    return git(repo, "cat-file", "blob", "%s:%s" % (rev, path))


def line_set(raw, strip_cr):
    if strip_cr:
        raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return set(raw.split(b"\n")) - {b""}


def prefix_ok(old_raw, new_raw):
    """CR-stripped, empty-dropped base content is a verbatim prefix of the
    tip's CR-stripped, empty-dropped content: every pre-existing content line
    survives in order (an inserted blank line is an addition, not an
    alteration — r62 inserted one into LOG.md)."""
    def content(raw):
        lines = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n").split(b"\n")
        return [l for l in lines if l != b""]
    old, new = content(old_raw), content(new_raw)
    return len(old) <= len(new) and new[:len(old)] == old


def measure(repo, base, tip, path):
    old_raw = blob_bytes(repo, base, path)
    new_raw = blob_bytes(repo, tip, path)
    out = {"schema": SCHEMA, "file": path, "base": base[:12], "tip": tip[:12]}
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


def verdict_line(m):
    return ("ADDITIVITY file=%s base=%s tip=%s raw_old_only=%d raw_new_only=%d "
            "norm_cr_old_only=%d norm_cr_new_only=%d verbatim_prefix=%s "
            "eol_rewrite_disclosed=%s") % (
        m["file"], m["base"], m["tip"], m["raw_old_only"], m["raw_new_only"],
        m["norm_cr_old_only"], m["norm_cr_new_only"],
        str(m["verbatim_prefix"]).lower(),
        str(m["eol_rewrite_disclosed"]).lower())


def judge(m, require_raw):
    """Append-only is judged on the normalized comparison; --require-raw
    additionally demands the raw comparison be clean (no rewrite absorbed)."""
    judged = m["norm_cr_old_only"] if not require_raw else m["norm_cr_old_only"] + m["raw_old_only"]
    ok = judged == 0
    return ok, ("append-only-content" if not require_raw
                else "append-only-raw")


def run_arm(name, expect_exit, repo, base, tip, path, require_raw=False):
    m = measure(repo, base, tip, path)
    ok, mode = judge(m, require_raw)
    exit_code = 0 if ok else 1
    line = verdict_line(m)
    print(line)
    passed = exit_code == expect_exit
    print("ARM-%s exit=%d expected=%d %s" % (
        name, exit_code, expect_exit,
        "PASS" if passed else "FAIL"))
    return passed, line


def selftest():
    tmp = tempfile.mkdtemp(prefix="tameshi-additivity-")
    r = subprocess.run(["git", "init", "-q", tmp], capture_output=True)
    if r.returncode != 0:
        die("git-init: %s" % r.stderr.decode(errors="replace")[:200])
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "selftest"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "selftest@local"

    def commit_all(msg):
        subprocess.run(["git", "-C", tmp, "add", "-A"], capture_output=True, env=env)
        r = subprocess.run(["git", "-C", tmp, "commit", "-q", "-m", msg],
                           capture_output=True, env=env)
        if r.returncode != 0:
            die("commit: %s" % r.stderr.decode(errors="replace")[:200])
        return subprocess.run(["git", "-C", tmp, "rev-parse", "HEAD"],
                              capture_output=True).stdout.decode().strip()

    body = "\r\n".join("line-%02d" % i for i in range(1, 21)) + "\r\n"
    p = os.path.join(tmp, "REC.md")
    with open(p, "wb") as f:
        f.write(body.encode("ascii"))
    subprocess.run(["git", "-C", tmp, "add", "REC.md"], capture_output=True, env=env)
    base = commit_all("base: CRLF record file")

    # ARM-ALTER: change an existing line's content (red under every mode).
    with open(p, "wb") as f:
        f.write(body.replace("line-07", "line-SEVEN-ALTERED").encode("ascii"))
    altered = commit_all("alter one line")
    # ARM-DELETE: drop an existing line (red).
    subprocess.run(["git", "-C", tmp, "reset", "-q", "--hard", base],
                   capture_output=True, env=env)
    with open(p, "wb") as f:
        f.write(body.replace("line-11\r\n", "").encode("ascii"))
    deleted = commit_all("delete one line")

    # ARM-CLEAN-APPEND and ARM-EOL-REWRITE built from the base bytes.
    subprocess.run(["git", "-C", tmp, "reset", "-q", "--hard", base],
                   capture_output=True, env=env)
    with open(p, "ab") as f:  # append CRLF lines, touch nothing else
        f.write(b"new-a\r\nnew-b\r\n")
    clean = commit_all("clean append")

    subprocess.run(["git", "-C", tmp, "reset", "-q", "--hard", base],
                   capture_output=True, env=env)
    # the r62 shape: rewrite the tail blocks LF->CRLF, then append new lines
    raw = open(p, "rb").read()
    head_lines = raw.split(b"\r\n")
    rewritten = b"\n".join(head_lines[:10]) + b"\n" + b"\r\n".join(head_lines[10:])
    with open(p, "wb") as f:
        f.write(rewritten + b"new-c\r\nnew-d\r\n")
    rewritten_rev = commit_all("append with LF->CRLF rewrite of tail blocks")

    passed = []
    passed.append(run_arm("CLEAN-APPEND", 0, tmp, base, clean, "REC.md")[0])
    passed.append(run_arm("EOL-REWRITE", 0, tmp, base, rewritten_rev, "REC.md")[0])
    passed.append(run_arm("REQUIRE-RAW", 1, tmp, base, rewritten_rev, "REC.md",
                          require_raw=True)[0])
    passed.append(run_arm("ALTER", 1, tmp, base, altered, "REC.md")[0])
    passed.append(run_arm("DELETE", 1, tmp, base, deleted, "REC.md")[0])
    print("ADDITIVITY_SELFTEST: %d/%d pass" % (sum(passed), len(passed)))
    subprocess.run(["git", "-C", tmp, "gc", "-q", "--prune=now"],
                   capture_output=True)
    try:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass
    return 0 if all(passed) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog="additivity-receipt.py")
    ap.add_argument("--repo")
    ap.add_argument("--base")
    ap.add_argument("--tip")
    ap.add_argument("--file", action="append",
                    help="repeatable; one receipt per file")
    ap.add_argument("--require-raw", action="store_true",
                    help="append-only must also hold on the raw bytes")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.repo and a.base and a.tip and a.file):
        ap.error("--repo --base --tip and --file are required "
                 "(unless --selftest)")
    rc = 0
    for path in a.file:
        m = measure(a.repo, a.base, a.tip, path)
        print(verdict_line(m))
        ok, _ = judge(m, a.require_raw)
        if not ok:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
