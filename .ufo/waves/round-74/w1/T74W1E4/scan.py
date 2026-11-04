#!/usr/bin/env python3
"""scan.py — INDEPENDENT per-commit additivity scan (seat T74W1E4, round 74).

Written for R74-C2's before-state. It does not import
tools/additivity-receipt.py (only its docstring was read); every number is
computed here from committed bytes read with `git cat-file blob <rev>:<path>`.

Definitions used by every printed number (all on committed bytes):

  line set (raw)       = set(raw.split(b"\\n")) - {b""}
  line set (norm_cr)   = same after \\r\\n -> \\n and \\r -> \\n
  raw_old_only         = |raw old \\ raw new|
  raw_new_only         = |raw new \\ raw old|
  norm_cr_old_only     = |norm old \\ norm new|
  verbatim_prefix      = CR-stripped, empty-dropped old content, as an ordered
                         list, is a prefix of the tip's CR-stripped,
                         empty-dropped content
  eol_rewrite_disclosed = raw_old_only != norm_cr_old_only (the raw view and
                         the normalized view disagree, so the raw comparison
                         shows a rewrite that the normalized comparison
                         absorbs; a receipt carrying both views discloses it)

`raw_old_only` is a count of distinct non-empty committed lines, matching the
line-set convention of the round-63 receipt instrument.

Usage:
  scan.py --repo DIR --base REV --tip REV --path P [--path P ...]
          [--focus REV:PATH ...]

Output (stdout): one ROW line per (commit, file) whose blob differs from its
first parent, then SUMMARY lines, then one TOTAL line per file for
base -> tip, then FOCUS lines for named (rev, path) pairs.

Exit: 0 scan completed; 2 setup/usage error.
"""
import argparse
import subprocess
import sys


def die(msg):
    print("SCAN error=%s" % msg, file=sys.stderr)
    sys.exit(2)


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        die("git-%s rc=%d: %s" % (args[0], r.returncode,
                                  r.stderr.decode(errors="replace").strip()[:300]))
    return r.stdout


def blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob",
                        "%s:%s" % (rev, path)], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def line_set(raw, norm_cr):
    if norm_cr:
        raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return set(raw.split(b"\n")) - {b""}


def content_list(raw):
    b = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return [ln for ln in b.split(b"\n") if ln != b""]


def prefix_ok(old_raw, new_raw):
    old = content_list(old_raw)
    new = content_list(new_raw)
    return new[:len(old)] == old


def measure(old_raw, new_raw):
    return {
        "raw_old_only": len(line_set(old_raw, False) - line_set(new_raw, False)),
        "raw_new_only": len(line_set(new_raw, False) - line_set(old_raw, False)),
        "norm_cr_old_only": len(line_set(old_raw, True) - line_set(new_raw, True)),
        "verbatim_prefix": prefix_ok(old_raw, new_raw),
    }


def fmt(m):
    return ("raw_old_only=%d raw_new_only=%d norm_cr_old_only=%d "
            "verbatim_prefix=%s" %
            (m["raw_old_only"], m["raw_new_only"], m["norm_cr_old_only"],
             "true" if m["verbatim_prefix"] else "false"))


def eol_disclosed(m):
    return m["raw_old_only"] != m["norm_cr_old_only"]


def tf(b):
    return "true" if b else "false"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--tip", required=True)
    ap.add_argument("--path", action="append", required=True)
    ap.add_argument("--focus", action="append", default=[])
    a = ap.parse_args()

    repo = git(a.repo, "rev-parse", "--show-toplevel").decode().strip()
    base = git(repo, "rev-parse", "--verify", a.base + "^{commit}").decode().strip()
    tip = git(repo, "rev-parse", "--verify", a.tip + "^{commit}").decode().strip()

    revs = git(repo, "rev-list", "--reverse", "--first-parent",
               "%s..%s" % (base, tip)).decode().split()
    if not revs:
        die("empty range %s..%s" % (base, tip))

    print("SCAN repo=%s base=%s tip=%s first_parent=1 revs=%d files=%d" %
          (repo, base[:12], tip[:12], len(revs), len(a.path)))

    removed = []
    rewrites = []
    rows = 0
    for rev in revs:
        parent = git(repo, "rev-parse", "--verify", rev + "^").decode().strip()
        for path in a.path:
            old = blob(repo, parent, path)
            new = blob(repo, rev, path)
            if old is None or new is None:
                print("ROW %s path=%s parent=%s MISSING_BLOB old=%s new=%s" %
                      (rev[:12], path, parent[:12],
                       "absent" if old is None else "present",
                       "absent" if new is None else "present"))
                continue
            if old == new:
                continue
            rows += 1
            m = measure(old, new)
            print("ROW %s path=%s parent=%s %s eol_rewrite_disclosed=%s" %
                  (rev[:12], path, parent[:12], fmt(m), tf(eol_disclosed(m))))
            if m["raw_old_only"] > 0:
                removed.append((rev, path, m["raw_old_only"]))
            if eol_disclosed(m):
                rewrites.append((rev, path, m["raw_old_only"],
                                 m["norm_cr_old_only"]))

    print("SUMMARY rows=%d" % rows)
    print("SUMMARY raw_removed=%d %s" %
          (len(removed), " ".join("%s:%s:%d" % (r[:12], p, n)
                                  for r, p, n in removed) or "none"))
    print("SUMMARY rewrite_visible=%d %s" %
          (len(rewrites), " ".join("%s:%s:raw=%d:norm=%d" % (r[:12], p, ro, no)
                                   for r, p, ro, no in rewrites) or "none"))

    for path in a.path:
        old = blob(repo, base, path)
        new = blob(repo, tip, path)
        if old is None or new is None:
            print("TOTAL path=%s MISSING_BLOB" % path)
            continue
        m = measure(old, new)
        print("TOTAL path=%s range=%s..%s %s eol_rewrite_disclosed=%s" %
              (path, base[:12], tip[:12], fmt(m), tf(eol_disclosed(m))))

    for spec in a.focus:
        rev, sep, path = spec.partition(":")
        if not sep or not path:
            die("--focus expects REV:PATH, got %r" % spec)
        rev = git(repo, "rev-parse", "--verify", rev + "^{commit}").decode().strip()
        parent = git(repo, "rev-parse", "--verify", rev + "^").decode().strip()
        old = blob(repo, parent, path)
        new = blob(repo, rev, path)
        if old is None or new is None:
            die("focus pair %s:%s has an absent blob" % (rev[:12], path))
        m = measure(old, new)
        print("FOCUS rev=%s parent=%s path=%s %s eol_rewrite_disclosed=%s" %
              (rev, parent, path, fmt(m), tf(eol_disclosed(m))))


if __name__ == "__main__":
    main()
