#!/usr/bin/env python3
"""T55W2SimplDiff: census of the C0 diff's non-production (evidence) churn.

For every path C0 adds under .ufo/waves/round-55/: count files, bytes, exact
duplicate blobs (same blob in several seat dirs), and zero-byte receipts.
A zero-byte receipt is an observation ("no stderr"), not waste; a duplicated
blob is redundant bytes but usually per-seat provenance.

Usage: python3 evidence-census.py <lane-repo>
"""
import collections
import subprocess
import sys

BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
EMPTY = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


def main():
    lane = sys.argv[1]
    changed = subprocess.run(["git", "-C", lane, "diff", "--name-only", BASE, C0],
                             capture_output=True, text=True, check=True).stdout.split()
    wave = [p for p in changed if p.startswith(".ufo/waves/round-55/")]
    prod = [p for p in changed if not p.startswith(".ufo/")]
    batch = subprocess.run(
        ["git", "-C", lane, "cat-file", "--batch-check=%(objectname) %(objectsize)"],
        input="\n".join("%s:%s" % (C0, p) for p in wave),
        capture_output=True, text=True, check=True).stdout.splitlines()
    info = []
    for line in batch:
        parts = line.split()
        info.append((parts[0], int(parts[1]) if len(parts) > 1 else 0))
    groups = collections.defaultdict(list)
    for path, (blob, size) in zip(wave, info):
        groups[blob].append((path, size))
    dups = {b: v for b, v in groups.items() if len(v) > 1 and b != EMPTY}
    redundant = sum((len(v) - 1) * (v[0][1] or 0) for v in dups.values())
    print("changed paths total: %d (production %d, wave-55 evidence %d)"
          % (len(changed), len(prod), len(wave)))
    print("wave-55 bytes: %d" % sum(size for _, size in info))
    print("duplicate blob groups (non-empty): %d, redundant bytes: %d" % (len(dups), redundant))
    for blob, v in sorted(dups.items(), key=lambda kv: -(len(kv[1]) - 1) * (kv[1][0][1] or 0))[:5]:
        print("  %2d copies x %6d bytes  newest path: %s"
              % (len(v), v[0][1] or 0, v[-1][0]))
    print("zero-byte receipts: %d (an empty stderr is the observation)" %
          sum(1 for _, size in info if size == 0))
    print("production paths:")
    for p in prod:
        print("  " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
