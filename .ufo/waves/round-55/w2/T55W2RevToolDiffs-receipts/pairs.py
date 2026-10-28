#!/usr/bin/env python3
"""Render the TMPDIR pair table from the seat's receipt dirs (attack receipt)."""
import os
import sys

R = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w2/T55W2RevToolDiffs-receipts"


def cell(path):
    with open(path, "rb") as fh:
        data = fh.read()
    return data


def main():
    tags = sys.argv[1:] or ["base", "c0"]
    for tag in tags:
        d = os.path.join(R, tag)
        if not os.path.isdir(d):
            continue
        print("### %s" % tag)
        print("| arm | rc | stdout bytes | stdout first line | stderr first line |")
        print("|---|---|---|---|---|")
        arms = sorted(n[: -len(".rc")] for n in os.listdir(d) if n.endswith(".rc"))
        for arm in arms:
            rc = cell(os.path.join(d, arm + ".rc")).decode().strip()
            out = cell(os.path.join(d, arm + ".stdout"))
            err = cell(os.path.join(d, arm + ".stderr"))
            first = out.decode("utf-8", "replace").splitlines()[:1]
            efirst = err.decode("utf-8", "replace").splitlines()[:1]
            print("| %s | %s | %d | %s | %s |" % (
                arm, rc, len(out),
                (first[0][:110].replace("|", "\\|") if first else ""),
                (efirst[0][:130].replace("|", "\\|") if efirst else "")))
        print()


if __name__ == "__main__":
    main()
