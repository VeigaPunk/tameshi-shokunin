#!/usr/bin/env python3
"""Rejected-option fixture (NOT lane code): tools/scratch_root.py, shared by the seven.

Generates the module the item asks to cost out, so the costs are measured on
working code rather than asserted. Applies to a scratch clone at the R55 base.

Per tool: the `class ScratchRootUnusable` block (when present) and the whole
`strict_scratch_root()` body are replaced by one import. Nothing else changes,
so the handler shapes stay exactly as the base shipped them (which is the point:
a shared module does not by itself fix the three bare-raise handlers).

Line-based on purpose: a regex over these files backtracks for minutes.

Usage: make-module-fixture.py CLONE
"""
import sys
from pathlib import Path

TOOLS = ("env-diff", "repeat-control", "registry-check", "bash-witness-study",
         "pin-disposition", "evidence-disposition", "context-capture")

MODULE = '''"""Scratch root for the seven tameshi tools (rejected-option fixture).

Round 55 refused this module: the tools are copied as single files, loaded by
path, and surfaced as one git blob; a sibling import is not resolvable in any of
those paths. Reproduced here only to measure the cost.
"""
import os
import tempfile


class ScratchRootUnusable(RuntimeError):
    """A set-but-unusable TMPDIR: could-not-evaluate (exit 2), never a traceback."""


def strict_scratch_root():
    t = os.environ.get("TMPDIR")
    if t:
        if not os.path.isdir(t) or not os.access(t, os.W_OK):
            raise ScratchRootUnusable(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()
'''

IMPORT = ("# The seven tools share one definition (rejected-option fixture).\n"
          "from scratch_root import ScratchRootUnusable, strict_scratch_root\n")


def rewrite(lines):
    start = next(i for i, l in enumerate(lines) if l.startswith("def strict_scratch_root():"))
    end = next(i for i in range(start, len(lines))
               if lines[i].rstrip("\n") == "    return tempfile.gettempdir()")
    # The class block, when present, sits directly above with two blank lines.
    block = start
    if start >= 3 and lines[start - 3].startswith("class ScratchRootUnusable(RuntimeError):"):
        block = start - 3
    out = lines[:block] + [IMPORT] + lines[end + 1:]
    return out


root = Path(sys.argv[1])
(root / "tools/scratch_root.py").write_text(MODULE)
print("wrote tools/scratch_root.py (%d lines)" % MODULE.count("\n"))
for tool in TOOLS:
    p = root / ("tools/%s.py" % tool)
    lines = p.read_text().splitlines(keepends=True)
    before = len(lines)
    new = rewrite(lines)
    p.write_text("".join(new))
    print("%-22s %d -> %d lines" % (tool, before, len(new)))
