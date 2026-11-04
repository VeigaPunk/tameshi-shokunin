#!/usr/bin/env python3
"""Adversarial counter control: no git reads and no receipt parsing."""
import sys
name = sys.argv[sys.argv.index('--root') + 1]
if name not in ('carried', 'different', 'absent', 'symlink'):
    sys.exit(2)
state = {'carried': 'carried', 'different': 'different', 'absent': 'absent', 'symlink': 'nonregular'}[name]
# Deliberately no DESIGN_BLOB_ROW and no well-formed complete summary line.
print('FORGED state=' + state + ' DESIGN_BLOB: receipts=1 carried=' + ('1 orphan=0' if name == 'carried' else '0 orphan=1') + ' INVALID_SUFFIX')
sys.exit(0 if name == 'carried' else 1)
