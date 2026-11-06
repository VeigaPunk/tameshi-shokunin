#!/usr/bin/env python3
"""R90-C2 attack: keep the routed docs honest and replace the registry row's argv
with a one-liner that prints the row's expected needle. The registry row keeps its
name, kind, source (`tools/ledger-witness.py@ff7a4b06:1-60`) and expect block, so
the row still claims provenance from the witness while executing nothing of it.

Usage: python3 -I T90C2-forge-registry.py REPO
"""
import json
import os
import sys

repo = os.path.realpath(sys.argv[1])
rp = os.path.join(repo, "tools/registry.json")
reg = json.load(open(rp, encoding="utf-8"))
rows = [r for r in reg["rows"] if r.get("name") == "ledger-witness-selftest"]
assert len(rows) == 1, rows
row = rows[0]
assert row["argv"] == ["python3", "-I", "tools/ledger-witness.py", "--selftest"], row
row["argv"] = ["python3", "-I", "-c",
               "print('LEDGER_WITNESS_SELFTEST: 21/21 pass')"]
with open(rp, "w", encoding="utf-8") as f:
    f.write(json.dumps(reg, indent=1, ensure_ascii=True) + "\n")
print("forged registry row name=%s kind=%s source=%s argv=%r"
      % (row["name"], row["kind"], row["source"], row["argv"]))
