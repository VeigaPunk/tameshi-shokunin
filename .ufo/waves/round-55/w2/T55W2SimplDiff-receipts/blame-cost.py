#!/usr/bin/env python3
"""T55W2SimplDiff: blame attribution cost of the whole-file registry rewrite.

Compares, for tools/registry.json, how many lines each commit owns at
(a) base, (b) C0, and (c) a counterfactual child of base carrying only the
seven cell replacements.

Usage: python3 blame-cost.py <lane-repo> [counterfactual-rev [clone-for-that-rev]]
Exit 0 always; the numbers are the receipt.
"""
import collections
import subprocess
import sys

BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
PATH = "tools/registry.json"


def blame(lane, rev):
    out = subprocess.run(["git", "-C", lane, "blame", "--line-porcelain", rev, "--", PATH],
                         capture_output=True, text=True, check=True).stdout
    owners = collections.Counter()
    for line in out.splitlines():
        if line.startswith("summary "):
            owners[line[8:60]] += 1
    return owners


def main():
    lane = sys.argv[1]
    cases = [("base", lane, BASE), ("C0", lane, C0)]
    if len(sys.argv) > 2:  # the counterfactual commit lives in the scratch clone
        cases.append(("counterfactual", sys.argv[3] if len(sys.argv) > 3 else lane, sys.argv[2]))
    for label, repo, rev in cases:
        owners = blame(repo, rev)
        total = sum(owners.values())
        print("%-15s rev=%s lines=%d distinct-owner-commits=%d top=%s"
              % (label, rev[:10], total, len(owners),
                 ", ".join("%d" % n for _, n in owners.most_common(4))))
        for summary, n in owners.most_common(4):
            print("    %4d  %s" % (n, summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
