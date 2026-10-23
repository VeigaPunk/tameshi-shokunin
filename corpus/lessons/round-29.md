# Round 29 — lesson (tameshi)

Base `367ec0f1d79cb9b67d724f2962e7554a0841b1fc` (round-28 spot-check head).
L1 TameshiR29, attempt 1 (repair-first round; driver block lifted 00:35Z).

Claims, frozen before data in `.ufo/evidence/round-29/contract.json`
(`9f3084bc`) and re-frozen before data after the control wave in
`contract-amendment-1.json` (C2) and `contract-amendment-2.json` (C1):

- **C1 calibration repair** (routed item 1 of
  `round-28-verifier-spotcheck.md`): `python3 .ufo/evidence/round-29/c1-measure-v2.py --repo CLONE --rev REV`,
  predicate `C1_R29_V2_PASS`. Base: covered 63/64, restraint 6, box3_mismatch 1.
- **C2 coverage, frontier F6** (never worked before; sourced on S024):
  `python3 .ufo/evidence/round-29/c2-measure-v2.py --repo CLONE --rev REV`,
  predicate `C2_F6_V2_PASS`. Base: fixture absent.

Round order (QUALITY 56): every widely read input edit (SOURCES S024,
README Round-29 section, QUALITY 55-57) landed in `9f3084bc` with the
contract, before any cold read; the cold reads target `9f3084bc`.

## Gate

- S024 re-opened: https://www.fuzzingbook.org/html/Reducer.html, fetched 2026-10-23T01:09Z with `curl -sL`, snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` sha256 3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99; located quote (section "Delta Debugging", after the MysteryRunner trace): "Its result is 1-minimal, meaning that every character contained is required to produce the error" (15 words).
- Change log: S024 `status` queued → mined; `used-by` — →
  `corpus/knowledge/survivor-fixture-minimization.md`. Tier B, kind `book`,
  recheck `365d` unchanged. No new row (URL already registered; QUALITY
  check from round-28 Mistake 2 applied: `grep -c fuzzingbook.org/html/Reducer corpus/SOURCES.md` → 1).
- S059 re-checked (routed item 2; seat ReopenS059, `.ufo/waves/round-29/w1/ReopenS059.md`):
  https://bazel.build/remote/caching fetched five times 2026-10-23 01:29–01:31Z, all
  `83f1c659…` (300387 B); the markdown alternate three times, all `266915c5…`. The HTML is
  deploy-keyed (`dpl_*` ids and hashed asset names change on each deploy; three digests
  in about 30 h), the markdown drifted once. Both row quotes are still verbatim in the live
  markdown. Because the stale digest sits in the immutable `anchor` cell, the fix is a
  supersedes row. It is **not** written this round: any SOURCES edit after `9f3084bc` would
  drift the cold-read credit this round restored (QUALITY 56). Routed to round 30 as the
  first SOURCES edit, before that round's content revision. No row status changed.

## Controls and redesign before data

- Control call 1 (6 seats, `.ufo/waves/round-29/ctl/`): C1 v1 controls K1-K4 did not meet
  it (CtlC1Cheap; K4 re-anchored old entries and gained one section of monitor credit, the
  binding check rejected it). Seat CriticC2Design met C2 v1 three ways (handwritten 2-unit
  fixture, external absolute census row with a host symlink, rewritten snapshot) → C2
  re-frozen as v2 (`contract-amendment-1.json`, `6ab11a62`). Seat CriticC1Design found the
  C1 v1 executable identity unpinned → C1 re-frozen as v2 (`contract-amendment-2.json`,
  `09e4f273`). CtlC1Shortcut and CtlC2Shortcut ended on a provider safety refusal (holds;
  error text in the report).
- Control call 2 (2 seats): CtlC2v2Port's seven controls did not meet v2. CriticC2v2's
  report (Q5: target unreachable) landed at 01:33:57Z, after the wave-1 dispatch at
  01:27:45Z; see Mistake 1.

## After measurement

- C1: `python3 .ufo/evidence/round-29/c1-measure-v2.py --repo CLONE --rev REV`
  base `367ec0f1` → `covered=63/64 restraint=6 box3_mismatch=1`, PASS false;
  `9f3084bc` (all input edits) → 52/64; `bc2058a4` (22 bound entries appended, ledger
  371 → 393) and `7a45f7b9` → `covered=64/64 restraint=8 box3_mismatch=0 appended=22
  bound=22 prefix_equal=1`, `PREDICATE: C1_R29_V2_PASS=true`, exit 0
  (`.ufo/evidence/round-29/c1-at-D.stdout`, `c1-at-E.stdout`). 36 readers, 34 reports
  assembled into 32 entries (two pairs merged), 2 rejected by the assembler on format
  (Read07A non-hex input digest, Read10B a URL in `external_inputs`). No read failed.
  Post-data integration step: `coldread/select-bound.py` kept the 22 entries that meet the
  frozen binding check and excluded 10 passing entries (4 seats wrote their full agent id as
  `seat`; 6 entries carry the assembler's normalized verdict, not the report's). Dry run of
  all 32: 64/64 but `bound=22`, PASS false (`coldread/c1-dry-all32.txt`). Excluding passing
  entries cannot raise coverage; the excluded list is `coldread/select-receipt-w1.json`.
- C2: `python3 .ufo/evidence/round-29/c2-measure-v2.py --repo CLONE --rev REV` at
  `7a45f7b9` → `fixture=present anchored=1 kill_original=0 units_original=105
  units_minimized=105 ddmin_match=0 kill=0 one_minimal=0`, PASS false. **Missed (honest
  stop).** The target is unreachable under the pinned declaration: all three exec rows
  declare 755, so the B5 mutant fails the exact-mode check for any file lacking the
  execute bit (BuildF6B: 512-mode sweep over the three rows, no killing state;
  CriticC2v2 Q5). Recorded as knowledge in `corpus/knowledge/survivor-fixture-minimization.md`.
- Census at the lane head: exit 0, `tameshi ok`, the same seven W04 warnings
  (`.ufo/evidence/round-29/census-E.stdout`). At `9f3084bc` the census exited 1 (E11, S024
  `used-by` named a file not yet landed; Mistake 2).

## Mistakes

1. **class:** data dispatched before the control call settled. **evidence:** seat
   CriticC2v2 ended "without a final message" and was taken as dead; its report
   `.ufo/waves/round-29/ctl/CriticC2v2.md` (mtime 22:33:57-03) proves the C2 v2 target
   unreachable, and landed after the wave-1 dispatch record `.ufo/waves/round-29/task-adapter-w1.json`
   (22:27:45-03). The BuildF6 seats then spent the wave on an unreachable target; C2 missed.
   **captured-by:** the orchestrator's pre-freeze control rule (controls scored before data)
   — not applied, because the L1 did not wait for the report file. **fix:** before any data
   dispatch, every control seat either has its report file at its path or is recorded dead
   with its error text after a final check of that path; and each frozen target carries a
   committed reachability witness (one hand-built instance that meets it, or a stated proof).
   Shown able to fail: `stat -c %Y` of `CriticC2v2.md` is later than that of
   `task-adapter-w1.json`, so the check fails for round 29.
2. **class:** pre-registered `used-by` pointing at a file not yet landed. **evidence:**
   S024 `used-by` named `corpus/knowledge/survivor-fixture-minimization.md` at `9f3084bc`,
   where the file did not exist: census exit 1 (`E11 S024 missing used-by …`), registry row
   `sources-census` `expect=0 got=1` (seats RerunCensusA, RegistryNoHarm). Cold readers of
   sections that run the census read a red lane at the content revision. **captured-by:**
   census E11 (it fired). **fix:** a SOURCES `used-by` change lands in the same commit as the
   file it names. Shown able to fail: the census at `9f3084bc` exits 1 (`RerunCensusA.md`).
3. **class:** misrooted seat report. **evidence:** Read10C wrote
   `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/w1/Read10C.md` at the fleet root
   despite the absolute-path rule; the L1 found it because the first dry assembly lacked a
   Round-18 entry from a seat that reported done. Copied byte-exact into the lane (sha256
   `fafd4c3698e38009f7742352600b9aaf6d220145ed5543549e375cc8a34b03e8`), `cmp` clean, fleet copy
   deleted. **captured-by:** the misroot sweep. **fix:** before assembly, compare the report
   files present with the registry members that returned; a gap triggers the sweep. Shown able
   to fail: the 01:3xZ dry assembly listed 11 entries with Read10C absent.
4. **class:** seat containment breach. **evidence:** BuildF6B killed PID 2758108 and two
   children belonging to BuildF6A (matched by `pgrep`, cwd not checked;
   `.ufo/waves/round-29/w1/BuildF6B.md`). BuildF6A wrote no report and was cancelled at the
   wave deadline. **captured-by:** none (the wave context said "kill any process tree you
   started" but not "never kill one you did not start"). **fix:** the residual context of
   this round adds "Never kill a process you did not start (check /proc/<pid>/cwd first)".
   Shown able to fail: the wave-1 context (`spec-w1.json` key `context`) lacks that sentence.
5. **class:** binding check frozen without checking the assembler's output shape.
   **evidence:** 10 of 32 passing entries fail the frozen C1 binding (seat self-labels;
   assembler verdict normalization and report merging), `coldread/c1-dry-all32.txt`.
   **captured-by:** none. **fix:** a binding check is run on one real assembled entry before
   it is frozen, and the wave context fixes the `seat` label to the registry name. Shown able
   to fail: `select-receipt-w1.json` lists the 10.

## Routed defects of round-28-verifier-spotcheck.md

1. C1 remainder → done: `C1_R29_V2_PASS=true` at `7a45f7b9` (64/64, restraint 8, box3_mismatch 0).
2. S059 digests → re-checked (above); supersedes row routed to round 30 as its first SOURCES edit.
3. Close against one head → QUALITY 57 (`9f3084bc`); this round's report names its final head
   and no lane commit lands after it.
4. Round-27 items: 4 (README F8 wording) → README Round-29 section; 5 (QUALITY 53/54) →
   QUALITY 55; 6 (runner `--regression` leg sum) → defect confirmed by seat MutateLegSum
   (dropping one status from the tally prints `PASS (cases=9 passed=8 …)`, exit 0; selftest
   97/97 does not catch it; unapplied diff in `.ufo/waves/round-29/w1/MutateLegSum.md`). Not
   applied: `tools/mutate-and-run.sh` is an input of most credited cold-read entries, so the
   fix must open a round's content revision. Routed to round 30.

Known imprecision at `9f3084bc` (seat ReviewR1Edits): README `:443-444` and QUALITY 55 name
the v1 counters (`c2-measure.py`, `c1-measure.py`); both were superseded before data by the
v2 counters. Not corrected this round (input files; QUALITY 56).

## Residual review (8 seats, `.ufo/waves/round-29/res/`)

- RerunC1Head: `C1_R29_V2_PASS=true` reproduced at `7a45f7b9` and `9bb699ad`; base 63/64
  restraint 6; counter digest equals contract-amendment-2; ledger diff `1781 0`. Agree.
- CriticSelectBound: C1 verifies with a disclosed bound; no failing verdict excluded;
  Read07A and Read10B are format rejects. Agree; the bound stays in SCORECARD and here.
- SampleBoundReads: 4 of 22 appended entries re-checked (Read01A, Read03B, Read04C,
  Read10C), all hold; Read10C's moved report sha256 matches.
- RerunC2Head: miss confirmed structural; amendment committed before data. Agree.
- CriticNoHarm: depth 9 → 9; registry rows checked hold at base and head; census warnings
  unchanged; no protected path edited after `9f3084bc`. Agree.
- ReviewControls: partial pass — both counters re-frozen before data, but wave 1 left before
  CriticC2v2 settled (Mistake 1), and CtlC2Shortcut's refusal hold was first recorded in this
  lesson, not in an amendment; the shortcut control class was never scored for either claim
  (both seats refused). Agree; recorded here as a disagreement with the round's own
  process, not repaired after data.
- ReviewEntryF6: entry accurate in substance; five wording defects (mode `-` was "only",
  byte vs unit copy, the S024 assert, a missing counter field, the round-3 receipt). Four
  corrected in the entry after review; the round-3 receipt is absent at the head and the
  entry now cites only the kaika probe.
- ReviewLessonGate: reviewed the 27-line draft before the lesson landed (Gate passes; it
  found `## Mistakes` absent at that time). Its disagreement on routed item 2 (supersedes
  row not written) stands; the deferral reason is in `## Gate`.

Late seat: BuildF6A was cancelled at the wave deadline (02:47Z) but its report and fixtures
landed at 02:58Z (`.ufo/waves/round-29/w1/BuildF6A.md`, `.ufo/evidence/round-29/f6/BuildF6A/`).
It agrees the anchored target is unreachable (anchored variant: 98 units, `kill_original=0`).
Its other variant, the pinned declaration plus one probe row, reduces 100 → 2 units with
`kill=1 one_minimal=1 ddmin_match=1` but `anchored=0`, so it does not meet the frozen C2
predicate and is not counted. It is the reachable starting point for the next F6 round.
