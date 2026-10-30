#!/usr/bin/env python3
"""Control: always-accept tool. Prints BOUND and exits 0 for every cell.
Certification requires C1_R60_PASS=false for this control."""
import sys

print("EXECUTOR_SOURCE_BOUND: control always accepts")
sys.exit(0)
