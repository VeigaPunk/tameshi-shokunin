#!/usr/bin/env python3
"""Does the frozen C2 grammar line conform to GNU Coding Standards §4.4?

Read-only: the frozen regex is re-derived from .ufo/evidence/round-55/c2/measure.py
and recompiled here; nothing is written to the lane. Run from anywhere.
"""
import pathlib
import re

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin")
SRC = (LANE / ".ufo/evidence/round-55/c2/measure.py").read_text()
BLOCK = SRC.split("GRAMMAR = re.compile(", 1)[1].split(")\n", 1)[0]
PARTS = re.findall(r'r"([^"]*)"', BLOCK)
GRAMMAR = re.compile("".join(PARTS))
TOOLS = ("env-diff", "repeat-control", "registry-check", "bash-witness-study",
         "pin-disposition", "evidence-disposition", "context-capture")
MSG = ("could-not-evaluate: cannot create clone scratch under the scratch root: "
       "TMPDIR is not a usable directory: '/nonexistent/r55' (could-not-evaluate)")


def gnu_shape(line: str) -> dict:
    """GNU §4.4: `program: message`; message not capitalised, no final period."""
    head, sep, body = line.partition(": ")
    return {
        "one_line": "\n" not in line,
        "program_colon_message": bool(head) and bool(sep),
        "message_lowercase": bool(body) and body[0].islower(),
        "no_trailing_period": not body.endswith("."),
    }


print("grammar re-derived from measure.py:", "".join(PARTS))
bad = 0
for tool in TOOLS:
    line = f"{tool}.py: {MSG}"
    shape = gnu_shape(line)
    ok = bool(GRAMMAR.fullmatch(line)) and all(shape.values())
    bad += not ok
    print(f"{'OK ' if ok else 'FAIL'} {tool}.py  grammar={bool(GRAMMAR.fullmatch(line))} "
          f"{shape}")

note = (LANE / "corpus/knowledge/scratch-root-contract.md").read_text()
doc = [l.strip() for l in note.splitlines() if l.strip().startswith("<tool>: ")]
print("note line:", doc[0] if doc else "ABSENT")
if doc:
    substituted = doc[0].replace("<tool>", "repeat-control.py")
    print("note line matches frozen grammar after substituting <tool>:",
          bool(GRAMMAR.fullmatch(substituted)))

for label, line in (("negative: capitalised message",
                     "repeat-control.py: Could-not-evaluate: x (could-not-evaluate)"),
                    ("negative: trailing period",
                     "repeat-control.py: could-not-evaluate: x (could-not-evaluate).")):
    shape = gnu_shape(line)
    print(f"{label}: {shape}")

print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
