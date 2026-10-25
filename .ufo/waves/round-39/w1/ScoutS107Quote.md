# ScoutS107Quote — S107 source verification

## Question
Re-fetch `golden_tests.md` at commit `4d3a89c9b72f9c19352318d1457a5f7c01462824`, locate the update-flag sentence, and compare to the committed snapshot pinned at sha256 `eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe`.

## Update-flag sentence (section heading + ≤25-word quote)
Heading: `## How do I update \`.expected\` files?`

> ".expected files can be updated by running the affected test target with the arguments `--test_arg=--update_goldens --test_strategy=local`."

## Comparison result — MATCH
```
$ curl -fsSL https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md | sha256sum
eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe
$ diff <live> .ufo/evidence/round-39/sources/golden_tests.md → identical
```
Live fetch sha256 equals the pinned snapshot sha256; `diff` reports no byte differences.

## Locations
- Live URL: `https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md`
- Snapshot: `.ufo/evidence/round-39/sources/golden_tests.md:63-66` (heading line 63, sentence lines 65-66)

## Confidence
High — byte-identical re-fetch, hash matches the contract source pin. No drift; the committed snapshot faithfully reproduces upstream.

## Remaining unknowns
None for this question.
