#!/usr/bin/env python3
"""T88M1 — truth-table probe for the three mutants whose edit is a pure counting
predicate (M5, M6, M7). The full counter runs are the primary detector; this probe
shows exactly which (agree, n, killed) / (verdict, recorded) inputs each edit
changes, so a SURVIVED verdict can be attributed to the predicate or to the
absence of a control that drives it.

usage: T88M1-predicate-probe.py <frozen-measure.py> <dir-with-T88M1-M*.py>
"""
import itertools
import sys
from pathlib import Path

FROZEN = Path(sys.argv[1])
BASE = Path(FROZEN).parent if Path(sys.argv[1]).parent.name == "round-88" else Path("/")
MUT = Path(sys.argv[2])

FROZEN_SRC = FROZEN.read_text().split("\n")


def condition(src_lines, head):
    hits = [ln.strip() for ln in src_lines if ln.strip().startswith(head)]
    assert len(hits) == 1, (head, hits)
    cond = hits[0][3:]
    assert cond.endswith(":"), cond
    return cond[:-1]


COUNT_HEAD = 'if out["agree"]'
AGREE_HEAD = 'if v == table[d["id"]]'

frozen_count = condition(FROZEN_SRC, COUNT_HEAD)
frozen_agree = condition(FROZEN_SRC, AGREE_HEAD)
print("frozen counting   : if %s:" % frozen_count)
print("frozen agreement  : if %s:" % frozen_agree)
print()

for mid in ("M5", "M6"):
    src = (MUT / ("T88M1-%s.py" % mid)).read_text().split("\n")
    cond = condition(src, COUNT_HEAD)
    print("%s counting: if %s:" % (mid, cond))
    print("  agree n killed | frozen counts | %s counts" % mid)
    for agree, n, killed in itertools.product((0, 3, 10), (10,), (0, 5)):
        skip = agree not in (0, n) and agree != 3
        f = eval(frozen_count, {}, {"out": {"agree": agree, "n": n, "killed": killed}})
        m = eval(cond, {}, {"out": {"agree": agree, "n": n, "killed": killed}})
        flag = "  <-- differs" if f != m else ""
        print("  %5d %2d %6d | %-13s | %-13s%s" % (agree, n, killed, f, m, flag))
    print()

src7 = (MUT / "T88M1-M7.py").read_text().split("\n")
cond7 = condition(src7, AGREE_HEAD)
print("M7 agreement: if %s:" % cond7)
print("  measured verdict / recorded | frozen agrees | M7 agrees")
for v, want in (("KILLED", "KILLED"), ("SURVIVED", "SURVIVED"), ("SURVIVED", "KILLED"),
                ("INCONCLUSIVE", "KILLED"), ("INCONCLUSIVE", "SURVIVED")):
    f = eval(frozen_agree, {}, {"v": v, "table": {"X": want}, "d": {"id": "X"}})
    m = eval(cond7, {}, {"v": v, "table": {"X": want}, "d": {"id": "X"}})
    flag = "  <-- differs" if f != m else ""
    print("  %-12s / %-10s | %-13s | %-13s%s" % (v, want, f, m, flag))
