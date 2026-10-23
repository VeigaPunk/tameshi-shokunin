# Round 33 — lesson (tameshi)

Base `66e1fb444615b3afe380e7df0244ef7fae1dd985` (round-32 spot-check head). L1 TameshiR33, attempt 2
(attempt 1 died with the phase-4 orchestrator, no report; working tree was clean, nothing inherited).
Round order: freeze `f6d8a891` (C1 tool v2 + counters + contract, before-values, dev selftest 21/21) →
wave 1 (33 seats via the orchestrator: 4 controls, 12 dev sweeps, 8 reviews, 2 panel checks, frontier
source seats) → amendment 1 `27902a16` (counter --receipt fix) → amendment 2 `e6a5f4b` (c2 hardening) →
amendment 3+4 `49876298` (tool pre-data hardening from seven converging seats + counter boundary/gate
repairs + contract kill-rule sentences) → amendment 5 (DevHead twice-only head rule: 19/35 survivors killed,
validated on all 35) → content `this commit` (C2 landing, records) → measurement
runs below. No wave 2 was dispatched: at the 2 h freeze the orchestrator directed an honest landing;
C1's sealed held-out set was never authored, so C1 was not measured (honest stop, routed to round 34).

## Gate

Sources opened this round:

- **S100** (new; seats SrcDoctestReopen + ReviewSrcDoctest): https://docs.python.org/3.15/library/doctest.html,
  accessed 2026-10-23 UTC, 216574 bytes, sha256 `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899`
  (committed snapshot `.ufo/evidence/round-33/c2/doctest-snapshot.html`; fetch receipt records two fetches
  byte-identical at freeze time). Quote (module introduction, first bullet, lines 245-246 of the page,
  17 words): "The doctest module searches for pieces of text that look like interactive Python sessions".
  Gate pin: the digest is verified against the COMMITTED snapshot, never a live re-fetch — both seats
  observed the live page's generated footer clock move (18:17Z vs 18:41Z) with everything else identical;
  the /3/ alias S055 names drifted the same way in round 31. `teaches` opens `supersedes S055 -`.
- **S099** (re-opened; seat SrcPitestReopen): https://pitest.org/, accessed 2026-10-23 UTC, HTTP 200,
  12023 bytes, sha256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc` — byte-identical
  to the round-32 Gate digest. Quote (section "What?", HTML lines 121-122, 19 words, distinct from the
  round-32 quote which is still present at line 114): unchanged-source recheck, no row change.

Rejections:

- Live-digest pins for python docs pages (S055's original /3/ form and even the versioned 3.15 build's
  live bytes): rejected as pin targets — the generated footer makes live digests unstable within the
  round; committed snapshot bytes are the pin (ReviewSrcDoctest, SrcDoctestReopen).
- The C1 measurement: rejected by the L1 at the freeze mark — the sealed held-out set (predicate
  conjunct: >=8 must-kill + >=6 must-accept authored after the tool freeze) does not exist; running
  the counter would print `ho_kill=0/0 ho_accept=0/0 ... C1_R33_PASS=false`, a structural false that
  spends the kill rule on a missing fixture instead of the tool.

Row changes, old → new (`corpus/SOURCES.md`, rows 96 → 97): S100 added (mined; used-by
`corpus/lessons/round-33.md`, `corpus/knowledge/executable-self-assessment.md`). No other cell changed.

## What the wave-1 seats found (all pre-data; fixes in amendment 3+4 unless marked routed)

- **Controls (4 seats, all caught)**: do-nothing (kill 0/18), always-pass (0/18), always-fail
  (accept 0/8), sha-only (accept 1/8 — seven of eight must-accept copies are byte-different
  behavior-preserving rewrites, so a digest compare passes them; CtlShaOnly). Each control also
  reported counter interface defects; amendment 1 fixed them before any data run.
- **DevHead**: 19/35 head mutants survived — every post-capture leg-status write not line-initial
  (`(( st_x = 0 ))`, `printf -v`, `read`, `unset`, wrapping) escaped line-anchored scans; the twice-only
  rule (each leg name appears exactly twice in the head: the `local` declaration and its bare `st_x=$?`)
  kills all 35, pristine and selftest 21/21 green.
- **DevGuard**: five surviving config-conjunct guards (`&& $KEEP -eq 1` etc.) — the audit driver
  pinned `auto=0 KEEP=1` while the runner's real default is `auto=1 KEEP=0`. Fix: every vector under
  both configs; replayed, all five die.
- **DevHarness**: five harness-region weakenings (deleted status-1/status-2 tvec entries, loosened
  line match, dropped all-pass case, `rc -ge`) passed the panel; runtime still backstopped them
  (quantified), but the panel now carries a fault per weakening. Plus one false reject (unquoted
  second extraction line) — regex fixed.
- **DevStderr**: stdout-only rule enforced (12/13 kills; 7/7 equivalents; 0 false rejects); one
  escape into SETUP via an embedded-CR fake record (kill copies that crash the tool's parser score
  a miss, not a kill) — routed: per-index record parsing.
- **CriticTool**: a nested-function wrapper masks ALL tally exits (the audit truncated run_regression
  at the first `\n}\n` and never tested the outer exit) — fixed with nesting-aware extraction plus
  tally-block depth and postamble checks; renamed loop variables and `while`/`until` traversals were
  refused — fixed by case-subject dataflow identification. Quoted `case "$st"` and helper-function
  refactors still refused — routed.
- **ReviewTool** (full round-32 sealed 22-set replay): 17/22 correct; FALSE-PASS x2 (Guard-2
  divisibility class; TallyArms-02 126+127 coexistence) and FALSE-SETUP x3 (helper/quoted/arithmetic
  case subjects). The two false-pass classes need a doubled-status panel stress and coexistence
  vectors — routed. False-setup overlaps CriticTool/DevLoopOps — partially fixed, rest routed.
- **DevArm/DevLoopOps/DevNlegs/DevMulti** (four seats, one convergence): no generated vector ever
  combined a status >=3 with another non-zero leg — 16+ survivors across arms, skips, nlegs
  recomputions, all die on co-occurrence vectors. Fix: every unordered position pair x every ordered
  status pair over {1,2,3,4,5,7,9,120,126,127,128,255} (runtime now ~6 s, 15158 vectors x 2 configs).
- **DevAccept**: one false reject (head-local rename of `auto` collides with the synthetic driver
  preamble) — routed: seed the preamble from head-declared locals.
- **CriticCounter/SentinelSandbox/ReviewCounterA/DevStderr(adjacent)**: the execution boundary was
  docstring-only (v1.run_tool ran the auditor with no bwrap) and block_run could not exec `timeout`
  inside its own sandbox (no runtime mounts) — every witness run failed closed, which would have
  structurally failed C1 at measurement. Fixed with read-only runtime mounts and timeout outside the
  sandbox; controls gate now requires non-empty controls all predicate_pass=false; witness vectors
  must name all 9 legs.
- **ReviewContract/ReviewFreeze/ReviewCounterA/ReviewCounterB/LedgerAudit/PanelCheckA/B**: contract
  kill-rule sentences written (deciding run, measurement revision, seat re-runs are observations);
  freeze conformance clean; panel calibrated (v1 and v2 tools both 18/18, 8/8 under four seeds);
  c2 counter hardened (Gate-scoped digest + row id + URL binding); monitor baseline 64/64 restraint 8.
- **ConnectorOverlap**: three sibling adjacency imports catalogued (mado/kotoba/kake waves) with a
  projection-aware paired-witness card proposed for r34; no ownership transfer.

## Mistakes

1. **class:** shipping a counter whose documented flag did not exist. **evidence:** the four control
   seats all hit `unrecognized arguments: --receipt` at the freeze. **captured-by:** none (the L1
   smoke-tested controls mode only with the default receipt path). **fix:** amendment 1, disclosed;
   shown able to fail by the seats' frozen-byte receipts (exit 2).
2. **class:** docstring claiming a sandbox the code did not implement. **evidence:** v1.run_tool ran
   the auditor outside bwrap; block_run execvp'd `timeout` inside a mount-less sandbox — four
   independent seats. **captured-by:** none (the r32 closure did not test the boundary either).
   **fix:** amendment 3 boundary repair; shown able to fail by the frozen-boundary witness runs
   (rc=1 for pristine and mutant alike) and the repaired runs in `.ufo/evidence/round-33/dev/`.
3. **class:** a coverage hole seven seats converged on independently. **evidence:** DevArm/DevLoopOps/
   DevNlegs/DevMulti survivor batteries; DevGuard's driver-pin class; ReviewTool's replay. **captured-by:**
   none — the v2 design repeated v1's single-status-at-position-0 sweep with more positions, never
   questioning co-occurrence. **fix:** co-occurrence vectors + dual-config sweep; shown able to fail
   by each seat's pre-fix survivor and post-fix replay (DevGuard's five re-run).
4. **class:** a round plan whose critical path (wave 2) could not fit the session budget. **evidence:**
   at the 2 h mark, wave 1 had produced 7 amendment-driving findings and no sealed set existed.
   **captured-by:** the orchestrator's clock directive. **fix:** honest-stop landing: C2 measured, C1
   frozen-and-hardened with the measurement routed, every finding committed as evidence; r34's first
   wave authors the sealed set against the amended tool.

## Holds (routed to round 34)

- C1 measurement: author the sealed held-out set against tool sha `7a59f576…8833` (amendment 3),
  mint the controls receipt at the measurement revision, run the counter. v3 tool classes if any
  seat finds another survivor: Guard-2 divisibility, TallyArms-02 coexistence, quoted case subject,
  helper-function refactors, per-index record parsing, preamble seeding, all-pairs nlegs recompute.
- Cold-read re-crediting: this lesson + the SCORECARD/LOG/SOURCES appends drift monitor sections;
  r34's first wave re-reads them (LedgerAudit sized ~19 SOURCES-citing sections + 3 all-four).
- Dead seats: none in wave 1 (33/33 returned). Round total: 33 seats, one wave, no residual call.

Misroot sweep: no seat files landed at the fleet root (checked at report time).
