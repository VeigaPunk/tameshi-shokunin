seat: ConnPackageCross
item: cross-map of the shokuknow merge/tameshi package (103 staged rows S153–S255, 86 entries) against the lane registry (117 rows) and frontier F1–F10; (a) same-document staged→held matches, (b) open-ground candidates ranked by staged rows × fetchability, (c) other staged citations of the three adopted documents.

Method: read-only. Package files read from /home/vgpnk/Projects/shokuknow/merge/tameshi (SOURCES.append.md, MERGE-REPORT.md, knowledge/corpus/knowledge/); lane files read from the checkout (corpus/SOURCES.md, corpus/README.md); round-46 assimilation receipts read (adoption-map.json, guard-map.json, staged-ids, reg-ids, collisions). Scratch under /tmp/tameshi-r46-ConnPackageCross/. All parsing in one Python pass over copied files (cp ... /tmp/tameshi-r46-ConnPackageCross/; 109-line staged file, 467-line lane file). URL equality = same string modulo scheme (http/https), leading www., trailing slash (no other normalization). HTTP probes = `curl -sIL -m 20` (one `GET` confirmation for the Kyoto page). No lane writes beyond this report.

## (a) staged rows citing a document the lane already holds (same URL modulo scheme/www/trailing slash)

Rows parsed: staged 103 (S153–S255), lane 117 (S001–S160, S256–S257). Match rule: any normalized URL in a staged row equals any normalized URL in a lane row. 11 staged rows hit held rows:

| staged id | lane id | shared URL |
|---|---|---|
| S153 | S105 | https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html |
| S154 | S106 | https://raw.githubusercontent.com/google/golden/master/golden.go |
| S159 | S155 | https://pitest.org/quickstart/basic_concepts/ |
| S160 | S156 | https://pitest.org/faq/ |
| S196 | S152 | https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download |
| S202 | S256 | https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md |
| S203 | S257 | https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md |
| S209 | S107 | https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md |
| S211 | S002 | https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json |
| S212 | S026 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html |
| S216 | S026 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html |

Notes: S202/S203 are already adopted lane rows from round 45 (README round-45 block names staged S202/S203; the package kept the staged rows). S212/S216 both carry the rendered-page URL of the same Google post in their row text (their citation carriers are feeds, see (c)). The guard's adoption-map/dedupe recorded 4 of these 11 (S153/S154/S159/S160); S196, S202, S203, S209, S211, S212, S216 are 7 same-document matches the guard receipt does not list (guard-map.json `map_dedupe` has only S153/S154/S159/S160; `collisions` only S153–S160).

## (b) package themes still new ground for F1–F10 after this round's three entries, ranked

Open after round 46: F3 (measurement half; this round adds literature only), F6, F7, F9, F10, F8 (partly held), F1b (NoCoverage, under held F1). F5 is Core (round 21) and is not new ground; F4 is partly held. Counts = staged rows whose declared scope names the ground, external only (kind ≠ own-work), excluding adopted (S190/S195/S216/S225), refused (S204), and dedupe-to-held rows (S153/S154/S159/S160/S196/S202/S203/S209/S211/S212). HTTP status = `curl -sIL -m 20` final code (GET-confirmed where noted).

| rank | ground | staged candidate rows (external) | fetchability of probed URLs |
|---|---|---|---|
| 1 | F3 (flaky-aware verdicts / determinism) | S155 (arXiv 2302.09330), S158 (mir.cs.illinois.edu LamETAL20 PDF), S169 (juse.or.jp SQIP PDF), S171 (DOI 10.1109/TSE.2026.3685588), S206 (arXiv 2607.09345), S207 (Semantic Scholar API for ICST'24 DOI) — 6 tagged; flaky-adjacent untagged: S237/S248 (arXiv 2602.09311 abs/html), S241 (Google feed post 5678277460708842788), S252 (TUM SSE index) | 200 ×9; S171 DOI → 202 IEEE landing (ieeexplore.ieee.org/document/11540001/) |
| 2 | F7 (incremental re-sweep granularity) | S161 (DOI 10.1145/3540250.3558911 — ACM), S162 (arXiv 2212.11762), S205 (arXiv 1810.05286), S206 (arXiv 2607.09345), S207 (Semantic Scholar); cadence/quarantine same-theme: S241, S243 (qam-hub), S244 (flakyguard) + S236 (own-work decision) | S162/S205/S206/S207/S241/S243/S244 200; S161 ACM 403 on HEAD |
| 3 | F10 (PBT generators for gate fixtures) | S157 (DOI 10.21105/joss.01891), S170 (Tufts QuickCheck experience PDF), S182 (DOI 10.1145/351240.351266 — ACM), S183 (smallbone.se lic.pdf), S166 (zenn.dev), S199 (cjc.ict.ac.cn) — 6 | S157→200 JOSS, S170/S183/S166/S199 200; S182 ACM 403 on HEAD |
| 4 | F9 (LLM-era mutant generation + equivalence) | S156 (arXiv 2406.09843), S165 (pdf.dfcfw.com), S168 (jos.org.cn 2024/7/7113), S200 (arXiv 2609.09315) — 4 | all 200 |
| 5 | F6 (fixture minimization for survivors) | S167 (Purdue delta-debugging PDF), S177/S192 (Kyoto IEICE guide; same URL), S197 (archive.org capture of Osaka Univ pman3) — 4 rows / 3 docs | S167/S197 200; Kyoto `curl -sIL` 404 but `curl -sL` GET 200 (HEAD refused; reachable) |
| 6 | F8 (oracle anchoring) | S166 (zenn.dev), S181 (jos.org.cn 6953), S199 (cjc.ict.ac.cn) — 3 | all 200 (F8 partly held, hence last) |
| 7 | F1b (NoCoverage classification, under held F1) | no row targets F1b directly; metric-definition rows S163 (Huawei CodeArts), S164 (GIST slides), S168, S181 could inform the denominator choice | S163/S164/S168/S181 200 |

Ranking logic: F3 first (6 tagged external rows, all reachable, and the round's own entries leave its measurement half open); F7 second (5 tagged + 4 same-theme external rows; one ACM 403); F10 third (6 rows; one ACM 403); F9 fourth (4 rows, all 200); F6 fifth (3 docs; one HEAD-404/GET-200); F8 sixth (3 rows; partly held); F1b has no package candidate.

## (c) other package entries citing the three adopted documents

Adopted: S195→S258 (arXiv 2504.16777), S190→S259 (TUM portal record of TSE 2026 undetected-flaky-failures), S216→S260 (Google Testing Blog per-post feed 6277555988217606236?alt=json). Searches: `grep -c 'portal.fis.tum.de'` = 1 (only S190); `grep -c '2504.16777'` = 1 (only S195); `grep -c '6277555988217606236'` = 4 (S216, S225, S229, S235); `grep -c '6277555988217606236' SOURCES.md` = 0.

| adopted doc | other staged rows citing it | disposition for the lane |
|---|---|---|
| arXiv 2504.16777 (S195) | none — S195 is the only staged row | no fold-in needed |
| TUM portal record (S190) | none — S190 is the only staged row; S252 (cs.cit.tum.de/en/sse/publications/) is the same group's *index*, a different document | no fold-in needed |
| Google Testing Blog feed post 6277555988217606236 (S216) | S225, S229, S235 (same per-post feed URL) and S212 (general feed `feeds/posts/default?alt=json&max-results=200`; row text also names the rendered page) — all five staged rows are the same 2016-05-27 Micco post | S225/S229/S235 dedupe to S260 per the adoption note; S212 is the same document too — fold/dedupe it to S260 as well, and note S212/S216's underlying document is already held as S026 (rendered page URL); the feed is a new carrier, not a new document |

## Risks / limits

- URL normalization is exactly scheme/www/trailing-slash; path-level equivalence (e.g. arXiv abs vs pdf, raw vs blob) is intentionally not treated as the same URL.
- Own-work staged rows (45 of 103) reference lane-internal receipts, not external documents; they are excluded from (a)/(b) but were parsed and counted (kind distribution: paper 26, docs 21, own-work 45, talk 3, community 3, spec 2, code 2, dataset 1).
- HTTP probes are `curl -sIL`; ACM DL returns 403 to HEAD (GET may differ for a browser UA — unprobed); the Kyoto IEICE page refuses HEAD but serves GET 200.
- The round-46 guard receipts (collisions, adoption-map) list 4 same-document dedupes + the 3 adoptions; this seat's full cross-map finds 7 additional staged→held matches ((a) table) and 5 staged rows for one adopted document ((c)).
