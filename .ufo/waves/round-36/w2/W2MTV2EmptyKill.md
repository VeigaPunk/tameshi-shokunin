# W2MTV2EmptyKill — kill-half-only panel mutant against the round-36 v2 counter (round 36, w2)

**Verdict: KILLED — with the kill half of the public panel emptied and the accept half
intact, the frozen v2 counter prints `C1_R36V2_PASS=false` (first failing frozen clause
`PUB_KILL_SLOTS_TARGET`), while the frozen v1 counter prints `C1_R35_PASS=true` at
`pub_kill=0/0 pub_accept=3/3`. The v1 vacuous accept is real on this shape, and the v2
cardinality target closes it.**

## Attacked

Contract `C2` (`.ufo/evidence/round-36/contract.json`), frozen successor counter
`.ufo/evidence/round-36/c1/c1-measure-v2.py` sha256
`9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` — specifically the
public-surface conjuncts added over round-35 v1:

```python
and pub_kill_slots == PUB_KILL_SLOTS_TARGET      # 6
and pub_accept_slots == PUB_ACCEPT_SLOTS_TARGET  # 3
and pub_distinct == PUB_DISTINCT_TARGET          # 9
```

Behaviour-bearing point mutated: the **committed public panel** at
`.ufo/evidence/round-35/c1/panel` (read by both counters via
`load_copies_rev(lane, rev, …)`), not the counter. Six kill-set copies deleted; three
accept-set copies untouched.

## Mutation (scratch clone only)

Scratch root: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2EmptyKill/`
(`pristine` = faithful clone at rev `b455001e…`; `mutant` = second clone carrying the
mutant commit; the lane checkout was never written).

- Base rev: `b455001e2589b3f4f471d94a3de7e5e549b9f54c` (the contract's measurement
  commit; `git diff b455001e..fbb01cf -- .ufo/evidence/round-35 .ufo/evidence/round-36/c1 tools`
  is empty, so the lane tip `fbb01cf46f8437fd1264c1a3acc053c882fa2164` carries identical bytes).
- Mutant commit: `e293975f58c7ae88cefde1293ba478fc764d5525`
  (child of base, scratch clone identity `tameshi-w2 <w2@tameshi.invalid>`).
- Delta: exactly 6 files deleted, 90 lines, nothing else:
  `cfg00-accept-swap.json`, `cfg11-pass-mask.json`, `root-keyed-auto-mask.json`,
  `root-keyed-auto-zero.json`, `root-keyed-shape6.json`, `workdir-branch-swap.json`
  (all `"set": "kill"`). Retained byte-identical: `comment-brace.json`,
  `comment-esac.json`, `comment-names-leg.json` (all `"set": "accept"`).
- Panel tree ids: base `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e` → mutant
  `d19568770f5517d22cc76f28a3db66a252cf7555`.
- Patch artifact: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2EmptyKill/mutant-kill-half-empty.patch`
  (3524 bytes, sha256 `786c2cea3feedc72f259703043c2104a8d1c32c987f24ecae332796a03e43e60`).

Clone fidelity (read-only checks): `diff -r` of `panel/` and `sealed/` against the lane
checkout → identical; committed frozen bytes at `b455001e` →
tally-audit-v3.py `6188db16…d354`, mutate-and-run.sh `a7d3f2dd…2eb9`,
c1-measure-v2.py `9eb8944c…8fa53`; v1 counter `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3`.

## Commands run

All from scratch; `--work` is a fresh empty directory per run (the counter refuses a
non-empty one); `--sealed .ufo/evidence/round-35/c1/sealed` is lane-relative inside each
clone. Lane argument is the clone path in every run.

Pristine baseline (cwd `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2EmptyKill`):

```
python3 pristine/.ufo/evidence/round-35/c1/c1-measure.py \
  --lane "$S/pristine" --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c \
  --work "$S/work-v1-base" --sealed .ufo/evidence/round-35/c1/sealed
python3 pristine/.ufo/evidence/round-36/c1/c1-measure-v2.py \
  --lane "$S/pristine" --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c \
  --work "$S/work-v2-base" --sealed .ufo/evidence/round-35/c1/sealed
```

Mutant (same commands against the mutant clone at the mutant rev, fresh work dirs
`work-v1-mut` / `work-v2-mut`):

```
python3 mutant/.ufo/evidence/round-35/c1/c1-measure.py \
  --lane "$S/mutant" --rev e293975f58c7ae88cefde1293ba478fc764d5525 \
  --work "$S/work-v1-mut" --sealed .ufo/evidence/round-35/c1/sealed
python3 mutant/.ufo/evidence/round-36/c1/c1-measure-v2.py \
  --lane "$S/mutant" --rev e293975f58c7ae88cefde1293ba478fc764d5525 \
  --work "$S/work-v2-mut" --sealed .ufo/evidence/round-35/c1/sealed
```

Restored (mutant clone hard-restored to base, fresh work dirs `work-v1-restored` /
`work-v2-restored`): identical commands at rev `b455001e…`.

Attribution checker (scratch-only, executes no panel):
`python3 check_predicate.py <LABEL> "<predicate line>"` re-evaluates the printed integers
against the frozen constants and the v2 source's `ok =` clause, naming failing conjuncts.

## Outputs

Pristine panel (6 kill / 3 accept / 9 distinct bodies):

| Counter | Exit | Predicate line |
|---|---|---|
| v1 | 0 | `C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R35_PASS=true` |
| v2 | 0 | `C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=true` |

Mutant panel (kill half emptied: 0 kill slots / 3 accept / 3 distinct bodies; all 3
surviving accept rows `pass=True`, holdout still 4/4 kill, 3/3 accept, 7 distinct):

| Counter | Exit | Predicate line |
|---|---|---|
| v1 | **0** | `C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=3/3 pub_slots=3 pub_distinct=3 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=e293975f58c7ae88cefde1293ba478fc764d5525 C1_R35_PASS=true` |
| v2 | **1** | `C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=3/3 pub_slots=3 pub_distinct=3 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=e293975f58c7ae88cefde1293ba478fc764d5525 C1_R36V2_PASS=false` |

Restored panel (exact base bytes): v1 exit 0 `… pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 … C1_R35_PASS=true`;
v2 exit 0 `… pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 … C1_R36V2_PASS=true`.

Checker attribution on the mutant v2 line:

```
CHECK C1_R36V2 slots=0/3 distinct=3 ho=4/4+3/3 sealed=1
CHECK_FAILING: PUB_KILL_SLOTS_TARGET, pub_kill==PUB_KILL_SLOTS_TARGET, PUB_DISTINCT_TARGET
CHECK_FIRST: PUB_KILL_SLOTS_TARGET
CHECK_PASS_AGREES: True
```

`PUB_ACCEPT_SLOTS_TARGET` and both accept-count clauses pass, so the failure is located
in the public **kill** surface, exactly as tasked. `PUB_DISTINCT_TARGET` also fails
because the surviving 3 accept bodies are 3 distinct bodies — an unavoidable consequence
of the same kill-half deletion, not independent evidence. v1's checker run reports no
failing clause (`CHECK_FAILING: (none)`), i.e. its pass is genuine under its own
self-relative predicate: `0 == 0` kill slots and `3 == 3` accept slots.

Predicate-line capture files (scratch): `base-v1.stdout`, `base-v2.stdout`,
`mut-v1.stdout`, `mut-v2.stdout`, `rest-v1.stdout`, `rest-v2.stdout`;
stderr empty (0 bytes) for all six runs.

## Restoration evidence

- Mutant clone before restore: HEAD `e293975f58c7ae88cefde1293ba478fc764d5525`,
  panel tree `d19568770f5517d22cc76f28a3db66a252cf7555`.
- After `git reset --hard b455001e…`: HEAD `b455001e2589b3f4f471d94a3de7e5e549b9f54c`,
  panel tree `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e` — equals the pristine clone's
  tree id; all nine panel file sha256 values match the pre-mutation values
  (`c5e5c652…2d46`, `f5da18e8…5c30`, `8fbf2436…9f33`, `2f10fb95…b276`,
  `e39a524b…83a5a`, `c02c7851…6ddc`, `d6e26e1a…95f5`, `a8950eb9…4768`,
  `920a0e3d…6027`); `git status --porcelain` in the clone is empty; frozen artifact
  hashes re-checked on restored bytes (unchanged pins above).
- Detector re-run on restored bytes: v1 PASS true (exit 0), v2 PASS true (exit 0).
- The pristine clone was never mutated (mutant work was done in a separate clone).
- The lane checkout was not written: `git -C tameshi-shokunin status --porcelain` still
  shows only the pre-existing untracked `.ufo/waves/round-36/w1/` and `/w2/` dirs;
  HEAD `fbb01cf…`; frozen hashes unchanged. This report is the only lane file created.

## Findings / limits

1. The frozen v2 counter **kills** the kill-half-empty public panel; the frozen v1
   counter **survives** it. Killed/survived is measured against the same detector set
   (v1, v2) on pristine, mutant, and restored bytes; baseline is green on both counters
   at the same rev, so the v2 exit 1 is attributable to the mutation, not the harness.
2. This mutant is strictly narrower than the round-36 empty-*whole*-panel control
   receipt (`.ufo/evidence/round-36/control/v1-at-emptypanel.stdout`, `v2-at-emptypanel.stdout`,
   both `pub_kill=0/0 pub_accept=0/0`): keeping the accept half intact shows the v1 pass
   is not merely an all-empty special case — v1 passes with a fully healthy accept surface
   and zero kill slots.
3. The C2 claim itself (v2 deciding PASS at `b455001e`) is independently reproduced here
   from a fresh clone: v2 `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9`,
   exit 0.
4. Limits: one mutant shape, one run per state (no repeats); only the public panel was
   mutated; the counter, sealed set, runner, and tool are pinned byte-for-byte and were
   not edited. Nothing here judges C1, the ledger algorithm, or the SCORECARD.

## Tools installed

None (no package manager invoked; no tool installs or upgrades).
