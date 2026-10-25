seat: T46RevRows
item: review registry rows S258/S259/S260 in `corpus/SOURCES.md` (lines 133-135) against the CORPUS.md SOURCES.md contract v1 and the three committed snapshots; checks: 13 pipe-split cells, no `|` inside cells, URL = document's own URL = counter's frozen doc key, snapshot path exists and anchor 8-hex = sha256 prefix, scope/teaches/kind/tier/used-by correctness, id uniqueness, sources-census diff, and the three Gate quotes in `corpus/lessons/round-46.md` (≤25 words, located in the folded snapshot, labeled token count).

Lane tree at review time: `git log -1` → `eada0b36d4c9e6380d111d2037acd97cdf91d2eb`; `git diff 6f2168e… -- corpus/SOURCES.md` → empty, so the reviewed rows are exactly the content-revision bytes.

## Verdict

Rows S258/S259/S260 pass every check in the item. One HIGH and one INFO finding, both in the surrounding ledger, not in the three row cells.

## Findings

### HIGH — `## Id allocation` ledger is stale: "Next unused id: S258" while S258-S260 are used (SOURCES.md:470)

- Attack: the id-allocation record the row-append discipline maintains at the tail of `corpus/SOURCES.md`.
- Evidence: `sed -n '470p' corpus/SOURCES.md` → `- Next unused id: S258 (the staged-id guard's safe floor after this append; staged ids S161–S255 stay reserved by document for the package).` That is the round-45 line; after the round-46 append of S258/S259/S260 (`corpus/SOURCES.md:133-135`) it is false. Per the round-46 lesson (`corpus/lessons/round-46.md:73-74`) and `assimilation/adoption-map.json`, S261-S264 are additionally map-only reserved, so the honest floor is S265. `grep -n 'Round 46\|round-46\|S261' corpus/SOURCES.md` → no block anywhere in `## Id allocation` (or the file) records the round-46 append; every earlier round (41, 42, 43, 44, 45) appended its block plus a new pointer.
- Impact: none on the counters — `measure.py` and `staged-id-guard` read the registry rows themselves, not the pointer. But this is the same failure class the round fenced with QUALITY criterion 90 (id collision across concurrent work): a future seat reading the ledger would be told to append at an already-used id, and S261-S264's reservation is recorded nowhere in the file. Silent staleness, not a cell defect. Reproduced: the line reads as quoted at both the working tree and `6f2168e` (diff empty).

### INFO — `used-by` omits the round-46 lesson that cites the rows (convention drift, matches recent rounds)

- Contract cell rule: "used-by — repo-relative paths of the knowledge entries or lessons citing the row." `corpus/lessons/round-46.md` cites S258/S259/S260 throughout (lines 9, 19, 32, 48, 73, 80, 108), and older rows list lessons/tools that cite them (S102 → `tools/tally-audit-v3.py, corpus/lessons/round-35.md`; S104 → `…round-37.md`). S256/S257 (round 45) and S160 (round 44) also list only the knowledge entry, so the new rows follow current practice; the drift is that the lesson citation is now consistently unlisted. Recorded for the ledger, not counted as a row defect — the counter's used-by contract (the citing entry path is a member of the cell) is satisfied: `measure.py` `entry_ok` checks `path in rows[c]['used']`, and `r5/r6/r9` are exactly the three members.

## Passed checks (each with command and output)

1. **13 pipe-split cells, no `|` inside any cell.** Python split of lines 133/134/135: each `fields=13` (11 cells + 2 edge empties); cells 1-11 = id/source/kind/tier/scope/anchor/teaches/status/opened/recheck/used-by in order. Census awk equivalent over the whole file: `malformed: 0` on 120 rows.
2. **URL = document's own URL = counter's frozen doc key.** `measure.py:43-47` DOCS = `arxiv.org/abs/2504.16777`, `portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures`, `testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`. Row source cells carry exactly these after `doc_key` normalization (`measure.py:67-69` strips scheme/`www.`/trailing slash; the row's S259 URL has a trailing `/`, normalized equal). Each is the document's own canonical URL: the arXiv abs page, the TUM portal record (DOI in scope cell resolves to 202-empty per the lesson), and the publisher's per-post feed record (its `entry.link[rel=alternate]` is the rendered page already held as S026 — a second carrier of the same document, honestly disclosed in `r9-false-red-rate.md:10`).
3. **Snapshot path exists; 8-hex prefix = sha256.** `sha256sum .ufo/evidence/round-46/coverage/sources/*`:
   - `28d2954d…` arxiv-2504.16777-abs.html (row anchor `sha256 28d2954d`) — match, file 43,376 B = lesson's (43,376 bytes).
   - `5eb59adf…` tum-portal-flaky-failures.html (row `5eb59adf`) — match, 51,850 B.
   - `434d8658…` google-flaky-feed-6277555988217606236.json (row `434d8658`) — match, 8,353 B; 0 newlines, consistent with the entry's field-level citation claim.
4. **scope states only what the row grounds.** All three scope to F3 claims each snapshot supports: S258 clustering-with-shared-root-causes ("co-occurring failures that share the same root causes" present in folded text); S259 same-job rerun as detection mechanism and blind spot ("rerun failed tests within the same job to identify flaky failures … overlooking undetected flaky failures", ×4); S260 false-red prior ("about 84% … involve a flaky test", "common to ignore legitimate failures in flaky tests"). S259's scope also carries the DOI `10.1109/TSE.2026.3729363`, which is verbatim in the snapshot metadata (×8 occurrences).
5. **teaches supported by snapshot text** (extracted with `python3 .ufo/evidence/round-45/freshness/measure.py --extract <snapshot>`, then folded per `measure.py::fold`):
   - S258 "75% of the 810 flaky tests … 10,000 test suite runs across 24 Java projects … mean size 13.5": snapshot holds "75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5" (×1), "dataset of 10,000 test suite runs from 24 Java projects", "It contains 810 flaky tests" (×1). Supported.
   - S259 "9.8%-16.3% of failed pipeline runs across 8.8 billion test executions in four industry-scale projects, spiking on code changes and test reordering": "9.8 %-16.3 % of failed pipeline runs" ×3, "8.8 billion test executions from four industry-scale projects" ×4, "spike temporarily, triggered primarily by code changes and test reordering" ×4. Supported.
   - S260 "84% … so legitimate failures get dismissed as false positives and a red build is more likely a flake than a defect": post states "about 84% of the transitions we observe from pass to fail involve a flaky test", "It is quite common to ignore legitimate failures in flaky tests due to the high number of false-positives", "developers dismiss a failing result as flaky only to later realize that it was a legitimate failure". Supported.
6. **kind/tier justified.** S258 `paper|A` original arXiv paper; S259 `paper|A` original TSE paper via institutional record; S260 `docs|A` — official publication venue record, same `docs|A` as the lane's own S026 row for the same document (`SOURCES.md:37`); `community` is never A but a publisher per-post record is not `community`.
7. **used-by lists exactly the citing entry.** r5/r6/r9 each carry `source: S25x —` on line 1; grep of `corpus/` for `S258|S259|S260` outside SOURCES.md finds only those three entries, `corpus/README.md:573-575` (index rows), and the lessons (see INFO). All three used-by paths exist.
8. **ids unused elsewhere / no duplicates.** Per-id counts: `grep -cE '^\|\s*S25x\s*\|' corpus/SOURCES.md` = 1 row each; `grep -c S25x .ufo/evidence/round-46/assimilation/reg-ids` = 0 each (ids were unused at freeze; reg-ids has 117 ids); staged-ids = 0 each. Round-45 lesson's map-only targets S258-S261 (`round-45.md:74`) were never appended — the round-46 lesson states this and the registry confirms it. Duplicate-id census: `awk … | sort | uniq -d` prints nothing.
9. **Census.** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0; `diff` vs `evidence/round-46/census-start.stdout` → identical (11 baseline lines: 10×W04 + 1×W01, zero E codes). No new W/E codes; no duplicate-URL warning between S026 and S260 (different URLs).
10. **Gate quotes (rule 1: ≤25 words, located, labeled).** Located with the counter's own `fold` (NFKC + quote/dash fold + whitespace collapse):
    - S258: "finding that 75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests" — 22 tokens (label: 22), occurrences 1. ✓
    - S259: "We found that, across all projects, undetected flaky failures account for 9.8 %-16.3 % of failed pipeline runs." — 18 tokens (label: 18), occurrences 3 — the lesson itself discloses the ×3 (abstract appears three times on the page). ✓
    - S260: "about 84% of the transitions we observe from pass to fail involve a flaky test" — 15 tokens (label: 15), occurrences 1. ✓
    All three ≤25 words and the lesson labels match measured counts.
11. **Other cells.** `status` = `mined` and each row is cited by ≥1 used-by path (contract definition). `opened` = 2026-10-25 = lesson access dates. `recheck` = `365d` is a valid cadence. Anchors name exact section + revision: S258 "§Abstract @ arXiv:2504.16777v1 (submitted 23 Apr 2025)" — "[Submitted on 23 Apr 2025]" and "arXiv:2504.16777v1" both in snapshot; S259 "IEEE TSE, accepted/in press 2026" — "State Accepted/In press - 2026" in snapshot; S260 post id `tag:blogger.com,1999:blog-15045980.post-6277555988217606236` and `published 2016-05-27T17:31:00-07:00` in the JSON record. No bare homepages.

## Informational counter run (not the deciding run)

`python3 .ufo/evidence/round-46/coverage/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32` → `C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=6f2168e… C3_R46_PASS=true`, exit 0 (run from `/tmp/tameshi-r46-T46RevRows`; read-only `git show`/`ls-tree` against the lane). Observed only; the deciding run is the L1's.

## Not run

- No live re-fetch of any URL (lane is a snapshot-pinning corpus; the frozen snapshots are the surface under review).
- No `--selftest` of the coverage counter (out of this item's scope; C2 seats own counter hardening).
- No tools installed (pacman paused; none needed).
