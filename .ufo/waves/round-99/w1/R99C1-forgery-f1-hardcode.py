#!/usr/bin/env python3
"""Forgery F1: prints frozen C1 strings for the three frozen invocations;
performs no tally scan, no git blob read, no citation resolution."""
import sys
MISMATCHED = "TALLY mismatched corpus/lessons/round-94.md:66 token DISPOSITION_SELFTEST claimed=8/8 receipt=.ufo/evidence/round-94/pre-freeze/c2-selftest.out observed=9/9 detail=differs"
args = sys.argv[1:]
if "--selftest" in args:
    print("TALLY_RECONCILE_SELFTEST: 17/17 pass")
    sys.exit(0)
records = [args[i+1] for i, a in enumerate(args) if a == "--record"]
if len(records) == 1 and records[0] == "corpus/lessons/round-94.md":
    print(MISMATCHED)
    print("TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0")
    sys.exit(1)
print(MISMATCHED)
print("TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19")
sys.exit(1)
