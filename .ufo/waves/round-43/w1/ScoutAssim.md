# ScoutAssim — round-43 wave 1: assimilation package inventory and the next theme

Seat `L1Tameshi43.ScoutAssim` · 2026-10-25 · read-only on the lane; the only write is this file.
Package read at `/home/vgpnk/Projects/shokuknow/merge/tameshi/` (READ-ONLY: no campaign tool run,
nothing fetched, written, committed or pushed there). **Assimilation: none** this round — nothing
below is an adoption; §4 is a recommendation for the *next* assimilation round. No tools installed.

Axes this seat serves: **coverage** (what the package actually carries), **provenance** (which of it
is new ground vs the lane's own bytes), **operability** (the cheapest gated theme that is not blocked).

---

## 1. What the package is, and its counts

`MERGE-REPORT.md:1-9`:

| quantity | value |
|---|---|
| staged by | `corpus-expansion-1` |
| proposed rows accepted | **103** |
| proposed rows refused by the package | **0** |
| proposed knowledge entries | **86** |
| lane registry at packaging time | **107** rows |
| first staged id | **S153** (staged set S153–S255) |

Cross-checked against `MERGE-REPORT.json`: `accepted=103`, `refused=[]` (0), `entries=86`,
`existing_rows=107`, `renumbered=0`, `first_id=S153`.

Row shape, from the package's own header (`MERGE-REPORT.md:9`; sum verified = 103):
round1=14, round10=5, round11=5, round12=4, round13=8, round14=11, round15=4, round16=3,
round2=8, round3=7, round4=6, round5=5, round6=4, round7=5, round8=9, round9=5.

Entry kinds (`MERGE-REPORT.json`, `Counter(kind)`): **81 `new-file`**, **4 `amendment`**,
**1 `folded-into-canonical`** ≈ 86. On disk that is **85 files**: `knowledge/corpus/knowledge/*.md`
= 81, `amendments/corpus/knowledge/*.md` = 4 — the 86th entry is the round-2
`japanese-flaky-verdict-and-environment` copy folded into the round-13 canonical entry
(`MERGE-REPORT.md:15-21`; only one file on disk).

Two packaging notes that gate any later adopt:

- One target-path conflict: `corpus/knowledge/japanese-flaky-verdict-and-environment.md`
  (round13 + round2; `MERGE-REPORT.md:19-21`) — fold, do not create a second file.
- Five staged rows point at documents the lane already holds (`MERGE-REPORT.md:114-124`):
  `S153`↔S105, `S154`↔S106, `S196`↔S152, `S209`↔S107, `S211`↔S002. Four `used-by` pointers were
  corrected at packaging time (`MERGE-REPORT.md:126-135`).

---

## 2. The package by theme, with counts

Method: each of the 85 files was read for its `source:` lines, classified into exactly one theme
(mapped 85, unique 85, none unmapped, none extra — coverage check). `staged rows` is the number of
distinct `S###` ids on that theme's `source:` lines; `external` = the entry cites at least one source
outside the lane's own tree; `lane-tree-only` = every `source:` line points at this lane
(`VeigaPunk/*`, `lanes/tameshi/*`, `*.ufo` receipts) and therefore adds no new ground.

| theme | entries | new-file | amendment | staged rows | external | lane-tree-only | already in lane |
|---|---|---|---|---|---|---|---|
| F3 flaky verdict / determinism / run identity | 21 | 21 | 0 | 26 | 9 | 12 | 0 |
| F1/F6/F9 outcome vocabulary, score denominators, equivalence | 13 | 13 | 0 | 16 | 8 | 5 | **1** |
| F1 interop blocker accounting | 12 | 12 | 0 | 16 | 1 | 11 | 0 |
| F4 golden / snapshot fixture discipline | 11 | 7 | 4 | 13 | 5 | 6 | 4 targets* |
| F5 environment normalisation / instrument staging | 8 | 8 | 0 | 9 | 0 | 8 | 0 |
| F7 re-sweep cadence + quarantine | 6 | 6 | 0 | 11 | 4 | 2 | 0 |
| F10 PBT generators | 5 | 5 | 0 | 7 | 5 | 0 | 0 |
| source access / reachability | 4 | 4 | 0 | 4 | 2 | 2 | 0 |
| agent-evaluation tradition (round 16) | 3 | 3 | 0 | 3 | 0 | 3 | 0 |
| landing kit | 2 | 2 | 0 | 2 | 0 | 2 | 0 |
| **total** | **85** | **81** | **4** | **107 refs → 103 distinct** | **34** | **51** | **1 (+4 targets)** |

\* The four F4 amendment *target* files already exist in the lane (`golden-comparison-verdict.md`,
`r3-snapshot-fixture-update-paths.md`, `r6-snapshot-practice-corpus.md`, `r8-golden-update-flag.md`),
but **none of their staged bodies is applied**: 0 of 24, 0 of 30, 0 of 43 body sentences are verbatim
in the lane file, and 1 of 35 for the diff amendment; the lane files still open on their old rows
(S105/S106, S132, S152, S107) and the staged bodies cite `S153`/`S154`, `S176`, `S196`, `S209`+`S210`.

The 107 refs vs 103 distinct staged ids: four ids are cited by two entries each — `S156`
(`llm-mutant-equivalence-cost`, `survivor-classification`), `S160` (`flaky-aware-verdict-evidence`,
`pit-outcome-vocabulary`), `S165` (`mutation-score-semantics-cjk`, `llm-mutant-equivalence-cost`),
`S167` (`repeat-control-measured-n3`, `delta-debugging-minimization-contract`).

Whole-package split: **34 entries carry at least one external source; 51 are lane-tree-only.** The
same-ground half is not expansion — it is the lane's own receipts circulated back, which is the
class the round-41 Gate refused (`LOG.md:2138-2141`).

---

## 3. What is still unadopted

### 3.1 Round 42's four dispositions (source: `corpus/lessons/round-42.md`)

`corpus/lessons/round-42.md:9-11`: "Two entries admitted, one refused, one left unadopted with
positive gate verdicts."

| disposition | entry | package ids | evidence |
|---|---|---|---|
| **adopted #1** (the only package entry ever adopted) | `corpus/knowledge/pit-outcome-vocabulary.md` | `staged:S159`, `staged:S160` → lane S155, S156 (+S158, +held S001) | `:22-58`; `LOG.md:2198-2199` |
| **adopted #2** (NOT from the package) | `corpus/knowledge/r42-attribute-and-outflag-destinations.md` | lane S157 (new) + S158 (new) | `:60-80`; `LOG.md:2198` |
| **refused** | `survivor-classification.md` | `staged:S166`, `staged:S156` | `:82-97` |
| **deferred** (both gates said admit) | `mutation-score-semantics-cjk.md` | `staged:S163`–`staged:S165` | `:99-106` |

So "adopted two" is two *lane entries*, of which exactly one is a package entry. Package-wide
adoption is **1 of 86 entries**; the round-42 adopt also left S155/S156 no longer free, which is why
`corpus/SOURCES.md:449` now reads `Next unused id: S159`.

Refusal grounds, all still open (`:82-97`): (1) one direct quote drifted (`とは当たりません` on the
page vs `とは限りません` in the staged text); (2) recheck predicate false on live bytes
(`grep -c '168 killed'` → 2, entry expects 1); (3) thesis duplicates the held F8 entry
`corpus/knowledge/oracle-anchored-survivors.md`. The entry exists; its coverage row is
`corpus/README.md:422` (the round-42 lesson's `corpus/README.md:85` points at the F8 *frontier* row,
which is now line 85 in the frontier table — a citation that resolves to the right ground but not to
the entry).

Deferral grounds and flip, verbatim at `:99-106`: both gates said admit
(`.ufo/waves/round-42/w1/ScoutCjkEntry.md`, `ReviewCjkGate.md`); it was not adopted only because the
round's theme slot was filled by the PIT entry; its ground — the score denominator for equivalent
mutants — is "a second, adjacent question no admitted entry covers"; the flip is to re-open the three
sources, snapshot them, and repair the dangling `CANNOT-ANSWER.md §3.7` pointer, which
`ReviewCjkGate.md` made a condition of admission (not a waiver).

Gate conditions for that deferral, still in force
(`.ufo/waves/round-42/w1/ReviewCjkGate.md:78-104`): finding 4 = repair the dangling pointer
(**no such file exists**: `find … -iname '*CANNOT*'` finds only an unrelated coldread trace;
`grep -rn 'CANNOT-ANSWER' corpus/` → no matches). Flip conditions: (a) any quoted string absent from
a live source; (b) the lane adopts a scoring contract counting equivalent mutants *in* the
denominator; (c) the pointer is not repaired at adoption.

Package state per entry: **85 of 86 unadopted** — 80 of 81 new-file entries (only
`pit-outcome-vocabulary.md` is in the lane), all 4 amendment bodies, and the folded duplicate.
Four unadopted entries carry a verdict (§3.2 plus the refused and deferred ones above); **81 have
never been gated at all**.

### 3.2 Earlier verdicts among the package's entries

The package was already read and partly refused two rounds before this one.
`corpus/lessons/round-41.md:28-38`: the two staged F4 gate-census entries
`r4-gate-write-path-audit` (staged `S185`) and `r5-gate-write-site-census-corrected` (staged `S189`)
carry `source:` lines that point at this lane's own tree at revision `31687496`, not at an external
surface, so adopting them would add same-ground rows, not expansion (CORPUS rule 4) — refused.
`r4-gate-write-path-audit` had already been refused by the round-40 Gate, and its flip condition is
measurable: `git cat-file -e 31687496:tools/write-path-census.py` fails at the recorded revision
(`:35-38`), so no write-path census artefact exists there. Both refusals stand on that predicate,
not on taste.

`corpus/SOURCES.md:451` carries the hand-off hazard: after round 42 the staged set collides with
**six** lane rows (`S153`–`S158`) — and the collisions are by id only (lane S153 = Python `ast`,
staged S153 = POSIX `diff`; lane S155 = PIT basic concepts, staged S155 = arXiv 2302.09330). Any
append must renumber **by document** in scratch first.

---

## 4. Next theme: the deferred score-denominator / equivalent-mutant theme (F1/F9)

**Recommendation: round 44 takes the CJK score-denominator theme — `mutation-score-semantics-cjk.md`
(`staged:S163`–`staged:S165`) as the lead entry, with `cjk-mutation-metric-and-tool-comparison.md`
(`staged:S168`) and `r3-cjk-test-suite-effectiveness.md` (`staged:S181`) as the optional fill to the
addendum's 1–3 entry budget.**

Reason, in the order the record itself supplies it:

1. **It is the only carried, pre-declared next move.** `corpus/lessons/round-42.md:99-106` names the
   flip in full, and both gates already returned admit. Nothing has to be re-litigated except the
   re-grounding; every other theme needs its gates designed from zero.
2. **The ground is adjacent but genuinely uncovered.** The held F1 entry fixes the *verdict
   vocabulary* and `k/(k+s)` vs Stryker `detected/valid` (`corpus/README.md:60`), and the round-42
   entry fixes *which outcomes count as a kill* (`corpus/lessons/round-42.md:22`). Neither states
   the denominator's treatment of **equivalent mutants**. The deferred entry does — with three
   sources — so it extends F1 without duplicating it.
3. **It is external ground, not the lane's own bytes.** Its three sources are huaweicloud
   CloudTest docs, the NJU GIST 2015 slides, and a dfcfw LLM-era deck; none of these domains has a
   row in the lane (`grep -n "gist.nju\|jos.org.cn\|cjc.ict.ac.cn\|dfcfw" corpus/SOURCES.md` → no
   matches). Compare the same-ground themes — F1-blocker accounting 11/12 lane-tree-only, F5 8/8,
   landing kit 2/2, agent-eval 3/3 — those add no ground (the round-41 refusal class,
   `LOG.md:2138-2141`).
4. **It is not quarantined.** The absent-defect register's tameshi slice covers `S105`–`S143` only
   and every id has a verdict (`corpus/lessons/round-40.md` Quarantine table; re-derived
   `awk … absent-defect-register.md` → 17 rows, `S105`…`S143`). `S163`–`S166`, `S168`, `S181` are
   absent from it — no pending ABSENT/could-not-be-fetched verdict stands against them.
5. **Cheapest operation.** One entry, three rows, no tool, no measurement: re-open, snapshot,
   re-quote, repair one pointer. F10 (the runner-up) needs five fresh gates for five entries.

**Preconditions the next round must discharge (all recorded, none waived):**

- Re-open the three sources and commit snapshots under `.ufo/evidence/round-44/sources/`, with a
  located ≤25-word quote per source, an in-round `verified-at:`, and a recheck command whose
  expected count is fixed (the staged recheck is huaweicloud `用例通过率`, "non-zero").
- **Repair the `CANNOT-ANSWER.md §3.7` pointer** (`ReviewCjkGate.md:78-84`): point it at a real
  record (coverage-map Known-gaps, or a `LOG.md` debt entry) or delete the sentence.
- **Renumber by document in scratch before appending**: next unused lane id is **S159**
  (`corpus/SOURCES.md:449`), six ids already collide (`:451`). By document:
  `staged:S163` (huaweicloud) → S159, `staged:S164` (NJU GIST slides) → S160,
  `staged:S165` (dfcfw deck) → S161; if the siblings come in,
  `staged:S168` (软件学报 2024 35(7):3093-3114) → S162 and `staged:S181` (软件学报 survey) → S163.
  Use the 0–3-space extractor, not column-zero — the round-42 guard proof
  (`.ufo/waves/round-42/assimilation/guard/`) shows a two-space-indented row is missed by the latter.
- Re-check flip (b): the lane must not have adopted a scoring contract that counts equivalent
  mutants in the denominator, or the entry contradicts rather than parallels the held semantics.
- Do **not** bundle the refused `survivor-classification.md`: its three grounds are still unmet
  (drifted quote, `grep -c '168 killed'` → 2, duplicate of the held F8 entry) and its `staged:S156`
  is a package id, not the lane's S156.

**Runner-up: F10 PBT generators (5 entries, all external).** Genuinely uncovered — F10 is `open`
with "no PBT fixture method" (`corpus/README.md:87`) and all 5 entries cite outside sources
(JOSS `hypothesis`, Hughes' QuickCheck lecture, the ICFP paper, googletest's generator docs). It
loses only on cost: zero gate verdicts exist for it, and its README candidate rows S018–S021 are
still unopened leads, so a round would pay five gates for one theme.

**Ruled out, with evidence:** F4 golden/snapshot (4 of its 11 are amendment-only edits to held
files, and the package's write-site-census half is same-ground — refused as such at
`LOG.md:2138-2141`; the round-42 `tools/write-path-census-v4.py` already measured the lane's own
write paths); F3 (21 entries but its ground is held — `corpus/README.md:127`, and 12/21 are
lane-tree-only); F1-blocker accounting (11/12 lane-tree-only, the twelfth external entry is a
host-block reachability note), F5 (8/8), landing kit (2/2) and the agent-eval tradition (3/3) — all
same-ground; `survivor-classification` (refused).

---

## 5. Evidence (commands; all read-only)

```
wc -l MERGE-REPORT.md SOURCES.append.md                       → 146, 109
python3 -c "json.load(open('MERGE-REPORT.json')) …"            → accepted 103 refused [] entries 86
                                                                 existing_rows 107 renumbered 0 first_id S153
Counter(kind) over entries                                     → new-file 81, amendment 4,
                                                                 folded-into-canonical 1
find knowledge amendments -type f | wc -l                      → 85
source: lines across all 85 files → distinct S### ids          → 103 (S153…S255)
per-theme source-id union, sum                                 → 107 refs; overlaps S156 S160 S165 S167
entries with ≥1 non-lane source / lane-tree-only               → 34 / 51
ls corpus/knowledge | wc -l (lane)                             → 49
pkg knowledge ∩ lane corpus/knowledge                          → pit-outcome-vocabulary.md only (1)
pkg amendment ∩ lane corpus/knowledge                          → all 4 targets exist
staged body sentences verbatim in the lane target              → 0/24, 0/30, 0/43, 1/35
grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md                  → 113
grep -n "Next unused id" corpus/SOURCES.md                     → :449 S159
grep -n "post-append hazard" corpus/SOURCES.md                 → :451 six collisions S153–S158
grep -n "gist.nju\|jos.org.cn\|cjc.ict.ac.cn\|dfcfw" corpus/SOURCES.md → no matches
find … -iname '*CANNOT*'                                       → only round-17 coldread trace
grep -rn 'CANNOT-ANSWER' corpus/                               → no matches
awk -F'|' -v l=tameshi … absent-defect-register.md             → 17 rows, S105…S143
```

No campaign tool was run. No lane file other than this report was written; the lane's jj/Git state
and index were not touched. Scratch was unnecessary; nothing left in `/tmp`.

## 6. Unknowns / open

- **Amendment semantics.** The four amendments cite the same documents the lane already holds under
  older ids (S105/S106, S132, S152, S107). Whether the operator appends them as dated amendments or
  treats them as superseded-by-held is an operator call (`MERGE-REPORT.md:137-146` step 5 says
  append; the rows' "already held" status argues the other way). No claim here depends on it.
- **Round-42 record vs round-42 review on the CJK flip.** `.ufo/waves/round-42/w2/ReviewLessonGate.md:62`
  says the lesson's flip omits the pointer repair; the lesson at `corpus/lessons/round-42.md:104-106`
  does state it. Reading the lesson, the flip includes the repair; the review's quote is truncated.
  A round-44 seat should use the lesson text plus `ReviewCjkGate.md:78-84`, not the review's summary.
- **Sibling scope for the next theme.** `r7-metamorphic-oracle-chinese` (S199, cjc.ict.ac.cn) and
  `r7-llm-era-criteria-cost` (S200, arXiv 2609.09315) sit on the same subject but have never been
  gated; including them with the deferred entry would exceed the 1–3 entry budget. They are next
  after, not with, it.
- Nothing in this report moves a frontier to Core; F1 stays partly held, F4/F7/F10 stay open.
