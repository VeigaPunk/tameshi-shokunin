# tameshi round 98 — frozen declarations (plan)

Lane `tameshi` (verification-fixture craft). Round 98, attempt 1. Base (lane tip at
round start): `034240a591575167f0747ad7372a1f4b9cd33a58`, branch `master`.
Instruments commit: `d32043ec836ca097e93ae0b095faa7cae4125697` (the audit tool, the
registry audit, the repaired driver `.ufo/evidence/round-98/controls98.py` and the
refusal battery with its exit-code repair). The records revision R is the commit that
carries this plan, `claims.json` and the pre-freeze receipts; R is named in
`.ufo/waves/round-98/records-rev.txt` when it lands.

Round 97 landed admitted; its non-author spot-check
(`corpus/lessons/round-97-verifier-spotcheck.md`) left seven status-neutral defects
D-1…D-7. This round closes **D-2** and **D-6** as its two claims and lands D-1, D-3,
D-4, D-5 and D-7 as routed-defect work items (see §Routed defect closures). D-2: the
round-97 pre-freeze driver registered `c2-nowork-absent` with the literal `0` as its
graded code, so the control could not fail whatever the wrapped `git grep` returned.
D-6: two of the round-97 matrix's six `GUARD_SETUP` refusal classes had no committed
receipt or selftest case; only their code existed.

Axes: depth + calibration (lane axes). C1 moves **calibration** (the lowest
non-retired axis, pinned 8): the lane's own control battery proves, mechanically, that
each recorded code is a measurement — the class the spot-check found by eye. C2 moves
**operability**: a runnable battery that exercises every declared refusal class of a
frozen tool through its public CLI and can fail. The DoD control for C1 is the round-97
driver unchanged at the instrument revision (one literal-coded site, exit 1); for C2 it
is the committed evidence at the base (neither code-only class token appears anywhere,
`git grep` exit 1).

The frontier step (§2b) rides inside this cap: S012 is re-opened for C1's knowledge
entry, the round's mined mistake is the round-97 in-place `anchor` edit (D-1) with the
new registry audit as its able-to-fail fix, and the census runs before and after.

---

## Claims (frozen before data)

### C1 — calibration: every recorded control code is a measurement

- **Axis:** calibration (a record's assertion is a function of the measured result, not
  of a literal typed beside it).
- **Surface:** `tools/control-assertion-audit.py` at R, reading the committed driver
  blobs `.ufo/evidence/round-97/controls97.py` and `.ufo/evidence/round-98/controls98.py`
  at R through `git cat-file`; and the repaired driver's own end-to-end run.
- **Wording (frozen):** at the records revision R,
  `python3 -I tools/control-assertion-audit.py --repo . --rev R --driver .ufo/evidence/round-98/controls98.py`
  prints `CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0` and exits 0, and
  the same command with `--driver .ufo/evidence/round-97/controls97.py` prints
  `CONTROL_ASSERT sites=15 measured=14 literal=1 unmeasured=1` and exits 1, naming the
  literal site at line 156 (`c2-nowork-absent`). The audit reads the driver blob at R
  through `git cat-file` (never the worktree), counts static `add(...)` call sites (a
  site inside a loop counts once), and classifies a recorded code as measured only when
  its expression derives from a runner call (`sh`, `git`, `run`, `subprocess.run`): a
  constant, a constant bound through a name, a loop variable, a plain call, or a
  `returncode` attribute on a value not assigned from a runner call is unmeasured. The
  diagnosed repair, `c2-nowork-absent` in `controls98.py`, grades the measured
  `git grep` rc (1 at base `07e50d6d`) instead of the literal 0, and the repaired
  driver's full run
  (`python3 -I .ufo/evidence/round-98/controls98.py --lane . --base 07e50d6d0142b21e8443b5417b8edc4d1dd76455 --rev R --work <empty dir> --outdir <dir>`)
  prints `CONTROLS98 states=18 matched=18 mismatched=0` and exits 0, with
  `c2-nowork-absent.out` carrying outer `rc=1` where the round-97 receipt carries
  outer `rc=0`.
- **Counter:** the `controls98.py` audit command above.
- **Red arm:** the `controls97.py` audit command above; selftest
  `python3 -I tools/control-assertion-audit.py --selftest` → `CONTROL_ASSERT_SELFTEST: 12/12 pass`.
- **Predicate:** `CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0` (exit 0).
- **Before:** at the base `034240a5` no committed tool prints a `CONTROL_ASSERT` line
  (`git grep -c 'CONTROL_ASSERT' 034240a5 -- .` prints nothing, exit 1;
  `.ufo/evidence/round-98/pre-freeze/c1c2-before-tokens.out`); the round-97 driver's
  `c2-nowork-absent` is `add("c2-nowork-absent", 0, …)` and its committed receipt
  carries outer `rc=0` while the wrapped `git grep` returns 1 (spot-check D-2;
  `.ufo/evidence/round-97/pre-freeze/c2-nowork-absent.out`). The defect was found by a
  non-author reading, not by any lane instrument.
- **After:** the two audit lines and exits, the selftest tally, and
  `CONTROLS98 states=18 matched=18 mismatched=0`, all at R.
- **Kill rules:**
  - a: a constant, or a name bound to a constant, is reported `measured`;
  - b: a `returncode` attribute on a value not assigned from a runner call is reported
    `measured`;
  - c: the round-97 driver reports `unmeasured=0` or a literal count other than 1;
  - d: a call site is skipped, or a site inside a loop is counted more than once;
  - e: the audit reads the worktree instead of the blob at R (a worktree-only edit
    changes the line);
  - f: the repaired driver's run cannot fail (a wrong recorded code still prints
    `mismatched=0`).
- **Declared limits:** the audit is static — it classifies `add(...)` call sites, not
  the runtime state set, and a driver registering through a differently named recorder
  is zero-site and passes vacuously (R98L1 probes the boundary). "Measured" means the
  expression derives from a runner call somewhere in its name chain, not that the
  runner ran the command the state claims (a `sh(["true"]).returncode` passes while
  running nothing relevant); the claim is provenance, not command identity. The
  repaired driver's `--base` is the round-97 base `07e50d6d` because its two no-work
  states are round-97 states; at the round-98 tip both tokens exist, so the same driver
  run with `--base 034240a5` prints `mismatched=2` by design
  (`.ufo/evidence/round-98/pre-freeze/controls98-at-round-base.out`).

### C2 — operability: every declared guard refusal class is exercised end to end

- **Axis:** operability (a runnable battery produces each declared refusal through the
  frozen tool's public CLI, with a receipt).
- **Surface:** `.ufo/evidence/round-98/refusals/guard-refusals.py` at R, driving the
  frozen tool blob `.ufo/evidence/round-97/c2/guard-inertia.py` at R.
- **Wording (frozen):** at the records revision R,
  `python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --lane . --rev R --tool .ufo/evidence/round-97/c2/guard-inertia.py --tool-sha 634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8 --work <empty dir>`
  prints `GUARD_REFUSALS classes=6 refused=6 wrong=0 positive=ok` and exits 0. It reads
  the frozen tool as a blob at R and refuses a `--tool-sha` that is not 64 hex or does
  not equal the blob's sha256 (setup exit 2); it builds one manifest fixture per class
  in a scratch clone and runs the tool's public CLI once per class with the fixture's
  own digest, requiring exit 2 and a line of the tool's own stdout equal to
  `GUARD_SETUP <class>` or prefixed by `GUARD_SETUP <class>:` for each of edit-no-op,
  edit-ambiguous, state-unbuildable, limit-mechanism-missing, manifest-sha-mismatch and
  manifest-empty; the committed manifest is run once and must print
  `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0` with exit 0. With
  `--red state-unbuildable` the positive manifest replaces that class's fixture and the
  battery prints `GUARD_REFUSALS classes=6 refused=5 wrong=1 positive=ok red=state-unbuildable`
  and exits 1. At the base `034240a5`,
  `git grep -c 'GUARD_SETUP state-unbuildable'` and
  `git grep -c 'GUARD_SETUP limit-mechanism-missing'` over `.ufo/evidence` each print
  nothing and exit 1.
- **Counter:** the battery command above.
- **Red arm:** the `--red state-unbuildable` command above; selftest
  `python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --selftest` →
  `GUARD_REFUSALS_SELFTEST: 9/9 pass`.
- **Predicate:** `GUARD_REFUSALS classes=6 refused=6 wrong=0 positive=ok` (exit 0).
- **Before:** at the base no committed tool prints a `GUARD_REFUSALS` line; the two
  class tokens appear in no committed receipt (`git grep` rc 1,
  `.ufo/evidence/round-98/pre-freeze/c1c2-before-tokens.out`); the round-97 record
  receipted four classes and left `state-unbuildable` and `limit-mechanism-missing`
  code-only (spot-check D-6).
- **After:** the battery line at R, exit 0; the six per-class runs in the transcript;
  the red line and exit 1.
- **Kill rules:**
  - a: a class counted refused when its run's exit is not 2;
  - b: a class token accepted from anything but a line of the tool's own stdout (a
    manifest string, a stored receipt, an earlier run's output);
  - c: the red arm still counts the substituted class refused (the battery cannot
    fail);
  - d: the tool is read from the worktree or a blob whose sha256 is not the pinned
    value;
  - e: the positive is not run, or its predicate is not the exact line with exit 0;
  - f: the summary is printed without all six fixtures and the positive run.
- **Declared limits:** the battery measures that the frozen tool refuses each fixture
  with the declared token, not that the refusal is semantically the right one (a tool
  refusing every manifest at its first row with the right token would pass all six;
  R98R2 verifies that each fixture reaches its declared branch in the tool's order).
  The tool's wording is the frozen round-97 wording; this round adds receipts, not a
  re-declaration. The six fixtures share the frozen tool's four-file store limit.

## Pre-registered controls (executed and committed before this freeze)

All under `.ufo/evidence/round-98/pre-freeze/`, run by the L1 against the instruments
commit `d32043ec` before any scored record exists. Every command exits with the listed
code.

| state | attack | expected |
|---|---|---|
| `c1-audit-r97-driver` | audit the round-97 driver at `d32043ec` | `sites=15 measured=14 literal=1 unmeasured=1`, line 156 named, rc 1 |
| `c1-audit-controls98` | audit the repaired driver at `d32043ec` | `sites=15 measured=15 literal=0 unmeasured=0`, rc 0 |
| `c1-audit-selftest` | the audit's 12 fixture arms | `CONTROL_ASSERT_SELFTEST: 12/12 pass`, rc 0 |
| `controls98-run` | the repaired driver, base `07e50d6d` | `CONTROLS98 states=18 matched=18 mismatched=0`, rc 0 |
| `controls98-at-round-base` | the same driver at base `034240a5` (both tokens present) | `states=18 matched=16 mismatched=2` (the two no-work controls), rc 1 |
| `c2-refusals-positive` | six classes + positive at `d32043ec` | `classes=6 refused=6 wrong=0 positive=ok`, rc 0 |
| `c2-refusals-red` | `--red state-unbuildable` | `classes=6 refused=5 wrong=1 positive=ok red=state-unbuildable`, rc 1 |
| `c2-refusals-selftest` | the battery's nine grading arms | `GUARD_REFUSALS_SELFTEST: 9/9 pass`, rc 0 |
| `registry-red-r96-r97` | the registry audit on `0b19af5f..29734beb` | two `anchor` findings (S006, S159), `changed=2`, rc 1 |
| `registry-green-r97-instr` | the registry audit on `29734beb..d32043ec` | `changed=0 removed=0 added=0`, rc 0 |
| `registry-selftest` | the registry audit's ten arms | `REGISTRY_IMMUTABLE_SELFTEST: 10/10 pass`, rc 0 |
| `c1c2-before-tokens` | `git grep` at `034240a5` for `CONTROL_ASSERT` / `GUARD_REFUSALS` | no output, rc 1 |

## Do-nothing controls

- **C1:** leave the round-97 driver unchanged and run the audit on it — the target line
  reads `measured=14 literal=1 unmeasured=1` and exits 1. Read no driver at all — no
  `CONTROL_ASSERT` line exists at the base (`git grep` rc 1). The target is reachable
  only by the repair plus the audit.
- **C2:** write no battery — no `GUARD_REFUSALS` line exists, and neither code-only
  class token appears in committed evidence (`git grep` rc 1 each). The target is
  reachable only by running the six fixtures.

## Kills for the round

- C1 kill rules (a)–(f); C2 kill rules (a)–(f).
- Any `falsifies-wording` artifact of this round's own wave that contradicts a frozen
  sentence is amended **before the records run** in §Amendments (wording narrowed to
  the enforceable property, with the artifact cited); a sentence the instrument cannot
  enforce is an honest stop naming the narrowing, never a wider filing.

## Amendments

Pre-data: no claim receipt exists when a row here is written (the pre-freeze controls
are controls, not a scored record; the records run postdates every row). Rows are added
only from this round's wave artifacts, before the records run.

| id | artifact | falsified sentence | amendment |
|---|---|---|---|
| — | — | (none at freeze) | — |

## Routed defect closures (round-97 spot-check, not claims)

| id | closure | evidence |
|---|---|---|
| D-1 | the in-place `anchor` additions on S159/S006 are logged old→new in the round-98 lesson (append-only remedy B of the spot-check); no cell is rewritten; the new registry audit measures the class | `corpus/lessons/round-98.md` §Registry changes; `registry-red-r96-r97` (two findings) |
| D-3 | the three pre-A15 fragments (`pre-freeze/c1-forge-conjunct.out`, `w1/SC1-quote-backability.txt`, `w1/SC1-receipt-catalog.txt`) are marked superseded by an appended note beside them, with both digests, never rewritten | `.ufo/evidence/round-97/pre-freeze/NOTE-superseded-r98.txt`, `.ufo/waves/round-97/w1/NOTE-superseded-r98.txt` |
| D-4 | `committed-battery binder` and `guard-inertia matrix` enter the SCORECARD `## Capabilities` table | `SCORECARD.md` round-98 append |
| D-5 | the report erratum (S159 15 words / snapshot `4b5a8374`; S006 span 490-491 vs 490-492) and a committed `CONTROLS97` summary receipt | `corpus/lessons/round-98.md` §Errata; `.ufo/evidence/round-97/pre-freeze/CONTROLS97-summary.txt` |
| D-7 | the stale-lane line grades this round `progressing` with commit counts | round-98 report |

## Frontier step (§2b)

- Sources: S012 is re-opened live this round (snapshot + located quote in the lesson
  `## Gate`); S009's flip is probed and reported; no new row is written; census before
  and after must be exit 0 with 183 rows.
- Sourced claim: C1's knowledge entry `corpus/knowledge/control-assertion-anchoring.md`
  cites S012 (opened this round) — a control whose expectation does not flow from the
  measured output cannot fail, which is the state-anchored-oracle class.
- Mined mistake: the round-97 in-place `anchor` edit (D-1), captured by the non-author
  spot-check and not by the census; fix = `tools/registry-cell-immutability.py`, whose
  red run prints the two findings and whose green run prints zero.
- Registry changes are limited to `status`/`recheck`/`used-by`, each logged old→new.
