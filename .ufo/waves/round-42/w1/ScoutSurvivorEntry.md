# Scout — survivor-classification.md (staged S166 + S156)

Scout seat L1Tameshi42.ScoutSurvivorEntry, round 42 wave 1. Access date 2026-10-25.
Entry: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/survivor-classification.md`.

## 1. Re-open of S166 (zenn.dev) and S156 (arXiv 2406.09843)

```
curl -fsSL -m 60 'https://zenn.dev/seckeyjp/articles/j-six-mutation-testing' -o /tmp/tameshi-r42-ScoutSurvivorEntry/zenn-j-six.html
# 171806 bytes, sha256 a6bcc4ec7e4523161d6c9cfcc70f25b8e55b01f08c6a18c1851377ff658d4335
curl -fsSL -m 60 'https://arxiv.org/abs/2406.09843' -o /tmp/tameshi-r42-ScoutSurvivorEntry/arxiv-2406-09843.html
# 44019 bytes, sha256 7af7e470fca3ef38e97d858b308dca20e815a4b919c9c235adae4d4f59c4a86e
```

Both live; arXiv page title = "A Comprehensive Study on Large Language Models for Mutation
Testing", carries 2406.09843v5. Scratch snapshots kept at the paths above.

## 2. Quoted claims — located

**S166 (zenn) — present, except one quote drifted:**
- "カバレッジ 99% のテストに mutation testing をかけたら、監査ログの穴が見つかった" (article title / meta) — present.
- 168 killed / 15 survived out of 183; "mutation score = 168 / 183 = 91.80%" — present (article §3 結果).
- 「生き残ったミュータントがすべてテストの穴とは当たりません」 — **NOT verbatim in the page opened 2026-10-25**: the page reads 「生き残ったミュータントがすべてテストの穴とは限りません。」 (限りません, not 当たりません). Semantically identical; direct-quote wording drifted. Located in the article body (the "テストの穴とは限りません" sentence, 2 occurrences incl. JSON-escaped duplicate).
- 「生存ミュータントは「穴の候補」であり、1件ずつ分類する必要があります」 — present verbatim (2 occurrences).
- "3 real holes out of 15" — present: 「本物のテストの穴が3件」 (4 occurrences).
- Section headings: 「生存ミュータントから「性質」を導く」 present (§4); §3 結果 numbers verified above.
- recheck command drift: `grep -c '168 killed'` on today's HTML returns **2**, not the entry's expected 1 (page now carries the phrase twice — rendered + JSON-escaped). String is present; count changed.

**S156 (arXiv 2406.09843) — present:**
- Abstract: "…the LLM-generated mutants have worse non-compilability, duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage points, respectively." — present in `citation_abstract` meta (3 occurrences of "3.51"). The entry's paraphrase ("equivalent-mutant rate is 3.51 percentage points worse than for rule-based mutants") matches exactly.
- Recheck string "equivalent mutant rates" present (count 3).

## 3. PROVINCE fit

- Domain: verification-fixture craft — mutation testing and survivor handling are within the domain; the entry is a `knowledge/` entry, the PROVINCE-designated carrier for frontier ground ("ground moves to Core only through an admitted, source-headed knowledge/ entry whose source: cites a mined SOURCES.md row"). It cites S166/S156, both **mined** staged rows in `SOURCES.append.md` (S166 line 20, tier B community, used-by pbt-generator-as-fixture.md; S156 line 10, tier A, used-by llm-mutant-equivalence-cost.md).
- Boundary discipline: marks S166 as community tier B scoped to one small system (207 statements), and explicitly does not transfer S156's Java numbers to the lane's JS/bash legs. Fits the lane's honest-check standard.
- Note: the lane's live SOURCES.md still lists arXiv 2406.09843 as an unopened Lead (line 254); the row becomes held only on adoption of the staged SOURCES.append.md.

## 4. F8 ground (oracle anchoring) — NOT moved by this entry

- F8 is **already partly held** since round 27 via `corpus/knowledge/oracle-anchored-survivors.md` (S012/S090/S091; measured probe `.ufo/evidence/round-27/f8/`, 4/4 anchored holes; round-29 wording correction bounds it to 3 of 4 anchored in the gate's header contract + 1 by convention).
- The candidate entry states "ground: F8" but performs **no classification measurement** — its own Boundary section says "the lane's own classification is not performed in this round". It supplies the classification *rule* (equivalent vs behaviourally-different survivors, S166) and a yield-rate datum (15 → 3, 20%) that support F8's shape; it does not move F8's status (no new probe, no new anchored expectation, no re-measurement). No duplication of the held oracle-anchored-survivors.md (different scope: rule vs executed classification) nor of survivor-fixture-minimization.md (F6).

## 5. Verdict: ADMIT, with one flip condition

Reason: both sources live and re-verified; the central claims check (99% coverage, 91.8% score, 15/183 survivors, 3/15 real holes, S156's 3.51 pp equivalence gap); the entry is properly scoped and PROVINCE-fitting; it supports (does not move) already-partly-held F8.

Flip condition (before append): correct the drifted direct quote 「生き残ったミュータントがすべてテストの穴とは当たりません」 → 「…とは限りません」 to match the page opened 2026-10-25, and update the recheck expectation (`grep -c '168 killed'` now yields 2 lines, not 1) or pin the quote to the saved snapshot (sha256 a6bcc4ec…). If the package prefers the original 2026-10-23 fetch, save that snapshot and anchor the quote to it; either way the quote and the recheck must name the same page state.

Could not check: the article's published date (2026-09-20) on the live page (no `published_time` meta found in the fetched HTML); the pre-2026-10-23 version of the page (no archive consulted) — so whether the page changed or the quote was originally imprecise is unresolved.
