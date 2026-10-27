# Tameshi round 52 — registry-home repair, closure-found false records, honest re-key

L1 TameshiR52, hyaku run 9, attempt 1. Base `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`. Frozen predicates, controls and deciding script: `.ufo/evidence/round-52/contract.json` (freeze `acc27abe`; amendment 1 `8827f319`, controls harness only). Claims: C1 operability (the two registry homes return their registered outcomes), C2 calibration (the records the round-51 closure found false). Both repair what `corpus/lessons/round-51-verifier-spotcheck.md` routed back.

## Gate

Rows opened this round (CORPUS.md SOURCES contract v1 rule 1):

- **S274** — Bazel documentation, "Hermeticity", `https://bazel.build/basics/hermeticity` (markdown rendition `https://bazel.build/basics/hermeticity.md`), opened 2026-10-27 (05:15Z) by seat T52W1ScribeSource, HTTP 200, 5878 B, sha256 `2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6` (snapshot `.ufo/waves/round-52/w1/T52W1ScribeSource-snapshot.txt`); re-opened independently by T52W2RevSource, same sha. Located quote (18 words, snapshot lines 12-14): "hermetic build system always returns the same output by isolating the build from changes to the host system". Second quote (10 words, :28-29): "Hermetic build systems try to ensure the sameness of inputs".
  - Use: `tools/round21-measure.py --selftest` reads the pinned sibling blobs at the fleet root its subject counter `c2-count.py` names (`FLEET`). By the source's definition that is an undeclared host input, so the self-test is not hermetic; round 52 declares it fleet-bound (it now reads exactly the root its subject reads, and fails where that root is absent) instead of claiming hermeticity. Scope limit (T52W2RevSource): Bazel defines hermeticity for builds; the lane applies it to a test run by analogy, not as a categorical verdict.

Candidates rejected:
- **A truly hermetic round21-measure self-test** (fixture sibling repos built in TMPDIR). Rejected: the frozen subject counter `.ufo/evidence/round-21/c2-count.py:19` hard-codes `FLEET`, so a hermetic fixture would stop testing the subject's real input path. Flip: a counter that accepts a fleet-root argument.
- **The wave-1 kill-rate supersession variant** (`.ufo/waves/round-52/w1/T52W1ScribeKillNote.md:31`). Rejected as duplicate: the landed line already satisfies the frozen m5 rule with the same pointers. T52W2RevRouting later asked to scope "floor" to the two observed runs.
- **The kagi routing draft's `grep -qxF "$3"` fix** (`.ufo/waves/round-52/w1/T52W1ScribeKagiRoute.md`). Rejected after T52W2RevRouting: the combined output carries more than the verdict line; the report recommends comparing an extracted verdict field instead.

Rows touched: none besides the S274 append and its bookkeeping line.

## C1 — operability

The `mte-interop-check` row now expects `legs_conforming=10/10` (`tools/registry.json:1014`), and its source points at the round-51 routed defect. `tools/round21-measure.py` reads its subject's `FLEET` root, so the round-51 C3 counter's fresh clone outside the fleet no longer turns it red. Pre-freeze base runs: `REGISTRY_CHECK: held=48/49` and C3 `covered=29 total=1`. Probe at CAND0 (T52W2ExecC1Probe): rows `49/49`, but C3 was still 29/30. The cause was the round's own SKILL row edit, which put two extra backticked words in the self-test cell, and the frozen C3 row rule allows exactly one backticked command there. The cell was rewritten before CAND1.

## C2 — calibration

At CAND0 the frozen C2 probe prints `total=0` (from 27). The 20 correction records carry 73 findings from the wave-1 scribes. The wave-2 non-author review (T52W2RevCorr*) re-graded them:
- 11 records are exact (03, 04, 05, 07, 08, 14-20).
- 8 over-count (01, 02, 06, 09-13). Example: Corr12, where the reviewer found 0 of 14 findings to be statements the reader marked as not holding.
- No reviewer found a missed failure.

So m4's counts are an upper bound on what the round-51 readers recorded; the frozen counter cannot see this (contract `cannot_see`).

## Re-key

Measured at CAND0 (`.ufo/evidence/round-52/integrate/precheck-cand0.stdout`), the round's edits drop 18 sections from cold-read credit (64 → 46). Fourteen of those drops come from the one-line kill-rate-ledger append, because their old entries pin that file's sha.

The round-21 monitor credits a section only when its entry records zero wrong expectations. Round 52 records each reader's actual count (C2 m6), so stale statements had to be fixed before the re-read:
- **Wave 2 drafted the fixes.** 18 fix-read seats were dispatched and 17 delivered; T52W2Fix08, the round-26 registry section, ended with no deliverable.
- **The L1 applied them in-line.** 53 replacements went in on the first pass and 6 on the second (`.ufo/evidence/round-52/integrate/apply-fixes*.stdout`). SKILL.md kept its 2171 lines.
- **Wave 3 re-reads the fixed bytes.** Readers are fresh seats, and the findings are copied mechanically from each reader's JSON block.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `tool-change-without-registry-row` — round 51 changed `tools/mte-interop.py` to ten legs while its registered gate row kept `9/9` and SKILL.md kept "nine ledger legs"; a scope monitor allowed the tool change and nothing replayed the row | `corpus/lessons/round-51-verifier-spotcheck.md:84-88,126`; recurrence of R47.1 (`.ufo/waves/round-52/w1/T52W1ScoutRecurrence.md`) | none at round 51 (no monitor replayed `tools/registry.json` at the candidate) | QUALITY criterion 103; round-52 C1 counter. Shown able to fail: `C1_CTL_0` (base, `held=48/49`), `C1_CTL_STALE`, `C1_CTL_SUPERSEDE`, `C1_CTL_NEEDLE` all false; `C1_CTL_POSITIVE` true (`.ufo/evidence/round-52/control/controls.stdout`) |
| `fleet-bound-run-outside-fleet` (this round) — the first controls run placed its clone outside the fleet, so registry rows that read siblings through the fleet mirror went red and `C1_CTL_POSITIVE` came out false; evidence-disposition rows also refused control commits on no branch | `.ufo/evidence/round-52/control/a0/controls.stdout` (POSITIVE `total=5`); `.ufo/evidence/round-52/contract.json` amendment 1 | the pre-registered positive (reachability) control | amendment 1 (fleet-mirror clone, branch per control); re-run 11/11 as pre-registered. Shown able to fail: the a0 receipt is the red run |
| `own-edit-breaks-frozen-row-rule` (this round) — the L1's SKILL row edit declaring round21-measure fleet-bound added backticked words to the self-test cell, which the frozen round-51 C3 row rule counts as commands (`selftest-cell-commands=3`) | `.ufo/waves/round-52/w2/T52W2ExecC1Probe.md` | the wave-2 C1 probe (a non-deciding counter run at the candidate) | cell rewritten without backticks before CAND1. Shown able to fail: the CAND0 probe receipt `c3_total=1` |

## Limits

- C1 cannot see whether a non-mte row's needle is meaningful. T52W1CritC1 and T52W2MutC1Survivors show that a lane edit can reach the base-active drop clause and the dual-needle hole.
- C2 cannot see stale statements outside its frozen set. T52W2MutC2Followup reproduced a C2 pass that coexists with an unrelated stale "nine" statement.
- Neither counter can see the completeness or the over-count of the correction records.
- `tools/registry-check.py:766` creates its clone under a hard-coded `/tmp` (scratch directive §7.4). It is frozen this round and routed for next round.
