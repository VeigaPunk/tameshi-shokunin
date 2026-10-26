# T49ScribePkgQuickCheckCorr — F10 assimilation triage: `r4-quickcheck-primary-correction.md`

Seat: leaf scribe (assimilation triage, read-only package). Round 49, wave 1, base
`8ca67421111fa354b47b803358391d0b07fc6db9`. Package under triage:
`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r4-quickcheck-primary-correction.md`
(69 lines; cited below as `PKG:<line>`). No counter was invoked, no claim decided, no lane file
edited, no mutant panel or `~/.local/state/` entry read.

## Verdict — REFUSE as written

**Decisive reason.** The entry's identifying claim — that "the lane's leads list has carried
`doi:10.1145/1660572.1660575` as 'the QuickCheck paper' since before round 1, and rounds 1–3 of this
lane each recorded a failed attempt to open it" (`PKG:12-14`, restated `PKG:27-29`) — is false for
the lane it is proposed to, and its replacement identification of that DOI as "a *different* ICFP
2009 item" (`PKG:21-22`) is disproved by DOI resolution. Both failures are mechanical:

```
$ git -C LANE grep -n 1660572 8ca67421111fa354b47b803358391d0b07fc6db9          -> no output (0 matches)
$ git -C LANE rev-list --all | while read c; do git grep -q 1660572 $c -- corpus/SOURCES.md && echo HIT $c; done
   -> no HIT over every ref (1342 commits at capture); #0 of the lane's 16 base lead bullets carries it
$ curl -s -o /dev/null -w '%{http_code}' https://api.crossref.org/works/10.1145/1660572.1660575   -> 404
$ curl -s -o /dev/null -w '%{http_code}' https://doi.org/10.1145/1660572.1660575                  -> 404
```
(`.ufo/waves/round-49/w1/T49ScribePkgQuickCheckCorr.lane-grep.txt`,
`…doi-probe.txt`.) The DOI is not registered with any registration agency — not merely "another
ICFP 2009 item": four neighbouring suffixes of the same container (`.1660570`, `.1660571`,
`.1660576`, `.1660579`) also answer `404`, while the three DOIs the entry does name answer
`crossref=200 / doi.org=302`.

**What the entry gets right, and is therefore not refused for.** The QuickCheck paper is Claessen &
Hughes, ICFP 2000, pp. 268-279, DOI `10.1145/351240.351266` (`PKG:17-20`); the ICFP 2009 QuickCheck
paper is PULSE, DOI `10.1145/1596550.1596574`, with the seven authors as listed (`PKG:22-25`); and
the S183 sentences quoted at `PKG:39-44` are verbatim in the fetched bytes. I re-opened all three
myself (§1). The refusal is against the entry's *lane-history premise and its locator metadata*, not
against its sources.

**Flip condition (conjunction; each item is one command away from checkable).**

1. Carry the claim at campaign scope: cite
   `shokuknow/lanes/tameshi/CANNOT-ANSWER.md:33`, `REJECTIONS.md:50`, `round2/REJECTIONS.md:28`,
   `round3/REJECTIONS.md:28`, `round4/REJECTIONS.md:19` (these *do* carry the DOI) and drop "the
   lane's leads list" / the `corpus/SOURCES.md:233-253` anchor (F7) — or exhibit one tameshi-shokunin
   `file:line` in which the DOI appears.
2. Replace `PKG:21-22` with the measured result: the identifier resolves to no registered work
   (Crossref 404 + doi.org 404 on the retrieval date). The campaign's own round-4 record already
   says this — "belongs to neither QuickCheck paper" (`lanes/tameshi/round4/REJECTIONS.md:19`).
3. Correct the locators: S183 is §2.10 "Generating Test Data", printed p. 34 (PDF p. 39 of 116), not
   "§4.1 … p. 44" (`PKG:3`; F3); S182's `recheck:` (`PKG:5`) must normalize spaces on both sides and
   be measured to return 1 (today it returns 0; F4); the S182 carrier must be named (aaron's
   `scihub` tier / Tufts mirror `sha256 bfddcaa6…`; F5).
4. Re-open both sources on the round day: C2's sourced predicate requires a row **opened
   2026-10-26** (`contract.json` `claims.C2.sourced`: "cites at least one SOURCES row opened 2026-10-26"); the staged rows and this entry both carry `2026-10-23` (`PKG:4`,
   `merge/tameshi/SOURCES.append.md:36-37`).

Even with 1–4 satisfied, the economical landing is the two rows with corrected locators plus one
sentence of the F10 inference (`PKG:48-53`); the correction narrative then carries no F10 content
(F6). F10 stays `open` until C2's pilot measures it — this entry measures nothing
(`PKG:58-60`, its own words).

## 1. CORPUS rule 1 — I re-opened both sources

| source | command | observed |
|---|---|---|
| S182 metadata | `curl -sS https://api.crossref.org/works/10.1145/351240.351266` | title `['QuickCheck']`; container `Proceedings of the fifth ACM SIGPLAN international conference on Functional programming`; authors Koen Claessen, John Hughes; issued 2000-09; page `268-279`; type `proceedings-article` |
| S182 text | `aaron papers fetch 10.1145/351240.351266` | exit 0; JSON `tier=scihub`, `format=markdown`, `meta={mirror: https://sci-hub.ee, pdfUrl: https://sci.bban.top/pdf/10.1145/351240.351266.pdf, pdfBytes: 313371}`; abstract present as `QuickCheck is a to ol which aids the Haskell programmer in form ulating and testing prop erties of programs` (OCR intra-word spacing) |
| S182 publisher route | `curl -sS -L https://doi.org/10.1145/351240.351266` | `http=403` final `https://dl.acm.org/doi/10.1145/351240.351266` (reproduces round-40 and round-49 sibling findings) |
| S183 bytes | `curl -fsSL -o lic.pdf https://smallbone.se/papers/lic.pdf` | `http=200`, 1 269 821 B, `sha256 eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08`, 116 pages; identical sha256 to the independent fetch by seat `T49ExecSrcSmallbone` (`.ufo/waves/round-49/w1/T49ExecSrcSmallbone.json`) |
| S183 quotes | `pdftotext -layout lic.pdf` then count on the flattened text | "the quality of the test data determines the quality of the generated equations" → 1; "it is important to provide good test data generators, that fit the program at hand" → 1; the `property-based … building custom generators` sentence → 1 after de-hyphenating `property- based` |
| S183 locator | `pdftotext -f 39 -l 39 -layout lic.pdf` | the statement sits on PDF p. 39, printed folio `34`, under §2.10 "Generating Test Data" (`T49ScribePkgQuickCheckCorr.s183-p39.txt:18,21`) |
| S183 claimed locator | `pdftotext -f 49 -l 49 -layout lic.pdf` | printed folio `44` begins `3.4 shr: Problems with Partiality`; the document's `§4.1` is "A Parallel Correctness Criterion" (`T49ScribePkgQuickCheckCorr.s183-pin.txt`) — neither is about generators |
| PULSE | `curl -sS https://api.crossref.org/works/10.1145/1596550.1596574` | `Finding race conditions in Erlang with QuickCheck and PULSE`, ICFP 2009 (issued 2009-08-31), pp. `149-160`, authors Claessen, Palka, Smallbone, Hughes, Svensson, Arts, Wiger |

The round's sibling seats reached the same two facts independently: `T49ExecSrcQuickCheck.md`
(§"Row-level observation for S182": bare DOI resolution is 403, and the row's "§Abstract and §1"
location understates where the F10 material sits) and `T49ExecSrcSmallbone.json`
(`staged_location_verdict: … §2.10 "Generating Test Data", printed p. 34 (PDF p. 39) … printed p. 44
is §3.4`). My measurements agree with both; the locator error is not a reading artifact.

## 2. Gates

**PROVINCE — pass.** F10 is the lane's own frontier ground (`PROVINCE.md:40` → `corpus/README.md:87`,
`F10 | PBT generators for gate fixtures | … | open`); nothing here touches a sibling lane's gate or
code, and the package is a read-only input. The subject matter (source identification for a frontier
ground) is in province.

**QUALITY — fail on four criteria.**
- **criterion 2** (`corpus/QUALITY.md:4`, every claim carries a measured anchor): the headline claim
  `PKG:12-14` names no `file:line`. The only anchor anyone supplies is
  `lanes/tameshi/round4/CANNOT-ANSWER.md:16` → `corpus/SOURCES.md:233-253`, which at base is round-20/21
  search-log prose with no DOI (`T49ScribePkgQuickCheckCorr.lane-grep.txt` §4). Unanchored.
- **criterion 14** (`corpus/QUALITY.md:50`, normalized provenance must agree with its declaration
  source): the S183 locator (`PKG:3`) and the S182 channel statement (`PKG:64-65`) both disagree with
  what the bytes show (F3, F5).
- **criterion 10** (`corpus/QUALITY.md:27`, an external source enters through a row opened in the
  round that writes it): `PKG:4` `verified-at: 2026-10-23`; the lane writes on 2026-10-26.
- **criterion 97** (`corpus/QUALITY.md:1428`, evidence pointers resolve at the landing revision): the
  pointer `PKG:12-14` implies (`corpus/SOURCES.md:233-253`) resolves to unrelated text, and the row
  locator `PKG:3` misses by one section and ten printed pages.
Criteria 1/3/4/5 hold in the body (inference is labelled at `PKG:50` and `PKG:58`; the boundary
section `PKG:62-67` is honest about tier and retrieval route).

**Ground not already held — duplicate, not new.** F10 is open, but the entry's one true novel
statement (the QuickCheck identification) is already recorded in-lane at
`.ufo/waves/round-40/w1/ReviewQ134.md:20-41` — same DOI, same aaron `scihub` channel, same abstract
string — and the two rows are already staged and cross-listed
(`merge/tameshi/SOURCES.append.md:36-37`, `.ufo/waves/round-46/w1/ConnPackageCross.md:34`). Admitting
the entry would add a false lane history, not ground.

**CORPUS rule 1 — discharged by this seat, not by the package.** My re-open above is the round's
evidence; the package's own `verified-at:` cannot serve it (criterion 10) and cannot satisfy C2's
"row opened 2026-10-26".

## 3. Findings

- **F1 (decisive).** `PKG:12-14` and `PKG:27-29` assert a lane lead record that does not exist in the
  receiving lane. Command: `git grep 1660572 8ca67421` → 0; all-refs loop over `corpus/SOURCES.md` → 0
  HIT; base `## Leads (unopened)` block = 16 bullets, `grep -c '1660572\|1660575'` → 0
  (`corpus/SOURCES.md:271-292` at base).
- **F2.** `PKG:21-22` ("is a *different* ICFP 2009 item") is false: `10.1145/1660572.1660575` is
  unregistered at Crossref and at doi.org (404/404), as are four neighbouring suffixes; the campaign's
  own round-4 record contradicts the entry here (`lanes/tameshi/round4/REJECTIONS.md:19`: "belongs to
  neither"; `round4/SEARCH-LOG.md:86-94`; `.ufo/scopes/corpus-expansion-4/ScoutTameshi.md:33`).
- **F3.** `PKG:3` locates the S183 statement at "§4.1 … p. 44". Measured: §2.10, printed p. 34 (PDF 39
  of 116). Printed p. 44 is §3.4 "shr: Problems with Partiality"; the document's §4.1 is "A Parallel
  Correctness Criterion". The same wrong locator is staged at
  `merge/tameshi/SOURCES.append.md:37` — the error originates in the staging row, and the entry copies
  it.
- **F4.** `PKG:5` `recheck:` is vacuous-false as written — `tr -d ' \n'` strips the haystack's spaces
  but the needle keeps them: measured **0** (expect 1), space-normalized needle measured **1**
  (`T49ScribePkgQuickCheckCorr.rechecks.txt`). This is the identical defect the lane already recorded
  against this DOI at `.ufo/waves/round-40/w1/ReviewQ134.md:52-60`.
- **F5.** `PKG:64-65` says the text "was retrieved through a DOI resolver, not from a publisher page".
  True but understated — the resolver path aaron offers is the `scihub` tier via
  `https://sci-hub.ee` (`meta.mirror`), while `dl.acm.org` answers 403. The lane now has a lawful,
  pinned alternative carrier: the Tufts CS257 copy, 194 315 B,
  `sha256 bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172`
  (`.ufo/waves/round-49/w1/T49ExecSrcQuickCheck.md` §1). The row's channel should name which was used.
- **F6.** `PKG:33-38` renders the abstract as normalized prose; the fetched bytes read
  `a to ol which aids … form ulating … prop erties`. Quote-fidelity note only — the substance is
  present, and the sibling seat's excerpt check locates it in the pinned carrier (11/11).
- **F7.** The provenance conflation is mechanical: the "lane's leads list" carrying the DOI is the
  **shokuknow campaign's** prose (`lanes/tameshi/CANNOT-ANSWER.md:33`, `REJECTIONS.md:50`,
  `round2/REJECTIONS.md:28`, `round2/CANNOT-ANSWER.md:32`, `round3/REJECTIONS.md:28`), not the
  receiving lane's corpus; its cited anchor `corpus/SOURCES.md:233-253` is unresolvable in that corpus
  (F1). Campaign history is not receiving-lane history.
- **F8.** `PKG:64-65` calls `10.1145/351240.351266` "the canonical DOI", but Crossref carries the same
  paper twice: `10.1145/351240.351266` (ICFP proceedings) and `10.1145/357766.351266` (ACM SIGPLAN
  Notices, pp. 268-279, 2000-09). A canonical-DOI claim must name which record it pins.
- **F9 (adjacency, cross-entry).** The merge package's row ids collide with the lane's: merge `S157` is
  the Hypothesis JOSS paper (`merge/tameshi/SOURCES.append.md:11`) while lane `S157` is Python
  `argparse` (`corpus/SOURCES.md:127`). For *this* entry's ids there is no collision — the lane has no
  `S182`/`S183` row (max id `S268`, 128 rows) — so the contract's re-numbering check passes for
  S182/S183 and fails for the sibling entry's S157.

## 4. What is worth keeping (adjacency)

- **The two rows, corrected.** S182 (tier A, ICFP 2000) + S183 (tier B, Chalmers TR 76L) are the right
  F10 sources and are now twice independently verified; they can be opened 2026-10-26 with the F3
  locator fix and the F5 carrier named. S183's §2.10 material is the sharper of the two for C2: the
  generator is per-program, distribution must be observed (`classify`/`collect`), and an inappropriate
  generator yields a *wrong law* — the same discipline C2's predicate encodes by freezing 12 input
  classes before the panel is revealed.
- **The F10 refinement at `PKG:48-53`** ("not a sampling exercise; a choice of generator whose laws
  mean something for that gate's domain") is a usable sentence for the pilot entry — as the inference
  it is labelled as.
- **F7 as a lesson candidate**: a merged package's own campaign history must be re-anchored in the
  receiving lane before it is cited as that lane's history. This is the same class as the lane's
  criterion 14 (provenance field vs declaration source), one level up: whole-document provenance.

## 5. Out of scope / non-actions

No counter was run (`--selftest`, `--list`, or otherwise) — no counter is in this item's scope. No
lane file, contract, control receipt, `.ufo/evidence/` path, jj state or Git index was touched; no git
mutation; `git` was used read-only (`grep`, `show`, `rev-list`). Nothing under
`~/.local/state/` and no `c2-*.stdout` panel file was opened. No model was invoked. No tool was
installed (`aaron` was already at `/home/vgpnk/.local/bin/aaron`; it wrote nothing — `~/aaron-library`
does not exist after the run).

Touched surfaces (all inside `.ufo/waves/round-49/w1/`): this report plus six receipts —
`T49ScribePkgQuickCheckCorr.doi-probe.txt`, `…lane-grep.txt`, `…carrier.txt`, `…rechecks.txt`,
`…s183-pin.txt`, `…s183-p39.txt`. Scratch `/fast/scratch/hyaku/tameshi-r49/T49ScribePkgQuickCheckCorr`
deleted before yielding; no `/tmp` path is cited as evidence.

## Summary

1. Verdict: **REFUSE as written** — the entry's identifying claim (a lane lead list that carried the
   DOI) is false: 0 occurrences at base, in all 1342 commits, and in the 16-bullet lead list.
2. The chased DOI `10.1145/1660572.1660575` is unregistered (Crossref 404, doi.org 404; four
   neighbouring suffixes also 404), so `PKG:21-22`'s "different ICFP 2009 item" is false too.
3. S182 is verified correct (Crossref + aaron + 403 ACM); S183's quotes are verbatim but the locator is
   wrong: §2.10, printed p. 34 (PDF 39/116), not §4.1 p. 44.
4. S182's `recheck:` measures 0 (vacuous), repeating the defect the lane already recorded at round 40;
   the space-normalized form measures 1.
5. PROVINCE passes; QUALITY fails criteria 2, 14, 10 and 97; F10 is still open and the entry adds no
   ground beyond what round-40 already holds.
6. Flip: campaign-scoped anchoring + resolution-based DOI statement + corrected locators/recheck +
   rows re-opened 2026-10-26; after that, land the two rows and one inference sentence, not the
   correction narrative.
7. Receipts: six files beside this report; measurements agree independently with seats
   `T49ExecSrcQuickCheck` and `T49ExecSrcSmallbone` (identical S183 sha256 `eaee48f9…`).
8. No counter, no claim decided, no lane edit, no panel read.
