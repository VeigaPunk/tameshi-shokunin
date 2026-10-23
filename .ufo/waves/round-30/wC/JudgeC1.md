JUDGE C1: unprovable-but-better

Non-author review of exploratory claim C1 (`.ufo/evidence/round-30/contract-amendment-4.json` `exploratory_claim`), axis operability, surface = the `--regression` case-tally block of `tools/mutate-and-run.sh` plus the runner's `--selftest` as its detector. Head under review: `bb681566b18211adf8ae9c28df91e17678e3f545`; base: `9ed6db840dc97a0a5f4758b6b5f60cee83a61645`. I did not write or alter any of the reviewed content. All runs in my own clone `/fast/scratch/hyaku/tameshi-r30a3-seats/JudgeC1/c` (detached at `bb681566…`) and scratch copies beside it, with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset.

## What the change is (diff base→head, `tools/mutate-and-run.sh` only)

- Header comment: exit map extended with the SETUP "case-tally mismatch" outcome (lines ~131-136).
- `run_regression`: a completeness guard inserted after the existing FAIL and SETUP branches and before the PASS print (`bb681566:1453-1461`): `if (( npass + nfail + nsetup != nlegs ))` prints `REGRESSION: SETUP (case-tally mismatch: cases=N counted=M)`, keeps the workdir, exits 2.
- `selftest`: a tally harness (`bb681566:1989-2038`) that extracts the tally block from `$SELF` by the literal `  local nlegs=9 npass=0 nfail=0 nsetup=0 st` marker, reads the nine leg-status names from `run_regression`'s `st_*=$?` lines (not from the loop), then runs the extracted block in separate Bash processes under fixed status vectors: all-zero; single 1 and single 2 at each of nine positions (exact first line + exit each); four multi/unknown vectors (`1 1`, `2 2`, `1 2`, `3`) from the MutateTallyExtra survivor set; and a guard stress case that deletes the loop's last operand and requires `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)`, exit 2. Selftest total went from 101 to 106 cases (base was 97 at round-29; the other cases predate).

## Evidence at head

Clone at `bb681566…`; `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 timeout 300 bash tools/mutate-and-run.sh --selftest`:
- `MUTATE_SELFTEST: 106/106 pass`, `VERDICT: PASS`, `EXIT=0`, ~6.9 s wall. All nine `tally harness:` cases PASS, including `loop missing one operand -> SETUP case-tally mismatch, exit 2`.

Base has no guard: `git show 9ed6db84:tools/mutate-and-run.sh | grep -n 'case-tally\|npass + nfail'` → exit 1 (no match); base loop at `1425-1438` is the unguarded tally of `.ufo/waves/round-29/w1/MutateLegSum.md`.

## Dropped-operand mutant (the named defect)

Copy `mutant.sh` (pristine head copy) with line 1433 changed to remove `"$st_citecheck"` — the round-29 MutateLegSum mutation.

- `--selftest` on the mutant: `MUTATE_SELFTEST: 98/106 pass`, `VERDICT: FAIL`, `EXIT=1`. All eight behavioral harness cases fail (the extracted block now counts 8 statuses, so every vector produces `case-tally mismatch` instead of its expected line), and the guard-stress case also fails: its sed removes a ninth operand from the already-mutated loop, so the block prints `counted=7` where the stress requires the exact `counted=8` line. Only tally-harness lines fail; every leg/spec/tuple structural check still passes (98 PASS lines elsewhere). At base this same mutant ran `97/97`, exit 0 (MutateLegSum.md:143-144).
- Runtime probe on the mutant's extracted block, fixed statuses `0 0 0 0 0 0 0 0 {0,1,2}` for the dropped leg: each prints `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)`, exit 2. At base the identical harness printed `REGRESSION: PASS (cases=9 passed=8…)` exit 0 for all three (MutateLegSum.md:103-114). The named surface — a tally that silently passes with a leg uncounted — now refuses loudly at both layers.

## No-harm check on other behavior

- The guard is `!=` behind the existing FAIL and SETUP branches, so pristine runs (sum always 9) are unreachable by it; FAIL-before-SETUP precedence is unchanged. Every pre-existing selftest case still passes at head (106/106 vs. 97/97 at r29 base), so no asserted line or exit changed.
- When a dropped leg's uncounted status is 1, the mutant still enters the SETUP-mismatch refusal rather than FAIL; exit 2 instead of 1. That is a refusal where base printed false PASS — directionally honest, and it keeps the workdir like other SETUPs. No path that printed PASS at base is altered.
- The selftest additions only add cases; the extraction asserts `${#tnames[@]} -eq 9` and fails loudly (`st` line) rather than silently skipping if the marker or names move.

## Residual risk (why "unprovable" prefix is honest)

- The runtime guard checks only the sum, not operand identity. A second mutant duplicating `"$st_js"` and dropping `"$st_citecheck"` (nine operands, sum 9) printed `PASS (cases=9 passed=9)` exit 0 for dropped-leg status 0, 1, and 2 — the guard cannot see it. The selftest does catch that mutant (`mutant_dup.sh --selftest`: 100/106, `VERDICT: FAIL`, exit 1; single-leg vectors red because the duplicated name counts twice while the dropped name never reaches the loop). Detection therefore rests on running the selftest, not on the runtime guard alone.
- The detector is structural: fixed extraction markers, fixed `nlegs=9`, fixed vector set. A tally spelled differently enough to break the awk markers is caught (names≠9 or empty block fails), but an attacker who keeps markers and rewrites semantics in the extracted text could in principle evade specific vectors; the v4 counter already demonstrated that a verifier cannot distinguish executing the block from modelling it (CtlS2SymEval, `v4/ctl2/CtlS2SymEval-v4.stdout`), which is exactly why the claim is exploratory.
- No full `--regression` replay was run (each leg needs network-pinned repos); my evidence covers the extracted-block harness identical in construction to the runner's own, plus the selftest.

## Smallest safe correction (proposal only, never applied)

If a later round wants runtime completeness for miscounts that preserve the sum, compare the loop's operand list against the `st_*=$?` names at tally time — e.g., build the operand list from the same name enumeration the selftest uses (`mapfile` over `st_[a-z]+=\$\?`) so dropping/duplicating an operand changes the loop itself, not just the sum. Cheaper: inside the block, hash or string-compare `"$*"` of operands against the nine declared names. Neither is required to consider head better than base on the assigned surface.

## Bounds

No production files edited; clone and mutants lived only under `/fast/scratch/hyaku/tameshi-r30a3-seats/JudgeC1`. No git write commands and no `jj` anywhere; lane repo touched only via read-only `git show`/`diff` with `GIT_OPTIONAL_LOCKS=0`. Two `timeout 300` selftest runs and fixed-status harness runs completed in ~6-7 s each; no stray processes left (checked `/proc/*/cwd`). The selftest's own scratch dirs under `/tmp/tameshi-r4-2-selftest.*` are retained by the tool on FAIL by design. No tools installed or updated.
