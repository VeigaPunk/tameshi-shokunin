# FShonenNoHarm — scoped falsifier (2026-10-21)

- Axes checked: count semantics; frozen-revision/source attribution; C1 measurement revision.
- Scope: ShonenNoHarm F2 and its cited primary surfaces; read-only Git/JSON inspection only. No lane suite, selftest, build, lint, formatter, or measure execution.

## Strongest assertion attacked — F2

- **Verdict: partial disagreement.** The report accurately records the `cecaefe` snapshot: prose said eleven while its ledger had thirteen L1 re-anchor entries. But its “stated count must equal” *entry* count rule is not supported by the prose's unit (“buckets”), and its no-later-correction claim is stale at delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c`.
- At `55e1`, `corpus/lessons/round-19.md:192–200` explicitly says “two further source entries after the initial eleven” and names buckets 1499 (SHONEN link) and 1855 (recipe migration). This post-`cecaefe` addendum reconciles eleven initially affected buckets plus two later buckets; it falsifies F2's claim that the cited lesson contains no mention of either correction. `SCORECARD.md:738–740` still says “eleven invalidated buckets,” so its wording remains ambiguous, not fully carried forward.
- Read-only JSON arithmetic on the **55e1 ledger** using the exact seat `L1 TameshiR19-2 author source re-anchor`: **15 entries, 13 distinct `start` buckets** (`6,131,375,1380,1479,1499,1517,1548,1563,1609,1855,1905,1925`). Starts 6 and 1925 each have a second re-anchor; counting entry rows as bucket identities conflates rereads with distinct buckets. Thus F2's “13 entries” is no longer the delivered-revision count, while 13 remains the distinct-bucket count.
- Attribution check: those two repeat entries record `read_rev=eedbc95f232cde4a5aabd6e4e34fc2e78a1a5626`; the pinned `coldread/refresh-postbuild-receipts.json` records the same `read_revision`, matching `trace-inputs.py` argv prefixes and source-read code, exit 0, stdout/stderr digests, and trace digests. `eedbc95` is an ancestor of `55e1`. The embedded read explicitly says no recipe argv was executed; these are source rereads, not claimed command executions.
- **Concrete falsifier:** the exact delivered ledger has 15 source-reanchor rows but only 13 distinct bucket starts, and the final lesson explicitly accounts for the two additional buckets absent from ShonenNoHarm's `cecaefe` snapshot. F2's row-count criterion and “no mention” premise do not hold at `55e1`.

## Revision and measurement boundary

- The pinned `.ufo/evidence/round-19/measure.py` accepts a full `--rev` and reads that revision's paths; its `--check` exit depends on all five corrected (lines 367–403). Pinned `before.json` is 0 corrected / 5 open at baseline `7243e7f`; the only pinned after JSON is 5 / 0 at `21e7932`, with the same ruler SHA. The `55e1` tree contains no after receipt for `55e1`; do not attribute the 21e7932 result to the delivered revision. I did not run the ruler.
- The later master `e7039fdb8237fa567704f54d422a7c0b7e009611` contains `current-ledger-monitor-55e1d31.json` with `revision=rev_input=55e1`, score 8, 60/60, full-page true, overrides false, strict trace gate and committed ledger. It is absent from the `55e1` tree and the JSON has no argv/exit envelope; this later monitor makes ShonenNoHarm F4’s `cecaefe` observation time-bounded, but does not supply the missing final C1 `measure.py` after receipt or establish its invocation.

## Residual

- The scorecard's “eleven” is not explicitly labeled as the initial cohort, so a reader may mistake it for the final total; the lesson's addendum clarifies the distinction. Final same-ruler C1 count at `55e1` remains unobserved here. Confidence: high on ledger counts, dated text, and revision/receipt attribution; no admission or closure authority claimed.