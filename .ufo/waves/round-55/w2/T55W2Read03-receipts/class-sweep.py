#!/usr/bin/env python3
"""Unusable-arm sweep over the seven self-tests named by Standing rules ("the
seven self-tests"), plus the two extra documented allocating modes.

For each mode: exit code, whether stderr matches the section's grammar, and how
many bytes the OTHER stream carries. Run from a C0 clone.
"""
import os
import pathlib
import re
import subprocess

CLONE = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W2Read03/clone")
TMP = "/nonexistent-r55-sweep"
GRAMMAR = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone "
    r"scratch under the scratch root: TMPDIR is not a usable directory: '.+' "
    r"\(could-not-evaluate\)$")
MODES = [
    ("repeat-control", ["python3", "tools/repeat-control.py", "--selftest"]),
    ("registry-check", ["python3", "tools/registry-check.py", "--selftest"]),
    ("bash-witness-study", ["python3", "tools/bash-witness-study.py", "selftest"]),
    ("pin-disposition", ["python3", "tools/pin-disposition.py", "--selftest"]),
    ("evidence-disposition", ["python3", "tools/evidence-disposition.py", "--selftest"]),
    ("context-capture", ["python3", "tools/context-capture.py", "--selftest"]),
    ("env-diff", ["python3", "tools/env-diff.py", "--selftest"]),
]
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env["TMPDIR"] = TMP
print("%-22s %-3s %-8s %-9s %s" % ("mode", "rc", "grammar", "stdout_b", "stdout first line"))
for name, argv in MODES:
    p = subprocess.run(argv, cwd=str(CLONE), env=env, capture_output=True, text=True, timeout=300)
    ok = any(GRAMMAR.match(l) for l in p.stderr.splitlines())
    first = (p.stdout.strip().splitlines() or [""])[0][:60]
    print("%-22s %-3s %-8s %-9s %s" % (name, p.returncode, "yes" if ok else "NO",
                                       len(p.stdout.encode()), repr(first)))
