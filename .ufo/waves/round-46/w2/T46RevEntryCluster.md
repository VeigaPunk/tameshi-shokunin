seat: T46RevEntryCluster
item: Non-author claim-vs-source review of `corpus/knowledge/r6-flaky-failures-cluster.md` (row S258) against the committed snapshot `.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html`, with an extraction+fold pipeline independent of the lane's counter.

# Verdict: ADMIT

Every check in the item passed under my own measurement (details below). No BLOCKING/HIGH/LOW finding; two INFO observations.

## Reviewed state

`git log` HEAD = `eada0b3` (wave-2 spec commit). `git diff 6f2168e028ce7ff6e82ac92093ac05dd1f147c32..HEAD` over the entry, SOURCES.md, README.md, the snapshot and the package copy printed nothing — the reviewed bytes are the content revision's bytes. `cmp` of `corpus/knowledge/r6-flaky-failures-cluster.md` vs wave-1 deliverable `.ufo/waves/round-46/w1/ScribeEntryCluster.entry.md`: IDENTICAL. `cmp` of the committed package copy vs `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r6-flaky-failures-cluster.md`: IDENTICAL.

## Independent method (no lane counter code)

`/tmp/tameshi-r46-T46RevEntryCluster/audit.py`: `html.parser` text extraction skipping `script`/`style` (`convert_charrefs=True`), NFKC + `\s+`→space fold, substring test; a second pass tested each span verbatim (no NFKC) against whitespace-collapsed decoded text. The abstract block was extracted separately (`<blockquote class="abstract mathjax">`) to verify the `§Abstract` location claims. Result: 43,376-byte HTML → 5,155 chars page text, 1,714-char abstract.

## Checks

### 1. Quoted spans — all 15 verified

15 double-quoted spans (every line has an even `"` count, no span crosses a newline). For each: verbatim substring of the snapshot text (true under BOTH the NFKC fold and the raw decoded text — no Unicode hiding), true substring of the abstract block (§Abstract claim holds), and my whitespace-token count equals the stated `(N tokens)`:

| line | stated | mine | line | stated | mine |
|---|---|---|---|---|---|
| 12 | 14 | 14 | 20 | 22 | 22 |
| 14 | 21 | 21 | 20 | 6 | 6 |
| 16 | 20 | 20 | 22 | 11 | 11 |
| 16 | 13 | 13 | 22 | 17 | 17 |
| 16 | 18 | 18 | 24 | 16 | 16 |
| 18 | 24 | 24 | 24 | 17 | 17 |
| 18 | 19 | 19 | 32 | 8 | 8 |
| 20 | 12 | 12 | | | |

All 15 are inside the 6–25-token band. Line 8's claim "14 of the 15 located quotes do not occur in the committed package copy" verified: exactly the L20 `finding that 75% …` span occurs in the folded package text; the other 14 do not.

### 2. Header trio — exact

- Line 1 `source:` carries `S258`, `https://arxiv.org/abs/2504.16777`, the snapshot path, and prefix `28d2954d`. `sha256sum` of the snapshot = `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14`, `wc -c` = 43,376 — prefix matches.
- Line 2 `verified-at: 2026-10-25` — exact.
- Line 3 `recheck:` — **run verbatim**: `curl -fsSL 'https://arxiv.org/abs/2504.16777' | grep -c 'co-occurring failures that share the same root causes'` → `3`, pipeline exit 0 — equals the stated `→ 3`. Saved page: 43,376 bytes, sha256 `28d2954d…`, `cmp`-identical to the snapshot — so the parenthetical "(43,376 bytes, sha256, cmp-identical)" is true as observed 2026-10-25.

### 3. Numbers and names

Snapshot-side numbers all present in the snapshot text: 2504.16777 (5×), 1.28%, $2,250, 10,000 (2×), 24, 810, 75%, 13.5, 23 Apr 2025, 14:51:23, 79. Authors verified: `Owain Parry`, `Gregory Kapfhammer`, `Michael Hilton`, `Phil McMinn` each occur (the entry's "(Owain Parry, Gregory Kapfhammer, Michael Hilton, Phil McMinn)" is verbatim author list). Numbers not in the snapshot are all correctly attributed: `N ≥ 3` and `three-control` are lane ground (README:80 F3 row states `N ≥ 3 byte-identical controls`, entry cites it) and sit inside `Inference:` sentences; `14 of the 15`, `(N tokens)`, `365d`, `43,376`, and path `round-46` are self-audit/header material verified above. `GitHub`, `Java`, `networking`, `dependencies`, `machine learning`, `agglomerative` each occur in the snapshot. No unlabelled number or name found.

### 4. Negative claims — verified

Line 42: `Journal reference`/`Journal-ref`/`Comments` = 0 occurrences in extracted text AND in raw HTML (`grep -oi` → only `Subjects`×2). `arXiv:2504.16777v1 [cs.SE]`, `Submitted on 23 Apr 2025`, `Wed, 23 Apr 2025 14:51:23 UTC (79 KB)` each occur 1×. `CC BY` = 0 in text and raw HTML (the `abs-license` div holds only a linked icon `creativecommons.org/licenses/by/4.0/` with alt `license ic…` — the dropped `CC BY 4.0` clause was indeed not a visible-text statement, so dropping it was conservative and honest). Line 38: `mutation` = 0 occurrences in the snapshot — "contains no data on mutation survivors" holds. Line 44: `rerun`, `distribution`, `per-project`/`per project` = 0 — the "no rerun-blindness rate / no per-project rate / no distribution" boundary holds. Line 45: PDF is linked (4× `PDF`) but the entry correctly rests on the abstract page only.

### 5. Registry and index

- `corpus/SOURCES.md:133` row S258: last cell (used-by) = `corpus/knowledge/r6-flaky-failures-cluster.md` — the entry is listed.
- `corpus/README.md:573`: `` `knowledge/r6-flaky-failures-cluster.md` `` indexed with `S258` source cell.
- Anchor cell carries the snapshot path + `sha256 28d2954d` (row-review is T46RevRows' scope; noted only as used-by evidence).

### 6. Package comparison

Dropped from the package copy (verified none survives in the entry): `CC BY 4.0` (not visible text in the snapshot — justified); `tier A for its own scope` (lane grading); `S140, round 5: 9.8 %–16.3 %` rerun-miss cross-reference (not in this snapshot — the entry states so at line 44); "preprint, not peer-reviewed" (softened to "no peer-review status is claimed", matching zero `peer`/`review`/`Journal` hits); the fresh-environment-rerun prescription and "the lane has not classified any survivor set" (lane-state claims, not restated). Kept: the 75%/13.5 quote, `challenging the deep-seated assumption` (re-located within an 18-token span), the shared-root-cause premise, F8/F3 relevance, all `Inference:` marks. Added by the entry: 14 fresh located quotes (property, cost, data, measurement, cheap substitute, attributed causes), the quote/token-count/freshness self-audit, the F3 distinct-causes bound argument (upper bound on independent evidence; N ≥ 3 bounds distinct causes only from above — correctly directed), the F8 one-anchor-not-two restatement, the §4 fixture-craft bullets, the §5 boundary (sub-line granularity: venue facts, no per-project rate, body not fetched), and a re-grounded recheck probing `co-occurring failures that share the same root causes`.

## Findings

1. **INFO** — `r6-flaky-failures-cluster.md:32`: "An expectation that reads one member of such a cluster therefore reads the cause the other members also carry." is a deductive restatement of the quoted premise, not an observation — borderline inference presented without the `Inference:` label; the next sentence's stronger claim (survivor verdict tables overstate independent anchors) IS labelled, so the practice is right there. Judged acceptable: it is a tautology of the premise.
2. **INFO** — `:28`: "The snapshot says the failures such controls probe are not scattered" — the snapshot states 75% of flaky tests belong to clusters and mean cluster size 13.5; "most of them sit in clusters that share a root cause, and the clusters are large (mean 13.5 members over the authors' 810 flaky tests)" is a fair paraphrase with correct attribution (the 810 are the authors' tests, not the lane's). No overreach found; flagged only because the clause mixes the lane's controls into the snapshot's sentence.

## Residual risk / gaps

- The counter itself was not run (item required an independent method; the deciding run is the L1's). My fold is NFKC+whitespace; the counter's fold additionally maps curly quotes/dashes/NBSP — all quotes passed under BOTH my fold and verbatim raw text, so the difference cannot flip a located/non-located result.
- Quote positions reported are offsets in my extracted page text (e.g. `pos=624..2192`), not source offsets; ScribeRows' quote-vs-anchor offsets were out of this item's scope.
- `grep -c` counts lines not occurrences (page is minified); the entry itself documents this caveat in line 3.

## Bounds compliance

Lane checkout untouched except this report (read-only `git log`/`diff`/`rev-parse` only, no mutations). Scratch confined to `/tmp/tameshi-r46-T46RevEntryCluster/` (`audit.py`, `live-abs.html`). Package opened read-only. No installs, no pacman; tools used: python3 html.parser (stdlib), curl, grep, sha256sum, cmp, wc.
