#!/usr/bin/env python3
"""T88M1 — single-edit mutants of the frozen round-88 counter.

usage: T88M1-make-mutants.py <frozen-measure.py> <out-dir>

Each mutant applies exactly ONE edit to the frozen counter (count==1 asserted, so a
mutant cannot silently miss its anchor). The frozen file is never written.

M1  drop the top-name sibling check (repo dir must not be `tameshi-shokunin`)
M2  drop the suite allow-list check (SUITES.get(suite) != interpreter)
M3  drop the duplicate-target check ((real repo, path) already seen)
M4  drop the prereg sha comparison (any single counted py leg reads as prereg=ok)
M5  count a leg when `agree < n` (equality relaxed to <=)
M6  count a leg without requiring at least one KILLED verdict
M7  accept INCONCLUSIVE as agreement with the recorded table
M8  drop the pinned-blob sha256 check
"""
import sys
from pathlib import Path

EDITS = [
    ("M1", '    if top == "tameshi-shokunin" or not repo.is_dir():\n',
           '    if not repo.is_dir():\n'),
    ("M2", '    if SUITES.get(leg["suite"]) != interp:\n',
           '    if False:  # M2: suite allow-list dropped\n'),
    ("M3", '    if key in seen:\n',
           '    if False:  # M3: duplicate-target check dropped\n'),
    ("M4", '    elif len(py) == 1 and py[0]["spec_sha"] == PREREG_SHA:\n',
           '    elif len(py) == 1:\n'),
    ("M5", '    if out["agree"] == out["n"] and out["killed"] >= 1:\n',
           '    if out["agree"] <= out["n"] and out["killed"] >= 1:\n'),
    ("M6", '    if out["agree"] == out["n"] and out["killed"] >= 1:\n',
           '    if out["agree"] == out["n"]:\n'),
    ("M7", '        if v == table[d["id"]]:\n',
           '        if v == table[d["id"]] or v == "INCONCLUSIVE":\n'),
    ("M8", '    if hashlib.sha256(blob.stdout).hexdigest() != leg["pin"]:\n',
           '    if False:  # M8: pin sha256 check dropped\n'),
]


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    text = src.read_text()
    out.mkdir(parents=True, exist_ok=True)
    import hashlib
    print("frozen %s sha256=%s" % (src, hashlib.sha256(text.encode()).hexdigest()))
    for mid, old, new in EDITS:
        assert text.count(old) == 1, "%s anchor count=%d" % (mid, text.count(old))
        dst = out / ("T88M1-%s.py" % mid)
        dst.write_text(text.replace(old, new, 1))
        d = dst.read_bytes()
        print("%s %s old=%r new=%r bytes=%d sha256=%s" % (
            mid, dst, old.strip(), new.strip(), len(d), hashlib.sha256(d).hexdigest()))
        # exactly one line must differ from the frozen bytes
        a, b = text.split("\n"), dst.read_text().split("\n")
        diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        extra = abs(len(a) - len(b))
        assert len(diff) == 1 and extra == 0, "%s diff lines=%d extra=%d" % (mid, len(diff), extra)
        print("   single-line diff at line %d" % (diff[0][0] + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
