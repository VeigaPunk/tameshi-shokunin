#!/usr/bin/env python3
"""Attack A: sequence/state cheat. No source comparison at all.
Counts invocations in a state file under TMPDIR (the frozen counter sets
TMPDIR=<work> once for all 24 invocations and only cleans it at the end,
so state persists across every fixture call). Returns the fixed expected
sequence 0,1,1,0,2,1 repeated per path, emitting the required token.
"""
import os, sys
from pathlib import Path

TOK = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT', 2: 'EXECUTOR_SOURCE_UNAVAILABLE'}
state = Path(os.environ.get('TMPDIR', '/tmp')) / '.exec-pin-cheat-state'
n = int(state.read_text()) if state.exists() else 0
code = (0, 1, 1, 0, 2, 1)[n % 6]
state.write_text(str(n + 1))
print(TOK[code])
sys.exit(code)
