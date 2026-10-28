#!/usr/bin/env python3
"""T55W2SimplDiff: measure what the C0 registry.json rewrite actually changed.

Usage: python3 measure-churn.py <lane-repo>
Exit 0 iff the file's parsed payload differs from base in exactly seven cells and
every other changed line is whitespace/layout.
"""
import json
import subprocess
import sys

BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
PATH = "tools/registry.json"


def show(lane, rev):
    return subprocess.run(["git", "-C", lane, "show", "%s:%s" % (rev, PATH)],
                          capture_output=True, text=True, check=True).stdout


def main():
    lane = sys.argv[1]
    base_txt, c0_txt = show(lane, BASE), show(lane, C0)
    base = json.loads(base_txt)
    c0 = json.loads(c0_txt)
    changed = []
    for b, c in zip(base["rows"], c0["rows"]):
        if b != c:
            keys = [k for k in b if b.get(k) != c.get(k)]
            changed.append((b["name"], keys))
    stripped = [{k: v for k, v in r.items() if k != "scratch_root"} for r in base["rows"]]
    stripped_c0 = [{k: v for k, v in r.items() if k != "scratch_root"} for r in c0["rows"]]
    numstat = subprocess.run(["git", "-C", lane, "diff", "--numstat", BASE, C0, "--", PATH],
                             capture_output=True, text=True, check=True).stdout.split()
    added, removed = int(numstat[0]), int(numstat[1])
    lines_b, lines_c0 = len(base_txt.splitlines()), len(c0_txt.splitlines())
    print("rows base/c0: %d/%d" % (len(base["rows"]), len(c0["rows"])))
    print("schema equal: %s" % (base["schema"] == c0["schema"]))
    print("payload identical outside scratch_root: %s" % (stripped == stripped_c0))
    print("changed cells: %d" % sum(len(k) for _, k in changed))
    for name, keys in changed:
        print("  %s -> %s" % (name, ",".join(keys)))
    print("diff lines: +%d -%d (semantic +7/-7, layout +%d/-%d)"
          % (added, removed, added - 7, removed - 7))
    print("file lines base/c0: %d/%d (+%d from re-serialization)"
          % (lines_b, lines_c0, lines_c0 - lines_b))
    # every changed line that is not one of the seven cells must be layout only:
    # collapse all whitespace after blanking every scratch_root value
    def blank(text, rows):
        for r in rows:
            if "scratch_root" in r:
                text = text.replace(json.dumps(r["scratch_root"]), '"<CELL>"')
        return "".join(text.split())

    layout_only = blank(base_txt, base["rows"]) == blank(c0_txt, c0["rows"])
    print("whitespace-collapsed bytes identical except the seven cells: %s" % layout_only)
    return 0 if (sum(len(k) for _, k in changed) == 7 and stripped == stripped_c0
                 and layout_only) else 1


if __name__ == "__main__":
    sys.exit(main())
