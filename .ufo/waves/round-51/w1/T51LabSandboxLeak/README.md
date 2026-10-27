# T51LabSandboxLeak — receipts

Round 51 C2 sandbox-id leak confirmation (seat T51LabSandboxLeak). Gate: kagi `corpus/drift-pins.sh` @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`, 451 lines). Mutants rebuilt from `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; all ten byte-identical to the sweep's mutant shas (`mutants-sha.csv`). Suite form reproduced from `tools/mutate-and-run.sh`'s guarded sandbox (`h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" bash "$MUTANT" --selftest`).

Forms: **A** = sandbox `sandbox-<DEFECT_ID>` (sweep form); **B** = sandbox `sandbox-n<ordinal>` (neutral; one variable changed); **C** = sandbox named with a verdict word on purpose: `MOVED-COUNT-LINK` for the KILLED mutants, `GONE-AMBIG-SHAPE` for K_GONE_ARM. 3 repeats each; all repeats identical per (defect, form).

## A/B/C table

| defect | form | exit (3 reps) | fail cases | per-case failing line |
|---|---|---|---|---|
| K_MODE_CMP | A | 1 | 1 | drift-selftest: FAIL mode drift: exit 0 want 1; |
| K_MODE_CMP | B | 1 | 1 | drift-selftest: FAIL mode drift: exit 0 want 1; |
| K_MODE_CMP | C | 1 | 1 | drift-selftest: FAIL mode drift: exit 0 want 1; |
| K_GONE_ARM | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| K_GONE_ARM | B | 1 | 1 | drift-selftest: FAIL symbol gone: no /GONE/ in output; |
| K_GONE_ARM | C | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| K_AMBIG_GT | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| K_AMBIG_GT | B | 1 | 1 | drift-selftest: FAIL symbol ambiguous: no /AMBIG/ in output; |
| K_COUNT_GE | A | 1 | 1 | drift-selftest: FAIL count drift: no /COUNT.*#1->#2/ in output; |
| K_COUNT_GE | B | 1 | 1 | drift-selftest: FAIL count drift: no /COUNT.*#1->#2/ in output; |
| K_COUNT_GE | C | 1 | 1 | drift-selftest: FAIL count drift: no /COUNT.*#1->#2/ in output; |
| K_SHAPE_OPTIN | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| K_SHAPE_OPTIN | B | 1 | 1 | drift-selftest: FAIL shape drift: no /SHAPE/ in output; |
| S_SHA_CMP | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_SHA_CMP | B | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_HARDLINK | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_HARDLINK | B | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_POLICY | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_POLICY | B | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_DUP_UNIQ | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_DUP_UNIQ | B | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_USAGE_EXIT | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| S_USAGE_EXIT | B | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| ctrl | A | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |
| ctrl | B | 0 | 0 | DRIFT_SELFTEST: PASS (13 cases) |

All runs: `raw/<defect>-<form>-r<repeat>.out` (TSV: defect, ordinal, repeat, exit, fails, last line, failing lines). Summary of all runs: `table.tsv`.

## Minimal red/green pair (K_GONE_ARM)

- `red-gone-id.sh` — suite sandbox `sandbox-K_GONE_ARM`: selftest PASS (13/13), exit `0` (`red-gone-id.out`, `red-gone-id.exit`).
- `green-gone-neutral.sh` — neutral sandbox `sandbox-n2`: selftest FAIL (1/13), `drift-selftest: FAIL symbol gone: no /GONE/ in output`, exit `1` (`green-gone-neutral.out`, `green-gone-neutral.exit`).

## Files
- `table.tsv` — all runs (control + A/B/C × 3 repeats)
- `raw/` — raw per-run outputs
- `mutants-sha.csv` — build identity vs sweep mutant shas
- `red-gone-id.sh` / `green-gone-neutral.sh` (+ `.out`, `.exit`) — red/green pair
