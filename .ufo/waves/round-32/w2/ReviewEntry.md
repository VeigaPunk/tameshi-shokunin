# ReviewEntry — runner-tally-audit.md review (round 32 wave 2)

Seat: `ReviewEntry`. Target: `corpus/knowledge/runner-tally-audit.md` at `a4f718138bdad20de741faeca57891645e5a64d9` (clone at
`/fast/scratch/hyaku/tameshi-r32-seats/ReviewEntry/c`). Reviewed against `corpus/QUALITY.md` and the actual behavior of
`tools/tally-audit.py` and `tools/mutate-and-run.sh` at that revision.

## Verdict

The document is factually sound and honest on the tool's mechanics: the three checks, the oracle, the 27-fault panel, the
8 MutateHead survivors, the counter copy sets, the S### citations, and the Limits section all re-derive from the code and
committed evidence, and the tool passes on the pristine runner. Two headline numbers on line 7 (the ledger entry count and
the drifted-sections estimate) are stale or not re-derivable at this revision.

## Findings

### 1. [High] "input of 270 of 480 cold-read ledger entries" is stale — the ledger count is 282 at this revision

- Doc line 7: "`tools/mutate-and-run.sh` is an input of 270 of 480 cold-read ledger entries".
- Evidence (read-only recount of `.ufo/evidence/round-21/coldread/ledger.json` at `a4f7181`):
  - total `entries` = 480 (checks out);
  - entries whose `inputs` contains `tools/mutate-and-run.sh` = **282** (exact key 282; substring match 282; the only
    extra substrings are two round-17/18 `staged/` copies and one pinned-input key, i.e. no false positives);
  - no verdict/class filter yields 270 (verified-record 29, wrong-expectation 31, gap-minor 209, executed-ok 12,
    gap-blocking 1; record 142, instruction 140).
- The number is a carry-over: at the round-31 measure revision `c111dab` the same recount gives exactly 270 of 456, so
  270/456 was genuine; the round-31 wave-1 review already flagged that the round-32 contract re-used 270 with the new
  480-entry ledger without re-counting (`.ufo/waves/round-32/w1/ScoutDeferrals.md:39`). The doc (part of this content
  revision) repeats the stale pair.
- Smallest correction (line 7): recount at the content revision and use the computed value (282 of 480 at `a4f7181`),
  or drop the exact counts and write directionally ("an input of most cold-read ledger entries") until a recount lands.

### 2. [Medium] "about 26 credited SKILL.md sections" is not re-derivable at this revision

- Doc line 7: "any edit to it drifts about 26 credited SKILL.md sections".
- Evidence: no straightforward ledger metric at `a4f7181` yields 26:
  - runner-input entries with verdict `verified-record`: 29 (was 26 at `c111dab`);
  - sections keyed by their latest entry (`skill_sha256`, `start`): 224 runner-keyed of 384;
  - any-entry runner sections: 231; distinct heading strings among runner entries: 41; distinct `start` values: 44.
- The origin of the figure is the round-31 review's estimate ("sections whose latest entry keys on it → 26",
  `.ufo/waves/round-31/w1/ReviewRoutedR30.md:35`), which the same review itself could not reproduce exactly for the
  sibling figure ("about 31 sections … is the same order, not exactly reproduced", `:48`). Carrying 26 into the
  480-entry ledger without re-derivation fails the acceptance bar ("every number on the page must be re-derivable").
- Smallest correction: replace with a recomputed value at the content revision and name the metric, or remove the number
  and state directionality only.

### 3. [Low] "the measured result is in SCORECARD.md's round-32 block" is a forward reference at this revision

- Doc line 2: "the measured result is in SCORECARD.md's round-32 block, not on this page".
- Evidence: `SCORECARD.md` at `a4f7181` ends its round-32 section (lines 1555–1580) with "Measured results are appended
  below only after execution." — no measured row exists yet, consistent with C1's measurement still pending (the
  held-out set is written in this wave). The sentence asserts an existing result.
- Smallest correction: phrase as a pointer to where the result will be appended ("the measured result will be appended in
  SCORECARD.md's round-32 block"), or leave it once the block carries the row.

## Verified statements (no defect)

- Tool run at `a4f7181` in the clone, pristine runner `tools/mutate-and-run.sh` (sha256
  `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, byte-identical to the pinned pin):
  - `python3 tools/tally-audit.py` → `CHECK static PASS legs=9 operands=9 nlegs=9`; `CHECK runtime PASS vectors=349
    mismatched=0`; `CHECK harness PASS reference cases=9; faults rejected=27/27`; `TALLY_AUDIT: PASS (static=pass
    runtime=pass harness=pass)`; exit 0.
  - `python3 tools/tally-audit.py --selftest` → 11/11 cases PASS (pristine accept; dup-drop operand, nlegs wrong,
    status-4-passes, guard-undercount-only, harness exit-only/swallowed/position-8/0/1-skipped all exit 1; reversed
    operands exit 0); `TALLY_AUDIT_SELFTEST: 11/11 pass`; exit 0.
- The 27-fault panel counts exactly as described (doc line 13): label, fail-exits-0, drop-last-operand (3); nine
  `ignore-*`; nine `ignore-alone-*`; guard-removed + guard-overcount-only (2); setup-before-fail (1); fail- and
  setup-needs-exactly-one (2); status-3-passes (1) = 27 (`fault()` at `tools/tally-audit.py:256-292`).
- Runtime sweep structure (doc line 12) matches code (`check_runtime`, `:218-253`): all 0–255 single-status vectors at
  leg 1 (255 + all-zero baseline), 1 2 3 4 126 127 255 at each of the 9 positions (63), ten multi-status pair vectors
  plus all-1/all-2 (12), and dup/drop operand stress at each of the 9 positions (18); total 349 vectors, all oracle-
  matched.
- The oracle restates the runner's printed contract (doc line 24) exactly (`oracle`, `:183-195`), so the "agrees with a
  wrong contract" limit is honest.
- Static check semantics (doc line 11) verified: `st_*=$?` leg names, loop operand multiset, and `nlegs=9` all agree;
  the sum-only guard weakness and its detection are demonstrated by the dup-drop selftest case.
- MutateHead survivor facts (doc line 7, line 19): `.ufo/waves/round-30/wC/MutateHead.md` reports exactly eight
  non-equivalent survivors (T08, H03, H04, H05, N01, N02, N03, N05; T07/H01/H02 equivalent), and
  `.ufo/evidence/round-32/before/mutant-fidelity.txt` confirms the eight frozen kill copies plus B1-T07 are byte-identical
  to that report's mutated SHA-256 column; D01 (duplicate-and-drop loop) has no report counterpart.
- Counter copy sets (doc line 19) match the frozen code: `c1-measure.py` `frozen_kill` = 9 (8 survivors + D01),
  `generated_kill` = 9 families seeded from `rng`; `frozen_accept` = 6 (B0 pristine, B1-T07, B2 reversed, B3 decoys
  carrying every frozen mutant's text, B4 cosmetic, B5 renamed harness variable), `generated_accept` = 2 (gB6 random
  permutation, gB7 nonce comments); totals 18 kill / 8 accept as in `contract.json` and amendment 1.
- S-cites (doc line 1) agree with `corpus/SOURCES.md` rows: S097 (Bash 5.3 texi exit-status range + `case` first-match,
  lines 3890–3916 / 1044–1084), S099 (PIT home page, seeded-fault kill metric), S094 (Dwork et al. arXiv:1411.2664v3
  holdout; re-opened round 32, used-by updated in the SOURCES note, lines 387–389). Coverage row exists in
  `corpus/README.md:470` (criterion 7 satisfied).
- Limits section (lines 21–26) is honest: generated families ≠ all runner edits; tally-block/harness-scope statement true
  of the tool; `--then-regression` only compares the printed `cases=` to the leg count (`then_regression`, `:380-393`)
  without re-deriving a leg status; runner selftest bytes unchanged (same pinned sha) so "still passes the eight
  survivors" reflects the round-30 measurement.
- `SCORECARD.md` round-32 block exists and carries the same frozen markers the page uses (`c3181497` is the freeze commit
  `c31814978969a41a8e9b0f7d99fa308c5993c1b7` for both `contract.json` and `c1-measure.py`, verified via `git log`).

## Verification gaps

- Section-level drift count depends on an undocumented metric; the boundary number 26 was checked against several
  plausible derivations, none reproduces it at this revision (finding 2).
- I did not run `bash tools/mutate-and-run.sh --selftest`; the "unchanged / still passes the eight survivors" statement is
  supported by the pinned byte-identity and the round-30 measured report instead.
