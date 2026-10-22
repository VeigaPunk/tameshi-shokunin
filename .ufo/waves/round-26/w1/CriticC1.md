# CriticC1 — round 26, wave 1: is the ninth leg a depth move or a count bump?

Seat: TameshiR26.CriticC1 (critic). Axis judged: depth. Measured revision: integration
`a08e85c5d7f899e8a5992e20517edb1a380d79eb`, base `d4140796f4e48e8ec81b793facba73fbd03b4443`.
All code ran in `/tmp/criticc1-r26/` (clones, variants, mutants). No lane file other than this
report was written. No git write commands and no jj commands were run. No tools were installed.
Host: node v24.21.0, Python 3.14.8.

## Verdict

**In substance this is a real depth move, not just a count bump. At `a08e85c` it is not yet
admissible as one, and the instrument that measures it cannot tell the difference.**

- The leg is new evidence. It has a new target path, a new blob, and a new spec of 10 defects.
  The sweep was executed and the landed runner replays it exactly: on a clean `/tmp` clone at
  `a08e85c`, `REGRESSION_TABLE js-cite-check: match=10/10 … flips=0` and
  `REGRESSION: PASS (cases=9 passed=9 …)`. Running it also taught something that reading the
  code did not: one prediction got the verdict right but the mechanism wrong (objection 3).
- Five objections hold:
  - The counter passes a duplicated leg, and the regression companion passes it too
    (objection 5).
  - At `a08e85c` there is no learning record (objection 7).
  - "Never-measured" is false provenance (objection 2b).
  - One of the five survivors is provably an equivalent mutant (objection 6).
  - The 5/10 kill rate and the 10/10 prediction score are produced by the design, not by blind
    measurement (objection 3).
- Three objections do not hold against C1 as written: the PROVINCE two-lane rule (1), the
  round-12 ruling (2a), and the hermetic-only suite (4).

| # | Objection | Holds? | Impacted axes |
|---|---|---|---|
| 1 | The PROVINCE two-lane rule is breached | no (it is a tradeoff to watch) | depth (generality) |
| 2a | Round-12: this is reanalysis of a measured target, so it is depth within a case | no | depth |
| 2b | "Never-measured" provenance | **yes** | calibration, depth provenance |
| 3 | Predictions were written by the L1 after reading the suite | **yes, as a bound** | depth (learning content) |
| 4 | The suite is only the hermetic group | no (one wording fix) | depth |
| 5 | The counter can pass while the leg is wrong | **yes** | depth (ruler) |
| 6 | (found) S_EMPTY_GUARD is an equivalent mutant, not a suite hole | **yes** | depth, calibration |
| 7 | (found) The leg's knowledge entry is missing at `a08e85c` | **yes** | depth (learning), sourced criterion |

## Evidence per objection

### 1. PROVINCE two-lane rule: does not hold

- `PROVINCE.md:15-16`: "a pattern is admitted from evidence in TWO independent lanes before it
  is claimed general". The rule is triggered only by a claim of generality.
- C1 claims a case count (`contract.json:11-14`). It does not claim a pattern. The draft entry
  limits itself explicitly (`.ufo/waves/round-26/w1/DraftEntry.md:457-459`): "The 50 % is a
  property of this suite at this pin, not of kumitate's gates in general."
- Residual tradeoff: the ledger is now concentrated in one lane. Five of the nine ledger lines
  are kumitate (`tools/mutate-and-run.sh:87-95` at `a08e85c`). The last four legs are all
  kumitate, and the last three all score 5/10. This is not a defect today. Any wave-2 text
  that reads the survivor classes or the 50 % as a fleet pattern would breach the rule.

### 2a. Round-12 ruling: does not hold for the real leg

- `SCORECARD.md:290-291`: "reanalysis of the same bash target is depth within a case, not a
  new independent case."
- `corpus/lessons/round-12.md:23`: the flip condition is "a genuinely new independently
  recorded case, not another analysis dimension".
- cite-check was never a recorded leg. At `a08e85c` the ledger has 9 lines with 9 distinct
  target paths and 9 distinct `PIN_*` values (my check is in objection 5). The round-26 spec
  is 10 new defects. It is not a reclassification of an earlier table, so the flip condition
  is met.

### 2b. "Never-measured" provenance: holds

- `contract.json:11`: "ninth recorded mutation case on a never-measured kumitate gate".
- `corpus/knowledge/fleet-kill-rate-ledger.md:94` records a probe at the same pin `40573448…`:
  "PREP-T6 **probe**: 4 defects — **1 killed** (K3 …)".
- The same file at `:107` says "**probe only, 1/4** (§2); full sweep open".
- `corpus/knowledge/fleet-suite-census.md:611` also lists cite-check as "**probe only**".
- So the case is the first pre-registered full sweep of a gate that was already probed. It is
  not a never-measured gate. TameshiR26.ConnectorOverlap reached the same finding
  independently (`ConnectorOverlap.md:10,42-48`). I re-located the ledger and census quotes
  myself this session.
- The probe's three CLI-accounting survivors (aggregate-verdict collapse, n/n summary counts,
  CLI exit fail-open) are not re-measured by the round-26 spec.

### 3. Predictions written by the L1 after reading the suite: holds, as a bound

- Every prediction names the selftest case that asserts it, or says "none: no hermetic case
  passes …" (`predictions.json:9-18`). The control run was observed before pre-registration
  (`predictions.json:6`). The predictions are therefore suite-informed by construction.
- The composition is fixed by design (`cite-check.defects.spec:4`): "5 kill-aimed / 5
  hole-aimed". Round 18 used the same design (`.ufo/evidence/round-18/sources-check/sources-check.defects.spec:4`)
  and got the same 5/10. Round-gate also recorded 5/10 (`tools/mutate-and-run.sh:93-95`).
- Consequence: "10/10 verdict predictions held" measures how well the L1 read the suite. The
  5/10 is set by the composition. Neither number is a blind estimate of how strong the suite
  is.
  - The depth rubric counts recorded cases (`SCORECARD.md:66`), so the +1 is unaffected.
  - Any learning claim built on the rate or on the hit count is unsupported.
  - `tools/mte-interop.py` will export this leg's 50 % as a mutation score next to the
    swept legs.
- Counter-evidence that the run still taught something reading did not: the K_PIN_KIND
  reason was wrong.
  - It predicted rev-classified pins "come back REV_UNKNOWN, not OK or PIN_MISMATCH"
    (`predictions.json:10`).
  - Observed: `FAIL  content pin match → OK; mismatch → PIN_MISMATCH — match=yes mismatch=no`
    (`sweep/evidence/K_PIN_KIND.out:8`). The match arm still returns OK.
  - The kill widths also vary: K_UNRESOLVED_SEV fails 7 of 62 cases
    (`sweep/sweep.txt:21`), K_FENCE_TILDE fails 2 (`:39`), and the others fail 1.
  - So this is not purely a count bump.

### 4. Suite is only the hermetic group: does not hold, but one sentence is wrong

- `cite-check.mjs:73-81` (pinned bytes): `--selftest` runs only the hermetic group, and
  `--integrations` runs the live-tree group.
- I ran the pristine pin and all 10 mutants with `--selftest --integrations --self
  <kumitate> --fleet /home/vgpnk/Projects/shokunin`, with the live tree at
  `~/Projects/ufo-fsd-alpha`. Scratch only, TMPDIR in `/tmp/criticc1-r26/itmp*`.
  - **Control:** `6/9 cases passed (integration)`, `VERDICT: FAIL`, exit 1. The three
    failures are the F4, F2 and F3 live-tree cases. The runner's green-control gate would
    therefore refuse the integration group as an oracle today.
  - **Per-case diff against the control:** none of the five survivors (S_OOR_EDGE, S_STRICT,
    S_EMPTY_GUARD, S_USAGE, S_PIN_INCLUDES) changes any integration case. The only difference
    is the random temp-repo hash in the `real rev → resolved-by-git` line.
  - **Net:** widening the suite adds 0 kills.
- `DraftEntry.md:462-464` says the hermetic rate "is a lower bound on what the gate's own full
  suite would kill". That is true in direction, but it implies headroom that does not exist.

### 5. The counter can pass while the leg is wrong: holds

I built four runner variants with `/tmp/criticc1-r26/make_variants.py` and ran
`python3 .ufo/evidence/round-26/c1-measure.py --repo <variant>` on each. Every one printed
`C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9` and exited 0.

| Variant | What is wrong | Counter | Regression companion |
|---|---|---|---|
| CE1 ghost (on base) | The ninth "leg" exists only as comment lines plus a dead `: <<'DEAD'` heredoc | 9, exit 0 | [INFERENCE] `cases=8`; only real calls run, so the contracted `cases=9` string is not met |
| CE2 swap (on `a08e85c`) | K_UNRESOLVED_SEV and S_OOR_EDGE verdicts swapped; killed count still 5 | 9, exit 0 | ran: `match=8/10 … flips=2`, `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)`, exit 1 |
| CE3 duplicate (on base) | A ninth leg `js-sources-check-dup` that replays leg 8's target, pin and spec again | 9, exit 0 | ran: `REGRESSION_TABLE js-sources-check-dup: match=10/10 … flips=0`, **`REGRESSION: PASS (cases=9 passed=9; ledger legs exact …)`**, exit 0 |
| CE4 bad pin (on `a08e85c`) | Garbage `PIN_CITECHECK`/`REV_CITECHECK`, and the ledger line relabelled `9/10 (90 %)` | 9, exit 0 | [INFERENCE] SETUP on the pin mismatch (`mutate-and-run.sh:217-218`) |

- The contract bound (`contract.json:32`) admits only the gap between the table and the sweep.
  CE2 shows the companion closes that gap.
- CE3 is the strongest counterexample. It is exactly the duplicate case that the round-12
  ruling rejects, yet it passes both the counter and the regression companion with the exact
  contracted string. Of the remaining companions:
  - `mte-interop` would refuse it only by leg name, through its hard-coded `LEG_TABLE`
    (`tools/mte-interop.py:74-78`). That is a one-line edit away from passing.
  - `registry-check` and `sources-census` do not read the ledger.
  - No instrument in C1's ruler enforces target independence.
- Real leg: the counter on base gives `recorded_cases=8 wired_legs=8 depth_score=8` (exit 1).
  On `a08e85c` it gives `recorded_cases=9 wired_legs=9 depth_score=9` (exit 0). The real
  regression also passes (see the verdict). The independence check below gives
  `ledger_lines=9 distinct_targets=9 pins=9 distinct_pins=9` on `a08e85c`, against
  `distinct_targets=8 … distinct_pins=8` on CE3. So C1's number is right; the ruler is weaker
  than the contract states.

### 6. S_EMPTY_GUARD is equivalent, not a suite hole: holds

- `cite-check.mjs:1553-1583` (pinned bytes): `totals.filesScanned++` (`:1556`) runs before any
  `totals.resolved++` (`:1583`), inside the same per-document loop. A failed read does
  `continue` before both.
- Therefore `resolved > 0` implies `filesScanned > 0`, and the dropped conjunct at `:1590` is
  redundant for every input. `main()`'s fail-closed message (`:2527-2528`) reads `totals`,
  not `verdict`, so nothing else can tell the two apart.
- `DraftEntry.md:157,466-467` says "none proved equivalent". `DraftEntry.md:397` proposes the
  killing fixture "or vice versa" (resolved > 0 with filesScanned = 0), which cannot exist.
  The other proposed fixture (files scanned but zero resolved) gives FAIL under both the
  original and the mutant.
- So there are 4 real survivors, not 5. Against killable mutants the rate is 5/9. The recorded
  table stays as measured. TameshiR26.CriticEquivalence owns the full equivalence audit.

### 7. Learning record missing at `a08e85c`: holds

- The `a08e85c` SKILL section says "Entry: `corpus/knowledge/mutation-case-kumitate-cite-check.md`"
  (`git diff d414079 a08e85c -- SKILL.md`, added section "Ninth recorded case — round 26").
- That file does not exist at `a08e85c` (`test -e` in the clone gives `no`), nor in the lane
  worktree (`worktree-no`). The `a08e85c` diff stat adds no `corpus/knowledge/` file.
- The contract requires (`contract.json:25`) "the knowledge entry for the leg cites a
  SOURCES.md row opened this round". `DraftEntry.md:480-482` says S088 and S089 "are
  placeholder ids — neither row exists yet".
- At `a08e85c`, then, C1 is a ledger row, a table and a dangling pointer. The "count bump"
  charge holds at this revision. It is discharged only when the entry lands with a mined,
  this-round source row.

## Smallest safe corrections (L1 to apply; frozen contract unchanged)

1. **Ruler bound (objection 5).** Add one sentence to the C1 bound in the lesson and SCORECARD
   row: neither the counter nor the regression companion checks that the leg is independent of
   the other legs. Record this independence receipt next to it (it reads only the runner):
   `python3 -c 'import re,sys;t=open(sys.argv[1]).read();l=re.findall(r"^#   ((?:js|bash)-\S+)\s+(\S+)\s+\d+/\d+",t,re.M);p=re.findall(r"^PIN_[A-Z]+=([0-9a-f]{64})$",t,re.M);print(len(l),len({x for _,x in l}),len(p),len(set(p)))' tools/mutate-and-run.sh`
   Expected output `9 9 9 9` at the measured revision. CE3 gives `9 8 8 8`.
2. **Learning record (objection 7).** Land `corpus/knowledge/mutation-case-kumitate-cite-check.md`
   with a real mined source row before C1 is admitted. Until then, mark the SKILL pointer
   as not yet resolving.
3. **Provenance (objection 2b).** In the entry, lesson and SKILL, say "first pre-registered full
   sweep; a PREP-T6 probe recorded 1/4 at the same blob". Append the ledger supersession for
   `fleet-kill-rate-ledger.md:94,107` and `fleet-suite-census.md:611`. Record the contract's
   "never-measured" as a corrected claim, not edited.
4. **Design bound (objection 3).** In the entry's limits, state that the 5/10 is set by the 5/5
   composition and that 10/10 measures how well the suite was read. Keep the K_PIN_KIND
   mechanism miss as the run's own finding.
5. **Equivalence (objection 6).** Mark S_EMPTY_GUARD equivalent, citing `cite-check.mjs:1553-1590`.
   Drop the impossible "or vice versa" probe. Report 4 real survivors alongside the measured 5/10.
6. **Hermetic wording (objection 4).** Replace the "lower bound" sentence with the measured
   result: on 2026-10-22 the integration group's control is red (6/9), and it distinguishes
   none of the five survivors from the control.

## Commands run (all observed this session)

- `python3 …/c1-measure.py --repo /tmp/criticc1-r26/base` gives `depth_score=8`, exit 1.
  `--repo /tmp/criticc1-r26/clone` gives `depth_score=9`, exit 0.
- `python3 make_variants.py`, then the counter on the four variants: all give `depth_score=9`,
  exit 0.
- `GIT_OPTIONAL_LOCKS=0 bash tools/mutate-and-run.sh --regression --workdir /tmp/criticc1-r26/regr-<v>`.
  These ran inside `/tmp/criticc1-r26/fleet-<v>/tameshi-shokunin`, with sibling repos
  symlinked and read only through `git show`.
  - real: PASS 9/9.
  - ce2-swap: FAIL, flips=2.
  - ce3-dup: PASS 9/9.
- `python3 make_mutants.py`, then
  `node mut/<ID>/scripts/cite-check.mjs --selftest --integrations --self <kumitate> --fleet <fleet>`
  for the control and all 10 mutants, followed by a normalized per-case diff (objection 4).
- `git -C kumitate-shokunin show 1205c66…:scripts/cite-check.mjs` gives sha256 `40573448…0c9f`
  and 2537 lines, matching the pin. `git diff --stat 1205c66 HEAD -- scripts/cite-check.mjs`
  is empty.

No tool was installed or upgraded. The scratch lives at `/tmp/criticc1-r26/`.
