#!/usr/bin/env python3
"""pointer-sweep-a2.py — re-resolve the pointers round-60 attempt 2 added.

Criterion 116, attempt-2 sweep (records land at f0ec3a5b4514b64752ff8fb1f97760bbc88f2acf;
receipt files land with the receipts commit and are DEFERRED until then).

Usage:
    python pointer-sweep-a2.py --lane LANE --rev REV --receipt OUT.json

Read-only: it reads git objects only and writes one receipt file.
"""

import argparse
import json
import subprocess
import sys

# (id, path, first_line, last_line, what the pointer claims) — resolved
# against --rev (the records commit).
POINTERS = [
    ("A2-counter", "tools/executor-source-pin-measure-v2.py", 1, 34,
     "portable counter header and declared paths"),
    ("A2-plan", "plans/round-60-attempt2.plan.md", 1, 1,
     "attempt-2 plan (frozen pre-data)"),
    ("A2-contract", ".ufo/evidence/round-60/win-host/contract-a2.json", 1, 1,
     "attempt-2 contract"),
    ("A2-amend", ".ufo/evidence/round-60/win-host/contract-a2-amend1.json", 1, 1,
     "amendment A1 (order-dependent sequence arm re-stated)"),
    ("A2-freeze", ".ufo/evidence/round-60/win-host/freeze-v2.json", 1, 1,
     "attempt-2 instrument freeze"),
    ("A2-freeze-amend", ".ufo/evidence/round-60/win-host/freeze-amend1.json", 1, 1,
     "amendment freeze"),
    ("A2-probe", ".ufo/evidence/round-60/win-host/host-probe.txt", 1, 1,
     "win32 host probe receipt"),
    ("A2-red", ".ufo/evidence/round-60/win-host/red-v1-counter.err", 1, 1,
     "v1 counter red receipt on win32 (UnicodeEncodeError + PermissionError)"),
    ("A2-s292-src", ".ufo/evidence/round-60/win-host/sources/s292-update-index.html", 1, 1,
     "S292 fetch extract"),
    ("A2-s073-src", ".ufo/evidence/round-60/win-host/sources/s073-cmdline-refetch.html", 1, 1,
     "S073 win32 refetch extract"),
    ("A2-s292-row", "corpus/SOURCES.md", 167, 167,
     "S292 registry row"),
    ("A2-q118", "corpus/QUALITY.md", 1883, 1884,
     "criterion 118 heading (host scope + instrument revision)"),
    ("A2-q119", "corpus/QUALITY.md", 1917, 1918,
     "criterion 119 heading (deterministic vs order-dependent arms)"),
    ("A2-mistake6", "corpus/lessons/round-60.md", 165, 166,
     "lesson mistake 6 (host-scoped-instrument)"),
    ("A2-mistake7", "corpus/lessons/round-60.md", 190, 191,
     "lesson mistake 7 (over-specified-predicate)"),
    ("A2-mistake8", "corpus/lessons/round-60.md", 216, 217,
     "lesson mistake 8 (host-infeasible-instrument)"),
    ("A2-attempt2-lesson", "corpus/lessons/round-60.md", 306, 307,
     "lesson Attempt 2 section heading"),
    ("A2-province", "PROVINCE.md", 120, 121,
     "PROVINCE host correction heading"),
    ("A2-scorecard", "SCORECARD.md", 2989, 2990,
     "SCORECARD attempt-2 measured claims heading"),
]

# (id, path, what the pointer claims) — land with the receipts commit;
# resolved against the working tree at sweep time.
DEFERRED = [
    ("A2-cert", ".ufo/evidence/round-60/win-host/amend1/cert.out",
     "C1_R60V2 certification receipt 8/8 at ffa56602"),
    ("A2-cert-repeat", ".ufo/evidence/round-60/win-host/amend1/cert-repeat.out",
     "repeat certification receipt (other nonce/order)"),
    ("A2-first-family-seq", ".ufo/evidence/round-60/win-host/first-family/ctl-sequence.out",
     "first scored family's sequence draw (1/8, mistake 7 evidence)"),
    ("A2-fv2-verify", ".ufo/evidence/round-60/win-host/amend1/freeze-v2-verify.json",
     "freeze-v2 verification receipt"),
    ("A2-noharm-cand", ".ufo/evidence/round-60/win-host/noharm-cand.json",
     "no-harm substitute receipt (46/64 credited at cand)"),
    ("A2-precheck-status", ".ufo/evidence/round-60/win-host/amend1/coldread-precheck.out",
     "frozen precheck infeasibility status receipt"),
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
        import os
        present = os.path.exists(os.path.join(a.lane, path))
        deferred.append({"id": pid, "path": path, "claim": claim,
                         "resolved": present,
                         "note": "lands with the receipts commit"})
    unresolved = [r for r in rows if not (r["resolved"] and r["lines_in_range"])]
    unresolved += [d for d in deferred if not d["resolved"]]
    receipt = {"schema": "tameshi-pointer-sweep-v1", "lane": a.lane,
               "rev": a.rev, "pointers": rows, "deferred": deferred,
               "unresolved": [r["id"] for r in unresolved],
               "resolved_count": len(rows) - len([r for r in rows if not (r["resolved"] and r["lines_in_range"])]),
               "total": len(rows)}
    with open(a.receipt, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("POINTER_SWEEP rev=%s resolved=%d/%d deferred=%d/%d unresolved=%s"
          % (a.rev[:12], receipt["resolved_count"], receipt["total"],
             sum(1 for d in deferred if d["resolved"]), len(deferred),
             ",".join(receipt["unresolved"]) or "none"))
    for r in unresolved:
        print("DRIFTED %s" % r["id"])
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
