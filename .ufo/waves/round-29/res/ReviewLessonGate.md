# ReviewLessonGate — round-29 lesson review (RESIDUAL falsify seat)

Reviewed `corpus/lessons/round-29.md` as it stands in the lane working tree.
Lane head: `7a45f7b9d6a2542a553276330c8b02ac2e28c7ef` (E). The lesson file is
**untracked** (`git status` shows `?? corpus/lessons/round-29.md`);
`git show master:corpus/lessons/round-29.md` fails with "exists on disk, but
not in 'master'", so there is no committed version to diff against — the
working-tree file is the only review object. It is a partial draft: **27
lines, 10131 bytes, mtime 2026-10-22 23:49:10 -0300**, ending inside
`## Gate`. Also untracked and presumably still in flight:
`.ufo/evidence/round-29/c1-at-E.stdout`, `c2-at-E.stdout`, `census-E.stdout`,
`.ufo/evidence/round-29/f6/BuildF6A/`.

## Verdict

**INCOMPLETE — Gate check passes; `## Mistakes` and the routed-defect
dispositions are absent.** Everything present checks out; the file is a
stub of the required deliverable, not a finished lesson.

## (1) Gate — S024 row change and snapshot quote: PASS

- `git diff 367ec0f1 9f3084bc -- corpus/SOURCES.md` is a single-line edit
  (`corpus/SOURCES.md:35`): `status` `queued` → `mined`, `used-by` `—` →
  `corpus/knowledge/survivor-fixture-minimization.md`. Lesson
  `round-29.md:24-25` describes exactly this ("`status` queued → mined;
  `used-by` — → `corpus/knowledge/survivor-fixture-minimization.md`").
  Tier `book`/B and recheck `365d` unchanged, as claimed (line 25-26).
  `corpus/knowledge/survivor-fixture-minimization.md` exists (committed in
  `7a45f7b` per its commit message).
- No new row: `grep -c 'fuzzingbook.org/html/Reducer' corpus/SOURCES.md`
  → 1, matching the lesson's stated check (line 27).
- Snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`
  exists; `sha256sum` =
  `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99`,
  matching line 23. File mtime `Oct 22 22:09` local (-03:00) =
  `2026-10-23T01:09Z`, matching the claimed fetch time.
- Located-quote check: literal `grep -F` for "Its result is 1-minimal,
  meaning that every character contained is required to produce the error"
  returns **0** in the raw file because the snapshot marks up
  `<em>1-minimal</em>` and uses `\xa0` for "29\xa0steps". After tag-stripping
  and unescaping, the quote is **verbatim at byte offset 251323**, right
  where the lesson says ("section 'Delta Debugging', after the
  MysteryRunner trace"). 15 words, ≤25. See LOW-1.
- LOW-1 (`corpus/lessons/round-29.md:23`): the lesson's quote is verbatim
  in the *rendered text* of the snapshot but is **not a contiguous byte
  string** in the raw HTML (the saved source inserts `</em>,` inside it).
  Any verifier running `grep -F` on the snapshot gets 0. Smallest fix:
  note "(markup-stripped)" beside the quote, or pick the contiguous byte
  fragment after `</em>, `.
- LOW-2 (`corpus/SOURCES.md:35`): the S024 locator still reads "fetched
  2026-10-19" although the round re-fetched on 2026-10-23T01:09Z; the
  lesson itself records the re-fetch. Not required by the gate diff, but
  the row's provenance cell is stale. (Same staleness class as round-28
  Mistake 2's date discipline.)

## (2) `## Mistakes` rows: ABSENT — nothing to verify

The file ends at line 27 inside `## Gate`. There is no `## Mistakes`
section, so no row exists to check for class / evidence pointer /
captured-by / fix-able-to-fail. Nothing to re-run; zero rows named a
failing-case command.

## (3) Dispositions for `round-28-verifier-spotcheck.md` routed items 1–4:
no disposition text exists yet

The lesson contains no routed-defect section. Observable state of each
item (dispositions a finished lesson could cite):

1. **C1 calibration repair + input-ordering**: disposition work exists and
   is consistent — lesson `round-29.md:10-12,17-19` describes the v2
   counter and the ordering fix; QUALITY row 56 (`corpus/QUALITY.md:628`)
   codifies it; untracked `c1-at-E.stdout` shows
   `C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=22
   bound=22 … exit=0`, consistent with the frozen claim. But the lesson
   does not state item 1's disposition anywhere.
2. **S059 pinned digests / supersedes row**: disposition work **not
   done** — `corpus/SOURCES.md:68` still pins `0d362d11…` in the S059
   locator, no supersedes row exists (`grep 'supersede'` hits only
   S047/S048/S050/S075/S076…), and no non-determinism note was added.
   A `ReopenS059` wave receipt exists (`.ufo/waves/round-29/w1/ReopenS059.md`)
   but the lane has not recorded the outcome. Nothing in the lesson either.
3. **Close against one head**: not yet testable (round not closed);
   QUALITY row 57 (`corpus/QUALITY.md:638`) was added and names routed
   item 3 as captured-by. No disposition text in the lesson.
4. **Round-27 routed items 4–6 (README, QUALITY, runner ledger inputs)**:
   partially landed — `corpus/README.md:431` adds "Round 29 — F8 wording
   correction" (item 4, though marked "partly held", not fixed);
   QUALITY 55 (item 5) at `corpus/QUALITY.md:613`; the w1 cold-read append
   receipt (`coldread/select-receipt-w1.json`, ledger 371 → 393) covers
   the ledger-input part. Still no explicit disposition in the lesson.

## Smallest safe correction

Finish the file before close: append `## Mistakes` (each row with class,
evidence pointer, captured-by, and a failing-case command), and a routed-
defects block naming items 1–4 of `round-28-verifier-spotcheck.md` with
one-line dispositions. Item 2 needs real work, not just prose: add the
S059 supersedes row (or record the non-determinism in the locator) —
currently nothing on disk does. Apply the LOW-1 quote note.

## Method note

All checks were read-only in the lane (`git diff`/`show`/`status`, `grep`,
`sha256sum`, `stat`); no scratch clone was needed and no mutating command
was run. No tools installed. LSP not applicable (markdown/docs review).
Time used ≈ 10 min.
