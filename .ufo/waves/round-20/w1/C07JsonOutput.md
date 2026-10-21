# C07 JSON gate output

## Scope and setup

Ran the byte-identical staged `receipt-window.py` copied with the frozen contract into a private `/tmp` sandbox. No lane production file was run or modified. Clean fixture: six valid, unique receipts (the two current identity instruments plus all four classified historical shas). Failing fixture: same six rows except `history-witness-runner` uses an unrecognized sha.

Observed SHA-256:

```text
f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  staged and sandbox receipt-window.py
9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715  staged and sandbox contract.json
```

## Commands

```sh
python3 /tmp/tameshi-r20-c07-json.lnG789/receipt-window.py --contract /tmp/tameshi-r20-c07-json.lnG789/contract.json --receipts /tmp/tameshi-r20-c07-json.lnG789/clean.json --json
python3 /tmp/tameshi-r20-c07-json.lnG789/receipt-window.py --contract /tmp/tameshi-r20-c07-json.lnG789/contract.json --receipts /tmp/tameshi-r20-c07-json.lnG789/failing.json --json
python3 /tmp/tameshi-r20-c07-json.lnG789/receipt-window.py --contract /tmp/tameshi-r20-c07-json.lnG789/contract.json --receipts /tmp/tameshi-r20-c07-json.lnG789/clean.json
python3 /tmp/tameshi-r20-c07-json.lnG789/receipt-window.py --contract /tmp/tameshi-r20-c07-json.lnG789/contract.json --receipts /tmp/tameshi-r20-c07-json.lnG789/failing.json
```

## Observed JSON results

Schema id for both results: `tameshi-receipt-window-v1`. Observed verdict values: `CLEAN` and `FAIL`. Each reports `receipts: 6`.

Clean (`--json`), exit 0:

```json
{"findings": [], "infos": [{"detail": "classified round18-measure", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-round18-measure"}, {"detail": "classified round19-ruler-wave1", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-round19"}, {"detail": "classified witness-runner", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-witness-runner"}, {"detail": "classified witness-tool", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-witness-tool"}, {"detail": "receipt-window: frozen and installed bytes are identical", "id": "INSTALL_IDENTITY", "receipt": "receipt-window-current"}, {"detail": "round20-measure: frozen and installed bytes are identical", "id": "INSTALL_IDENTITY", "receipt": "round20-measure-current"}], "receipts": 6, "schema": "tameshi-receipt-window-v1", "verdict": "CLEAN"}
```

Failing (`--json`), exit 1:

```json
{"findings": [{"detail": "instrument_sha256 is neither frozen, installed, nor historical", "id": "UNKNOWN_INSTRUMENT", "receipt": "history-witness-runner"}], "infos": [{"detail": "classified round18-measure", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-round18-measure"}, {"detail": "classified round19-ruler-wave1", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-round19"}, {"detail": "classified witness-tool", "id": "HISTORICAL_INSTRUMENT", "receipt": "history-witness-tool"}, {"detail": "receipt-window: frozen and installed bytes are identical", "id": "INSTALL_IDENTITY", "receipt": "receipt-window-current"}, {"detail": "round20-measure: frozen and installed bytes are identical", "id": "INSTALL_IDENTITY", "receipt": "round20-measure-current"}], "receipts": 6, "schema": "tameshi-receipt-window-v1", "verdict": "FAIL"}
```

## Text mode and agreement

Clean text output, exit 0:

```text
RECEIPT_WINDOW: CLEAN (receipts=6 historical=4)
RECEIPT_WINDOW info=HISTORICAL_INSTRUMENT receipt=history-round18-measure classified round18-measure
RECEIPT_WINDOW info=HISTORICAL_INSTRUMENT receipt=history-round19 classified round19-ruler-wave1
RECEIPT_WINDOW info=HISTORICAL_INSTRUMENT receipt=history-witness-runner classified witness-runner
RECEIPT_WINDOW info=HISTORICAL_INSTRUMENT receipt=history-witness-tool classified witness-tool
RECEIPT_WINDOW info=INSTALL_IDENTITY receipt=receipt-window-current receipt-window: frozen and installed bytes are identical
RECEIPT_WINDOW info=INSTALL_IDENTITY receipt=round20-measure-current round20-measure: frozen and installed bytes are identical
```

Failing text output, exit 1:

```text
RECEIPT_WINDOW: FAIL (findings=1 receipts=6)
RECEIPT_WINDOW finding=UNKNOWN_INSTRUMENT receipt=history-witness-runner instrument_sha256 is neither frozen, installed, nor historical
```

Agree: JSON and text modes return matching exit codes for both fixtures (0 for clean, 1 for findings). JSON contains the same clean/fail classification and finding/info content expressed by text mode. No defect observed in this scoped check. Could-not-evaluate output/exit behavior was not exercised.
