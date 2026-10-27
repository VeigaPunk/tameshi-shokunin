source: S105 — https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html — §EXIT STATUS (lines 564-574) and §ENVIRONMENT VARIABLES, entries LANG (162), LC_ALL (166), TZ (191) — Issue 7, 2018 edition (IEEE Std 1003.1-2017) — fetched 2026-10-24, sha256 dda9f57dac3b2420966b5f4d14417b84dfc76ac7c4bb14ead5e901af86a1de5a
source: S106 — https://raw.githubusercontent.com/google/golden/master/golden.go — `Compare` doc comment (lines 72-73) and the `shouldUpdateGolden()` branch (line 78) — master as fetched 2026-10-24, sha256 4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f
verified-at: 2026-10-24 (both sources re-opened by this round's own writer; located quotes in `corpus/lessons/round-38.md` `## Gate`)
recheck: 365d — re-run `curl -fsSL 'https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html' | grep -c 'An error occurred'` (expect a non-zero count) and `curl -fsSL 'https://raw.githubusercontent.com/google/golden/master/golden.go' | grep -c 'update_golden'` (expect a non-zero count)
ground: F4 (golden / snapshot fixture discipline)

# A golden comparison has three outcomes, and the path that writes the expected value is a flagged path

## What the sources state

- POSIX `diff` returns three exit values, not two: `0` "No differences were found", `1`
  "Differences were found", and greater than `1` "An error occurred" (S105, §EXIT STATUS,
  lines 564-574). The same specification names `LANG` (162), `LC_ALL` (166) and `TZ` (191)
  among the environment variables that affect the execution of `diff` (§ENVIRONMENT
  VARIABLES).
- `google/golden`'s `Compare` returns the unified diff when the actual value differs from
  the golden file, and the write path that overwrites the golden file is gated on the
  `-update_golden` flag (S106, `Compare` doc comment, lines 72-73; `shouldUpdateGolden()`
  branch, line 78).

## The three-outcome rule

A golden comparison is classified into exactly three outcomes, and the third one is the one
a two-outcome harness drops:

| outcome | condition | what it means for a fixture |
|---|---|---|
| match | the comparison ran and found no differences | the fixture's expectation holds; this is the only outcome that may be called green |
| differ | the comparison ran and found differences | the artifact under test changed, or the expected value is stale |
| error | the comparison could not be made (exit > 1, or a required file is absent) | nothing was compared; the fixture proved nothing and must not be recorded as a red |

Two consequences for the lane's own craft:

1. **A comparison that could not be made is not a failure of the code under test.** S105's
   `>1` class is an error class, distinct from the difference class. A harness that
   collapses "differ" and "error" into one verdict cannot tell "the code changed" from
   "the comparison never happened". The lane's fixture for this rule classifies three
   outcomes and asserts the error class explicitly
   (`tools/golden-verdict.py --selftest`; counter `.ufo/evidence/round-38/golden/measure.py`).
2. **The write path must be explicit.** In S106 the overwrite path sits behind
   `-update_golden`; the normal path only reads and compares. Inference from S106's
   structure: a golden fixture whose expected value can be rewritten without a
   distinguishable flag has no fail-closed arm for that write. The lane's own open F4
   measurement — "update paths that write expected values without an explicit flag:
   unmeasured -> counted per surveyed gate" — is **not** measured here; the lane's
   surveyed gates were not audited in this round.

## Boundary of this entry

- The exit-status class is POSIX `diff`'s. `cmp`, `git diff --exit-code` and other
  comparators have their own lattices and are not covered by this entry.
- The environment-variable list names what the specification says affects `diff`; it does
  not by itself make any comparison byte-reproducible under an unnormalized environment.
- Nothing here measures the lane's own gates, and no claim is made that the lane's
  fixtures are golden-comparison fixtures today.
