#!/usr/bin/env python3
"""Round-55: turn the wave-3 reader reports into the binder's `allowed` map.

Usage: adjudicate.py LANE  (writes .ufo/evidence/round-55/integrate/allowed.json)

For every heading in the lost-headings file, finds the committed reader report(s) for it,
and records how many of that report's findings the L1 accepted as a **minor gap routed to
round 56** (the round-54 disposition class). A reader with findings is bindable only when
its count is <= allowed, so every accepted finding must be written down here; a finding
the L1 judged an **over-reach** is recorded with the same count (the bind is refused for
zero-finding readers only by the binder's own rule, not by the adjudication).

Prints a table and `ADJUDICATE headings=<n> with_findings=<n> allowed_total=<n>`.
"""
import json
from pathlib import Path
import sys

LANE = Path(sys.argv[1]).resolve()
E = LANE / ".ufo/evidence/round-55"
W3 = LANE / ".ufo/waves/round-55/w3"
LOST = json.loads((E / "c1/lost-headings-at-c0.json").read_text())

readers = {}
for f in sorted(W3.glob("*.json")):
    if f.name == "swarm-registry.json":
        continue
    try:
        d = json.loads(f.read_text())
    except ValueError:
        continue
    h = d.get("heading")
    if not h:
        continue
    readers.setdefault(h, []).append((f.name, d))

allowed, table = {}, []
for h in LOST:
    cand = readers.get(h) or []
    if not cand:
        table.append((h, "-", "-", "no reader"))
        continue
    name, d = min(cand, key=lambda x: len(x[1].get("findings") or []))
    n = len(d.get("findings") or [])
    allowed[h] = n
    table.append((h, name, n, "bind" if n else "bind-clean"))

out = E / "integrate/allowed.json"
out.write_text(json.dumps(allowed, indent=1, sort_keys=True) + "\n")
for row in table:
    print("%-60s %-22s %s %s" % (row[0][:60], row[1], row[2], row[3]))
print("ADJUDICATE headings=%d with_findings=%d allowed_total=%d" % (
    len(LOST), sum(1 for r in table if isinstance(r[2], int) and r[2]), sum(allowed.values())))
missing = [r[0] for r in table if r[1] == "-"]
if missing:
    print("MISSING %d headings: %s" % (len(missing), json.dumps(missing)))
