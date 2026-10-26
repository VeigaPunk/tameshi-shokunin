# T48ScoutPackage — assimilation check (read-only), round 48

## Recommendation

**`Assimilation: none`.** Reasons:

1. Neither declared claim (C1 calibration, C2 freshness) needs a package row or entry. C2 refreshes the four held rows from their own live URLs.
2. Every staged row or entry that touches the four C2 documents is **already held** or **already adopted** (table below). None adds a new document.
3. The one candidate left over is a documentation-consistency item for C2, not an adoption. See "C2 hazards".
4. If the L1 wants a theme anyway, the least-bad one is the **round-3 snapshot-practice amendment** (`r3-snapshot-fixture-update-paths.md`, staged S196/S152). Weakest alternative: the F5 measurement block (r4–r7, r13 — 12 own-work rows). Both are off the C1/C2 axes and cost a quality criterion apiece, so no.

## Staged themes (`merge/tameshi/MERGE-REPORT.md`, 103 rows S153–S255, 86 entries, 4 `amendment`s)

| theme (rounds) | what it is | lane status |
|---|---|---|
| F1 golden/diff vocabulary (r1) `golden-comparison-verdict.md` (S153/S154 → held S105/S106) | three-valued compare, explicit update flag | **held** (dedupe map S153→S105, S154→S106) |
| F3 flaky-aware verdict, measurement half (r1, r5, r6, r8, r10–r13, r15) | `flaky-aware-verdict-evidence`, `r5-undetected-flaky-failures`, `r6-flaky-failures-cluster`, `r8-flakiness-not-static`, `r8-flaky-cost-baseline`, `r9-false-red-rate`, ... | **adopted** in rounds 46–47: S258 (S195), S259 (S190), S260 (S216), S261 (S155-entry's Gruber paper), S262–S264 (S158, S206, S207). Rounds 43–45 deferred S155/S158 by document: S155/S156/S159/S160 are held as lane S155/S156/S159/S160 dedupes |
| PIT vocabulary, survivor classification, change-aware resweep, LLM mutants (r1, r7, r8) | `pit-outcome-vocabulary`, `survivor-classification`, `change-aware-resweep-cadence`, `llm-mutant-equivalence-cost`, `r7-llm-era-criteria-cost`, `r8-predictive-test-selection-cost` | not adopted. F7 prediction/cadence half. Off-axis for round 48 |
| CJK / Japanese literature (r1, r2, r3, r7, r16) | `mutation-score-semantics-cjk`, `cjk-mutation-metric-and-tool-comparison`, `r3-cjk-test-suite-effectiveness`, `r7-metamorphic-oracle-chinese`, `r16-*` | not adopted (round 45 took S202/S203 as S256/S257 by document only) |
| F4 golden/snapshot practice (r3, r6, r7, r8, r11, r12) | `r3-snapshot-fixture-update-paths`, `r6-snapshot-practice-corpus`, `r8-golden-update-flag` (amendments), `r4-gate-write-path-audit`, `r5-gate-write-site-census-corrected` | S209→S107, S196→S152 held. Own-work census rows not adopted |
| own-work F1/F5 instrument blocks (r2, r4–r7, r9–r15) | 30+ entries. Staged rows cite `lanes/tameshi/roundN/evidence/*` receipts that are not in this lane | not adoptable without the receipts; round 46 reserved the ids, adopted none |
| landing kit / interop schema (r9, r14, r15) | `r14-landing-kit`, `r9-mte-schema-vocabulary` (S211→S002 held) | not adopted |
| PBT / GoogleTest (r1, r2, r8) | `pbt-generator-*`, `r8-gtest-*` (S204→S256, S205→S257 adopted round 45) | partly adopted |

Lessons grep: round-43 `Assimilation: none`; round-44 `none`; round-45 adopted S256/S257; round-46 adopted S258–S260; round-47 adopted the F3 measurement half as S261–S264. This matches the task brief.

## Do any staged rows or entries concern S026, S048, S093 or S108?

| held row (document) | staged row/entry on the same document | disposition |
|---|---|---|
| **S026** Google flaky-tests blog (rendered page) | **S212** (feed list `feeds/posts/default?alt=json&max-results=200`), **S216** (per-post feed `.../6277555988217606236?alt=json`), amendment entry `r10-blog-carrier-reachability.md` (says S026's body is inside `<script type='text/template'>`), also `r13-flaky-false-red-rate`, `r9-false-red-rate`, `r13-f7-cadence-and-floor` | **S216 is already adopted as lane S260** (round 46, same feed document). S212 is a second row for the same document with a different carrier: not adopted. This is a C2 *candidate* under CORPUS.md rule 1 only in the sense that the package carries the carrier defect — see hazards |
| **S048** PIT incremental analysis | **none** (`grep -i 'pitest.org/quickstart/incremental'` over `SOURCES.append.md`, `knowledge/`, `amendments/` → 0 hits; only S155/S156/S159/S160 are PIT pages, and those are held) | no candidate |
| **S093** bubblewrap `bwrap.xml` | **none** (`grep -i -E 'bubblewrap\|bwrap'` → 0 hits in SOURCES.append.md) | no candidate |
| **S108** zh-cn TFF golden tests | **S210** (zh-cn page via **web.archive.org `2026id_` capture**, stated reason: the live page OAuth-loops for browser UAs), **S209** (upstream `golden_tests.md` at commit 4d3a89c9, = held **S107**), amendment `r8-golden-update-flag.md` (append to lane's existing entry of the same name; lane entry already cites S107 and S108) | S209 held (S107). S210 not adopted; same document as S108 with a different carrier. **No staged row supplies a live-page snapshot** — C2 must fetch it itself |

So: no staged row *requires* a C2 change; the package overlaps S026 and S108 only through alternative carriers.

## Id-collision commands (addendum commands, scratch only)

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' merge/tameshi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

- `reg-ids` **124** (S001–S037, S040–S097, S099–S108, S132, S152–S160, S256–S264); `staged-ids` **103** (S153–S255).
- `collisions` **8**: S153 S154 S155 S156 S157 S158 S159 S160. Unchanged from rounds 44–47 (S261–S264 are above the staged max, so adopting them added no collision). Next free id above both: **S265**, matching the contract.
- Collision-by-document map still holds: S153→S105, S154→S106, S159→S155, S160→S156 are dedupes. S155/S156/S157/S158 as *lane* ids are different documents and cannot take the staged rows' ids. Any adoption needs `tools/staged-id-guard.py` with a map; none is needed for `none`.

## C2 hazards found while checking (read-only, live fetches into scratch, all 2026-10-26)

All five fetches returned HTTP 200 with no redirect, with `curl` and with a `Mozilla/5.0` UA.

| target / URL | bytes | contract required phrase present after the amendment-2 extraction (drop `<script>`/`<style>` contents, strip tags, unescape, collapse whitespace) |
|---|---|---|
| S026 rendered page | 236 387 | `84%` yes. Also `84% of the transitions we observe from pass to fail involve a flaky test`, `1.5%`, `hardly a perfect solution` |
| S026 feed (per-post JSON; the S260 carrier) | 8 353 | `84%` yes (same sentence) |
| S048 `pitest.org/quickstart/incremental_analysis/` | 8 892 | `should therefore be prioritised` yes |
| S093 raw tag URL `raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml` | 33 289 (same size as the row's 33289-byte digest) | `--unshare-all` and `--unshare-cgroup-try` yes |
| S108 `tensorflow.org/federated/golden_tests?hl=zh-cn` | 104 924 | `--update_goldens` yes: `...可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。` |

Points for the C2 builder and L1:

1. **S026 body location.** On the rendered page the `84%` sentence occurs twice, at byte offsets 34455 (inside `<script type='text/template'>`, which the contract extraction drops) and 40624 (inside the `<noscript>` fallback copy, which the contract extraction keeps because it strips only script/style). The quote is therefore located today, but only via the `<noscript>` copy. This is why `r10-blog-carrier-reachability.md` and S260 exist. A seat or counter that also drops `<noscript>`, or an `html.parser`-based extractor that treats it as raw text, would lose the quote. The feed route is robust (JSON has no tags), but S026's row URL is the rendered page. Under amendment 1 the receipt `url` must be in the set of https URLs in R's source and anchor cells, so R can carry both URLs. R's source cell must carry T's base URL (the rendered page). A JSON snapshot quote must avoid JSON-escaped characters (`\"`, `\u003c`); the 84% sentence has none.
2. **S093 URL set.** The base URL is the GitHub blob page, which returns 200 HTML. The bytes come from the raw URL at the same tag. Amendment 1 covers this, provided both URLs appear in R's source/anchor cells.
3. **Snapshots are not byte-stable.** Two fetches differ in sha256 for the dynamic pages (TFF, Google blog, PIT: three distinct 12-hex prefixes observed across my fetches in this seat, not compared to any other fetch). Only the committed snapshot's digest matters for the contract, but the live-fetch comparison at the deciding run must either compare extracted text or not require digest equality. I did not test which `measure.py` does.
4. **S108/S210.** The live zh-cn page was reachable without the OAuth loop that S210 reports, from this host and with both UAs. The Internet Archive carrier is not needed for round 48. The staged S210 note does not apply today, but a different UA or header set may reproduce it.

## Bounds kept

Nothing written in `/home/vgpnk/Projects/shokuknow`, the lane, jj state or the Git index; no counter run; no tool installed. Network fetches were GET-only into `/fast/scratch/hyaku/tameshi-r48/T48ScoutPackage/`, which is deleted at the end of this seat.
