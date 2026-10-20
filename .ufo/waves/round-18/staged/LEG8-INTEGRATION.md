# Round 18 leg 8 integration

The staged `tools/mutate-and-run.sh` starts from lane commit
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. It wires `js-sources-check` to
kumitate `scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5`,
blob SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`
(mode `100755`). The implementation is mechanically integrated; the following
marked values are intentionally temporary and must be replaced by L1 from the
round-18 pre-registration and measured sweep before landing.

## Required placeholder replacements

1. **Header count — `tools/mutate-and-run.sh:93`.** Replace `0/10` with the
   measured killed/total count. Keep the row in the `#   js-... path COUNT`
   form matched by command D's ledger regex.
2. **Header provenance — lines 99–101 and 107–108.** Replace the prose describing
   temporary two-defect fixtures and pending measurement with the actual
   pre-registration source and measured result. The source path at line 98 is
   `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`.
3. **Recorded table — lines 620–622.** Replace
   `TABLE_SOURCESCHECK='R18D1:KILLED,R18D2:KILLED'` with the complete measured
   `ID:KILLED|SURVIVED,...` table in the pre-registered spec's order. Update or
   remove the adjacent `PLACEHOLDER ONLY` comment.
4. **Embedded spec — lines 1016–1028.** Replace the complete contents of the
   `js-sources-check.spec` heredoc with the pre-registered
   `.ufo/evidence/round-18/sources-check/sources-check.defects.spec` verbatim.
   Remove/update its `PLACEHOLDER ONLY` comments.
5. **Selftest tuple counts — lines 1835–1836.** Replace `:2:2` with the measured
   defect total and killed count respectively. Keep the `js-sources-check`
   tuple in the array (it is the leg-presence assertion); remove/update the
   adjacent `PLACEHOLDER` comment.

The revision and SHA-256 pin constants (`PIN_SOURCESCHECK`, `REV_SOURCESCHECK`)
are already populated and should remain unchanged.

## Integration evidence

- In an isolated `/tmp` fleet-mirror clone, the committed baseline runner's
  `--selftest` exited 0 with `MUTATE_SELFTEST: 95/95 pass`.
- With the staged runner and the two-defect integration fixture installed,
  `--selftest` exited 0 with `MUTATE_SELFTEST: 96/96 pass`.
- `--regression --keep` exited 0: all eight cases passed. The dummy leg reported
  `defects=2 killed=2 survived=0 inconclusive=0`, table `match=2/2`, and
  `REGRESSION_CASE js-sources-check: PASS`.
- Removing the leg-8 selftest tuple in a temporary clone produced
  `FAIL leg-count agreement: selftest leg tuples=7 (want 8)` and exit 1. The
  staged file was not modified for this red-before check.

The complete output receipts and command details are in the executor report at
`.ufo/waves/round-18/w1/X02RunnerLeg8.md`.
