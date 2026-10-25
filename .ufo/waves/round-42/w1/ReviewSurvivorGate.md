# Review — survivor entry gate (round 42 wave 1)

Reviewer: `L1Tameshi42.ReviewSurvivorGate` · date 2026-10-25
Candidate: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/survivor-classification.md`
(assimilation package, read-only). Gate: `corpus/QUALITY.md`, `PROVINCE.md`,
and the lane's F8 ground (`corpus/README.md` `## Frontier` F8 + held entry
`corpus/knowledge/oracle-anchored-survivors.md`).

## Verdict: REFUSE as submitted

Not admitted as it stands. The entry duplicates the held F8 ground, its source
rows are not opened/collide in the lane registry, its own recheck predicate is
false on the live bytes, and it was not re-grounded in-round. Flip condition at
the end.

## Findings (by severity)

### 1. [HIGH] Duplicates the held F8 entry `knowledge/oracle-anchored-survivors.md`

The candidate's thesis — "A surviving mutant is a candidate hole; it becomes a
hole only after it is classified" (candidate `:8`) — is the same ground the
lane already holds at F8:

- `corpus/README.md:85` F8 row: "oracle anchoring as a survivor class … 0
  test-oracle lines → one survivor classified against an independently anchored
  expectation".
- `corpus/README.md:418-429` (round 27): F8 moves open → **partly held** via
  `knowledge/oracle-anchored-survivors.md`; corrected in round 29
  (`corpus/README.md:431-438`) to "3 of 4 survivors anchored in the gate's own
  header contract and 1 held by convention only".
- The held entry's recipe (`knowledge/oracle-anchored-survivors.md:90-93`):
  "a hole call needs an expectation the mutant cannot move. Before calling a
  survivor a hole, name its anchor; when the only anchor is the pristine run,
  say 'differential hole'".

The candidate even concedes it performs no new classification: "the lane's own
classification is **not performed** in this round" (candidate `:47`). It is a
restatement of held ground illustrated with two new external sources, not a
measured advance. Per `PROVINCE.md:40-42`, a frontier ground moves only through
an admitted, source-headed entry citing a mined row; an entry that does not
perform the next falsifiable move cannot claim `ground: F8` in its header
(candidate `:6`).

### 2. [HIGH] Source rows S156/S166 are not in the lane registry; S156 collides with the planned adoption

- `grep -n "S156\|S166" corpus/SOURCES.md` → no matches. Lane registry ends at
  S154; `corpus/SOURCES.md` tail: "Next unused id: S155."
- The assimilation plan for this round (operator context, round-42 contract)
  reserves: S155 = staged:S159 (PIT basic concepts), S156 = staged:S160 (PIT
  FAQ), S157 = new Python argparse docs. The candidate cites `S156` =
  arXiv:2406.09843 (candidate `:3`), which **collides** with the planned lane
  S156 = PIT FAQ. S166 (Zenn) does not exist in the lane at all.
- QUALITY criterion 10 (MK-7): an external source enters through a `SOURCES.md`
  row opened in the round that writes it. Not satisfied; the entry must be
  renumbered (collision-free) and its rows opened as mined in this round.

### 3. [MED] The entry's own recheck predicate is false on the live bytes

Entry recheck (`:5`): "re-run `curl -fsSL 'https://zenn.dev/seckeyjp/articles/j-six-mutation-testing' | grep -c '168 killed'` (expect 1)". Executed 2026-10-25:

- `curl -fsSL 'https://zenn.dev/seckeyjp/articles/j-six-mutation-testing' | grep -c '168 killed'` → **2** (the string appears in the visible code block and once more in the page's escaped JSON payload). The stated expectation (1) is wrong as written; the check would fail.
- Claim content itself verifies: page shows "183 ミュータント: 168 killed / 15 survived", "mutation score = 168 / 183 = 91.80%", and "本物のテストの穴が3件ありました" (3 real holes of 15) — candidate `:12-18` numbers are accurate.

### 4. [MED] Not re-grounded in-round; S156 has no located quote

- `verified-at: 2026-10-23` (candidate `:4`) predates round 42 (frozen_at
  2026-10-25). The assimilation rule requires in-round re-grounding with the
  adopting lane's own access date (2026-10-25) and an own ≤25-word located
  quote.
- S166 quotes are present and located (§3. 結果, §4. 生存ミュータントから「性質」を導く).
  S156 has only paraphrase — no located quote from the arXiv abstract.

### 5. [LOW] Coverage-map row required in the same round (QUALITY 7)

The entry must land with its README coverage-map row in the same round (or
named debt in `LOG.md` with owner). No round-42 row exists yet; this is a
landing requirement, not a content defect.

## Residual risk / verification gaps

- I could not check that the planned adoption ids (S155–S157) have actually
  been committed to the lane registry yet — they were not at review time
  (registry ends S154). If the L1 renumbers the candidate's rows before
  append, finding 2 is resolvable; the collision hazard is real either way.
- Live fetches were saved under `/tmp/tameshi-r42-ReviewSurvivorGate/`:
  `zenn.html` (sha256 `1688b8a184510e9acaae65debc9da120a760e9b29ca3e2468a12f2c0d33078bf`, 171806 B) and `arxiv.html` (sha256 `7af7e470fca3ef38e97d858b308dca20e815a4b919c9c235adae4d4f59c4a86e`, 44019 B). The arXiv abstract confirms "increasing non-compilability, duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage points" — the S156 paraphrase is accurate.
- No tools installed/updated this seat (curl only; no package changes).

## Flip condition

Admit only if all of the following hold, otherwise keep refused:

1. S166 and S156 (renumbered to free lane ids, collision-free vs the planned
   S155/S156/S157 adoptions) are opened as **mined** `SOURCES.md` rows this
   round, and the entry's header citations are rewritten to those ids.
2. The entry is re-grounded in-round: access date 2026-10-25, verified-at
   updated, quotes verified against committed snapshots, and a located
   ≤25-word S156 quote added.
3. The `recheck:` predicate is corrected to match the live bytes (e.g.,
   `grep -c '168 killed / 15 survived'` → 1, or a unique anchor string).
4. The header claim `ground: F8` is replaced by an explicit statement that the
   entry **supports the already-held F8 ground** (`knowledge/oracle-anchored-survivors.md`),
   claims no new classification, and cites the held entry.
5. The README coverage-map row lands in the same round (QUALITY 7).
