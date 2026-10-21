# ReceiptFields — round 19 / wave 1

## Scope and axes

- **C1 / calibration:** this seat contributes only receipt-integrity evidence for routed defect R18-4. It does not claim a calibration-score increase, promotion, or independent closure of the five-item population.
- **Receipt integrity:** validate the corrected selftest record's exact JSON key set and types, nonempty/expected argv, explicit revision, exit, and stdout/stderr SHA-256 against the referenced bytes.
- **No-harm boundary:** read-only against the repository; only the requested report was written in-tree. The investigation script and its probes are in unique `/tmp/tameshi-r19-ReceiptFields-a0Jc6L/`. No installs, selftests, builds, linters, formatters, external commands from the receipt, or production edits.

## Sources and observed evidence

Read on 2026-10-21:

1. `corpus/lessons/round-18-verifier-spotcheck.md` §5, defect 4, says the old final receipt has an argv exit of 64 and empty stdout, and directs: “Do not leave a failed invocation as the selftest row of the final receipt bundle.” Defect 5 says “no receipt names `4b7c682`.”
2. `.ufo/evidence/round-18/final/checks.json`, `bash-witness-selftest` record: argv ends in `--selftest`, revision `921ef8077440f90d092aab4b9fdc750a45de1224`, exit `64`, and stdout SHA-256 is the empty-byte digest `e3b0c442…b855`. The record has no stderr path/hash fields. The matching `bash-witness-selftest.stdout` is empty; `.stderr` contains the argparse usage error that `mode` is required.
3. `.ufo/evidence/round-19/bash-witness-selftest-complete.json`: corrected argv is `python3 tools/bash-witness-study.py selftest`; revision is `4b7c6823a462f5ea2eafcb262275300a545f3ed7`; exit is `0`; both output paths and SHA-256 fields are present. It also has `tool_sha256`, `runner_sha256`, `cwd_kind`, `recorded_at`, `supersedes`, and `historical_receipt_preserved`.
4. The corrected receipt points to `.ufo/evidence/round-19/bash-witness-selftest-complete.stdout` and `.stderr`. The bounded probe read those bytes and recomputed both digests. The stdout contains `WITNESS_SELFTEST: 43/43 pass` and `VERDICT: PASS`; stderr is empty.
5. `.ufo/evidence/round-19/contract.json` records the frozen baseline and R18 defect population. `.ufo/evidence/round-19/after-21e7932.json` records the corrected receipt, stdout, and stderr as inputs; its receipt input digest is `1939f9f48a85ceb4d4087ce89abfe7c65c4cfb1b43a16e6ad35f86a5d46b9809`.

## Bounded investigation

Code: `/tmp/tameshi-r19-ReceiptFields-a0Jc6L/receipt_fields.py`. It reads only the named receipt and its referenced output bytes (each capped at 1,000,000 bytes), never executes the recorded argv, and applies three in-memory negative mutations. Command, from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

```text
python3 /tmp/tameshi-r19-ReceiptFields-a0Jc6L/receipt_fields.py
```

Observed output:

```text
PASS corrected receipt: exact keys/types, nonempty argv, pinned revision, stdout/stderr SHA-256
OBSERVED revision=4b7c6823a462f5ea2eafcb262275300a545f3ed7 exit=0 argv_items=3
OBSERVED stdout_sha256=316b97139aaa2fafa1ab08c2df6471ba8dec5b4480efa1a9589ae0341e5020be
OBSERVED stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
REJECT bool-as-int: exit-not-int
REJECT empty-argv: argv-empty
REJECT mismatched-revision: revision-mismatch
```

Full investigation code:

```python
#!/usr/bin/env python3
"""Read-only shape/type and byte-digest probe for the corrected R18-4 receipt."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin").resolve()
RECEIPT = ROOT / ".ufo/evidence/round-19/bash-witness-selftest-complete.json"
EXPECTED_REVISION = "4b7c6823a462f5ea2eafcb262275300a545f3ed7"
EXPECTED_ARGV = ["python3", "tools/bash-witness-study.py", "selftest"]
KEYS = {
    "argv", "revision", "tool_sha256", "cwd_kind", "exit",
    "stdout_sha256", "stderr_sha256", "stdout", "stderr", "recorded_at",
    "supersedes", "historical_receipt_preserved", "runner_sha256",
}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
REVISION = re.compile(r"[0-9a-f]{40}\Z")
MAX_BYTES = 1_000_000


class ReceiptError(ValueError):
    pass


def reject(reason: str) -> None:
    raise ReceiptError(reason)


def safe_output(root: Path, name: Any) -> bytes:
    if type(name) is not str or not name:
        reject("output-path-type-or-empty")
    relative = Path(name)
    if relative.is_absolute():
        reject("output-path-absolute")
    path = (root / relative).resolve(strict=True)
    try:
        path.relative_to(root)
    except ValueError:
        reject("output-path-escapes-root")
    if not path.is_file():
        reject("output-not-file")
    if path.stat().st_size > MAX_BYTES:
        reject("output-too-large")
    return path.read_bytes()


def validate(record: Any, expected_revision: str, root: Path) -> None:
    if type(record) is not dict:
        reject("receipt-not-object")
    if set(record) != KEYS:
        reject("receipt-key-set-mismatch")

    argv = record["argv"]
    if type(argv) is not list:
        reject("argv-not-list")
    if not argv:
        reject("argv-empty")
    if any(type(arg) is not str or not arg for arg in argv):
        reject("argv-element-not-nonempty-string")
    if argv != EXPECTED_ARGV:
        reject("argv-mismatch")

    revision = record["revision"]
    if type(revision) is not str or REVISION.fullmatch(revision) is None:
        reject("revision-format")
    if revision != expected_revision:
        reject("revision-mismatch")

    for key in ("tool_sha256", "stdout_sha256", "stderr_sha256", "runner_sha256"):
        if type(record[key]) is not str or SHA256.fullmatch(record[key]) is None:
            reject(f"{key}-format")
    if type(record["cwd_kind"]) is not str or not record["cwd_kind"]:
        reject("cwd-kind-type-or-empty")
    if type(record["exit"]) is not int:
        reject("exit-not-int")
    if record["exit"] != 0:
        reject("exit-not-zero")
    if type(record["recorded_at"]) is not str or not record["recorded_at"]:
        reject("recorded-at-type-or-empty")
    if type(record["supersedes"]) is not list or not record["supersedes"]:
        reject("supersedes-not-nonempty-list")
    if any(type(item) is not str or not item for item in record["supersedes"]):
        reject("supersedes-element-not-nonempty-string")
    if type(record["historical_receipt_preserved"]) is not bool:
        reject("historical-preserved-not-bool")
    if record["historical_receipt_preserved"] is not True:
        reject("historical-receipt-not-preserved")

    stdout = safe_output(root, record["stdout"])
    stderr = safe_output(root, record["stderr"])
    if hashlib.sha256(stdout).hexdigest() != record["stdout_sha256"]:
        reject("stdout-digest-mismatch")
    if hashlib.sha256(stderr).hexdigest() != record["stderr_sha256"]:
        reject("stderr-digest-mismatch")


def main() -> None:
    if RECEIPT.stat().st_size > MAX_BYTES:
        reject("receipt-too-large")
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    validate(receipt, EXPECTED_REVISION, ROOT)
    print("PASS corrected receipt: exact keys/types, nonempty argv, pinned revision, stdout/stderr SHA-256")
    print(f"OBSERVED revision={receipt['revision']} exit={receipt['exit']} argv_items={len(receipt['argv'])}")
    print(f"OBSERVED stdout_sha256={receipt['stdout_sha256']}")
    print(f"OBSERVED stderr_sha256={receipt['stderr_sha256']}")

    probes = (
        ("bool-as-int", lambda item: item.__setitem__("exit", True), "exit-not-int"),
        ("empty-argv", lambda item: item.__setitem__("argv", []), "argv-empty"),
        ("mismatched-revision", lambda item: item.__setitem__("revision", "0" * 40), "revision-mismatch"),
    )
    for label, mutate, expected_reason in probes:
        candidate = copy.deepcopy(receipt)
        mutate(candidate)
        try:
            validate(candidate, EXPECTED_REVISION, ROOT)
        except ReceiptError as error:
            if str(error) != expected_reason:
                raise
            print(f"REJECT {label}: {error}")
        else:
            raise RuntimeError(f"negative probe unexpectedly accepted: {label}")


if __name__ == "__main__":
    main()
```

## Limits and handoff

- The strict schema is derived from this corrected receipt and its use; it intentionally rejects extra/missing keys and argv variants. If L1 adopts a different receipt schema or argv, re-derive rather than weakening checks by inference.
- `tool_sha256` and `runner_sha256` are checked for lowercase SHA-256 shape only; this probe does not resolve them to source bytes, validate the `recorded_at` timestamp syntax, prove revision ancestry, or establish receipt execution provenance. Stream digests are independently recomputed from the referenced bytes.
- No blocker for this bounded receipt-shape/digest investigation. The code's three negative outcomes are synthetic in-memory cases, not edits to retained evidence.
