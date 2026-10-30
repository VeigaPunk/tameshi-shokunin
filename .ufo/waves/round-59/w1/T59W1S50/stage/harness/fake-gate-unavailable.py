#!/usr/bin/env python3
"""Fake gate: always-unavailable. Ignores all arguments, always refuses.

Seat T59W1S50 CLI integration probe: negative control that must NEVER earn
credit from the frozen 24-case counter. Expected: all 24 fixtures report
ok=false (wrong exit/token for the 8 pass classes and 8 drift classes;
only the 8 unresolvable cases match exit 2, but token emitted on stderr
must still differ in spirit -- it prints the same token so ok turns on the
exit code alone for unresolvable rows).
"""
import sys

print("EXECUTOR_SOURCE_UNAVAILABLE fake-gate=always-unavailable", file=sys.stderr)
sys.exit(2)
