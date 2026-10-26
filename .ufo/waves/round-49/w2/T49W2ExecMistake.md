# T49W2ExecMistake — round-49 `deciding-run.sh` gate 0, able to fail, re-run independently (probe, not a verdict)

Seat: wave-2 executor. Item: re-run the able-to-fail demonstration of gate 0 of
`.ufo/evidence/round-49/deciding-run.sh` (round-48 routed defects 2–3) without copying wave-1's commands
(`.ufo/waves/round-49/w1/T49ExecMistakeGate.md`). Object: gate 0, `deciding-run.sh:22–29`. The first outside-OUT
side effect is `:30` (`mkdir -p "$SCR"`); `FROZEN_UNCHANGED` prints at `:33`; monitors run `:34–42`; the start
receipts are written at `:43`/`:46`, immediately before counters `:44`/`:47`.

Blob under test: `5e059dafd5eefd728b0b0840e4b932918f71f7ad` at both `f181a961ae44061af486f600e5ea257d2baf78f8`
and the freeze `14d03ea4270c6904064022b62b6faf467e5c0968`; sha256 `31e9838e735b27a9aa6ac3ee5ccc3e8f2d39432a32e3dd6a80ab456125dd10f5`,
equal to `freeze.json:15` and to the executed worktree copy (`T49W2ExecMistake/fixture.txt`, `sha256sum` +
`git show REV:… | sha256sum`).

Setup (all inside scratch; no lane write, no lane git mutation, no fleet write):
`S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecMistake`; `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"`;
`git -C "$S/clone" rev-parse --show-toplevel` → `$S/clone`; `git -C "$S/clone" checkout -q --detach f181a96…`;
every later git call is `git -C "$S/clone" …` (or the lane read-only). Work dirs under `$S`, `TMPDIR=$S`.

## Result: all three assigned conditions reproduce, each with the exact refusal line and no counter started

| case | REV | OUT before | observed stdout | rc | OUT after | SCR (`$HYAKU_SCRATCH/tameshi-r49/deciding`) |
|---|---|---|---|---|---|---|
| a1 one receipt deleted | `01af854` | empty | `DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c2-controls.exit` | 3 | empty | absent |
| a2 no receipts at all | `8ca67421…` (base) | empty | `DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c1-controls.stdout` | 3 | empty | absent |
| b1 `c1.start` present | `f181a96` | `c1.start` | `DECIDING_REFUSED second-invocation c1` | 3 | `c1.start` only | absent |
| b2 `c2.start` present | `f181a96` | `c2.start` | `DECIDING_REFUSED second-invocation c2` | 3 | `c2.start` only | absent |
| c receipts present, OUT empty | `f181a96` | empty | `FROZEN_UNCHANGED=1 freeze=14d03ea… rev=f181a96…` then killed | `-15` (SIGTERM) | `frozen.stdout` only | exists, **empty** |

Receipts: `T49W2ExecMistake/cases.json` (per-case argv, timestamped lines, listings), `case-a1.stdout`,
`case-a2.stdout`, `case-b1.stdout`, `case-b2.stdout`, `case-c.stdout`, `case-c-repeats.stdout`,
`case-d-freeze-arg.stdout`, `repeat.json`, `fixture.txt`, driver `drive.py`/`repeat.py`, `commands.txt`.

### F1 — (a) a missing control receipt refuses at `deciding-run.sh:25`, before `:30`

Attacks: the round-48 routed defect "controls scored after the deciding run" and its fix clause
`git cat-file -e "$REV:$f" || { … exit 3; }` (`deciding-run.sh:25`).

Fixture: commit `01af8543ed67e97aed1fa1b7a6af06d61b0f6fcf`, tree = `f181a96`'s tree minus exactly
`.ufo/evidence/round-49/control/c2-controls.exit`, built with plumbing only (`read-tree`/`rm --cached`/`write-tree`/
`commit-tree` under `GIT_INDEX_FILE=$S/fixture.idx`), so the clone's worktree, index and HEAD stayed at
`f181a96` (`git -C "$S/clone" status --porcelain` empty; `git -C … for-each-ref --contains 01af854…` empty;
`git -C lane cat-file -e 01af854…` → `LANE-DOES-NOT-HAVE-IT`). `git -C "$S/clone" diff --stat f181a96 01af854…`:

```
 .ufo/evidence/round-49/control/c2-controls.exit | 1 -
 1 file changed, 1 deletion(-)
```

```
$ bash .ufo/evidence/round-49/deciding-run.sh "$S/clone" 01af854 14d03ea "$S/out-a1"
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c2-controls.exit
[rc=3] out_listing=[] scr_exists=false scr_listing=ABSENT
```

Cause control: at `REV=f181a96` with the same clone, script and FREEZE argument the *same* gate passes and prints
`FROZEN_UNCHANGED=1` (F3 below). The two runs differ only by that one deleted path, so the refusal is attributable
to the missing receipt rather than to the fixture.

"Before any counter starts" is shown structurally, not by timing: the refusal is at `:25`, five lines above `:30`,
the first side effect outside OUT; `$HYAKU_SCRATCH/tameshi-r49/deciding` was never created, so `:34–:47`
(no-harm, cold-read precheck, census, both counters) did not execute; `out-a1` is empty, i.e. no `frozen.stdout`,
no `no-harm.stdout`, no `c1.start`/`c2.start`, no `c1.stdout`/`c2.stdout`.

Variant a2 (`REV=8ca67421111fa354b47b803358391d0b07fc6db9`, the base, where `.ufo/evidence/round-49/` does not
exist) refuses on the first path it tests, `c1-controls.stdout`, rc=3, OUT empty, SCR absent — same shape with
all four receipts absent.

### F2 — (b) a pre-existing `c1.start` refuses at `deciding-run.sh:29`

Attacks the one-invocation clause `for k in c1 c2; do [ -e "$OUT/$k.start" ] && { … exit 3; }; done` (`:29`).

```
$ bash .ufo/evidence/round-49/deciding-run.sh "$S/clone" f181a96 14d03ea "$S/out-b1"   # out-b1/c1.start pre-created
DECIDING_REFUSED second-invocation c1
[rc=3] out_listing=['c1.start'] scr_exists=false scr_listing=ABSENT
```

`c2.start` behaves identically (`b2`: `second-invocation c2`, rc=3). The out dir is unchanged by the run
(still exactly the pre-created receipt) and SCR is absent, so nothing downstream ran.

### F3 — (c) all four receipts present and an empty OUT: gate 0 passes, run killed on `FROZEN_UNCHANGED`

At `REV=f181a96` the receipt loop's inputs all satisfy `:25`/`:27` (`fixture.txt`):
`c1-controls.stdout` 1061 B, `c1-controls.exit` 2 B, `c2-controls.stdout` 684 B, `c2-controls.exit` 2 B, all
`present=yes`, all last touched by `6885adb40e3d5f2af061ab323d289b55e2a47bd3`, `descends-from-FREEZE=YES`
(`git merge-base --is-ancestor 14d03ea… <last-touch>`).

```
$ bash .ufo/evidence/round-49/deciding-run.sh "$S/clone" f181a96 14d03ea "$S/out-c"   # empty OUT
t=0.018s: FROZEN_UNCHANGED=1 freeze=14d03ea4270c6904064022b62b6faf467e5c0968 rev=f181a961ae44061af486f600e5ea257d2baf78f8
          -> killpg(SIGTERM) on the line
[rc=-15] out_listing=['frozen.stdout'] scr_exists=true scr_listing=[]
```

Kill mechanics (recorded, so the kill is not a claim): the child ran as a session/group leader
(`start_new_session=True`; `pid 2103100 pgid 2103100 equal True`), so `killpg` reached the script *and* its `tee`
child; `$S/out-c/frozen.stdout` holds exactly the `FROZEN_UNCHANGED=1` line, written before the kill; after the
kill `ps -eo pid,pgid,etimes,cmd | grep -F "$S/clone"` is empty. The script's own `rm -rf "$SCR"` (`:51`) never ran,
so its SCR directory survives **empty** — no `no-harm.sh` (`:34`), no monitor output (`:35–:42`), and no start
receipt or counter output (`:43–:48`). Three repeats (`out-c` again, a fresh `out-c3`, and the pid/pgid run) all
stopped on the same first line with rc=-15 and `out_listing=['frozen.stdout']` (`repeat.json`,
`case-c-repeats.stdout`). No counter was invoked at any revision; nothing here is a verdict.

### F4 — measured limit: the one-invocation guard is keyed to start receipts, which are written after the monitors

Attacks `:29`'s guarantee as stated ("one deciding invocation per counter"). `[ -e "$OUT/$k.start" ]` consults only
`$OUT/{c1,c2}.start`; those files are created at `:46` and `:43`, i.e. after `:35–:42` (no-harm, cold-read precheck,
census). An attempt that stops or dies before `:43` therefore leaves an OUT that the guard does not recognise as a
prior invocation. Measured: the `out-c` state left by F3 (`frozen.stdout` only, no start receipt) was accepted a
**second** time —

```
$ bash .ufo/evidence/round-49/deciding-run.sh "$S/clone" f181a96 14d03ea "$S/out-c"   # same dir, second run
FROZEN_UNCHANGED=1 freeze=14d03ea… rev=f181a96…
[rc=-15] out=['frozen.stdout'] scr_exists=true scr=[] counter_artifacts=[]
```

This is not a hole for the round-48 defect (no counter had started, so the first attempt was not a deciding
invocation), but the round report should not describe the guard as "at most one invocation" without the qualifier
"at most one invocation that reached a counter".

### F5 — measured limit: `:25` tests existence, not blob-ness

`git cat-file -e <rev>:<path>` exits 0 for a tree as well as a blob (`fixture.txt`):

```
$ git -C "$S/clone" cat-file -e f181a96:.ufo                       ; echo $?   # 0
$ git -C "$S/clone" cat-file -e f181a96:.ufo/evidence/round-49/control/c2-controls.exit ; echo $?  # 0
$ git -C "$S/clone" cat-file -e f181a96:.ufo/nope                  ; echo $?   # 128
```

So a directory committed at a receipt path would satisfy `:25` (and `git log -1 -- <path>` at `:26`). At REV the
four paths are blobs of the sizes above, so this is a property of the check, not a defect of this revision; no
fixture was built for it (it would require letting gate 0 pass again, which adds nothing to F3).

### F6 — measured: the FREEZE argument is checked in the right direction

Attacks `:27` orientation. Passing `FREEZE=REV` (d1) or `FREEZE=9b9b2a0` — a commit that already contains the
receipt commit `6885adb` — refuses rather than passing on a trivially empty `FREEZE..REV` diff:

```
$ … "$S/clone" f181a96 f181a96 "$S/out-d1"   -> DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-49/control/c1-controls.stdout  rc=3
$ … "$S/clone" f181a96 9b9b2a0  "$S/out-d2"  -> DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-49/control/c1-controls.stdout  rc=3
```

with `out=[]`, `scr_exists=false` in both. (`git merge-base --is-ancestor 6885adb 9b9b2a0` → YES, and
`… 9b9b2a0 6885adb` → NO, i.e. the refusal is the ancestor test firing, not a missing path.) Wave-1 reported a
different sub-case — a receipt committed *inside* the freeze commit passes `:27` by reflexivity — which I did not
re-test and am not relying on.

### F7 — recorded, deliberately not exercised: the counters are not coupled to the gate

`c1/measure.py:549–554` accepts only `--lane --rev --work --fleet --list --selftest`; `c2/measure.py:429–435` only
`--lane --rev --work --panel --generator-path --witness --selftest`; `grep -n 'controls\|\.start\|receipt'` over
both finds no read of a control receipt and no start-receipt write. A direct counter invocation at a revision is
therefore invisible to gate 0 — the fix constrains invocations *made through `deciding-run.sh`*. I verified the
lines only; I ran no counter (any run against the lane/REV would shade into a deciding run).

## Limits of this seat

- No counter was invoked at any revision, so "no counter starts" in (a)/(b) is established by the refusal's
  position relative to `:30` plus the absence of every downstream artifact, not by watching a counter not run.
- The three assigned cases all reproduce; F4–F7 are limits of the fix's reach, each labelled measured or code-read.
- I did not re-test wave-1's cases (receipt committed before FREEZE via a replace-ref fixture; synthetic receipt
  content; reflexivity at `:27`); nothing in this report depends on them.

## Reproduction

`.ufo/waves/round-49/w2/T49W2ExecMistake/`: `commands.txt` (setup, fixture build, all case command lines),
`cases.json` (argv, timestamped lines, OUT/SCR listings, exit codes), `repeat.json`, `repeat.py`, `drive.py`,
`fixture.txt` (clone toplevel and HEAD, REV/FREEZE, script blob + three sha256 values + freeze.json line, the four
receipts' presence/size/last-touch/ancestor facts, fixture-commit diff and isolation, `cat-file -e` exit codes,
FREEZE-direction facts, kill mechanics), `case-a1.stdout`, `case-a2.stdout`, `case-b1.stdout`, `case-b2.stdout`,
`case-c.stdout`, `case-c-repeats.stdout`, `case-d-freeze-arg.stdout`, `freeze-arg-cases.json`,
`deciding-run-executed.sh` (byte copy, `31e9838e…`).
Scratch `$S` was deleted after the receipts were copied here; the lane checkout, the fleet repo and
`~/.local/bin` were not written. Tooling: nothing installed or upgraded (git, bash, python3 as present).

## Summary

- Gate 0 was re-run independently in a scratch clone at `f181a961ae44061af486f600e5ea257d2baf78f8`; the executed
  blob is `5e059daf…`, sha256 `31e9838e…`, identical to `freeze.json:15`.
- (a) deleting exactly one receipt (`c2-controls.exit`, fixture commit `01af854…`) refuses at `:25` with
  `control-receipt-missing`, rc=3, empty OUT, SCR never created; the same run without the deletion passes gate 0.
- (b) a pre-existing `c1.start` (and `c2.start`) refuses at `:29` with `second-invocation`, rc=3, OUT untouched.
- (c) with all four receipts (last touch `6885adb`, descendant of the freeze) and an empty OUT, gate 0 prints
  `FROZEN_UNCHANGED=1` at t=0.018 s; the run was killed by `killpg` on that line — rc=-15, OUT holds only
  `frozen.stdout`, SCR empty, no monitor and no counter artifact; three repeats behave identically.
- Limits recorded: the one-invocation guard keys on start receipts written at `:43`/`:46`, so a pre-counter OUT is
  reusable (measured, second pass admitted); `:25` accepts a tree as well as a blob; a wrong FREEZE argument
  refuses; the counters take no gate input, so direct invocations remain invisible.
- No counter was invoked, no claim decided; all three assigned conditions reproduce.
