#!/usr/bin/env python3
"""Round-19 ledger selection over the unchanged round-18 input-keyed ruler.

This selects a new default ledger, not an override/legacy trace mode. All
credit, trace, veto and CLI rules remain the frozen round-18 implementation.
Historical ledgers and implementation bytes are never rewritten.
"""
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location(
    'tameshi_round18_measure', ROOT / '.ufo/evidence/round-18/measure.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
LEDGER = '.ufo/evidence/round-19/coldread/ledger.json'
module.DEFAULT_LEDGER_PATH = LEDGER
module.LEDGER_PATH = LEDGER
module.BOX3_LINK = LEDGER
module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))

if __name__ == '__main__':
    sys.exit(module.main())
