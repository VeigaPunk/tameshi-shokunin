# MTV2Predicate2 — mutation probe of the v2 distinctness assert (C2)

Round 36, wave 1. Leaf mutation-tester seat. Scope: challenge the C2 successor
counter's `pub_distinct == PUB_DISTINCT_TARGET` term with one plausible defect
— the weakest possible frozen target, `9 -> 1` — and run the contract's own
deciding command on pristine, mutated and restored bytes. All work happened in
an isolated scratch copy; the lane was only read.

## Attacked

- Counter: `.ufo/evidence/round-36/c1/c1-measure-v2.py`, frozen at sha256
  `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`
  (contract C2 `counter_sha256`).
- Claim term: `pub_distinct == PUB_DISTINCT_TARGET` with
  `PUB_DISTINCT_TARGET = 9` (assert added by v2 over the round-35 tally-audit
  panel; contract C2 `frozen_targets.PUB_DISTINCT_TARGET`, predicate line 541).
- Mutant: a single-line edit at line 70, `PUB_DISTINCT_TARGET = 9` →
  `PUB_DISTINCT_TARGET = 1` (one occurrence; `diff` = 4 lines, exactly one
  changed line). Mutant sha256
  `bcbafee956957adfdf892b8170cb12a0226fc84587a7e52eb1e3aac3f269c7eb`.
  This is the weakest value that still leaves a non-vacuous `==` term: it
  asserts the panel has at least the cardinality of a single body.
- Detector: the contract C2 counting command (below), deciding mode, at the
  round-36 refresh/measurement commit
  `b455001e2589b3f4f471d94a3de7e5e549b9f54c` — the revision the round-36
  receipt `.ufo/evidence/round-36/after/c1v2-at-b455001e.stdout` records as
  the PASS run. Controls: frozen v1 counter at the same rev/panel (the
  "v1 would pass" arm) and the unmutated v2 baseline.

## Scratch copy and pins (all absolute)

- Scratch root: `/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/`
- `cp -a /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/lane`
  — scratch HEAD `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (lane tip).
- Scratch pins re-verified before any run, all equal to the dispatch pins:
  v2 counter `9eb8944c…`; v1 counter `d360a159…`; `tools/tally-audit-v3.py`
  `6188db16…`; `tools/mutate-and-run.sh` `a7d3f2dd…`.
- Pristine byte backup kept at
  `…/MTV2Predicate2/evidence/c1-measure-v2.pristine.py` (`9eb8944c…`).

## Commands run (from `/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/lane`)

Detector, repeated once per arm with a fresh empty `--work` dir:
`/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/work/{pristine-v2,mutant-v2,restored-v2}`

```
python3 .ufo/evidence/round-36/c1/c1-measure-v2.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/lane \
  --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c \
  --work /fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/work/<arm> \
  --sealed .ufo/evidence/round-35/c1/sealed
```

v1 control arm (`--work …/work/pristine-v1`):

```
python3 .ufo/evidence/round-35/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/lane \
  --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c \
  --work /fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate2/work/pristine-v1 \
  --sealed .ufo/evidence/round-35/c1/sealed
```

Restoration: `cp -p evidence/c1-measure-v2.pristine.py lane/.ufo/evidence/round-36/c1/c1-measure-v2.py`,
then the detector was re-run on the restored bytes.

## Observed

All four runs scored the same 9-copy public panel (6 kill / 3 accept) and the
same sealed set (4 kill / 3 accept), at the same rev:

| arm | counter sha256 (first 8) | `pub_distinct` | target | predicate | exit |
|---|---|---|---|---|---|
| pristine v2 | `9eb8944c` | 9 | 9 | `C1_R36V2_PASS=true` | 0 |
| **mutant v2** | `bcbafee9` | 9 | **1** | **`C1_R36V2_PASS=false`** | 1 |
| frozen v1 (control) | `d360a159` | 9 (printed, not asserted) | — | `C1_R35_PASS=true` | 0 |
| restored v2 | `9eb8944c` | 9 | 9 | `C1_R36V2_PASS=true` | 0 |

- Mutant stdout: 16/16 `COPY … pass=True` rows (all behavioral/slot checks
  green), then `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 …
  C1_R36V2_PASS=false`.
- `diff` pristine-v2 vs mutant-v2 stdout = **one changed line** (line 17, the
  predicate line: `PASS=true` → `PASS=false`). Every per-copy row is
  byte-identical, so the flip is attributable solely to the weakened
  `PUB_DISTINCT_TARGET`; the term is load-bearing, not redundant with the
  slot/behavior counts.
- v1 control prints `pub_distinct=9` but has no distinctness term, so the same
  panel/rev yields `C1_R35_PASS=true` — confirming the task's
  "v1 would pass" premise and that the mutant arm is a v2-only kill.
- Mutant exit: the counter returned 1 (contract: exit 0 iff predicate true).
  The run wrapper propagated non-zero and aborted before the rc-echo step, so
  the code is taken from the wrapper's `Command exited with code 1`; the full
  mutant stdout was captured by redirection.

Evidence files (scratch, sha256):
`baseline-v2.stdout` `5e2b4e15c0a24face50273f3200da7ce7747f96908410ce61eaec22f85393efb` (17 lines);
`baseline-v1.stdout` `ec854c4bde56516a3c589fa981519b53c34e36a9ce4ac6dafd8e5aae90c980db`;
`mutant-v2.stdout` `53cfdc9a94c6b043c5e5744c6362f27bb6c2743f13560742b14bc6de86c744d3`;
`restored-v2.stdout` `5e2b4e15…` — byte-identical to the pristine baseline.

## Restoration evidence

- Post-restore counter sha256 = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`,
  equal to pristine and to the contract pin.
- `git -C <scratch lane> status --porcelain --untracked-files=no` is empty
  (mutant edit fully reverted).
- Restored-byte detector run: `C1_R36V2_PASS=true`, exit 0, stdout identical
  to the pristine baseline. Scratch copy retained at the path above.

## Bounds / tooling

- Lane, fleet repo, sibling lanes, `.ufo/state/` and all frozen artifacts were
  never written; the only lane write is this report. No subagents. No package
  installs or upgrades. All git invocations were read-only (`rev-parse`,
  `show`, `log`, `merge-base`, `status`) against the scratch copy.

## Verdict

**KILLED — the mutant is detected.** Weakening `PUB_DISTINCT_TARGET` from 9 to 1
flips `C1_R36V2_PASS` from true to false and the exit code from 0 to 1 while
every per-copy behavioral row stays green; the frozen v1 counter passes the
same panel at the same rev. The v2 distinctness assert is load-bearing, and the
unmutated counter is restored byte-exactly.
