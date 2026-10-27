# Round 27 — cold-read monitor repair and frontier F8 (oracle anchoring)

L1 TameshiR27, attempt 1, 2026-10-22. Base `91edf9cd82ccc72e10f62f81d37181f549d593b8`.
Pre-registration `70df8d6a485418d9e57fed9d21e84fba71d4be66` (contract, both
counters, before-values, round-26 C2 correction); anchors and probe
`06a6707904582cc2f268d8a74861c6a8d09dd1fe`; content revision
`2227d8338c02aa9a5fd7d95c1a41b76865ad7647` (F8 entry, receipt, SOURCES, README,
QUALITY 53–54, counter amendment 1). Every cold read of this round is made at
the content revision.

## Claims

- **C1 calibration, harm repair.** SHONEN box 3 `[~]` cites the cold-read
  ledger; the strict monitor credited 25 of 64 sections at base, so box 3
  and the repo disagreed. Repair: independent seat cold reads of every
  uncovered section at `2227d83`, assembled into the round-21 ledger by
  append only. Counter `.ufo/evidence/round-27/c1-measure.py`.
- **C2 coverage, frontier F8, learning claim.** The four round-26
  cite-check hole survivors re-judged against expectations fixed outside the
  mutated code. Counter `.ufo/evidence/round-27/c2-measure.py`. Entry
  `corpus/knowledge/oracle-anchored-survivors.md`.

## Gate

Sources opened this round (ordinary fetch, 2026-10-22):

- **S012** (re-opened; row since round 1) — https://arxiv.org/abs/2608.17214,
  abstract. Quote (25 words): "An expectation is specification-anchored when
  composed from values fixed outside the code under mutation, and
  state-anchored when it flows, directly or transitively, from that code."
  Status `queued` → `mined`; used-by `—` →
  `corpus/knowledge/oracle-anchored-survivors.md`; opened and recheck cells
  unchanged (append-only rule). Decision: admit as the definition source for
  the F8 entry; its measured rates (one system, one author, tier B) are not
  used.
- **S090** (new) — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3,
  §ERRORS. Quote (17 words): "EX_USAGE (64) The command was used incorrectly,
  e.g., with the wrong number of arguments, a bad flag". Status `mined`,
  recheck 365d. Decision: admit as an outside anchor for a usage exit of 64.
  The page calls the interface legacy and deprecated; the entry uses it only
  as a fixed convention, not as a recommendation.
- **S091** (new) — https://git-scm.com/docs/gitrevisions, §SPECIFYING
  REVISIONS `<sha1>`. Quote (18 words): "The full SHA-1 object name (40-byte
  hexadecimal string), or a leading substring that is unique within the
  repository." Status `mined`, recheck 365d. Decision: admit as a
  convention anchor only; it speaks of Git object names, not content pins, and
  the entry says so.

Rejected reading: "anchored_holes=4 shows the round-26 differential method is
sound". It shows the four calls agree with outside anchors on one gate; the
other eight legs' hole calls are not anchored.

## Mistakes

1. **Harm-repair wave cancelled; record contradicted the monitor (round 26).**
   Class: calibration record. Evidence:
   `lessons/round-26-verifier-spotcheck.md:112-135` (62/62, restraint 8 →
   25/64, restraint 6) against SCORECARD's round-26 C2 row "numeric 8 → 8".
   Captured-by: QUALITY 40, already in force at `d4140796`
   (`corpus/QUALITY.md:364`), which covers asserting unchanged calibration
   without naming the lower score; it was not applied, although the lane had
   restraint 6 in a committed seat report one minute before the SCORECARD row
   landed (wave seat ScribeMistakes). Fix: QUALITY 53 and the frozen counter
   `.ufo/evidence/round-27/c1-measure.py`, shown able to fail: it exits 1 with
   `box3_mismatch=1` at base `91edf9cd` (`c1-before.stdout`); the SCORECARD
   row is corrected by an appended entry.
2. **Frozen counter check that only a contract breach could pass (this
   round).** Class: counter design. Evidence: `c2-measure.py` as frozen in
   `70df8d6` required S012's `opened` cell to read 2026-10-22, but CORPUS.md
   SOURCES contract rule 2 lets only status, recheck and used-by change in
   place. Captured-by: the SOURCES contract, read before the row was edited.
   Fix: `contract-amendment-1.json`, before any after-measurement; the target
   (`classified=4`) is unchanged and the amended counter still reads 0 at base
   (`c2-before-amended.stdout`).
3. **Registry run outside a fleet mirror (this round).** Class: measurement
   setup. Evidence: `tools/registry-check.py --rev 2227d83` from clones in
   directories with no `*-shokunin` siblings read `held=46/49`: the runner
   regression and two dependent rows refused with `repo_identity_mismatch …
   is not its own repository`, because the tool symlinks the siblings of the
   clone's parent directory (`tools/registry-check.py:770-782`). Captured-by:
   none. Fix: run it from a clone whose parent holds symlinks to every
   sibling (the mirror receipt is the one committed); the earlier readings are
   kept in this lesson, not in the receipts.
4. **Seat report written at the fleet root (misroot).** Class: write
   scope. Evidence: wave seat Read38 first wrote its report with a relative
   path, which landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-27/w1/Read38.md`;
   the seat moved it into the lane with `mv -n` and removed the two empty
   directories (its receipts 15–16; report `.ufo/waves/round-27/w1/Read38.md`).
   The L1 sweep (`git -C <fleet> status --porcelain`) found no tameshi file
   left at the fleet root. Captured-by: the wave context sentence on
   `Report:` trailer paths. Fix: none new; the context rule held for 50 of
   51 seats and the one miss was self-corrected and disclosed.
5. **Whole-tree `git status` under the trace collector.** Class: cold-read
   receipt hygiene. Evidence: seats Read05, Read17, Read24, Read29 and
   Read39 ran `git status` under the collector; the index refresh read every
   tracked file (5,853 inputs), and the assembler merges every listed
   receipt's inputs into the entry, so two entries carried `SCORECARD.md`,
   `LOG.md` and the round-21 ledger and would have drifted at the L1's later
   appends. Captured-by: the trial assembly (`assemble.py` before the
   append). Fix: the seats renamed those receipts `EXCLUDED-*.json` and
   dropped them from `traces`; the final assembly has no entry with those
   paths. Shown able to fail: the trial assembly listed the two entries with
   5,850 inputs each.
6. **One wave-1 report did not parse.** Seat Read08's JSON block fails
   (`Expecting ',' delimiter`, line 41), so `assemble.py` rejected it; its
   section was corrected and re-read in the residual call anyway.

## Wave findings (wave 1, 51 seats)

- **Cold reads: 39 sections read at `2227d83`.** 27 credited
  (assembled verdicts in `.ufo/evidence/round-27/coldread/assembled-w1.json`:
  `verified-record` 3, `gap-minor` 24; three more seats reported
  `verified-record` with minor gaps listed, which the assembler records as
  `gap-minor`); 12 failed (`gap-blocking` 1:
  Read09; `wrong-expectation` 11: Read03, 06, 07, 08, 10, 15, 25, 32, 34,
  37, 38). Each failing section was corrected in SKILL.md with a pointer to
  the seat, keeping every section's line count so the page's own line
  citations stay valid, and the 12 corrected sections went to a residual call
  of 8 fresh reviewer seats at `b1cc95e`.
- **C2 attacks.** CriticAnchors: `classified=4` is necessary, not
  sufficient; the counter cannot tell an anchored expectation from one copied
  off the pristine run, and S_PIN_INCLUDES is held by convention only.
  MutateC2Counter: all four counter mutants killed; a probe that compares
  with the pristine survives once its receipt is re-bound, and a hand-edited
  class label passes. Response: a negative-control run
  (`f8/probe-negative-control.stdout`, `anchored_holes=0`) and an honest
  anchor-strength count in the entry (3 header-anchored, 1 convention-only).
  ReviewEntry: faithful, one ambiguous slice wording (fixed). ReopenSources:
  S090 and S091 agree; S012's tier B is disputed (an original paper; the
  registry tiers similar papers A) — append-only, left for a supersedes row
  next round; S090's second teaches clause is a use note, not page text.
- **Records.** CriticRecordNoHarm: SCORECARD numbers match; the round-26
  correction cited no receipt for `40a12bf` (receipt now committed,
  `after/c1-measure-40a12bf.stdout`) and the round-27 block did not name
  amendment 1 (named in the measured results). ReviewQuality: QUALITY 53 and
  54 reproduce their falsifiers but need amendments (53: trigger reading and
  "independent" is not checkable by the counter; 54: naming a digest is not
  provenance, the counter never recomputes a class). QUALITY.md is a traced
  cold-read input, so the amendments are routed to round 28, not edited
  after the reads.
- **Open, routed.** `corpus/SOURCES.md:338` still says "Next unused id:
  S090" (seat RerunRegistryCensus); SOURCES.md is a traced input of many
  entries, so the one-line fix waits for a round that re-reads them. The
  README F8 row says "independently anchored", which the entry now bounds to
  3 of 4. Kumitate (owner, via the integrator): the round-26 routing of the
  four cite-check holes was dropped by kumitate R39-5 (seat
  ConnectorOverlap); kumitate's own `round-close-gate.md:204-206` is a second
  owner anchor for S_USAGE.
- **Next F8 move (seat ScoutLegAnchors).** Across the other eight recorded
  legs, 35 survivors: 17 have an explicit header or usage anchor, 6 a
  derived one, 12 none. Re-judge the 17 first; route the 12 to owners as
  differential holes.

## After measurement

At `af7b70daf7754f1d9363669cf9bc97ec01f61f9c` (fresh clone):

- C1: `C1_MONITOR: covered=60/64 restraint=6 box3_mismatch=1`, exit 1
  (`.ufo/evidence/round-27/after/c1-measure-af7b70d.stdout`). Target missed.
  Calibration is still harmed relative to round 26's base (restraint 8).
- C2: `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.
- Census end: exit 0. Registry at `2227d83`: `held=49/49 superseded=7`.

Lesson: the cold reads were worth more than the credit. They found 15 real
defects in SKILL.md text (12 in wave 1, 3 more in the residual reads, two of
them in the L1's own corrections). A correction made after a cold read needs
its own cold read; one residual call could not close that loop.
