# Gate selftest at C0

**Revision:** `c0137451f5b7f22d65f748fc69f1b181f55e1378`  
**Source:** `tools/receipt-revision-gate.py` archived from the C0 tree into an isolated scratch directory, then run with Python 3.14.8. No tools installed or updated.

## Normal selftest

Command: `python3 <scratch-C0-copy>/tools/receipt-revision-gate.py --selftest`

Verbatim output:

```text
CASE matched-positive-accepted PASS
CASE content-identical-positive-accepted PASS
CASE content-drift-refused PASS
CASE strict-mismatch-refused PASS
CASE absent-refused PASS
CASE ambiguous-refused PASS
CASE unresolvable-refused PASS
CASE control-ancestors-accepted PASS
CASE control-not-ancestor-refused PASS
CASE digest-mismatch-refused PASS
CASE required-line-refused PASS
CASE missing-refused PASS
CASE empty-refused PASS
CASE codes-closed PASS
CASE not-blob-refused PASS
CASE json-rev-parsed PASS
CASE unknown-role-refused PASS
CASE zero-receipts-refused PASS
CASE unresolvable-certified-refused PASS
GATE_SELFTEST: 19/19 pass

SELFTEST_EXIT=0
```

## Set-but-unusable TMPDIR

Set `TMPDIR` to an existing regular file and ran the same command on the same C0 copy.

Verbatim output:

```text
CASE matched-positive-accepted PASS
CASE content-identical-positive-accepted PASS
CASE content-drift-refused PASS
CASE strict-mismatch-refused PASS
CASE absent-refused PASS
CASE ambiguous-refused PASS
CASE unresolvable-refused PASS
CASE control-ancestors-accepted PASS
CASE control-not-ancestor-refused PASS
CASE digest-mismatch-refused PASS
CASE required-line-refused PASS
CASE missing-refused PASS
CASE empty-refused PASS
CASE codes-closed PASS
CASE not-blob-refused PASS
CASE json-rev-parsed PASS
CASE unknown-role-refused PASS
CASE zero-receipts-refused PASS
CASE unresolvable-certified-refused PASS
GATE_SELFTEST: 19/19 pass

BAD_TMP_EXIT=0
```

**Finding:** A set-but-unusable `TMPDIR` did not cause a scratch-root refusal or crash: selftest still passed. Python's `tempfile.TemporaryDirectory` fell back from the unusable TMPDIR to an available temporary root. This is acceptable for this reader-run tool: the unusable environment variable did not prevent the selftest from completing, and no misleading pass or unhandled error occurred.
