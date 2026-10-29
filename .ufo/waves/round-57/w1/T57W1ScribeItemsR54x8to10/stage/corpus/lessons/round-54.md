# Tameshi round 54 — cold-read floor repair, one scratch-root exit class

L1 TameshiR54a2, hyaku run 11, attempt 2 (attempt 1 left nothing behind: no
`.ufo/waves/round-54/`, no evidence dir, clean tree — nothing inherited).
Base `d33053f7`, the round-53 closure tip. Claims frozen at `441c26be`
(`.ufo/evidence/round-54/contract.json`, `freeze.json`), before any seat ran.
The round carries the round-53 closure's honest stop forward: calibration is the
lowest non-retired axis (8) and C1 repairs the cold-read floor that round 53
left at 57 of 64 credited.

## Gate

Rows opened this round (CORPUS.md SOURCES contract v1 rule 1):

- **S277** — POSIX.1-2024, Base Definitions §8.1 Environment Variables
  (TMPDIR), `https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html`,
  opened 2026-10-28 by L1 TameshiR54a2 (HTTP 200, 33758 B text-extracted,
  sha256 `89294048…`, snapshot
  `.ufo/evidence/round-54/assimilation/S277-posix-env.html`). Located quote
  (21 words, §8.1 TMPDIR paragraph): "TMPDIR This variable shall represent a
  pathname of a directory made available for programs that need a place to
  create temporary files".
- **S278** — CPython 3.12.7 `Lib/tempfile.py`, `_candidate_tempdir_list`,
  `https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py`,
  opened 2026-10-28 by L1 TameshiR54a2 (HTTP 200, sha256 `fb44155f…`,
  snapshot `.ufo/evidence/round-54/assimilation/S278-tempfile.py`). Located
  quote (5 words, :163-165): "if dirname: dirlist.append(dirname)" — the empty
  value never becomes a candidate, so `TMPDIR=""` behaves as unset.
- **S279** — Python 3 documentation, `tempfile` — Generate temporary files and
  directories, `https://docs.python.org/3/library/tempfile.html`, opened
  2026-10-28 by L1 TameshiR54a2 (HTTP 200, 20462 B text-extracted, sha256
  `6b0edccf…`, snapshot
  `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html`). Located quote
  (11 words, §tempfile.gettempdir): "The directory named by the TMPDIR
  environment variable" — the first entry of the documented search list.

Admits (this round's set): all three rows are cited by one admitted note,
`corpus/knowledge/scratch-root-contract.md`, which states the three arms and
says explicitly that the empty arm is a lane declaration following the resolver,
because S277 fixes only the variable's meaning. Province: verification-fixture
craft (a gate's scratch root and exit class) — in scope. QUALITY bar: each claim
in the note cites its row with a located quote; no claim outruns its source.

Rejects (this round's set):

- **merge/tameshi's `delta-debugging-minimization-contract.md`** — REFUSED this
  round on capacity, not merit: §10 takes one theme and 1–3 entries, and this
  round's centre of gravity is the C1 floor repair plus the C2 exit class. Flip:
  it is the next-ranked entry for round 55 (its subject, a stated minimality
  witness, matches the round-50 shrinker's `cannot_see` line).
- **The other 80 staged `merge/tameshi` entries** — REFUSED for the same capacity
  reason; they stay reserved by document.

Assimilation verdict: one theme (the scratch-root contract) with three rows and
one note; the delta-debugging theme is refused above with its flip condition.

considerthese mining: `considerthese/2026-10-28.md` proposal 1 (the contract-debt
table: which SCORECARD contract sections are placeholders and for how long) is
mined into this round's SCORECARD `planned` line and the report's stale-lane
line rather than acted on; proposals 2–5 remain unmined (at most one per round).

## Mistakes

- **class: a bounded counter arm left structurally dead by a pathspec.**
  evidence: round 53's frozen C1 counter listed the re-key directory with
  `git ls-tree --name-only REV .ufo/evidence/round-21/coldread` (no trailing
  slash), which returns the directory itself, so `rekeyed` was `0/30` at every
  revision and every committed mutation-test receipt was INCONCLUSIVE
  (`.ufo/evidence/round-53/c1/measure.py`; routed as R53.1 by
  `corpus/lessons/round-53-verifier-spotcheck.md`). captured-by: none — the
  counter had no arm-level self-test, and the round-53 control scored the
  do-nothing tree (which fails for other reasons), so a dead arm looked
  healthy. fix: this round's counter lists the re-key directory with
  `git ls-tree -r` and the arm's own count is read at the deciding revision
  (7 of 7); the control pre-registered in phase B was cloned at the freeze
  commit, printed `CTL_MISMATCH` (3 of 7) and therefore never fired
  [ER-R54-1, round-55 correction]; the control receipts are committed under
  `.ufo/evidence/round-54/control/`.

## QUALITY criterion (drafted; lands with the round commit)

- **105. A counter arm that reads a directory by pathspec is proven on a tree
  where the arm must fire (the positive control), not only on the do-nothing
  tree. Falsifier: a control receipt in which the arm's own counter reads zero
  (the arm never fired); a pathspec that returns the directory itself is a
  defect even when the overall verdict is false for another reason.**

## The method (for the round report)

Round 53 lost the cold-read floor to a mechanism, not to prose: an entry credits
only while its pinned inputs still verify, so a re-key that pins `LOG.md` or
`SCORECARD.md` is stale one commit later, and a section whose bytes changed has
no matching entry at all. This round's repair is therefore ordering discipline:
all content edits land first (`c0`), readers read the final bytes, the entries
pin only artifacts those edits did not touch, and the deciding run re-derives
64/64 from the committed tree.

## Round-53 routed defects — dispositions (this round)

- **R53.1** (the frozen round-53 C1 counter's rekey arm was dead) — FIXED: this
  round's counter lists the re-key directory with `git ls-tree -r` (a recursive
  listing, so the directory's own name cannot shadow the match), and the arm
  reads 7 of 7 at the deciding revision; the control
  pre-registered in phase B was cloned at the freeze commit and printed
  `CTL_MISMATCH` (3 of 7), so it never fired [ER-R54-1, round-55 correction].
  The dead arm's own receipt is kept:
  `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`
  (`rekeyed=0/30` at the round-53 final revision). QUALITY 105 lands with it.
- **R53.2** (deciding receipts never committed) — FIXED by construction: this
  round's deciding run writes `.ufo/evidence/round-54/after/` and the report
  cites the receipts from there; nothing is quoted in past tense before it runs.
- **R53.3** (phase-B controls unbacked) — FIXED: `control/controls-b.stdout` and
  `controls-b.exit` are committed before the deciding run, which refuses to run
  without them.
- **R53.4** (a receipt anchored at a revision absent from the object DB) — FIXED:
  every receipt this round names revisions resolved in the lane's own object
  store, and the C2 counter runs the tool bytes from a clone of the lane at REV.
- **R53.5** (stale freeze receipts) — FIXED: `freeze.json` is regenerated at
  freeze time and the deciding run prints `FROZEN_UNCHANGED=1` against it; no
  amendment is recorded.
- **R53.6** (the CR47 exit class missing in four of seven tools) — FIXED by C2:
  the four now raise `ScratchRootUnusable` and map it to exit 2 with a naming
  line; the C2 counter's unusable arm is 7/7.
- **R53.7** ("inputs pinned at C7" was imprecise) — FIXED: the binder records
  `read_rev` (the read commit, C0) and the pin revision (PIN) separately, in the
  trace's `rev_reason` and in `refresh-receipts.json`; the report states both.
- **R53.8** (the S275 page locator) — FIXED: the quote was located this round on
  physical page 3 of the committed camera-ready snapshot (printed footer 1787),
  and the `p. 4` cells in `corpus/SOURCES.md` and
  `corpus/knowledge/change-aware-resweep-cadence.md` now read `p. 3 (physical)`.
  The round-53 lesson's own line is left as the historical record (errata are
  append-only); this entry is the correction.
- **R53.9** (six round-53 wave files untracked at the push tip) — CLOSED: all six
  are tracked in the lane at this round's base (`git ls-files` names each), so
  nothing was carried in uncommitted.

## Round-54 routed defects — corrections (round 55)

- **R54.8** — the `~/.omp/agent/config.yml` write is recorded in this lesson:
  seat `T54W1ExecStraceNoise` changed `scout` from `@m_grok` to `@m_glm53` outside
  its write scope, and the change was reverted. The report's word *fabricated* is
  withdrawn. The full record is `corpus/lessons/round-55.md` (R54.8 row) and SCORECARD
  `ER-R54-8`; the seat file is marked superseded.
