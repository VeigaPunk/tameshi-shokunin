#!/usr/bin/env python3
"""Replay the C2 counter's tmp_mkdirs arm verbatim against an arbitrary clone.

The arm block is sliced byte-exactly out of measure.py (start '    tmp_mkdirs = 0',
end '    docs = 0'), dedented and exec'd with the names measure.py itself binds.
measure.py is imported as a module for its helpers (run_tool, TIMEOUT, TOOLS), so
the replay tracks the counter's own definitions instead of paraphrasing them.

Usage: arm_replay.py MEASURE CLONE WORK NAME PATH ARG [REGEX]
  REGEX  optional replacement for the arm's detection pattern
"""
import importlib.util
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

MEASURE, CLONE, WORK, NAME, PATH, ARG = sys.argv[1:7]
PATCH = sys.argv[7] if len(sys.argv) > 7 else None

spec = importlib.util.spec_from_file_location('c2_measure', MEASURE)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

src = open(MEASURE, encoding='utf-8').read()
arm = textwrap.dedent(src[src.index('    tmp_mkdirs = 0'):src.index('    docs = 0')])
print('---- measure.py sha256 %s ----'
      % __import__('hashlib').sha256(src.encode()).hexdigest())
print('---- arm block replayed (verbatim slice) ----')
print(arm, end='')
print('---- end arm block ----')
if PATCH:
    i = arm.index("re.findall(r'") + len("re.findall(r'")
    j = arm.index("',", i)
    print('---- original regex: %s' % arm[i:j])
    arm = arm[:i] + PATCH.replace(chr(92) + chr(92), chr(92)) + arm[j:]
    print('---- arm regex patched to: %s ----' % PATCH.replace(chr(92) + chr(92), chr(92)))


class Args:
    explain = True


a = Args()
work = Path(WORK)
work.mkdir(parents=True, exist_ok=True)
usable = work / 'usable-tmpdir'
usable.mkdir()
clone = Path(CLONE)
TOOLS = [(NAME, PATH, ARG, '_')]
notes = []
usable_ok = 0
g = dict(os=os, re=re, subprocess=subprocess, sys=sys, Path=Path, TOOLS=TOOLS, work=work,
         usable=usable, clone=clone, a=a, notes=notes, usable_ok=usable_ok,
         TIMEOUT=M.TIMEOUT, run_tool=M.run_tool)
exec(compile(arm, '<arm-slice>', 'exec'), g)
log = work / ('strace-%s.log' % NAME)
print('REPLAY hits=%d usable_ok=%d log_lines=%d notes=%r'
      % (g['tmp_mkdirs'], g['usable_ok'],
         len(log.read_text(errors='replace').splitlines()), g['notes']))
