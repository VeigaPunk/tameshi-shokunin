# R23-REATTACK SchemaPriority (round 25, wave 1)

**Verdict: FINDING, severity LOW.** The round-23 defects this item targeted are fixed at lane revision c9ff09f. The command-binding gate's exact-key rule holds at all five levels. One counterexample remains in the same precedence class: on the requirement side, the reported finding ID depends on row order. The exit code is 2 in both orderings, so no mismatch passes and no pass/fail verdict flips.

## Subject and status

- The original seat, TameshiR23.SchemaPriority, never reported. `.ufo/waves/round-23/original-outcomes2.json` records status "failed", final_output_chars 0, report_file null, and death_basis "no task-result callback retained". `.ufo/waves/round-23/w2/` has no SchemaPriority.md. This re-attack is the first evidence for the item.
- Frozen subject: `.ufo/evidence/round-23/pre-review-command-binding.py`, sha256 `13fa4818a11bf4a51659cba6dc5ee906021a71d740df793aef78d9293768784a`. That hash equals the instrument pin in `.ufo/evidence/round-23/mixed-invalid-pre-review.json`.
- Repaired tool at 496d212: sha256 `d533dc1e…`. That equals the pin in `mixed-invalid-repaired.json`.
- Current tool at c9ff09f: blob sha256 `9230c68e…`. `git diff 496d212 c9ff09f -- tools/command-binding.py` has one hunk, `@@ -161,11 +161,12 @@`, inside `selftest()`. It only makes the selftest also load the round-24 fixtures. `evaluate()` and `check()` are unchanged since 496d212. `git diff` of command-binding.py and registry.json between c9ff09f and lane HEAD 5b69fb2 is empty.
- Registry: the round-23 rows (command-binding-selftest 38/38, command-binding-frozen-clean, command-binding-source-read-red) are superseded. Their active successors are command-binding-selftest-r24 (expects 44/44), command-binding-frozen-clean-pinned (expects bundle_sha256 `3d6c99b7…`), and command-binding-source-read-red-pinned (expects bundle_sha256 `db620668…`).
- The original "no repo writes" bound is superseded by the assignment. Every execution ran against scratch copies in /tmp, made with `git archive c9ff09f`. The only file I wrote is this report.

## Does the round-23 finding still apply at c9ff09f?

- Exact keys: no. Missing in the frozen draft, fixed in 496d212, still present at c9ff09f.
- Duplicate-before-malformed precedence on receipts: no. Frozen draft returned DUPLICATE_COMMAND (exit 1). c9ff09f returns INVALID_RECEIPT (exit 2).
- Requirement-side precedence: yes. It is present in the frozen draft, the 496d212 repair did not touch it, and it still applies at c9ff09f. See F1.

## Checks and observed results

Each run used the bundle shapes described in the probe notes. Outputs are the tool's own report.

1. Supplemental fixture differential, all 25 cases (19 from round-23 extra-cases.json, 6 from round-24).
   - Frozen pre-review: 21 of 25 pass. Failures: duplicate-before-malformed returned (1, DUPLICATE_COMMAND) where the fixture expects (2, INVALID_RECEIPT). unknown-expect-key, unknown-receipt-key, and unknown-bundle-key each returned (0, []) where the fixture expects (2, INVALID_*).
   - c9ff09f: 25 of 25 pass.
2. Selftests.
   - Frozen pre-review: `COMMAND_BINDING_SELFTEST: 19/19 pass`, rc 0. It never loads the supplemental fixtures, so it was blind to the defect.
   - c9ff09f: `COMMAND_BINDING_SELFTEST: 44/44 pass`, rc 0.
3. Frozen mixed-invalid artifact `.ufo/evidence/round-23/mixed-invalid-bundle.json`, sha256 `fe5964a5…`, which matches its expected pin.
   - Frozen pre-review: (1, DUPLICATE_COMMAND). This matches `mixed-invalid-pre-review.json` stdout.
   - c9ff09f: (2, INVALID_RECEIPT). This matches `mixed-invalid-repaired.json`.
4. Exact keys at each level. Probes used a valid base bundle with one extra key added.
   - Extra key on a requirement row: frozen (0, []), which is a clean pass. c9ff09f (2, INVALID_REQUIREMENT).
   - Extra key on the bundle: frozen (0, []). c9ff09f (2, INVALID_BUNDLE).
   - Extra key on a receipt: frozen (0, []). c9ff09f (2, INVALID_RECEIPT).
   - Extra key on the expected file: frozen (0, []). c9ff09f (2, INVALID_EXPECTED).
   - Receipt missing `stderr`: frozen (2, INVALID_RECEIPT). c9ff09f (2, INVALID_RECEIPT).
   - Clean control: (0, []) on both.
   - Unknown key inside `expect`: pinned by fixture unknown-expect-key, which passes at c9ff09f.
5. Receipt precedence, order swapped. Receipts [valid a, valid a, malformed] and [malformed, valid a, valid a].
   - Frozen: (1, DUPLICATE_COMMAND) and (2, INVALID_RECEIPT).
   - c9ff09f: (2, INVALID_RECEIPT) in both orders. Order-independent.
6. Requirement precedence, order swapped. Requirements [a, a-duplicate, b-malformed] and [a, b-malformed, a-duplicate].
   - Frozen and c9ff09f: (2, DUPLICATE_REQUIREMENT) and (2, INVALID_REQUIREMENT). Not order-independent. See F1.
7. Cross-section. Requirements [a, a-duplicate] with receipts [malformed].
   - Frozen and c9ff09f: (2, DUPLICATE_REQUIREMENT).
8. Fixture coverage. None of the 25 supplemental cases has a duplicate requirement name, and the selftest's only duplicate-requirement case uses valid rows (command-binding.py:158). Nothing pins the requirement-side behavior.
9. Pinned gate rows, run in scratch at c9ff09f.
   - Direct: `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` returns rc 0, `"finding_ids": []`, and bundle_sha256 `3d6c99b7…`. Held.
   - Direct: the source-read-red bundle returns rc 1, `["ARGV_MISMATCH"]`, and bundle_sha256 `db620668…`. Held.
   - `registry-check.py --only` for each of the three active command-binding rows: `held=1/1` each.

## F1 (LOW): requirement-side duplicate check is inline, so precedence depends on row order

- Evidence: command-binding.py:75–83 at c9ff09f. The requirement loop validates each row and checks `row['name'] in requirements` inside the same loop (lines 82–83). A duplicate at index i returns DUPLICATE_REQUIREMENT before a malformed row at index j > i is ever read.
- The receipt side was repaired. command-binding.py:87–96 completes structural validation first. The comment at line 93 reads "Complete structural validation before any semantic duplicate failure." The requirement side never got the same pass. The 496d212 repair left lines 82–83 unchanged, and the frozen draft has the same inline check.
- Concrete counterexample, c9ff09f, identical in the frozen draft. Bundle: revision a×40, cwd `/fixture/repo`, receipts [valid a]. Requirements, row order [valid a, valid a-duplicate, malformed b] gives (2, DUPLICATE_REQUIREMENT). Row order [valid a, malformed b, valid a-duplicate] gives (2, INVALID_REQUIREMENT). Here "malformed b" is a requirement with no `expect.exit`.
- Cross-section counterexample: requirements [a, a-duplicate] with receipts [malformed] gives (2, DUPLICATE_REQUIREMENT). The receipt-side rule would give INVALID_RECEIPT. [INFERENCE: the intended scope of "invalid before duplicate" is global. build-adjudication.json:6 accepts the phrase "exact finding sets and mixed invalid/duplicate precedence" without naming a section, so the global reading is my inference.]
- Why it is LOW: every requirement-side outcome here is exit 2 (could not evaluate). No mismatch passes, and the pass/fail verdict does not flip. Only the finding ID changes. The round-23 defect that mattered (duplicate-before-malformed flipping 2 to 1) is fixed for receipts.
- Why it still counts: the item asks about mixed invalid/duplicate precedence, and this is a concrete bundle where the outcome depends on which row comes first. No selftest or fixture catches it.
- Smallest safe correction, not applied because the lane is read-only for me:
  1. In `evaluate()`, split the requirement loop into two passes. First, structurally validate every row (lines 75–81). Then run the duplicate pass (lines 82–83). Both orderings then return INVALID_REQUIREMENT.
  2. Decide the cross-section rule. If structural-first is global, move the requirement duplicate pass after the receipt structural pass (after line 92). The cross-section case then returns INVALID_RECEIPT.
  3. Add supplemental fixtures for the swapped-order cases and, if the global rule is adopted, the cross-section case. Wire them into `selftest()` (lines 166–169 load the supplemental files).
  4. The selftest total changes, so `command-binding-selftest-r24` (pins 44/44) needs a successor row under the registry's supersession rule. The pinned bundle rows pin bundle digests, not the tool hash, so a tool change does not break them.

## A1 (adjacent, latent, not counted toward the verdict): registry row schema is not exact-key checked

- `registry-check.py:224–237` validates `expect.exit` and `expect.stdout_contains` only. Unknown keys are not rejected. `run_row` at line 652 reads `expect.get("stdout_contains", [])` and silently ignores any other key.
- Probe in /tmp/reschema-rc: a gate row with `expect {"exit": 0, "stdout_contain": ["NEEDLE-ABSENT"]}` (typo) prints `ROW typo-needle-probe expect=0 got=0 held`. The same row with the correct key prints `differs`. A misspelled needle key silently removes the stdout check.
- The live registry at c9ff09f has 54 rows. None has an unknown row key or unknown `expect` key, so this is latent rather than a current defect.
- I read "gate schema exact keys" as the command-binding bundle schema. The three named fixtures (unknown-expect-key, unknown-receipt-key, unknown-bundle-key) are all command-binding cases. If the registry owner reads it as the registry row schema too, the fix follows the same pattern: reject unknown keys in row and `expect` against an explicit allowed set.

## R1 (residual, not counted; outside the named invalid/duplicate pair)

- A duplicate receipt returns early at command-binding.py:94–96 and hides other findings. Probe: receipts [a, a], requirements [a, b]. Both the frozen draft and c9ff09f return (1, ["DUPLICATE_COMMAND"]), and MEMBERSHIP_MISMATCH is not reported. Exit 1 is the same class either way. Whether "exact finding sets" requires reporting both is a contract question for the owner.

## Verification gaps

- No lane gate, selftest, or registry run was executed in the lane. Bounds forbid it. All runs used scratch copies of c9ff09f.
- I ran the three active command-binding rows through `registry-check --only`. I did not run the other 51 registry rows.
- Producer authenticity, cold-read independence, and page coverage are out of scope for this claim. The tool docstring excludes them (command-binding.py:11–13).
- The intended section scope of the precedence rule is an inference (see F1).

## Tooling

No tools installed or upgraded. I used read-only git (`--no-optional-locks`), `git archive` into /tmp, python3 stdlib, and the c9ff09f copies of `command-binding.py` and `registry-check.py`. The scratch directories /tmp/reschema-c9f, /tmp/reschema-run, /tmp/reschema-prerev, and /tmp/reschema-rc were removed after the run.

Lane working tree at my status check (`git status --porcelain`) already held sibling-owned changes: modified `tools/mte-interop.py`, `corpus/SOURCES.md`, `.ufo/evidence/round-25/multitoken-cases.json`, `multitoken-mutants.spec`, and `guard-mutants.spec`; untracked `.ufo/evidence/round-25/build-disposition.py`, `c1-pins.py`, `census-start.*`, `.ufo/waves/round-25/record.json`, and `.ufo/waves/round-25/w1/`. I did not write any of them. `tools/command-binding.py` and `tools/registry.json` are unmodified in the working tree, so the c9ff09f comparison above stands.

R23-REATTACK SchemaPriority: FINDING
