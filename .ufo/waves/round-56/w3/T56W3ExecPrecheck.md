# T56W3ExecPrecheck — precheck + monitor at PIN 2f5512a8ab0771fb2eee463ec16db359174f5edd

## Verdicts
- Precheck PASS. Command:
  `bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 0a2010acd1e92e4e332774050825e21bcfc7e079 2f5512a8ab0771fb2eee463ec16db359174f5edd`
  Output was one line, exit 0, no `LOST` lines:
  `COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=2f5512a8ab07 cand_credited=64 lost=0 ok`
- Round-21 monitor at PIN PASS: `covered=64 score=8 box3=true`.
  Run as the C1 counter runs it: the round-18 and round-21 `measure.py` blobs from `git show PIN:` are mirrored at their lane-relative paths, then `python3 <mirror>/.ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev PIN`, exit 0.
  Blob sha256: round-18 `7ca87a7c9819...6dd37`; round-21 `657f009bdf1c...f3eb`.

## FINDING: the C1 counter reads FALSE at PIN (R56.W3.1, arm 6 restate)
Command:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work <empty dir> --explain`
```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=2f5512a8ab07 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
EXPLAIN arm3-rekey dirs=['rekey-r56-c0137451f5b7'] c0=c0137451f5b7f22d65f748fc69f1b181f55e1378
EXPLAIN arm4-readers 18/18
EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='Round-21 cold-read monitor `calibration_restraint_score`; tw' round='56'
C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false
```
Arms 1-4 pass (the rekeyed 18/18 and readers 18/18 are in the line above). The single `total=1` comes from arm 6, `restate_ok=False`.

Cause: `measure.py` line 275 tests `'round-21' in cells[2]`, which is case-sensitive. The SCORECARD calibration row last committed at `c1dd23b` / PIN (SCORECARD.md line 2718) writes `Round-21 cold-read monitor ...` with a capital R. All the other restate conditions hold in the output above:
- `row_score=8` equals the monitor score.
- `row_commit` resolves to `c1dd23b3f83f` and is an ancestor of PIN.
- `score_at_row=8`.
- Cell 4 is `56`.

I read the cells with the same split the counter uses. The check printed `round-21 in c2: False | 56 in c4: True`.

The earlier calibration rows use lowercase `round-21` (lines 2423 and 2579), so the capital R was introduced by the round-56 restate.

## Patch (diff only; no lane file was edited)
One SCORECARD.md line, the calibration row at 2718. Lowercase `Round-21` to `round-21`:
```
-| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points ...
+| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points ...
```
The rest of the row (score 8, commit `c1dd23b3f83f5dff676c4a4482498e87345375ef`, round 56) stays byte-identical.

Scratch-clone demonstration (`git clone --shared` of the lane, detached at PIN, one scratch commit `3b17acbb6b30d2922fdce28210d1f98b42669ee4`, toplevel asserted equal to the clone dir). The same command was run with `--lane <clone> --rev 3b17acbb...`:
```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=3b17acbb6b30 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='round-21 cold-read monitor ...' round='56'
C1_R56: rev=3b17acbb6b30 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
```
Only the SCORECARD cell changed, so the SKILL.md section hashes, the readers' `section_sha256` and the rekey bind are untouched. Arms 1-4 are unchanged.

Consequences for the L1:
- The fix creates a new content-final revision, so the PIN moves. Rerun the precheck and monitor at the new tip. They should be unaffected, since only SCORECARD.md changed.
- `c1` and `c2` must be run at the new certified revision.
- The row still names `c1dd23b3f83f`, whose monitor score is 8, so that part of the restate stays valid.
- Do not edit the frozen counter to accept `Round-21`. The counter is frozen, and the fix belongs in the lane's own row.

## Housekeeping
- No tools installed, and no lane or frozen file written.
- Scratch `/fast/scratch/hyaku/tameshi-r56/T56W3ExecPrecheck` is removed by trap. The mutating git calls were limited to the one scratch-clone commit above.
