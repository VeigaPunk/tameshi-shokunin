# Seat T48W2MutC1CounterA — mutation audit of the frozen C1 counter

Lane: tameshi, round 48 attempt 2 (hyaku run 8). Item: mutation-audit the FROZEN C1 counter
`.ufo/evidence/round-48/calibration/measure.py` against its own `--selftest`, one single-site
mutant at a time, ≥25 mutants, across row picking, the amendment-3 row grammar, the amendment-4
attestation rule, and the total/predicate. A survivor is reported with its site, the mutation,
and a concrete killing case; a survivor that changes the deciding verdict on the committed rows
is a finding against the claim.

## Frozen bytes verified

- `sha256sum .ufo/evidence/round-48/calibration/measure.py` →
  `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` — equals
  `freeze-2.json` `counters["calibration/measure.py"].sha256`. The scratch copy `$S/m.py`
  hashed the same before and after the whole sweep (restoration evidence below).
- Baseline detector: `python3 $S/m.py --selftest` →
  `C1_R48_SELFTEST: cases=76 failed=0` / `VERDICT: PASS` (92.9 s). A mutant counts as
  SURVIVED only when its own selftest still prints `failed=0` / `VERDICT: PASS`; KILLED when
  cases fail or the mutant crashes; TIMEOUT is inconclusive and is reported as such.

## Method

- Scratch: `S=/fast/scratch/hyaku/tameshi-r48/T48W2MutC1CounterA`; every mutant written to
  `$S/mutNNN.py`, run with `TMPDIR=$S/tNNN python3 $S/mutNNN.py --selftest` (isolated scratch
  root per run, fixtures never under /tmp); mutant file and its temp dir deleted after each
  run. The pristine `m.py` is never edited; restoration = its sha256 re-verified unchanged
  after the sweep. No lane file was touched; no git/jj state command was run in the lane.
- Each mutant is a single-site string replacement, checked unique (count==1) in the pristine
  source before application; one mutant refused as non-unique (M73, `if stmt['kind'] ==
  'axis':` appears at measure.py:223 and :617-adjacent emit helper — replaced by nothing, so
  the site count below excludes it).
- Detector = the counter's own frozen selftest (76 cases). Per the item, the selftest is the
  bounded behavioral detector; a selftest PASS on a mutant = the frozen test suite does not
  pin that behavior.
- Tooling: none installed or upgraded (python3 + git only). No pacman transaction.

## Site map (measure.py line numbers, frozen bytes)

| area | sites |
|---|---|
| row picking | :136 comment hiding, :139 fence toggle, :170 cap-kind header, :172 axis-kind header, :178 evidence column, :179 `runs 3` filter, :181 last-row-wins |
| amendment-3 grammar | :90 MEMBER_RE, :190 deps charset/`none`, :192 deps dup/sort, :201 evidence column (parse), :213 axis ` or ` split, :214 axis digit check, :226 member exactness, :229 member dedup, :231 class/count pairing |
| attestation (am. 4) | :480 extra counter, :483 extra profile, :484 extra work dir, :530 P1-seen source, :531 missing computation, :533 extra cap, :540 extra-outside-V, :543 UNATTESTED verdict |
| deps | :501 dep reference round, :503 env comparison, :506 variant comparison, :510 required=intersection, :512 never=complement, :551 dep verdict |
| total/predicate | :571 total terms, :572 partial flag, :573-574 passed gates, :582 exit code, :80/:81/:82 frozen constants, :1011 main base pin |
| mismatch counters | :247 compare_part, :429 append_only, :494 unpinned, :526 mismatch+sha, :470/:472 fleet drift/sibling moves |

## Results

(filled from the sweep — see the verdict table below)

## Restoration evidence

(filled after the sweep)
