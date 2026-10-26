# T50ScribePkgIeice — assimilation triage of `r7-ieice-mutant-abstraction-authority.md` (theme F6)

Seat T50ScribePkgIeice (scribe; axes coverage, adjacency), round 50 wave 1, 2026-10-26.
Subject: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r7-ieice-mutant-abstraction-authority.md`
(76 lines, cited below as `authority.md:N`) and the staged row it hangs on,
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:51` (S197).
Read-only seat: the only files I wrote are this report, its receipts and the source copy under
`.ufo/waves/round-50/w1/T50ScribePkgIeice/`. No counter was run (not `--selftest`, not `--explain`); no tool installed.

**Verdict: `defer`.** The source itself is clean — every content claim in the entry locates verbatim in the
opened report, and the copy I fetched is byte-identical to the one the campaign opened on 2026-10-24. What
fails is the *assignment*: the report is mutant-side reduction, F6's frozen row measures fixture-side
reduction, so it cannot be "the method authority for F6" (`SOURCES.append.md:51`) and cannot carry F6's
status or C2. It becomes admissible in one edit, under a re-scoped ground (§5).

## 1. What I opened, and what I could not

Copy of record for this triage:
`.ufo/waves/round-50/w1/T50ScribePkgIeice/ieice-techrep-125-376.pdf` (sha256 `344a5ae6cb83df12a9bf9841e5cd11c0ebefd1341eb878c5e2a8eba96e8f4b3c`, 676 980 B, PDF-1.5, 6 pages) and its
`pdftotext -layout` extraction `…/ieice-techrep-125-376.txt` (sha256 `4f1ac6f8…83e5`, 388 lines, cited as
`txt:N`). Commands and raw output: `…/T50ScribePkgIeice/receipts-1.md` (R1–R5), `…/receipts-2.md` (R6–R9).

| target the package cites | status | receipt |
|---|---|---|
| Wayback capture `…/web/20260416233249/https://sdl.ist.osaka-u.ac.jp/pman/pman3.cgi?DOWNLOAD=749` (`authority.md:2`) | **opened**; 676 980 B, `%PDF-1.5`, 6 pages | R1 |
| the campaign's persisted copy, `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round7/evidence/ieice-techrep-125-376.{pdf,txt}` (`authority.md:2`) | **opened**; PDF digest equal to mine, extracted text byte-identical | R2 |
| the entry's own `recheck:` command (`authority.md:4`) run verbatim | prints `1` (non-zero → the entry's check passes) | R3 |
| the round-6 ledger statement the entry calls wrong (`authority.md:13-14`) | **opened** in the campaign: `lanes/tameshi/round6/SEARCH-LOG.md:97`, `round6/CANNOT-ANSWER.md:19,46` | R8 |
| `ken.ieice.org` report index | **not openable**: HTTP 405, AWS WAF page — same as the campaign recorded (`round7/SEARCH-LOG.md:150`) | R7 |
| researchmap profile `read0013799` | **not openable**: HTTP 403 | R7 |
| CiNii OpenSearch | **not re-measured**: HTTP 307 today (redirect, not followed). The only measurement is the campaign's (`round7/SEARCH-LOG.md:151`: 200, 1.7 KB, no record) | R7 |
| J-STAGE `_article` / `_pdf` | **not retried**: campaign recorded 500 / login redirect (`round7/SEARCH-LOG.md:151-152`) | — |
| issue designation vol. 125 no. 376 pp. 025-030 | **not obtainable from the body**: no volume line; footers carry only `—2—`…`—6—` | R5 |

Unreachable is recorded as unreachable; nothing in §2 comes from a snippet, an index, or the campaign's claim.

## 2. The entry's content claims, checked against the opened bytes

| entry claim | location in the opened report | result |
|---|---|---|
| title, six authors, 大阪大学大学院情報科学研究科 / 株式会社 日立製作所, 信学技報 / IEICE Technical Report (`authority.md:2`) | `txt:1-10` | matches |
| abstract sentence 「…テスト不備の原因理解や改善方針の検討を困難にし，分析コストの増加につながる．」 (`authority.md:40`) | `txt:19` | verbatim |
| keyword line present (`authority.md:21`) | `txt:24` | present |
| §3 段階的ミューテーションテスト, §3.3 統合, §4.1 概要, §5.1 計算コストの削減 (`authority.md:22`) | `txt:135`, `txt:209`, `txt:232`, `txt:267` | present (see E4 for 表 1) |
| Table 1: 5 / 1 / 69 / 9 / 16 / 11 / 1.7 / 3.7 (`authority.md:27-34`) | `txt:295`, `:296`, `:297`, `:299`, `:301`, `:302`, `:304`, `:305` | all eight verbatim |
| 「提案手法によるミュータント生成・統合は手動で行った．」 (`authority.md:37`) | `txt:193` | exact substring present (`grep -c` → 1, R3) |
| proposed method 2× slower; §5.1 offers 抽象化の省略 (`authority.md:50-55`) | `txt:271-272` (「2 倍以上になっていた」), `txt:280` (「アイデアとして抽象化の省略が考えられる」) | matches |
| the manual time is excluded from the 3.7 s (`authority.md:51-53`, implied) | `txt:262-263` (「本来はそれらの時間の分が加算される」) | matches, and the entry's "no speed-up" reading is the conservative one |
| volume line absent, footers only page markers (`authority.md:65-69`) | `grep -cE '125|376|025|030'` → 0; markers at `txt:127,187,251,309,388` | matches |
| "technical report without peer review … may be published elsewhere" (`authority.md:72-74`) | `txt:54`: "This article is a technical report without peer review, and its polished and/or extended version may be published elsewhere." | verbatim |

**No content claim in the entry failed.** The three inference blocks (`authority.md:44-49`, `:50-55`,
`:56-61`) follow from the numbers; the third is additionally corroborated by the campaign's own wording
(`round6/SEARCH-LOG.md:97` "the Wayback has no snapshot" versus `round6/CANNOT-ANSWER.md:46` — the
`{"archived_snapshots": {}}` answer of the availability API, which is what was actually measured).

## 3. Gates

### PROVINCE — `PROVINCE.md:3-20`
In province. Mutation testing, survivor analysis and the cost of making survivors reviewable are the lane's
stated core craft; the document is not a product domain, not credential material (kagi), not endpoint health
(kama). **PASS.** The defect found below is not domain scope but ground assignment.

### QUALITY — `corpus/QUALITY.md`
- **1 falsifiable** — every content claim is a quote or a table cell. PASS.
- **2 measured anchor** — **FAIL for one sentence**: `authority.md:11-14` ("Seven rounds failed on this
  document: …researchmap's indexed profile id is stale, CiNii has no record…") carries no anchor. The
  campaign holds the record at `round6/SEARCH-LOG.md:97`, `round6/CANNOT-ANSWER.md:19,46` and
  `REJECTIONS.md:55`; the entry cites none of them. One-line fix.
- **3 observation / inference / unknown separated** — PASS, three explicit sections.
- **4 append-only errata** — n/a (new file).
- **5 a rejection is kept** — **OPEN.** The campaign rejected this paper (`REJECTIONS.md:55`) with
  `flip: the lab host answers on TCP/443 (or an IEICE/J-STAGE copy is published), and the PDF is opened
  firsthand.` Both clauses now hold (opened firsthand, R1; host answers `200` at root / `404` at the old
  endpoint on 443, R7), yet the entry never records the flip. QUALITY 5 requires the rejection to stay and
  the flip to be noted.
- **7 coverage-map row in the same round** — owed when it lands: the package has no coverage map, so the lane
  must add the round-50 row naming the entry and its (re-scoped) ground.
- **9 evidence copied into the repo** — **OPEN.** The entry's only locator for the extracted text is the
  campaign path (`authority.md:2`). `merge/tameshi` ships no `lanes/` directory and `find merge/tameshi -name
  '*125-376*'` finds nothing; the lane's own corpus has no IEICE reference at all
  (`grep -rln 'IEICE\|技報' corpus/` → ∅). A lane entry citing that path cites a file the lane does not
  hold. This wave's copy (§1) is the snapshot such an entry can cite.
- **10 header trio, row opened in the writing round, tier-C never sole support** — header present
  (`source:`/`verified-at:`/`recheck:`); **no digest** of the opened copy (recent lane entries carry one);
  the staged row is `opened 2026-10-24`, so a round-50 entry needs a row opened today (my re-open supplies
  it). **Tier**: `SOURCES.append.md:51` says `A` for "the method authority for F6". A is defensible only
  inside the report's own numbers (§2); for any general claim about survivor reduction the source is one
  unreviewed 研究会原稿 (`txt:54`) with n = 1, one subject program and a by-hand execution
  (`authority.md:70-71`) → **B**. OPEN as a tier-scope wording fix.

### Ground not already held — `corpus/README.md:83`, `corpus/SOURCES.md:33-35`
- The content is **new**: `grep -rln 'abstraction\|抽象' corpus/knowledge/*.md` → ∅. Nearest held entries are
  survivor *resolution* (`corpus/knowledge/r43-survivor-resolution-rule.md:1-13`), fixture-side minimisation
  (`corpus/knowledge/survivor-fixture-minimization.md:1-8`), oracle anchoring
  (`corpus/knowledge/oracle-anchored-survivors.md:1-5`) and score semantics
  (`corpus/knowledge/mutation-score-semantics.md:1-8`). None of them holds a survivor-set reduction method
  or its cost.
- **It is not F6's ground.** F6's frozen next move is `B5 probe fixture size: unmeasured → reduced size +
  kill check` (`corpus/README.md:83`), on candidates S022/S023/S024 — a *fixture-side* reduction whose
  measure is a kill. The report reduces the *mutant* set (5 → 1, `txt:295-296`) and never shrinks a fixture.
  So `SOURCES.append.md:51`'s "the method authority for F6" is a claim the lane's own F6 row does not
  support, and F6's status this round is carried by C2's shrinker, not by this citation.
- The entry's `ground:` also names **F2 and F8** (`authority.md:5`). F2's vocabulary (killed vs survived)
  is already held (`mutation-score-semantics.md:1-8`, S001/S004/S006) → no new ground. F8's shape appears
  only as a *seeded* oracle defect in the case study (`txt:189`: the multiple-of-5 assertion
  「機能しておらず」), with no gate and no anchoring probe → it cannot ground F8 either.
→ **PASS** for "new, unheld material"; **FAIL** as F6 and as F2/F8 support.

### CORPUS rule 1 — `/home/vgpnk/Projects/shokunin/CORPUS.md:112-114`
"A row is a claim. Write it only after opening the source in the round that writes the row." The one source
the entry is *about* was opened by me today and agrees byte-for-byte with the copy opened 2026-10-24 (R1,
R2); every quote the entry carries locates in the opened text (§2); the same `recheck:` command still
returns non-zero (R3). **PASS**, with the four non-openables and one non-re-measurement recorded in §1.

## 4. Package errata (report only — shokuknow and the merge tree are read-only to this seat)

- **E1 — page locator wrong.** `SOURCES.append.md:51` anchors 表 1 at "p. 6". It is on **p. 5**:
  `pdftotext -f 5 -l 5 -layout ieice.pdf - | grep -c '表 1'` → 2, `-f 6 -l 6` → 0 (R4). The same
  imprecision is in `authority.md:22` ("§4.1 概要 with 表 1"): the table is cited in §4.2 結果と過程
  (`txt:205`) and printed on p. 5, while §4.1 概要 (`txt:232`) is the setup.
- **E2 — standing network claim is stale.** `SOURCES.append.md:51` and `authority.md:11` say the lab host
  "refuses TCP for the seventh consecutive round". On 2026-10-26 the host answers `200` at `/`, `301` at
  `/pman/`, `404` for the exact `?DOWNLOAD=749` URL (R7): the endpoint is gone, the host is up. The entry's
  substance is untouched (its recheck uses the Wayback URL and passes, R3), but the sentence must be dated
  or dropped — a reader falsifies it in one command, which is precisely the sort of sentence this lane
  routes.
- **E3 — locator resolves only at the campaign root.** `authority.md:2` names
  `lanes/tameshi/round7/evidence/ieice-techrep-125-376.txt`, which exists under
  `/home/vgpnk/Projects/shokuknow/` (opened, R2) and nowhere under `merge/tameshi` or the lane. A lane entry
  must cite a lane-held snapshot (QUALITY 9).
- **E4 — rejection flip unrecorded.** `REJECTIONS.md:55` carries the flip that my open satisfies; see
  QUALITY 5 above. The rejection stays; the entry owes the flip note.

## 5. Verdict and flip conditions

**Verdict: `defer`.**

*Decisive reason.* The material is verified and in province, but it is filed on the wrong axis: F6's frozen
row measures a fixture-side reduction with a kill check (`corpus/README.md:83`), and this report measures a
mutant-side reduction (5 → 1) with no fixture at all. Admitting it as "the method authority for F6" would
let F6's row, and a future F6 entry, borrow authority the source does not have — the same mislabel class the
lane routed in round 49 ("a routed defect is not a closed defect") — while C2's own sourced clause names
S167, not this document. Nothing about the source blocks admission; the ground line does.

*Flip to `admit`* (all four, one edit plus one snapshot):
1. the entry's `ground:` names the **survivor-side review cost** as new lane ground and says in line that it
   is F6-adjacent and does **not** move F6; the round-50 coverage row says the same;
2. tier **A only inside the report's own numbers** (§2), **B** for any general claim (single unreviewed
   研究会原稿, n = 1, by-hand execution);
3. the anchor is corrected to 表 1 p. 5 (E1) and `authority.md:11-14` gets its citation
   (`round6/SEARCH-LOG.md:97`) and a dated wording for E2;
4. the entry cites a lane-held copy with its digest (`344a5ae6…f4b3c`), and records the `REJECTIONS.md:55`
   flip (E4).

*Flip to `refuse`:* if the L1 intends to cite this row as F6's method authority, as F6's status support, or
as C2's sourced row. On that reading the package is refused on ground, and the round's F6 move must rest on
the shrinker and S167 alone.

## 6. Adjacency notes for the L1 (not verdicts)

- **C2's sourced clause is mechanically satisfiable by this row, and must not be.** `c2/measure.py:325-353`
  accepts any new knowledge file that mentions `F6` whose `source:` line names a row with
  `cells[7] == 'mined'` and `cells[8] == '2026-10-26'`; it never checks what the row is about. A row for this
  report, opened today, would pass that check while saying nothing about fixture minimisation. The honest
  row is S167; the counter cannot see the difference, so the L1 must.
- **The one durable method contribution.** The report is the only opened statement I have seen in this
  campaign that prices survivor reduction and finds it *negative*: 3.7 s against 1.7 s on its single case,
  with the by-hand time excluded (`txt:262-263`, `txt:271-272`). That is a usable brake on any later
  "abstraction makes a survivor set cheap" claim, including the lane's own F6 framing
  (`authority.md:44-49`), and it says the cost must be reported with its exclusions named — the same
  discipline C2 applies when it fixes `runs` to the logged guard invocations.
- **Archive lesson, already exercised by the lane.** The availability API's `{"archived_snapshots": {}}`
  (`round6/CANNOT-ANSWER.md:46`) was an index answer, not an archive answer; a plain timestamped URL worked
  (`authority.md:56-61`, R1, R3). The lane has no entry holding that rule — it is the cheapest thing this
  package teaches, and it is orthogonal to F6.

## 7. Receipts (all under `.ufo/waves/round-50/w1/T50ScribePkgIeice/`)

| file | content |
|---|---|
| `ieice-techrep-125-376.pdf` | the opened copy, sha256 `344a5ae6cb83df12a9bf9841e5cd11c0ebefd1341eb878c5e2a8eba96e8f4b3c`, 676 980 B |
| `ieice-techrep-125-376.txt` | `pdftotext -layout` extraction, sha256 `4f1ac6f8b705428795ceb8e5d079d9b0a77ca516b5195b44751d1d1427ed83e5`, 388 lines |
| `receipts-1.md` | R1 fetch+digest, R2 identity with the campaign copy, R3 the entry's recheck, R4 page placement, R5 volume-line absence |
| `receipts-2.md` | R6 quote locations, R7 host probes (seven URLs, codes), R8 campaign ledger statements, R9 rejection row |

Tooling: nothing installed or upgraded (host pacman paused by operator guard; no install needed). Scratch
`/fast/scratch/hyaku/tameshi-r50/T50ScribePkgIeice/` was removed before this report was yielded; no scratch
path is cited as evidence.

## Summary

- Verdict **defer**: the report is verified verbatim (all 8 Table 1 values, the by-hand sentence at `txt:193`, the abstract at `txt:19`, the no-peer-review line at `txt:54`, no volume line) but it is mutant-side reduction, while F6's row (`corpus/README.md:83`) measures fixture-side reduction.
- The copy I fetched is byte-identical to the campaign's 2026-10-24 copy (`344a5ae6…f4b3c`); the entry's own recheck returns `1`.
- Corroborated the entry's correction: the round-6 "no snapshot" came from the availability API (`round6/CANNOT-ANSWER.md:46`), not the archive.
- Four package errata: 表 1 is on p. 5 not p. 6; "host refuses TCP" now 200/301/404; the persisted-text path exists only at the campaign root; the `REJECTIONS.md:55` flip is met but unrecorded.
- QUALITY 2 (unsourced history sentence), 5 (rejection flip), 9 (lane-held evidence), 10 (digest, tier scope) are open until fixed; PROVINCE and CORPUS rule 1 pass.
- Admit in one edit if the ground becomes "survivor-side review cost, F6-adjacent, does not move F6", tier A only inside the report's own numbers; refuse if it is used as F6's authority or as C2's sourced row (C2 names S167).
- Adjacency: C2's `records()` check (`c2/measure.py:325-353`) would accept this row mechanically and cannot see that it is off-axis.
