# T50W2ScoutS271 — S271 / S022 re-open (round 50, wave 2)

Revision read: `80ea77e99e239982ab0b93e416645ef2359725d3` (`git -C <lane> show 80ea77e9:<path>`). Read-only; scratch deleted.

## Fetches (mine, independent)

| source | HTTP | bytes | sha256 | UTC |
|---|---|---|---|---|
| S271 `https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf` | 200 | 247738 | `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa` | 2026-10-26T22:50:03Z |
| S022 `https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13` (1st) | 200 | 115315 | `ecf65b77…a0` | 2026-10-26T22:51:04Z |
| S022 (2nd, seconds later) | 200 | 115315 | `1a8dc0ad…fac` | same minute |

S271 matches the row, the lane snapshot (`.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf`, sha identical, committed as a blob at 80ea77e9) and `fetch-receipt.json`. `pdfinfo`: 17 pages, Ghostscript 5.50, created 2001-12-20.
Extraction: `pdftotext d.pdf` (default reading order), per page `pdftotext -f N -l N`; whitespace-collapsed substring search. Tool: poppler `pdftotext` already installed; nothing installed.

## S022 sha does not reproduce (finding)

The lane records S022 sha256 `fa3036a3…` (`T50ScribeSrcHeld.md:26,236,256`; lesson Gate). My two fetches differ from it and from each other. `diff` of the two HTML bodies (`tr '>' '>\n'`) shows the only difference is the per-request `csrf-token` meta (line 12) and hidden `_token` input (line 803). The byte count 115315 is stable and equals the lane's. So the byte count is a usable recheck handle; the sha is not. Anything that re-verifies S022 by sha will always "fail".

## Per quote (page = mirror PDF page; section from the extracted headings)

### S271 row (`corpus/SOURCES.md`, `| S271 |`) and lesson Gate block (`corpus/lessons/round-50.md` "## Gate")

| claim | verdict | location |
|---|---|---|
| Quote 1, 21 words: "It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear." | present (1 hit, default order; word count 21) | p.1, §I Introduction, paragraph "Simplification of test cases." |
| Quote 2, 16 words: "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case" | present (1 hit; 16 words) | p.1, §I, right after the Figure 2 sketch sentence |
| Re-verify hits each 1 in default order: `removing any single input entity`, `After 57 tests`, `139 automated test runs` | present (1/1/1) | p.1 (the 139 is in the Abstract) |
| "-layout hyphen-folds 'simplifies'" | present | `pdftotext -layout`: "sim- plifies" (`which it sim- plifies by successive testing`); under -layout `139 automated test runs`, `It stops when a minimal test case is reached`, `After 82 test runs` return 0 hits, `removing any single input entity` and `After 57 tests` still 1 |
| Running head "IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002" | present | on pp. 1,2,4,6,8,10,12,14,16 (9 hits); a small mirror page number (1, 2 …) sits beside it; no journal folios 183-200 anywhere (`grep -nE '18[3-9]\|19[0-9]'` on the extract finds none as folios) |
| "DOI 10.1109/32.988498" | absent from the PDF | `grep 10.1109 d.txt` finds nothing; the DOI and "183-200" come from the Crossref line of `fetch-receipt.json`, not from the carrier. The row cites them as bibliographic metadata, which is fine; they are not "located in the PDF". |
| Title block "Simplifying and Isolating Failure-Inducing Input" | present | p.1 lines 1-6 of the extract |
| Row anchor §I "Simplification of test cases" paragraph, mirror p.1 | present | p.1 |
| Row anchor §III-A Minimal Test Cases, Definition 10, mirror p.4 | present | heading "A. Minimal Test Cases" and "Definition 10 (n-minimal test case)", p.4 (formula text garbled by the extractor; the definition is there) |
| Row anchor §III-C Properties of ddmin, Propositions 11 and 12, mirror p.6 | present | "C. Properties of ddmin" then "Proposition 11 (ddmin minimizes)" and "Proposition 12 (ddmin complexity, worst case)" all on p.6 (Proposition 13 best case also p.6; Definition 10 and Proposition 12 text also recur on p.12-13 as isolation analogues). In `-layout` p.6 the "IV. CASE STUDIES" heading sits in the other column, so in default order it interrupts III-C; Props 11-12 stay under III-C. |
| Row anchor §IV-B Figs. 11-12 | present | §IV-B "B. Mozilla Cannot Print" starts p.8; Fig. 11 and Fig. 12 captions and the run counts are on p.9; §IV-C starts p.9 after them |

### corpus/knowledge/delta-debugging-minimization-contract.md

| claim | verdict | location |
|---|---|---|
| "is fed with a failing test case, which it simplifies by successive testing. It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear." | present | p.1 §I (default order; two-sentence run is contiguous) |
| Definition 10 (§III-A) states n-minimality formally | present | p.4 §III-A |
| Proposition 11 (§III-C): ddmin's result "is 1-minimal in the sense of definition 10" | present, verbatim in the source: "ddmin(c✘) is 1-minimal in the sense of definition 10" | p.6 §III-C |
| "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case" (§I) | present | p.1 §I |
| §IV-B (Fig. 11): "After 82 test runs (or 21 minutes), only 3 out of 95 user actions are left" | present (body text beside Fig. 11, not the caption; 16 words) | p.9 §IV-B |
| Abstract: "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC" | present | p.1 Abstract |
| "82 + 57 = 139" | arithmetic correct; **not stated in the source** (the source gives 139 once, in the Abstract, with no breakdown) — lane inference, correctly unmarked only in the pilot ("see") but not tagged `[INFERENCE]` in either entry | — |
| Line-to-tag stage "took '26 steps' (§V-A)" | present, but **misplaced against §I**: "After 26 steps, the line is reduced to the single <SELECT> tag." and "minimizing (Figure 2) required 26 tests" | p.12, §V-A "Isolation Illustrated" (default order); the entry's section is right |
| "57 is one reduction (896 lines to 1)", "26 steps is a second reduction of an already one-line input, not a competing count for the first" | present as an **inference that the paper contradicts in §I** | §IV-B p.9 says 57 runs take 896 lines to a 1-line input (so 57 ≠ <SELECT>); §I p.1 says the same 57 tests take the 896-line input to the minimal case `<SELECT>` and ties it to Figure 2; §V-A p.12 says Figure 2 (the same ddmin figure) took 26 tests. The paper is internally inconsistent (57 vs 26 for Figure 2; 57 reaches a 1 line in §IV-B, `<SELECT>` in §I). The entry picks the §IV-B reading and presents the 26 as a following stage; if 26 were an extra stage the case-study total would be 82+57+26 = 165, not 139. The entry's statement is defensible but is stated as fact, not flagged as a reconciliation. Nothing quoted is wrong; the framing "not a competing count" is the lane's resolution. |
| Running head "IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002" and the title block (Boundary section) | present | pp. 1,2,4,… (see above) |
| Mirror "17 pages paginated 1-17 with no journal folios" | present | `pdfinfo` Pages: 17 |
| recheck `curl … \| pdftotext - - \| tr -s ' \n' ' ' \| grep -c 'removing any single input entity'` expects 1 | present: I ran it with the full phrase `…would cause the failure to disappear`: 1 | — |
| Boundary: inputs are HTML, recorded user actions, GCC and fuzz inputs | present | Mozilla (§IV-B), GCC (§IV-A), FLEX fuzz (§IV-C, Fig. 13) |

### corpus/knowledge/fixture-shrinking-pilot.md

| claim | verdict | location |
|---|---|---|
| S271 §I quote "It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear." | present | p.1 §I |
| S271 §I "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case" | present | p.1 §I |
| "(the Abstract's 139 runs is the case study's two reductions summed, 82 + 57 …)" | the 139 is present in the Abstract; the "two reductions summed" breakdown is the lane's inference (the source never splits it); see the 26-step note above | p.1 Abstract |
| "the source gives 57 for that reduction (§I; §IV-B Fig. 12)" (also in lesson Gate) | present for the count; the end state differs between the two sections (§I: `<SELECT>`, §IV-B: 1-line input) | p.1, p.9 |
| S271 anchors in the `source:` line: §I "Simplification of test cases", §III-A Definition 10, §IV-B Fig. 12 | present | pp. 1, 4, 9 |
| recheck 365d, `grep -c 'removing any single input entity would cause the failure to disappear'` expect 1 | present (1, run against a fresh curl) | — |
| S024 quote "every character contained is required to produce the error" | not in scope; not checked | — |

### S022 (the pilot's quote; lesson Gate, SOURCES row `| S022 |`)

| claim | verdict | location |
|---|---|---|
| "internally, to the sequence of random choices made during generation" | present (1 hit) | Abstract (HTML page text), sentence "…we apply it internally, to the sequence of random choices made during generation, so that a test case is reduced by…" |
| "significantly mitigates the impact of the test-case validity problem, by ensuring that any reduced test case is one that could in principle have been generated" (lesson Gate: 25 words) | present (1 hit; I count 25 words) | Abstract, closing sentence "It also significantly mitigates…" |
| Row teaches cell "compared with C-Reduce and delta debugging" | present: "C-Reduce" once, "delta debugging" 3 times in the page | abstract tail and later page text |
| Title "Test-Case Reduction via Test-Case Generation: Insights from the Hypothesis Reducer"; DOI `10.4230/LIPIcs.ECOOP.2020.13`; MacIver, Donaldson | present | page header and citation block |
| lesson Gate: "HTTP 200, 115,315 B, sha256 `fa3036a3…`" | status and bytes present; **sha not reproducible** (see above) | — |
| the pilot calls it "internal reduction" | the string `internal reduction` is not on the page; the page says `internal test-case reduction` — the pilot's phrase is the lane's shorthand, not a quote | — |

## Summary
- Every quoted string (21-word and 16-word §I quotes, 82/3-of-95 sentence, Abstract's 139, Prop. 11 phrase, running head) is present verbatim at the stated section/page of the S271 mirror; sha256 7ed0c812…, 247738 B, HTTP 200 reproduce (2026-10-26T22:50:03Z).
- Anchors (§I p.1, Def. 10 §III-A p.4, Props 11-12 §III-C p.6, Figs. 11-12 §IV-B p.9, 26 steps §V-A p.12) all resolve; DOI and 183-200 are Crossref metadata and absent from the PDF.
- The "-layout hyphen-folds" claim holds ("sim- plifies"); default-order re-verify greps return 1 each.
- Finding 1: the lane's 82 + 57 = 139 decomposition and "26 steps is a second, following reduction" are lane inference; §I ties 57 to the `<SELECT>` end state and §V-A gives 26 for the same Figure 2, so the paper contradicts itself and the entries state one reading as fact (no wrong quote).
- Finding 2: S022 recorded sha `fa3036a3…` does not reproduce (the page embeds a per-request csrf token; bytes 115315 stable); both S022 quotes are present in the Abstract. "internal reduction" in the pilot is shorthand, not a quote.
