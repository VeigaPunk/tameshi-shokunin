# T48ExecObs2 — C1 independent observation run 2 of 3 (attestation receipts)

Seat: executor, round 48 / w1. Item: run the round-47 counter in `--emit` mode on the base tree
into an empty scratch work dir; deliver the three receipt files byte-exact; report wall time, the
`C1_R47:` line, the divergent `PROFILES` lines, and `df -h /fast` before/after.

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only).
REV: `473336d9d789f6081195e7376d17836a24666bc3` (contract `base_rev`).
BASE: `0b5b7cd2b2c15d23086e811a0f0348d84261277b`.
Counter: `.ufo/evidence/round-47/calibration/measure.py` (unmodified; `self_pin=1` in both runs,
so the file on disk hashes to the blob at REV).

## Deliverables (byte-exact, copied from the completed run 2)

| File | Bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-48/w1/T48ExecObs2.emit.stdout` | 19894 | `ba8edb765b5a59ebce89c4185a56e12b6700bbea81e7fc381e454c5d33965bd6` |
| `.ufo/waves/round-48/w1/T48ExecObs2.emit.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/waves/round-48/w1/T48ExecObs2.emit.exit` | 2 (`1\n`) | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |

stdout ends with a newline; 45 `STATEMENT`/`PROFILES` line pairs + 22 `EMIT_*` rows + the verdict line.
`stderr` is empty (0 bytes) in both runs.

## Two executions — provenance, read this before crediting the receipt

The assigned command was run **twice**. This is disclosed because the receipt must be complete and
honest, not because the first run's data was discarded.

**Run 1** — the exact assigned command through `bash`. The harness deadline (`timeout` 3600 s) killed
the process group *before* the shell could write `emit.exit` and `df -h /fast` (after), so the triple
was incomplete. Python had already produced its full stdout: 19867 bytes, ending with the verdict
line, last byte written 06:14:40 (T+34m02s from the 05:40:38 start). The `time` builtin never printed
(`emit.stderr` = 0 bytes), so run 1 has no measured wall time, only the 3600 s kill bound. Something in
that run's teardown did not return for the remaining ~26 minutes; the counter itself exits cleanly —
an `--only` probe on the same tree returns in 6.7 s with rc=1 (see *Probes* below).

**Run 2** — the same argv, same `--emit`, same REV/BASE, fresh empty work dir, executed under a
runner that captured the child's real return code and monotonic wall time. **This is the delivered
receipt.** Provenance of the three files: `.emit.stdout` / `.emit.stderr` are the child's own stdout
and stderr file descriptors; `.emit.exit` holds the child's actual `returncode` formatted exactly as
the shell's `echo $?` would write it (`1\n`). No value was inferred from the printed verdict.

Wall time, run 2: **1722.9 s (28m43s)**. Run 1 reached its last stdout byte at T+34m02s.

## Verdict line (identical in both runs)

```
C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=1 unparsed=0 unobservable=0 dep_mismatch=1 unpinned=0 append_only=1 total=2 rev=473336d9d789f6081195e7376d17836a24666bc3 C1_R47_PASS=false
```

`self_pin=1` and `stmts_pin=1`: the counter on disk and `statements.json`
(`924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`, 22 statements) both hash to
their blobs at REV. `total=2` = `mismatches=1` + `dep_mismatch=1`, both from the single statement below.

## Divergence against the round-47 deciding receipt

Round-47 deciding receipt: `.ufo/evidence/round-47/after/c1.stdout` (22 statements, 5 with unequal
profiles). Across all 22 statements, exactly **one** has a P0 tuple that differs from that receipt:
`six-leg regression ledger`. The other 21 P0 tuples are character-identical to round 47, and so are
all 21 remaining `PROFILES` lines.

### `six-leg regression ledger` — P0 differs from round 47, and this is the only differing statement

Round-47 P0: `REGRESSION: PASS (cases=9 passed=9|0`

Run 2 (delivered) — P0 differs from round 47, six profiles not all equal:

```
PROFILES six-leg regression ledger: P0=REGRESSION: FAIL (cases=9 passed=8|1 P1=REGRESSION: SETUP (cases=9 passed=8|2 P2=REGRESSION: FAIL (cases=9 passed=8|1 P3=REGRESSION: PASS (cases=9 passed=9|0 P4=REGRESSION: SETUP (cases=9 passed=4|2 P5=REGRESSION: SETUP (cases=9 passed=0|2
```

Run 1 (same seat, same tree, same argv; harness-killed, stdout complete) — P0 differs from run 2 and
from round 47's P0 in neither case being reproducible:

```
PROFILES six-leg regression ledger: P0=REGRESSION: PASS (cases=9 passed=9|0 P1=REGRESSION: PASS (cases=9 passed=9|0 P2=REGRESSION: PASS (cases=9 passed=9|0 P3=REGRESSION: PASS (cases=9 passed=9|0 P4=REGRESSION: SETUP (cases=9 passed=4|2 P5=REGRESSION: SETUP (cases=9 passed=0|2
```

Run 1's P0 is identical to round-47's P0 (`PASS passed=9|0`) — i.e. round 47's `PASS` is reproducible,
and so is run 2's `FAIL`, on the same tree and revision. The value is not a function of the tree.

Statement lines, both runs (declared deps are round 47's standing row):

```
RUN1 STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47 observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 (exit=0) MISMATCH declared_deps=env,fleet-root,node observed_deps=fleet-root,node DEPS-MISMATCH
RUN2 STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47 observed=REGRESSION: FAIL (cases=9 passed=8|1|a7d3f2dd7d47 (exit=1) MISMATCH declared_deps=env,fleet-root,node observed_deps=bwrap,env,fleet-root,jj,node DEPS-MISMATCH
```

Observed deps per observation (the counter's P1-as-reference rule): round 47 = `fleet-root,node`;
run 1 = `fleet-root,node`; run 2 = `bwrap,env,fleet-root,jj,node`. Intersection over the three =
`fleet-root,node`; union = all five names.

### The four other statements with unequal profiles (unchanged from round 47, reported as instructed)

Each has P0 equal to round 47's P0; only their non-P0 profiles differ, and they differ identically in
both of my runs and in the round-47 receipt.

```
PROFILES effective expectation reconciliation: P0=SELFTEST: PASS (66/66)|0 P1=SELFTEST: PASS (66/66)|0 P2=SELFTEST: PASS (66/66)|0 P3=UNOBSERVABLE|exit=1 P4=SELFTEST: PASS (66/66)|0 P5=SELFTEST: PASS (66/66)|0
PROFILES retained invocation-context gate: P0=SELFTEST: PASS (49/49)|0 P1=SELFTEST: PASS (49/49)|0 P2=SELFTEST: PASS (49/49)|0 P3=SELFTEST: PASS (49/49)|0 P4=SELFTEST: PASS (49/49)|0 P5=SELFTEST: PASS (49/49)|1
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 9/9 pass|0 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 9/9 pass|0 P4=ENVDIFF_SELFTEST: 8/9 pass|1 P5=ENVDIFF_SELFTEST: 9/9 pass|0
PROFILES mutation report interop: P0=MTE_SELFTEST: 17/17 pass|0 P1=MTE_SELFTEST: 17/17 pass|0 P2=MTE_SELFTEST: 17/17 pass|0 P3=MTE_SELFTEST: 17/17 pass|0 P4=UNOBSERVABLE|exit=2 P5=MTE_SELFTEST: 17/17 pass|0
```

`retained invocation-context gate` P5 is `|1` (same line text, different exit): that is the profile's
exit, so its six tuples are not all equal even though all six lines agree.

## Where the six-leg flake lands (evidence, not judgement)

Both runs' per-profile observation files were read; the divergence is one leg,
`bash-tsukuroi-census`, and inside it one selftest case. Quoted verbatim from the run-2 work dir
(scratch, since removed; the same paths are reproduced inside the delivered stdout's `log:` pointers):

- P0 (run 2): `REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1; log: .../P0/regression-wd/bash-tsukuroi-census/sweep.log)`
  and in that sweep, `DEFECT B10: SURVIVED (exit=0 duration-ms=7548) tsukuroi-census.sh:487-493` with
  `MUTATE: DONE (target=bash-tsukuroi-census defects=10 killed=7 survived=3 inconclusive=0 kill-rate=70%)`
  — the other eight legs report `defects=10` killed; this leg reports 7 of 10.
- P1 (run 2): `CONTROL: RED (exit=1 duration-ms=7218 ...)` on the pristine copy, then
  `TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)`. The one failing case:
  `FAIL blocked: nvidia hardware, driver offline: plane evidence missing: 'nvidia-smi not answering'; got: PLANE packages: HEALTHY (pacman -Qkk rc=0 sample=4(alpha,beta,gamma,delta) drift=0 backup_diffs=...`
- P3 (run 2), and every profile of run 1 except P4/P5: `REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`.

So the leg reads live host state (`nvidia-smi` answering) and one mutant survives when it does; the
leg's verdict is a function of the host at observation time, not of the tree. The declared dependence
set for this statement (`env,fleet-root,node` on the standing row) has no name for that dependence.

`P4` (node dropped) and `P5` (decoy fleet root) degrade to `SETUP` in both runs, for the reasons the
counter prints: `control run on the pristine copy is red (exit=127)` (node absent) and
`repo_identity_mismatch: ... is not its own repository; toplevel=unresolved` (decoy fleet).

## `df -h /fast`

Before (run 1 start, 05:40:38):
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  211G  593G  27% /fast
```
Run 2 bracket:
```
before: /dev/nvme1n1p2  804G  219G  585G  28% /fast
after:  /dev/nvme1n1p2  804G  221G  583G  28% /fast
```
After (end of run 2, 06:49): 804G total, 221G used, 583G avail, 28% — +10G used across both runs
(the six profiles clone the lane twice each per run and the regression sweeps write work dirs).

## Probes (seat-bounded, not verdicts)

- `--only 'staged-id adoption guard'` on REV into a fresh scratch work dir: rc=1 in 6.7 s,
  `C1_R47_PARTIAL: ... statements=1 ... total=0 rev=473336d9... C1_R47_PASS=false`. Used only to show
  the counter exits cleanly on this tree, i.e. run 1's missing exit file is a teardown/harness
  artifact, not a counter hang at `--emit`.
- No `--selftest`, no deciding run, no control scoring was performed by this seat.

## Risks and blockers

1. **The bash tool backend was starved for the whole seat.** Every `bash` call after the first was
   backgrounded and then killed at its deadline with "the shell backend did not respond" (a bare
   `ls -la`/`stat` did not return in 120-300 s). Host load average was 36.9 / 35.6 / 38.8 with 2913
   threads at 06:48. All file work in this report was done through the eval tool instead. This is why
   run 1 lost its exit file and why the receipt's exit code is recorded by a runner rather than by the
   shell's `echo $?`.
2. **Run 1 did not terminate for ~26 minutes after its last output byte** and was killed at 3600 s. If
   the L1 re-runs this command through the same bash backend, expect the same: the verdict and the
   full stdout are produced at ~28-34 min, and the exit file may never be written. Budget >60 min or
   capture the return code directly.
3. **`six-leg regression ledger` is genuinely nondeterministic on this tree**, with the flake pinned to
   `bash-tsukuroi-census` reading `nvidia-smi`. Two runs from one seat produced `PASS passed=9|0` and
   `FAIL passed=8|1` at P0. Any round-48 standing row for this statement that declares `stable` cannot
   be attested by these observations; and the five-name dep vocabulary has no name for the host-state
   dependence the sweep log shows.
4. **Counting caution for the L1:** my two runs are one seat, so they must not be counted as two of the
   R=3 independent observation rounds. The delivered receipt is run 2; run 1 is cited here only as
   corroboration (and as the sharper evidence that round 47's `PASS` was one draw from a set).
5. Scratch `/fast/scratch/hyaku/tameshi-r48/T48ExecObs2` was removed before this report was finished;
   no clone, work dir or temp file of this seat remains. Nothing in the lane was written except the
   three receipt files above and this report; no git/jj command was run in the lane; no package was
   installed or upgraded.
