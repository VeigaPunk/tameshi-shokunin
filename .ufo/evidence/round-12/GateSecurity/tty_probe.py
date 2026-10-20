#!/usr/bin/env python3
"""GateSecurity r12 P15: stdin=DEVNULL does not stop a child reading the controlling tty.
Run under a pty (interactive gate use). Each case is bounded by timeout=3."""
import subprocess
import sys
import time

CHILD = ["sh", "-c", "if read x </dev/tty; then echo got; else echo tty-unavailable; fi"]
for label, kw in (("inherit-session", {}), ("start_new_session", {"start_new_session": True})):
    t0 = time.monotonic()
    try:
        p = subprocess.run(CHILD, stdin=subprocess.DEVNULL, capture_output=True, timeout=3, **kw)
        res = f"exit={p.returncode} stdout={p.stdout!r}"
    except subprocess.TimeoutExpired:
        res = "BLOCKED on /dev/tty until timeout"
    print(f"PROBE P15 {label}: {res} after {time.monotonic()-t0:.1f}s", flush=True)
print(f"PROBE P15 stdin_isatty={sys.stdin.isatty()}")
