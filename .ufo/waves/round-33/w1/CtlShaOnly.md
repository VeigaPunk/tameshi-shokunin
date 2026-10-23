# CtlShaOnly — pre-data control for C1 (sha256-equality shortcut lookalike of `tally-audit-v2.py`)

Seat: `tameshi-r33-w1-CtlShaOnly`. Wave 1, pre-data control for C1. Lane rev under test:
`f6d8a891f1d966c5c3cdda385090da3a6e804675` (clone, detached). No production file was written.
Counter amendment 1 (`27902a1…`) was used as instructed by the L1 steer.

## Verdict

1. **Control killed.** Rows produced by the amended counter (the L1's instructed route):
   `ctl.py kill=18/18 accept=1/8 predicate_pass=False`, `all_false=True`, counter exit 0.
   No control of mine ever reached `predicate_pass=true`. The sha-equality shortcut is caught.
2. **The item's literal command could not run against the pre-amendment bytes** — recorded below
   because it happened: live production path `NameError` (exit 1, twice), committed bytes
   `unrecognized arguments: --receipt` (exit 2). Amendment 1 fixes exactly this.
3. **Gate trap, still open after amendment 1 (material for the mint).** The amended counter pins
   `counter_sha256` from `show(lane, rev, SELF_PATH)`, not from the running file. Minting with
   `--rev f6d8a89` therefore writes a receipt naming the *pre-amendment* counter sha
   `7ff776df…`, while any measurement rev carrying amendment 1 has counter bytes `edd8fbb0…`.
   Default mode compares the receipt against `show(measurement_rev, SELF_PATH)` and would report
   `controls_details=sha-or-allfalse-mismatch`, i.e. C1 cannot pass. Mint at a rev whose
   `SELF_PATH` bytes are `edd8fbb0…` (both receipts are below as evidence).
4. **Coverage note, not a finding against the tool.** A hash compare gets all 18 public kills
   right for free: every kill copy is a byte edit. The whole discrimination against this shortcut
   rests on the accept panel — 7 of 8 public accept copies differ in bytes; only `B0-pristine`
   is byte-identical. The kill panel alone cannot distinguish an audit from a hash comparison.

## Pins and setup

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/lane
  -> clone_exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../CtlShaOnly/lane \
  checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675
  -> checkout_exit=0
df -h /fast -> 804G total, 34G free (scratch here ~180 MB, mostly the clone)
```

Pins at the rev (match `contract.json`):

```
lane/tools/mutate-and-run.sh    a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
lane/tools/tally-audit-v2.py    9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4
frozen c1-measure.py at rev     7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6
amendment 1 c1-measure.py        edd8fbb0b6e4e235a3a59a86553715c5d27c28a7bb074c2df3dadd31351e531f
round-32 dependency (at rev)     ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca
```

Counter invocation semantics (frozen counter, `.ufo/evidence/round-33/c1/c1-measure.py`): the tool
runs as `python3 -I <tool> --runner <copy>` (`.ufo/evidence/round-32/c1-measure.py:177-196`); a kill
is `rc==1` with a last `TALLY_AUDIT:` line starting `TALLY_AUDIT: FAIL`, an accept is `rc==0` with
`TALLY_AUDIT: PASS`. Controls mode scores against the 18 public kill + 8 public accept panel
(`c1-measure.py:243-252` pre-amendment; `:221-252` amended).

## Control tool (full source)

Path: `/fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/ctl.py`
sha256 `4bc160675c044904dc9069eeee93392f969d4be807ca48a41269b653b4e04630`, 1200 bytes, unchanged
across every run reported below.

```python
#!/usr/bin/env python3
"""Round 33 C1 pre-data control: a SHORTCUT lookalike of tools/tally-audit-v2.py.

It mimics the interface (final stdout line `TALLY_AUDIT: PASS|FAIL (...)`; exit 0 on PASS,
1 on FAIL, 2 on SETUP) but performs no audit at all: it hashes the runner copy and compares
that hash with the pristine runner's digest. Equal -> PASS, different -> FAIL.

This is a deliberately defective tool: it cannot distinguish a behavior-preserving rewrite
from a fault. The controls receipt must record predicate_pass=false for it.
"""
import argparse
import hashlib
import os
import sys

PRISTINE_SHA = 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', required=True)
    a = ap.parse_args()
    try:
        with open(a.runner, 'rb') as f:
            got = hashlib.sha256(f.read()).hexdigest()
    except OSError as e:
        print('TALLY_AUDIT: SETUP (%s)' % e)
        return 2
    if got == PRISTINE_SHA:
        print('TALLY_AUDIT: PASS (sha=%s)' % got[:12])
        return 0
    print('TALLY_AUDIT: FAIL (sha=%s)' % got[:12])
    return 1


if __name__ == '__main__':
    sys.exit(main())
```

Standalone interface checks (the tool's own behavior, no counter involved):

```
python3 -I ctl.py --runner probe-mut.sh; echo "mut_exit=$?"
TALLY_AUDIT: FAIL (sha=9bed0e7f9d57)
mut_exit=1
python3 -I ctl.py --runner lane/tools/mutate-and-run.sh; echo "pris_exit=$?"
TALLY_AUDIT: PASS (sha=a7d3f2dd7d47)
pris_exit=0
```

`probe-mut.sh` is the clone's pristine runner with one trailing `#x` added to the tally-start line.

## Amendment 1 route (the L1's instructed command)

Extraction into a mirrored tree so the counter's `HERE/../../round-32/c1-measure.py` dependency
resolves inside scratch:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  27902a165aa932dabf65f0e13d55cb202b4cd770:.ufo/evidence/round-33/c1/c1-measure.py \
  > amended/.ufo/evidence/round-33/c1/c1-measure.py; echo $? > extract-amended.exit   -> 0
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  f6d8a891f1d966c5c3cdda385090da3a6e804675:.ufo/evidence/round-32/c1-measure.py \
  > amended/.ufo/evidence/round-32/c1-measure.py; echo $? > extract-v1.exit           -> 0
```

`27902a1` is a descendant of the freeze rev (`git merge-base --is-ancestor f6d8a89 27902a1` ->
exit 0); it changes only the counter file (10 insertions, 10 deletions).

### Route A — instructed rev `f6d8a89` (row correct, receipt sha stale)

```
timeout 900 python3 amended/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/w9 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/ctl.py \
  --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/receipt.json
  > amended-f6d8a89.out 2>&1; echo $? > amended-f6d8a89.exit
amended-f6d8a89.exit = 0
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/receipt.json
  ctl.py kill=18/18 accept=1/8 predicate_pass=False
```

`receipt.json`:

```json
{
 "all_false": true,
 "controls": [{"accept": "1/8", "kill": "18/18", "predicate_pass": false, "tool": "ctl.py"}],
 "counter": "c1-measure.py",
 "counter_sha256": "7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6",
 "runner_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
 "seed": "372c0fbb7c6989b9"
}
```

The row is right; the pinned `counter_sha256` is the pre-amendment counter, because
`c1-measure.py:231` takes `show(lane, rev, SELF_PATH)` at `f6d8a89`.

### Route B — a rev whose counter bytes are amendment 1 (gate-consistent mint)

Sandbox mirror inside my own clone (permitted writes, my clone only): branch `amend1` at the
freeze rev, amended counter bytes committed unchanged.

```
git -C lane checkout -q -b amend1 f6d8a89...; echo $? > amend1-checkout.exit          -> 0
cp amended/.ufo/evidence/round-33/c1/c1-measure.py lane/.ufo/evidence/round-33/c1/c1-measure.py
git -C lane add .ufo/evidence/round-33/c1/c1-measure.py
git -C lane commit -q -m "scratch seat: mirror round-33 amendment 1 counter bytes ..."
  -> amend1-commit.exit = 0
git -C lane rev-parse HEAD -> 0e88df90299fd56454fabf20cded1ddcfe5d3f37   (amend1-rev.txt)
sha256sum lane/.ufo/evidence/round-33/c1/c1-measure.py
  edd8fbb0b6e4e235a3a59a86553715c5d27c28a7bb074c2df3dadd31351e531f
```

```
timeout 900 python3 amended/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/lane \
  --rev 0e88df90299fd56454fabf20cded1ddcfe5d3f37 \
  --work /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/w10 \
  --write-controls /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/ctl.py \
  --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/receipt-amended-rev.json
  > amended-mirror.out 2>&1; echo $? > amended-mirror.exit
amended-mirror.exit = 0
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/receipt-amended-rev.json
  ctl.py kill=18/18 accept=1/8 predicate_pass=False
```

`receipt-amended-rev.json`:

```json
{
 "all_false": true,
 "controls": [{"accept": "1/8", "kill": "18/18", "predicate_pass": false, "tool": "ctl.py"}],
 "counter": "c1-measure.py",
 "counter_sha256": "edd8fbb0b6e4e235a3a59a86553715c5d27c28a7bb074c2df3dadd31351e531f",
 "runner_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
 "seed": "7955ca951f897fd4"
}
```

`git -C lane show 0e88df90...:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum` ->
`edd8fbb0b6e4e235a3a59a86553715c5d27c28a7bb074c2df3dadd31351e531f`, so this receipt names
exactly what a measurement rev carrying amendment 1 will compare against. A production rev carrying
`27902a1` has the same `SELF_PATH` bytes, so this mint is valid for it too.

## Per-copy evidence: which copies the shortcut got right

A scratch driver (`score_ctl.py`) loads the committed counter module from the clone at the freeze
rev, prints each public-panel copy's sha equality with the pristine runner, then calls the frozen
`write_controls()` with an explicit tool and receipt (pre-amendment function; seed
`ctlshaonly-seed`). Command: `timeout 1200 python3 score_ctl.py; echo $? > ctl-exit-direct.txt`
-> exit 0.

```
pristine_sha=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
COPY kill         pub-T08 sha_equal=0
COPY kill         pub-N05 sha_equal=0
COPY kill         pub-H03 sha_equal=0
COPY kill         pub-H04 sha_equal=0
COPY kill         pub-H05 sha_equal=0
COPY kill         pub-N01 sha_equal=0
COPY kill         pub-N02 sha_equal=0
COPY kill         pub-N03 sha_equal=0
COPY kill         pub-D01 sha_equal=0
COPY kill         pub-gT08(arm=97) sha_equal=0
COPY kill         pub-gN05(< nlegs) sha_equal=0
COPY kill         pub-gH03(form=1) sha_equal=0
COPY kill         pub-gH04(:) sha_equal=0
COPY kill         pub-gH05(drop=0,dup=5) sha_equal=0
COPY kill         pub-gN01(vector=3) sha_equal=0
COPY kill         pub-gN02(or) sha_equal=0
COPY kill         pub-gN03(or) sha_equal=0
COPY kill         pub-gD01(drop=st_citecheck,dup=st_sourcescheck) sha_equal=0
COPY accept       pub-B0-pristine sha_equal=1
COPY accept       pub-B1-T07 sha_equal=0
COPY accept       pub-B2-reversed sha_equal=0
COPY accept       pub-B3-decoys sha_equal=0
COPY accept       pub-B4-cosmetic sha_equal=0
COPY accept       pub-B5-renamed sha_equal=0
COPY accept       pub-gB6-permuted sha_equal=0
COPY accept       pub-gB7-nonce sha_equal=0
C1_R33_CONTROLS: controls=1 all_false=True receipt=/fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/receipt.json
  ctl.py kill=18/18 accept=1/8 predicate_pass=False
write_controls_rc=0
```

Every kill copy differs in bytes from the pristine runner, so the hash compare flags all 18
without reading the runner. Exactly one accept copy (`B0-pristine`) is byte-identical; the other
seven are behavior-preserving rewrites that the shortcut rejects — that is where it dies
(`accept=1/8`). The same row was reproduced through the amended CLI twice (routes A and B).

## Pre-amendment failures (recorded because they occurred)

### Frozen committed bytes, item's literal command

```
timeout 300 python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane .../lane --rev f6d8a891... --work .../w7 \
  --write-controls .../ctl.py --receipt .../receipt2.json
  > committed-cli-receipt.out 2>&1; echo $? > committed-cli-receipt.exit
committed-cli-receipt.exit = 2
usage: c1-measure.py [-h] --lane LANE --rev REV --work WORK [--seed SEED]
                     [--write-controls WRITE_CONTROLS [WRITE_CONTROLS ...]]
c1-measure.py: error: unrecognized arguments: --receipt /fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/receipt2.json
```

Cause: `--receipt` existed only on an inner parser inside `write_controls()` (`c1-measure.py:223-226`
at the rev); `main()` parsed strictly without it (`:257-263`) and never dispatched. No receipt
was written.

### Live production path (moving working tree)

The production counter was being edited concurrently during this seat. Snapshots observed:
`7ff776df…` (committed at the rev), `69d8188c…` at 15:41:06, `50aca8cb…` at 15:41:35,
`edd8fbb0…` at 15:42:29 (= amendment 1 bytes). Two runs of the item's literal command against the
live path both failed:

```
first run (tree 69d8188c, 15:41:06): NameError at c1-measure.py:245
  os.makedirs(os.path.dirname(a.receipt), exist_ok=True); exit 1
second run (tree 50aca8cb): captured verbatim in named-run.out, exit 1 (named-run.exit)
  File ".../c1-measure.py", line 267, in main
    return write_controls(a.lane, a.rev, a.work, seed, a.receipt, a.write_controls)
  File ".../c1-measure.py", line 249, in write_controls
    print('C1_R33_CONTROLS: controls=%d all_false=%s receipt=%s' % (len(rows), all_false, a.receipt))
  NameError: name 'a' is not defined
```

### Phantom receipt from the frozen inner parser (pre-amendment, corroborating a sibling finding)

Contract-form command (no `--receipt`, which the frozen CLI cannot take):

```
timeout 2400 python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
  --lane .../lane --rev f6d8a891... --work .../w2 \
  --write-controls .../ctl.py
  > /dev/null; echo $? > ctl-exit-contractform.txt
ctl-exit-contractform.txt = 0
C1_R33_CONTROLS: controls=1 all_false=True receipt=.../lane/.ufo/evidence/round-33/c1/controls-receipt.json
  lane kill=0/18 accept=0/8 predicate_pass=False
```

The row is named `lane` (a directory), not `ctl.py`: the inner parser's positional `tools`
(`:224,226,238`) binds the argument of whichever option appears first in argv. Reproduced with the
same parser shape in isolation:

```
prescribed order -> tools= ['.../CtlShaOnly/lane']
reordered order  -> tools= ['.../CtlShaOnly/ctl.py']
```

Receipt `receipt-phantom-lane.json` records `tool: "lane"`, `kill 0/18`, `accept 0/8`,
`all_false: true`, `counter_sha256: 7ff776df…`. The default-mode gate reads only
`counter_sha256` equality plus `all_false is True` (`:287-288`), so before amendment 1 a receipt
of that shape satisfied the controls gate without any control tool having been scored. Amendment 1
passes an explicit `tools` list from `main()` (`:267`) and no longer re-parses argv; it does not
add a non-file guard, but the phantom path is gone.

## Smallest safe corrections

1. **Mint at an amendment-bearing rev** (open item). Because `counter_sha256` comes from
   `show(rev, SELF_PATH)` (`amended c1-measure.py:231,243`), the mint must use `--rev` whose
   counter bytes are `edd8fbb0…` (production `27902a1` or a later rev with unchanged counter
   bytes). Then the receipt passes the `:287-288` gate at the measurement rev. If instead the
   counter sha is meant to identify the running file, hash `__file__` rather than `show(rev)`;
   either fix is one line, and the first needs no code change.
2. **Optional hardening, one line**: refuse to score a non-file control, so a mis-bound argument
   cannot produce a zero row that reads like a real failing control:
   `if not os.path.isfile(tpath): raise CounterError('control tool is not a file: %r' % tpath)`.
3. **Optional coverage note for sealed authoring**: the kill panel is free for any hash compare;
   only byte-differing accept copies test audit behavior. Keep behavior-preserving rewrites in the
   sealed accept set.

## Self-correction during this seat

My first scoring attempt returned `ctl.py kill=0/18 accept=0/8` because of a typo I introduced
while renaming a constant in `ctl.py` (`PRistine_SHA` left in the use site: every copy raised
`NameError`, so every copy was `OTHER`). That intermediate file was sha
`f7d27ef775352c8ecfe189ac30210b50218773bd6c98ce0fd56e9263ca52cb33`; the fix to `PRISTINE_SHA`
produced the reported file `4bc160675c044904dc9069eeee93392f969d4be807ca48a41269b653b4e04630`.
All rows above come from the fixed file. This was my defect, not the counter's.

## Bounds and restoration evidence

- Writes: only this report and files under
  `/fast/scratch/hyaku/tameshi-r33-seats/CtlShaOnly/`. No production file was created or edited.
- No counter default-mode run was executed (controls mode only, per the item and round-32 closure
  item 2). No sealed/held-out files touched.
- Clone restored: `git -C lane checkout -q --detach f6d8a89...` -> `restore.exit=0`;
  `git -C lane rev-parse HEAD` -> `f6d8a891f1d966c5c3cdda385090da3a6e804675`;
  `git -C lane status --porcelain` -> empty. Branch `amend1` (`0e88df90…`, counter bytes
  `edd8fbb0…`) is retained in the scratch clone for reproducibility of route B.
- Pins unchanged after every run (`hashes-after.txt`):
  `lane/tools/mutate-and-run.sh a7d3f2dd…2eb9`, `lane/tools/tally-audit-v2.py 9dbbce62…33a4`,
  `ctl.py 4bc16067…4630`.
- No `git` write command ran anywhere except my own scratch clone (the `amend1` branch/commit and
  the checkouts shown above). No `jj` command anywhere. No production git index or lane jj state
  touched.
- No processes left behind (`pgrep -af 'CtlShaOnly'` -> empty); every long run wrapped in
  `timeout`; each exit captured with `cmd; echo $? > file` as `*.exit`.
- No tools installed or upgraded (none were needed); `df -h /fast` -> 34G free.
- Scratch layout: `lane/` (clone at the rev), `amended/` (extracted amended counter plus its
  round-32 dependency), `ctl.py`, `score_ctl.py`, `probe-mut.sh`, `w1..w10` (work dirs),
  `receipt.json`, `receipt-amended-rev.json`, `receipt-cli-scored.json`,
  `receipt-phantom-lane.json`, `*.out`, `*.exit`, `hashes-{before,after,final}.txt`,
  `amend1-rev.txt`, `restore.exit`.
