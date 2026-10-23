# RerunV2 — independent rerun of counter v2 at the measurement revision

Seat: `TameshiR32.RerunV2` (advisory seat). Wave: round-32, wave 2.
Scope: observation only. This rerun does **not** replace the L1's first run
(`.ufo/evidence/round-32/after/c1v2-at-measurement.stdout`, exit 1, `C1_R32V2_PASS=false`).
The L1 `TameshiR32` remains the sole integrator; the tool at the measurement revision was not written by this seat.

## Verdict

**The L1's C1 miss is reproduced exactly. No difference in any held-out outcome.**

- Run 1 (fresh seed `ad89611ceb6c27e1`) and Run 2 (the L1's seed `63d2e2e95a1e35c5`) both print
  `ho_kill=1/10 ho_accept=8/12 ho_invalid=0 ... C1_R32V2_PASS=false`, exit **1**.
- All **22** held-out files are counter-valid (`valid=1`) in all three runs (L1 receipt, run 1, run 2);
  `ho_invalid=0` everywhere.
- Per-file held-out outcome, exit code and the tool's own `TALLY_AUDIT:` verdict are **byte-identical**
  across the L1 receipt and both of my runs: **0 of 22 files differ**.
- The counter is deterministic under a fixed seed: Run 2 and a repeated Run 3 (same seed) produce the same
  multiset of output lines; only the *order* of the `COPY` lines differs, because the counter shuffles
  copies with `random.Random(secrets.randbits(64))` before printing. Line order is not part of any verdict.

The failure is in the measured object, not in the counter or in the held-out set: the tool
`tools/tally-audit.py` at rev `24a5a5bb…` passes 9 of the 10 must-kill held-out copies (false PASS) and
wrongly rejects 4 of the 12 must-accept held-out copies (3 `FAIL`, 1 `SETUP`/exit 2).

## Evidence

### Environment and provenance

```
clone      : /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/clone
clone HEAD : 24a5a5bb598ae919546715267d76f814efaf8912  (== the measurement revision)
clone status: clean (`git status --porcelain` empty before and after both runs)
counter    : .ufo/evidence/round-32/v2/c1-measure-v2.py
             sha256 1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94
             (identical in my clone worktree, in the fleet worktree, and as the blob committed at the rev)
v1 counter : .ufo/evidence/round-32/c1-measure.py
             sha256 ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca (same in both trees)
held-out   : 22 files, byte-identical between the clone worktree and the rev
tool       : tools/tally-audit.py at the rev
             sha256 9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef
             == counter's TOOL_SHA256 (tool_sha_ok=1)
runner     : tools/mutate-and-run.sh at the rev
             sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
             == PINNED_RUNNER_SHA (runner_sha_ok=1)
tools used : bubblewrap 0.13.1 (/usr/bin/bwrap), python 3.14.8, git
installs   : none (no package installed or updated by this seat)
```

### Commands and exit codes

```
# clone (sandbox git only, in my own clone)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/clone

# Run 1 — fresh seed
cd /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/clone
timeout 1800 python3 .ufo/evidence/round-32/v2/c1-measure-v2.py \
  --lane /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/clone \
  --rev 24a5a5bb598ae919546715267d76f814efaf8912 \
  --work /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/work1
# exit 1   (stderr empty, 0 bytes)

# Run 2 — the L1's seed
timeout 1800 python3 .ufo/evidence/round-32/v2/c1-measure-v2.py \
  --lane /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/clone \
  --rev 24a5a5bb598ae919546715267d76f814efaf8912 \
  --seed 63d2e2e95a1e35c5 \
  --work /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/work2
# exit 1   (stderr empty, 0 bytes)

# Run 3 — the L1's seed again (determinism control, not part of the assignment)
timeout 1800 python3 .ufo/evidence/round-32/v2/c1-measure-v2.py \
  --lane /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/clone \
  --rev 24a5a5bb598ae919546715267d76f814efaf8912 \
  --seed 63d2e2e95a1e35c5 \
  --work /fast/scratch/hyaku/tameshi-r32-seats/RerunV2/work3
# exit 1   (stderr empty, 0 bytes)
```

Each `--work` directory was created empty before its run (the counter exits 2 on a non-empty `--work`);
each run took 27 s / 32 s / 31 s wall clock.

### The two C1_R32V2 lines

Run 1 (fresh seed `ad89611ceb6c27e1`):

```
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=ad89611ceb6c27e1 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

Run 2 (the L1's seed `63d2e2e95a1e35c5`):

```
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

Run 3 (the L1's seed repeated; determinism control):

```
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

The L1's first run, for comparison:

```
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

Exit codes: run 1 = 1, run 2 = 1, run 3 = 1; the L1's recorded exit file
`.ufo/evidence/round-32/after/c1v2-at-measurement.exit` contains `1`.

### Run 1 — every HELDOUT line and every `COPY src=ho` line

```
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-1.json valid=1 set=kill id=HeldOutGuard-1 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-2.json valid=1 set=kill id=HeldOutGuard-2 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-3.json valid=1 set=accept id=HeldOutGuard-3 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-4.json valid=1 set=accept id=HeldOutGuard-4 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-1.json valid=1 set=kill id=HeldOutLoop-1 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-2.json valid=1 set=kill id=HeldOutLoop-2 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-3.json valid=1 set=accept id=HeldOutLoop-3 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-4.json valid=1 set=accept id=HeldOutLoop-4 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-1.json valid=1 set=kill id=HeldOutPrintf-1 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-2.json valid=1 set=kill id=HeldOutPrintf-2 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-3.json valid=1 set=accept id=HeldOutPrintf-3 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-4.json valid=1 set=accept id=HeldOutPrintf-4 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a1.json valid=1 set=accept id=HeldOutRefactor-a1 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a2.json valid=1 set=accept id=HeldOutRefactor-a2 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a3.json valid=1 set=accept id=HeldOutRefactor-a3 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a4.json valid=1 set=accept id=HeldOutRefactor-a4 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-k1.json valid=1 set=kill id=HeldOutRefactor-k1 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-k2.json valid=1 set=kill id=HeldOutRefactor-k2 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-01.json valid=1 set=kill id=HeldOutTallyArms-01 author=HeldOutTallyArms
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-02.json valid=1 set=kill id=HeldOutTallyArms-02 author=HeldOutTallyArms
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-03.json valid=1 set=accept id=HeldOutTallyArms-03 author=HeldOutTallyArms
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-04.json valid=1 set=accept id=HeldOutTallyArms-04 author=HeldOutTallyArms
COPY src=ho set=kill id=HeldOutTallyArms-02.json outcome=ACCEPT exit=0 sha256=a3ae612ea6294170 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutRefactor-k2.json outcome=KILL exit=1 sha256=e5dbf0104c20186c last='TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)'
COPY src=ho set=kill id=HeldOutLoop-1.json outcome=ACCEPT exit=0 sha256=f9e0ac08a3da7242 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutLoop-2.json outcome=ACCEPT exit=0 sha256=51085f3a4e1a8ad9 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutTallyArms-01.json outcome=ACCEPT exit=0 sha256=f16185281b9e6dbe last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutPrintf-1.json outcome=ACCEPT exit=0 sha256=8b092abf1f3fd171 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutGuard-1.json outcome=ACCEPT exit=0 sha256=28176f17d8f5d72e last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutPrintf-2.json outcome=ACCEPT exit=0 sha256=e0142d719278f1f3 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutGuard-2.json outcome=ACCEPT exit=0 sha256=32d139f976f8c6eb last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutRefactor-k1.json outcome=ACCEPT exit=0 sha256=d55d0c5e772fc43f last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a3.json outcome=OTHER exit=2 sha256=2dd918c8ede34e46 last='TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)'
COPY src=ho set=accept id=HeldOutGuard-4.json outcome=ACCEPT exit=0 sha256=8fb8a090b1c9dc8f last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutTallyArms-04.json outcome=ACCEPT exit=0 sha256=e87e02a1b8dfc51c last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutTallyArms-03.json outcome=ACCEPT exit=0 sha256=529c4c631905bad0 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutLoop-4.json outcome=KILL exit=1 sha256=7be273bff723119c last='TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a1.json outcome=ACCEPT exit=0 sha256=d26e730d9e0d51e8 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a4.json outcome=KILL exit=1 sha256=f3888bd134c3d44e last='TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutLoop-3.json outcome=KILL exit=1 sha256=d0ba0a89bbf44eab last='TALLY_AUDIT: FAIL (static=fail runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a2.json outcome=ACCEPT exit=0 sha256=b79df45a003bf921 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutPrintf-4.json outcome=ACCEPT exit=0 sha256=abc9b1dabe71d8f2 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutPrintf-3.json outcome=ACCEPT exit=0 sha256=f3f57d4d2ca7a4fc last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutGuard-3.json outcome=ACCEPT exit=0 sha256=26a74300d8357e60 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
```

### Run 2 — every HELDOUT line and every `COPY src=ho` line

```
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-1.json valid=1 set=kill id=HeldOutGuard-1 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-2.json valid=1 set=kill id=HeldOutGuard-2 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-3.json valid=1 set=accept id=HeldOutGuard-3 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutGuard-4.json valid=1 set=accept id=HeldOutGuard-4 author=HeldOutGuard
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-1.json valid=1 set=kill id=HeldOutLoop-1 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-2.json valid=1 set=kill id=HeldOutLoop-2 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-3.json valid=1 set=accept id=HeldOutLoop-3 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutLoop-4.json valid=1 set=accept id=HeldOutLoop-4 author=HeldOutLoop
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-1.json valid=1 set=kill id=HeldOutPrintf-1 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-2.json valid=1 set=kill id=HeldOutPrintf-2 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-3.json valid=1 set=accept id=HeldOutPrintf-3 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutPrintf-4.json valid=1 set=accept id=HeldOutPrintf-4 author=HeldOutPrintf
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a1.json valid=1 set=accept id=HeldOutRefactor-a1 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a2.json valid=1 set=accept id=HeldOutRefactor-a2 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a3.json valid=1 set=accept id=HeldOutRefactor-a3 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-a4.json valid=1 set=accept id=HeldOutRefactor-a4 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-k1.json valid=1 set=kill id=HeldOutRefactor-k1 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutRefactor-k2.json valid=1 set=kill id=HeldOutRefactor-k2 author=HeldOutRefactor
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-01.json valid=1 set=kill id=HeldOutTallyArms-01 author=HeldOutTallyArms
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-02.json valid=1 set=kill id=HeldOutTallyArms-02 author=HeldOutTallyArms
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-03.json valid=1 set=accept id=HeldOutTallyArms-03 author=HeldOutTallyArms
HELDOUT file=.ufo/evidence/round-32/heldout/HeldOutTallyArms-04.json valid=1 set=accept id=HeldOutTallyArms-04 author=HeldOutTallyArms
COPY src=ho set=kill id=HeldOutRefactor-k1.json outcome=ACCEPT exit=0 sha256=d55d0c5e772fc43f last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutGuard-2.json outcome=ACCEPT exit=0 sha256=32d139f976f8c6eb last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutTallyArms-01.json outcome=ACCEPT exit=0 sha256=f16185281b9e6dbe last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutGuard-1.json outcome=ACCEPT exit=0 sha256=28176f17d8f5d72e last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutLoop-1.json outcome=ACCEPT exit=0 sha256=f9e0ac08a3da7242 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutLoop-2.json outcome=ACCEPT exit=0 sha256=51085f3a4e1a8ad9 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutPrintf-2.json outcome=ACCEPT exit=0 sha256=e0142d719278f1f3 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutPrintf-1.json outcome=ACCEPT exit=0 sha256=8b092abf1f3fd171 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutTallyArms-02.json outcome=ACCEPT exit=0 sha256=a3ae612ea6294170 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=kill id=HeldOutRefactor-k2.json outcome=KILL exit=1 sha256=e5dbf0104c20186c last='TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a4.json outcome=KILL exit=1 sha256=f3888bd134c3d44e last='TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a3.json outcome=OTHER exit=2 sha256=2dd918c8ede34e46 last='TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)'
COPY src=ho set=accept id=HeldOutLoop-3.json outcome=KILL exit=1 sha256=d0ba0a89bbf44eab last='TALLY_AUDIT: FAIL (static=fail runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutLoop-4.json outcome=KILL exit=1 sha256=7be273bff723119c last='TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a1.json outcome=ACCEPT exit=0 sha256=d26e730d9e0d51e8 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutRefactor-a2.json outcome=ACCEPT exit=0 sha256=b79df45a003bf921 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutGuard-3.json outcome=ACCEPT exit=0 sha256=26a74300d8357e60 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutGuard-4.json outcome=ACCEPT exit=0 sha256=8fb8a090b1c9dc8f last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutPrintf-3.json outcome=ACCEPT exit=0 sha256=f3f57d4d2ca7a4fc last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutPrintf-4.json outcome=ACCEPT exit=0 sha256=abc9b1dabe71d8f2 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutTallyArms-03.json outcome=ACCEPT exit=0 sha256=529c4c631905bad0 last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
COPY src=ho set=accept id=HeldOutTallyArms-04.json outcome=ACCEPT exit=0 sha256=e87e02a1b8dfc51c last='TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)'
```

### Per-file held-out comparison table (L1 receipt vs run 1 vs run 2)

| held-out file | set | valid L1/R1/R2 | outcome L1 | outcome R1 | outcome R2 | exit L1/R1/R2 | tool's own `TALLY_AUDIT:` verdict (identical in all three) | all three identical? |
|---|---|---|---|---|---|---|---|---|
| `.ufo/evidence/round-32/heldout/HeldOutGuard-1.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutGuard-2.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutGuard-3.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutGuard-4.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutLoop-1.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutLoop-2.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutLoop-3.json` | accept | 1/1/1 | KILL | KILL | KILL | 1/1/1 | `TALLY_AUDIT: FAIL (static=fail runtime=fail harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutLoop-4.json` | accept | 1/1/1 | KILL | KILL | KILL | 1/1/1 | `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutPrintf-1.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutPrintf-2.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutPrintf-3.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutPrintf-4.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutRefactor-a1.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutRefactor-a2.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutRefactor-a3.json` | accept | 1/1/1 | OTHER | OTHER | OTHER | 2/2/2 | `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutRefactor-a4.json` | accept | 1/1/1 | KILL | KILL | KILL | 1/1/1 | `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutRefactor-k1.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutRefactor-k2.json` | kill | 1/1/1 | KILL | KILL | KILL | 1/1/1 | `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutTallyArms-01.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutTallyArms-02.json` | kill | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutTallyArms-03.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |
| `.ufo/evidence/round-32/heldout/HeldOutTallyArms-04.json` | accept | 1/1/1 | ACCEPT | ACCEPT | ACCEPT | 0/0/0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes |

**Files compared: 22. Files differing between the L1 receipt, run 1 and run 2: 0.**

### Aggregate comparison

| quantity | L1 receipt | run 1 (fresh seed) | run 2 (L1 seed) | run 3 (L1 seed, repeat) |
|---|---|---|---|---|
| `v1_kill` | 18/18 | 18/18 | 18/18 | 18/18 |
| `v1_accept` | 8/8 | 8/8 | 8/8 | 8/8 |
| `ho_kill` | 1/10 | 1/10 | 1/10 | 1/10 |
| `ho_accept` | 8/12 | 8/12 | 8/12 | 8/12 |
| `ho_invalid` | 0 | 0 | 0 | 0 |
| `tool_sha_ok` / `runner_sha_ok` / `heldout_after_freeze` | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| `C1_R32V2_PASS` | false | false | false | false |
| exit | 1 | 1 | 1 | 1 |

### Where the run 1 (fresh seed) output differs from the L1 receipt

Only in the **v1 generated** copy families, which are seed-driven (`v1.generated_kill` / `v1.generated_accept`
draw from the seeded RNG). The frozen v1 families (all 15 non-`g` labels) are byte-identical in all runs.
The generated labels and their copy hashes differ, e.g. `gN03(or)` (L1, sha `741907e8…`) vs `gN03(split)`
(run 1, sha `16566843…`), `gD01(drop=st_roundgate,dup=st_mado)` vs `gD01(drop=st_tsu,dup=st_roundgate)`,
`gH03(form=2)` vs `gH03(form=1)`, `gH05(drop=7,dup=4)` vs `gH05(drop=3,dup=2)`,
`gT08(arm=165)` vs `gT08(arm=206)`, `gB6-permuted` and `gB7-nonce` (different copy bytes).
Every one of those variants was still killed/accepted correctly in both runs, so the aggregate is unchanged.
With the L1's seed the v1 output is byte-identical to the L1's receipt (same labels, same sha256s).
**The held-out section is seed-independent**: the same 22 files, the same verdicts, in every run and in the L1 receipt.

### Failure analysis of the measured object (observation, not a claim change)

The counter's own validity rules accepted all 22 held-out files (`ho_invalid=0`), so the held-out set is
mechanically sound. The misses come from the tool's verdict logic at rev `24a5a5bb…`:

- **False PASS on 9 of 10 must-kill copies** — `HeldOutGuard-1`, `HeldOutGuard-2`, `HeldOutLoop-1`,
  `HeldOutLoop-2`, `HeldOutPrintf-1`, `HeldOutPrintf-2`, `HeldOutRefactor-k1`,
  `HeldOutTallyArms-01`, `HeldOutTallyArms-02` all got `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`, exit 0.
  The single must-kill copy the tool did catch is `HeldOutRefactor-k2`, via `runtime=fail`.
- **False FAIL on 3 must-accept copies** — `HeldOutLoop-3` (`static=fail runtime=fail harness=pass`),
  `HeldOutLoop-4` (`static=pass runtime=fail harness=pass`), `HeldOutRefactor-a4` (`static=pass runtime=fail harness=pass`).
- **One must-accept copy aborts the tool** — `HeldOutRefactor-a3` exits 2 with
  `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)`: the copy's harness no longer
  contains the pinned `tblock=$(awk … "$SELF")` extraction line exactly once, so the tool refuses to audit it.

Because the tool is pinned by sha256 (counter `TOOL_SHA256`) and the round's kill rule states that a
counter run printing `C1_R32V2_PASS=false` at the measurement revision is reported as a miss and is never
re-scaled, re-seeded or amended, **no correction is admissible at this revision**. The smallest correction
belongs to a later round (a tool whose static/runtime/harness checks cover the guard-, printf-, loop- and
refactor-shaped edits above, re-audited under a fresh seal). This seat changed nothing in the fleet repo.

### Risks, blockers

- None for the rerun itself: both runs completed inside the 25-minute box, no timeout, no non-zero stderr,
  no fleet file touched except this report, no git write in the fleet repo.
- Not verified here (out of scope for this seat): whether the tool can be repaired without breaking the
  `tools/mutate-and-run.sh` byte-identity condition, and what the repair's cost is. The tool's
  `runtime` and `static` checks are the two surfaces that produced the wrong verdicts; the `SETUP` abort
  on `HeldOutRefactor-a3` is a third surface (anchor-exactness of the harness extraction line).
- Raw stdout of every run is kept in this seat's scratch at
  `/fast/scratch/hyaku/tameshi-r32-seats/RerunV2/logs/run{1,2,3}.{stdout,stderr,exit}`.
