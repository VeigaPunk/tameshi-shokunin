# T57W1ExecControls — controls.sh (C1 + C2), staged

Files (all STAGED under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ExecControls/stage/`; nothing in the lane was edited):
- `.ufo/evidence/round-57/controls.sh` (`controls.sh LANE BASE REV OUTDIR`, bash, `set -u`) sha256 `0a8561af…b444`
- `.ufo/evidence/round-57/control/gen_ledger.py` (C1 ledger generator, modes skip|fab|open) sha256 `ed5d2565…b444`
- `.ufo/evidence/round-57/control/gen_registry.py` (C2 registry generator, modes skip|fab|mut) sha256 `783322a6…d2`
(full digests in the .json). Install all three under the same repo-relative paths; they must be in REV: the harness runs the generators from the clone of REV.

## Design (what changed from round 56)
- ONE generation (R56.5): header comment states controls are recomputed, never read. No control reads a committed round-57 receipt: each is a fresh `git clone --shared` of LANE (`git -C` only, fixture identity, toplevel asserted before any commit, GIT_* env scrubbed), mutated by a generator, committed in the clone, and scored by the counter the clone carries (`measure.py --lane CLONE --rev CLONE_HEAD --work SCRATCH --explain`). A real guard: exit 2 `CTL_GENERATION_ERROR` if REV's tree already contains `.ufo/evidence/round-57/control/controls-*` or `after/*` (receipts must be committed AFTER REV; REV is content-final).
- Kept from round 56: `emit` relabelling of a `rev=` the lane cannot resolve to `clone_rev=`; CTL / CTL_MATCH / CTL_MISMATCH lines; phase A/B split; scratch `$HYAKU_SCRATCH/tameshi-r57/controls` removed on exit (verified absent after runs); TMPDIR exported to scratch.
- Summary lines: `CONTROLS_A: m/n as pre-registered` (8 controls, all but POS), `CONTROLS_B: m/n as pre-registered` (2 POS, scored in a fresh clone asserted equal to REV). Extra lines: `CTL_GEN <name> <json stats>` per synthetic control; full counter output (`--explain`) per control at `OUTDIR/ctl-<NAME>.full`; each CTL line has `counter_exit=`.
- CTL_0_c1/c2 deviation (stated in the header): the frozen set and counters do not exist at BASE, so `--rev BASE` against the lane ends in a setup error with no verdict token. CTL_0 is BASE + `c1/`, `c2/` (+ `contract.json` when present) overlaid from REV and committed in a scratch clone — the do-nothing tree the counters can grade. Its CTL line prints `clone_rev=`.

## Controls
| control | construction | arm it must trip |
|---|---|---|
| CTL_0_c1 / CTL_0_c2 | BASE + instruments | rows=0/N, gate_rows=0 |
| CTL_SKIP_c1 | 49 old rows kept; 51 new rows `declined`, reason 45 chars, real keyed evidence | declined cap (declined_over) + fixed floor |
| CTL_FAB_c1 | 51 new rows `fixed`, commit = clone HEAD, real path/lines, invented excerpt (names the key, occurs nowhere) | evidence resolution |
| CTL_OPEN_c1 | 51 new rows `open`, real evidence; newest `**Planned (round` paragraph of SCORECARD.md has `R\d+\.\d+` ids blanked | open-unplanned |
| CTL_SKIP_c2 | removes real non-selftest gate rows; 3 rows with correct commands, `expect.exit` rotated (accept→2, drift→0, unresolvable→3; declared set still {0,2,3}) | held N/N |
| CTL_FAB_c2 | 3 rows whose accept/drift receipts were never written (gate answers RECEIPT_MISSING); the unresolvable row still holds | held (1/3) |
| CTL_MUT_c2 | 3 rows that hold on the clean gate (accept 0, absent-rev refusal 3 `RECEIPT_REV_ABSENT`, unresolvable 2) and never run the drift branch | mutants arm |
| CTL_POS_c1 / CTL_POS_c2 | clone of REV, scored at REV | expected true |
Deviation on CTL_MUT_c2 (spec: "rows that only run an accepting fixture, so no mutant turns a row red"): rows must expect exits {0,2,3}, and any valid exit-2 row runs the branch mutant M3 breaks, so the achievable control is mutants=1/3 (M3 only) with held=3/3; rows that ran only an accepting fixture would fail arm 1/2 instead of isolating arm 3. Measured: `held=3/3 mutants=1/3 total=4 PASS=false`.

## Dry run (structure; counters are the siblings' staged versions at run time)
Dry lane = scratch clone of the lane at BASE with every seat's stage dir copied in and committed as "REV" (`dry-run-rev.txt`). Receipts in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ExecControls-receipts/`.
- `dry-real-counters.stdout` (staged real counters): `CONTROLS_A: 8/8 as pre-registered` (all 8 printed false with their pre-registered failing arms, e.g. `CTL_SKIP_c1 … declined=51 … total=65`, `CTL_FAB_c1 … fixed=51 agree=0/51`, `CTL_SKIP_c2 … held=0/3`, `CTL_FAB_c2 … held=1/3`, `CTL_MUT_c2 … held=3/3 mutants=1/3`). `CONTROLS_B: 0/2` — expected, the dry REV carries no content work (rows=0/51, gate_rows=0); POS cannot pass until the content lands.
- `dry-stub-counters.stdout` (counters replaced by stubs that print PASS=true): `CONTROLS_B: 2/2`, `rev=<REV12>` kept un-relabelled for POS, and `CONTROLS_A: 0/8` (shows the harness prints CTL_MISMATCH when a counter does not reach its boolean). Plumbing proof only, not counter evidence.
- `dry-generation-guard.stdout`: REV carrying `control/controls-a.stdout` → `CTL_GENERATION_ERROR`, exit 2.
- Positive-path scoring of a real passing tree was NOT exercised (no such tree exists yet); POS correctness with the real counters is an open check for the L1's first real run.

## Findings for the L1
1. `unkeyed=1` in every C1 generator stats line: R56.7's keys (`no byte changed`, `D-CF1`, `grew between`) occur only in the excluded spot-check, so the SKIP/FAB/OPEN controls carry one extra `key_miss`-class row until the R56.7 fix text lands in a lane file (then the stat reads 0). It does not change any control's verdict.
2. In the dry run the C1 counter printed `defects_pin` +1 in every total (staged `defects.json` sha not equal to the counter's pinned sha at that moment; siblings changed their staged files during the run). The pin must be reconciled before the freeze or CTL_POS_c1 cannot pass.
3. The Planned-paragraph id regex `R\d+\.\d+` in gen_ledger `open` mode assumes the counter reads ids from the newest `**Planned (round` paragraph (round-50 rule); `planned_ids_blanked` was 0 at BASE (the round-55 paragraph names no ids). If REV's paragraph names ids, the stats line shows how many were blanked.
4. Cost: full controls run ≈ 140-150 s (C2 counter's mutant arm dominates).
5. The generators run from the REV clone, so `control/gen_*.py` must be committed in REV; `controls.sh` itself is run from the lane working tree (as in round 56).

Tools installed: none. Repo mutations: none (scratch clones only; scratch removed).
