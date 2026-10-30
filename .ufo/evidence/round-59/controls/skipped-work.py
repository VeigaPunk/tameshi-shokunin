#!/usr/bin/env python3
# Control: skips all work, reports the unavailable token with exit 0 (mismatched exit/token). Must fail.
import sys
print("EXECUTOR_SOURCE_UNAVAILABLE: skipped")
sys.exit(0)
