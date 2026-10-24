# Review — proposed round-37 QUALITY criteria 73–75 (append-only section, QUALITY.md:858–889)

Reviewer: ReviewQualityCriterion (leaf, read-only). Review target is the committed section at `e6185d5f`, not any worktree draft. Axes: falsifiability, grounding, append-only form, gameability.

## Verdict

**Accept 73–75 with two wording defects and one verification gap.** All three are scoped, path-grounded, append-only, and carry executing falsifiers. None is materially gameable as written; criterion 73's falsifier cites an ambiguous file name that, read literally, cannot show the `mode=control` it requires.

## Append-only form — PASS

- `git diff --numstat e423c41ba253357ab8c8513f0376dad9d38ab248 e6185d5f0b63a6963205110cb098f2f1eca27622 -- corpus/QUALITY.md` → `33  0` (insertions only; prior criteria 1–72 byte-unchanged).
- Numbering continues 73 → 75 after 72; heading `## Criteria appended — round 37 (2026-10-24)` matches the r30/r31 convention (`QUALITY.md:647,748,858`).
- The criterion-75 correction is itself append-only: the r36 SCORECARD block is untouched; the erratum is appended at `SCORECARD.md:1788`.

## Falsifier execution — verified red-before, all three

- **73**: `.ufo/evidence/round-37/calibration/before-final-control.stdout` = `unresolved_control_inputs=1 … C1_R37_PASS=false`, exit 1. The killed label bug is real: `control/replay-at-final-fixed.stdout` prints `mode=deciding` yet ends `EMPTY_PANEL_REPLAY_PASS=true` — a false-pass receipt, exactly the hazard the criterion names. Corrected state: `control/replay-at-final-control.stdout` = `mode=control … v1_pass=1 v2_reject=1` (exit 0) and `calibration/after-control-final.stdout` = `unresolved_control_inputs=0 … C1_R37_PASS=true` (exit 0).
- **74**: `code-view/before.stdout` = escaped-quote FAIL / literal-hash PASS, exit 1; after `2/2` at `ae9b771a`, tool sha `da8c1ef4…`; `tool-selftest-after.stdout` = `35/35` including both new ANSI-C cases.
- **75**: `git show e423c41ba253…:SCORECARD.md` contains the `8, 64/64` measured-prose sentence (blob lines 1743, 1758) while the after receipt `.ufo/evidence/round-36/after/monitor-at-b455001e.stdout` is committed at the later revision `b455001e…` (resolves, type commit).

## Grounding — PASS

- 73 ← round-37 Mistakes 1 (reference-drift, scratch `91373d55…` unreachable) and 4 (attribution, `mode=deciding`), `corpus/lessons/round-37.md:15,19`; r36 W2 mode-label review exists (`.ufo/waves/round-36/w2/W2ReviewC2Predicate.md:155`).
- 74 ← Mistake 2 + S104 (`corpus/SOURCES.md:113`, tier A, mined, scoped to `$'...'`; over-scope explicitly disclaimed).
- 75 ← the lesson's unnumbered "Additional record corrections" bullet, not a Mistakes row. Grounded by path, but note the scribe item's own bar said "grounded in a round-37 Mistakes row"; 75 meets the letter of the criterion conventions (r30 criterion 62 similarly cites a Gate record), flag only.

## Gameability analysis

- **73 — not gameable.** Killed vectors: (a) citing the `mode=deciding` receipt — the text kills it by name and the receipt exists showing the false pass; (b) counter substitution — receipts pin `COUNTER_SOURCE v1/v2 sha256=…` and counter rev `d9c496b…`; (c) input substitution — the manifest binds source tree `4f3d8af5…` (`manifest_ok=1`), and any zero-specimen alternate is the canonical empty tree, so substitution is semantically vacuous. The wording honestly calls the input a "committed **alternate** input" — it does not claim to resurrect unreachable `91373d55…`. Kill condition ("scratch-only mutant revision or `mode=deciding` label is not closure-resolvable") is honest and matches the frozen contract's supersession semantics.
- **74 — gameable only by fixture hardcoding**, which the criterion's own mutation clause kills ("removing the ANSI-C state must make the escaped-quote case fail" — a hardcode survives branch removal). Overblanking is killed by the literal-hash control. The "does not imply a full Bash lexer" sentence blocks predicate widening beyond the frozen two-case fixture. See gap below.
- **75 — not gameable.** Falsifier is a pure read-only git command; the rule ("a later receipt cannot retroactively make an earlier commit's sentence a measurement") is checkable at any future revision.

## Findings

1. **[moderate · falsifier pointer ambiguity] C73 names one file for two proofs.** Falsifier requires `after-control-final.stdout` to "re-derive zero and `mode=control`". The only file of that name is `calibration/after-control-final.stdout`, whose line has no `mode=` field; `mode=control` lives in a differently named file, `control/replay-at-final-control.stdout`. Read literally, the cited file cannot witness half the conjunct. This is the dangling-pointer class criterion 72 polices (and this round's own LOG erratum fixed for `monitor-at-content-commit.*`). Fix: cite both paths. Because 73 is committed, the fix must be an append-only erratum.
2. **[minor · falsifier paraphrase] C75's "the 8/64-64 statement" does not match the bytes.** The blob contains ``8, 64/64``; a literal `grep 8/64` over `git show e423c41b…:SCORECARD.md` finds nothing. The SCORECARD erratum at `SCORECARD.md:1788` uses the correct string. Same class as the r31 QUALITY 69/71 errata.
3. **[minor · verification gap] C74's anti-hardcoding clause has no committed falsifier path.** `.ufo/evidence/round-37/` contains no mutation receipt (only calibration/census/code-view/control/selftest/c2-repin artifacts); the branch-removal probe ran on a disposable copy (wave report `MutateAnsiBranch.md`, untracked). The clause is executable but nothing committed fails if a future tool hardcodes the two fixture bytes.

## Residual risk / gaps

- The scribe's run was still in progress at review time; criteria text reviewed is the committed `e6185d5f` section. Any wording fix lands as erratum, not edit.
- I did not execute the ANSI-C branch-removal mutation (owned by the mutation seat; live checkout untouched). C74's kill condition is accepted on the clause's logic plus the frozen fixture bytes, pending that seat's recorded diff.
- No installs were needed; no tooling changes to record.
