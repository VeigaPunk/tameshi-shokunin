#!/usr/bin/env python3
"""Counter-arm liveness census (draft for `.ufo/evidence/round-56/quality/arm-census.py`).

Reads every committed receipt under `.ufo/evidence/` at REV, takes each counter
verdict line (`C1_R54: ... key=value ...`, also when prefixed by a control tag),
and prints, per counter arm, how many observations exist and how many are
non-zero. An arm with `observations>0` and `nonzero=0` has no committed input
that moves it -- the class `considerthese/2026-10-28.md` proposal 2 names.

  arm-census.py --lane LANE --rev REV [--json OUT] [--quiet]

Exit 0 always (this is a census, not a gate); a gate form would exit 1 when a
named arm's `nonzero` is 0.
"""
import argparse
import collections
import json
import pathlib
import re
import subprocess
import sys

SUFFIX = re.compile(r"\.(stdout|out|txt)$")
TAG = re.compile(r"\b(C[12]_R\d+):\s")
KV = re.compile(r"([a-z_]+)=([^\s]+)")
NUM = re.compile(r"^(\d+)")


def census(lane, rev):
    files = subprocess.run(["git", "-C", str(lane), "ls-tree", "-r", "--name-only", rev],
                           capture_output=True, text=True, check=True).stdout.split()
    receipts = [f for f in files if SUFFIX.search(f) and f.startswith(".ufo/evidence/")]
    obs = collections.defaultdict(list)
    for f in receipts:
        txt = subprocess.run(["git", "-C", str(lane), "show", "%s:%s" % (rev, f)],
                             capture_output=True, text=True).stdout
        for line in txt.splitlines():
            m = TAG.search(line)
            if not m:
                continue
            seen = set()
            for k, v in KV.findall(line):
                if k == "rev" or k in seen:
                    continue
                seen.add(k)
                obs[(m.group(1), k)].append((f, v))
    arms = []
    for (counter, arm), vs in sorted(obs.items()):
        nums = [int(NUM.match(v).group(1)) for _, v in vs if NUM.match(v)]
        arms.append({"counter": counter, "arm": arm, "observations": len(vs),
                     "numeric": bool(nums), "max": max(nums) if nums else None,
                     "nonzero": sum(1 for n in nums if n),
                     "receipts": sorted({f for f, _ in vs})})
    return {"rev": rev, "receipts_scanned": len(receipts), "arms": arms,
            "arms_with_no_nonzero": [a for a in arms if a["numeric"] and a["max"] == 0]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    c = census(pathlib.Path(a.lane).resolve(), a.rev)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(c, indent=1) + "\n")
    if not a.quiet:
        print("REV %s -- receipts scanned: %d, arms: %d, arms with no non-zero observation: %d"
              % (a.rev[:12], c["receipts_scanned"], len(c["arms"]), len(c["arms_with_no_nonzero"])))
        for arm in c["arms_with_no_nonzero"]:
            print("  %-8s %-20s obs=%-3d max=%s receipts=%s"
                  % (arm["counter"], arm["arm"], arm["observations"], arm["max"],
                     ";".join(arm["receipts"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
