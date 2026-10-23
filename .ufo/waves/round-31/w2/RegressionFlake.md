# RegressionFlake — B7 `measured=KILLED` at c111dab5

Seat: `RegressionFlake`. Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/RegressionFlake/` (fleet mirror
`fleet/`, sibling `tsukuroi-shokunin` symlinked read-only). Nothing outside this report and that
scratch dir was written; no production file, Git write command or `jj` command was run.

## Verdict

**Not a B7 property, not a timeout, not a parallel test.** The single observed
`REGRESSION_DEFECT bash-tsukuroi-census B7: measured=KILLED recorded=SURVIVED` is a
**scheduling race in the pinned suite's own case checker**, and it is load-sensitive:

1. Every case check ends with `printf '%s\n' "$out" | grep -q …`
   (`tsukuroi-census.sh@165307fe:771,773,777`). Bash's builtin `printf` emits **one `write()`
   per line** (measured, 6 writes for a 6-line `$out`, the first being the 82-byte header line
   that carries the eager match).
2. `grep -q` exits at the first matching line. If the writer subshell is preempted before its
   next write, that write takes `EPIPE`/`SIGPIPE` and the subshell dies with status 141.
3. The script runs under `set -euo pipefail` (`:139`), so `pipefail` reports **141** as the
   pipeline status; the leading `!` in `elif ! printf … | grep -q …` turns that into a
   spurious `bad()` — *"plane evidence missing"* while the evidence is present in the same
   `$out` (reproduced, below). One `bad()` makes `run_selftest` exit 1 (`:915-917`).
4. The sweep classifies any suite exit outside `{0,124,126,127}` as `KILLED`
   (`tools/mutate-and-run.sh:36,546-550`), so the flake is recorded as a kill of whichever
   defect happened to be running. Under the ledger's exact band (`killed-delta<=0 flips<=0`,
   `:1396-1399` + `regression_case_git … 0 0`) that single flip fails the whole case.

B7's mutation is **behaviourally inert** on this suite, so B7 is a victim, not a cause: the
byte-diff against the pristine copy is line 160 only, and `SAMPLE_N` is consumed solely as the
`head -n` bound over a 4-package fixture, so caps 8 and 9 cannot differ.

## 1. Pin and mutation are exactly the recorded ones

```sh
R=/fast/scratch/hyaku/tameshi-r31-seats/RegressionFlake
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $R/fleet/tsukuroi-shokunin \
  show 165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh > $R/src/tsukuroi-census.sh
sha256sum $R/src/tsukuroi-census.sh
```

Observed: `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` — equal to
`PIN_TSUKUROI` (`tools/mutate-and-run.sh:609-610`), 976 lines.

B7 spec is the embedded one verbatim (`.ufo` runner lines 772-775):

```
@defect B7 | tsukuroi-census.sh:160
@old SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
@new SAMPLE_N=${TSUKUROI_SAMPLE_N:-9}
```

Mutant vs pristine, produced by the runner itself:

```sh
diff $R/src/tsukuroi-census.sh $R/rg-b7/1/wd/mutant-B7.target.sh
```

```
160c160
< SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
---
> SAMPLE_N=${TSUKUROI_SAMPLE_N:-9}
```

The only consumer is the sample bound (`:270`), against a fixture whose package list is four
names (`:699`: `alpha beta gamma delta`); `sample_n=4` either way, so no case output can move.

## 2. Twenty isolated replays: B7 always survives, control always green

```sh
bash $R/fleet/tameshi-shokunin/tools/mutate-and-run.sh --target <copy of the pinned blob> \
  --defects $R/b7.spec --suite 'bash "$MUTANT" --selftest' \
  --workdir $R/rg-b7/<k>/wd --label B7-loop --timeout 200 --tail 40
```

Twenty consecutive iterations, verbatim shape of every row (`$R/b7loop.log`):

```
iter=8 sweep_rc=0 DEFECT B7: SURVIVED (exit=0 duration-ms=2549) tsukuroi-census.sh:160
  ctl=(CONTROL: GREEN (exit=0 duration-ms=2452 pristine-sha256=084951be…c78c5)) fails=()
```

`20/20 SURVIVED`, `fails=()` in every run (`LOOP_DONE` closes the log). A second look, unpinned,
24 concurrent full selftests, then a `strace -f -e trace=write` run of the whole suite: `26/26
PASS` each time.

## 3. The race, measured at the exact construct

Write granularity of the pipeline's producer (`strace` of the pinned text, `sp-1.log`):

```
write(1, "tsukuroi-census v3.2 … host=fixture-host …", 82) = 82
write(1, "PLANE packages: HEALTHY (pacman …", 176) = 176
write(1, "PLANE systemd: …", 122) = 122
write(1, "PLANE drivers: …", 161) = 161
write(1, "PLANE journal: …", 199) = 199
write(1, "TSUKUROI_CENSUS: HEALTHY …", 92) = 92
```

Six writes, not one — the first write already contains the `host=fixture-host` match, so
`grep -q` can exit while five writes are still pending.

Pipeline status histogram under `set -euo pipefail` (8 processes pinned to core 0,
`bench2.sh`, 1,500 iterations each):

```
rc=0 total=11996
rc=141 total=4
```

Conversely (8 pinned processes × 2,000, `bench.sh`): `iters=16000 failures=5`, and with
`pipefail` **off**, same text, same contention, same 16,000 iterations: `failures=0`.
The kill is `pipefail`-attributable `SIGPIPE`, not a grep miss (`grep` never returns 1 here:
the pattern is present; the histogram has no rc=1 at all).

Load dependence, same construct, one core per process (no preemption):

```
16 processes unpinned, 4,000 iterations each -> total_failures=0   (64,000 pipelines)
```

## 4. Reproduced end-to-end at suite level (the mechanism that produced the receipt)

Instrumented copy of the same bytes (`probe.sh` = pinned blob + repeat counters around the
`:771` pipeline; the real case check is untouched), 8 instances pinned to core 0,
`PROBE_REP=300`:

```
grep -c PROBE141 insitu/p*.log   -> 2 1 3 0 2 2 2 1   (13 failures / 62,400 repeats ≈ 2.1e-4)
cat insitu/p*.rc                 -> 0 0 0 0 0 0 0 1
```

Instance 8 turned the pinned suite itself red, as a **false negative**:

```
FAIL healthy: unrestricted dmesg ring preferred: plane evidence missing: 'ring=dmesg .*kerr=0';
got: PLANE packages: HEALTHY (…)|PLANE systemd: HEALTHY (…)|PLANE drivers: HEALTHY
(ring=dmesg dmesg_restrict=1 kerr=0 (oom=0 io=0 gpu=0 other=0); …)|PLANE journal: HEALTHY (…)
TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)
```

The required pattern is visibly present in the same `$out`; only the producer's SIGPIPE can
make that pipeline non-zero. This is exactly the shape that becomes `DEFECT B7: KILLED` when
the sweep runs the mutant.

Contention level explains the rarity: 192 unpinned suite runs (20 B7 iterations ×
control+mutant, 24-, 40-, 48- and 40-way waves) produced 0 red suites; 1 in 8 suites went red
only under 8-way single-core contention.

## 5. Ruled out

- **Timeout**: `timeout "$TIMEOUT_S"` yields 124 → `INCONCLUSIVE` with `note=timeout`
  (`tools/mutate-and-run.sh:547`), and the receipt reports `inconclusive=0`.
- **Mutation causality**: the edit is unreachable on a 4-package fixture (§1), and the same
  flake class reproduces on the pristine bytes (§4), so no mutant is required.
- **Parallel tests / shared workdir**: the nine legs run sequentially and each case owns
  `$WORKDIR/<case>`; the ledger's only cross-process reads are `git show` from the repo object
  store. The flake fires inside one suite process, with no second writer.

## 6. Smallest safe correction (and where it belongs)

Root fix, in the suite — `tsukuroi-shokunin/tools/tsukuroi-census.sh` (a sibling repo, not
tameshi): drop the producer process from the match, e.g.
`grep -q 'host=fixture-host' <<<"$out"` (and the same for the `-qE` sites). Three sites at the
pin (`:771`, `:773`, `:777`); the construct still exists at the live HEAD
`b40c01df` (`:2000`, `:2006`, `:2017`, `:2048`), so the fix belongs upstream regardless.

Ledger side, in `tools/mutate-and-run.sh`: the leg replays a **byte-pinned** blob
(`PIN_TSUKUROI`/`REV_TSUKUROI`, `:609-610`; exact band, `:1396-1399`), so a tameshi edit cannot
reach the race. Two honest options, in order of preference:

1. Re-cut the leg's pin to a tsukuroi revision carrying the here-string fix, re-measuring the
   recorded table (`TABLE_TSUKUROI`, `:625`) and every note/SCORECARD row that quotes `6/10`
   (e.g. `corpus/knowledge/mutation-case-tsukuroi-census.md`).
2. If the pin must stay: on a flipped row only, re-run that one defect once and count the flip
   only if it reproduces; log both verdicts (`DEFECT B7: SURVIVED (flake confirmed)`). A genuine
   kill reproduces, so the exact expectation is not weakened; cost is one suite run per flip.

Do **not** relax the recorded expectation or the exact band: B7's recorded `SURVIVED` is correct
and stays correct; the observation was wrong.

## 7. Risks, blockers, limits

- The original failing `sweep.log` is in the observing seat's scratch (off-limits), so the
  flake's own FAIL label is not recoverable; the reproduction here is on bytes with sha256
  equal to the recorded pin, with instrumentation confined to the repeat counters (the real
  case check is byte-identical).
- The measured in-situ rate (≈2.1e-4 per early-match pipeline; a suite run has ≈57 such
  pipelines) predicts a red suite in the low-percent range **under contention** — consistent
  with one flake per fleet regression batch, and consistent with round-18 CR20's independent
  `B9` flake in the same leg. A single `--regression` PASS is therefore not deterministic
  evidence for any SURVIVED row in this leg while the pin carries the race.
- No tool was installed or upgraded. No process started by this seat survives (checked:
  no `/proc/*/cwd` inside the scratch dir).
