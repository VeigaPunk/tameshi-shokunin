# T56W3ExecControlsA - controls phase A (round 56, wave 3)

Verdict: **phase A passes 7/7. The harness is not broken. A real defect exists at PIN: `CTL_POS_c1` is false because the standing row spells `Round-21` and the frozen counter tests for lowercase `round-21`. A one-word SCORECARD patch fixes it in a scratch clone (C1 total=0).**

## Command
`bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/controls.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 2f5512a8ab0771fb2eee463ec16db359174f5edd 21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 $S/out`

- Run with `HYAKU_SCRATCH=/fast/scratch/hyaku/T56W3ExecControlsA-iso`, so the harness's internal scratch is `.../T56W3ExecControlsA-iso/tameshi-r56/controls`, unique to this seat.
- The OUTDIR was an empty dir under my own scratch.
- Exit 0. Stderr empty. Wall time 1138 s (21:11:29 to 21:30:16 UTC), phases A and B together.
- Receipts, in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w3/T56W3ExecControlsA-receipts/`:
  - `controls-a.stdout`: the L1 commits it as `.ufo/evidence/round-56/control/controls-a.stdout`.
  - `controls-a.exit`: contains `0`. The L1 commits it as `controls-a.exit`.
  - `controls-a.stderr`: empty.
  - `start.txt`: start and end clock times.
  - `collided-run/`: the first attempt, kept as evidence (see Harness faults).
  - `timeout-killed-run/`: the second attempt (partial stdout), killed by my 900 s tool timeout during phase B. It is complete through phase A and identical in verdicts.
  - `scorecard-case-fix.diff`: the proposed patch.

## Output (controls-a.stdout, final run, verbatim essentials)
```
CTL CTL_0_c1 C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false
CTL_MATCH CTL_0_c1 expected=false actual=false
CTL CTL_0_c2 C2_R56: rev=21eb3c63cd0f selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false
CTL_MATCH CTL_0_c2 expected=false actual=false
CTL CTL_SKIP_c1 C1_R56: clone_rev=da60e9ede5e7 c0=c0137451f5b7 credited=46 lost=18 rekeyed=0/18 readers=18/18 monitor=6/46 unstable=0 restate=8 total=4 C1_R56_PASS=false
CTL_MATCH CTL_SKIP_c1 expected=false actual=false
fabricated T56W2Read01.json
CTL CTL_FAB_c1 C1_R56: clone_rev=1ebc11d4391e c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=17/18 monitor=8/64 unstable=0 restate=8 total=2 C1_R56_PASS=false
CTL_MATCH CTL_FAB_c1 expected=false actual=false
CTL CTL_RESTATE_c1 C1_R56: clone_rev=afe03c4521a5 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=9 total=1 C1_R56_PASS=false
CTL_MATCH CTL_RESTATE_c1 expected=false actual=false
CTL CTL_SKIP_c2 C2_R56: clone_rev=c71bd43741c0 selftest=18/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=2 C2_R56_PASS=false
CTL_MATCH CTL_SKIP_c2 expected=false actual=false
CTL CTL_FAB_c2 C2_R56: clone_rev=19cfd456b29d selftest=19/19 red54=RECEIPT_DIGEST_MISMATCH red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=2 C2_R56_PASS=false
CTL_MATCH CTL_FAB_c2 expected=false actual=false
CONTROLS_A: 7/7 as pre-registered
# phase B ...
CTL CTL_POS_c1 C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false
CTL CTL_POS_c2 C2_R56: rev=2f5512a8ab07 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false
CTL_MISMATCH CTL_POS_c2 expected=true actual=false
CONTROLS_B: 0/2 as pre-registered
```
**Tallies: `CONTROLS_A: 7/7 as pre-registered`, `CONTROLS_B: 0/2 as pre-registered`.**

## Correction to the assignment's wording
The harness prints `CTL_MATCH` when the counter reached the pre-registered boolean and `CTL_MISMATCH` when it did not. The assignment says each phase-A control "must print CTL_MISMATCH". That is inverted. Reading the harness and the contract:
- All seven phase-A controls pre-register `expected=false`. `CTL_MATCH ... actual=false` is the correct outcome and `CTL_MISMATCH` would mean a broken counter.
- All seven printed `CTL_MATCH`, so none is broken.

## Control-by-control check against the pre-registered design
The control names match `contract.json` (`C1.controls = CTL_0, SKIP, FAB, RESTATE, POS`; `C2.controls = CTL_0, SKIP, FAB, POS`). All seven mutation needles applied:

| control | applied? | failing arm that made it false |
|---|---|---|
| CTL_0_c1 (BASE) | yes | lost=18, rekeyed 0/18, readers 0/18, monitor 6/46 (total=5) |
| CTL_0_c2 (FREEZE) | yes | own-receipts-missing, docs 0/4 (total=2) |
| CTL_SKIP_c1 (rekey entries removed from ledger) | yes | credited=46, lost=18, rekeyed=0/18, monitor 6/46. readers=18/18 is correctly untouched. |
| CTL_FAB_c1 (section_sha256 zeroed) | yes (`fabricated T56W2Read01.json`) | readers=17/18 exactly, plus own-receipts-missing (see below) |
| CTL_RESTATE_c1 (row 8 to 9) | yes (row printed) | restate=9, total=1: only the restate arm fails, which isolates it cleanly |
| CTL_SKIP_c2 (binding arm removed) | yes (needle present) | selftest=18/19 (the mutation is caught by the gate selftest), plus own-receipts-missing |
| CTL_FAB_c2 (rev-only fabricated receipt) | yes | red54=RECEIPT_DIGEST_MISMATCH, plus own-receipts-missing |

Two caveats:
- **Bootstrap contribution to C2.** In this run every `c2` control also carries `own=own-receipts-missing`, which is the documented bootstrap (no committed `controls-a/b.stdout` at PIN). The `CTL_SKIP_c2` and `CTL_FAB_c2` falsity is therefore over-determined here. The unmasked second run must be re-read for `selftest=18/19` (SKIP_c2) and `red54=RECEIPT_DIGEST_MISMATCH` (FAB_c2) as the sole failing arms.
- **CTL_FAB_c2 refusal reason.** The gate refuses the fabricated receipt as `RECEIPT_DIGEST_MISMATCH`, not as a rev-binding failure. The fabricated receipt names the certified rev but the `.sha256` sidecar was not updated. This is the counter's declared provenance gap. A forger who also rewrites the sidecar would not hit this arm, as in `T56W2CritDoNothingC2.md`. I did not test that variant.

## DEFECT at PIN: CTL_POS_c1 is false (total=1), and the cause is a case-sensitivity bug
- `--explain` at PIN `2f5512a8ab07` shows arms 1 to 4 clean (precheck `lost=0 ok`, monitor 64/64 score 8 box3, one `rekey-r56-c0137451f5b7`, readers 18/18).
- Arm 6 prints `row_score=8 row_commit=c1dd23b3f83f score_at_row=8 ... round='56'` yet `restate_ok` is false.
- `c1/measure.py:275` requires `'round-21' in cells[2]` (case-sensitive).
- The SCORECARD row at PIN (`SCORECARD.md` line 2718) reads `| calibration | 8 | Round-21 cold-read monitor ...`, with capital R. The cell has no lowercase `round-21` (and no `.ufo/evidence/round-21/...` path).
- The other standing rows in SCORECARD.md, which say `round-21 cold-read monitor`, are lowercase and would pass.
- Because of this, `C1_R56_PASS` cannot be true at PIN, and `CONTROLS_B` cannot reach 2/2 there.

**Fix (SCORECARD.md cell only; the L1 applies it). Diff:**
```
-| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f...` | 56 |
+| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; ...same text... | `c1dd23b3f83f...` | 56 |
```
- Scratch demonstration: clone `--shared`, checkout PIN, apply the one-word change, commit in the clone, run the frozen counter.
- Command: `python3 <clone>/.ufo/evidence/round-56/c1/measure.py --lane <clone> --rev <clone HEAD> --work <empty> --explain`
- Verdict line: `C1_R56: rev=453976504c30 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true`
- The clone-local rev is not a lane revision. The deciding run has to be re-run at the real certified revision after the patch is committed.
- The patch edits `SCORECARD.md`, not `row_commit` (`c1dd23b3`), so the monitor score at the row's commit is unchanged.
- Since the patch moves PIN, the whole bootstrap sequence (controls-a/b, sidecars) must be re-run at the new PIN. This applies to the C2 `own=` arm as well.

## `CTL_POS_c2` at PIN (bootstrap, expected)
`own=own-receipts-missing total=1`: no committed `controls-a/b.stdout` exists at PIN. Everything else is at denominator: selftest 19/19, red54 refused with RECEIPT_REV_CONTENT_DRIFT (old gate accepted), red54b RECEIPT_REV_UNRESOLVABLE, red55 RECEIPT_REV_ABSENT, docs 4/4. This is the documented two-pass bootstrap and resolves when the L1 commits the receipts above and reruns at the next PIN.

## Harness faults found (not defects of the lane's counters)
1. **Shared fixed scratch path.** `controls.sh` sets `SCR=${HYAKU_SCRATCH}/tameshi-r56/controls` and does `rm -rf "$SCR"` plus an EXIT trap that removes it. Two seats that run controls with the default scratch collide.
   - My first run, with the default `HYAKU_SCRATCH`, collided with a concurrent controls run. Its stdout stops after CTL_0_c2: `fatal: destination path '/fast/scratch/hyaku/tameshi-r56/controls/skip-c1' already exists`, and CTL_0_c2 printed `error=work-not-empty`, and the exit was 2. This is kept in `collided-run/`.
   - Fix: give each seat its own `HYAKU_SCRATCH` (I did this for the final run). Run controls only from one seat at a time per scratch root. No harness change needed.
2. **Cost.** Phase A plus B takes about 19 min wall (each C1 counter call is about 2 min). Seat tool timeouts under 20 min kill the run mid-phase B (my second run, retained as `timeout-killed-run/`).
3. **`CONTROLS_A` count.** It is computed with `grep -c . "$SCR/matches"` on a file the `emit()` function appends to. It is correct here (7). It would read 0 if two harness runs shared one scratch, because of fault 1.

## Tool installs
None.

## Files changed
Only the receipts dir and this report, under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w3/`. No lane production files and no frozen instruments were touched. No git or jj mutations in the lane. Scratch dirs removed.

## Risks
- The `Round-21` case defect makes PIN uncertifiable as it stands. Round-56's C1 true-verdict path requires the SCORECARD fix, then a new PIN, then controls reruns (the bootstrap).
- The `.sha256` sidecars for `controls-a.stdout`/`.exit` are the L1's to compute, per the harness header.
