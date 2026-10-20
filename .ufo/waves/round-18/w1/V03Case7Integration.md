# Round 16 case 7 integration → case 8 checklist

**Axes:** depth (recorded mutation-leg count) and calibration (pinned, pre-registered evidence). **Scope:** tracked lane bytes at `183f87b899e6cae46be98d251cbc87fb5118f6ca`; the working-tree `HEAD` matched this revision. The status check showed only untracked round-18 work, not edits to the inspected tracked files.

## Reconstructed sequence and invariant

Read-only history commands (exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline --decorate --reverse --ancestry-path e69b488^..05a2247
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --no-patch --format='%H%n%P%n%s' e69b488 c699c8c 05a2247
```

The first command prints **e69b488 → c699c8c → 05a2247**. Their parent links are respectively `0baf52e…`, `e69b488…`, and `c699c8c…`; commit dates are 10:39:59, 10:49:37, and 11:18:08 (-03:00), as recorded by `git show`.

1. **Pre-register before running mutants — e69b488.** `git show --name-status e69b488` (exit 0) shows new `.ufo/evidence/round-16/round-gate/{predictions.json,round-gate.defects.spec,suite.txt}` and wave-1 reports, but no runner or case-note integration. `predictions.json:2-7,73` records the schema, target/rev/blob, suite, and registration time; `corpus/knowledge/mutation-case-kumitate-round-gate.md:35-48` records that the spec hash `e99b87eb…11c4` matched the later sweep copy. Ten IDs were predicted, five kill-aimed and five hole-aimed.
2. **Sweep after registration, before embedding.** The retained `.ufo/evidence/round-16/round-gate/sweep/sweep.log:1-5,104-106` gives the sweep time `13:40:15Z` (10:40:15 -03:00), target pin, spec, green pristine control (`exit=0`), and `MUTATE: DONE` with 5 killed / 5 survived / 0 inconclusive. The log identifies the pre-integration runner SHA `75ed934d…19adc5`; `results.tsv:1-11` records all ten per-ID outcomes, matching predictions. `SKILL.md:1766-1773` retains the reproduction command shape using a byte copy, `--target`, `--defects`, `--suite`, `--label`, and scratch `--workdir`. The original sweep log does not include an overall shell `rc=` trailer; do not invent one from its summary.
3. **Embed measured leg and documentation — c699c8c.** `git show --name-status c699c8c` (exit 0) lists modifications to `tools/mutate-and-run.sh`, `PROVINCE.md`, and `SKILL.md`; additions of `corpus/knowledge/mutation-case-kumitate-round-gate.md` and evidence receipts; and a `corpus/README.md` update. The runner embeds the pre-registered defect spec verbatim (`tools/mutate-and-run.sh:942-1005`), pins `round-gate.mjs` (`:604-605`), and carries its own suite wrapper. The case note specifies the pin, suite hazards, measured table, survivors, and limits (`corpus/knowledge/mutation-case-kumitate-round-gate.md:15-55,117-147`). The province append marks the seventh recorded mutation leg and the target as a read-only `kumitate scripts/*` primary surface (`PROVINCE.md:49-57`). The SKILL case section records the result and operational rules (`SKILL.md:1754-1796`); the corpus index adds the note row (`corpus/README.md:219-237`).
4. **Falsify silent count drift — 05a2247.** This commit is the runner/SKILL follow-up, not the first embedding. `legcount-redbefore-mutant.txt:71-85` records the pre-fix counterexample: seven files and calls but only six selftest tuples, `81/82` checks, `rc=1`. The new selftest cross-checks calls, generated specs, declared `nlegs`, and tuples, then verifies each tuple’s table IDs and kill/survivor counts (`tools/mutate-and-run.sh:1282-1289,1792-1825`). The retained final receipt passes those checks and the embedded `js-round-gate` tuple: `runner-selftest.txt:71-87` reports `83/83`, `VERDICT: PASS`, `rc=0`. The recorded regression receipt reports all seven legs exact, `REGRESSION: PASS (cases=7 passed=7...)`, `rc=0` (`runner-regression.txt:36-43`).
5. **Record score only after measurement.** `017a2b0` (parent `09ee1d0`, 11:47:11 -03:00) is the later commit that adds `SCORECARD.md`; its C1 row records ledger cases `6 → 7`, 5/10 killed, predictions committed before sweep, regression pass, and 7/7/7 agreement (`SCORECARD.md:568-571`). The score is not part of the e69 preregistration or the c699 embedding commit.

**Last-known-good invariant:** every regression leg replays its pinned source/spec against its recorded verdict table; the selftest also makes the declared leg count agree with calls, generated specs, and per-leg tuples. The divergence exposed between embedding and 05a2247 was that removing a tuple could otherwise shrink the selftest silently; the red-before receipt and new guard prove the correction. The seven entries at this point are **recorded mutation cases**, not the count of kumitate’s product gates.

## `TABLE_ROUNDGATE` contract

At the requested revision, `tools/mutate-and-run.sh:604-612` pins rev/hash and declares this exact 10-pair table:

```sh
TABLE_ROUNDGATE='A1:KILLED,A3:KILLED,B1:KILLED,E3:KILLED,C1060:KILLED,C1059:SURVIVED,A2:SURVIVED,B2:SURVIVED,CKIND:SURVIVED,E1:SURVIVED'
```

Wire shape: comma-separated `ID:VERDICT` pairs, no spaces; verdicts are `KILLED` or `SURVIVED`. The order follows the preregistered/result rows, not lexical ID order. `table_lookup` splits on commas and then the first colon; `table_count` and `table_total` count verdicts/rows (`tools/mutate-and-run.sh:615-637`). The integration call supplies the pinned path, hash, revision, embedded spec, guarded suite, and table (`:1276-1279`); the selftest tuple independently declares expected total and killed count (`:1798-1805`) and compares spec IDs to table IDs and counts (`:1813-1825`). The format is a compact serialized verdict ledger, not prose or a TSV transcription.

## File inventory and README distinction

- `tools/mutate-and-run.sh`: c699 embeds leg 7; 05a adds cross-list leg-count checks. Current anchors: `:604-612`, `:942-1005`, `:1276-1289`, `:1792-1825`.
- `corpus/knowledge/mutation-case-kumitate-round-gate.md`: c699 adds the evidence-led case record; 3490708 later edits it. Current anchors: `:1-55,117-152`.
- `PROVINCE.md`: c699 appends round-16 scope; 3490708 supplies a later correction. Current anchors: `:49-71`.
- `SKILL.md`: c699 adds the case section; 05a repairs it and subsequent round-17 commits continue editing the page. Current case anchors: `:1754-1796`.
- `corpus/README.md`: c699 appends the knowledge-index row, `:219-237`.
- `SCORECARD.md`: later measurement commit 017a2b0 records C1, `:568-571`.
- Root `README.md`: the scoped `git log ... -- README.md` returned no entries between e69b488’s parent and the requested revision; it remains a generic lane landing page. The round-16 README integration was **`corpus/README.md`**, not root `README.md`.

The required `lsp` device/server was not exposed in the available session tools. I therefore used commit ancestry/name-status, direct committed-file reads, and retained receipts; text search was navigation only, not semantic proof.

## Ordered integration checklist for case 8

1. **Establish scope and pin first.** Treat the declared target as kumitate `scripts/sources-check.mjs` at rev `0acb7752d19058b953ebbeba253b1e35f6548de5`, blob SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`; verify the committed object, mode, byte size, and the claimed 46-check `--selftest` before designing defects. It remains a read-only primary surface under `PROVINCE.md:7-12`; do not confuse the already-existing source-check gate with the count of recorded mutation legs.
2. **Freeze the specification and predictions.** Define the ten one-edit mutants, exact old/new strings, IDs, rationale, prediction and any rejected candidates. Record the suite and its verdict oracle. Commit the spec and predictions before any mutant run, and retain their hashes so sweep `spec.copy` can be compared byte-for-byte. This ordering is evidenced by e69b488 → sweep timing and the spec-copy identity above.
3. **Run the sweep on pinned bytes in scratch.** Materialize the source from its git object, run the mutation tool with a separate workdir, and retain the runner SHA, pristine control result, per-defect output, mutant hashes, restore proof, and explicit exit status. Decide from this target’s evidence whether output comparison is stable and whether environment isolation is needed; round-gate’s `env -i` wrapper and exit-only oracle addressed its own Git/TMPDIR and `mkdtemp` hazards, not an automatically transferable assumption.
4. **Resolve every survivor before claiming a gap.** Use a pristine-vs-mutant off-suite witness or document an equivalence argument; preserve probe commands and both outcomes. Keep predicted and measured verdicts side-by-side and report prediction accuracy separately from kill rate, as the case-7 note does (`:50-77,98-115,134-152`).
5. **Embed only the measured leg.** In the runner, add the exact immutable target pin, embedded pre-registered spec, recorded comma-delimited `ID:KILLED|SURVIVED` table, guarded suite if evidenced, regression call, and the `js-sources-check` leg label. Keep the table’s IDs exactly equal to the spec and measured rows. Do not run or claim the final replay before this integration commit.
6. **Raise every count together and test the dropped-tuple fault.** Update the leg header/list, regression calls, emitted spec files, declared `nlegs`, and selftest tuple from seven to eight. Assert all five counts agree and each tuple’s spec/table IDs, total, and killed/survived counts agree; retain a negative fixture that removes the new tuple and fails. The case-7 mutant receipt (`81/82`, six tuples) is the concrete falsifier motivating this guard.
7. **Replay and retain receipts.** Run `bash tools/mutate-and-run.sh --regression` and retain a `cases=8 passed=8` exit-0 receipt with the new table exact and no flips; run `--selftest` and retain its complete output/runner SHA. The expected total selftest count should come from the actual assertions, not a guessed increment.
8. **Append narrative/index/score only from those receipts.** Add the case note and `corpus/README.md` row; append the measured recorded-case change in PROVINCE/SKILL where appropriate; update SCORECARD’s count and claim only after the measured revision exists. Do not edit root `README.md` solely because “README” is listed—the round-16 precedent touched `corpus/README.md` only. Preserve the separation between preregistration, sweep, embedding, count-falsifier, and later score record.

**Confidence:** high for case-7 chronology, runner/table contract, and tracked-file mapping (direct parent links, path lists, line-anchored code and receipts); medium for case-8 checklist details that must be confirmed against the declared source-check bytes and its actual runtime behavior.

**Verdict: built — the case-7 integration path is reconstructed and the case-8 checklist is evidence-anchored.**