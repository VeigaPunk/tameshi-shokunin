# CtlAlwaysPass — round 33 wave 1, C1 pre-data control

## Verdict

PASS for this control item. The always-pass lookalike was caught by the amended counter:
`ctl.py kill=0/18 accept=8/8 predicate_pass=False`, `all_false=True`, counter exit 0. The control
got no must-kill copy right and all 8 must-accept copies right, so it never meets the C1 predicate.

Disclosure as requested by the L1 steer: I did fail one counter run with the frozen bytes before
the amendment was available. The exact tasked command against the frozen counter exited 2 because
the frozen artifact has no `--receipt` option (details in "Frozen-bytes history"). The authoritative
row below comes from amendment 1 at commit `27902a165aa932dabf65f0e13d55cb202b4cd770`.

## Control built

Path: `/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/ctl.py`
sha256: `ed13d65e58c7662c4e238f53303b7aa31159a2316cace560dd3a65adb7c06f09`

It mimics the CLI and output shape of `tools/tally-audit-v2.py`, reads the runner bytes (so the run
does real I/O and reports a byte count), then unconditionally prints PASS and exits 0. No head,
static, runtime or harness check is performed.

```python
#!/usr/bin/env python3
"""Control lookalike for tools/tally-audit-v2.py: interface-mimicking, audit-shortcut.

Reads the runner (so the run does real I/O), then always prints PASS and exits 0.
No static check, no runtime sweep, no harness panel. It exists only to give the round-33
C1 controls counter an always-pass control to score (expected: predicate_pass=false).
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', default=None)
    ap.add_argument('--then-regression', action='store_true')
    ap.add_argument('--workdir', default=None)
    ap.add_argument('--selftest', action='store_true')
    a, _unknown = ap.parse_known_args()

    path = a.runner or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'tools', 'mutate-and-run.sh')
    try:
        with open(path, 'rb') as f:
            body = f.read()
        size = len(body)
        legs = body.count(b'st_js')
    except OSError:
        size = -1
        legs = -1

    # Touch the bytes so the shortcut is not a pure constant: no decision depends on them.
    sys.stdout.write('CHECK head PASS (runner=%s bytes=%d)\n' % (os.path.basename(path), size))
    sys.stdout.write('CHECK static PASS (legs-mentions=%d)\n' % legs)
    sys.stdout.write('CHECK runtime PASS\n')
    sys.stdout.write('CHECK harness PASS\n')
    sys.stdout.write('TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

Standalone proof that it does not discriminate (scratch probe, exit 0):

```
pristine_sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
kill-copy T08 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy N05 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy H03 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy H04 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy H05 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy N01 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy N02 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy N03 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
kill-copy D01 ctl_exit 0 last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
pristine ctl_exit 0 stdout_last 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
```

The public panel is 18 kill copies (9 frozen + 9 generated) and 8 accept copies (6 frozen +
2 generated), counted directly from the imported round-32 module.

## Amended counter run (authoritative)

Fetch of the amended bytes, as instructed:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  27902a165aa932dabf65f0e13d55cb202b4cd770:.ufo/evidence/round-33/c1/c1-measure.py \
  > /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/c1-measure.py; echo $? > amended-fetch.exit
```

Exit `0`; sha256 of the fetched file
`edd8fbb0b6e4e235a3a59a86553715c5d27c28a7bb074c2df3dadd31351e531f`, 362 lines. The amended
counter imports the round-32 module through a path relative to itself (`HERE/../../round-32/...`),
so I placed the unchanged bytes at
`mirror/.ufo/evidence/round-33/c1/c1-measure.py` with the round-32 counter copied to
`mirror/.ufo/evidence/round-32/c1-measure.py`. Both amended copies hash `edd8fbb0...`; the shim
changes the import path only, not the counter bytes.

Command (fresh empty work directory `w8`; exit captured separately):

```
timeout 2400 python3 mirror/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/w8 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/ctl.py \
  --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/receipt.json \
  > amended.stdout 2> amended.stderr; echo $? > amended.exit
```

Exit `0` (`amended.exit`). Stdout verbatim:

```
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/receipt.json
  ctl.py kill=0/18 accept=8/8 predicate_pass=False
```

Stderr empty. Receipt `receipt.json`:

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
 "counter_sha256": "7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6",
 "runner_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
 "seed": "22123cb674b86a57"
}
```

A second amended run with the lane flag first (fresh work `w9`, receipt `receipt-lanefirst.json`)
also exited 0 with the same row, so the amendment removed the frozen counter's argv-order
sensitivity:

```
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/receipt-lanefirst.json
  ctl.py kill=0/18 accept=8/8 predicate_pass=False
```

## Frozen-bytes history (disclosure)

These runs predate the amendment and are recorded because the L1 asked for the frozen failure. The
live working-tree copy was also being edited during these probes; the committed amendment bytes
(`edd8fbb0...`) are what the authoritative run used. All exit codes below were captured as
`cmd; echo $? > file`.

A. Exact tasked command, 15:40:51, frozen-era live counter: exit `2` (`counter.exit`). Stdout empty,
stderr verbatim:

```
usage: c1-measure.py [-h] --lane LANE --rev REV --work WORK [--seed SEED]
                     [--write-controls WRITE_CONTROLS [WRITE_CONTROLS ...]]
c1-measure.py: error: unrecognized arguments: --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlAlwaysPass/receipt.json
```

B. Frozen clone copy, `--write-controls` first, 15:41:39 (counter sha
`7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6`): exit `0`, row
`ctl.py kill=0/18 accept=8/8 predicate_pass=False`, `all_false=True`.

C. Frozen clone copy, lane flag first, 15:41:53: exit `0`, row
`lane kill=0/18 accept=0/8 predicate_pass=False`, `all_false=True`. The controls parser scored the
lane directory instead of the control tool (finding below).

D. Frozen clone copy with `--receipt`, 15:42:10: exit `2`, same usage error as run A
(`frozen-receipt-reject.exit`).

E. Diagnostic run at rev `27902a16` against my clone, 15:43: exit `2` with
`C1_R33: SETUP (runner not found at 27902a16...)`. The amendment commit is not in my clone, which
was taken before it landed; this probe is inconclusive and is not a counter defect.

## Findings

### 1. Frozen counter missing `--receipt` (fixed by amendment 1)

At `f6d8a89`, `--receipt` existed only in a nested parser inside `write_controls` (line 225) while
main's parser had no such option (lines 257-263) and used `parse_args`. Runs A and D show the
result: exit 2, no receipt. The amended bytes `edd8fbb0...` add `--receipt` to main (line 261) and
pass it into `write_controls` (line 267). Verified by the authoritative run, exit 0.

### 2. Frozen counter scored the wrong file by argv order (fixed by amendment 1)

The frozen `write_controls` re-parsed `sys.argv` (lines 222-226) and iterated `a.tools` (line 238).
With the contract's flag order, the first non-option token is the lane path, so the "control" row
was `lane` with `accept=0/8`. Only the receipt field `all_false` was checked by the default-mode
gate (lines 287-288), so such a receipt would have passed the gate without any control tool having
run. The amendment takes `tools` from main's parsed `--write-controls`, and the second amended run
above shows the same correct row with either flag order.

### 3. The receipt still attests the committed counter at REV, not the executing bytes

The amended `write_controls` still computes `self_bytes` with `git show REV:SELF_PATH`
(lines 231-233) and stamps that hash at line 243. With `--rev f6d8a89` the receipt therefore names
`7ff776df...` while the executing counter is `edd8fbb0...`. The default-mode gate compares the
receipt's `counter_sha256` against committed counter bytes at its own REV (lines 287-288), so a
receipt produced at `f6d8a89` does not attest the amended counter at a later measurement revision
[INFERENCE from lines 231-233, 243-244 and 287-288; the hash mismatch itself is observed]. The
controls receipt for the committed run should be produced with `--rev` at the commit that contains
the amended counter, or `write_controls` should hash `__file__`.

### 4. The control itself was caught

No finding of `predicate_pass=true`. The control got all 8 accept copies right (PASS, exit 0) and
all 18 must-kill copies wrong (PASS where FAIL is required). The `accept=8/8` count also shows the
control really ran in the authoritative run, unlike the lane-path misgrab in Finding 2.

## Smallest safe correction

I made no production edits. For the L1:

1. Produce the committed controls receipt with `--rev` set to the commit that holds the amended
   counter (or a descendant), so `counter_sha256` names the bytes that ran (Finding 3).
2. Optionally hash the executing file (`__file__`) instead of `show(REV, SELF_PATH)`; the fallback
   already does this when the path is absent at REV (lines 232-233), so the committed path is the
   only gap.
3. When checking a controls receipt, also require the `tool` entries to be the intended control
   paths and the accept count to equal the full accept panel; `all_false` alone hid the frozen
   lane-path misgrab (Finding 2).

## Restoration and hygiene evidence

- The lane clone is at `f6d8a891f1d966c5c3cdda385090da3a6e804675`; `git status` shows only
  `?? .ufo/evidence/round-33/c1/controls-receipt.json`, written by the frozen counter inside the
  scratch clone. `git diff --stat` is empty; no tracked file changed.
- Clone hashes after all probes: runner `a7d3f2dd...2eb9`, tool `9dbbce62...33a4`, frozen counter
  `7ff776df...8cc6`.
- The amended counter bytes were read from the lane with `git show` (read-only) into scratch; no
  production file was written. No `git` write command ran outside the scratch clone; no `jj`
  command ran anywhere.
- No processes started by this seat remain; a `/proc/*/cwd` scan for this scratch directory
  returned nothing.
- No tools were installed or upgraded.
