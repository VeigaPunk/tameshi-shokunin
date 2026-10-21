# B05 — Naive ISO timestamp receipt gate

## Axes and finding

- **Interval correctness:** the staged gate rejects a timezone-naive ISO-8601 value with `BAD_INTERVAL` (exit 1).
- **Window bindability:** a naive local date-time has no UTC offset/time zone, so it does not identify a unique instant. It cannot be ordered reliably against the contract's timezone-aware install-window bounds. The checker parses with `datetime.fromisoformat()` and returns `None` when `tzinfo is None`; `require_interval()` consequently requires both endpoints to be aware ISO-8601 values.
- **Scope preservation:** exercised only the assigned staged checker with a private `/tmp` receipt fixture; no lane production file was edited.

## Fixture

Created `/tmp/tameshi-r20-b05-naive.fYhl1p/receipts.json` with one receipt, id `B05-naive-timestamp`, declared instrument `receipt-window`, the contract's frozen/installed instrument SHA-256, and interval:

```json
{"start":"2026-10-21T08:00:00","end":"2026-10-21T08:00:01Z"}
```

The start is timezone-naive; the end is timezone-aware. The staged checker SHA-256 was checked first:

```text
$ sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py
f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py
```

## Gate command and observed output

```text
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py --contract /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/contract.json --receipts /tmp/tameshi-r20-b05-naive.fYhl1p/receipts.json --json
{"findings": [{"detail": "B05-naive-timestamp: measurement_interval start/end must be aware ISO-8601", "id": "BAD_INTERVAL", "receipt": "B05-naive-timestamp"}], "infos": [], "receipts": 1, "schema": "tameshi-receipt-window-v1", "verdict": "FAIL"}
EXIT_CODE=1
```

## Assessment

**Agree** with the gate's result: `BAD_INTERVAL` is the correct finding because one endpoint cannot be interpreted as an absolute instant and therefore the interval cannot bind to a contract time window. **Defects observed:** none in this assigned case. No installs or updates were performed.
