#!/usr/bin/env python3
"""Fake gate: always-accept. Ignores all arguments, always passes.

Seat T59W1S50 CLI integration probe: negative control that must NEVER earn
credit from the frozen 24-case counter. Expected: all 24 fixtures report
ok=false (wrong exit for 16 drift/unavailable classes, wrong token for the
8 pass classes).
"""
import sys

print("EXECUTOR_SOURCE_BOUND fake-gate=always-accept")
sys.exit(0)
