# T58W2CritC3 — C3 installed-state attack (F9 entry + S286–S288)

Round 58 wave 2 · lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` · base `2a32aa8228d5f86a85c81a923a3148bf792a9538` · C0 `8063d0a551fc5b3cb5a2d397da7353af53444534` (verified lane head; base is an ancestor; checked corpus files porcelain-clean).

**Verdict: `gap-minor`.** All four item checks hold on the installed state except one README cell that no longer matches reality (finding F1, minor). Receipts: `T58W2CritC3-receipts/01…12`. Machine-readable twin: `T58W2CritC3.json`.

## (a) Counting commands — PASS

At the C0 clone:

| command | output |
|---|---|
| `grep -rl 2406.09843 corpus/knowledge \| wc -l` | `1` |
| contract's verbatim `counting_command` (`.ufo/evidence/round-58/contract.json`): `grep -rl '2406.09843' corpus/knowledge \| wc -l && grep -cE '^ {0,3}\| S(286\|287\|288) ' corpus/SOURCES.md` | `1`, `3` |
| per-id uniqueness `grep -cE '^\|[[:space:]]*S28[67 8]…\|'` | `1`, `1`, `1` |
| before-state: `git grep -l 2406.09843 2a32aa8… -- corpus/knowledge \| wc -l` | `0` |

The single F9 file is `corpus/knowledge/llm-mutant-equivalence-cost.md`; exactly three new registry rows exist, each once (receipts 02).

## (b) CORPUS rule 4 — PASS, with a wording caveat on the item itself

Verbatim rule 4 (fleet `CORPUS.md`, receipt 05) is **"Expansion is knowledge, not rows"** — not the seat item's paraphrase ("every appended row is cited by the admitted entry"). The used-by/uncited-row obligations live in the census block of the same file (mined rows) and in the round-58 contract predicate "the rows cite no more than the entry cites (CORPUS rule 4)". The installed state satisfies all of these:

- `git diff base..C0 -- corpus/SOURCES.md` shows exactly three appended rows plus one removed lead bullet (the arXiv lead, removed after S286 landed — the recorded S040–S046 precedent); S285 byte-untouched (receipt 03).
- S286 mined, S287 mined, both `used-by=corpus/knowledge/llm-mutant-equivalence-cost.md`; the entry's `source:` headers cite both ids and name no other row (`grep -cF S288 entry` → 0). S288 is `rejected`, `used-by=—`, cited by nothing — the rule-2 correction-row shape (supersedes S285), not an uncited expansion row (receipt 04).
- Under the item's literal paraphrase S288 would read as "an uncited row appended"; under the verbatim rule + census it is correct. No installed defect; the paraphrase mismatch is recorded for the L1.

## (c) Boundary honesty — PASS

The entry's `## Boundary of this entry` states verbatim: "The numerical transfer is **not measured**: no lane sweep has produced an LLM-generated mutant; this entry supplies a counting contract, not a pilot", and closes with "The F9 pilot move … remains unmeasured; this entry does not close it." It also carries the corrected source-gate distinction ("S286 reports a higher overall equivalent-mutant rate; it does not establish equivalence conditional on survival"). Interpretation claims carry `Inference:` labels. Every quoted source string was verified verbatim against the committed extracts: arXiv abstract ("equivalent mutant rates" ×1, "111.29% higher fault detection", "26.60, 10.14, and 3.51 percentage points, respectively", "851 real bugs from two Java real-world bug benchmarks"), deck extract lines 230–241 (class definition at 231, score-precision hazard, undecidability at 241 — all three quoted sentences byte-present), Atlassian extract ("severity of level 2 or higher" ×1). Receipts 06, 07.

## (d) README F9 row — DRIFT (finding F1, minor)

The live row `corpus/README.md:86` was updated this round in the candidate-sources cell (`+ S286, S287`, all six rows exist — receipt 12) and the status cell (`open — equivalence-cost contract entered (round 58, knowledge/llm-mutant-equivalence-cost.md); bounded pilot unmeasured` — true of the installed entry). The coverage-map addendum row (line 659) matches the entry and cites exactly S286/S287.

**F1.** The same row's last column still opens **"no LLM-specific search run yet (U)"** — false at C0: the round opened the previously-unopened arXiv LLM-mutation lead (converted to mined S286, lead bullet removed) and the S287 deck, both now mined with used-by → the F9 entry. The cell contradicts the row's own status cell.

```
cd /fast/scratch/hyaku/tameshi-r58/T58W2CritC3/clone
git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/README.md | grep -n '^| F9'
grep -n '^| F9' corpus/README.md
git diff 2a32aa8 8063d0a -- corpus/SOURCES.md | grep -- '- \*A Comprehensive Study'
```
Output (abridged): BASE:86 `… | open | no LLM-specific search run yet (U) → bounded pilot … |`; C0:86 `… | open — equivalence-cost contract entered (round 58 …) … | no LLM-specific search run yet (U) → bounded pilot … |`; diff removes `*A Comprehensive Study on Large Language Models for Mutation Testing* — https://arxiv.org/abs/2406.09843.` from the leads.

Smallest safe correction: update only that cell's before-state (one-cell README edit, no registry/entry bytes), e.g. "LLM-mutation literature searched (S286/S287 mined, round 58); bounded pilot unmeasured → bounded pilot with an independent outcome check" — or, if the L1 reads before→after cells as frozen move descriptors (house precedent: F3–F5 rows kept their old before-cells), record as accepted staleness and route.

## Supporting installed-state checks

- Pre-append receipts committed at C0: `assimilation/collisions` = S153–S160 (matches the corrected lesson), `scratch-census.exit` = 0 with "file ok" on the pre-append scratch mirror (`…/forecast-overlay/corpus/SOURCES.md`), `census-before.exit` = 0. All landed with the append and entry in one ancestor commit `d28c3044` (receipt 10, 11). The fleet round-end census receipt does not exist yet (round not closed) — closeout item, not this seat's.
- CORPUS census in the C0 clone: rows=148, malformed=0, no missing mined used-by paths, id-cite OK (receipt 08).
- `content-precheck` at C0 is RED (`COLDREAD_PRECHECK … lost=17` at `0fdb71d2`) — the cold-read credit drift this wave's reader seats audit; noted, not a C3 predicate.
- `corpus/knowledge/receipt-revision-binding.md` diff is the R56.3 recheck-cell correction (GATE_SELFTEST 14/14 → 19/19); unrelated to F9.

## Honesty

- Live refetches (recheck `curl` commands) were **not** run: cadence 365d, not due; all quote verifications above are against committed extract bytes, which is what the entry claims.
- Commit-order reading ("receipts ran before the append") rests on receipt content (scratch-mirror paths); commit-wise the receipts and the append share `d28c3044`. Stated as recorded fact, not inference.
- "The search ran" is evidenced by the lead→row conversion and two mined rows (commands above); no separate search-log artifact was audited beyond what SOURCES.md and the lesson record.

## Cleanup and tooling

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2CritC3` (shared clone) **deleted before yield**. No lane or evidence files edited; no tooling installed (no installs to record).
