# B10 — Historical round-19 ruler receipt gate

## Findings

- **Axes:** classification correctness; scoped evidence integrity; requested gate completion.
- The staged receipt-window gate accepted the single temporary fixture and classified SHA `96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef` as `round19-ruler-wave1`.
- **Agree:** this matches the label for that SHA in the supplied round-20 contract.
- The fixture was synthetic and kept in `/tmp`; its `2000-01-01T00:00:00Z` interval is a parser-valid sentinel only, not an assertion about when a historical measurement occurred. No production, staged, historical, Git, or JJ files were changed.

## Command and observed output

Fixture: `/tmp/tameshi-r20-b10-hist-96a68b60.json` (one receipt, the SHA above, ID `synthetic-check-round19-ruler-wave1`).

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py \
  --contract /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/contract.json \
  --receipts /tmp/tameshi-r20-b10-hist-96a68b60.json
```

Observed stdout and exit status:

```text
RECEIPT_WINDOW: CLEAN (receipts=1 historical=1)
RECEIPT_WINDOW info=HISTORICAL_INSTRUMENT receipt=synthetic-check-round19-ruler-wave1 classified round19-ruler-wave1
EXIT=0
```

## Defects and limits

- No gate defect was observed for this fixture.
- This check establishes schema acceptance and historical-label classification only. It does not establish historical instrument-byte provenance or a real measurement interval, and it does not run the six-population calibration measurement.
- No tools were installed or updated.
