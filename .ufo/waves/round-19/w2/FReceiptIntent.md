# FReceiptIntent — round 19 w2 (advisory)

Date: 2026-10-21. LSP route unavailable (`xd://lsp` is not mounted); findings below are direct file/JSON observations, not semantic LSP claims. Read-only review; no probe, suite, or selftest was run.

## Strongest assertion — agree

ReceiptIntent's historical diagnosis is correct: the R18 `checks.json#/bash-witness-selftest` row at frozen revision `55e1d31` records argv `python3 tools/bash-witness-study.py --selftest`, revision `921ef807…`, exit 64, and empty-stdout SHA-256; its retained stderr says “the following arguments are required: mode” (`.ufo/evidence/round-18/final/checks.json`, `.stderr`). The pinned parser requires a `mode` subcommand and registers `selftest` (`tools/bash-witness-study.py:1701,1709-1717`); the R18 registry row at `921ef807…` explicitly binds the expected positional argv and cites `SKILL.md@98bea7d:1504`.

The corrected L1 trace retained at `55e1d31` invokes positional `selftest` at `921ef807…`, exits 0, and records the tool/runner digests; both digests match the exact blobs at `921ef807…` and `4b7c682…`. The newer R19 receipt at `55e1d31` uses the same argv, records `4b7c682…`, exit 0, empty stderr, and pinned tool/runner hashes. Its stdout SHA-256 `316b9713…` matches the retained successful R18 tally; `measure.py:183-199` also requires byte equality with that tally. Thus ReceiptIntent's identified revision difference is real but does not contradict source identity or observed successful output. Round-19 lesson lines 202-208 accurately disclose the cross-revision identity and preserved failed attempt.

## Medium — failure-capable history check misses attribution

The delivered ruler does not verify the *failed* row's argv or revision. `measure.py:194-195` checks only its `exit == 64` and empty-stdout digest; `measure.py:378-395` accepts caller snapshots. The selftest fixture omits old-row argv/revision (`:245-248`), and its `wrong-argv` case mutates only the new success receipt (`:279-292`). A snapshot changing the old row's argv to positional `selftest` and its revision away from `921ef807…`, while retaining exit 64 and the empty-stdout digest, therefore leaves the R18-4 old-failure subpredicate true. This is a static control-flow counterexample, **not executed**; the actual committed row is correct. The ruler should bind the old row's exact argv and revision (and exercise both mutations) before treating preservation of that historical failure as checked.

## Arithmetic and residual limits

Plain JSON tally: `before.json` = 0 corrected / 5 open / 5 total; `after-21e7932.json` = 5 / 0 / 5. Both carry old ruler SHA-256 `c538c33d…`; the delivered `measure.py` at `55e1d31` hashes to `bb651e…`. These receipts reproduce the earlier arithmetic, **not** a final same-ruler 55e1d31 count; that after-count remains unverified here. No producer/environment authentication is inferred from receipt metadata.
