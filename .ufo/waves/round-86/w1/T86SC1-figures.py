#!/usr/bin/env python3
"""T86SC1: list, per capability row, the claimed figures (selftest tallies)
so they can be re-measured against the instrument each row names."""
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "d10a9c66d6181cddcad52cdbffd672beb886ff6c"


def blob(rev, path):
    return subprocess.run(["git", "-C", REPO, "cat-file", "blob", "%s:%s" % (rev, path)],
                          stdout=subprocess.PIPE, check=True).stdout.decode()


text = blob(REV, "SCORECARD.md")
lines = text.splitlines()
idx = next(i for i, l in enumerate(lines) if l.strip() == "## Capabilities")
rows = []
cur = None
for l in lines[idx + 1:]:
    if l.startswith("## "):
        break
    s = l.strip()
    if s.startswith("|"):
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: ") or cells[0] == "Capability":
            cur = None
            continue
        if len(cells) < 3:
            cur = None
            continue
        cur = {"name": cells[0], "ev": cells[2]}
        rows.append(cur)
    elif cur is not None and s:
        cur["ev"] += " " + s

FIG = re.compile(r"([A-Z][A-Z0-9_]{4,})\s*:\s*(\d+/\d+)")
for r in rows:
    figs = FIG.findall(r["ev"])
    # the command(s) the row names
    cmds = re.findall(r"`([^`]*(?:tools/|\.ufo/)[^`]*)`", r["ev"])
    print("ROW: %s" % r["name"])
    for tag, tal in figs:
        print("   FIG %s %s" % (tag, tal))
    for c in cmds:
        print("   CMD %s" % c[:150])
