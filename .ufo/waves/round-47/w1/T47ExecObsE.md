# T47ExecObsE — C1 dependence observation, five statements (round 47 / wave 1)

Seat: `T47ExecObsE`, leaf executor. Item: observe the six profiles for `bounded ANSI-C code_view`,
`write-path-census-v2`, `write-path census destination resolution`, `staged-id adoption guard`,
`six-leg regression ledger`, twice, and root-cause every observed dependence.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, freeze rev `9acfbe21435e1976636a276448dee1d5e7155915`, base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`.
- Counter: `.ufo/evidence/round-47/calibration/measure.py`. Both runs printed `self_pin=1 stmts_pin=1` (the counter hashed itself and `statements.json` to the frozen digests), `append_only=1`.
- Mode: seat probe (`--only`), so the verdict line is `C1_R47_PARTIAL`; this is not a deciding run.
- Nothing in the lane was edited except this report. No tool was installed or upgraded (no pacman, uv, npm, cargo call). Scratch: `/tmp/tameshi-r47-T47ExecObsE` (deleted after capture) and `/var/tmp/tameshi-r47-T47ExecObsE` (kept).

## 1. Exact commands

Run 1 and run 2 (one shell, both backgrounded, `wait`):

```
mkdir -p /tmp/tameshi-r47-T47ExecObsE/w1 /tmp/tameshi-r47-T47ExecObsE/w2
( python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
    --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
    --work /tmp/tameshi-r47-T47ExecObsE/w1 \
    --only "bounded ANSI-C code_view,write-path-census-v2,write-path census destination resolution,staged-id adoption guard,six-leg regression ledger" \
    --emit > /tmp/tameshi-r47-T47ExecObsE/run1.log 2>&1 ; echo "RUN1_EXIT=$?" >> /tmp/tameshi-r47-T47ExecObsE/run1.log ) &
( python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
    --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
    --work /tmp/tameshi-r47-T47ExecObsE/w2 \
    --only "bounded ANSI-C code_view,write-path-census-v2,write-path census destination resolution,staged-id adoption guard,six-leg regression ledger" \
    --emit > /tmp/tameshi-r47-T47ExecObsE/run2.log 2>&1 ; echo "RUN2_EXIT=$?" >> /tmp/tameshi-r47-T47ExecObsE/run2.log ) &
wait
```

Wall time 1339 s for the pair; both exited 1 (`C1_R47_PARTIAL`, `unparsed=5` — the freeze rows carry
no deps clause yet, as the item says to ignore).

Auxiliary probes (scratch only, no lane writes, no verdict):

```
# B10 selftest isolation, P3 shim (no jj) and P1 shim (jj), 3 runs each
env -i PATH=<shim> HOME=<d>/home TMPDIR=<d>/tmp LANG=C LC_ALL=C TZ=UTC bash b10.sh --selftest
# 12 concurrent repeats with the P3 shim
# two full ledger replays under the exact P3 env at the freeze rev
cd $R/fleet/tameshi-shokunin && env -i PATH=/tmp/.../w2/P3/shim HOME="$R/home" TMPDIR="$R/tmp" \
  LANG=C LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 REV=9acfbe21435e1976636a276448dee1d5e7155915 \
  bash tools/mutate-and-run.sh --regression --workdir "$R/regression-wd"
# the :771 construct, census-sized output, 4 x 3000 iterations under 16 CPU spinners
```

`b10.sh` is `w2/P3/regression-wd/bash-tsukuroi-census/mutant-B10.target.tsukuroi-census.sh`
(materialized by the sweep from the pinned blob). `$R/dep-P3-{a,b}/fleet` mirrors the counter's
P1-P5 layout: one symlink per sibling lane into `/home/vgpnk/Projects/shokunin` plus a clone of the
lane at the freeze inside `fleet/`.

## 2. Verdict and PROFILES lines

Run 1:

```
C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=5 mismatches=0 unparsed=5 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=5 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
PROFILES six-leg regression ledger: P0=REGRESSION: PASS (cases=9 passed=9|0 P1=REGRESSION: PASS (cases=9 passed=9|0 P2=REGRESSION: PASS (cases=9 passed=9|0 P3=REGRESSION: PASS (cases=9 passed=9|0 P4=REGRESSION: SETUP (cases=9 passed=4|2 P5=REGRESSION: SETUP (cases=9 passed=0|2
PROFILES bounded ANSI-C code_view: P0=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P1=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P2=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P3=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P4=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P5=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0
PROFILES write-path-census-v2: P0=WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0|0 P1=WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0|0 P2=WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0|0 P3=WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0|0 P4=WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0|0 P5=WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0|0
PROFILES write-path census destination resolution: P0=WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0|0 P1=WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0|0 P2=WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0|0 P3=WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0|0 P4=WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0|0 P5=WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0|0
PROFILES staged-id adoption guard: P0=STAGED_ID_GUARD_SELFTEST: cases=24 failed=0|0 P1=STAGED_ID_GUARD_SELFTEST: cases=24 failed=0|0 P2=STAGED_ID_GUARD_SELFTEST: cases=24 failed=0|0 P3=STAGED_ID_GUARD_SELFTEST: cases=24 failed=0|0 P4=STAGED_ID_GUARD_SELFTEST: cases=24 failed=0|0 P5=STAGED_ID_GUARD_SELFTEST: cases=24 failed=0|0
```

Run 2 — byte-identical except the first `PROFILES` line:

```
C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=5 mismatches=0 unparsed=5 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=5 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
PROFILES six-leg regression ledger: P0=REGRESSION: PASS (cases=9 passed=9|0 P1=REGRESSION: PASS (cases=9 passed=9|0 P2=REGRESSION: PASS (cases=9 passed=9|0 P3=REGRESSION: FAIL (cases=9 passed=8|1 P4=REGRESSION: SETUP (cases=9 passed=4|2 P5=REGRESSION: SETUP (cases=9 passed=0|2
```

`diff` of the `STATEMENT`/`PROFILES` lines of the two logs yields exactly one changed cell
(six-leg regression ledger / P3) and one changed `observed_deps`:

```
< STATEMENT cap/six-leg regression ledger: ... observed_deps=fleet-root,node DEPS-OK
> STATEMENT cap/six-leg regression ledger: ... observed_deps=fleet-root,jj,node DEPS-OK
```

## 3. Per-statement observation

Tuple = (`picked line` | exit | tool sha256 prefix). sha is identical in all six profiles and both runs.

| statement (tool) | P0 | P1 | P2 | P3 | P4 | P5 | run1 vs run2 | observed deps |
|---|---|---|---|---|---|---|---|---|
| bounded ANSI-C code_view (`tools/tally-audit-v3.py`) | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`\|0\|`da8c1ef4b30c` | same | same | same | same | same | agree | none |
| write-path-census-v2 (`tools/write-path-census-v2.py`) | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`\|0\|`402285329588` | same | same | same | same | same | agree | none |
| write-path census destination resolution (`tools/write-path-census-v3.py`) | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`\|0\|`095924a7a165` | same | same | same | same | same | agree | none |
| staged-id adoption guard (`tools/staged-id-guard.py`) | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`\|0\|`03a796c5726c` | same | same | same | same | same | agree | none |
| six-leg regression ledger (`tools/mutate-and-run.sh`) | `REGRESSION: PASS (cases=9 passed=9`\|0\|`a7d3f2dd7d47` | =P0 | =P0 | run1 =P0; **run2 `FAIL (cases=9 passed=8`\|1** | `SETUP (cases=9 passed=4`\|2 | `SETUP (cases=9 passed=0`\|2 | **disagree in P3** | run1 `fleet-root,node`; run2 `fleet-root,jj,node` |

The four Python selftests are not merely equal by tuple: the whole `obs-*.stdout` file is identical
across all six profiles and both runs — md5 `b17ab489…` (code_view), `15b6c47a…` (v2),
`3aa48b1f…` (v3), `2c067786…` (staged-id), 12 files each.

## 4. Root causes

### 4.1 `fleet-root` — legitimate prerequisite

The ledger replays each recorded case at its pinned blob, materialized from the sibling lane's
repository *inside the fleet root*:

- `measure.py:192-201` (`setup_profile`) builds `$work/<prof>/fleet` as one symlink per sibling lane
  into `/home/vgpnk/Projects/shokunin`, plus a clone of the lane at `$work/<prof>/fleet/tameshi-shokunin`;
  the statement's `cwd` is `mirror`, i.e. that clone.
- `tools/mutate-and-run.sh:1358` `FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")` resolves to
  `$work/<prof>/fleet`; `:1340` `local repo="$FLEET_ROOT/${rel%%/*}"`; `:1204-1216` reads
  `git show <rev>:<path>` out of that repo.
- `measure.py:212` runs P5 as `bwrap --bind / / --dev-bind /dev /dev --bind DECOY /home/vgpnk/Projects/shokunin`,
  so those nine symlinks dangle. `realpath` fails and the repo-identity guard at
  `tools/mutate-and-run.sh:1186-1193` refuses every leg:
  `REGRESSION_CASE <leg>: SETUP (repo_identity_mismatch: …/fleet/<lane> is not its own repository; toplevel=unresolved)`
  ×9 → `REGRESSION: SETUP (cases=9 passed=0 …)` exit 2 (`:1449`).

Both runs, all nine legs, same message. This is the ledger doing exactly its job: it reads pinned
blobs from the other lane repositories. **Declare `fleet-root`.** Note for the row author: the decoy's
`scripts/sources-census.sh` stub is never reached — refusal happens one layer earlier, at repo identity —
so the P5 divergence here proves a *fleet-root read*, not the stub.

### 4.2 `node` — legitimate prerequisite

Five of the nine legs run node suites (`tools/mutate-and-run.sh:1388`, `:1413`, and the three hermetic
`env -i PATH=… node "$MUTANT"` suites at `:1418`, `:1423`, `:1428`). P4 removes `node` from the PATH
shim (`measure.py:176-190`, `drop={'P4': ('node',)}`). Observed in `w1/P4` and `w2/P4`:

```
js-kimi-census,  js-claims-check   : bash: line 1: node: command not found
js-round-gate, js-sources-check, js-cite-check : env: 'node': No such file or directory
-> MUTATE: SETUP (control run on the pristine copy is red (exit=127); …)   # :533
-> REGRESSION_CASE <leg>: SETUP (sweep refused; …)                          # :1265
```

exit 127 = suite not runnable, so the pristine control run is red and the mutator refuses to
attribute kills. Four bash legs still pass → `REGRESSION: SETUP (cases=9 passed=4 …)`, exit 2.
**Declare `node`.**

Near-miss worth recording: P0 resolves `node` through the host PATH (fnm, v24.21.0) while P1-P5 link
`/usr/bin/node` (v26.12.0). The aggregate picked line is identical, so this statement's row proves
"the ledger passes", not "under which node". A future node major that changed one mutation outcome
would surface as `env` only if the aggregate passed-count moved.

### 4.3 `jj` in run 2, P3 — spurious (not a dependence of this statement)

Run 2's P3 cell is the only disagreement between the runs. The failing leg and case:

```
REGRESSION_DEFECT bash-tsukuroi-census B10: measured=KILLED recorded=SURVIVED
REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1; …)
w2/P3/…/bash-tsukuroi-census/sweep.log:95  DEFECT B10: KILLED (exit=1 duration-ms=6044)
w2/P3/…/bash-tsukuroi-census/evidence/B10.out:
  FAIL degraded: journal boot errors at entry level: hostname override not honoured — possible host read
  TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)
```

The mutant B10 (`tsukuroi-census.sh:487-493`, the "PCI inventory unreadable" nvidia branch) is a
recorded *survivor*; the case that killed it is unrelated to the mutation and to `jj`.

Mechanism, in the pinned leg `tsukuroi-census.sh` (rev `165307fe`, sha256 `084951be…`):

- `:638` `set -uo pipefail`
- `:771` `elif ! printf '%s\n' "$out" | grep -q 'host=fixture-host'; then`
- `:773` (verdict) and `:777` (plane regex loop) use the same `printf … | grep -q` shape.

`grep -q` exits on the first match; under CPU pressure the `printf` side can still be scheduled
afterwards, takes SIGPIPE (141), and `pipefail` promotes 141 to the pipeline status — so the `!`
fires **even though the match was found**. Every census run prints the banner
(`tsukuroi-census.sh:945-948`), so the fixture was present: the branch is a pipeline-status artifact,
not a host read. At `:777` the same artifact surfaces as `plane evidence missing …`, which is
indistinguishable from a genuine kill by the sweep's exit-status oracle.

Reproduced (the construct verbatim, `out` 872 bytes — the measured size of every case's census
output — containing the match, 4 × 3000 iterations under 16 CPU spinners):
`iterations=3000 false_branch=6 / 1 / 3 / 1`; zero on an idle host.

`jj` itself is not reachable from anything this statement runs:

- 3 isolated B10 selftests with the P3 shim (no `jj`) and 3 with the P1 shim (`jj` → `~/.local/bin/jj`): all exit 0, `PASS (26 cases, 26 passed)`.
- 12 further concurrent B10 selftests with the P3 shim: 0 FAIL lines.
- Two full ledger replays under the exact P3 environment (same shim, fresh `HOME`/`TMPDIR`, freeze rev, mirror layout identical to the counter's): both `REGRESSION: PASS (cases=9 passed=9 …)` exit 0, tsukuroi `match=10/10`.
- Run 1's P3 cell: PASS.
- No file on the statement's path invokes the `jj` binary: `tools/mutate-and-run.sh` mentions `jj` only in comments/prose; the nine pinned leg blobs mention it only in fixture prose and a `.jj` *directory* test (`mado-verify.sh`), and `tsukuroi-census.sh` mentions it in comments plus the phrase "…no /dev/nvidia* node".

Prior art in the lane: `.ufo/waves/round-18/w2/CR44.md:53` records the same symptom class
("B8 and B10 … killed only by `FAIL blocked: {boot record missing | systemd user bus unreachable}: hostname override not honoured — possible host read`", 17.8-20.6 s against ~6 s, clean on an
immediate re-run) and already inferred "sensitive to load or timing". This seat supplies the mechanism.

**Verdict: accident, not a prerequisite.** The honest row is `deps `fleet-root,node``; `jj` MUST NOT
be declared. The statement cannot shed the accident without re-pinning the tsukuroi leg — outside this
seat's scope and not needed for the dependence question.

### 4.4 `env` and `bwrap` — not observed, and why

- `env` (P0 ≠ P1): no divergence in either run, all five statements. For the ledger the only clock or
  path it prints is `REGRESSION_DATE:` (`:1361`) and the per-leg `REGRESSION_WORKDIR:` paths, neither
  of which the frozen `obs` regex `^(REGRESSION: \w+ \(cases=\d+ passed=\d+)` can select. The four
  Python tools print no path, clock, hostname or user.
- `bwrap`: nothing the statement executes consults it. P2 (shim without `bwrap`) equals P1 for all
  five statements in both runs; `write-path-census-v2.py`, `staged-id-guard.py` and
  `tally-audit-v3.py` contain no `bwrap` token at all, and the ledger's legs never call it.

## 5. The flags the item asked for

- **P1 ≠ P0 only through a printed path or timestamp:** none. No statement's picked line carries a
  path, a temp name or a clock; where the tools do print those (the audit's `mkdtemp` root, the
  ledger's workdir/date lines) the regex does not select them.
- **Timeouts in any profile:** none. Every one of the 60 observations returned a line and an exit
  code; the counter's timeout path (which would print `(timeout)`) never fired. The heaviest cell,
  the ledger, completed in roughly 8 minutes per profile.
- **Command crashed before reaching the tool:** none. The four Python tools printed their verdict
  line 12 times each; the ledger printed `REGRESSION_TOOL`/`REGRESSION_EXPECT` and a final
  `REGRESSION:` line in all 12 cells. In P4 and P5 the *legs* fail before producing a table, which
  is the tool reporting, not the tool crashing (obs sizes 6710 B and 2253 B against 7195 B in P1).

## 6. Rows this observation implies

```
EMIT_CAP | six-leg regression ledger | … | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `fleet-root,node` | …
EMIT_CAP | bounded ANSI-C code_view | … `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none`
EMIT_CAP | write-path-census-v2 | … tool sha256 `402285329588`, deps `none`
EMIT_CAP | write-path census destination resolution | … tool sha256 `095924a7a165`, deps `none`
EMIT_CAP | staged-id adoption guard | … tool sha256 `03a796c5726c`, deps `none`
```

(`--emit` printed exactly these five lines in both runs; only the ledger's deps clause differed,
`fleet-root,node` in run 1 and `fleet-root,jj,node` in run 2.)

## 7. Risk to the deciding run — read before scoring C1

The six-leg regression ledger's `(line, exit)` is **not stable** across identical profile
environments. Its P1/P2/P3 cells can print `REGRESSION: PASS (cases=9 passed=9|0` or
`REGRESSION: FAIL (cases=9 passed=8|1` depending on whether the tsukuroi `pipefail` race fires.
Observed rate here: 1 of the 12 ledger invocations (2 runs × 6 profiles); the failure mode was a
recorded survivor killed by the `:771` artifact.

Consequences for the deciding run:
- a flake in **P0** turns the row into `MISMATCH` → `total>0` → honest miss, through no fault of the row;
- a flake in **P1** makes every other profile differ → all five dependence names appear at once;
- a flake in **P2** or **P3** adds a spurious `bwrap` or `jj`.

Recommendation: take the deciding run on an otherwise idle host, and if the ledger row shows an
isolated `jj`, an isolated `bwrap`, or a lone P0 mismatch, read
`…/regression-wd/bash-tsukuroi-census/evidence/*.out` for the two artifact labels
(`hostname override not honoured — possible host read`, `plane evidence missing`) before treating it
as a real dependence.

Unrelated but noted while root-causing: `tsukuroi-census.sh:630` roots its selftest under a hardcoded
`/tmp/tsukuroi-r3-2-selftest.XXXXXX` (TMPDIR is ignored). Under a full `/tmp` the selftest aborts with
`printf: write error: No space left on device` — I reproduced that class in a private mount namespace
with a size-capped tmpfs. It is *not* what run 2 shows (`B10.out` carries no write error), but it is
the same statement's other environmental soft spot while `/tmp` is under pressure host-wide.

## 8. Receipts

Kept under `/var/tmp/tameshi-r47-T47ExecObsE/` (the `/tmp` trees were deleted after capture, per the
L1's ENOSPC instruction; `/tmp` work dirs were 4.6 GB):

- `receipts/run1.log`, `receipts/run2.log` — the two full probe logs, including every `STATEMENT`,
  `PROFILES` and `EMIT_CAP` line and the two `C1_R47_PARTIAL` verdicts;
- `receipts/w1/P{0..5}/obs-*.stdout`, `receipts/w2/P{0..5}/obs-*.stdout` — all 60 instrument outputs;
- `receipts/p3-replay-a.log`, `receipts/p3-replay-b.log` — the two full ledger replays under the
  exact P3 environment (`REGRESSION: PASS (cases=9 passed=9 …)`, exit 0);
- `b10.sh`, `shim-P3/` (the counter's P3 PATH shim, no `jj`), `race.sh` — the isolation probes and the
  3000-iteration reproduction of the `:771` pipeline artifact.
