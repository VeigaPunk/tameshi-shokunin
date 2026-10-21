# PredK2 — falsification of frozen predicate K2 (`argv-casefold`)

**Verdict: K2 is sound and discriminating — it cannot pass vacuously, it passes for the
right reason, and the base receipt in `before.json` is honest and reproducible. Two
calibration defects remain, one of them concrete: (F1) the shipped suite has **zero**
coverage of case differences in `argv[0]` (the program name), so a plausible
case-folding weakening passes all 44 public cases; (F2, latent) the frozen ruler counts
*any* `CASE … FAIL` line, so a collateral kill would also read green.**

Reviewed revision: `c8c5b88c8e961a929cdc351b95a7074c76958909` (`git rev-parse HEAD`).
Base under attack: `6a1821a8897eea6e7d9669292160ec9593669409`.
Lane: leaf reviewer, no dispatch. No production file was edited; no repo tooling
(`--selftest`, gates, registry battery) was executed inside the repo.

---

## Axes (godspeed)

| Axis | Question for K2 |
|---|---|
| **Vacuity** | Can the K2 row be green without any case-only argv evidence existing? |
| **Wrong reason** | Can the mutant be "killed" by something other than argv case strictness? |
| **Discrimination** | Does the shipped suite actually kill a *plausible* case-folding weakening? |
| **Base honesty** | Is `before.json` (1/11) reproducible, or a convenient number? |

---

## What the frozen predicate actually is

`.ufo/evidence/round-24/measure.py:24` fixes the anchor
`if receipt['argv'] != required['argv']:` (one occurrence, `tools/command-binding.py:103`),
and `:30` freezes the K2 mutant text:

```python
('K2', 'argv-casefold', ARGV,
 "if [a.lower() for a in receipt['argv']] != [a.lower() for a in required['argv']]:")
```

Discrimination rule (`measure.py:72-82`): the pristine public selftest must exit 0
(`control_exit`), the anchor must occur exactly once, and the mutated selftest must exit 1
**and** print at least one line matching `CASE … FAIL` (`:80`). The selftest is
`tools/command-binding.py:121-194`; the case-only fixture is
`.ufo/evidence/round-24/extra-cases.json:74` (requirement `argv` `['gate','--check']` at
`:84`, receipt `argv` `['gate','--Check']` at `:112`), loaded by the two-path fixture loop
at `tools/command-binding.py:164-170`.

### Method (read-only; no repo execution)

I re-implemented the delivered `evaluate()` (`tools/command-binding.py:66-111`) verbatim
in a scratch script (`/tmp/tameshi-r24-predk2/sim.py`, `sim2.py`), parameterised only by
which guard is mutated, and ran it over the *exact* case sources the selftest uses:
17 inline `changed()` cases + 19 round-23 fixture cases + 6 round-24 fixture cases
(+2 harness-only cases `tampered` / `duplicate-json-key` that exercise `check()`, not
`evaluate()`). Base suite = 38 cases, delivered suite = 44 cases.

**Fidelity check (the simulator is validated against the recorded receipt, not asserted):**
the simulator predicts, for the base suite, that the K1/K2/K3 mutants fail *no* case and
that the K4 mutant fails exactly `all-of-tokens` — which is precisely what
`before.json` records (`K1/K2/K3`: `exit 0`, `failing_cases []`, tail
`COMMAND_BINDING_SELFTEST: 38/38 pass`; `K4`: `exit 1`,
`failing_cases ["CASE all-of-tokens FAIL"]`, tail `37/38 pass`). Independent second
cross-check: the new registry row `command-binding-selftest-r24` expects
`COMMAND_BINDING_SELFTEST: 44/44 pass`, and the simulator's delivered case count is 44.

```
mode pristine  base-suite failing: []                    delivered-suite failing: []
mode K1        base-suite failing: []                    delivered-suite failing: ['argv-swapped-between-names']
mode K2        base-suite failing: []                    delivered-suite failing: ['argv-case-only']
mode K3        base-suite failing: []                    delivered-suite failing: ['negative-exit-mismatch']
mode K4        base-suite failing: ['all-of-tokens']     delivered-suite failing: ['all-of-tokens']
```

---

## Findings by severity

### F1 — MEDIUM (calibration / concrete counterexample): no coverage of `argv[0]` case folding

The **only** case-only argv difference anywhere in the 44-case suite is at **argv index 1**
(a flag). An exhaustive case-difference inventory over every suite case yields exactly one
row:

```
CASE-ONLY DIFF argv-case-only   elements [1]   receipt=['gate','--Check'] required=['gate','--check']
```

Therefore a weaker implementation that folds case in the **program name only** survives the
entire shipped suite:

```python
# tools/command-binding.py:103, weakened variant
if receipt['argv'][0].lower() != required['argv'][0].lower() or receipt['argv'][1:] != required['argv'][1:]:
```

Simulated result: **0 failing cases out of 44** — the public selftest still reports
`44/44 pass`, exit 0. The frozen K2 mutant folds *all* elements, so it dies on the flag
difference and never touches `argv[0]`; the frozen ruler therefore reports K2 green while
this weaker implementation is completely unobserved.

Why it is plausible rather than exotic: `argv[0]` is a command path/name whose case varies
legitimately on case-insensitive filesystems and under `PATH` resolution, so an implementer
"normalising" argv comparison would plausibly normalise the program name while keeping
flags exact — the one element the suite never probes. The knowledge entry's wording
"change only case" (`corpus/knowledge/replay-projection-hardening.md:13`) reads as covering
all elements and is therefore stronger than the evidence supports.

**Smallest safe correction (does not touch the frozen ruler, changes no K1–K4 verdict):**
add one more case to `.ufo/evidence/round-24/extra-cases.json` whose receipt argv differs
from the requirement only in `argv[0]` case (e.g. requirement `['gate','--check']`,
receipt `['GATE','--check']`, `expected_exit 1`, `finding_ids ["ARGV_MISMATCH"]`).
Consequences to price in: the public selftest becomes 45 cases, so the registry row
`command-binding-selftest-r24` expectation `COMMAND_BINDING_SELFTEST: 44/44 pass`
(`tools/registry.json`) must become `45/45`, and the after-measurement must be re-run.
Under the pristine gate the new case passes; under the frozen K2 mutant it fails, so K2
stays green and the `argv[0]` gap closes.
*Zero-code alternative if the wave will not re-run the ruler:* record the gap verbatim in
`corpus/lessons/round-24.md`'s "Reject" list (one clause) instead of leaving it implicit.

### F2 — LOW (latent wrong-reason risk in the frozen ruler)

`measure.py:80-82` discriminates on `bool(fails)` — *any* `CASE … FAIL` line qualifies —
while `failing_cases` is recorded but never asserted. A mutant that broke an unrelated case
while `argv-case-only` still passed would also read green, and the receipt could not
distinguish "killed by the case-only fixture" from "killed by collateral damage". This is
**not** the situation today: I verified that the frozen K2 mutant's *unique* failing case is
`argv-case-only` (expected `(1, ['ARGV_MISMATCH'])`, got `(0, [])`), i.e. it passes for
exactly the right reason. The gap is in the instrument's attribution, not in this run.
Recommendation (not applied — `measure.py` is frozen): a future ruler generation should
carry an expected-killer case name per mutant and require it in `failing_cases`; for round
24, the after-receipt should state the killer case per row.

### F3 — INFORMATIONAL (scope honesty; already disclosed — not a defect)

K2's discrimination is **suite-borne, not logic-borne**. `tools/command-binding.py` between
base `6a1821a8` and delivered `c8c5b88` changes only the selftest's fixture-loading loop
(5 insertions / 4 deletions at `tools/command-binding.py:164-170`); the production argv
comparison at `:103` is byte-identical, and the base tree has neither the round-24 fixture
nor `tools/registry-replay.py` (`git show 6a1821a:.ufo/evidence/round-24/extra-cases.json`
→ absent; `…:tools/registry-replay.py` → absent), which is exactly why `before.json` shows
K7–K11 `tool-absent`. So "1/11 → 11/11" on K1–K4 measures the shipped selftest's
mutation-detection power; the gate's argv comparison was already case-exact at base. The
contract bound ("K1-K4 count selftest kills of four specific mutants, not general mutation
adequacy", `contract.json` `bounds[0]`) and the lesson/knowledge text
(`corpus/lessons/round-24.md:23-24`, `corpus/knowledge/replay-projection-hardening.md:38`)
already disclose this, so no correction is required — but the phrase "harden
required-command binding" must be read as "harden the selftest that would catch a
case-folding binding", not as a change to the binding logic.

### Base honesty: PASS (no defect found)

`before.json` is honest and reproducible:

* `instrument_sha256` (`before.json:13`) `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64`
  equals `sha256sum .ufo/evidence/round-24/measure.py` at the reviewed tree, and
  `git log --follow -- .ufo/evidence/round-24/measure.py` shows exactly **one** commit
  (`e338f1b`) — the ruler was frozen before any seat and is unchanged since, as the lesson
  claims (`corpus/lessons/round-24.md:10-11`).
* The recorded base rows are exactly what the base tree can produce: base suite = 38 cases
  (17 inline + 19 round-23 + 2 harness cases); the base tree lacks the round-24 fixture, so
  K1/K2/K3 mutants kill nothing (`exit 0`, `failing_cases []`, `38/38 pass`) while the K4
  mutant kills `all-of-tokens` (`exit 1`, `37/38 pass`) → exactly the recorded 1/11 with K4
  as the control. The simulator reproduces all of these, including the `stdout_tail`
  strings recorded in `before.json`.
* `control_exit 0` / `restored_exit 0` on every K1–K4 row are consistent with the pristine
  38-case suite passing and with the file being restored between mutants
  (`measure.py:79`).
* No vacuity path exists in the green direction: if the round-24 fixture were missing from
  the copy, the K2 mutant would exit 0 and the row would be red (`discriminated false`), not
  green; and a crash in the mutated selftest would print no `CASE … FAIL` line, so
  `measure.py:80` would also refuse to count it.

---

## Counterexample summary

| Question | Answer | Evidence |
|---|---|---|
| Can K2 pass vacuously? | **No** | Pristine 44/44 control passes; the only green path is the mutant failing the case-only fixture; missing fixture ⇒ red, crash ⇒ red (`measure.py:80`) |
| Can K2 pass for the wrong reason? | **Not in this run** (instrument gap F2 remains) | Unique failing case under the K2 mutant is `argv-case-only` (expected `(1,['ARGV_MISMATCH'])`, got `(0,[])`) |
| Does K2 fail to discriminate a plausible weaker implementation? | **Yes — F1**: fold-case-in-`argv[0]`-only passes 44/44 | Simulated 0 failing cases; only case-only diff in the suite is at argv index 1 (`extra-cases.json:84` vs `:112`) |
| Is `before.json` honest? | **Yes** | instrument digest matches, ruler has one commit, base-tree absences match `tool-absent` rows, simulator reproduces all four K1–K4 base rows verbatim |

---

## Residual risk & verification gaps

* I did **not** execute `tools/command-binding.py --selftest`, the registry battery or the
  ruler inside the repo (lane bound). The 44/44 and 38/38 figures above are from a faithful
  simulation of `evaluate()`, cross-validated twice against recorded artefacts
  (`before.json` tails, registry row `44/44`). The authoritative after-measurement remains
  the sibling ruler run; note that **no after artefact is present in the delivered tree**
  (`.ufo/evidence/round-24/` contains `before.json` only), so the 11/11 claim is currently
  unbacked inside the repository.
* F1's counterexample is a *static* result; confirming it by execution would require
  mutating `tools/command-binding.py` in a private clone, which this lane did not do.
* F1's severity depends on the intended threat model: if only the frozen mutant matters,
  F1 is documentation-only; if "argv case strictness" is meant generally (as
  `corpus/knowledge/replay-projection-hardening.md:13` reads), F1 is a real coverage hole.
* K2 says nothing about the other nine predicates; K5/K6 (`registry.json` digest pins) and
  K7–K11 (`tools/registry-replay.py`) were out of this lane's scope.

## Tooling

No tool was installed or upgraded for this review (analysis required only the system
`python3` and read-only `git` with `GIT_OPTIONAL_LOCKS=0`). Scratch scripts live outside the
repo at `/tmp/tameshi-r24-predk2/`; no repo file, index or sibling lane was touched.
