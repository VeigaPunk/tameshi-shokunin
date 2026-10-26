# T48CritLoad — H: the ledger FAIL is load-induced (round 48 / w1)

Seat: critic (leaf, no dispatch). Lane: tameshi-shokunin, base `473336d9d789f6081195e7376d17836a24666bc3`
(clone HEAD verified equal before the first run). Read-only on the lane; scratch
`/fast/scratch/hyaku/tameshi-r48/T48CritLoad` (deleted at close). No tool installed or upgraded.

## 0. Verdict

**H is unsupported by the specified test, and not refuted. The test cannot decide H.**

- 0 `REGRESSION: FAIL` lines in 6 runs (3 baseline, 3 with my load generators running). By the item's own
  rule — "no FAIL appears under load in 3 tries" — H is **unsupported, not refuted**.
- The `refuted` branch could not fire either: **no low-load condition existed on this host at any time**
  (minimum 1-min load over all six runs: 39.6 on 32 cores; the experiment opened at 74.50 and never went
  below 39.6). "Nothing else of mine running" was satisfiable; "low load" was not.
- The intended contrast **inverted**: ambient fleet load fell while I added load, so the "baseline" runs
  (means 86.5 / 97.8 / 94.8) ran at *higher* load than the "loaded" runs (64.0 / 43.1 / 44.2).
- The one anomaly that did occur is a **same-mechanism corruption of the same leg**, and it occurred in a
  *baseline* run at the highest minimum load of the six: the byte-pinned `bash-tsukuroi-census` **control**
  run went RED, so the sweep refused and the ledger printed `SETUP`, not `FAIL`.
- The tree is therefore not the variable — but "load" is not the demonstrated cause either: the artifact
  reproduces **with and without my added load** (see §4), because this host is never idle.

## 1. Method and deviations from the item's wording

Runs: `bash <clone>/tools/mutate-and-run.sh --regression --workdir <scratch>/wd/<label>` from the clone,
`TMPDIR` inside scratch, sequential, one at a time, all six against the same tool bytes
(`REGRESSION_TOOL … sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, prefix
`a7d3f2dd7d47` = the pinned prefix of the round-47/48 standing row).

Deviations, disclosed:

1. **Fleet root.** The tool derives `FLEET_ROOT=$(dirname×3 "$SELF")`; in a clone at `<scratch>/lane` that
   resolves to `<scratch>`, which holds no sibling repos. I placed the four read-only sibling repos there
   as symlinks to `/home/vgpnk/Projects/shokunin/{kagi,kumitate,tsukuroi,mado}-shokunin`. The tool's own
   `repo_identity` guard passes through the symlink (`realpath(repo) == realpath(git rev-parse
   --show-toplevel)`), and it only ever `git show`s from them. All nine leg pins were pre-verified to
   resolve and to match their recorded sha256 before the first run.
2. **Four copies, not four clones.** The bound allows one live clone per seat, so the load generators are
   four byte-identical `cp -a` copies of the clone tree (`<scratch>/load/ld{1..4}/lane`), each with its own
   `TMPDIR`.
3. **Looped, not single-shot.** One `python3 tools/env-diff.py --selftest` completes in **0.58 s** (measured
   before the experiment), while one regression run takes 285–525 s. A single-shot copy would be a 0.6 s
   burst inside a 6–9 minute window, i.e. no load at all. Each copy therefore loops `--selftest` for the
   whole loaded phase (`while [ -e active ]`), 9/9 pass on every iteration, no non-zero exits
   (19,500–19,530 output lines per copy).
4. **Harness truncation.** The outer bash job was killed at its 3600 s deadline, but the script had already
   finished (all six `.out`, all six `.load` series, `ps-after-load.txt` present). Verified afterwards:
   zero surviving processes matching my scratch path; the generators were stopped by the script's own kill.

## 2. The table (each first `REGRESSION:` line, exit, wall, load before)

`uptime`/load is `/proc/loadavg`; "mean/min/max" are over that run's 2 s samples of the 1-min field.

| run | phase | load before (1/5/15) | load mean | min | max | wall | exit | first `REGRESSION:` line |
|---|---|---|---|---|---|---|---|---|
| base1 | baseline | 74.50 44.49 23.18 | 86.5 | 74.5 | 106.6 | 461.6 s | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| base2 | baseline | 106.63 83.83 50.23 | 97.8 | 88.9 | 110.8 | 525.5 s | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| base3 | baseline | 93.46 92.23 69.74 | 94.8 | 89.1 | 107.5 | 387.8 s | **2** | **`REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`** |
| load4 | loaded | 87.95 93.02 78.08 | 64.0 | 51.8 | 88.0 | 390.9 s | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| load5 | loaded | 52.28 66.27 71.05 | 43.1 | 39.6 | 52.4 | 285.5 s | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| load6 | loaded | 40.13 50.21 62.92 | 44.2 | 40.1 | 48.0 | 338.8 s | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |

Load generators were visibly running during the loaded phase (top of `ps -eo pcpu` mid-`load4`):
`30.7 python3 (792642) · 30.0 python3 (793129) · 26.6 python3 (792426) · 20.0 python3 (792474)` — the four
`env-diff.py --selftest` loops — against `162 omp` and three browser/bot processes of the fleet. Four
looped copies are ~1 core-equivalents against an ambient 40–110; they cannot move the host.

Per-leg detail, all six runs: 8 of 9 legs `PASS` with `inconclusive=0` every time; the only deviation in
53 of 54 leg cells is base3's `bash-tsukuroi-census`.

## 3. The one anomaly: base3, `bash-tsukuroi-census`, control RED → ledger `SETUP`

```
REGRESSION_CASE bash-tsukuroi-census: SETUP (sweep refused; log: …/wd/base3/bash-tsukuroi-census/sweep.log)
```

`sweep.log` (verbatim, abridged to the verdict block):

```
MUTATE_TARGET: …/target.tsukuroi-census.sh sha256=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5 bytes=44947
CONTROL: RED (exit=1 duration-ms=8880 pristine-sha256=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5)
  | TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)
MUTATE: SETUP (control run on the pristine copy is red (exit=1); cannot attribute kills; log: …/evidence/control.out)
```

`evidence/control.out`, the failing case (verbatim, wrapped):

```
FAIL blocked: both kernel rings unusable: plane evidence missing: 'kernel ring unusable'; got:
PLANE packages: HEALTHY (pacman -Qkk rc=0 sample=4(alpha,beta,gamma,delta) drift=0 backup_diffs=0 nonroot_artifacts=0; foreign=0; pins=none; holds=pacman glibc; db.lck=absent)|
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)|
PLANE drivers: BLOCKED (kernel ring unusable: dmesg rc=1, journalctl -k rc=1)|
PLANE journal: BLOCKED (err stream unreadable: journalctl -b -p err rc=1 [fails closed; no fake pass])|
```

**The expected phrase is in the output that was printed next to the failure** (`PLANE drivers: BLOCKED
(kernel ring unusable: …)`). The assertion that fired is not a content assertion. In the byte-pinned leg
(`tsukuroi-census.sh`, rev `165307fe…`, sha256 `084951be…`, materialized copy verified equal by the tool):

```
 638  set -uo pipefail
 777        printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"
 780        bad "$label: plane evidence missing:$miss; got: $(printf '%s\n' "$out" | grep '^PLANE ' | tr '\n' '|')"
 866  check 'blocked: both kernel rings unusable' 2 BLOCKED 'kernel ring unusable'
```

`grep -q` exits on the first match; the still-scheduled `printf` takes SIGPIPE (141); `pipefail` promotes
141 to the pipeline status; `||` fires although the match was found. Round 47 already root-caused this
shape at `:771`/`:777` (`.ufo/waves/round-47/w1/T47ExecObsE.md` §4.3, "the tsukuroi `pipefail` race") and
round 18 recorded the same symptom class (`.ufo/waves/round-18/w2/CR44.md:53`). My run is the same defect
at the **control** position, which the sweep reports as `SETUP` (rc 2) instead of `FAIL` (rc 1).

Rate in my data: 1 corrupted selftest in 66 invocations (11 per tsukuroi leg × 6 runs) ≈ **1.5 %**.

## 4. Isolated reproduction of the artifact (does my added load matter?)

The construct of `:777` verbatim, on a faithful `out` (574 B: banner + 4 `PLANE` lines + verdict, the
matched phrase on the 3rd `PLANE` line so `printf` still has bytes to write when `grep -q` exits):

```
set -uo pipefail
for ((i=0; i<n; i++)); do miss=''
  printf '%s\n' "$out" | grep -qE -- 'kernel ring unusable' || miss=1
  [ -n "$miss" ] && false_branch=$((false_branch+1)); done
```

| arm | iterations | false branches | rate | added spinners | load during |
|---|---|---|---|---|---|
| A | 2000 | 5 | 0.25 % | 0 | 51.12 |
| B | 2000 | 9 | 0.45 % | 16 | 52.24 |
| C | 2000 | 5 | 0.25 % | 0 | 51.82 |
| D | 2000 | 3 | 0.15 % | 16 | 52.95 |

No dose-response from 16 spinners (A/C without, B/D with: 5,5 vs 9,3). The artifact fires at ~0.2 % per
site **at ambient load ~51 regardless of my contribution**, because the fleet already keeps the host at
1.2–3× oversubscription. This is the honest reading of my own load manipulation: on this host it is not a
manipulable variable, and "load-induced" cannot be separated from "ambient-load-induced" by adding four
processes.

## 5. Why the specified test cannot decide H (power)

With the observed 1.5 % per-invocation rate, a regression run has 11 tsukuroi invocations → P(≥1 firing)
≈ 15 %; of those, 10/11 hit a *mutant* (→ verdict flip → `FAIL`) and 1/11 hits the *control* (→ `SETUP`).
So P(FAIL) ≈ 14 % per run, and **P(no FAIL in 3 loaded runs) ≈ 64 %**. Even at an optimistic 5 % per
invocation the 3-run arm still returns "unsupported" ≈ 22 % of the time. A 3 + 3 design is therefore
almost guaranteed to produce the null the item's rule then reads as "unsupported"; the item's falsifier
has ~36 % power at best, and its "refuted" branch requires a low-load window this host never offers.

## 6. Impacted axes

- **calibration (C1), directly.** The standing row for `six-leg regression ledger` cannot be restated as
  `stable`: my six runs at one tool sha256 (`a7d3f2dd7d47…`) and one revision produced **two** distinct
  `(line, exit)` tuples — `PASS (cases=9 passed=9`, 0 (5×) and `SETUP (cases=9 passed=8`, 2 (1×) — and
  round 47 recorded a third, `FAIL (cases=9 passed=7`, 1. The class is `nondeterministic`.
- **C1 member set, concretely.** The contract's row grammar allows three members; the **`SETUP` member must
  be one of them** (and attested), not just `PASS`/`FAIL`. A row declaring only {PASS, FAIL} misses when a
  deciding run hits the control — a `total>0` through no fault of the row, exactly the round-47 failure
  mode with a different label.
- **C1 deps clause.** `env` is not supported by my data for this statement. All six runs share one profile
  (P0); the divergence is *within* a profile, which the env-diff contract itself classes as nondeterminism
  ("a changed repeated clean tuple is nondeterminism, not attributable environment sensitivity"). The
  round-47 `deps env,fleet-root,node` on the FAIL observation is an artifact of the same accident.
- **freshness (C2)**: untouched — nothing here reads SOURCES.md, the Gate lines, the entries or snapshots.
- **depth**: untouched (no case added or removed; `REGRESSION_EXPECT` printed the same nine recorded rates
  in all six runs).
- **Provenance gap, noted for the record.** No raw receipt of the round-47 `FAIL (cases=9 passed=7` /
  `FAIL (cases=9 passed=8` observations is committed anywhere in `.ufo/`; the only committed traces are the
  *restated* claim (`.ufo/evidence/round-47/after/c1.stdout:5`, `SCORECARD.md:2270`) and the round-47 seat's
  prose plus its uncommitted `/var/tmp` receipts. A standing row restating a flake has no byte-pinned
  observation behind it — that is the defect round-48 C1 is meant to close, and it is still open for this
  statement unless a receipt is committed.

## 7. Smallest safe correction

1. **Do not** restate the ledger row as `stable`, and do not restate `FAIL` as the value. Declare
   `nondeterministic` with the three attested members above and deps `fleet-root,node`.
2. If the L1 wants a stable value instead, the only honest route is to repair the leg (drop `pipefail`
   dependence from the selftest's assertions, e.g. `case "$out" in *"$re"*) …` at `:771`/`:773`/`:777`, or
   `set +o pipefail` inside the selftest). That re-pins the leg and moves its recorded table — outside this
   seat's scope, and it must not be done silently.
3. For the deciding run: before scoring a mismatch on this statement, read
   `…/regression-wd/bash-tsukuroi-census/evidence/control.out` and `…/sweep.log`. The artifact's signature
   is a `plane evidence missing: '<phrase>'` or `hostname override not honoured — possible host read` whose
   `got:` string **contains the phrase** — a false assertion, not a defect of the tree.

## 8. Limits of this report

- One host, one hour, one revision, one tool sha; the rate estimate rests on a single event (1/66; 95 % CI
  roughly 0.04 %–8 %). The direction of the conclusion (the leg is nondeterministic; the tree is not the
  variable) does not depend on that interval.
- "Baseline" here means "no load generator of mine", not "idle host". No idle-host measurement exists in
  this report and none was possible.
- The scratch tree and all raw logs were deleted at close; the excerpts above are the cited receipts.
