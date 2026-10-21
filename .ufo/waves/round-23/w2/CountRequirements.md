**Axes assessed:** exact registry-contract membership; replay receipt coverage and recorded exit concordance.

**Findings:** `requirements.json` has 43 entries; `registry-baseline.json` has 43 active rows. The frozen registry digest matches, and all 43 `name`/`argv`/`expect` entries match exactly, with no missing or extra rows. In `replay/bundle.json` (revision `496d212bc46789cdf8cafab72978bdb7f4182963`), all 43 declared requirements match exactly; all 43 receipts are covered by requirement `name`/`argv` pairs, with no missing or extra pairs. All 43 recorded exits match the corresponding expected exits.

**Evidence retained:** `.ufo/evidence/round-23/requirements.json`, `registry-baseline.json`, and `replay/bundle.json`; the single read-only Python count produced the figures above. `replay.py` lines 34–41 show the frozen-digest and active-row checks; lines 62–75 show how requirements and receipts are recorded.

**Files changed:** none. **Risk/limitation:** this count checks the bundle’s declarations and recorded receipt exits; it does not independently re-execute commands or validate receipt output content. No tests, builds, or formatters were run. The requested report file was not written because the scoped instructions prohibit all file writes; these findings are provided for L1 to persist.
