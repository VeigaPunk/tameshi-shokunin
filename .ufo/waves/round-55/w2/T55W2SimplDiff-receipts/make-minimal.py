#!/usr/bin/env python3
"""T55W2SimplDiff: rebuild C0's registry.json as seven changed lines.

Keeps the base file's own layout (2-space rows with the later rows' inline
arrays/objects) and substitutes only the seven `scratch_root` values C0 wrote.
Writes <out> and proves json.loads(<out>) == json.loads(C0).

Usage: python3 make-minimal.py <lane-repo> <out-file> [value-source]
`value-source` is a revision (default C0) or the path of a JSON file whose
scratch_root values are the final ones -- re-run this after the seven cells'
text changes, e.g. with the lane worktree file as the source.
Exit 0 iff the output parses to exactly the source's payload.
"""
import json
import os
import re
import subprocess
import sys

BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
PATH = "tools/registry.json"
NAME = re.compile(r'^(\s*)"name": "(.*)",$')
CELL = re.compile(r'^(\s*)"scratch_root": ')


def show(lane, rev):
    return subprocess.run(["git", "-C", lane, "show", "%s:%s" % (rev, PATH)],
                          capture_output=True, text=True, check=True).stdout


def main():
    lane, out = sys.argv[1], sys.argv[2]
    source = sys.argv[3] if len(sys.argv) > 3 else C0
    base_txt = show(lane, BASE)
    c0_txt = open(source).read() if os.path.exists(source) else show(lane, source)
    base, c0 = json.loads(base_txt), json.loads(c0_txt)
    want = {b["name"]: c["scratch_root"]
            for b, c in zip(base["rows"], c0["rows"])
            if b.get("scratch_root") != c.get("scratch_root")}
    lines, cur, patched = [], None, 0
    for line in base_txt.splitlines(True):
        m = NAME.match(line)
        if m:
            cur = m.group(2)
        m = CELL.match(line)
        if m and cur in want:
            tail = "\n" if line.endswith("\n") else ""
            comma = "," if line.rstrip().endswith(",") else ""
            lines.append('%s"scratch_root": %s%s%s' % (m.group(1), json.dumps(want[cur]), comma, tail))
            patched += 1
            cur = None
            continue
        lines.append(line)
    new = "".join(lines)
    with open(out, "w") as fh:
        fh.write(new)
    ok = json.loads(new) == json.loads(c0_txt)
    print("patched cells: %d (%s)" % (patched, ",".join(sorted(want))))
    print("lines base/out: %d/%d" % (len(base_txt.splitlines()), len(new.splitlines())))
    print("payload == source(%s): %s" % (source, ok))
    return 0 if ok and patched == 7 else 1


if __name__ == "__main__":
    sys.exit(main())
