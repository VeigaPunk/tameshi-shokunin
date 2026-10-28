# T56W3ExecControlsB — controls bootstrap run at initial PIN

Judged on: calibration. No lane production file or frozen instrument was edited.

## Command (run 2, valid)
```
export HYAKU_SCRATCH=/fast/scratch/hyaku/tameshi-r56/T56W3ExecControlsB   # unique per seat
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/controls.sh \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 2f5512a8ab0771fb2eee463ec16db359174f5edd \
  21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 $HYAKU_SCRATCH/out
```
exit=0, stderr empty (sha256 e3b0c442...). Receipts (actual harness output, unedited), in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w3/T56W3ExecControlsB-receipts/`:
`controls-b.stdout` (sha256 452990dc3d9b780cd1073297274231b40194818687e4c3ce1f99cc5ffbbfeee7),
`controls-b.stderr`, `controls-b.exit`.

## Exact verdict lines
```
CONTROLS_A: 7/7 as pre-registered
CTL CTL_POS_c1 C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false
CTL CTL_POS_c2 C2_R56: rev=2f5512a8ab07 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false
CTL_MISMATCH CTL_POS_c2 expected=true actual=false
CONTROLS_B: 0/2 as pre-registered
```
Phase A per-control (all false as pre-registered): CTL_0_c1 total=5; CTL_0_c2 total=2; CTL_SKIP_c1 total=4 (rekeyed 0/18); CTL_FAB_c1 readers=17/18 total=2; CTL_RESTATE_c1 restate=9 total=1; CTL_SKIP_c2 selftest=18/19 total=2; CTL_FAB_c2 red54=RECEIPT_DIGEST_MISMATCH total=2.

## Run 1 (collision evidence, retained)
`collision-run1.stdout/.stderr`: first run shared the default scratch `/fast/scratch/hyaku/tameshi-r56/controls` with sibling seats (A and the L1 bootstrap); a sibling's exit trap removed it mid-run (`matches: No such file or directory`, CONTROLS_A 4/7, CTL_SKIP_c1 `monitor-blobs-missing`, no phase B). Not a verdict. Cause: controls.sh derives SCR from HYAKU_SCRATCH only; concurrent runs need distinct HYAKU_SCRATCH (done in run 2).

## Finding 1 — CTL_POS_c1 is false at PIN for a case-sensitivity reason in arm 6 (bootstrap-independent)
Run 2 is the first run in which every other C1 arm passes at PIN (precheck lost=0, monitor 64/64 score=8, 18/18 rekeyed, 18/18 readers). The single remaining C1 failure (`total=1`) is arm 6 (`restate`):
```
EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='Round-21 cold-read monitor ...' round='56'
```
`c1/measure.py` line 275 tests `'round-21' in cells[2]` case-sensitively; the round-56 standing row in SCORECARD.md (line 2718 at PIN) begins `Round-21 cold-read monitor ...` (capital R). The earlier rows (2423, 2579) use lowercase `round-21`. Score 8 == monitor 8, row commit c1dd23b3f83f resolves and its monitor score is 8, round cell `56`: all other restate conditions hold.

Patch (SCORECARD.md is a production file; L1 integrates; frozen counter must NOT change):
```
-| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points ...
+| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points ...
```
(only the leading `R` of the evidence cell on the round-56 calibration row, SCORECARD.md line 2718.)

Scratch-clone demonstration (clone --shared at PIN, one-char sed on line 2718, committed in the clone with toplevel asserted, then):
```
python3 <clone>/.ufo/evidence/round-56/c1/measure.py --lane <clone> --rev <clone HEAD> --work <empty> --explain
EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='round-21 cold-read monitor ...' round='56'
C1_R56: rev=8ef862770802 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
```
Caveat: the row commit is already `c1dd23b3f83f` and the fix changes SCORECARD.md, so the certified revision moves; the L1 must rebind the PIN/row-commit relationship accordingly (the row's commit must still be an ancestor of the new rev; it is). Note the fix is a standing-row text edit at a new revision, so `rev=` receipts must be produced at that new revision.

## Finding 2 — CTL_POS_c2 false = declared bootstrap limitation
`own=own-receipts-missing` (total=1; selftest 19/19, red54/red54b/red55 refusals correct, docs=4/4). No committed `controls-a/b.stdout` at PIN, as the assignment predicted. This run's `controls-b.stdout` has a CONTROLS_A 7/7 and may serve as the bootstrap input the L1 commits (with `.sha256` sibling computed by the L1); it is not a deciding pass. Also the known arm-5 blind spot (hand-written receipts accepted) is unchanged and untouched.

## Tools
None installed or upgraded. Scratch dirs removed (traps).

## Re-run note for the L1
After committing the bootstrap receipts and fixing the SCORECARD case, rerun the same frozen controls.sh at the new PIN with a unique `HYAKU_SCRATCH` per concurrent seat (~20 min wall).
