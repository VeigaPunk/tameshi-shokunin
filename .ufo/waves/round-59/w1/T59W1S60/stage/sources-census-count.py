#!/usr/bin/env python3
"""Independent SOURCES census counter for seat T59W1S60.

Row rule (census-valid 0-3-space contract, cf. tools/pbt-staged-id.py,
tools/staged-id-guard.py): a row is a line matching "^ {0,3}\\|\\s*S\\d{3,}\\s*\\|"
(rows indented 4+ spaces are NOT rows). Table schema (13 fields split on '|'):
  1:'', 2:id, 3:source, 4:kind, 5:tier, 6:scope, 7:anchor, 8:teaches,
  9:status, 10:opened, 11:recheck, 12:used-by, 13:''
tier field=5, status field=9 (1-based, same awk -F'|' view the v2 shell census uses).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROW_0_3 = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
ROW_0 = re.compile(r"^\|\s*(S\d{3,})\s*\|")  # column-zero-only, for delta

KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}
STATUSES = {"queued", "mined", "rejected"}

def count(lines, row_re):
    rows, malformed, ids = 0, 0, []
    tiers, statuses, kinds = Counter(), Counter(), Counter()
    enums, dups = [], []
    for ln in lines:
        m = row_re.match(ln)
        if not m:
            continue
        rows += 1
        ids.append(m.group(1))
        f = ln.split("|")
        if len(f) != 13:
            malformed += 1
            continue
        i = f[1].strip(); k = f[3].strip(); t = f[4].strip(); s = f[8].strip()
        tiers[t] += 1; statuses[s] += 1; kinds[k] += 1
        if t not in ("A", "B", "C"):
            enums.append(("tier", i, t))
        if s not in STATUSES:
            enums.append(("status", i, s))
        if k not in KINDS:
            enums.append(("kind", i, k))
        if t == "A" and k == "community":
            enums.append(("tier-inflation", i, ""))
    for i, n in Counter(ids).items():
        if n > 1:
            dups.append(i)
    return {"rows": rows, "malformed": malformed, "tiers": dict(tiers),
            "status": dict(statuses), "kinds": dict(kinds),
            "dup_ids": sorted(dups), "enum_violations": enums}

def main():
    path = Path("corpus/SOURCES.md")
    lines = path.read_text(encoding="utf-8").splitlines()
    r03 = count(lines, ROW_0_3)
    r0 = count(lines, ROW_0)
    report = {
        "file": str(path),
        "indent_0_3_space_contract": r03,
        "column_zero_only_delta": {
            "rows_0_space": r0["rows"],
            "rows_added_by_0_3_rule": r03["rows"] - r0["rows"],
            "ids_only_in_0_3": sorted(set(
                m.group(1) for ln in lines if ROW_0_3.match(ln)
                for m in [ROW_0_3.match(ln)]) - set(
                m.group(1) for ln in lines if ROW_0.match(ln)
                for m in [ROW_0.match(ln)])),
        },
    }
    json.dump(report, sys.stdout, indent=1, sort_keys=True)
    print()

if __name__ == "__main__":
    main()
