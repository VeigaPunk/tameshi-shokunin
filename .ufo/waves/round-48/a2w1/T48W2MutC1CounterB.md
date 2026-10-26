# T48W2MutC1CounterB — mutation audit of the frozen C1 counter (round 48, wave a2w1)

Seat: T48W2MutC1CounterB (godspeed). Target attacked: the FROZEN round-48 C1 counter
`.ufo/evidence/round-48/calibration/measure.py` (sha256
`572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3`, recorded in
`freeze-2.json`), via its own `--selftest` as the behavioral detector.

## Method

- Worked entirely on a scratch copy: `S=/fast/scratch/hyaku/tameshi-r48/T48W2MutC1CounterB`;
  `pristine.py` = byte copy of the frozen counter (hash above verified before and after the sweep;
  the lane checkout was never written).
- Detector: `python3 mut_<name>.py --selftest` on each single-site mutant (full 76-case selftest,
  `TMPDIR=$S`). Baseline pristine run: `C1_R48_SELFTEST: cases=76 failed=0`, `VERDICT: PASS`,
  rc=0, 232 s wall (receipt in `baseline.stdout`/`baseline.rc`, scratch).
- 64 mutants, one behavior-bearing site each, grouped exactly by the assigned behaviors:
  round loop (R=3, sequential rounds, cleanup), per-round dependence comparison (variant vs that
  round's P1; env = P0 vs P1), required/unstable/never classification, dep_mismatch rule,
  mismatch over ALL rounds' P0 tuples, unobservable, `--only`/`--rounds` PARTIAL labels,
  self_pin/stmts_pin/append_only, total composition, amendment-4 extras/attestation.
- Killed = selftest rc≠0 or `failed>0`. Survivor = full selftest still green. Every survivor was
  then attacked with a targeted killing case (`probe.py`): a scratch git fixture driving the
  mutated `measure()` directly with fake observation/fleet functions.
- Static committed-row probe (`probe_rows.py`): applied the pristine row grammar to SCORECARD.md +
  statements.json at the content revision `c7586b9a10e…` in a `--shared` scratch clone:
  **all 22 rows status=ok, all single-member `stable`, all sha pins match** — i.e. unparsed=0,
  oversize=0, unpinned=0 structurally on the committed rows.
- These are probes, not verdicts: nothing here scores C1.

## Results

(sweep table inserted here on completion)

## Restoration evidence

- Frozen file sha256 before sweep: `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3`
- Frozen file sha256 after sweep: (recomputed at cleanup; must be identical — no write to the lane
  was ever attempted; all mutants lived and died under `$S`)
- Scratch dir deleted before finish.

## Tooling

None installed or upgraded (existing python3/git sufficient).
