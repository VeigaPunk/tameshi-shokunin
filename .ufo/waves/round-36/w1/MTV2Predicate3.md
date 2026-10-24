# MTV2Predicate3 — mutation probe: C2 v2 accept-slot target

Seat: mutation tester (leaf, no subagents). Wave: round-36 / w1. Verdict: **KILLED**.

## Target
- File under attack (frozen v2 successor counter): `.ufo/evidence/round-36/c1/c1-measure-v2.py`
  at lane rev `b455001e2589b3f4f471d94a3de7e5e549b9f54c` (committed content rev named in the
  round-36 receipt; lane tip at probe time `d9c496b`, clean tree apart from other seats'
  untracked report dir).
- Frozen sha256 (verified before and after): `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`.
- Pins re-verified in-process by v2 itself: runner `a7d3f2dd…12eb9` (runner_sha_ok=1),
  tool `6188db16…d354` (tool_sha_ok=1).

## Mutant (smallest behavior-bearing point)
- Single-token mutation inside the assigned isolated scratch copy:
  `.ufo/evidence/round-36/c1/c1-measure-v2.py:69` `PUB_ACCEPT_SLOTS_TARGET = 3` → `= 2`.
- Usage sites of that name (only three, verified by grep): line 69 definition, line 539
  (`pub_accept_slots == PUB_ACCEPT_SLOTS_TARGET`, declared-slot cardinality) and line 540
  (`pub_accept == PUB_ACCEPT_SLOTS_TARGET`, passing-slot cardinality). No other behavior reads it.
- Byte evidence (mutant differs from pristine by that line only —
  `diff <(sed 's/= 2$/= 3/' mut) pristine` empty):
  - pristine snapshot `c1-measure-v2.pristine.py` = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`
  - mutant snapshot `c1-measure-v2.mut.py` = `c73c8f073f526fc995a044677c9e0b44104e537419944232ac2e1448d43bc040`
- Scratching: lane cloned to
  `/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate3/lane-copy` (`git clone --shared`,
  read-only against the lane); the lane itself was never written. v2 reads its panel, runner
  and tool from `git show` at `--rev`, and uses no `__file__`/script-relative path (grep), so
  running the mutant snapshot is behaviorally identical to running it in place.

## Detector (same bounded check on all three byte-states)
`python3 <counter> --lane <clone> --rev b455001e… --work <fresh empty dir> --sealed .ufo/evidence/round-35/c1/sealed`
— i.e. the contract's `counting_command` (`.ufo/evidence/round-36/contract.json:35`).
Pass criterion: exit 0 **and** final line `C1_R36V2_PASS=true`. Anything else fails the detector.

## Actual outputs
```text
PRISTINE  EXIT=0 (214s)
C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=true

MUTANT    EXIT=1 (207s)
C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=false

RESTORED  EXIT=0 (159s)
C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=true
```
`diff base.out mut.out` is exactly one line (line 17): the verdict token `true` → `false`.
All 16 `COPY …` scorer rows are byte-identical across the three runs, as are every measured
count (`pub_kill=6/6`, `pub_accept=3/3`, `pub_distinct=9`, `ho_*`, `sealed_after_freeze=1`).
So the flip is caused by the mutated target constant alone, not by any measurement drift:
the added v2 bind (`== PUB_ACCEPT_SLOTS_TARGET`, lines 539/540) is load-bearing, and v1's
panel-derived comparison would not have caught this mutant.

Full transcripts: `/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate3/{base,mut,restore}.out`.

## Restoration evidence
- Scratch lane copy: script was never mutated in place; hash before/after probe both
  `9eb8944c…da8fa53`; `git -C lane-copy status --porcelain` empty after all three runs.
- Restored snapshot `c1-measure-v2.restored.py` = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`,
  `cmp` against the pristine snapshot byte-identical, and its run reproduces the baseline
  verdict (`EXIT=0`, `PASS=true`).
- Lane file untouched: `.ufo/evidence/round-36/c1/c1-measure-v2.py` hashes to the frozen pin
  after the probe; nothing was written to the lane except this report.

## Verdict
`PUB_ACCEPT_SLOTS_TARGET 3→2` — **KILLED** (baseline PASS → mutant FAIL, restored PASS;
single-line output delta; exact bytes restored, hash-verified).

Calibration note (coverage observation, no contract change requested): the verdict line
prints the *measured* accept count against the *measured* slot count (`pub_accept=3/3`) and
never prints the frozen targets, so a reader of a receipt cannot tell from the line which
targets produced `PASS`; only the counter's bytes pin them. The assert itself is verified
binding here.

## Tooling
No installs or upgrades were made; no `pacman`. Python 3 from the host only.
