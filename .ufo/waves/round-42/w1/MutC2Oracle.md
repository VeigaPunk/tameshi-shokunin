# Round-42 wave-1 — C2 oracle mutants (L1Tameshi42.MutC2Oracle)

Scope: three single-point mutants of the C2 counter
`.ufo/evidence/round-42/census/measure.py` (copy at
`/tmp/tameshi-r42-MutC2Oracle-/m.py`, sha256
`3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2`, 19650 bytes),
probed against the lane at `322b5cd32b4319a05340d249ae752d12a9e6b19f`
(freeze == rev). No deciding run was performed; every run below is a
`--probe-mutant` CONTROL run (exit 0, `C2_R42_CONTROL` line).

## Findings

All three mutants are **killed (distinguished by the bounded probe)**: each
flips the oracle's verdict on a concrete tool file versus the pristine counter,
so each is a real, measurable mis-score. The mis-scores:

1. **M1 — count non-zero exit as killed** (`m1.py:314`, oracle: `return
   'killed', errors[0]` instead of `'runtime_error'`). Concrete tool:
   `T_crash.py` — emits the frozen-correct JSON for every fixture/live target,
   then `sys.exit(1)` (models a real v4 that crashes after computing, e.g. an
   unhandled post-processing exception). Pristine counter reports
   `runtime_error`; M1 reports `killed`. PIT/Stryker classify a non-zero exit
   as Run error / RuntimeError, not a kill — M1 would over-count kills.
   - pristine: `PROBE outcome=runtime_error detail=F01_attr_scratch exit=1 ['boom']`
   - M1:     `PROBE outcome=killed detail=F01_attr_scratch exit=1 ['boom']`

2. **M2 — drop the Traceback check** (`m2.py:238`, `if proc.returncode != 0:`
   dropping `or 'Traceback' in err`). Concrete tool: `T_trace.py` — correct
   JSON on stdout, a Traceback on stderr, exit 0 (models a real v4 emitting a
   warning/deprecation traceback yet producing valid output). Pristine
   counter rejects it as `runtime_error`; M2 silently accepts it (`survived`),
   under-counting defects.
   - pristine: `PROBE outcome=runtime_error detail=F01_attr_scratch exit=0 ['SyntaxError: boom']`
   - M2:     `PROBE outcome=survived detail=`

3. **M3 — drop the resolved-needle check** (`m3.py:278`, `check_site` no
   longer checks `needle in resolved`). Concrete tool: `T_const.py` — a
   constant table with every bit right (expected/scratch/explicit_out/unflagged)
   but `resolved` empty — exactly the table the contract's resolved-text
   inspection exists to reject ("so a constant table cannot satisfy them").
   Pristine counter kills it; M3 passes it (`survived`).
   - pristine: `PROBE outcome=killed detail=F01_attr_scratch resolved lacks 'mkdtemp'`
   - M3:     `PROBE outcome=survived detail=`

Kills/survivors, per mutant: all three mutants **survive as mutations of the
counter** (they change counting behavior) but are **killed by the probe** (the
bounded detector distinguishes them from the pristine counter — the verdict
flip is demonstrated). Coverage finding only; no contract change is proposed.

## How the self-pin was bypassed (amended-contract scratch clone)

The mutant copies hash differently from the contract pin, so the pristine
self-pin check (`measure.py:366-378`: `at_freeze`/`at_rev`/`running` all must
equal `claims.C2.counter_sha256` from the contract at freeze) refuses. Per
mutant:

1. Full local clone of the lane:
   `git clone /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r42-MutC2Oracle-/clone_m<N>`.
2. Replaced two blobs at `322b5cd…` with `git replace` (refs/replace, local to
   the clone; lane untouched): the contract blob
   (`85d5cb21dca0132a2a51b0d8fbdb3a132bac869f`) with `counter_sha256` set to
   the mutant's sha256, and the measure.py blob
   (`328cb09bda2544fb58c951b89522ec4117fe3a66`) with the mutant bytes.
   New blobs created by `git hash-object -w` inside each clone.
3. Verified: `git -C clone_m<N> show 322b5cd…:.ufo/evidence/round-42/contract.json`
   now yields the amended pin and `…/census/measure.py` yields the mutant bytes,
   so `at_freeze == at_rev == running == pin` and `self_pin=1` (each probe run
   printed `self_pin=1`; the m1 `--tool-file` control also passed the pin gate).

Amended contract files (snapshots, sha256 / bytes):
`contract-amended-m1.json` `4de38ef9…cd5d65` 8300; `contract-amended-m2.json`
`8ba86aa3…da1794` 8300; `contract-amended-m3.json` `10fc6c06…35fdee` 8300.

## Evidence files (scratch root /tmp/tameshi-r42-MutC2Oracle-)

- Mmutants (one-line diffs vs m.py, verified with `diff -u`):
  `m1.py` `7c88e949…ce63b` 19643; `m2.py` `6a045def…bf4586` 19628;
  `m3.py` `dd08de25…538265` 19551.
- Crafted tools: `T_crash.py` `7f6c95fd…14c27` 2784; `T_trace.py`
  `5e9ec49a…1e28` 2793; `T_const.py` `5bf64f1a…b48b2d` 2735.

## Commands (exact)

Pristine (lane, freeze=rev=322b5cd…; read-only, allowed control run):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --probe-mutant /tmp/tameshi-r42-MutC2Oracle-/T_crash.py   # runtime_error
  # … same with T_trace.py -> runtime_error; T_const.py -> killed
```

Mutants (amended clone):

```
python3 /tmp/tameshi-r42-MutC2Oracle-/m1.py \
  --lane /tmp/tameshi-r42-MutC2Oracle-/clone_m1 \
  --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --probe-mutant /tmp/tameshi-r42-MutC2Oracle-/T_crash.py   # killed
# m2.py + clone_m2 + T_trace.py -> survived ; m3.py + clone_m3 + T_const.py -> survived
```

Also run (contrast, both exit 1): `--tool-file T_crash.py` on pristine and on
m1+clone_m1 produce identical control lines (`run_errors=13`, 13 ERROR lines,
`selftest_exit=1`): the M1 divergence surfaces only through the oracle verdict
(probe path), not through the `--tool-file` control line — noted as a probe
observation, not a defect.

## Could not check

- Whether the L1 deciding run passes at the measurement revision (that run is
  not mine; no measurement was taken).
- Nothing else: all runs executed against the lane at 322b5cd… or the amended
  clones.

## Restoration / hygiene

- Live lane checkout never modified: no mutating git/jj commands, no writes
  under `/home/vgpnk/Projects/shokunin/tameshi-shokunin` except this report
  file at `.ufo/waves/round-42/w1/MutC2Oracle.md`.
- The three scratch clones (clone_m1/m2/m3) were removed after recording the
  replace refs; the replacement refs existed only inside those clones, so the
  lane object store and refs are byte-identical to before.
- No tools installed (git 2.56.0, python3 3.14.8 already present; no pacman/
  uv/cargo transactions).
