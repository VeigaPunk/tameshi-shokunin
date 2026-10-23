# CtlAlwaysFail — pre-data control for C1 (always-fail lookalike of tally-audit-v2.py)

Seat: `tameshi-r33-w1-CtlAlwaysFail`. Wave 1, pre-data control. Lane rev under test:
`f6d8a891f1d966c5c3cdda385090da3a6e804675` (clone, detached). No production file touched.

## Verdict

**Control behaves as required: the frozen counter catches the always-fail shortcut.**
Scored against the counter bytes committed at the frozen rev, my control rows as
`kill=18/18 accept=0/8 predicate_pass=False`, `all_false=True`, counter exit 0. No control of mine
ever reached `predicate_pass=true`.

**Two counter-side interface defects found** (not defects of the control; both are in
`c1-measure.py` as committed at the rev, and both are cheap to fix before the receipt is minted):

- **F1** The prescribed controls command cannot run: the top-level parser has no `--receipt`, so the
  exact command exits 2 (`unrecognized arguments: --receipt ...`) and no receipt is written.
- **F2** `write_controls()` re-parses `sys.argv` with a positional `tools` list. Under the prescribed
  argument order it takes the value of `--lane` (a directory named `lane`) as the control tool, runs
  it (0/18, 0/8), and still reports `all_false=True` with exit 0. **A receipt of that shape passes
  the default-mode controls gate (`counter_sha256` match + `all_false is True`) without any control
  tool having been executed.** Correct argument order (or an explicit tool list) is required.

Both are stated precisely below with the smallest safe correction. They do not change my verdict.

## Setup and pins

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/lane
  -> clone_exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../CtlAlwaysFail/lane \
  checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675
  -> checkout_exit=0
df -h /fast -> 804G total, 34G free (scratch use here is a few MB)
```

Pins verified at the rev (both match `contract.json`):

```
git -C lane show f6d8a...:tools/mutate-and-run.sh | sha256sum
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9   (contract runner_sha256)
git -C lane show f6d8a...:tools/tally-audit-v2.py | sha256sum
  9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4   (contract tool_sha256)
git -C lane show f6d8a...:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum
  7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6
```

The control is invoked by the counter exactly as `python3 -I <tool> --runner <copy>`
(`.ufo/evidence/round-32/c1-measure.py:177-196`); a kill is `rc==1` plus a last `TALLY_AUDIT:` line
starting `TALLY_AUDIT: FAIL`, an accept is `rc==0` plus `TALLY_AUDIT: PASS`.

## Control tool (full source)

Path: `/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/ctl.py`
sha256 `101dd5b625119df69c26b86fbd212e176d1502381ba9a0dd1f566748959f9509`, 926 bytes, unchanged
before and after every run (`sha256sum -c ctl.sha.before` -> `ctl.py: OK`).

```python
#!/usr/bin/env python3
"""Always-fail control lookalike of tools/tally-audit-v2.py (round 33, C1 pre-data control).

Interface mimicry: `python3 -I ctl.py --runner COPY` prints one line to stdout whose text begins
`TALLY_AUDIT: FAIL (...)` and exits 1. It never reads or audits the runner copy: every runner,
pristine included, is reported as a failure. This is the shortcut the frozen counter must catch
(predicate_pass=false, all_false=true).
"""
import sys


def main(argv):
    runner = None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == '--runner' and i + 1 < len(argv):
            runner = argv[i + 1]
            i += 2
            continue
        if a.startswith('--runner='):
            runner = a.split('=', 1)[1]
        i += 1
    print('TALLY_AUDIT: FAIL (always-fail control: runner %r not audited)' % (runner,))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
```

Standalone check on the pristine runner (the runner it should have accepted):

```
python3 -I ctl.py --runner lane/tools/mutate-and-run.sh; echo "ctl_exit=$?"
TALLY_AUDIT: FAIL (always-fail control: runner 'lane/tools/mutate-and-run.sh' not audited)
ctl_exit=1
```

Because the counter runs against committed bytes (`git show LANE:path`), I ran the counter itself
from an extracted copy of the committed file, with its round-32 dependency mirrored beside it:
`frozen/.ufo/evidence/round-33/c1/c1-measure.py` (7ff776df...) and
`frozen/.ufo/evidence/round-32/c1-measure.py` (ecb26529...). It reads only from `--lane`, and its
`show(lane, rev, SELF_PATH)` path means the receipt still pins the committed counter sha.

## Runs (each `--work` fresh and empty)

### Route 1 — the prescribed command, verbatim

```
timeout 900 python3 frozen/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/w6 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/ctl.py \
  --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/receipt.json
  > route1.out 2> route1.err; echo $? > route1.exit
route1_exit=2
route1.out: (empty)
route1.err:
usage: c1-measure.py [-h] --lane LANE --rev REV --work WORK [--seed SEED]
                     [--write-controls WRITE_CONTROLS [WRITE_CONTROLS ...]]
c1-measure.py: error: unrecognized arguments: --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/receipt.json
```

No `receipt.json` was created. Cause: `--receipt` exists only on the inner parser inside
`write_controls()` (`c1-measure.py:224-225`), while `main()` parses strictly with a parser that
omits it (`c1-measure.py:257-267`), so dispatch never happens. The same failure occurs against the
live lane copy.

### Route 2 — prescribed order, without the unsupported `--receipt`

```
timeout 900 python3 frozen/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/w5 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/ctl.py
  > route2.out 2> route2.err; echo $? > route2.exit
route2_exit=0
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/lane/.ufo/evidence/round-33/c1/controls-receipt.json
  lane kill=0/18 accept=0/8 predicate_pass=False
```

The row is named `lane`, not `ctl.py`: `write_controls()` builds its own parser with a positional
`tools` (`c1-measure.py:223-226`) and calls `parse_known_args()` on the whole `sys.argv`, so the
first bare token after an unknown option — the path supplied to `--lane` — is taken as the control
tool. A directory is handed to `python3 -I`, which fails to execute it, so both counters stay at
zero. `all_false=True`, exit 0. Receipt: `receipt-misparsed.json` (tool `lane`, `kill 0/18`,
`accept 0/8`).

### Route 3 — control list first, so the positional binds to the control

```
timeout 900 python3 frozen/.ufo/evidence/round-33/c1/c1-measure.py \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/ctl.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/w7
  > route3.out 2> route3.err; echo $? > route3.exit
route3_exit=0
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/lane/.ufo/evidence/round-33/c1/controls-receipt.json
  ctl.py kill=18/18 accept=0/8 predicate_pass=False
```

Receipt written (`receipt-scored.json`, seed differs per run):

```json
{
 "all_false": true,
 "controls": [{"accept": "0/8", "kill": "18/18", "predicate_pass": false, "tool": "ctl.py"}],
 "counter": "c1-measure.py",
 "counter_sha256": "7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6",
 "runner_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
 "seed": "a326c40e8d2ff739"
}
```

The control is correctly killed on all 18 public must-kill copies and correctly never accepts any of
the 8 must-accept copies. The counter does what the item asks: an always-fail shortcut cannot reach
the predicate.

## Findings and smallest safe correction

**F1 (operability).** The frozen counter rejects its own documented receipt path. Because the
prescribed command is the one the wave is told to run, the first attempt fails with exit 2. The
smallest fix is to hoist the flag to the parser that dispatches:

```python
# main()
ap.add_argument('--receipt', default=None)
...
if a.write_controls is not None:
    return write_controls(a.lane, a.rev, a.work, seed, a.write_controls,
                          a.receipt or os.path.join(a.lane, CONTROLS_PATH))
```
and change `write_controls(lane, rev, work, seed)` to accept `(lane, rev, work, seed, tools,
receipt_path)`, deleting the inner parser and its `parse_known_args()` re-parse.

**F2 (vacuous gate).** Any argv order in which `--lane` precedes `--write-controls` makes the
receipt name a directory as its control. `all_false=True` then carries no information, yet it is
exactly the field the default mode gate trusts (`c1-measure.py:286-291`). Minimal hardening, in
addition to F1: iterate the explicit `tools` list received from `main()`, and refuse to score a
non-file:

```python
if not os.path.isfile(tpath):
    raise CounterError('control tool is not a file: %r' % tpath)
```

With that guard, route 2 exits 2 with `C1_R33: SETUP (control tool is not a file: .../lane)`
instead of minting a receipt. Recommend minting the committed receipt from a verbose log that
shows `ctl.py kill=18/18 accept=0/8`, and keeping an always-fail control in the committed controls
set.

**Observation (not a finding against the tool).** The lane's working-tree counter changed twice
while this seat ran: committed at the rev `7ff776df...`, live at `15:41:19` `69d8188c...`, live again
`50aca8cb...`. The `69d8188c...` intermediate is broken: running it raises
`NameError: name 'a' is not defined` at `c1-measure.py:245` via the call at line 267 (captured in
`reordered.err`), and it had a different `--receipt` plumbing than the committed bytes. All numbers
in this report come from the committed bytes at the frozen rev, not from the moving tree. Whoever
mints the receipt should extract the counter at the measurement rev.

## Bounds and restoration evidence

- No production file was written; the only writes are under
  `/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysFail/` and this report.
- `ctl.py` sha256 `101dd5b6...9509` before and after all runs (`sha256sum -c ctl.sha.before` -> OK).
- No mutation of the runner or tool was performed (this is a control seat, not a mutation probe):
  the clone's `tools/mutate-and-run.sh` still hashes `a7d3f2dd...2eb9` and `tools/tally-audit-v2.py`
  `9dbbce62...33a4` at the rev, i.e. pristine.
- No counter default-mode run was executed (controls mode only, per the item and round-32
  closure item 2).
- No `git` write commands anywhere; no `jj` command anywhere; no process spawned outside the
  scratch dir and none left running; no tools installed or upgraded (nothing was needed).
- Scratch layout: `lane/` (clone), `frozen/` (extracted committed counters), `w1`..`w7` (empty or
  used work dirs), `route1/2/3.{out,err,exit}`, `receipt-scored.json`, `receipt-misparsed.json`,
  `ctl.py`, `ctl.sha.before`.
