# Round 19 w2 — MetadataDraft falsifier

- **Strongest assertion attacked:** w1 MetadataDraft §Verdict/§2 says its two routed metadata defects (R18-1 and R18-2) were durably corrected and factually accurate at `21e7932` (2026-10-21).
- **Disposition:** Agree with the underlying 2/2 correction; no false metadata fact found in these two errata at frozen revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`. Disagree that the current ruler fully enforces R18-1 receipt attribution.

## Evidence and arithmetic

- `55e1d312` is on `refs/heads/master`, descends from `21e7932`; relative to baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, `git diff --numstat` is `38 0` for `guard-kill-closure.md` and `18 0` for `mutation-case-kumitate-sources-check.md` (append-only).
- At `55e1d312`, `guard-kill-closure.md` contains R18-1, names line 2 and the exact historical tool revision `921ef8077440f90d092aab4b9fdc750a45de1224`. Its `checks.json` `probes` row has argv `python3 .ufo/evidence/round-18/defect-probes.py --rev 921ef8077440f90d092aab4b9fdc750a45de1224`, matching revision, exit 0 and stdout SHA `d37c99e3…eb8cf0`; the exact frozen `probes.stdout` independently hashes to `d37c99e3…eb8cf0` and contains `DEFECT_PROBES: open=0 closed=11 total=11`.
- At the same revision, R18-2 names line 1 and delivered-round-18 revision `4b7c6823a462f5ea2eafcb262275300a545f3ed7`. The S008 row is mined/opened 2026-10-19 and lists this knowledge entry in `used-by`; it agrees with the ruler's pinned `source-round18-final.txt` row. The old `**queued**` wording remains above the append-only erratum, which explicitly supersedes it.
- The later sweep addenda correct w1 §3.1–3.3: the case-8 lines 215–219 obligations; guard note lines 99/133; and source backlinks (S063/S077/S078) are recorded in the delivered source rows. The R18-1 text also clarifies S077/S078 supersede the old S068/S072 anchors.
- **Reproduced by reading predicates and committed JSON only (no ruler/selftest run):** baseline `before.json` has R18-1 and R18-2 open; at `55e1d312`, `measure.py`'s `guard()` and `source()` predicates evaluate true for both from the facts above: **2/2 for this item**. This is not a new receipt.

## Concrete falsifier / gap

- `measure.py:139–148` (`guard()`) reads the old probe receipt's `revision`, `exit`, and `stdout_sha256`, then checks the tally; it never reads `old['argv']` (nor validates a stderr stream). The exact argv is correct in the actual frozen `checks.json`, so that observation does not falsify w1's manual check. But a concrete counterexample to the ruler's attribution guarantee is a snapshot differing only in `checks.json['probes']['argv']` (e.g. `--rev 183f87b`): this predicate still marks R18-1 corrected. This is static control-flow analysis, not an executed mutation. `receipt()` at lines 78–96 has exact-argv checks, but `guard()` does not call it.

## Residuals and verification gap

- The guard entry's recheck instruction still says `--rev <branch tip>` at line 3, while R18-1 says not to replace the pinned result with an unpinned branch-tip claim. This was already flagged as optional in w1 §3.4; it is not one of the two routed defects and was not overlooked there.
- `after-21e7932.json` records revision `21e7932` and ruler SHA `c538c33d…`; frozen `measure.py` at `55e1d312` hashes to `bb651eef…`. No `after-55e1d31` measurement receipt was present in the inspected evidence listing, so the final same-ruler after count and public selftest remain unobserved here. The prior receipt is not final-revision verification.
- Read-only inspection only; no suites, builds, tests, or selftests run.