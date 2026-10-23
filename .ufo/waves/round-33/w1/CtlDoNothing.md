# CtlDoNothing — pre-data control for C1 (do-nothing lookalike of tally-audit-v2.py)

Seat: `tameshi-r33-w1-CtlDoNothing`. Wave 1, pre-data control. Lane rev under test:
`f6d8a891f1d966c5c3cdda385090da3a6e804675` (scratch clone, detached). No production file touched;
no `git` write command and no `jj` command was run anywhere.

## Verdict

**The control is caught.** Under the amended counter (commit `27902a16`, amendment 1), controls mode
reports `ctl.py kill=0/18 accept=8/8 predicate_pass=False`, `all_false=True`, exit 0. The do-nothing
shortcut never reaches `predicate_pass=true`.

**Frozen-bytes note for the L1 (as requested):** my first attempt used the tasking's exact command
against the frozen counter at `f6d8a89` and failed with exit 2 — the frozen parser rejects
`--receipt`. No receipt was written and no scoring happened in that run. Amendment 1 fixes that.
Every scoring number below comes from the amended counter; the frozen-counter runs are retained only
as evidence of the two interface defects.

The `accept=8/8` is incidental, not credit: an unconditional `TALLY_AUDIT: PASS` coincides with the
expected verdict on the 8 must-accept copies by construction. All 18 must-kill copies escaped
(`kill=0/18`), and `predicate_pass` requires `kill_hit == kill_total`, so the shortcut is rejected.

## Setup and pins

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane
  -> CLONE_EXIT=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../CtlDoNothing/lane \
  checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675
  -> exit 0; git rev-parse HEAD = f6d8a891f1d966c5c3cdda385090da3a6e804675
df -h /fast -> 804G total, 34G free (this seat used a few MB)
```

Pins verified (both match `contract.json`):

```
sha256sum lane/tools/mutate-and-run.sh
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
sha256sum lane/tools/tally-audit-v2.py
  9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4
git -C lane show f6d8a...:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum
  7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6   (frozen counter)
```

Amended counter, extracted read-only from the lane at `27902a16` into my scratch (mirrored tree so
its `HERE/../../round-32/c1-measure.py` import resolves):

```
git -C <lane> show 27902a16:.ufo/evidence/round-33/c1/c1-measure.py \
  > amended/.ufo/evidence/round-33/c1/c1-measure.py        -> exit 0
  edd8fbb0b6e4e235a3a59a86553715c5d27c28a7bb074c2df3dadd31351e531f
git -C <lane> show 27902a16:.ufo/evidence/round-32/c1-measure.py \
  > amended/.ufo/evidence/round-32/c1-measure.py          -> exit 0
  ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca
```

The amendment touches only `write_controls()` and `main()` (10 insertions, 10 deletions): it hoists
`--receipt` to the dispatching parser, passes the `--write-controls` list explicitly, and uses
`receipt_path` throughout. Predicate, kill rule and label are untouched by the diff.

Frozen before-value (`c1-at-base.stdout`) shows the counter runs and is false:

```
C1_R33: tool_present=0 tool_sha_ok=0 runner_sha_ok=1 controls_ok=0(not-checked) v1_kill=0/0 v1_accept=0/0 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 heldout_after_freeze=0 seed=2ce55dbe3f51538e rev=66e1fb444615b3afe380e7df0244ef7fae1dd985 C1_R33_PASS=false
```

The counter invokes a tool as `python3 -I <tool> --runner <copy>`
(`.ufo/evidence/round-32/c1-measure.py:177-196`); a kill needs `rc==1` and a last line starting
`TALLY_AUDIT: FAIL`, an accept needs `rc==0` and `TALLY_AUDIT: PASS`.

## Control tool (full source)

Path `/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/ctl.py`, 885 bytes, sha256
`7587926d41161466abb244c775d4f20f3484376011c164a6ce697bacc1536d29` (unchanged before and after
every run).

```python
#!/usr/bin/env python3
"""Control (do-nothing) lookalike of tools/tally-audit-v2.py.

Interface mimicry only: same final stdout line shape, same exit code range.
The audit is short-circuited: --runner is parsed but never opened, hashed or run.
A correct counter must score this control predicate_pass=false.
"""
import argparse
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', default='tools/mutate-and-run.sh')
    ap.add_argument('--then-regression', action='store_true')
    ap.add_argument('--workdir', default=None)
    ap.add_argument('--selftest', action='store_true')
    ap.parse_args()
    # No file is read. No runner is inspected. Always accept.
    print('TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        raise
```

Shortcut proof on a runner that does not exist — the control still accepts:

```
python3 ctl.py --runner /nonexistent/runner.sh; echo "EXIT=$?"
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
EXIT=0
```

## Runs (each `--work` fresh; exits captured with `cmd; echo $? > file`)

### Route 1 — tasking's exact command, frozen counter bytes (fails)

```
timeout 2400 python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/w1 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/ctl.py \
  --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/receipt.json \
  > route1-missing.out 2> route1-missing.err; echo $? > w1-exit.txt
```

`w1-exit.txt = 2`, `route1-missing.out` empty, `route1-missing.err` verbatim:

```
usage: c1-measure.py [-h] --lane LANE --rev REV --work WORK [--seed SEED]
                     [--write-controls WRITE_CONTROLS [WRITE_CONTROLS ...]]
c1-measure.py: error: unrecognized arguments: --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/receipt.json
```

No receipt was written and `w1` stayed empty (`w1_entries=0`): dispatch never reached controls
mode. This is the known frozen defect that amendment 1 repairs.

### Route 2 — frozen counter, documented controls form (mis-binds the tool)

```
timeout 900 python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/w4 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/ctl.py
  ; echo $? > formB-frozen-exit.txt
```

`formB-frozen-exit.txt = 0`, output:

```
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane/.ufo/evidence/round-33/c1/controls-receipt.json
  lane kill=0/18 accept=0/8 predicate_pass=False
```

The row is named `lane`, not `ctl.py`: the frozen `write_controls()` re-parses `sys.argv` with a
positional `tools` list, so the value of `--lane` is bound as the control. My control was never
executed. The receipt (`receipt-formB-frozen.json`) still says `all_false: true` with exit 0, i.e.
it would satisfy the default-mode controls gate having scored nothing. Amendment 1 removes the
re-parse and passes the list explicitly, so this is repaired as well.

### Route 3 — frozen counter, value syntax that binds the control (`=` forms)

```
timeout 2400 python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane=/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane \
  --rev=f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work=/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/w2 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/ctl.py
  ; echo $? > frozen-exit.txt
```

`frozen-exit.txt = 0`, output verbatim:

```
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane/.ufo/evidence/round-33/c1/controls-receipt.json
  ctl.py kill=0/18 accept=8/8 predicate_pass=False
```

### Route 4 — amended counter, exact steered command (`--receipt` supported)

```
timeout 2400 python3 amended/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/w-amended \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/ctl.py \
  --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/receipt-amended.json
  ; echo $? > amended-exit.txt
```

`amended-exit.txt = 0`, output verbatim:

```
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/receipt-amended.json
  ctl.py kill=0/18 accept=8/8 predicate_pass=False
```

### Route 5 — amended counter, `--rev` at the amendment commit (receipt pins amended bytes)

Same as route 4 with `--lane /home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only `git show`
access) and `--rev 27902a165aa932dabf65f0e13d55cb202b4cd770`, fresh work `w-amended-279`:

```
amended-279-exit.txt = 0
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/receipt-amended-279.json
  ctl.py kill=0/18 accept=8/8 predicate_pass=False
```

## Receipts

Authoritative control result (identical in routes 3, 4, 5; seed differs):

```json
{
 "all_false": true,
 "controls": [
  {
   "accept": "8/8",
   "kill": "0/18",
   "predicate_pass": false,
   "tool": "ctl.py"
  }
 ],
 "counter": "c1-measure.py",
 "counter_sha256": "<see below>",
 "runner_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
 "seed": "<per run>"
}
```

`counter_sha256` by run:

| run | executed counter | `--rev` | `counter_sha256` | receipt sha256 |
|---|---|---|---|---|
| 3 (`receipt.json`) | frozen `7ff776df` | f6d8a89 | `7ff776df...f8cc6` | `293d946c...1553` |
| 4 (`receipt-amended.json`) | amended `edd8fbb0` | f6d8a89 | `7ff776df...f8cc6` | `05aa780d...65f8` |
| 5 (`receipt-amended-279.json`) | amended `edd8fbb0` | 27902a16 | `edd8fbb0...531f` | `d04cc7bb...2f22` |

Routes 4 and 5 differ only in `--rev`, yet the pinned counter sha differs: the receipt records the
counter committed at `--rev`, not the bytes that actually ran. For the default-mode controls gate
(`c1-measure.py:277-293`, comparing the receipt to `show(rev, SELF_PATH)`) the receipt must be minted
with `--rev` at the measurement revision. Route 5 shows the shape that matches the amended counter.

## Findings and corrections

**F1 (fixed by amendment 1).** The frozen dispatching parser omitted `--receipt`; the prescribed
controls command exited 2. Amendment `27902a16` hoists the flag and passes
`(seed, receipt_path, tools)` into `write_controls()`.

**F2 (fixed by amendment 1).** The frozen `write_controls()` re-parsed `sys.argv` with a positional
`tools` list, so the `--lane` value could be scored as the control while `all_false=True` was still
reported. The amended function iterates the explicit list from the dispatching parser. A residual
hardening, not required by the diff, is to refuse a non-file tool:

```python
if not os.path.isfile(tpath):
    raise CounterError('control tool is not a file: %r' % tpath)
```

**F3 (open, procedural).** The controls receipt's `counter_sha256` is the sha of the counter
committed at `--rev`, not of the executing file. Route 4 demonstrates the divergence
(executes `edd8fbb0`, pins `7ff776df`). Consequence for the L1: mint the committed controls receipt
with `--rev` at the measurement revision, or the gate will reject it (`sha-or-allfalse-mismatch`).
Recording `sha256(open(__file__, 'rb').read())` next to the committed sha would make the divergence
visible.

**Observation.** The lane's working-tree counter changed several times while this seat ran:
committed `7ff776df`, then live `69d8188c`, `50aca8cb`, and finally `edd8fbb0` (the committed
amendment). The `50aca8cb` intermediate raised `NameError: name 'a' is not defined` at the summary
print after writing a correct receipt. All scoring numbers here come from extracted copies of
committed bytes, never from the moving tree.

## Recommendation for the receipt mint

Mint from the amended counter at the measurement rev (route 5 shape) with this control in the
controls set. Expected verbose line: `ctl.py kill=0/18 accept=8/8 predicate_pass=False`, so
`all_false=True`. Keep this control: it is the variant that exercises the must-accept side fully
(8/8) while failing every must-kill copy.

## Bounds and restoration evidence

- No production file written; no mutation of the runner or the tool. The clone's
  `tools/mutate-and-run.sh` still hashes `a7d3f2dd...2eb9` and `tools/tally-audit-v2.py`
  `9dbbce62...33a4`.
- Writes are confined to `/fast/scratch/hyaku/tameshi-r33-seats/CtlDoNothing/` and this report. The
  only file changed inside the clone is the untracked default receipt path
  `lane/.ufo/evidence/round-33/c1/controls-receipt.json`, restored to the route-3 receipt
  (`sha256 293d946c...1553`) after the route-2 demo.
- `ctl.py` sha256 `7587926d...6d29` before and after all runs.
- Controls mode only; no default-mode counter run; no fixed `--seed` (the counter generated each).
- No tool installed or upgraded (nothing was needed); no pacman transaction attempted.
- No process from this seat remains. Controls mode spawns no `bwrap`; the `bwrap` processes visible
  during the run belong to `kumitate-r48*` seats (their command lines point at those scratch trees),
  were not started by me, and were left untouched.
- Scratch layout: `lane/` (clone at f6d8a89), `amended/` (committed counter `7ff776df` plus the
  amended `edd8fbb0` tree at `.ufo/evidence/round-33/c1/` with its round-32 dependency), `ctl.py`,
  `w1` (empty, route 1), `w2` (route 3), `w4` (route 2), `w-amended` (route 4), `w-amended-279`
  (route 5), `receipt*.json`, `*-exit.txt`, `route1-missing.{out,err}`.
