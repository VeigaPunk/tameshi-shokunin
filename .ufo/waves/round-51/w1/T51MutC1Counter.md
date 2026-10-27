# T51MutC1Counter — C1 counter mutation probe

## Method and baseline

Probed the frozen `.ufo/evidence/round-51/c1/measure.py` bytes (freeze commit `84aa673a1a476e48ccf239335696f0518d08bae7`, SHA-256 `ed6968327a2dcecc2b0142c27c665b184a41abe0103268a90fab5b895743b919`). The detector was the counter's `--selftest` (expected six cases, zero failures) plus the committed C1 control fixtures `CTL_0`, `CTL_S022`, `CTL_ALLHELD`, `CTL_NOPTR`, `CTL_REWRITE` (expected each exit 1 / `C1_R51_PASS=false`). For mutant runs I used a scratch-only adapter copied from `control/controls.py`: it kept the committed C1 fixture edits and runner, filtered out C2/C3, and allowed the counter executable to be overridden by each isolated mutant copy. No lane file was edited.

Pristine: selftest `cases=6 failed=0`; all five controls were `as-pre-registered`, `unexpected=0`. Restored/pristine-copy rerun: same outputs. The lane counter SHA-256 before and after was identical to the frozen and scratch pristine hash above. Per-mutant original and mutant hashes, selftest result, and control unexpected count are in `T51MutC1Counter.receipts/mutation-matrix.tsv`.

## Mutation outcomes

Line references below are in `.ufo/evidence/round-51/c1/measure.py`; `nl -ba .ufo/evidence/round-51/c1/measure.py` shows the cited source lines. Each change was applied alone to a copy of the original bytes.

| Mutant (source line) | Single weakening | Detector result |
|---|---|---|
| M01 (82) | Keep the first frontier table instead of replacing it with the last. | **KILLED** by selftest (`failed=1`); controls all remained expected-false. |
| M02 (108) | Accept one or more rows instead of requiring exactly one. | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |
| M03 (124) | Require a round value but ignore whether it equals the frozen round. | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |
| M04 (133) | Raise the pointer-span maximum from 5 to 50 line differences. | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |
| M05 (136) | Require the F-id token in pointer text but omit the expected-status phrase check. | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |
| M06 (183) | Treat any README as preserving the required base prefix. | **KILLED** by selftest (`failed=1`) and `CTL_REWRITE` (control unexpected). |
| M07 (32) | Ignore indented SOURCES rows by requiring a column-zero pipe. | **KILLED** by selftest (`failed=1`); controls unexpected=0. |
| M08 (166) | Skip existence checks for mined used-by paths. | **KILLED** by selftest (`failed=1`); controls unexpected=0. |
| M09 (158) | Ignore queued rows that name a used-by path. | **KILLED** by selftest (`failed=1`); controls unexpected=0. |
| M10 (120) | Accept `held` whenever it is a substring of the expected status (`partly held`). | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |
| M12 (75) | Recognize a table whose second header is not `ground`. | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |
| M13 (128) | Initialize every status row as already having a valid pointer. | **KILLED** by selftest (`failed=2`) and `CTL_NOPTR` (control unexpected). |
| M14 (277) | Return CLI success regardless of the measured total. | **KILLED** by controls (all five unexpected); selftest itself passed (`failed=0`). |
| M15 (161) | Ignore `mined` rows with no used-by path. | **SURVIVED**; selftest `failed=0`, controls unexpected=0. |

Result: 7 killed, 7 survived out of 14 behavior-bearing single edits. The baseline and every run's actual output are retained in the receipt bundle.

## Surviving blind spots: forged witnesses

Each witness was created in an isolated scratch clone at the frozen tree, with S022 corrected to avoid an unrelated conflict where applicable. The mutant accepted (`rc=0`, `total=0`, `C1_R51_PASS=true`) while the pristine counter rejected the same bytes (`rc=1`, `C1_R51_PASS=false`):

- **M02, duplicate frontier ID:** append an otherwise-correct table, then append a second F1 row with status `open`. The mutant uses the first F1 row and ignores the contradictory duplicate; pristine reports `frontier_bad=1`. Receipt: `M02_duplicate_rows-forge.txt`.
- **M03, wrong round:** append correct status words but use round 99 for every non-open status. Mutant passes; pristine reports `frontier_bad=7`. Receipt: `M03_ignore_round-forge.txt`.
- **M04, overlong pointer:** give F1 pointer `README.md:385-397` (13 lines, containing F1 and “held”). Mutant accepts the span; pristine rejects it and reports `frontier_bad=1`. Receipt: `M04_pointer_span-forge.txt`.
- **M05, unsupported status phrase:** give F1 pointer `README.md:385`, which contains the F1 token but not the expected status phrase. Mutant passes; pristine reports `frontier_bad=1`. Receipt: `M05_pointer_phrase-forge.txt`.
- **M10, collapsed status:** write `held` rather than `partly held` for F2, F4, and F8 while keeping their supporting pointers. Mutant passes; pristine reports `frontier_bad=3`. Receipt: `M10_held_for_partly-forge.txt`.
- **M12, wrong table header:** append the rows under `| id | label | candidate sources | status | next falsifiable move |`, not an `id | ground` header. Mutant treats it as the frontier table and passes; pristine selects the stale base table and reports `frontier_bad=10`. Receipt: `M12_no_ground_header-forge.txt`.
- **M15, mined without used-by:** append a 11-cell S999 row with status `mined` and used-by `—`, alongside the otherwise-correct frontier table. Mutant passes; pristine reports `status_conflicts=1`. Receipt: `M15_skip_mined_empty-forge.txt`.

## Restoration evidence

Pristine/restored selftest both returned 0 with `C1_R51_SELFTEST: cases=6 failed=0`; pristine/restored C1 controls both returned 0 with `CONTROLS: total=5 unexpected=0`. The lane file and pristine scratch copy both hash to `ed6968327a2dcecc2b0142c27c665b184a41abe0103268a90fab5b895743b919` after probing, matching the pre-probe hash. Full outputs and hashes are in `T51MutC1Counter.receipts/` (`pristine-*`, `restored-*`, `hashes-and-restoration.txt`, and individual mutant/forge receipts).

## Summary
- 14 isolated, behavior-bearing single-edit mutants tested; 7 killed, 7 survived.
- All survivors have a forged fixture where mutant passes and pristine fails.
- Selftest catches the indented-row, path-existence, queued-conflict, and first-table weakenings; controls additionally catch forced-success and no-pointer mutations.
- No lane bytes changed; pristine/restored hashes match.
