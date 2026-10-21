# FReceiptLaundering — critic review (2026-10-21)

## Strongest material assertion / verdict

**Disagree with the mechanical assertion** in `w1/ReceiptLaundering.md` §§39–45, 98–102: it says any byte change to `checks.json` breaks the digest-bound baseline and even a same-file append necessarily cannot score. The *policy conclusion*—do not replace the failed historical row—is sound, but that particular enforcement claim is not implemented by the delivered ruler.

## Evidence

- Baseline `.ufo/evidence/round-19/before.json:1–19` records `corrected: 0`, `open: 5`, revision `7243e7f…`, and the baseline `checks.json` digest `fed3c8e…`. This pins the baseline observation; it is not an equality check in the delivered `measure.py`.
- `.ufo/evidence/round-19/measure.py:45–51` includes `OLD_CHECKS` in `PATHS` but not `before.json`. `main()` at `:391–403` reads those paths at the selected revision and emits their digests; its check-mode failure is only `corrected != 5`. `evaluate().witness()` at `:183–199` checks the old row's exit `64` and empty-stdout digest plus the separate successor receipt/supersession. It never compares the whole old-checks blob with the before-pin.
- **Concrete falsifier (static code-path counterexample; not executed):** add a sibling JSON member to the current-revision `checks.json`, leaving `bash-witness-selftest` unchanged. The current blob digest differs from the `7243e7f…` pin, yet `witness()`'s tested old-row fields and valid successor remain unchanged; this ruler has no whole-file digest predicate to reject it. By contrast, changing the old row's exit to `0` does fail `witness()` and leaves R18-4 open.
- Receipt attribution itself is consistent: `measure.py:21` fixes `REV18=4b7c682…`; `witness()` requires argv `python3 tools/bash-witness-study.py selftest`; the complete receipt at `.ufo/evidence/round-19/bash-witness-selftest-complete.json:2–20` has that argv and revision. That is the historical replay revision, not delivered lane revision `55e1d312…` (also shown in `current-ledger-monitor-55e1d31.json:1954–55`). Do not conflate these revisions.
- QUALITY quote (criterion 39, `corpus/QUALITY.md:352–355`, read 2026-10-21): “A failed usage/setup attempt stays failed and byte-preserved.” This justifies the no-overwrite policy independently of the ruler's missing whole-file check.
- Arithmetic read directly from JSON: baseline is `0 corrected / 5 open`; `after-21e7932.json:2,18–40` reports `5/5`, but at revision `21e7932…` with ruler hash `c538c33…`. It is stale for delivered `55e1d312…` after the ruler was strengthened. The `55e1d31` monitor is calibration-only (60/60, restraint 8), not the five-defect result; final same-ruler C1 arithmetic remains for L1 to record.

## Impacted axes

- **Quality / integrity:** the report's append-only recommendation is supported, but its claimed mechanical whole-file enforcement is overstated.
- **Calibration (C1):** this review neither validates nor denies final 5/5; the only 5/5 artifact is stale at `21e7932…`.

## Residual unknowns / smallest safe correction

No same-file mutation was executed; the counterexample follows the current predicate and is not evidence that anyone edited the artifact. QUALITY also expressly says the ruler does not authenticate the historical producer (`QUALITY.md:360–363`); the receipt fields establish declared attribution, not independent execution provenance. Keep the failed row immutable and successor separate, but revise the report to say replacement is rejected by the exit-64 predicate and byte-preservation policy—not by a whole-file comparison in this ruler. If mechanical rejection of same-file edits is intended, pin/compare the complete `OLD_CHECKS` bytes in the evaluator.

## Erratum — hardened delivered ruler (2026-10-21)

The preceding mechanical counterexample is scoped to the `55e1d312…` version I initially reviewed. Re-opened explicit landed revision `329b6ddb826b16b1814b4ca87425f766c87e853d`: its `measure.py` SHA-256 is `7af3e951…f856cf72`; `OLD_CHECKS_PIN` and `witness()` now require the entire `checks.json` digest to equal `fed3c8e…671d`. Read-only SHA-256 of the original baseline blob at `7243e7f…` is exactly that pin. Thus the same-file-append counterexample no longer applies to 329b6ddb; **agree** with the report's mechanical preservation assertion for that later revision (the old failed-row replacement also fails its exit-64 check).

At 329b6ddb the measurement predicate also compares the effective receipt's embedded `observation` with the raw measurement JSON; the new metadata states it is derived, not a replay or producer authentication. QUALITY 39 likewise excludes historical-producer authentication. No probe/selftest was run. This bounded review does not establish the final five-row C1 score at 329b6ddb; the 21e7932 result remains stale for that purpose.
The earlier pin suggestion is superseded for 329b6ddb: its full-blob guard is already present.