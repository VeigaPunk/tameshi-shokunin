#!/usr/bin/env python3
"""Arm-level corroboration: apply the frozen counter's own GRAMMAR to the captured
streams of each mutant, so the table is the counter's predicate, not a re-invention."""
import importlib.util
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
MEASURE = ("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/"
           "c2/measure.py")
spec = importlib.util.spec_from_file_location("c2measure", MEASURE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

MODE = {
    "m-base": ["repeat-control --selftest"],
    "m-rc-revert": ["repeat-control --selftest"],
    "m-rc-drop-value": ["repeat-control --selftest"],
    "m-rc-drop-class": ["repeat-control --selftest"],
    "m-rc-drop-label": ["repeat-control --selftest"],
    "m-rc-stdout": ["repeat-control --selftest"],
    "m-rc-wrong-prefix": ["repeat-control --selftest"],
    "m-cc-revert": ["context-capture --selftest"],
    "m-cc-stdout": ["context-capture --selftest"],
}

rows = []
for branch, modes in MODE.items():
    out = open(os.path.join(S, "direct", branch + ".out"), encoding="utf-8").read()
    err = open(os.path.join(S, "direct", branch + ".err"), encoding="utf-8").read()
    row = {
        "branch": branch,
        "modes": modes,
        "stderr_lines": err.splitlines(),
        "stdout_first": out.splitlines()[:2],
        "grammar_on_stderr": any(m.GRAMMAR.match(l) for l in err.splitlines()),
        "runtimeerror_token": ("RuntimeError" in err + out),
        "traceback_token": ("Traceback" in err + out),
    }
    rows.append(row)
print(json.dumps(rows, indent=1))
