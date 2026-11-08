#!/usr/bin/env python3
"""Round 100 C2 do-nothing control: the lane's prior check class — is the quote present anywhere
in the rendered snapshot (`C1_SOURCE ... quote:1`) — run over the same Gate pointers the C2 tool
binds. It reuses the tool's own extraction and binding (loaded from the tool blob path given) and
only replaces the verdict: `present` iff the quote is located anywhere, ignoring the cited line.

Usage: python3 -I quote-presence-control.py <gate-line-recheck.py path> <lane> <rev> <record>...
Prints one `QUOTE_PRESENCE <verdict> <record>:<line>` per pointer and
`QUOTE_PRESENCE pointers=P present=N absent=A unbound=U flagged_d1=F` where flagged_d1 counts the
pointers the C2 tool grades `miss` that this control flags (absent); exit 0 when absent=0.
"""
import importlib.util
import os
import re
import sys


def main():
    tool, lane, rev, records = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    spec = importlib.util.spec_from_file_location("glr", tool)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    lines, _ = m.recheck(m.Tree(os.path.abspath(lane), rev), records, m.DEFAULT_RENDERER)
    counts = {"present": 0, "absent": 0, "unbound": 0}
    flagged = 0
    for ln in lines[:-1]:
        f = ln.split()
        verdict, where = f[1], f[2]
        observed = re.search(r"observed=(\S+)", ln).group(1)
        if verdict == "unbound":
            v = "unbound"
        elif observed != "-":
            v = "present"
        else:
            v = "absent"
        if verdict == "miss" and v == "absent":
            flagged += 1
        counts[v] += 1
        print("QUOTE_PRESENCE %s %s tool_verdict=%s" % (v, where, verdict))
    total = sum(counts.values())
    print("QUOTE_PRESENCE pointers=%d present=%d absent=%d unbound=%d flagged_d1=%d"
          % (total, counts["present"], counts["absent"], counts["unbound"], flagged))
    return 0 if counts["absent"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
