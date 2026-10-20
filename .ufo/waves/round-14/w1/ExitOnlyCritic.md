# ExitOnlyCritic: round 14, wave 1

Seat: critic, leaf, read-only. Lane HEAD is `d6809df7775338f000e44c8a916067b8866867fb`, the same as the baseline. I did not run any check argv, selftest, gate, build or lint. Every observation below comes from reading or parsing committed bytes with JSON/sha256 in Python. I did not install or update any tool.

At the time of reading, `tools/evidence-disposition.py`, `.ufo/evidence/round-14/dispositions-before.json` and `dispositions.json` **did not exist**. This report therefore reviews the agreed contract, not finished code.

## Verdict

**The historical `producer_before` exit 1 does not show the mechanism failing. It shows a setup crash.** It passed only because the round-13 harness compared exit codes and nothing else. Every check in `verification.json` stores just `exit`, `expected_exit` and `exit_matches`. None of them evaluates `contains`.

## Counterexample (all literal and committed)

1. **The run crashed before reaching the target assertion.** In `verification.json`, the `producer_before` check ran `python3 .ufo/evidence/round-13/producer-before.py selftest` and got exit 1 with `exit_matches: true`. Its stderr ends with:
   `FileNotFoundError: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/tools/mutate-and-run.sh'`
   - Cause: `producer-before.py:93,95` sets `REPO = Path(__file__).resolve().parent.parent` and `RUNNER = REPO/"tools"/...`. Moving the file into `.ufo/evidence/round-13/` makes REPO resolve to `.ufo/evidence`.
   - The crash happens at `:1478` (`sha256_file(RUNNER)`), which is fixture setup before the summary checks. The target `check(...)` sits at `:1542-1544`.
2. **The crashed output is an exact prefix of the oracle's output and stops before the target.** The crashed stdout has 34 lines, all `ok`. Those 34 lines equal the first 34 of the 43 lines from `producer_before_oracle`. Oracle lines 35–38 never ran in the crashed run. The target is oracle line 39: `check summary preserves top-level exposed declaration kind FAIL`. No `WITNESS_SELFTEST:` or `VERDICT:` line was printed.
3. **Exit codes collide.** `producer-before.py:118` defines `EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64`.
   - `cmd_selftest` has `try/finally` with no `except`, so the uncaught `FileNotFoundError` leaves Python with exit 1.
   - That is the same code as a real assertion `EXIT_FAIL` (`:1568-1569`).
   - By the producer's own contract this was a could-not-evaluate case (2). The exit code turned it into a semantic failure.
4. **The stale expectation would not discriminate even if the assertion had been reached.** `expected.json` `producer_before.contains` is `summary preserves top-level exposed declaration kind`, with no verdict suffix.
   - `producer_after_oracle` stdout, which is green, also contains that substring, because the line ends in `ok`.
   - So exit 1 plus this needle can be met by "target ok, some other check failed".
   - It never pins red-on-target.
   - The real discriminator is the original `producer_before_oracle` row, which requires the suffix `FAIL`.
5. **A bare `FAIL` token gives a false positive.** The crashed stdout contains `FAIL` inside an `ok` line: `check FAIL without denominator is inconclusive, not a crash ok`. Any `"FAIL" in stdout` shortcut would score the crash as red.

## Target-assertion discriminator (what the evidence actually proves)

The proof is the oracle pair, not the historical row:

- **Same assertion and runner in both runs.** `producer-oracle.py` copies `--source` and `--runner` into a temp `tools/` directory, which fixes the path layout, then runs `selftest`. Both oracle runs use the same oracle (sha `d5ae0bd4…`) and the same runner.
- **Exactly 3 of 43 lines differ between the before and after oracle stdout:**
  - line 39: `... kind FAIL` → `... kind ok`
  - line 42: `WITNESS_SELFTEST: 40/41 pass` → `41/41 pass`
  - line 43: `VERDICT: FAIL` → `PASS`
  - Both stderrs are `''`.
- **The target is the only failure before the fix.** "40/41 + target FAIL" means no other check failed. Together with the single source delta (`producer-oracle-repair.json` `single_delta`; independently diffed in the round-13 lesson, lines 120–122), this attributes red-then-green to the nested→top-level kind getter.
- **What exit-only cannot prove:**
  - which check failed;
  - whether the check list was enumerated completely;
  - whether the failure was "cannot evaluate" or a semantic failure.
  - SKILL.md:200-204 already says: "Adjudicate exit AND token/verdict; never exit alone."

## The expected stale row

- **What it records.** `expected_checks.producer_before` records the intent before relocation. It cannot be satisfied by the raw receipt: the needle is absent from both stdout and stderr.
- **What already superseded it.** Supersession appears in prose in three places:
  - `producer-oracle-repair.json` `supersedes`;
  - `verification-verdict.json` `excluded_initial_failure`, and that file has no `producer_before` row;
  - lesson routed item 1.
- **Correct round-14 disposition:**
  - keep the raw check row byte-identical and point to it;
  - mark it `superseded`, with a reason naming the path-layout crash before the target;
  - list both replacement rows, `superseded_by: [producer_before_oracle, producer_after_oracle]`;
  - do **not** mark it effective-pass by exit, and do not reinterpret the needle.

## Static read of the contract's predicates against the receipts (no execution)

Reading stdout only:

- 11 of 12 rows meet their original predicates.
- `producer_before` fails on `contains` and passes on exit.
- Every `contains` needle that is met appears in stdout; none appears only in stderr.
- All 13 `expected.inputs` digests match HEAD bytes.

## Risks and smallest safe corrections for Gate and DispositionSpec

1. **R1 (high, calibration): `dispositions-before.json` must fail with `producer_before` named.**
   - Expected result: exit 1 with a stable `contains`-mismatch finding on `producer_before`, not a pass on the exit match.
   - The output should show the raw check as `exit_ok=true, contains_ok=false`. The exit match must never count as partial credit.
   - The selftest's "exit-only false positive" fixture should be an exit-1 crash whose stdout lacks the needle.
2. **R2 (high): search `contains` in `stdout` only.**
   - In every receipt, the target lines are in stdout and stderr is `''` wherever a needle is met.
   - Joining stdout and stderr lets a Python traceback through. A traceback that echoes the source line `check("summary preserves top-level exposed declaration kind",` would meet the stale needle when the program crashes inside that statement. [INFERENCE] This depends on the CPython traceback source excerpt; I did not execute it.
   - Note: round-14 `measure.py:40` joins `stdout+stderr`. That is harmless for its present/absent measurement here (False), but the gate should not copy it.
3. **R3 (medium): the replacement rows keep their original, verdict-bearing needles.**
   - `producer_before_oracle` must keep the `...kind FAIL` suffix plus exit 1.
   - `producer_after_oracle` must keep `WITNESS_SELFTEST: 41/41 pass` plus exit 0.
   - Do not "harmonize" either needle with the stale row's needle, which has no suffix.
   - The 40/41 sole-failure fact belongs in the disposition `reason` text as evidence. It must not be a new predicate, because the contract enforces only the original fields.
4. **R4 (medium): the `pin_live` structured keys are not literal stdout keys.**
   - Parsed stdout has no `rows` or `statuses` keys. It has `counts={legs:6, unchanged:3, changed:3, unavailable:0}`, `legs[6]` each with `content_status`, and top-level plus per-leg `result_reuse`.
   - The gate must state the mapping explicitly:
     - `rows` ↔ `len(legs)` and `counts.legs`;
     - `statuses` ↔ the `counts` subset, cross-checked against a `Counter(content_status)` where missing keys count as 0;
     - `result_reuse` ↔ the top level and every leg.
   - A literal-key lookup gives a false exit-1 mismatch. A lookup that ignores missing keys gives a false pass.
   - `metadata_old_null` and `metadata_corrected` do expose `id` and `reason` directly as top-level JSON keys.
5. **R5 (medium): count mismatch in the goal text.**
   - The goal says "All13 expected rows", but `expected_checks` has **12** keys.
   - The 13 is the count of `expected.inputs`.
   - Correct statement: 11 effective + 1 superseded in the after file; 12 effective in the before file. No row should be invented to reach 13.
6. **R6 (low, tradeoff):** the gate checks `expected.inputs` against the working tree. All 13 match at d6809df. Any later edit to `tools/{bash-witness-study.py, pin-disposition.py, witness-metadata.py, mutate-and-run.sh}` will make the reconciliation exit 2 permanently. This is acceptable as fail-closed behavior, but say so in the report and lesson; it must not be "fixed" by re-pinning history.
7. **R7 (low): the gate must not execute any receipt argv.** This includes the oracles. Replacement evidence is the retained `producer-oracle-repair.json` receipt, pinned in `inputs`.

## Checks L1 should run after all seats finish

1. `python3 tools/evidence-disposition.py --selftest`: exit 0. The tally must include an exit-1 crash-without-needle fixture rejected with a stable ID (R1). Ideally it also includes a traceback-echo-needle fixture (R2).
2. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json`: **exit 1**. Exactly one failed expectation, `producer_before`, with exit matched and contains mismatched. The other 11 are effective and pass.
3. The same command with `dispositions.json`: **exit 0**. `producer_before` is superseded by both oracle rows; each oracle row passes its original needle and exit.
4. Mutation spot-checks on temp copies only, never on the round-13 files:
   - drop the `FAIL` suffix from the replacement row: must exit 1 or be rejected;
   - remove one replacement from `superseded_by`: exit 1;
   - flip one pinned digest: exit 2.
5. `git diff --quiet d6809df -- .ufo/evidence/round-13 .ufo/evidence/round-12 tools/mutate-and-run.sh`: exit 0 (historical bytes unchanged). The raw files must keep these sha256 values:
   - `verification.json` `a02718e9…f06f`
   - `producer-oracle-repair.json` `df83a729…ef8d`
   - `expected.json` `a0160794…4336`
