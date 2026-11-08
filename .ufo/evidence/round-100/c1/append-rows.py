#!/usr/bin/env python3
"""Round 100 C1: append the twelve r100-c1 rows to tools/registry.json (append-only; existing
rows byte-identical — asserted). Run from the lane root: python3 -I .ufo/evidence/round-100/c1/append-rows.py"""
import json, sys
P = "tools/registry.json"
raw = open(P, encoding="utf-8").read()
d = json.loads(raw)
assert json.dumps(d, indent=1, ensure_ascii=False) + "\n" == raw, "registry does not round-trip"
R99 = "808a43778701cf1b05762584954d435481dc6fa2"
SRC = "SCORECARD.md@34d8d7cef87ec78ed84bf5247e2609814cce74c8:5933"
TAGS = ["r100-c1"]
def row(name, kind, argv, rc, needles, timeout=300):
    return {"name": name, "kind": kind, "argv": ["python3", "-I"] + argv,
            "expect": {"exit": rc, "stdout_contains": needles}, "timeout_s": timeout,
            "source": SRC, "status": "active", "tags": TAGS}
new = [
    row("tally-reconcile-selftest", "selftest", ["tools/tally-reconcile.py", "--selftest"], 0,
        ["TALLY_RECONCILE_SELFTEST: 25/25 pass"]),
    row("tally-reconcile-red-r94", "gate", ["tools/tally-reconcile.py", "--repo", ".", "--rev", R99,
        "--record", "corpus/lessons/round-94.md"], 1,
        ["TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0"]),
    row("tally-reconcile-green-r93", "gate", ["tools/tally-reconcile.py", "--repo", ".", "--rev", R99,
        "--record", "corpus/lessons/round-93.md"], 0,
        ["TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=1 mismatched=0 unbound=0 uncited=0"]),
    row("control-assert-v2-selftest", "selftest", ["tools/control-assertion-audit-v2.py", "--selftest"], 0,
        ["CONTROL_ASSERT_V2_SELFTEST: 38/38 pass"]),
    row("control-assert-v2-red-alias", "gate", ["tools/control-assertion-audit-v2.py", "--repo", ".", "--rev", R99,
        "--driver", ".ufo/evidence/round-99/c2/alias-driver.py"], 1,
        ["CONTROL_ASSERT_RECORDERS aliases=1 ambiguous=0 partial=0 names=add,record",
         "CONTROL_ASSERT sites=4 measured=3 literal=1 unmeasured=1"]),
    row("control-assert-v2-green-controls98", "gate", ["tools/control-assertion-audit-v2.py", "--repo", ".",
        "--rev", R99, "--driver", ".ufo/evidence/round-98/controls98.py"], 0,
        ["CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0"]),
    row("control-assert-selftest", "selftest", ["tools/control-assertion-audit.py", "--selftest"], 0,
        ["CONTROL_ASSERT_SELFTEST: 18/18 pass"]),
    row("control-assert-red-controls97", "gate", ["tools/control-assertion-audit.py", "--repo", ".", "--rev", R99,
        "--driver", ".ufo/evidence/round-97/controls97.py"], 1,
        ["CONTROL_ASSERT sites=15 measured=14 literal=1 unmeasured=1"]),
    row("control-assert-green-controls98", "gate", ["tools/control-assertion-audit.py", "--repo", ".", "--rev", R99,
        "--driver", ".ufo/evidence/round-98/controls98.py"], 0,
        ["CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0"]),
    row("registry-cell-immutability-selftest", "selftest", ["tools/registry-cell-immutability.py", "--selftest"], 0,
        ["REGISTRY_IMMUTABLE_SELFTEST: 10/10 pass"]),
    row("registry-cell-immutability-red-r97", "gate", ["tools/registry-cell-immutability.py", "--repo", ".",
        "--from", "0b19af5f8666f9c54a437f511e9155a66d0d418d", "--to", "29734beb095984038d66bb5dd4d149d81378de31"], 1,
        ["REGISTRY_CELL S006:anchor changed", "REGISTRY_CELL S159:anchor changed",
         "REGISTRY_IMMUTABLE from=0b19af5f8666 to=29734beb0959 shared=183 changed=2 removed=0 added=0"]),
    row("registry-cell-immutability-green-r98", "gate", ["tools/registry-cell-immutability.py", "--repo", ".",
        "--from", "29734beb095984038d66bb5dd4d149d81378de31", "--to", "3b7ae1272d161aa0297e1d04b2b7ec5b40112912"], 0,
        ["REGISTRY_IMMUTABLE from=29734beb0959 to=3b7ae1272d16 shared=183 changed=0 removed=0 added=0"]),
]
names = set(r["name"] for r in d["rows"])
clash = [r["name"] for r in new if r["name"] in names]
if clash:
    sys.exit("name clash: %s" % clash)
d["rows"].extend(new)
out = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
assert out.startswith(raw[: raw.rfind("\n ]")]), "existing bytes changed"
open(P, "w", encoding="utf-8").write(out)
print("APPENDED rows=%d total=%d" % (len(new), len(d["rows"])))
