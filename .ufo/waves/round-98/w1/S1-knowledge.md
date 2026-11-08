# Control-assertion anchoring — a control's graded code must be a measurement

> Draft by seat R98S1 (scribe) for the records commit. Proposed full text of
> `corpus/knowledge/control-assertion-anchoring.md`. Every receipt line and every source
> quote below was matched against a blob committed at
> `764aca97e513d650949999362cd4b0f5f0e566a5` (the freeze) with `git show`/`git grep -F`; the
> exception is the two boundary probes in §6 marked as wave artifacts, which land with the wave
> record and are cited by path, not quoted as receipts.

source: S012 — https://arxiv.org/abs/2608.17214 (Canedo, "Oracles That Cannot Fail"), abstract
re-opened 2026-11-08 (HTTP/2 200, `date: Sun, 08 Nov 2026 15:46:31 GMT`; 42588 B), snapshot
`.ufo/evidence/round-98/sources/s012.html` sha256
`fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80`; the round-97 driver
`.ufo/evidence/round-97/controls97.py` (sha256 `a75c542824a94947dd7ed54de175bd3e3a1e660cdcc4eb6c93091ea76170d6ad`)
and the repaired driver `.ufo/evidence/round-98/controls98.py` (sha256
`f1c1db0edb670fdefdb1b27a193b315db8da90f4580cc7c4c225648f3fbf924b`), read as blobs at
`d32043ec836ca097e93ae0b095faa7cae4125697`; instrument `tools/control-assertion-audit.py`
sha256 `774a5b5979fa53f9725553cf1169419d4a11519143083a87635bf7be71956b2c`; audit and driver
receipts `.ufo/evidence/round-98/pre-freeze/`, committed at
`764aca97e513d650949999362cd4b0f5f0e566a5`
verified-at: 2026-11-08 — every figure in §1–§6 is a line a named receipt prints at the named
revision, or a line of the committed tool source
recheck: 90d — reopen S012 and re-run the audit at the next driver revision; a scope-aware
resolver or a differently named recorder changes §4 and §7
ground: calibration — the lane's own control battery, found by the non-author round-97
spot-check (D-2). This is not a frontier row and claims no coverage-map ground.

## 1. The question

A control battery registers states. Each state carries a name, a recorded exit code, a
body, and the exit code it declares. The verdict compares two integers: the code the
driver recorded and the code the state declares. If the recorded integer is typed beside
the state instead of taken from the process the state claims to run, one side of the
comparison is a constant and the comparison cannot fail, whatever the process returns.

Round 97's driver carried exactly one such state. `controls97.py:156` registered

    add("c2-nowork-absent", 0,
        "git grep GUARD_INERTIA at base %s: rc=%d out=%r" % (...), 0)

The wrapped `git grep` returned 1. The committed receipt
`.ufo/evidence/round-97/pre-freeze/c2-nowork-absent.out` reads
`git grep GUARD_INERTIA at base 07e50d6d0142b21e8443b5417b8edc4d1dd76455: rc=1 out=''`
followed by outer `rc=0` — the 1 exists only in the body text, where no oracle reads it.
The batch's own summary was stdout-only; it is restated, labelled as a restatement and not a
re-execution, in `.ufo/evidence/round-97/pre-freeze/CONTROLS97-summary.txt` (round-97
spot-check D-5). A non-author spot-check found the state by reading (D-2); no lane instrument
classified a recorded code at all.

## 2. The class, and S012's dual

S012 names the oracle failure this lane already tracks from the survivor side: a
**state-anchored** oracle takes its expected value from the system it judges, so a fault
moves measurement and expectation together and the comparison cancels. The abstract, line
112 under the lane renderer
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py:strip_tags`), 16 words:

> A test oracle that obtains its expected value from the system it is judging cannot fail.

[OBS] The round-97 state is the same failure in the other direction: the recorded side does
not flow from any measurement, so the comparison is constant against constant. [INF] Both
directions answer S012's question — *what fixed, outside value anchors this comparison?* —
but the constant-where-a-measurement-belongs direction is the lane's own observation, not a
claim of the paper.

## 3. The rule

`tools/control-assertion-audit.py` reads a driver blob at a revision through
`git cat-file` (never the worktree) and classifies the recorded-code argument of each
static `add(...)` call site:

- **measured** — the expression derives from a runner call, where the runner allowlist is
  exactly `sh`, `git`, `run`, `subprocess.run`: directly (`p.returncode` where
  `p = run(...)`), through a name chain, or as the first element of `code, out = run(...)`;
- **literal** — a constant, directly or bound through a name;
- **unresolved** — a loop variable, a plain call, arithmetic, a non-runner `.returncode`,
  or a name with no prior assignment.

A driver conforms only when every site is `measured`; the expectation (`want_code`) is data
and is not classified. The audit prints one `CONTROL_ASSERT_SITE` line per site, then
`CONTROL_ASSERT sites=N measured=N literal=N unmeasured=N`, and exits 0 when every site is
measured, 1 when any site is not, 2 at setup (bad revision, driver absent or unparsable, an
`add` without a code argument), 64 on usage.

Sites are counted statically, so a site inside a loop counts once. Both drivers carry 15
`add(...)` call sites (`grep -cE '^[[:space:]]+add\('` over each committed blob prints
15). Two of the sites sit inside loops and register 3 and 2 states at runtime, so the run
covers 18 states — `sites=` is the static count, never the state count.

## 4. The measured lines

At `d32043ec`, the audit on the round-97 driver prints
`CONTROL_ASSERT sites=15 measured=14 literal=1 unmeasured=1` and `rc=1`, naming the site:
`CONTROL_ASSERT_SITE line=156 name=c2-nowork-absent measured=no class=literal detail=constant`.

The repair replaces the literal with the measured `git grep` rc and keeps the expectation
as data (`controls98.py:159`):

    add("c2-nowork-absent", g.returncode,
        "git grep GUARD_INERTIA at base %s: rc=%d out=%r" % (a.base, g.returncode, ...), 1)

The audit on the repaired driver prints `CONTROL_ASSERT sites=15 measured=15 literal=0
unmeasured=0` and `rc=0`. The repaired driver's own run at base `07e50d6d` prints
`CONTROLS98 states=18 matched=18 mismatched=0`, and its `c2-nowork-absent.out` now carries
outer `rc=1` where the round-97 receipt carried outer `rc=0`.

## 5. The audit's own selftest

Twelve arms, `CONTROL_ASSERT_SELFTEST: 12/12 pass`, `rc=0`: a direct literal and a literal
bound through a name are `literal`; `subprocess.run(...).returncode`, a tuple-bound `code`
from `run(...)`, and a name rebound to a measured value are `measured`; a `returncode`
attribute on a class that defines it as a constant is `unresolved`; a constant `if`-expression
is `literal`; a loop site is `measured` and a name with no prior assignment is `unresolved`;
exit codes follow the unmeasured count (`exit-conforming` 0, `exit-literal` 1); and
`loop-site-count` measures one site, not one per iteration.

## 6. Boundaries

- The audit is static: it classifies `add(...)` call sites, not the runtime state set. A
  driver registering through a differently named recorder is zero-site and passes vacuously.
- Name resolution is linear in source order over the whole module and is **scope-blind**: the
  last assignment before the call wins even when it sits in a nested scope. A fixture with
  `p = 0` at the site's scope and a nested `p = subprocess.run([...])` assigned earlier than
  the site in line order is reported `measured` with `detail=returncode-of-runner-name` while
  the site records the constant 0 (`CONTROL_ASSERT_SITE line=9 name=shadowed-constant
  measured=yes class=measured detail=returncode-of-runner-name`; wave artifact
  `.ufo/waves/round-98/w1/R98C1-c1-kill-a-shadow.txt`). The audit closes the literal class
  as its resolution sees it, not every constant.
- `measured` is provenance, not command identity: `p = sh(["true"])` then
  `add(..., p.returncode, ...)` is `measured` while running nothing the state claims. The
  runner set is also matched by **call name**, so a locally defined function named `run`,
  `sh` or `git` is indistinguishable from the real runner (`tools/control-assertion-audit.py`
  selftest arm `measured-tuple-run` calls a local `run` stub; plan amendment A2 discloses
  it). The claim is that the value flows from a call the audit names as a runner, not that it
  ran the right command.
- The expectation is data by design, so a driver that sets `want = code` is a tautology the
  audit still reports green: the freeze-rev `controls98.py` with its `c2-nowork-absent`
  expectation changed to `g.returncode` prints `sites=15 measured=15 literal=0 unmeasured=0`,
  `rc=0` (wave artifact `.ufo/waves/round-98/w1/R98C1-c1-expectation-slot.txt`). The entry
  covers the recorded side; it does not close the comparison.
- The audit reads the blob at the resolved `--rev`; a worktree-only edit is not a subject of
  the verdict (wave fixture `R98E1-r05-classifier-attacks.txt` case_g: a worktree edit of the
  committed fixture leaves the line at `measured=no`).
- The audit's setup refusals (`rev-not-a-commit-id`, `rev-unresolvable`,
  `driver-absent-at-rev`, `driver-not-utf8`, `unparsable`, `add-without-code`) are source
  paths; at the freeze no committed receipt exercises them.

## 7. Evidence

- `.ufo/evidence/round-98/pre-freeze/c1-audit-r97-driver.out` (committed at `764aca97`) —
  the 15 sites, `line=156 … class=literal detail=constant`, `unmeasured=1`, `rc=1`.
- `.ufo/evidence/round-98/pre-freeze/c1-audit-controls98.out` — `measured=15 literal=0
  unmeasured=0`, `rc=0`.
- `.ufo/evidence/round-98/pre-freeze/c1-audit-selftest.out` — `CONTROL_ASSERT_SELFTEST:
  12/12 pass`, `rc=0`.
- `.ufo/evidence/round-98/pre-freeze/controls98-run.out` — `CONTROLS98 states=18 matched=18
  mismatched=0` at base `07e50d6d`; `pre-freeze/controls/c2-nowork-absent.out` — inner
  `rc=1`, outer `rc=1`; `pre-freeze/controls98-at-round-base.out` — the same driver with
  `--base 034240a5` prints `matched=16 mismatched=2`, the plan's disclosed limit (A1).
- The `CONTROLS98` line attests the round-97 instruments the driver executes from the lane
  worktree path (A1), not their blobs at the records revision; the byte-pinned statements
  belong to the audit and to the refusal battery.
