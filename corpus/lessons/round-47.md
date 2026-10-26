# Round 47 lesson

L1 TameshiR47, hyaku run 7, attempt 1. Three claims on distinct axes (contract `.ufo/evidence/round-47/contract.json`, frozen at
`9acfbe21435e1976636a276448dee1d5e7155915`, `amendments: []`): C1 calibration (standing rows state what each statement depends on), C2
operability (the hardened counters' selftests kill a deterministic mutant pool), C3 coverage (F3 flaky-test measurement ground, sourced).
Frontier step: SOURCES curation (rows S261-S264), one mined mistake, one sourced claim (C3). Assimilation: theme "F3 measurement half" from
`merge/tameshi` and one considerthese proposal (2026-10-25 idea 3).

## Gate

Candidates: the F3-tagged staged rows of `merge/tameshi/SOURCES.append.md` (21 of 103: `grep -cP '^ {0,3}\x7c S\d{3,}.*F3' SOURCES.append.md`)
plus the package entries that cite them. Admitted: three entries (four rows by document). Refused or not adopted: five package entries and
several package claims inside the admitted entries. The non-author spot-check is the closure's (LEARNING.md: a seat this lane dispatched is
still the lane); the reviewer seats named below are lane-dispatched and are not that check.

### Admit — S261 (new row): *Practical Flaky Test Prediction using Common Code Evolution and Test History Data* (Gruber, Heine, Oster, Philippsen, Fraser; arXiv 2302.09330)

- URL https://arxiv.org/abs/2302.09330; access date 2026-10-25; snapshot `.ufo/evidence/round-47/coverage/sources/arxiv-2302.09330-abs.html`
  (43,549 bytes), SHA-256 `2965343ceaac627ccf71f587d3108073c6b45e08b89db3bbe1521a5716e14bc6`. Row `corpus/SOURCES.md:136`; entry
  `corpus/knowledge/flaky-aware-verdict-evidence.md` (staged S155, re-pointed by document: the lane's own S155 is PIT basic concepts).
- Located quote, 24 tokens, §Abstract: "Detecting flaky tests is therefore a crucial task in maintaining code quality, as it builds the necessary foundation for any form of systematic response".
- Decision: **admit** (tier A scoped to the abstract's own claim). PROVINCE fit (`w1/T47RevProvince.md`): craft, because it states what a flaky
  verdict can rest on without added reruns. The entry grounds F3 only; the package's F7 tag is not supported by the snapshot
  (`w1/T47ScoutHeld.md`). Coverage ground unheld at base: `w1/T47ScoutHeld.md` (four independent greps).

### Admit — S262 (new row, uncounted by C3): Lam, Winter, Astorga, Stodden, Marinov, *Understanding Reproducibility and Characteristics of Flaky Tests Through Test Reruns in Java Projects* (author-hosted camera-ready)

- URL https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf; access date 2026-10-25; PDF
  file lam-2020-reruns.pdf beside the text snapshot (565,435 bytes, SHA-256
  `0b88045817f146db3eb26d305c864291010e5c083aa8d5cac480be3c5350895d`); text snapshot
  `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.txt` (pdftotext 26.08.0 `-layout`, 81,725 bytes, SHA-256
  `bf52c9089e331f18bb65c3c03449de070723c7ec52725c0e6dc84ca249b025b9`; two columns interleave across the gutter, so every quote below is one
  column fragment). Row `corpus/SOURCES.md:137`; entry `corpus/knowledge/flaky-aware-verdict-evidence.md` (staged S158; the lane's own S158 is PIT `DetectionStatus.java`).
- Located quote, 12 tokens, §I guidelines box (text snapshot line 113, left column): "one can use ≤ 5 reruns (50% less than Google’s default ten".
- Decision: **admit** as the fourth row: it is the carrier of the at-most-5-reruns-check-at-least-82%-correctly statement and of the
  order-versus-repetition guidance, neither of which a held row states (`repeated-control-precondition.md:29` says no source prescribes a
  repeat count). The register's quarantine row S110 names the same URL and quote (`w1/T47ScoutQuarantine.md`): hand-checked this round against
  the committed PDF with `pdftotext` non-layout extraction, the staged quote is contiguous and byte-exact with the PDF's curly apostrophe
  (`Google’s`); in the layout text snapshot it is interleaved, so the register's payload-absent cause is the apostrophe fold. Verdict for S110: present,
  adopted as S262 with the anchor located here.

### Admit — S263 (new row): *How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection* (Gültekin, Berndt, Bell, Bach, Baltes; arXiv 2607.09345)

- URL https://arxiv.org/abs/2607.09345; access date 2026-10-25; snapshot `.ufo/evidence/round-47/coverage/sources/arxiv-2607.09345-abs.html`
  (44,459 bytes), SHA-256 `16ecdefca1f247d3acef2439576ca380bd0bacdd2fa1215e16c71006547a925d`. Row `corpus/SOURCES.md:138`; entry
  `corpus/knowledge/r8-flakiness-not-static.md` (staged S206).
- Located quote, 10 tokens, §Abstract: "C-IDoFT is a controlled counterfactual, not a benchmark for reuse".
- Decision: **admit**. The package copy attributed the paper to Baltes, McKim, Zaidman and Wagner; the committed snapshot lists Gültekin, Berndt,
  Bell, Bach and Baltes (`w1/T47ExecMirror.md`): the re-grounded entry and row carry the snapshot's authors. The paper is posted 2026-07 and
  under review: the entry names no venue.

### Admit — S264 (new row): *Cost of Flaky Tests in Continuous Integration: An Industrial Case Study* (Leinen, Elsner, Pretschner, Stahlbauer, Sailer, Jürgens), Semantic Scholar graph record of DOI 10.1109/ICST60714.2024.00037

- URL https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=title%2Cabstract%2Cyear%2Cvenue%2Cauthors%2CexternalIds
  (the first fetch answered HTTP 429, a later one 200); access date 2026-10-25; snapshot
  `.ufo/evidence/round-47/coverage/sources/s2-icst24-cost-of-flaky.json` (3,116 bytes), SHA-256
  `6ab5b3f58b27827c265422f958689bbeda4514286a532b3ce2f4a6b720bfde06`. Row `corpus/SOURCES.md:139`; entry
  `corpus/knowledge/r8-flaky-cost-baseline.md` (staged S207).
- Located quote, 23 tokens, `abstract` field: "The insights gained from our case study have led to the decision to shift effort from investigation and repair to automatically rerunning tests".
- Decision: **admit narrowly**, tier B: the carrier is a third-party metadata index whose `venue` field reads "International Conference on Information Control
  Systems & Technologies", which cannot be reconciled with the record's own DOI and DBLP key. The entry cites the DOI and the abstract, reports the carrier defect, and
  refuses transfer of the cost figures beyond the one industrial context (`w1/T47RevProvince.md` §0).

### Ids, collisions and the guard receipts

- Id check (prompt section 10, the 0-3-space extractor), `w1/T47ExecIdGuard.receipts.md`: `reg-ids` 120, `staged-ids` 103, `collisions` 8 (S153-S160); the
  guard `tools/staged-id-guard.py` prints `collisions=8 unmapped=0 held=4 cascade=0 next_free=S261 verdict=answered` and refuses the naive arithmetic map.
  Renumber map, by document: staged S155 (arXiv 2302.09330) → S261, S158 (Lam PDF) → S262, S206 (arXiv 2607.09345) → S263, S207 (Semantic Scholar ICST 2024) → S264.
  The round-46 map-only ids S261-S264 (S155-S158 arithmetic) were never appended; the by-document map replaces them.
- Proof the guard can fail: a scratch registry with the indented row `  | S002 |` yields a nonempty `collisions` (receipt in the same file).
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exit 0 at round start (`.ufo/evidence/round-47/census-start.stdout`, 120 rows) and at round end (`census-end.*`).

### Refused / not adopted

| Package entry | Verdict | Reason (line / criterion) | Flip condition |
|---|---|---|---|
| `r14-quarantine-threshold-is-a-policy.md` | refused | `PROVINCE.md:14-16` (a policy is not a method; two tier-C practitioner pages); QUALITY 10, 9, 34 | a held tier-A row states the threshold and the lane adopts a policy |
| `r13-flaky-false-red-rate.md` | refused (duplicate) | the 84% figure is held through S026/S260; QUALITY 15 | none; duplicate |
| `r12-flaky-mitigation-and-quarantine.md` | refused (duplicate) | same ground as S026 and `r9-false-red-rate.md` | none |
| `r8-gtest-order-and-seed.md` | refused (already landed) | adopted round 45 as `r8-gtest-order-and-seed.md` (S256); stale package copy | none |
| `r8-predictive-test-selection-cost.md` | refused | out of province (vendor-scale test selection; `PROVINCE.md:14-18`), unopened row; QUALITY 10, 2 | a row opened by the lane that ties selection to an own-leg re-sweep decision (F7) |

(`w1/T47RevProvince.md` §0 and §6.) Package claims dropped from the admitted entries, each with its reason in the scribe's report: the S160 (pitest FAQ) paragraph (lane
row S156 already holds it), a "timeout counted as a kill" convention the frozen C2 contract contradicts, a per-case outcome series the lane does not keep, the "ACM version
was access-controlled" sentence and a characterisation of the lane's six gates (`w1/T47ScribeEntryPredict.md` §"Package claims dropped or softened"; `w1/T47ScribeEntryCost.md`).

### Quarantine slice

`w1/T47ScoutQuarantine.md`: 17 rows, identical to `.ufo/evidence/round-46/assimilation/quarantine-slice`; none is S155, S158, S206 or S207. The one document-level overlap is
S110 = the Lam PDF = S262 (above, present, adopted). The other 16 rows stay quarantined; no new verdict.

### considerthese — `considerthese/2026-10-25.md` idea 3 (dead-code debt list)

Operator-authored, read-only. Mined as a scan, not a deletion: `w1/T47ExecDeadCode.scan.py` (python `ast`; classes after-terminator, constant-test, unreferenced) over `tools/` and
`.ufo/evidence/round-44` to `round-47` (51 files, 0 parse errors) finds `after-terminator=0 constant-test=0 unreferenced=2`: `brace_depth_at` in `tools/tally-audit-v2.py:135` and
`tools/tally-audit-v3.py:234` (dead since round 35, HYGIENE-1 in `.ufo/waves/round-35/w2/AttackPerIndexParse.md`, copied into v3). The one case the idea names, the round-43
`dead_code_only` survivor, is a string constant in `.ufo/evidence/round-43/mutants/measure.py` that is written as tool *input*; it is not code in `tools/write-path-census-v3.py`
(`w1/T47ExecDeadCode.md`). Nothing is deleted this round: both tools are pinned by sha256 in the standing rows (editing them changes the rows) and their deletion is routed. Counting command:
`python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py` (exit 1 while the two findings stand; planted-case non-vacuity in the report).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift + vacuous | `corpus/lessons/round-46.md:42` prints `9.8 %-16.3 %`; the snapshot holds `9.8 %–16.3 %` (U+2013); round-46 spot-check defect 4 | none (QUALITY 79 and 87 compare through the counter's `fold`, which maps U+2013 to `-`) | `.ufo/evidence/round-47/quality/lesson-quote-check.py` + QUALITY criterion 91; red before: `python3 … corpus/lessons/round-46.md` exits 1 (`LQ FAIL tum-portal-flaky-failures.html`); green after the one-character delta (`.ufo/evidence/round-47/quality/c91-lesson-quote-red-green.stdout`); selftest 11/11. This lesson's own Gate quotes are its first live input |
| scope + vacuous (C2 target) | `w1/T47CritC2Control.md` (a): a differential oracle (the pristine counter embedded as a packed string under an `_x` name, exec'd, every rule compared) scores `killed=160 neutral_killed=0 C2_R47_PASS=true` with no new rule case; `extra_*` and `_x*` are exempt from the pool by design | none (the neutral set refuses pins, not oracles) | the deciding run adds `ADDITION_LINT_OK` (`.ufo/evidence/round-47/quality/addition-lint.py`: no exec/eval/compile, packed payload, oversized literal or verbatim copy of rule code in any addition), QUALITY criterion 93; selftest 7/7; falsifier: the planted oracle is refused, the nine real additions pass. The frozen counter, pool and target are unchanged; the cheat is disclosed beside the claim |
| landing (pins self-referential) | `w1/T47CritC1Control.md` §3-4: editing the C1 counter and the hash constant inside it together passes `self_pin` and `stmts_pin`; a rewritten tool under an unchanged `sha_file` path passes because `tools/` was outside the frozen diff | `deciding-run.sh` `FROZEN_UNCHANGED` (counters only) | `FROZEN` now also lists `tools/` and the evidence directories the 22 statements pin by sha256 (`git diff FREEZE..REV` over them is empty at the deciding revision) |
| attribution | the package copy of `r8-flakiness-not-static.md` attributes arXiv 2607.09345 to Baltes, McKim, Zaidman and Wagner; the snapshot lists Gültekin, Berndt, Bell, Bach, Baltes (`w1/T47ExecMirror.md`) | CORPUS.md rule 1 (re-open the source), not any counter | the re-grounded entry carries the snapshot's authors; no counter reads authors (routed: a located-name check is not built this round) |
| provider/scope | `/tmp` filled to 100% mid-wave: each C1 counter pass clones the lane twelve times (about 2.3 GB) and one seat held 16-20 GB; two probes died on ENOSPC (`w1/T47ExecObsD.md` blocker note, orchestrator message) | none | seats relocated scratch to `/var/tmp`; wave 2 context names `/var/tmp/tameshi-r47-<seat>`; the deciding script defaults its work dir to `/var/tmp`. No claim read a result from a run that died on ENOSPC |

Sweep that found no further mistake in the round-46 landing: `grep -c '^| ' ` of the round-46 `## Mistakes` table is 9 rows, all with a fix named; rows 5, 6, 9 and 11 of the scout's candidate table
(`w1/T47ScoutMistakes.md`) are landed fixes, not new mistakes.

## Hardening and standing results

C2: `python3 .ufo/evidence/round-47/hardening/pool.py --lane LANE --rev REV --targets v2`; baseline `killed=122` of 183 (`before/pool-base.stdout`). C1: `python3 .ufo/evidence/round-47/calibration/measure.py --lane LANE --rev REV --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b --work EMPTY_DIR`;
at the freeze `total=22` (every row lacked the clause; `before/c1-at-freeze.stdout`); observed dependence sets: `six-leg regression ledger` {fleet-root, node}, `effective expectation reconciliation` {jj},
`retained invocation-context gate` {fleet-root}, `hermetic env-differential probe` {env, node}, `mutation report interop` {node}; the other 17 observed `none`. C3: `python3 .ufo/evidence/round-47/coverage/measure.py --lane LANE --rev REV`; before `rows=0 entries=0`.
The deciding values are in the report and SCORECARD.md; this lesson carries no after number.
