#!/usr/bin/env bash
# T57W1ScribeKnowledge: lane-level evidence for gate-row-exit-map.md (read-only on the lane).
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=5e3569969b532310d2b8a3d130901757a3df356b
R=$LANE/.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts
cd "$LANE" || exit 9
echo "== gate sha256 at base bytes and in the lane tree"
git -C "$LANE" show "$BASE:tools/receipt-revision-gate.py" | sha256sum
sha256sum tools/receipt-revision-gate.py
echo "== staged accept row's command, run from the lane (fixture not yet installed at base)"
python3 tools/receipt-revision-gate.py --lane . --certified "$BASE" --receipt tools/fixtures/receipt-gate/accept.receipt:positive; echo "rc=$?"
echo "== selftest in the same tree"
python3 tools/receipt-revision-gate.py --selftest | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "== code coverage: codes the gate defines vs codes each registry row emits (staged rows)"
python3 - "$R/gate-sweep.stdout" <<'PY'
import re, sys
codes = set("""RECEIPT_MISSING RECEIPT_EMPTY RECEIPT_NOT_BLOB RECEIPT_REV_ABSENT RECEIPT_REV_AMBIGUOUS
RECEIPT_REV_UNRESOLVABLE RECEIPT_REV_MISMATCH RECEIPT_REV_CONTENT_DRIFT RECEIPT_CONTROL_NOT_ANCESTOR
RECEIPT_DIGEST_MISMATCH RECEIPT_REQUIRED_LINE_MISSING""".split())
seen = set(re.findall(r'RECEIPT_[A-Z_]+', open(sys.argv[1]).read()))
rows = {'receipt-gate-accept': set(), 'receipt-gate-content-drift': {'RECEIPT_REV_CONTENT_DRIFT'},
        'receipt-gate-unresolvable-certified': {'RECEIPT_REV_UNRESOLVABLE'}}
covered = set().union(*rows.values())
print('codes defined:', len(codes), '| emitted by the sweep:', len(seen & codes), '| not emitted by the sweep:', sorted(codes - seen))
print('codes emitted by a staged row:', len(covered), sorted(covered))
print('codes emitted by no registry row:', len(codes - covered), sorted(codes - covered))
PY
