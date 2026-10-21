# Registry no-harm findings — round 19, attempt 1

## Finding

No active registry row or round-13 pin/evidence-disposition input directly names the three round-18 corpus files being corrected. Those existing registry and disposition receipts do not need rewriting solely because append-only corrections land.

The round-19 **after** receipt is `.ufo/evidence/round-19/after-21e7932.json`, pinned to revision `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`. It records `corrected=5`, `open=0`, and input digests for `corpus/knowledge/guard-kill-closure.md`, `corpus/knowledge/mutation-case-kumitate-sources-check.md`, `corpus/lessons/round-18.md`, and `corpus/SOURCES.md`. I did not replay it. **Any later append to one of those paths makes this receipt unsuitable as evidence for a successor revision.** Preserve it as historical and generate the successor measurement/receipt at the final delivered revision. If the intended append is already included in 21e7932, this receipt is already the corresponding round-19 measurement.

## Evidence: registry and manifests

- Source: `tools/registry.json`; read-only JSON selection `.rows[] | select(.status == "active") | select((.argv | join(" ")) | contains("pin-disposition"))` returned active `pin-disposition-read` (argv names `.ufo/evidence/round-13/pin-manifest.json`) and `pin-disposition-selftest`. Selection for `evidence-disposition` returned active round-18 gate rows for `.ufo/evidence/round-18/dispositions.json` and `dispositions-before.json`, plus its selftest. Active-entry selection for `corpus/knowledge`, `corpus/lessons`, or `corpus/` returned no rows. **Observed:** none of the active registry argv paths is one of the three metadata targets.
- Source: `.ufo/evidence/round-13/pin-manifest.json` and `pin-dispositions.json` (result `observed_at=2026-10-20T04:59:26Z`). The manifest has six configured legs in kumitate, kagi, tsukuroi, and mado repositories; the result reports six legs, 3 unchanged / 3 changed / 0 unavailable and `result_reuse=not_established`. No tameshi corpus metadata target is pinned there. This is not a source-reuse guarantee.
- Source: `.ufo/evidence/round-18/dispositions.json` and `dispositions-before.json`. Their `inputs` keys are round-13 expected/verification/oracle-repair receipts and the corresponding round-14 dispositions file; no corpus metadata path appears. The committed final result `.ufo/evidence/round-18/final/disposition.stdout` says `effective=11`, `superseded=1`, `exit=0` (tool identity dates it to 2026-10-20). Its `expected_inputs_verified` likewise lists round-12/13 evidence and tools, not these corpus files. These historical disposition receipts therefore do not drift from the append.

## Receipt crosswalk

- `.ufo/evidence/round-19/before.json`: revision is frozen baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, `corrected=0`, `open=5`; it holds the pre-correction corpus hashes. It remains a truthful baseline receipt, not a receipt to refresh against a new tip.
- `.ufo/evidence/round-19/after-21e7932.json`: the only receipt here whose corpus input hashes must be refreshed to make a claim about a successor revision. At its recorded revision it reports all five corrected and pins the four corpus paths listed above (plus round-18 receipts and round-19 evidence files). A mutation to any pinned corpus input changes that input's digest; the stored result itself remains a valid historical observation at 21e7932.
- `.ufo/evidence/round-19/round18-final-measure.json`: command record says `--rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0, recorded `2026-10-21T05:28:25.715990+00:00`; its stdout reports calibration-restraint score 8. This is a revision-pinned historical measurement and is not rewritten by a later append. It cannot, by itself, stand in for a measurement of a successor revision.

## Commands / outcome / limits

Only static file reads and JSON filters were used; no registry, pin-disposition, evidence-disposition, selftest, or measurement command was executed. Relevant selectors and observed results are recorded above. No production file, receipt, manifest, or repository state was changed; the only write is this unique report. The successor revision is not established by the inspected evidence, so its exact resulting digests remain unknown.