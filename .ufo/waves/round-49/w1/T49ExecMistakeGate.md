# T49ExecMistakeGate — can the round-49 gate-0 fix fail? (probe, not a verdict)

Seat: wave-1 executor, round 49. Lane clone only; the lane checkout was never modified.
Object under test: `.ufo/evidence/round-49/deciding-run.sh` gate 0, lines 22–29. The blob I ran is
pinned by `freeze.json:15` — `"…/deciding-run.sh": "31e9838e735b27a9aa6ac3ee5ccc3e8f2d39432a32e3dd6a80ab456125dd10f5"`
— and `sha256sum` of the copy I executed is the same `31e9838e…` (`T49ExecMistakeGate/fixture.txt`, "script under test").
Blob `5e059dafd5eefd728b0b0840e4b932918f71f7ad` is that file at both `14d03ea` and the case-(b) fixture commit.

Mined mistake (round 48): `corpus/lessons/round-48-verifier-spotcheck.md:27` (defect 2, controls scored after the
deciding run) and `:28` (defect 3, undisclosed `--only` previews at the content revision); routed as `:116`.
The fix is gate 0: receipts must exist at REV (`deciding-run.sh:25`), their last-touch commit must descend from
FREEZE (`:26–27`), and no start receipt may already be in OUTDIR (`:29`). Everything else is downstream of `:30`.

## Result: the fix is able to fail — three conditions, each refused with exit 3 and no counter started

All runs: `HYAKU_SCRATCH=$S` (so the script's work root stayed inside my scratch), `cwd=$S/lane`,
`$S=/fast/scratch/hyaku/tameshi-r49/T49ExecMistakeGate`, clone `git clone --shared … "$S/lane"` verified
`toplevel=$S/lane` before every mutation, `checkout --detach 14d03ea…`.

### (a) no control receipts at the freeze revision

```
$ bash .ufo/evidence/round-49/deciding-run.sh "$S/lane" HEAD 14d03ea…  "$S/out"
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c1-controls.stdout
exit=3
```
`$S/out` empty; `$S/tameshi-r49` (the script's `SCR`, created at `:30`) never created ⇒ no counter, no no-harm,
no census, no cold-read precheck. Receipts: `case-a.stdout`, `case-a.stderr` (0 bytes).

### (b) receipts committed after the freeze, but a start receipt already exists

Fixture commit `56077d135c4edb224195202f2313a3d7a3ac533c` (child of `14d03ea`, adds exactly the four files
`c1-controls.stdout/.exit`, `c2-controls.stdout/.exit`), so gate 0's receipt loop passes; `$S/out2/c1.start`
pre-created.

```
$ bash .ufo/evidence/round-49/deciding-run.sh "$S/lane" HEAD 14d03ea… "$S/out2"
DECIDING_REFUSED second-invocation c1
exit=3
```
`$S/out2` still holds only `c1.start`; `SCR` absent. Receipts: `case-b.stdout`, `case-b.stderr`.

### (c) control receipt committed *in an ancestor of* the freeze revision

`git merge-base --is-ancestor` cannot be satisfied by a commit hash that gains an ancestor, so the fixture rewrites
the branch (the item's own wording) and additionally reproduces the literal "ancestor of 14d03ea" shape:

- receipt commit `ebd2e6419f2d8a827ee2a457235c2ccbf460e746` (parent `8ca67421`), then
- freeze commit `e5eb093d43cac903495a264ef43a4b47af82e66d` = `14d03ea`'s tree **plus** the four receipts,
  parent `ebd2e64` (`git diff --stat 14d03ea e5eb093` → the four `A` rows only, `fixture.txt`).

```
$ bash "$S/deciding-run-c.sh" "$S/lane" e5eb093… e5eb093… "$S/out3"
DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-49/control/c1-controls.stdout
exit=3
```
Receipts: `case-c.stdout`, `case-c.stderr`; `$S/out3` empty.

Literal variant (receipt commit `ebd2e64` made an ancestor of the real `14d03ea` via
`git replace 14d03ea f8b10b6bf271a8a7bb03b846edf00f080a84cf48`, a substitute commit whose tree is the freeze tree
plus the receipts, parent `ebd2e64`; `git log -1 14d03ea -- …/c1-controls.stdout` → `ebd2e64`,
`replace` ref removed afterwards):

```
$ bash "$S/deciding-run-c.sh" "$S/lane" 14d03ea… 14d03ea… "$S/out4"
DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-49/control/c1-controls.stdout
exit=3
```
Receipts: `case-c-literal.stdout`, `case-c-literal.stderr`; `$S/out4` empty.

Every case wrote its refusal before `deciding-run.sh:30`, the first side effect outside OUT: `$S/tameshi-r49`
absent after all four runs (`SCR_ABSENT_AFTER_ALL_FOUR_RUNS`). No case reached a counter, so nothing had to be killed.

## Gate-strength findings from the same fixtures (code reading + the sub-check table; no extra runs)

1. **The ordering check proves commits, not scoring.** In case (b) my four one-line synthetic receipts
   (`e78333f…`, `573541a…`, `5bfaa44…`, `573541a…`, `fixture.txt`) satisfied `deciding-run.sh:24–28` completely:
   `present` + `after-freeze` for all four (`gate0-subchecks.txt`, case b). Only the start-receipt check at `:29`
   stopped that run. So gate 0's guarantee is "a commit adding these four paths descends from FREEZE and is reachable
   from REV", not "the controls ran at freeze bytes". A placeholder receipt committed after the deciding run and then
   amended into history (or committed from a shell whose scoring order nobody checks) still passes.
2. **A receipt whose last-touch commit *is* FREEZE passes `:27`** — `git merge-base --is-ancestor 14d03ea 14d03ea`
   exits 0 (`fixture.txt`, "is-ancestor reflexivity"). Receipts committed inside the freeze commit are therefore
   accepted, i.e. the check separates "before" from "at-or-after", not "at" from "after". Case (c) refuses the strict
   ancestor only.
3. **The one-invocation guard is per-OUTDIR** (`:29` reads `$OUT/$k.start` only). A second invocation with a fresh
   empty directory passes gate 0. Not exercised — exercising it means letting gate 0 pass, which the item forbids;
   recorded as a code fact at `:29` with the sub-check table showing no other state is consulted.
4. **The counters are not coupled to the gate.** `c1/measure.py:549–554` and `c2/measure.py:429–435` accept only
   `--lane/--rev/--work[--fleet|--panel]|--list|--selftest` and neither reads control receipts nor writes a start
   receipt. A direct invocation at the content revision — round 48's defect-3 preview channel — leaves no trace and
   gate 0 cannot see it. The fix constrains invocations *made through the script*, not the counters.
   (Round-48's `--only` flag is gone from the round-49 CLI; the bypass is now an ordinary full invocation.)

These four are limits of the fix's reach, not failures of the three assigned cases; the rejected case set above is
what shows the gate fires. I do not decide C1 or C2 — no counter was invoked at any revision.

## Reproduction and receipts

`.ufo/waves/round-49/w1/T49ExecMistakeGate/`: `commands.txt` (setup + all five command lines),
`case-a.stdout`/`.stderr`, `case-b.stdout`/`.stderr`, `case-c.stdout`/`.stderr`,
`case-c-literal.stdout`/`.stderr`, `gate0-subchecks.txt` (lines 24–28 re-derived per case: case a absent,
case b present+after-freeze, case c present+not-after-freeze, literal variant marked), `fixture.txt`
(clone toplevel, script blob + sha256, fixture commit hashes, receipt blob hashes, `diff --stat`, OUTDIR listings,
reflexivity), `deciding-run-frozen-blob.sh` (byte copy, sha256 `31e9838e…`).
Scratch `$S` deleted before yield; the lane checkout and the fleet repo were not written.

Tooling: none installed or upgraded (git, bash, python3 as present). `/home/vgpnk/.local/bin` untouched.

## Summary

- Gate 0 of `deciding-run.sh` (frozen sha256 `31e9838e…`, `freeze.json:15`) was shown to fail on all three assigned
  conditions, each `exit 3` with the exact `DECIDING_REFUSED …` line and zero counter artifacts.
- (a) `control-receipt-missing` at `14d03ea`; (b) `second-invocation c1`; (c) `control-receipt-not-after-freeze`,
  plus the literal ancestor-of-`14d03ea` shape via a replace-ref fixture.
- No run passed gate 0: `OUT` dirs stay empty (except the pre-created `c1.start`), `SCR` never created.
- Limits: receipts are existence + commit-order only (synthetic one-liners pass); receipts inside the freeze commit
  pass (`:27` reflexivity); one-invocation is per-OUTDIR (`:29`); counters are gate-free, so defect-3 previews
  remain invisible.
- Probe only, no verdict; C1/C2 counters were not invoked.
