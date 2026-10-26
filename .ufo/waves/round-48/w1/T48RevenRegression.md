# T48RevenRegression — root cause: `--regression` ledger flake (`passed=9` ↔ `passed=8`)

Seat: T48RevenRegression (round 48, w1, calibration axis / C1 feed). Read-only on the lane; one
scratch root `/fast/scratch/hyaku/tameshi-r48/T48RevenRegression` (deleted before exit). Lane base
`473336d9d789f6081195e7376d17836a24666bc3`. Tool under study `tools/mutate-and-run.sh`, pin
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (prefix `a7d3f2dd7d47`, the same
pin the round-47 rows carry — the flake is not a tool-revision artifact). Two replays of the real
command were made, the item's full budget; no tool was edited, no install was needed.

One structural note first, because it shapes the method: `run_regression` derives the fleet root from
its own path — `FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")`
(`tools/mutate-and-run.sh:1358`) — so a copy of the tool in a scratch clone resolves
`FLEET_ROOT=<scratch>` and every leg refuses at the repo-identity guard
(`repo_identity_mismatch`, `:1186-1193`; precedent receipt
`.ufo/waves/round-21/w1/depth/regression-attempt1-setup.out`, `SETUP (cases=8 passed=0 cannot-verify=8)`).
The faithful way to exercise it is the lane's own tool with `--workdir` in scratch, which writes only
the workdir. That is what the two replays below do.

## 1. Verdict (short)

1. **One mechanism, in the pinned leg bytes, not in the runner.** The tsukuroi leg's selftest sets
   `set -uo pipefail` (`tsukuroi-census.sh:638`, pinned blob `084951be50bc…` @ `165307fe`) and then
   tests each case with piped `printf | grep -q` (`:771` banner, `:773` verdict, `:777` plane
   regexes). `grep -q` exits as soon as it matches; when the `printf` side is scheduled late it takes
   SIGPIPE on its write, `pipefail` promotes 141 to the pipeline status, and the `!` / `||` turns a
   *found* match into “not found”. The case is then recorded `FAIL … hostname override not honoured —
   possible host read` (or `plane evidence missing: …`), the suite exits 1, the mutant is scored
   `KILLED`, and the ledger's exact expectation (`ktol=0 ftol=0`, `:1342`) fails the whole leg:
   `REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1)` →
   `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` (`:1328`, `:1442`).
2. **It is one-sided.** In 12 000 instrumented repetitions of the exact construct, every false branch
   had `grep` exit **0** and `printf` exit **141**: the race can only turn a green case red. The
   ledger's PASS is therefore trustworthy; its FAIL is the unreliable value.
3. **Exactly one leg is materially exposed:** `bash-tsukuroi-census` (4 piped `grep -q` sites, ~78
   pipeline invocations per suite run). `bash-surface-census` carries the same class at a single site
   (`surface-census.sh:681`, under `set -euo pipefail` at `:73`) — ~78× less exposure, 0/40 observed.
   The other seven legs are immune by construction (§4).
4. **Reproduced end to end, in host env:** replay A `PASS (cases=9 passed=9)` exit 0, 449 s, load
   70→87; replay B `FAIL (cases=9 passed=8 failed=1 setup=0)` exit 1, 233 s, load 32→36, with
   `REGRESSION_DEFECT bash-tsukuroi-census B7: measured=KILLED recorded=SURVIVED` and evidence line
   `FAIL blocked: pacman db.lck: hostname override not honoured — possible host read`. Independently,
   the pinned blob's own selftest failed **4 of 40** runs (10 %) at 6-way concurrency with the same
   two messages as the round-47 receipt (`.ufo/waves/round-47/w1/T47ExecObsE.md:151-152`).
5. **Class verdict: `nondeterministic` is honest**, with members
   `{REGRESSION: PASS (cases=9 passed=9 | exit 0, REGRESSION: FAIL (cases=9 passed=8 | exit 1}`.
   A third asserted member, `FAIL (cases=9 passed=7 | exit 1`, has **no organic receipt anywhere in
   the lane** (§5); it must not be declared unless a run prints it.
6. **The instability cannot be removed without editing the tool** (§6). The jitter lives in a fleet
   file the runner reads by pin; `--timeout`, `--workdir`, `--keep`, `--tail` do not reach it, and the
   exact tolerance is precisely what converts one spurious case into a leg FAIL. Tool-free
   mitigations (idle host, `jobs=1` counter, roomier `TMPDIR`) only lower the probability.

## 2. The two replays (the item's whole run budget)

```bash
S=/fast/scratch/hyaku/tameshi-r48/T48RevenRegression; export TMPDIR=$S
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  --regression --workdir "$S/wd1"   # replay A
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  --regression --workdir "$S/wd2"   # replay B
```

| replay | start (UTC) | load (start → end) | wall | tally line | exit |
|---|---|---|---|---|---|
| A | 08:43:53 | 70.42 → 87.35 | 449 s | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` | 0 |
| B | 09:45:15 | 32.14 → 36.44 | 233 s | `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` | 1 |

Replay B, tsukuroi block verbatim (`runB.out`):

```
REGRESSION_PIN bash-tsukuroi-census: source=git repo=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev=165307fe4746a8807b02ec4a7d7ecac0368454a6 path=tools/tsukuroi-census.sh mode=100755 sha256=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5
REGRESSION_SWEEP bash-tsukuroi-census: MUTATE: DONE (target=bash-tsukuroi-census defects=10 killed=7 survived=3 inconclusive=0 kill-rate=70%)
REGRESSION_DEFECT bash-tsukuroi-census B7: measured=KILLED recorded=SURVIVED
REGRESSION_TABLE bash-tsukuroi-census: match=9/10 recorded-killed=6 measured-killed=7 survived=3 inconclusive=0 flips=1
REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1; …)
```

`wd2/bash-tsukuroi-census/sweep.log`: `CONTROL: GREEN (exit=0 duration-ms=3005 …)`, `DEFECT B7:
KILLED (exit=1 duration-ms=5215)`, `MUTATE_RESTORE: OK`. `evidence/B7.out` — 25 `PASS …` lines, one
`FAIL`:

```
FAIL blocked: pacman db.lck: hostname override not honoured — possible host read
TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)
```

B7's recorded verdict is SURVIVED (`@old SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}` → `-9`), and the case that
failed is unrelated to the mutation text: the mutant is *green* and was scored red. The control run in
the same leg was green, so the leg failed only through the mutant path — the flip face of the class.

Per-leg suite cost in replay A (from `results.tsv` / `sweep.log` durations), for the timeout question:

| leg | suite runs | control ms | mutants ms | total ms |
|---|---|---|---|---|
| js-round-gate | 11 | 11 204 | 108 344 | 119 548 |
| bash-tsukuroi-census | 11 | 8 482 | 84 788 | 93 270 |
| bash-checklist-run | 16 | 5 154 | 86 331 | 91 485 |
| bash-surface-census | 11 | 4 441 | 56 020 | 60 461 |
| js-sources-check / js-kimi-census / js-claims-check / bash-mado-verify / js-cite-check | 11 | 1 708 / 1 577 / 1 627 / 1 819 / 417 | ~16–17 k / 16 k / 18 k | ≤ 19 128 |

Slowest *single* suite run in either replay: 11.2 s (js-round-gate control) against the runner's
`timeout "$TIMEOUT_S"` at `:456` with `TIMEOUT_S=300` (`:186`) — a 27× margin at load 87.

## 3. Mechanism, with path:line

1. `tsukuroi-census.sh:638` `set -uo pipefail` (selftest entry). Its `check()` runs the census into a
   variable and then asserts on it with pipelines:
   `:771 elif ! printf '%s\n' "$out" | grep -q 'host=fixture-host'; then` →
   `bad "$label: hostname override not honoured — possible host read"`;
   `:773` the same shape for the verdict line; `:777`
   `printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"` → `bad "$label: plane evidence
   missing:$miss"`. A fourth site, `:286`, sits in the body and only mis-classifies a probe.
2. `pipefail` makes the pipeline status `141` when the *writer* dies of SIGPIPE even though `grep`
   found the match and exited 0. Nothing in the runner suppresses this: `SHELLOPTS` is **not**
   inherited by the files the runner executes (measured: a child of a `set -o pipefail` shell reports
   `SHELLOPTS=[braceexpand:hashall:interactive-comments]` and `set -o | grep pipefail` → `off`), so
   the exposure of each leg is exactly what its own bytes set.
3. One failing case makes the suite exit 1 (`run_selftest` prints `TSUKUROI_CENSUS_SELFTEST: FAIL …`
   and returns non-zero). The sweep maps any exit other than 0/124/126/127 to `KILLED`
   (`tools/mutate-and-run.sh:546-550`), so a recorded *survivor* becomes `KILLED`.
4. `regression_case` compares against the recorded table with `ftol=ktol=0` for ledger legs
   (`:1342`, reasons at `:1312-1313`), so `flips=1 killed-delta=1` is out of band (`:1328`) and the
   run prints the FAIL tally (`:1442`).
5. Rate, measured here: instrumented construct, 12 000 repetitions → false branches 9/12 000 with
   `it status` 141 every time and `grep` status 0 every time (0.075 % per pipeline invocation at load
   ~70-87); pinned blob selftest standalone, 60 runs at 4-6-way concurrency → 4 failures (6.7 %,
   4/40 of the second batch, 0/20 of the first); ledger level → 1 FAIL in 2 replays (mine), 1 in the
   round-47 receipts (`.ufo/waves/round-47/w1/T47ExecObsE.md:151`), 0 in the committed replays of
   rounds 7-46. Prior art in the lane already recorded the symptom class without the cause:
   `.ufo/waves/round-18/w2/CR44.md:52-53` (“killed only by `FAIL blocked: {boot record missing …}:
   hostname override not honoured`”, 17.8-20.6 s against ~6 s, clean on immediate re-run).

## 4. Which legs can flip, and what is ruled out

| leg | piped `grep -q`? | own `pipefail`? | verdict |
|---|---|---|---|
| bash-tsukuroi-census | yes, 4 (`:286,771,773,777`) | yes (`:139,638`) | **the observed flake** |
| bash-surface-census | yes, 1 (`:681`) | yes (`:73`) | same class, ~78× less exposure; 0/40 runs failed |
| bash-mado-verify | 0 pipes (all grep calls read files; `:770` pipes into `grep -q` but **no** `pipefail`) | no | immune |
| bash-checklist-run | 0 pipes (herestrings `<<<"$out"`, `:274,420`) | yes (`:62`) | immune |
| js-kimi-census, js-claims-check, js-round-gate, js-sources-check, js-cite-check | no shell pipelines | n/a | immune to this class |

Ruled out by measurement, not by assumption:

- **Per-suite timeout under load.** Max single suite run 11.2 s vs `TIMEOUT_S=300` (`:456/:186`); the
  whole replay 233-449 s vs the frozen statement's `timeout: 2700`
  (`.ufo/evidence/round-47/calibration/statements.json`). Even at the counter's `jobs=14` this has
  ~6× headroom. `inconclusive>0` never fired in either replay.
- **Parallelism / ordering / shared state inside the runner.** `run_regression` runs the nine legs
  sequentially (`:1370-1430`); each leg owns `$root/<leg>` and its sweep rewrites
  `results.tsv`/`sweep.log`/`evidence/*` with `>`-truncation, so a reused `--workdir`
  (the counter passes one: `statements.json` argv `--workdir {work}/regression-wd`) cannot feed a
  stale table into a later run. `match=10/10` in eleven legs across the two replays is consistent.
- **Temp dirs / `/tmp` pressure.** Default root is `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`
  (`:1360`) and is kept on FAIL/SETUP (`:1466` is the PASS arm), but one root is ~7.0 MB (`du -sh`
  of `wd1`), so the failure mode of a full `/tmp` is a SETUP (mktemp/cp refusal), never a FAIL, and
  neither replay came near it. The /tmp pressure note in round 47 (`.ufo/waves/round-47/w1/T47ExecObsB.md:113`)
  is a different statement's mechanism.
- **Network, clock.** No leg dials out; the only clock read is `REGRESSION_DATE` (`:1394`), which the
  frozen obs regex `^(REGRESSION: \w+ \(cases=\d+ passed=\d+)` cannot select.
- **node / jj / bwrap.** node is a prerequisite of five legs (absent → `127` → INCONCLUSIVE → SETUP),
  jj is reachable from nothing the legs execute (only the counter's P3 shim removes it), and no leg
  invokes bwrap. None of the three appears in the failing path of replay B.
- **Git object store / fleet repo state.** `git show <rev>:<path>` reads pinned blobs (`:1204-1216`);
  a missing repo/rev/blob or a pin mismatch is a SETUP, never a FAIL. Both replays printed all nine
  pins at the recorded sha256.

## 5. Provenance of the round-47 `passed=7` value — not an observation

SCORECARD.md:2314 (disclosed limit) states the ledger “printed `FAIL (cases=9 passed=7` once under
P0”, and the landed round-47 row restates exactly that (SCORECARD.md:2270). No committed receipt
supports it:

- the line has no organic occurrence in `.ufo` evidence — the only `REGRESSION: FAIL … passed=7`
  line in any real-invocation receipt is `.ufo/evidence/round-18/coldread/traces/CR18/6.out.txt`,
  which is a **doctored-table control** (`rg-doctored`, `js-kimi-census D1: measured=KILLED
  recorded=SURVIVED`) on a `cases=8` run, not the live tree;
- the string exists verbatim in the tool's own selftest tally vector,
  `tools/mutate-and-run.sh:2024` `'1 1 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)'`,
  and in `.ufo/waves/round-30/wA/MutateTallyExtra.md`; the counter's obs regex truncates at
  `passed=\d+`, so that literal and an observation are textually identical;
- `.ufo/waves/round-47/w1/T47ConnCross.md:150-152` drew the same conclusion (a fixture string, not a
  measurement) — this seat confirms it independently and adds the second half: the *organic* FAIL
  receipt the round-47 record lacked is `passed=8`, not `passed=7` (replay B above;
  `T47ExecObsE.md:151` for the round-47 P3 instance).

Consequence for C1: `passed=7` is **unattested** and must not be declared as a member. If a round-48
observation prints it, the class becomes three-member (still inside the contract's 2-3 member
`nondeterministic`), and only then.

## 6. Class verdict and removability

**`nondeterministic` is the honest class for this statement on this host**, with
`V = {PASS (cases=9 passed=9, exit 0), FAIL (cases=9 passed=8, exit 1)}`:

| outcome | exit | organic receipt | status |
|---|---|---|---|
| `REGRESSION: PASS (cases=9 passed=9` | 0 | replay A; rounds 7-46 receipts | attested |
| `REGRESSION: FAIL (cases=9 passed=8` | 1 | **replay B**; `T47ExecObsE.md:151` (P3) | attested |
| `REGRESSION: FAIL (cases=9 passed=7` | 1 | none (fixture vector, §5) | **not attested** |
| `REGRESSION: SETUP (cases=9 passed=4` / `0` | 2 | round-47 P4/P5 cells | profile-deterministic, not jitter |

The same class also has a SETUP face that has not been observed organically: a spurious case failure
in the **control** run makes the pristine red, and the sweep then refuses (`:533` → `:1265`) → leg
SETUP. That is mechanical (`check()` is the same code path for control and mutants), so a P0 receipt
printing `SETUP (cases=9 passed=8` would not be an anomaly — it would be the same root cause.

**Not removable without editing the tool.** The jitter is in `tsukuroi-census.sh:771/773/777` at pin
`165307fe`/`084951be50bc…`, a fleet blob the runner materializes read-only from `git show`; the
runner's knobs (`--timeout`, `--workdir`, `--keep`, `--tail`, `BAND_*` which is bypassed for ledger
legs) do not touch it, no environment variable can suppress SIGPIPE inside the leg's own shell, and
the exact tolerance (`:1342`) is what turns one spurious case red into a FAIL. Removing it means
either re-pinning the leg (editing `PIN_TSUKUROI`/`REV_TSUKUROI`) or editing the fleet gate — both
out of scope and both changes to the object under measurement. What a caller *can* do without
editing anything is lower the probability (idle host, single-job counter, `TMPDIR` on a roomy
filesystem so the SETUP face cannot piggyback), and what the C1 row must do is declare the class
rather than a single value.

## 7. Confidence and limits

- `[O]` Observed: both replays and their tally lines; the B7 evidence line; 4/40 standalone selftest
  failures of the pinned blob with the two receipted messages; 12 000-invocation construct probe with
  `grep=0 / printf=141` in every false branch; `SHELLOPTS` non-inheritance; per-leg durations;
  the exposure scan of all five bash legs; absence of an organic `passed=7` receipt.
- `[I]` Inferred: that replay B transfers to the counter's P0 cell. My replays ran with
  `cwd=$S` (not the counter's mirror clone), `TMPDIR=/fast/…` (not `/tmp`) and `FLEET_ROOT` = the live
  fleet (the counter symlinks the same directories under `$work/P0/fleet`); the race is
  CPU-scheduling driven and independent of those three, and P0 is otherwise the host environment,
  which is what my replays used. Also `[I]`: a second failing leg in one run (`passed=7`) would have
  to be `bash-surface-census` — the only other leg carrying the class — at ~1 % of the tsukuroi
  exposure.
- `[I]` The load average is contention-shaped, not monotone: the FAIL happened at load 32-36 and the
  PASS at 70-87. Do not read the tally as a function of `/proc/loadavg`.
- Compliance: lane checkout untouched (only this report written); the tool was never edited; every
  clone/temp lived under `/fast/scratch/hyaku/tameshi-r48/T48RevenRegression` and the tree was
  removed; no package or tool installs were made, so the tooling ledger for this seat is empty.
