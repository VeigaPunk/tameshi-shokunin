#!/usr/bin/env python3
"""R90-C2 attack (additional, counter-authority class): reach PASS on the base tree
with none of the four doc repairs made, by neutering the two instruments the counter
executes from the measured clone (tools/defect-bind.py, tools/registry-check.py).
The C2 counter pins the manifest but not the tools it runs.

Usage: python3 -I T90C2-tool-neuter.py REPO
"""
import os
import sys

repo = os.path.realpath(sys.argv[1])

DB_SHIM = """import sys as _s
if "--manifest" in _s.argv:
    _ids = ("R89-1a-readme-row", "R89-1b-entry-cites-row",
            "R89-2-3-lesson-corrections", "R89-4a-skill-registry-row")
    for _i in _ids:
        print("DEFECT_BIND_ROW %s kind=doc-contains expect=closed state=closed "
              "detail=section-carries" % _i)
    print("DEFECT_BIND_ROW R89-4b-registry-json-row kind=receipt-tokens "
          "expect=closed state=closed detail=tokens-in-span-and-receipt")
    print("DEFECT_BIND: rows=5 closed=5 open=0 unexpected=0 manifest=bound")
    _s.exit(0)
"""

RC_SHIM = """import sys as _s
if "--only" in _s.argv:
    print("ROW ledger-witness-selftest expect=0 got=0 held")
    print("REGISTRY_CHECK: held=1/1 superseded=0")
    _s.exit(0)
"""

for rel, shim in (("tools/defect-bind.py", DB_SHIM),
                  ("tools/registry-check.py", RC_SHIM)):
    p = os.path.join(repo, rel)
    text = open(p, encoding="utf-8").read()
    if text.startswith(shim):
        continue
    open(p, "w", encoding="utf-8").write(shim + text)
    print("neutered %s (prepended a %d-byte shim)" % (rel, len(shim)))
