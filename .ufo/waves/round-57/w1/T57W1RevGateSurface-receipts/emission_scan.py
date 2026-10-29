#!/usr/bin/env python3
# Scan the gate source for emission sites of each CODES entry. Read-only.
import sys
path = sys.argv[1]
src = open(path, encoding='utf-8').read().splitlines()
codes = ['RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',
         'RECEIPT_REV_AMBIGUOUS', 'RECEIPT_REV_UNRESOLVABLE', 'RECEIPT_REV_MISMATCH',
         'RECEIPT_REV_CONTENT_DRIFT', 'RECEIPT_CONTROL_NOT_ANCESTOR',
         'RECEIPT_DIGEST_MISMATCH', 'RECEIPT_REQUIRED_LINE_MISSING']
SELFTEST_START = next(i + 1 for i, l in enumerate(src) if l.startswith('def selftest'))
TUPLE_LO, TUPLE_HI = 45, 50  # CODES = ( ... ) block, 1-based
print('source=%s lines=%d selftest_starts=%d' % (path, len(src), SELFTEST_START))
for c in codes:
    emit, tup, doc, st = [], [], [], []
    for n, l in enumerate(src, 1):
        if c not in l:
            continue
        if TUPLE_LO <= n <= TUPLE_HI:
            tup.append(n)
        elif n < 34:
            doc.append(n)
        elif n >= SELFTEST_START:
            st.append(n)
        else:
            emit.append(n)
    print('%-30s emit=%s tuple=%s docstring=%s selftest=%s' % (c, emit, tup, doc, st))
