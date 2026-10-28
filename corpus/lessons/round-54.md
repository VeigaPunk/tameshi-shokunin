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
- **The other 84 staged `merge/tameshi` entries** — REFUSED for the same capacity
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
  `git ls-tree -r` and proves the arm on the positive control CTL_POS_c1, which
  requires `rekeyed=7/7`; the control receipts are committed before the deciding
  run (`.ufo/evidence/round-54/control/`).

## QUALITY criterion (drafted; lands with the round commit)

- **105. A counter arm that reads a directory by pathspec is proven on a tree
  where the arm must fire (the positive control), not only on the do-nothing
  tree. Falsifier: a control receipt in which the arm's own counter reads a
  non-zero value; a pathspec that returns the directory itself is a defect even
  when the overall verdict is false for another reason.**

## The method (for the round report)

Round 53 lost the cold-read floor to a mechanism, not to prose: an entry credits
only while its pinned inputs still verify, so a re-key that pins `LOG.md` or
`SCORECARD.md` is stale one commit later, and a section whose bytes changed has
no matching entry at all. This round's repair is therefore ordering discipline:
all content edits land first (`c0`), readers read the final bytes, the entries
pin only artifacts those edits did not touch, and the deciding run re-derives
64/64 from the committed tree.
