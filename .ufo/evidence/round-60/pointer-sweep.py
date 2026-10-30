#!/usr/bin/env python3
"""pointer-sweep.py — re-resolve every line/page pointer the round added.

Criterion 116: a pointer the round adds (path:line, path:lines, page or
section reference) is re-resolved against the bytes at the revision that
lands it; unresolved or drifted pointers are named, never left as prose.

Usage:
    python3 pointer-sweep.py --lane LANE --rev REV --receipt OUT.json

Read-only: it reads git objects only and writes one receipt file.
"""
import argparse
import json
import re
import subprocess
import sys

# (id, path, first_line, last_line, what the pointer claims)
POINTERS = [
    ("Q111-cheatfp", ".ufo/evidence/round-59/controls/cheat-cheat-fp.out", 1, 1,
     "round-59 fingerprint cheat receipt (24/24)"),
    ("Q111-r60fp", ".ufo/evidence/round-60/controls/ctl-fingerprint.out", 1, 1,
     "round-60 fingerprint cheat receipt (3/8)"),
    ("Q112-firstpath", ".ufo/evidence/round-60/controls/ctl-first-path-only.py", 1, 1,
     "first-path-only strawman source"),
    ("Q112-firstpath-out", ".ufo/evidence/round-60/controls/ctl-first-path-only.out", 1, 1,
     "first-path-only strawman receipt (6/8)"),
    ("Q113-ready59", ".ufo/waves/round-59/w1.ready", 1, 1,
     "round-59 ready file naming the dead L1"),
    ("Q114-results59", ".ufo/waves/round-59/w1-results.json", 1, 1,
     "round-59 wave results (64 settled seats)"),
    ("Q115-contract59", ".ufo/evidence/round-59/contract.json", 1, 1,
     "round-59 contract without coldread_forecast"),
    ("Q115-freeze60", ".ufo/evidence/round-60/freeze.json", 1, 1,
     "round-60 freeze digesting the contract"),
    ("Q116-lesson59", "corpus/lessons/round-59.md", 1, 1,
     "round-59 lesson (word-count claim)"),
    ("Q116-considerthese", "considerthese/2026-10-28.md", 71, 71,
     "considerthese proposal 5 (stale-closure-pointer sweep)"),
    ("L-gate-secrets", ".ufo/evidence/round-60/sources/s290-secrets.html", 1, 1,
     "S290 fetch extract"),
    ("L-gate-indexformat", ".ufo/evidence/round-60/sources/s291-indexformat.html", 1, 1,
     "S291 fetch extract"),
    ("L-gate-lstree", ".ufo/evidence/round-60/sources/s291-lstree.html", 1, 1,
     "rejected source extract (git-ls-tree)"),
    ("L-mistake-v1red", ".ufo/evidence/round-60/controls/v1-tool-red.out", 1, 1,
     "v1 tool red receipt (7/8, corrupt only)"),
    ("L-cert", ".ufo/evidence/round-60/after/cert.out", 1, 1,
     "C1 certification receipt (8/8)"),
    ("L-cert-repeat", ".ufo/evidence/round-60/after/cert-repeat.out", 1, 1,
     "C1 repeat receipt (8/8, other nonce/order)"),
    ("K-amendment-tool", "tools/executor-source-pin.py", 249, 266,
     "v2 plumbing arm (exit 2)"),
    ("K-amendment-counter", "tools/executor-source-pin-measure.py", 1, 34,
     "installed counter header and declared paths"),
    ("R59.1-counter", "tools/executor-source-pin-measure.py", 1, 27,
     "ledger row R59.1 evidence lines"),
    ("R59.2-paths", "tools/executor-source-pin-measure.py", 30, 34,
     "ledger row R59.2 evidence lines"),
    ("R59.7-tool", "tools/executor-source-pin.py", 249, 266,
     "ledger row R59.7 evidence lines"),
]

# Pointers that must exist only after the metadata commit (receipts).
DEFERRED = [
    ("R59.6-precheck", ".ufo/evidence/round-60/after/coldread-precheck-final.out",
     "cold-read precheck receipt at the final revision"),
]


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                       timeout=60)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--deferred-ok", action="store_true",
                    help="treat deferred pointers as resolved when present")
    a = ap.parse_args()
    rows = []
    for pid, path, first, last, claim in POINTERS:
        rc, out = git(a.lane, "show", "%s:%s" % (a.rev, path))
        resolved = rc == 0
        excerpt = ""
        line_ok = False
        if resolved:
            lines = out.splitlines()
            line_ok = 1 <= first <= len(lines) and last <= len(lines)
            excerpt = lines[first - 1][:200] if line_ok else ""
        rows.append({"id": pid, "path": path, "lines": "%d-%d" % (first, last),
                     "claim": claim, "resolved": resolved,
                     "lines_in_range": line_ok, "excerpt": excerpt})
    deferred = []
    for pid, path, claim in DEFERRED:
        rc, _ = git(a.lane, "show", "%s:%s" % (a.rev, path))
        deferred.append({"id": pid, "path": path, "claim": claim,
                         "resolved": rc == 0,
                         "note": "lands with the metadata commit"})
    unresolved = [r for r in rows if not (r["resolved"] and r["lines_in_range"])]
    receipt = {"schema": "tameshi-pointer-sweep-v1", "lane": a.lane,
               "rev": a.rev, "pointers": rows, "deferred": deferred,
               "unresolved": [r["id"] for r in unresolved],
               "resolved_count": len(rows) - len(unresolved),
               "total": len(rows)}
    with open(a.receipt, "w") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    print("POINTER_SWEEP rev=%s resolved=%d/%d unresolved=%s"
          % (a.rev[:12], receipt["resolved_count"], receipt["total"],
             ",".join(receipt["unresolved"]) or "none"))
    for r in unresolved:
        print("DRIFTED %s %s:%s resolved=%s lines_in_range=%s"
              % (r["id"], r["path"], r["lines"], r["resolved"], r["lines_in_range"]))
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
