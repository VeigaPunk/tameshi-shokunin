# T47ScribeEntryPredict — re-grounded entry draft for `corpus/knowledge/flaky-aware-verdict-evidence.md`

Seat: scribe, leaf. Claim touched: C3 (coverage), F3 measurement half. This report records only what was executed; the deciding runs of the C1/C2/C3 counters were not taken here and no pass is claimed.

## Behaviour

Drafted the replacement entry at `.ufo/waves/round-47/w1/T47ScribeEntryPredict.entry.md` (the L1 copies it to `corpus/knowledge/flaky-aware-verdict-evidence.md` after review). The lane checkout was not modified except that one deliverable file; `SOURCES.md`, `corpus/README.md`, git/jj state and every counter were left untouched.

Entry shape:

- line 1 `source: S261 — https://arxiv.org/abs/2302.09330 — §Abstract — arXiv:2302.09330v2; S262 — https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf — §I Introduction guidelines block (RQ1 & RQ3; RQ2 & RQ3), §V-C, §VI-B, §VII`
- line 2 `verified-at: 2026-10-25`
- line 3 `recheck: 365d — <sha256 of the Lam PDF, then grep -cF of an arXiv abstract phrase>`, with the statement that both checks were run against the committed snapshots, not the live URLs
- line 4 `ground: F3 — …`; then a title and the four required sections (What the sources state / What this means for fixture craft / What is not shown / Gate-relevant limits).

Quotation accounting (measured, see Verification): 40 straight-double-quoted spans in the entry, whitespace-token counts 6–22 after the counter's `fold`, all 40 located in at least one committed snapshot's normalized text, 37 of them absent from the committed package copy. Numbers carry a location in every case: `lam-2020-reruns.txt:NNN` for S262 and the arXiv `§Abstract`/metadata cells for S261, plus a 16-row number→location table inside the entry.

## Verification exercised

All commands run from `/tmp/tameshi-r47-T47ScribeEntryPredict` unless a path is absolute; scratch only.

1. Snapshot digests recomputed, matching the assignment exactly:
   `sha256sum arxiv-2302.09330-abs.html lam-2020-reruns.txt lam-2020-reruns.pdf` →
   `2965343c…6bc6` (HTML, 43,549 B), `bf52c908…25b9` (txt, 81,725 B), `0b880458…95d` (PDF, 565,435 B, `pdfinfo` Pages: 11).
2. arXiv abstract extracted twice (round-45 `freshness/measure.py --extract`, and an independent tag-strip + `html.unescape`), then compared to the abstract block read from the HTML.
3. Locator replicating the counter's `fold`/`norm_text` (`measure.py:63-89`): every straight-double-quoted span of 10–400 chars in the draft tested for membership in the folded arXiv snapshot, the folded Lam text, and the folded package copy. Result: `quotes: 40 located: 40 fresh: 37 bad: 0 min/max tok: 6 22`.
4. `entry_ok` simulated with synthetic `rows` built from the two snapshots and `used-by` containing `corpus/knowledge/flaky-aware-verdict-evidence.md`: cited rows `[S261, S262]`, located True, fresh True → `ok`. This is a probe of my own draft, not the counter's verdict.
5. Seat probe of the frozen counter: `python3 .ufo/evidence/round-47/coverage/measure.py --selftest` → `C3_R47_SELFTEST: cases=24 failed=0`, `VERDICT: PASS`, exit 0. Probe only; the deciding run belongs to the L1.
6. Negative-claim sweeps on the folded snapshots (case-insensitive counts): `mutation` 0/0, `bash` 0/0, `Node` 0/0, `shell` 0/0, `Java` 0 (arXiv) / 16 (Lam), `Maven` 0/17, `JUnit` 0/8, `JavaScript` 0/2, `cost` 0/3, `$` 0/0. These counts are what the entry's absence claims rest on.

Not run: any `--rev`/`--lane` invocation of the C1, C2 or C3 counter, any live URL fetch, any git/jj command in the lane, any mutation of a counter or snapshot.

## Grounding decisions

- **S261**: the abstract page is one folded paragraph, so its quotations carry no line numbers; provenance is `§Abstract` plus the page's metadata cells (`arXiv:2302.09330v2 [cs.SE]`, `Submitted on 18 Feb 2023 (v1), last revised 18 Mar 2023 (this version, v2)`, the ICST-2023 comments cell, DOI `10.48550/arXiv.2302.09330`).
- **S262**: the committed text is pdftotext 26.08.0 `-layout` and every page is two columns, so a sentence crossing the gutter is interleaved in the folded text. I verified that the package's own Lam quotations — including the short forms `one can use ≤ 5 reruns (50% less than Google's default ten reruns [6])` and `run tests in a test suite instead of in isolation` — return **0** hits against the committed `lam-2020-reruns.txt` fold (they hit only in the package copy). The entry therefore quotes single-column fragments only and says so in Gate-relevant limits; adjacent fragment quotations sometimes complete one sentence.
- Section label corrected: the guideline block is in **§I Introduction** (`lam-2020-reruns.txt:112-119`), not a named `§Guidelines` section. The page is p. 2, matching the package.
- The venue of the Lam paper is **not** claimed: the text carries `©2020 IEEE` (`:63`) and no proceedings string, and `pdfinfo` metadata names only TeX/pdfTeX 1.40.20.

## Package claims dropped or softened (and why)

Package input: `.ufo/evidence/round-47/assimilation/package/flaky-aware-verdict-evidence.md`.

| Package claim | Disposition | Reason |
|---|---|---|
| `S160` (pitest.org/faq) paragraph and its quotation (`Both these measurements can be affected by external factors …`) | **dropped** | S160 is not one of my snapshots; the item forbids keeping it unless I re-open pitest.org/faq myself, and lane row S156 already holds the document. Nothing from the FAQ appears in the draft. |
| "the lane's own convention scores a timeout as a kill (per its held S001) … a live inconsistency in the lane's own conventions" | **dropped** | Contradicted by the frozen contract: C2's kill rule says a crash or a timeout is not a kill (`.ufo/evidence/round-47/contract.json` C2 `statement`). There is no timeout-as-kill convention to repair. The clock-dependent point is carried instead by S262's 1500 ms example. |
| "S155's flip-rate feature is computable from the lane's retained per-case outcome tuples (the lane's own ledger keeps outcomes and exit codes per case)" | **dropped** | Not supported: a search of `tools/`, `corpus/knowledge/` and `.ufo/evidence/` for `exit_code|outcome|per-case` finds no per-case outcome series over time; this round's evidence is per statement-profile `(line, exit)` and one selftest invocation per mutant. Replaced by the conditional inference that a verdict needs either reruns or an existing history. |
| "five reruns classify ≥ 82% of failures correctly" | **softened** | The source says one can "check correctly ≥ 82% of the time" whether failures are due to flaky tests (`lam-2020-reruns.txt:113-115`), on 26 modules from 23 projects, with flaky defined as both outcomes across reruns (`:29`). The draft keeps the sentence's referent and refuses to extend it to verdict correctness. |
| "§Guidelines, RQ1 & RQ3 / RQ2 & RQ3" | **corrected** | The block is §I Introduction `:112-119`; no section literally named "Guidelines" exists in the text. |
| "A small N is defensible *if* the control is byte-identical rather than merely green … S158 also says the cheaper axis is order diversity" | **kept as inference, re-scoped** | The sources state order diversity helps detection; they say nothing about byte-identical controls. The draft states the 82% must not be transferred to the F3 control count. |
| "S158 … the ACM version was access-controlled" | **dropped** | Not in any snapshot and not fetched; only the author-hosted URL is recorded. |
| `recheck: curl … then grep -c '5 reruns'` | **replaced** | Grepping the live PDF binary for `5 reruns` is a weak, encoding-dependent check; replaced by the PDF sha256 plus a phrase count on the arXiv page. |
| `verified-at: 2026-10-23`; sources labelled `S155`/`S158` | **replaced** | Re-verified 2026-10-25 against the round-47 committed snapshots; adopted ids by document are S261 (arXiv 2302.09330) and S262 (Lam camera-ready). |
| "the lane's six fleet gates are bash/JS CLI suites with case counts in the tens" | **dropped** | A lane characterisation I did not ground; the draft states only what the snapshots contain (their populations) and marks the transfer question as inference. |
| QUALITY criterion 11 anchor (`corpus/QUALITY.md:34-37`) | **kept** | Verified: criterion 11 begins at `corpus/QUALITY.md:34`. |

## Integration requirements (for the L1, not done by this seat)

1. Rows S261 and S262 must list `corpus/knowledge/flaky-aware-verdict-evidence.md` in their **used-by** cell, or the counter's `entry_ok` refuses the entry (`not in used-by`).
2. S261 row: source URL must normalise to `arxiv.org/abs/2302.09330`; snapshot cell must name `.ufo/evidence/round-47/coverage/sources/arxiv-2302.09330-abs.html` together with an 8+-hex prefix of its bytes (`2965343c`).
3. S262 row (uncounted by the counter, still must be self-consistent): the counter's row reader takes the **first** snapshot path in the anchor cell and compares its bytes' digest against hexes in the same cell. Naming the `.txt` while listing only the PDF digest would fail that check. Safest anchor lists both pairs — `lam-2020-reruns.txt` with `bf52c908`, `lam-2020-reruns.pdf` with `0b880458`.
4. `corpus/README.md` must carry the backticked path in either form the counter accepts: `corpus/knowledge/flaky-aware-verdict-evidence.md` or `knowledge/flaky-aware-verdict-evidence.md`, and the F3 coverage-map row should be updated in the same round (QUALITY criterion 7).
5. Keep the first four lines byte-exact when copying; the header carries the provenance trio the counter parses.

## Findings

- **The package's Lam quotations are not locatable in the committed snapshot.** Because `-layout` interleaves the two columns, both package sentences and their short forms return 0 hits after fold. Any entry that copies them would carry unlocatable quotations even though the sentences exist in the PDF; the draft's fragment quoting is the fix, and this is the main correction this seat contributes.
- **The package mixed a vendor FAQ into a paper-based entry and drew a false lane claim from it** (timeout scored as a kill), contradicted by the frozen C2 kill rule.
- **The package's "ledger keeps outcomes and exit codes per case" is unsupported** in this lane at this revision.
- **S261's abstract does not name a language.** It says one large-scale industrial software system; the "Java systems" framing in the package belongs to S262 only.
- **Counted-row dependency**: the counter admits entries through S261's snapshot only for the located/fresh rule, because S262's URL is not in `DOCS`; the draft still keeps S262 quotations locatable by the same fold so the uncounted row is not decorative.

## Out of scope / not done

- Did not copy the draft into `corpus/knowledge/`, did not edit `corpus/SOURCES.md` or `corpus/README.md`, did not touch any counter, snapshot, contract, statement list, pool or control.
- Did not fetch the live URLs; the `recheck:` commands are for a future run and were only executed against the committed snapshots.
- No tool installs or upgrades (none needed), so no tool/version/channel records.
- No subagents spawned (leaf).

## Artifacts

- Deliverable: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-47/w1/T47ScribeEntryPredict.entry.md` (16,464 B).
- Report: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-47/w1/T47ScribeEntryPredict.md`.
- Scratch (not committed): `/tmp/tameshi-r47-T47ScribeEntryPredict/{abstract.txt,abstract_wrapped.txt,check.py,validate.py,q1.json,q2.json,q3.json}`.
- Inputs read: `.ufo/evidence/round-47/contract.json`; `.ufo/evidence/round-47/coverage/{measure.py,sources/*}`; `.ufo/evidence/round-47/assimilation/package/flaky-aware-verdict-evidence.md`; `corpus/README.md` (F3 rows), `corpus/QUALITY.md:34-37`, `corpus/knowledge/r6-flaky-failures-cluster.md`, `corpus/knowledge/r8-gtest-order-and-seed.md`, `corpus/SOURCES.md` (tail, S152–S160, round notes).
