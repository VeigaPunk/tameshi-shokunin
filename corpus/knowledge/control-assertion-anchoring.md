# Control-assertion anchoring — the code a control grades must be a measurement

source: S012 — https://arxiv.org/abs/2608.17214 (Canedo, "Oracles That Cannot Fail"),
abstract re-opened 2026-11-08, snapshot `.ufo/evidence/round-98/sources/s012.html`
42588 B sha256 `fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80`;
the round-97 driver `.ufo/evidence/round-97/controls97.py` and the repaired driver
`.ufo/evidence/round-98/controls98.py`, read as blobs at `d32043ec836ca097e93ae0b095faa7cae4125697`
verified-at: 2026-11-08; audit receipts `.ufo/evidence/round-98/pre-freeze/c1-audit-*.out`,
`c1-audit-selftest.out`, `controls98-run.out`; instrument
`tools/control-assertion-audit.py` sha256 `82c2e54b24bab55e9f01bb3f15afcb2c3b2654c3486bf6de29a06981cc5c0cd4`
recheck: 90d; reopen S012 and re-run the audit at the next driver revision
ground: calibration — the lane's own pre-freeze battery (round-97 spot-check D-2); not a
frontier row, no coverage-map ground is claimed by this entry

## 1. The question

A control battery is a set of states, each registering a name, the exit code it
observed, a body, and the code it expects. The verdict is the comparison of two
numbers: the code the driver recorded and the code the state declares. If the
recorded number is typed into the driver instead of taken from the process the
state claims to run, the comparison has no measurement on one side, and it cannot
fail whatever the process returns.

Round 97's driver carried exactly one such state. `controls97.py:156` registered
`c2-nowork-absent` with the literal `0` as its recorded code and `0` as its
expectation; the wrapped `git grep GUARD_INERTIA` returned 1, and the committed
receipt `.ufo/evidence/round-97/pre-freeze/c2-nowork-absent.out` carries outer
`rc=0` with the inner `rc=1` visible only in the body text. The batch printed
`CONTROLS97 states=18 matched=18 mismatched=0`. A non-author spot-check found it by
reading (D-2); no lane instrument classified the recorded code at all.

## 2. The class, and S012's dual

S012 names the oracle failure this lane already knows from the survivor side: a
**state-anchored** oracle obtains its expected value from the system it judges, so
a fault moves measurement and expectation together and the comparison cancels. Its
abstract, line 112 under the lane renderer
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py:strip_tags`), 16 words:

> A test oracle that obtains its expected value from the system it is judging cannot fail.

[OBS] The round-97 defect is the same failure in the other direction: the recorded
side does not flow from the measurement at all, so the comparison is
constant-versus-constant. [INF] Both are covered by S012's question — *what fixed,
outside value anchors this comparison?* — but the dual direction (a constant where
a measurement belongs) is the lane's own observation, not a claim of the paper.

## 3. The rule

`tools/control-assertion-audit.py` reads a driver blob at a revision through
`git cat-file` (never the worktree) and classifies the recorded-code argument of
every `add(...)` call site:

- **measured** — the expression derives from a call *spelled* `sh`, `git`, `run` or
  `subprocess.run`, directly (`p.returncode`) or through a name chain; a name is
  followed through the call's own scope chain (function locals, enclosing functions,
  module) to **every** assignment before the call, and all of them must be measured;
  `code, out = run(...)` binds `code` as measured;
- **literal** — a constant, directly or through a name whose scope chain carries a
  literal assignment;
- **unresolved** — a loop variable, a plain call, an augmented assignment, a
  non-runner `.returncode`, a `returncode` reassigned after its runner call, a name
  with no assignment in its scope chain, or any site in a module with more than one
  `add` definition.

A driver conforms only when every site is `measured`; the expectation
(`want_code`) is data and is not classified. Sites are counted statically, so a
site inside a loop counts once. At `d32043ec` the round-97 driver prints
`CONTROL_ASSERT sites=15 measured=14 literal=1 unmeasured=1` (exit 1, line 156
named) and the repaired driver prints `sites=15 measured=15 literal=0 unmeasured=0`
(exit 0). The repair makes the recorded code the measured `git grep` rc; the
repaired driver's full run prints `CONTROLS98 states=18 matched=18 mismatched=0`
with `c2-nowork-absent`'s outer `rc=1` at base `07e50d6d`.

## 4. The audit's own selftest

Eighteen arms, `CONTROL_ASSERT_SELFTEST: 18/18 pass` at the repaired instrument
(sha256 `82c2e54b…`): a direct literal and a literal bound through a name are
`literal`; a name with a mixed literal-then-runner history is `literal` (all
assignments must be measured), while two all-runner assignments stay `measured`;
`subprocess.run(...).returncode` and a tuple-bound `code` from `run(...)` are
`measured`; a `returncode` attribute on a class constant, a `p.returncode = 0`
reassignment after the runner, an augmented assignment and a module with two `add`
definitions are `unresolved`; a nested-scope shadow does not leak into the call's
scope chain; a constant `if`-expression and a name with no prior assignment are
`unresolved`; exit codes 0/1 follow the unmeasured count; a loop site counts once.

## 5. Boundaries

- The audit is static: it classifies bare-name `add(...)` call sites, not the
  runtime state set. A driver registering through a differently named recorder or a
  method call is zero-site and passes vacuously — the audit cannot see a shape it
  does not name.
- Branch reachability is approximated by "every pre-call assignment measured", so a
  correct driver that assigns a literal only in an unreachable branch is flagged
  (conservative); control flow is not analyzed.
- A locally defined function *named* `run`/`sh`/`git` is indistinguishable from the
  real runner by spelling: a driver of stubs scores `measured` while recording
  literals. The rule closes the constant class for the spelling it accepts, not the
  stub class.
- `measured` is provenance, not command identity: `p = sh(["true"])` then
  `add(..., p.returncode, ...)` is measured while running nothing the state claims.
  The rule closes the literal class, not every vacuous assertion.
- A driver that computes its recorded code correctly but copies its expectation
  from the recorded code stays out of scope; the expectation is data by design.
- The audit reads committed bytes at a resolved commit id; a worktree-only edit is
  not a subject of the verdict.

## 6. Evidence

- `.ufo/evidence/round-98/pre-freeze/c1-audit-r97-driver.out` — the 15 sites, line
  156 literal, `unmeasured=1`, exit 1.
- `.ufo/evidence/round-98/pre-freeze/c1-audit-controls98.out` — 15/15/0, exit 0.
- `.ufo/evidence/round-98/pre-freeze/controls98-run.out` — `CONTROLS98 states=18
  matched=18 mismatched=0` at base `07e50d6d`.
- `.ufo/evidence/round-98/pre-freeze/controls98-at-round-base.out` — the same run
  with `--base 034240a5` prints `matched=16 mismatched=2` (the two no-work states),
  the disclosed limit.
