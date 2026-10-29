# T57W1ScribeItemsR53x1to3 — routed items R53.1–R53.3 (round 57, wave 1)

Seat: T57W1ScribeItemsR53x1to3. Lane base `5e3569969b532310d2b8a3d130901757a3df356b` (tameshi-shokunin, master, 5e35699). Spot-check: `corpus/lessons/round-53-verifier-spotcheck.md`, added at `2ef0a5ad429de7f204b0e8138b2f36dcbb32a626` (`routed_at`). No lane file was edited; every fix is staged. Machine output: `T57W1ScribeItemsR53x1to3.json`; rows: `T57W1ScribeItemsR53x1to3/rows.json`; receipts: `T57W1ScribeItemsR53x1to3-receipts/`.

## Verdicts (against the tree at base)

| id | status at base | disposition | why (one line) |
|---|---|---|---|
| R53.1 | open | fixable-costly | Frozen round-53 `c1/measure.py` lines 94–97 still list the re-key dir without a trailing slash and match full paths, so `rekeyed=0/30` and `rekey-dir-count=0`; SCORECARD quotes `total=6` where the counter prints `total=37`. The round-54 successor counter fixes the class; the cited file did not change. |
| R53.2 | open | fixable-cheap | No `.ufo/evidence/round-53/after/` path exists at base (0 matches); LOG.md:2489–2490 and SCORECARD.md:2526, 2543 still name it in past tense. |
| R53.3 | open | fixable-costly | No round-53 `CONTROLS_B:` receipt exists under `.ufo/`; `control/break-fixtures.py` crashes at base with `IndexError` on line 99 (same pathspec defect as R53.1). |

Not `fixed`: no later lane commit changed the cited surfaces (`git log 2ef0a5a..5e35699 -- .ufo/evidence/round-53` is empty). The round-54 lesson's "FIXED" dispositions for R53.1 and R53.3 are successor-instrument fixes (round-54 counter, `round-54/control/controls-b.stdout`). They leave the round-53 bytes the items cite unchanged, so they do not meet contract rule (b). An L1 that treats round-53 as frozen history could record R53.1 as `declined` with a reason of at least 40 characters; I did not choose that.

Not `declined`: the lane can reach each fix; the frozen-file cost is recorded above instead.

## Verification sweeps (commands and results)

1. Resolver check of the drafted base rows, using `check_evidence` and `has_key` imported from the round-50 `measure.py` (`T57W1ScribeItemsR53x1to3-receipts/verify-base-rows.stdout`): `R53.1 resolves [] keyed 3`, `R53.2 resolves [] keyed 3`, `R53.3 resolves [] keyed 2`, `base rc=0`.
2. Post-fix variants against the fixture commit `cf61f0860ca1a89709bc5cf7172e65b5cee0e7b6` (rule `fixed`: commit touches the path, excerpt absent at `routed_at`, no ACK words; `verify-fix-rows.stdout`): all three `pass`.
3. Frozen round-53 counter `C1_R53` at base and at 88afa941 (`c1-frozen-counter-*.stdout`):
   - base `5e35699`: `credited=64 lost=0 rekeyed=0/30 readers=18/30 total=43 C1_R53_PASS=false` (exit 1).
   - 88afa941: `credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false` (exit 1). This reproduces the closure's numbers.
   - `git ls-tree --name-only 5e35699 .ufo/evidence/round-21/coldread` returns the directory itself (`ls-tree-trailing-slash-less.txt`). With the trailing slash the listing gives full paths (`ls-tree-with-slash-rekey-r53.txt`), so the full-path `re.fullmatch` still fails. Both defects must be fixed together.
4. Frozen round-53 counter `C2_R53` at 88afa941: `tmp_hits=0 … cr47=rc=2 docs=ok total=0 C2_R53_PASS=true` (exit 0).
5. Patched round-53 counter (staged copy) at 88afa941: `credited=58 lost=6 rekeyed=28/30 readers=25/30 total=8 C1_R53_PASS=false` (exit 1). The rekey arm now fires; the six lost sections are the closure's known miss.
6. Phase-B script:
   - Committed `control/break-fixtures.py` (`break-fixtures-frozen-at-base.stderr`): `IndexError: list index out of range` at line 99, before any control prints.
   - Staged patched copy at 88afa941 (`break-fixtures-patched-run.stdout`, exit 1): `CONTROLS_B: total=7 pass=6`. `PROBE_C1_CANDIDATE` is `verdict=false … expected=true FAIL`; the other six controls pass. The SCORECARD statement that the unmodified candidate printed true is therefore false for C1.
   - The C1 controls cannot discriminate. The frozen counter prints `PROBLEM rekey-dir-count=0` at base and at 88afa941 (`c1-frozen-counter-at-88afa941.stdout`), so every C1 fixture is false for that reason, whatever was planted.
7. Cold-read no-harm (`.ufo/evidence/round-21/coldread/measure.py --repo … --rev …`, score and coverage from the JSON):
   - base 5e35699: score 8, 64/64 credited (`coldread-monitor-at-base.json`).
   - base + SCORECARD/LOG diff (scratch clone, commit 4d9027c0): score 8, 64/64 (`coldread-monitor-scorecard-log-diff.json`).
   - base + all staged files (fixture cf61f086): score 8, 64/64 (`coldread-monitor-all-staged-at-fixture.json`).
   The round-53 counters and receipts are not in the cold-read ledger inputs (no `round-53/c1`, `round-53/control` or `round-53-verifier` in `ledger.json`). Three rekey-r53 trace receipts (`rekey-r53-651773ab9e32/traces/section-04.json`, `…/section-07.json`, `rekey-r53-a9773948087e/traces/section-04.json`) name SCORECARD.md as an external input; crediting was not affected.
8. Other greps (`T57W1ScribeItemsR53x1to3-receipts/`): `grep-CONTROLS_B-at-base.txt` (no round-53 tally); `grep-round-53-after-at-base.txt` (LOG 2490, SCORECARD 2507/2526/2543); `count-round-53-after-paths-at-base.txt` = 0; `round53-tree-commits-after-spotcheck.txt` (none).

## Staged files (under `.ufo/waves/round-57/w1/T57W1ScribeItemsR53x1to3/stage/`; the L1 copies them)

- `.ufo/evidence/round-53/c1/measure.py`: rekey discovery with a trailing-slash pathspec and basename match (lines 94–97). Full-file copy of the frozen file with only those lines changed. R53.1 cost: changes the round-53 freeze digest (`da89149…`) and makes the historical dead-arm record non-reproducible from the frozen bytes.
- `.ufo/evidence/round-53/control/break-fixtures.py`: the same discovery fix at lines 98–99. R53.3 cost: changes the round-53 freeze digest (`c80f5a8c…`).
- `.ufo/evidence/round-53/direct-runs/c1-at-88afa941.{stdout,exit}`: frozen counter, direct run at 88afa941 (exit 1). Additive.
- `.ufo/evidence/round-53/direct-runs/c2-at-88afa941.{stdout,exit}`: frozen C2 counter at 88afa941 (exit 0). Additive.
- `.ufo/evidence/round-53/direct-runs/c1-patched-counter-at-88afa941.{stdout,exit}`: patched counter, labelled as such (exit 1, `rekeyed=28/30`).
- `.ufo/evidence/round-53/control/controls-b.{stdout,exit}`: output of the patched phase-B run (exit 1). The line is `CONTROLS_B: total=7 pass=6`, not the `CONTROLS_B: n/n as pre-registered` form that the round-54 deciding gate greps for.
- `SCORECARD.md.diff` (`diff -u` against base, 46 lines) and `LOG.md.diff` (13 lines). These correct the past-tense pointers (`after/` → "none committed", R53.2), mark the phase-B claim as unreceipted (R53.3), and replace the quoted `total=6` with `total=37` (R53.1). Applied to a clone, the cold-read monitor stays 64/64.

Cheap part (R53.2): the two diffs plus the three additive `direct-runs/` receipts. Costly part: the two frozen round-53 scripts. The L1 may accept the diffs and receipts while declining the frozen-script patches; R53.1 and R53.3 would then stay open with the disposition recorded.

## Caveats the L1 must act on

- **Base rows and staged-fix rows are mutually exclusive.** The base rows cite SCORECARD.md 2518–2519, 2526, 2543, 2550–2551 and LOG.md 2489–2490, which the staged diffs rewrite; applying the diffs makes those excerpts fail. If the L1 lands the staged fixes, use `staged_fix_variant` in `rows.json` (each has `status: fixed`, a commit placeholder, evidence and keys, and was verified against the fixture). The L1 must substitute its own commit hash.
- **Open rows must be named in the newest `**Planned (round` paragraph of SCORECARD.md at REV.** At base that paragraph is round 55's and names none of R53.x. The planned-id regex in the round-50 counter is `\bR4\d\.\d+\b`, so it would never match an R53 id; the round-57 counter needs a wider pattern, or the rows must change. I did not check the round-57 counter (it is not in the tree at base).
- **Frozen round-53 bytes.** The staged `c1/measure.py` and `break-fixtures.py` diverge from round-53 `freeze.json`; the round-53 freeze verification would fail on them. Copy them only if the L1 accepts a re-freeze or a recorded amendment.
- **SCORECARD/LOG edits are shared.** The L1 writes SCORECARD and LOG at close; the diffs need a rebase onto whatever it has already changed.
- **Tools:** none installed or upgraded. Python 3 standard library and git only.

## Caution about my own receipts

- The patched break-fixtures receipt comes from a modified copy of the frozen script. The receipt file name and this report both say so.
- The `direct-runs/c1-patched-counter-at-88afa941` receipt is a run of the patched counter, not the frozen one.

## Not verified

- No round-57 counter run: `.ufo/evidence/round-57/…` does not exist at base; the L1 stages it.
- Whether the patched counter is correct beyond the arm firing (28/30 rekeyed, matching the closure's "28 of 30") is not settled here.
- The fixture commit `cf61f086` exists only in scratch; the L1 must re-verify the rows at its own content commit.
