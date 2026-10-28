#!/usr/bin/env python3
"""Fixture transformer (NOT lane code): make the docs/note/skill arms conform in a
scratch clone so the C2 counter's own aggregation can be exercised at its best case.

Takes the clone root as argv[1]. Marker text is copied verbatim from the frozen
counter (measure.py MARKER) so the fixture cannot drift from what is measured.
"""
import json
import sys
from pathlib import Path

MARKER = "could-not-evaluate: cannot create clone scratch under the scratch root"
MODES = ("repeat-control --selftest", "registry-check --selftest",
         "bash-witness-study selftest", "pin-disposition --selftest",
         "evidence-disposition --selftest", "context-capture --selftest",
         "env-diff --selftest", "env-diff --contract", "registry-check --rev")
SEVEN = ("env-diff", "repeat-control", "registry-check", "bash-witness-study",
         "pin-disposition", "evidence-disposition", "context-capture")

root = Path(sys.argv[1])
reg_path = root / "tools/registry.json"
reg = json.loads(reg_path.read_text())
n = 0
for row in reg["rows"]:
    if not row.get("scratch_root"):
        continue
    if not any("tools/%s.py" % t in " ".join(row.get("argv", [])) for t in SEVEN):
        continue
    row["scratch_root"] = (
        "TMPDIR set but unusable => exit 2, one stderr line "
        "\"<tool>: %s: TMPDIR is not a usable directory: '<value>' "
        "(could-not-evaluate)\"; TMPDIR empty => unset, the platform default applies"
        % MARKER)
    n += 1
reg_path.write_text(json.dumps(reg, indent=1) + "\n")

note = root / "corpus/knowledge/scratch-root-contract.md"
note.write_text(note.read_text() + "\n\n## One line (fixture)\n\n"
                "%s: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)\n\n"
                "Allocating modes: %s.\n" % (MARKER, "; ".join(MODES)))

skill = root / "SKILL.md"
skill.write_text(skill.read_text() + "\n\n%s: TMPDIR is not a usable directory: "
                 "'<value>' (could-not-evaluate)\n" % MARKER)

print("cells rewritten:", n)
