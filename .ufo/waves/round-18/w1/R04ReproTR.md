# R04ReproTR — falsification attempt: C2 before-state for P05–P07 (trace-inputs survived mutants)

Seat: TameshiR18.R04ReproTR · Rev: 183f87b899e6cae46be98d251cbc87fb5118f6ca · 2026-10-20

## Axes

- **Depth:** faithful one-shot reproduction of the three SURVIVED mutants from round 17 (`.ufo/waves/round-17/w2/MutateTraceInputs.md`) against the round-17 coldread collector at the round-18 lane tip.
- **Calibration:** pristine control run; mutated-byte hash equality against round-17's recorded mutant hashes; count==1 uniqueness of each mutation site.
- **Operability (monitor only):** no tool installs; Python 3.14.8 / git 2.56.0 / strace as found on host.

## Setup

Fleet-mirror clones in `/tmp/tameshi-r18w1-R04ReproTR-E53bhZ` (siblings symlinked, clone detached at `183f87b8`), four independent clones: `pristine`, `m01`, `m03`, `m04`. All `GIT_*` scrubbed from each detector invocation (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`), `TMPDIR=$W`, cwd inside each clone. No lane writes; no git/jj writes outside /tmp clones.

- Target file per contract A resolution: `git ls-tree 183f87b8` lists `tools/trace-inputs.py` as **not tracked** at this rev; collector = `.ufo/evidence/round-17/coldread/trace-inputs.py` (mode 100755, blob `ae8310de`).
- Pristine sha256 at 183f87b: `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070` — identical in all four clones and equal to round-17's `H0` (MutateTraceInputs.md), so instrument bytes are unchanged since the round-17 mutation landing `eb7838b`.

## Mutants applied (each site unique, count==1 verified by grep before edit)

| Probe | Round-17 mutant | Site (path:line at rev) | Change |
|---|---|---|---|
| P05 | M01 | `.ufo/evidence/round-17/coldread/trace-inputs.py:82` | delete `RDWR\|` from `WRITE_FLAGS_RE` |
| P06 | M03 | `trace-inputs.py:516` | `env["PYTHONPYCACHEPREFIX"] = cache` → `= "."` |
| P07 | M04 | `trace-inputs.py:644` | drop `or tracer.first_pid not in tracer.exec_ok` |

## Results — `python3 trace-inputs.py --selftest` (exit / tally / stderr bytes)

| Run | Exit | Tally | stderr | sha256 after |
|---|---|---|---|---|
| Pristine | 0 | `SELFTEST: 27/27` | 0 | `521be955…` (H0) |
| P05 = M01 mutated | **0** | `SELFTEST: 27/27` | 0 | `12194d0e323d748bd42aed675d6a27013fb13e691b408f8beb7eb48fdf0b5125` |
| P06 = M03 mutated | **0** | `SELFTEST: 27/27` | 0 | `686a0fcd18313188e7df9822ac403f2f650993e56761ff8777f6065f907009f7` |
| P07 = M04 mutated | **0** | `SELFTEST: 27/27` | 0 | `25fa1839663ad919b9e5d24030f5901a0b96af0f22d12d2c4316c71b4de62897` |

All 27 named checks PASS in every run (including `write-open-excluded`, `env-scrubbed`, `missing-command-exit2` under their mutants). All stderr empty; no timeouts (≈1.4 s per run).

## Findings

1. **C2 before-state for P05–P07 holds at 183f87b; not falsified.** All three survived mutants survive again: selftest exits 0 with `27/27` while the guarded behavior is deleted — detector gap, not production failure (per round-17 framing; contract A defines `open` = mutant survives selftest).
2. **Mutant application is byte-exact vs round 17:** each mutated sha256 equals the round-17 kill-table hash for M01/M03/M04, so this reproduction ran the identical mutants — no drift in the probes or the instrument between `eb7838b` and `183f87b`.
3. **Pristine control healthy:** 27/27, exit 0, empty stderr at H0 bytes.

Residual risk: `--selftest` survival is exactly what P05–P07 measure; no behavioral witnesses (M01 O_RDWR receipt / M03 prefix receipt) were re-run — the round-17 report already carries them and contract A does not require them for `open`. Fix location for the C2 after-state: contract B's promoted `tools/trace-inputs.py` must add selftest cases that fail on exactly these three mutants.

## Verdict

Holds — P05/P06/P07 before-state reproduced open (mutant survives, 27/27 exit 0) with byte-exact round-17 mutants and pristine 27/27 at 183f87b899e6cae46be98d251cbc87fb5118f6ca.
