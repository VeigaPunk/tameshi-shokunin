# Round 48 report — draft of `## Work performed` and `## Landed changes`

Seat T48A2ScribeReportWork, draft only (the L1 writes the report). Every pointer below was resolved against the
lane checkout at `c7586b9a10effc63b4bd327f976edc094c1bdc17` plus the untracked `a2w1` report directory; every
commit named is in `git -C tameshi-shokunin log --format='%h %ci %s' 473336d9..`. Placeholders the L1 must fill
from the deciding receipts are marked `<PENDING>`, not guessed.

## Work performed

Declared claims (pre-registered at `e73389c0b47484cd007819cbf20a6e21c436f9ae` and `f1cfaad360130933983cac19f7036a8151f9054b`,
`.ufo/evidence/round-48/contract.json`, `amendments` 1-10, counter freeze `755298415f8c4eef3bed0c0d7625e2aacb03d6c2`),
two distinct axes, none exploratory: **C1 calibration** (the lowest non-retired axis, monitor 6) — the 22 frozen
statements of `.ufo/evidence/round-47/calibration/statements.json` are restated in SCORECARD.md section
`### Standing self-assessment — re-stated at round 48` from R=3 observation rounds of the six profiles P0-P5, each row
declaring a `stable`/`nondeterministic` value class, a tool sha256 prefix and a deps set, every value attested by the
counter's own observation in the same invocation (amendment 4), predicate `C1_R48_PASS` (`contract.json:82-95`);
**C2 freshness** (the round's sourced claim) — held rows S026, S048, S093, S108 superseded by S265-S268 opened
2026-10-26, with committed snapshots and fetch receipts, <=25-word `C2-QUOTE` Gate lines carrying the required
phrases, and the four citing knowledge entries re-pointed, predicate `C2_R48_PASS` (`contract.json:96-125`). Neither
claim was narrowed; no third claim, no assimilation (`corpus/lessons/round-48.md:8-9`).

- **Pre-registration, before any seat.** Contract with the two claims, their predicates, targets, kill rules, R=3 and
  the C1/C2 control definitions, plus the census-start receipt (`e73389c0`, `contract.json:82-126`); then amendments
  1-3 (C2 URL set for the S093 raw-vs-blob case, Gate-line grammar and extraction, row grammar incl. the `runs 3`
  skip rule) and the wave-1 spec, briefs and dispatch (`f1cfaad3`, `contract.json:9-26`). Census start:
  `scripts/sources-census.sh validate --root FLEET tameshi` exit 0 (`.ufo/evidence/round-48/census-start.exit`
  = `0`), with the base registry count 124 from the no-harm monitor
  (`before/no-harm-at-base.stdout`, `NOHARM registry-rows-not-below-124 124 ok`).
- **Counters built in wave 1, then frozen by the L1 (step 2) before any restated row, control score or deciding run.**
  `calibration/measure.py` sha256 `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` and
  `freshness/measure.py` sha256 `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f`
  (`freeze-2.json:12-24`), the C1 changes from the wave-1 counter recorded as `calibration/freeze-diff-vs-w1.patch`
  (amendments 4, 5, 7 implemented: in-invocation attestation, `FLEET` lines and `fleet_drift`, `BASE` pinned);
  selftests `C1_R48_SELFTEST: cases=76 failed=0` and `C2_R48_SELFTEST: cases=43 failed=0`
  (`selftest/c1-r48-selftest.stdout` then `VERDICT: PASS`; `selftest/c2-r48-selftest.stdout` last line; both exit 0); the control
  harnesses `control/run-controls.py` (CTL_A-E) and `control/c2-controls.py` (CTL_F-H), the deciding script
  `deciding-run.sh`, and the no-harm monitors at base, 8 of 8 ok (`before/no-harm-at-base.stdout`) with the cold-read
  count at base 60 (`before/coldread-sections-at-base.stdout`).
- **Amendments 4-10 are the wave-1 attack's product, recorded before any row, control score or deciding run.** The C1
  design critic's findings F1-F7 (self-attesting lane receipts, dependence-vs-value confusion, fleet/lane drift, the
  table-of-its-kind rule, base pinning, one deciding invocation, controls scored at the freeze) became amendments 4-9;
  amendment 10 records a declined proposal with its reason (`.ufo/waves/round-48/w1/T48CritC1Design.md`,
  `contract.json:27-68`). Two wave-1 reversals changed the round's reading of its own base tree:
  `hermetic env-differential probe`'s P1 `2/9` is `--work`-under-`/tmp` harness masking, not nondeterminism
  (`.ufo/waves/round-48/w1/T48RevenEnvDiff.md`), and `six-leg regression ledger` is genuinely nondeterministic (a
  one-sided SIGPIPE race under `pipefail` in the pinned tsukuroi leg,
  `.ufo/waves/round-48/w1/T48RevenRegression.md`).
- **Wave 1 was dispatched, crashed with the orchestrator, and is counted from its artifacts.** 32 seats
  (`.ufo/waves/round-48/spec-w1.json`: 11 executor, 4 critic, 4 scribe, 4 scout, 3 reviewer, 2 revenger, 2 connector,
  1 mutation-tester, 1 sentinel); the attempt-1 L1 died in the host crash of 2026-10-26 ~08:50 -03 before any results
  file was written, so the count rests on the dispatch file and the 24 seat reports (plus 2 unintegrated `.draft.md`
  files) under `.ufo/waves/round-48/w1/`. Attempt 1 scored no control and ran no deciding run
  (`LOG.md:2364`).
- **Attempt 1's unlanded LOG/QUALITY drafts and wave evidence were landed by the orchestrator, not by a round.** The
  salvage commit `15b1521ea2e95d0d708059458c090e9f334adf32` is recorded as "not a landed round" in its own subject and
  in `LOG.md:2359-2361`; the attempt-1 entry above it is kept as written and corrected by an appended entry, never
  rewritten.
- **C1 was observed, not asserted.** The counter's own `--emit` at the salvage tip ran three rounds over the six
  profiles for all 22 statements (54m41s, `.ufo/evidence/round-48/calibration/emit-15b1521.time`), printed the
  `STATEMENT`/`ROUND`/`PROFILES`/`EMIT_CAP`/`EMIT_AXIS` records the rows restate
  (`.ufo/evidence/round-48/calibration/emit-15b1521.stdout:1-118`), and exits 1 with
  `total=22 unparsed=22 ... C1_R48_PASS=false` on that tree because it carried no `runs 3` row yet — the `before`
  datum, not a verdict. Its `fleet_drift=1` is the counter's cleanliness pathspec `corpus`, `tools`, `SCORECARD.md`
  (`calibration/measure.py:376-380`) seeing the uncommitted round-48 record edits during the 55-minute run
  [INFERENCE: the edits that landed at `c7586b9a`]; the row values it prints are the ones the content revision
  restates. A second observation receipt from a wave-1 seat (round-47 counter emit at base) is committed at
  `calibration/observations/obs2-r47counter-base.emit.stdout` and is evidence for the report only — amendment 4 bars
  committed observation files from attesting a row.
- **C2's controls were scored at the frozen bytes, against scratch trees, and are receipts, not verdicts.**
  `control/c2-controls.py --measure freshness/measure.py` printed `CTL_F refreshed=0`, `CTL_G refreshed=0`,
  `CTL_H refreshed=2`, `CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true`, exit 0
  (`control/c2-controls.stdout`, `control/c2-controls.exit`); the meta line records the freeze bytes
  (`control/c2-controls.py` sha256 `46b8c039`, `freshness/measure.py` sha256 `faefe9b4`) and the revision each control
  was scored at — `473336d9` for CTL_F (BASE, no commit) and two throwaway commits in a `git clone -q --shared` of
  the lane at BASE for CTL_G and CTL_H (`control/c2-controls.meta`: `a865909b`, `b83f2424`; harness header
  `control/c2-controls.py:5-20`).
- **C2 records at the content revision.** Four rows appended — S265 (`corpus/SOURCES.md:140`), S266 (`:141`), S267
  (`:142`), S268 (`:143`) — each `docs`/`A` or `B`/`mined`, opened 2026-10-26, each `teaches` cell opening
  `supersedes T —`, each `anchor` cell carrying its snapshot digest
  (`a4c5c46b4af9`, `e9cbc3e1ab7c`, `2cb77df2f4be`, `04e4c091715a`); the four snapshots and receipts under
  `.ufo/evidence/round-48/freshness/sources/` (236387 / 8892 / 33289 / 111409 bytes, `http_status 200`,
  `fetched_at` 2026-10-26T08:40:42Z-08:41:18Z, receipt sha256 equal to the snapshot digest); the Gate block at
  `corpus/lessons/round-48.md:19-24` with one `C2-QUOTE` line per target, at 15 / 21 / 25 / 6 words; the four citing
  entries re-pointed with `source:` carrying the new row on line 1 and `verified-at: 2026-10-26` on line 2
  (`corpus/knowledge/repeated-control-precondition.md:1`, `incremental-pin-disposition.md:1`,
  `regression-tally-completeness.md:1-2`, `r8-golden-update-flag.md:1`).
- **Mistakes mined with red-before receipts.** The prospective-record mistake (attempt 1's QUALITY 94-96 block cited
  two receipts that did not exist at the revision that landed it) is stated at `corpus/lessons/round-48.md:356-361`
  with the criterion it produced (QUALITY 97, `corpus/QUALITY.md:1428-1434`); the attribution mistake (environment
  masking reported as host-load nondeterminism) at `corpus/lessons/round-48.md:350-355` (QUALITY 96); the red receipt
  is `quality/pointer-check-red-15b1521.stdout`, which prints two `MISSING` lines and exits 1 at the salvage tip
  (`checked=7 missing=2`) where the LOG block passes (`checked=8 missing=0`), and the checker's own selftest refuses a
  fixture with a missing path (`quality/pointer-check-selftest.stdout`, `cases=4 failed=0`).
- **Falsifiers for the new criteria.** `quality/falsifiers.sh` gives each of QUALITY 94-96 an input that must fail and
  one that must pass, printing `CRITERION-94-FALSIFIER-OK` etc. Block 95 reads
  `control/c1-controls.stdout` (`quality/falsifiers.sh:32-35`), so its receipt and the C1 controls' are the same
  object — see the pending line below.
- **Falsification wave `a2w1` (64 seats) at the content revision.** Dispatch validated and committed at
  `17cc5ce141868454d05bf75ef5cd230e35f0cdf4` (`.ufo/waves/round-48/spec-a2w1.json`: 19 executor, 12 reviewer,
  11 critic, 6 mutation-tester, 4 scout, 4 connector, 3 revenger, 3 scribe, 2 sentinel; the 32 falsify items prepared
  for the unrun `w2` in `.ufo/waves/round-48/w2-items.py`, patched where amendments 4-10 changed their premise, plus
  32 new items in `.ufo/waves/round-48/a2-items.py`). 38 of 64 seat reports had landed at 2026-10-26T10:46 -03
  (`ls .ufo/waves/round-48/a2w1/*.md | wc -l`), the wave still in flight; `<PENDING: final seat count, dead seats and
  the findings that changed records>`.
- **Pending at draft time, and not to be written up as measured.** The deciding run's receipts do not exist yet:
  `.ufo/evidence/round-48/after/` is absent (`ls .ufo/evidence/round-48/after` → No such file or directory), so
  `after/c1.stdout`, `after/c2.stdout`, `after/frozen.stdout`, `after/no-harm.stdout`, `after/coldread-sections.stdout`
  and `census-end.*` are all unwritten; and no `control/c1-controls.*` exists at the content revision
  (`git cat-file -e c7586b9a:.ufo/evidence/round-48/control/c1-controls.stdout` → `does not exist`), i.e. CTL_A-E are
  scored but not yet receipted, although QUALITY 95's falsifier (`corpus/QUALITY.md:1418`), the freeze plan and the
  LOG bullet (`LOG.md:2364`) all name that receipt. A probe of QUALITY 97 at the content revision
  (`quality/pointer-check.py --lane LANE --rev c7586b9a --file corpus/QUALITY.md --start "## Criteria appended — round 48"`)
  prints `POINTERS: checked=11 missing=2` and exit 1 for exactly those two paths, so criterion 97 stands unverified at
  `c7586b9a` until the receipts-only commit lands with them. `<PENDING: CTL_A-E lines, then the deciding values>`.
- **Hygiene.** No tool was installed or upgraded (pacman transactions are paused host-wide and nothing was needed); no
  lane `corpus/`, `tools/` or `SCORECARD.md` file was edited by a seat after the content revision — `git status
  --porcelain` in the lane prints only the wave directory `?? .ufo/waves/round-48/a2w1/` that every seat writes into
  and the orchestrator's dispatch marker `?? .ufo/waves/round-48/a2w1.ready.dispatched`, so no seat dirtied a checked
  path.

## Landed changes

Every change is tied to the round's LOG.md entries (`LOG.md:2348-2357`, the attempt-1 entry landed by salvage, and
`LOG.md:2359-2368`, the attempt-2 correction appended to it) and to the commit carrying it:

- `e73389c0b47484cd007819cbf20a6e21c436f9ae` — pre-registration: `.ufo/evidence/round-48/contract.json` (claims,
  predicates, targets, kill rules, controls, R=3), `census-start.*`.
- `f1cfaad360130933983cac19f7036a8151f9054b` — pre-data amendments 1-3, wave-1 spec `spec-w1.json`, the two counter
  briefs, `w1.ready` and `w1-dispatch.json`.
- `755298415f8c4eef3bed0c0d7625e2aacb03d6c2` — counter freeze (step 2): both counters, amendments 4-10, the
  `freeze-diff-vs-w1.patch`, both selftest receipts, `control/run-controls.py`, `control/c2-controls.py`,
  `deciding-run.sh`, `no-harm.sh`, the before receipts, `freeze-2.json`, `w2-items.py`, and the wave-1 evidence that
  had landed by then.
- `50545328e7ac4ba1703d70030e37dacec9362e68` — C2 records: rows S265-S268 in `corpus/SOURCES.md`, the four snapshots
  and fetch receipts, the four re-pointed entries, the lesson draft.
- `15b1521ea2e95d0d708059458c090e9f334adf32` — **not a landing**: the orchestrator's salvage of attempt-1's unlanded
  LOG/QUALITY drafts and wave/evidence files after the host crash (its own subject says so; `LOG.md:2361`).
- `41c1bc081c07900dd0127c86a61268e325872b57` — **outside the round's claims**: the fleet-level
  `considerthese/2026-10-26.md` daily reflection, committed in this lane's range but not a round-48 landing.
- `c7586b9a10effc63b4bd327f976edc094c1bdc17` — content revision (attempt 2, the deciding run reads this revision): the
  22 standing rows (19 capability rows `SCORECARD.md:2332-2350`, 3 axis rows `:2354-2356`) and the round-48
  SCORECARD block (`SCORECARD.md:2320-2367`), QUALITY 94-97
  (`corpus/QUALITY.md:1380-1434`), the integrated lesson (`corpus/lessons/round-48.md`), the LOG correction,
  `quality/pointer-check.py` with its selftest and red receipt, the `emit-15b1521.*` and observation receipts, the C2
  control receipts, and the a2 wave builder (`a2-items.py`, `build-spec-a2.py`).
- `17cc5ce141868454d05bf75ef5cd230e35f0cdf4` — `a2w1` wave spec and validated 64-seat dispatch at the content
  revision (`spec-a2w1.json`, `a2w1-dispatch.json`, `a2w1.ready`), `<PENDING: plus the a2w1 reports and receipts as
  they land>`.
- `<PENDING: the receipts-only commit — after/c1.stdout, after/c2.stdout, after/frozen.stdout, after/no-harm.stdout,
  after/coldread-sections.stdout, census-end.*, control/c1-controls.*>` — the deciding run is a single invocation at
  `c7586b9a` (amendment 8) and its receipts land in a receipts-only commit; at draft time it has not run.
