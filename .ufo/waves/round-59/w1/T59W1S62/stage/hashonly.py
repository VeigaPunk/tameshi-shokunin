#!/usr/bin/env python3
"""Attack C: revision-hash-only discrimination, zero repo access.
candidate==trusted -> 0 ; all-zeros -> 2 ; else 1.
Bounds what pure hash syntax can achieve."""
import sys

argv = sys.argv[1:]
trusted = argv[argv.index('--trusted') + 1]
cand = argv[argv.index('--candidate') + 1]
if cand == trusted:
    print('EXECUTOR_SOURCE_BOUND')
    sys.exit(0)
if cand == '0' * 40:
    print('EXECUTOR_SOURCE_UNAVAILABLE')
    sys.exit(2)
print('EXECUTOR_SOURCE_DRIFT')
sys.exit(1)
