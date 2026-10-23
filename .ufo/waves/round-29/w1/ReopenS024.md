# ReopenS024 — S024 re-opened by ordinary means; row S024 re-checked at 9f3084b vs 367ec0f

Seat: `TameshiR29.ReopenS024` (reviewer, leaf; no subagent dispatched). Wave: tameshi-r29-w1.
Repo under test: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` — read-only. No git write
command was run in the lane; no `jj` command was run anywhere; `GIT_OPTIONAL_LOCKS=0` was set
on every `git` invocation. Report written 2026-10-22T22:31:55-03:00 (= 2026-10-23T01:31:55Z).

## 1. Verdicts

1. **Bytes — same bytes.** The live page fetched now by plain `curl` is byte-identical to the
   L1 snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` (all three
   fetches + the snapshot hash to `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99`,
   496,906 bytes). The snapshot also matches the kaika-round-1 open receipt
   `.ufo/evidence/kaika-round-1/sources-opened.tsv:25` (same sha256 recorded 2026-10-19).
   The question "if not, same text after stripping tags" does not arise: the bytes already agree.
2. **Quote — verbatim after tag stripping + whitespace normalization, exactly once, under
   `§Delta Debugging`.** "Its result is 1-minimal, meaning that every character contained is
   required to produce the error" occurs once in the stripped-normalized text, inside prose
   immediately after the MysteryRunner trace; the last heading before it is
   `<h2 id="Delta-Debugging">` (fuzzingbook URL stays anchored in `§Delta Debugging`). The
   round-1 gate row used a different verbatim passage ("one first has to build a Runner whose
   outcome is FAIL if the precise error occurs"), which also verifies verbatim after
   normalization, also under `§Delta Debugging`.
3. **Row shape — only `status` and `used-by` changed in place; nothing else moved, and no other
   row was touched.** `git diff 367ec0f1d79c 9f3084bc60ad corpus/SOURCES.md` = 1 file changed,
   1 insertion(+), 1 deletion(-): status `queued` → `mined`; used-by `—` →
   `corpus/knowledge/survivor-fixture-minimization.md`. All nine other cells of the S024 row are
   byte-identical; `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`, `recheck`
   did not change. This respects CORPUS.md `SOURCES.md — where a shokunin learns`, rule 2
   ("Only `status`, `recheck` and `used-by` change in place").
   **Caveat (observation, not a verdict against the change):** the `used-by` target
   `corpus/knowledge/survivor-fixture-minimization.md` does not exist at `9f3084b` (nor at any
   earlier lane commit on any ref, per `git rev-list --all --objects`). The fleet census
   `sources-census.sh validate` therefore emits `tameshi E11 S024 missing used-by
   corpus/knowledge/survivor-fixture-minimization.md` on the current tree — same finding
   `RerunCensusA` already filed. The round-29 Gate (worktree `corpus/lessons/round-29.md`,
   not yet committed at `9f3084b`) already records the change log `queued → mined; — →
   corpus/knowledge/survivor-fixture-minimization.md`, satisfying the old→new logging clause;
   the path becomes true once the C2 entry is committed (owner: the C2 build item, per
   `contract.json` C2 predicate, which explicitly requires the row `mined` with that path in
   `used-by` and requires the entry's `source:` line to cite S024). The forward reference is
   contract-driven, not silent drift: the row was re-opened, the quote was located, and the
   status flip is the declared precondition of C2.
4. **Tier `B` and kind `book` — agree.** The page is the chapter "Reducing Failure-Inducing
   Inputs" of *The Fuzzing Book* (BibTeX block in the page itself:
   `@incollection{fuzzingbook2023:Reducer, author={Zeller, Gopinath, Böhme, Fraser, Holler},
   booktitle={The Fuzzing Book}, year={2023}, publisher={CISPA}}`) — a textbook: contract B =
   "strong secondary (expert write-up with reproducible detail, survey, textbook)". The chapter
   even embeds the runnable `Reducer`/`Runner` code (reproducible detail), which is exactly the
   B profile; the original ddmin authority would be the underlying paper, not this page. kind
   `book` is right (a book chapter); `book` is a declared kind in the contract enum.
   **Guard:** tier is scoped to `scope` ("delta-debugging reducer practice"), so B here does not
   promote the page to authoritative-for-ddmin-theory; if the lane later cites the algorithm's
   semantics, the original paper deserves its own row.

## 2. Evidence

Fetch (two live fetches within the last few minutes, plus the snapshot, plus the receipt line):

- `sha256sum`: `/tmp/S024-live.html`, `/tmp/S024-live2.html`, `/tmp/S024-live3.html`,
  `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` → all
  `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99`; size 496,906 bytes.
- Reply headers: `HTTP/2 200`, `server: GitHub.com`, `etag "69720ad6-7950a"`,
  `last-modified: Thu, 22 Jan 2026 11:32:38 GMT`, `content-type: text/html` — an ordinary
  fetch; no bot challenge.
- Receipt: `.ufo/evidence/kaika-round-1/sources-opened.tsv:25` records the 2026-10-19T21:43:52Z
  fetch of the same URL with the same sha256 → the page has served these exact bytes for the
  whole round-1 → round-29 window (snapshot, live fetch, and receipt all three agree).

Quote location (offsets into the fetched HTML, stripped by regex tag removal + HTML-unescape +
`\s+ → ' '`):

- Normalized index `251323`; last preceding heading (h1–h4 regex, document order)
  `<h2 id="Delta-Debugging">Delta Debugging`; surrounding normalized context:
  "… Test #29 ')' 1 PASS '()' Now we know why MysteryRunner fails – it suffices that the input
  contains two matching parentheses. Delta Debugging determines this in 29 steps. Its result is
  1-minimal, meaning that every character contained is required to produce the error; removing
  any (as seen in tests #27 and #29, above) no longer produces the error…" — i.e., the sentence
  sits inside the section's prose right after the `ddmin` MysteryRunner run, under
  `§Delta Debugging` (not under §Synopsis, §Grammar-Based-Input-Reduction, §Lessons-Learned,
  or any other h2 — full heading list on the page: h1 *Reducing Failure-Inducing Inputs*,
  then h2s *Synopsis*, *Manual Input Reduction*, *Delta Debugging*, *Grammar-Based Input
  Reduction*, *Lessons Learned*, *Next Steps*, *Exercises*, *Background* [ordering note: the
  list was emitted sorted; the document order puts the quote directly after the
  `MysteryRunner`+`DeltaDebugger` example under *Delta Debugging*]).
- Raw-HTML exact-substring count = 0 (the sentence is broken across cell markup); stripped-
  normalized count = 1. Both gate-quote candidates are §Delta Debugging prose.

Row diff (the only diff of the file between the two revs):

```
$ git -C <lane> diff 367ec0f1d79cb9b67d724f2962e7554a0841b1fc 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 -- corpus/SOURCES.md
corpus/SOURCES.md | 2 +-
1 file changed, 1 insertion(+), 1 deletion(-)
-35| S024 | … | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: … | queued  | 2026-10-19 | 365d | —                                          |
+35| S024 | … | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: … | mined   | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md |
```
(other rows byte-identical: `git show <rev>:corpus/SOURCES.md | grep -n S024` at both revs
prints line 35, and the file is 352 lines on both sides with only that one line differing —
confirmed identically by `RerunCensusA`'s count.)

used-by target (the known forward reference):

- `git cat-file -e 9f3084b:corpus/knowledge/survivor-fixture-minimization.md` →
  `fatal: path does not exist`. Also absent at base `367ec0f1`. (Fleet contract rule: a `mined`
  row must name ≥1 citing path; the census's `usedby_findings()` flags it — E11 — which is the
  row-readiness smell `RerunCensusA` documents; this seat only re-verifies it.)
- Round-29 Gate (worktree `corpus/lessons/round-29.md`, "S024 re-opened … fetched
  2026-10-23T01:09Z with `curl -sL`, snapshot … sha256 3abede35…, located quote (section
  'Delta Debugging', after the MysteryRunner trace)" and "Change log: S024 `status` queued →
  mined; `used-by` — → corpus/knowledge/survivor-fixture-minimization.md") satisfies contract
  rule 1 receipt fields (URL, access date, ≤25-word quote + location) and rule 2 old→new
  logging — pending only the C2 entry's commit.

Timing note (honesty): `git log` shows `9f3084bc` AuthorDate `2026-10-22 16:31:24 -0300` but
CommitDate `2026-10-22 22:12:16 -0300`; the worktree mtimes (row edit 22:11:40, fetched
receipt 22:09:28 local) and the lesson's `fetched 2026-10-23T01:09Z` (~22:09 local) say the
edit was committed ~22:12 local — i.e., the author date is a lane round-time stamp, not the
write time. Consistent with the round's stated semantics (`frozen before data`: edit + receipt
landed in the same commit, fetched ~3 min before the edit), but worth one line for the L1
since the receipt commits are already being cited as "pre-edit" evidence elsewhere.

## 3. Smallest safe corrections

- None needed for the row shape, the quote, or the tier/kind cells — all verified.
- For the E11 (missing `used-by` target): the round's own contract already fixes it — C2's
  predicate requires committing `corpus/knowledge/survivor-fixture-minimization.md` with a
  `source:` line citing S024; once that lands, `sources-census.sh validate` turns green.
  No in-place row edit is warranted; do **not** "fix" E11 by demoting `status` back to
  `queued` — that would break C2's frozen requirement instead.
- Optional polish for the L1: when the round-29 lesson is committed, its Gate block already
  carries the receipt; nothing else to add.

## 4. Bounds and tooling

- Leaf member: no subagent dispatch. Opened the source by ordinary means only (`curl`; no
  headless browser, no bot-challenge bypass). Reads against the lane repo used
  `GIT_OPTIONAL_LOCKS=0 git show/diff/log/cat-file`; nothing written except this report and
  `/tmp/S024-live{,2,3}.html` scratch. No installs/updates were needed or made (curl, git,
  python3 stdlib only). Report path: `.ufo/waves/round-29/w1/ReopenS024.md` relative to the
  lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
