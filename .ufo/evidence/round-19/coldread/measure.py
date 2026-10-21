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
sys.dont_write_bytecode = True
spec.loader.exec_module(module)
LEDGER = '.ufo/evidence/round-19/coldread/ledger.json'
OLD_LEDGER = module.DEFAULT_LEDGER_PATH
module.DEFAULT_LEDGER_PATH = LEDGER
module.LEDGER_PATH = LEDGER
module.BOX3_LINK = LEDGER
module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))
# The inherited suite starts child CLI processes and has import-time fixture
# links. Exercise this selector, not the historical CLI with mismatched data.
if '--selftest' in sys.argv[1:]:
    module.__file__ = str(Path(__file__).resolve())
    for name in ('SHONEN_BOX3', 'SHONEN_TEXT', 'SHONEN_NOLINK_TEXT',
                 'SHONEN_CONT_TEXT', 'SHONEN_WRONGBOX_TEXT', 'SHONEN_OLDLINK_TEXT'):
        setattr(module, name, getattr(module, name).replace(OLD_LEDGER, LEDGER))

if __name__ == '__main__':
    sys.exit(module.main())
