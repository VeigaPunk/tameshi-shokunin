# PanelCheckA — public panel calibration (round-33 w1)

Seat: `tameshi-r33-w1-PanelCheckA-4`
Date: 2026-10-23

## Verdict

The public v1 panel is live and calibrated as expected. The frozen round-32 v1
tool meets it, and the frozen round-33 v2 tool meets it too on the **same** v1
panel (same counter, same copy families and seeds). **No findings** — deviation
from the expected numbers.

- v1 (frozen `tools/tally-audit.py`): `kill=18/18 accept=8/8 other=0
  runner_sha_ok=1 tool_present=1 C1_R32_PASS=true` on both runs (default seed and
  `--seed 0123456789abcdef`).
- v2 (frozen `tools/tally-audit-v2.py`): identical numbers on both runs via the
  same counter (only the tool-path constant changed to point at the v2 blob).

## Setup (scratch only)

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/PanelCheckA
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r33-seats/PanelCheckA/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  f6d8a891f1d966c5c3cdda385090da3a6e804675
# setup_exit=0
```

Identity checks on the frozen blobs:

- `git show f6d8a891...:tools/tally-audit.py | sha256sum` → `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`, byte-identical (`git diff --stat 66e1fb44 f6d8a89 -- tools/tally-audit.py` empty) to the round-32 v1 freeze `66e1fb444615b3afe380e7df0244ef7fae1dd985:tools/tally-audit.py`. So the v1 runs score exactly the specified frozen v1 tool.
- `git show f6d8a891...:tools/tally-audit-v2.py | sha256sum` → `9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4` (matches the working tree). `git show 66e1fb44:tools/tally-audit-v2.py` fails (exit 128) — the v2 blob exists only at the round-33 freeze, as expected.
- Runner pin: `tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (PASSNED_RUNNER_SHA); the counter verified `runner_sha_ok=1` at the frozen rev.

## Counter

Used the frozen round-32 counter `round-32/c1-measure.py` verbatim for the two v1
runs. For the two v2 runs the same counter was copied into this seat's scratch and
its `TOOL` constant was changed from `tools/tally-audit.py` to
`tools/tally-audit-v2.py` (one line; everything else — predicates, copy families,
labels, seeding, panel — untouched). This is the only way the counter can be
pointed at the v2 blob; the counter itself has no tool-path argument. No lane or
production file was touched.

## Runs (receipt discipline: `cmd; echo $? > file`)

Run 1 — v1, default seed:
```
timeout 2200 python3 c1-measure-v1.py --lane lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 --work w1
# exit 0
# C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1
#   seed=f8f241eaf88098b1 rev=f6d8a891f1d966c5c3cdda385090da3a6e804675
#   C1_R32_PASS=true
```

Run 2 — v1, seeded replay:
```
timeout 2200 python3 c1-measure-v1.py --lane lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 --seed 0123456789abcdef --work w2
# exit 0
# C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1
#   seed=0123456789abcdef rev=f6d8a891f1d966c5c3cdda385090da3a6e804675
#   C1_R32_PASS=true
```

Run 3 — v2, default seed:
```
timeout 2200 python3 c1-measure-v2.py --lane lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 --work w3
# exit 0
# C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1
#   seed=c735d6de6db10382 rev=f6d8a891f1d966c5c3cdda385090da3a6e804675
#   C1_R32_PASS=true
```

Run 4 — v2, seeded replay:
```
timeout 2200 python3 c1-measure-v2.py --lane lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 --seed 0123456789abcdef --work w4
# exit 0
# C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1
#   seed=0123456789abcdef rev=f6d8a891f1d966c5c3cdda385090da3a6e804675
#   C1_R32_PASS=true
```

All four runs printed 26 `COPY` lines each (18 must-kill, 8 must-accept), every
must-kill copy `outcome=KILL`, every must-accept `outcome=ACCEPT`, `other=0`.

## Residual risk / verification gaps

- The v2 run is a panel calibration, not a v2-claim measurement: the round-32
  counter has no v2-specific rows (it does not include the four v1-defeated
  families, the run-vector pair sweep, or the `--then-regression` timeout). The
  v2 claim itself will be measured in wave 2 by the round-33 C1 counter on a fresh
  sealed set.
- Run 2/4 used the seeded replay `0123456789abcdef`; run 1/3 used fresh random
  seeds. Both generators of the panel were exercised.
- Report file written at `/.ufo/waves/round-33/w1/PanelCheckA.md` (lane-relative
  path). Scratch artifacts live only under
  `/fast/scratch/hyaku/tameshi-r33-seats/PanelCheckA/`.
