# T50ScribePkgDD — assimilation triage: `delta-debugging-minimization-contract.md` (theme F6)

seat: T50ScribePkgDD · round 50 wave 1 · read-only triage, no lane edit outside this wave directory
lane base: `e3729de862f73ae080d98fcf522a7081ce16e40a` · contract: `.ufo/evidence/round-50/contract.json`

package document triaged:
`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/delta-debugging-minimization-contract.md`
(47 lines, read in full; package row `SOURCES.append.md` `| S167 |`, package merge entry
`MERGE-REPORT.json` target `corpus/knowledge/delta-debugging-minimization-contract.md`)

## Verdict

**ADMIT the document and its headline claim; refuse one of its two claims; 14 mandatory edits before landing.**

The headline claim — "A reduced fixture has a stated minimality witness and a stated cost in test runs" —
is true, and I verified both halves against the document's own bytes this round (quotes in §Re-open record).
The second claim, that the 896-line reduction cost **139 automated test runs**, is not supported: the source
gives **57** for that reduction (§I, §IV-B) and its own two run counts decompose the Abstract's 139 exactly —
**82** runs (21 minutes) for the 95-user-action run + **57** for the HTML line run = 139 (receipts R7).
Landing it as written would put the lane's shrinker cost accounting (`runs`) on the wrong denominator.

**Decisive reason for the edits, not for refusal:** the entry's `source:` id `S167` names no lane
`SOURCES.md` row — QUALITY 10 clause 2 (`corpus/QUALITY.md:27`), the clause the round-48 closure used to
refuse `r8-predictive-test-selection-cost.md` (`corpus/QUALITY.md:1382-1396`). `S167` is a staged id inside
the lane's reserved range `S161–S255` (`corpus/SOURCES.md:495`); `reg-ids 130 · staged-ids 111 ·
collisions 9 (S026,S153–S160) · S167 ∉ reg-ids · next unused S271` (receipt R4). The document *can* be
re-grounded this round because I re-opened it myself (CORPUS rule 1; `corpus/lessons/round-46.md:15-17`),
so the row can be opened as **S271**, which `corpus/SOURCES.md:495` still names as next unused and which
C2's counter accepts (`cells[7]=='mined' and cells[8]=='2026-10-26'`,
`.ufo/evidence/round-50/c2/measure.py:349-353,61`).

**Flip conditions.**
- Flip to **REFUSE** if the landing keeps "139 runs" as the cost of the 896→1 reduction (no sentence in the
  source supports it; §IV-B's own figure is 57) — that fails QUALITY 2 (`corpus/QUALITY.md:4`) and imports a
  wrong cost unit into F6.
- Flip to **REFUSE** if no snapshot of the fetched bytes is committed with the entry (QUALITY 79,
  `corpus/QUALITY.md:944`) — the package cites a live URL only.
- Flip to **REFUSE** if S271 is taken by another seat's row for the same document this round (deduplication
  by document, the rule round 48 applied at `corpus/lessons/round-48.md:93`); check the registry before
  appending.
- Flip to **REFUSE** if a held row is discovered to state the same per-reduction cost datum (none does at
  base; see §Coverage).

## Gates

| gate | decisive anchor | result |
|---|---|---|
| PROVINCE scope | `PROVINCE.md:3-10` (verification-fixture craft, method), `README.md:83` (F6 is a declared frontier) | **pass** — fixture minimization for survivors is this lane's own frontier; the document is neither generic filler nor sibling-gate code, and it bounds its own transfer ("S167's input is a crashing web browser, not a test gate; the 1-minimality criterion and the cost accounting transfer, the domain does not") |
| QUALITY 1 falsifiable | `corpus/QUALITY.md:3` | pass — minimality and cost are checkable statements |
| QUALITY 2 source anchor | `corpus/QUALITY.md:4` | **fail as written** — 139-runs attribution (D1), page locators (D2), broken recheck (D3); the §I quote is otherwise verbatim |
| QUALITY 3 observation/inference/unknown | `corpus/QUALITY.md:6` | pass with one defect — inferences are labelled `Inference:`; "the Mozilla test suite" is an unmarked mischaracterization (D4) |
| QUALITY 9 evidence copied into the repo | `corpus/QUALITY.md:24` | **fail as written** — no snapshot; supplied now at `w1/T50ScribePkgDD.src/delta-debugging.pdf` (sha256 `7ed0c812…`) |
| QUALITY 10 header trio + a row opened in the writing round | `corpus/QUALITY.md:27` | **fail as written** — source id S167 has no lane row → re-point to S271 (mined, opened 2026-10-26) |
| QUALITY 34 anchor, not a bare line/page into a file the lane does not own | `corpus/QUALITY.md:251-261` | **fail as written** — page anchors do not resolve on this mirror (D2); use Definition 10 / Proposition 11 / §IV-B / Fig. 12 |
| QUALITY 51 `verified-at` names the byte sha (applied here as the lane's source rows do: round-49 Gate records `194,315 B, sha256 bfddca6a…`) | `corpus/QUALITY.md:560-575`; `corpus/lessons/round-49.md` Gate | **fail as written** — no sha; the fetched bytes are `7ed0c812…` |
| QUALITY 79 a located quote needs a committed snapshot | `corpus/QUALITY.md:944` | **fail as written** — fixable; snapshot pinned this round |
| QUALITY 91 quote compared byte-exact under the declared fold | `corpus/QUALITY.md:1355-1369` | **fail on one quote** — the §I quote matches reading order but not the `-layout` bytes (D5-fold) |
| QUALITY 97 evidence pointers resolve at the landing tip | `corpus/QUALITY.md:1428` | fixable — `CANNOT-ANSWER.md §2` resolves nowhere (D7) |
| QUALITY 98 cold-read precheck before freeze | `corpus/QUALITY.md:1436` | landing obligation — this edit touches `SOURCES.md` and `knowledge/`, both cold-read-pinned |
| QUALITY 7 coverage row same round | `corpus/QUALITY.md:18` | landing obligation |

## Re-open record (CORPUS rule 1 — the package's `opened 2026-10-23` proves nothing)

Fetch (receipt R1): `https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf` →
HTTP 200, 247,738 B, sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`,
17 pages A4, `Producer: GNU Ghostscript 5.50`, created 2001-12-20.

Identity confirmed from the bytes: running head `IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2,
FEBRUARY 2002`, title `Simplifying and Isolating Failure-Inducing Input`, `Andreas Zeller … and Ralf
Hildebrandt`. The venue/volume/issue/month in the package header is correct.

Quote and locator table (extract line numbers: `delta-debugging.txt` is the `-layout` extract, 1,587 lines;
`reading-order` is the default extract, 4,227 lines; the PDF's own page numbers are the mirror's 1…17):

| claim in the package | source state | verdict |
|---|---|---|
| minimality: "is fed with a failing test case, which it simplifies by successive testing. It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear" (§I) | verbatim in the reading-order extract (68-70); the `-layout` extract hyphen-folds `sim-\nplifies` (30-31) | supported in reading order; name the extract quoted |
| "it simplified 896 lines of HTML to the single line that caused the failure. The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC" | verbatim at extract 18-20, **Abstract only**; `grep -n 139` finds only line 19 | quote supported; **attribution refused** (D1) |
| the same reduction's cost | §I (extract 54-57): "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case <SELECT>." §IV-B / Fig. 12 (extract 891-892): "…ter 57 test runs, the ddmin algorithm minimizes the original 896 lines to a 1-line input" | the source's own per-reduction figure is **57** |
| the other runs inside 139 | §IV-B / Fig. 11 (reading-order extract 2105-2106): "After 82 test runs (or 21 minutes), only 3 out of 95 user actions are left"; §V-A (reading-order 2890): "After 26 steps, the line is reduced to the single <SELECT> tag" | 82 + 57 = 139; the 26 is the *second* run on the already-1-line input, not a competing cost for the 896→1 run |
| "p. 183-184" | the mirror prints 1…17 (R1), carries no journal page numbers, and holds 17 pages against the cited 18-page range 183-200 | **unverifiable** (D2) |
| 1-minimality as the contract | Definition 10 (extract 350) and Proposition 11 (extract 562): "ddmin … is 1-minimal in the sense of definition 10." | supported and stronger than the package's informal §I gloss; the package does not cite either |

### Defects found (each with the command that shows it)

- **D1 — 139 is the case-study total, not that reduction's cost.** The one 139 sentence (extract 19) is in the
  Abstract; §I and §IV-B both give 57 for 896 lines → 1 line, and the source's other run count (82 runs, 21
  minutes, §IV-B/Fig. 11, reading-order 2105-2106) plus 57 sums to 139 exactly. Commands:
  `grep -n '139' T50ScribePkgDD.src/delta-debugging.txt` → `19` only;
  `grep -n "After 82 test\|After 57 test runs" T50ScribePkgDD.src/delta-debugging.reading-order.txt` → `2105`,
  `2124`.
- **D2 — page locators do not resolve.** `pdftotext -layout -f 1 -l 1 …` prints page `1`; the last page
  prints `17`; no journal folio appears anywhere. `pdfinfo` → `Pages: 17`. Command in receipt R1. A journal
  page can be *inferred* by offsetting from 183, but the mirror carries 17 pages for the cited 18-page range,
  so any such offset assumes no page was dropped — an inference, not an observation (QUALITY 3).
- **D3 — the package's `recheck:` command cannot see the text.**
  `curl -fsSL URL | grep -c 'minimal test case'` → `0`, exit 1 (compressed PDF stream). Command in receipt R2.
  The package's own parenthetical ("the string was present in the copy opened 2026-10-23") is only true of
  *extracted* text.
- **D4 — "the Mozilla test suite" is not the source.** The source's inputs are the Mozilla web browser's HTML
  input, 95 recorded user actions, GCC and UNIX fuzz inputs (extract 16-20, 553, 875-905, 958-964); no test
  suite is named as the case-study input.
- **D5 — the witness direction is inverted.** The package says the reduction should publish "the entity whose
  removal restores the failure"; the source says "removing any single input entity would cause the failure to
  disappear" (extract 31-33), and C2's minimality check is "removing any single unit no longer kills"
  (`.ufo/evidence/round-50/c2/measure.py:21-23`). A landed sentence in the package's wording would describe
  the opposite witness.
- **D5-fold — the §I quote is byte-exact only in reading order.** Under `pdftotext -layout` the PDF hyphen-folds
  `sim-\nplifies` (layout extract 30-31); under the default reading-order extraction the sentence is whole
  (reading-order extract 68-70, sha256 `2157fadf…`). The package's quote matches the reading-order bytes and
  not the layout bytes, so QUALITY 91 (`corpus/QUALITY.md:1355-1369`) is satisfied only if the entry names the
  extract it quotes from (or declares `printed folded`). Quote from the reading-order extract.
- **D6 — the F6 next move the package proposes is already dead.** The package says "the lane's own B5 probe
  has not been reduced". Round 29 did attempt it: `ddmin made 171 oracle tests and kept nothing`
  (`corpus/knowledge/survivor-fixture-minimization.md:53`), because "B5 is masked under the pinned
  declaration" (`:57`): every exec row of the pinned census declares 755, so the exec-bit arm is redundant
  with the exact-mode check. The live F6 move is round 50's shrinker over the round-49 generator's cases.
- **D7 — dangling file.** `CANNOT-ANSWER.md §2` exists neither in the package (`ls
  /home/vgpnk/Projects/shokuknow/merge/tameshi/` → `MERGE-REPORT.json MERGE-REPORT.md SOURCES.append.md
  amendments knowledge`) nor in the lane (`find . -maxdepth 3 -name 'CANNOT-ANSWER*'` → nothing);
  `ls corpus/knowledge | grep -i ieice` → nothing.
- **D8 — §I conflates two runs; the paper's own numbers separate them.** §I's sentence ("After 57 tests, the
  original 896-line HTML input is reduced to the minimal failing test case <SELECT>") reads as one count for
  the whole reduction, while §V-A says the last stage took "26 steps" (reading-order 2890) and §IV-B/Fig. 12
  gives 57 for 896 lines → 1 line (reading-order 2124). The entry must state the stage boundaries (57 for the
  line run, 26 for the line→`<SELECT>` run) and must not present 26 as a competing cost for the same run.

## Coverage: what the lane holds, what this adds

- **Held already:** the 1-minimal criterion, restated from S024 (tier B) in the mined entry
  `corpus/knowledge/survivor-fixture-minimization.md:3,16` ("1-minimal, meaning that every character
  contained is required to produce the error"); the F6 row itself is `open` with the next move "B5 probe
  fixture size: unmeasured → reduced size + kill check" (`corpus/README.md:83`); the round-29 attempt and its
  honest stop (`corpus/README.md:440-447,482`); a recorded reduction cost of 171 oracle tests (`:53`).
- **New ground the document adds:** the primary TSE 2002 statement (tier A) that replaces the tier-B
  restatement as sole support; Definition 10 (`n-minimal`) and Proposition 11 (ddmin returns a 1-minimal test
  case); and the published **per-reduction** cost figure (57 test runs for 896 lines → 1 line) plus the
  case-study total (139 runs / 35 minutes / 500 MHz), which the lane does not hold at any tier.
- **Therefore the entry must not claim "the lane had no published specification".** It had one, from S024.
  The delta is: primary source, formal definition, and a per-reduction cost datum to compare the lane's own
  `runs` against.
- Nothing here moves F6; the status line is C2's (below).

## Required edits (every one, with its target)

1. `source:` (line 1) — re-point `S167` → **S271**; keep the URL but add `re-opened 2026-10-26`,
   `sha256 7ed0c812…`, and the snapshot path. Row fields the counter reads: type `paper`, tier `A`,
   status `mined`, opened `2026-10-26`, recheck, anchor cell, used-by.
2. `corpus/SOURCES.md` — append a row after `:145` (S270) with those 11 cells; **append** a registry note
   after `:499` recording that the Zeller lead bullet at `:278` moved to row S271 and that the earlier stop
   rationale at `:184` ("author PDFs timed out (HTTP 000), ResearchGate HTTP 403, DOI resolver gave metadata
   only") is superseded by the course mirror (HTTP 200, sha above). Do not delete `:278` or `:184`
   (append-only, QUALITY 4/35).
3. `verified-at:` — `2026-10-26`, naming `7ed0c812…` and the mirror's 17-page/1…17-pagination fact
   (QUALITY 51).
4. `recheck:` — replace the broken command with the tested one:
   `curl -fsSL URL | pdftotext - - | tr -s ' \n' ' ' | grep -c 'removing any single input entity'` (expect
   `1`; receipt R2). Use the default reading-order extraction, not `-layout`: `-layout` hyphen-folds
   `simplifies` and would break a quote check. A second clause may check `After 57 test runs` (expect `1`).
5. Quotes — quote from the reading-order extract (`w1/T50ScribePkgDD.src/delta-debugging.reading-order.txt`,
   sha256 `2157fadf…`); label the 139/35-minute sentence **Abstract** (not "§Abstract/§I"); state that §I and
   §IV-B give 57 for the 896→1 reduction and §V-A gives 26 steps for the line→`<SELECT>` stage; cite
   **Definition 10** and **Proposition 11** by name for the 1-minimality contract (page anchors unreplaceable
   on this mirror).
6. Refuse the 139-as-reduction-cost sentence. Landable form: "the Abstract reports the case study's total
   cost as 139 automated test runs, or 35 minutes on a 500 MHz PC; the source's two runs are 82 test runs
   (21 minutes) for the 95-user-action reduction (§IV-B, Fig. 11) and 57 test runs for the 896-line→1-line
   HTML reduction (§I; §IV-B, Fig. 12), which sum to 139; the line→`<SELECT>` stage then took 26 steps
   (§V-A)."
7. Fix the witness direction: the witness is the entity whose removal makes the failure **disappear** (the
   kill is lost), not one whose removal restores it.
8. Replace "the lane's B5 probe has not been reduced" with the round-29 record:
   `survivor-fixture-minimization.md:53` (171 oracle tests, nothing kept) and `:57` (B5 masked under the
   pinned declaration), and point the F6 move at the round-49 generator's cases.
9. Drop `CANNOT-ANSWER.md §2`; if the IEICE comparison is kept, name it in words or drop it (D7).
10. Add the §Coverage delta paragraph so the entry does not claim to supply a contract the lane already
    held from S024.
11. Keep `ground: F6 (fixture minimization for survivors)`; add no status claim in the entry itself.
12. Reference the lane's shrinker result as follows: `tools/shrink-case.py` (C2 deliverable) is the reduction
    implementation; its unit vocabulary is *registry line + staged line + map entry*
    (`contract.json:54`), its cost is `runs` = every guard invocation, pristine and mutant (`:54`), and its
    1-minimality is checked by removing each single unit
    (`.ufo/evidence/round-50/c2/measure.py:21-25`). The status line is `corpus/README.md` carrying
    `F6 … held (round 50)` plus the deciding receipt `.ufo/evidence/round-50/after/c2.stdout`
    (`C2_R50: … C2_R50_PASS=…`); the entry must not claim F6 held from its own text. Ordering: QUALITY 97
    (`corpus/QUALITY.md:1428`) means the entry may cite the after-receipt only if it exists at the landing
    tip — otherwise name it in words as pending. Compare the lane's own cost datum (round-29's 171 oracle
    tests, `survivor-fixture-minimization.md:53`) with the published 57, and say which quantity each measures.
13. `corpus/README.md` — a coverage row for the new entry (QUALITY 7) and, under the F6 frontier block, the
    `held (round 50)` line C2 requires (`measure.py:324-333`). Do not edit the F6 table row at `:83`
    (append-only).
14. Before freezing the content revision, run `.ufo/evidence/round-48/quality/coldread-precheck.sh LANE BASE
    CAND` (QUALITY 98) — this edit touches `SOURCES.md` and `knowledge/`.

## Adjacency (reported, not absorbed)

- **Same document, second package entry:** `repeat-control-measured-n3.md:3,54` also cites the staged S167
  with "§I (minimality and reduction cost)" and the same "reduction cost is the same currency" inference. Its
  ground (F3 repeat control) is already held (round 12, `tools/repeat-control.py`), so it is same-ground, not
  new coverage; not my item. T50ScribeSrcHeld confirmed to me that their held doc covers S022/S024 only and
  cites no S167 — no duplicate row from that seat.
- **F10 adjacency:** `corpus/README.md:599` says F10's next move is "a second gate, or shrinking"; the
  round-50 shrinker shrinks F10's generator cases, so the same artifact serves both rows. The entry must not
  claim F10 movement.
- **S024 corroboration (other seat, reported):** T50ScribeSrcHeld re-fetched S024 → 200, 496,906 B,
  sha256 `3abede35…`, byte-identical to the round-29 snapshot — the held S024 restatement the delta above is
  measured against is still live.

## Bounds and receipts

- Read-only on the lane outside `.ufo/waves/round-50/w1/T50ScribePkgDD*`; no git/jj mutation, no fleet-root
  write, nothing read under `/home/vgpnk/.local/state/`, no mutant names or edits quoted from
  `control/c2-*.stdout`.
- No counter was run; none was needed. No tool installed (`curl 8.23.0`, `pdftotext 26.08.0`, `python3
  3.14.8`; host pacman guard paused and unused).
- Pinned bytes and extract: `.ufo/waves/round-50/w1/T50ScribePkgDD.src/delta-debugging.pdf`
  (sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`, 247,738 B);
  `.ufo/waves/round-50/w1/T50ScribePkgDD.src/delta-debugging.reading-order.txt` (4,227 lines, sha256
  `2157fadf4f0c45151a5fa6bee89e839fb6cec81ce2034f110cedb1762a412145` — the extract to quote from); and
  `.ufo/waves/round-50/w1/T50ScribePkgDD.src/delta-debugging.txt` (`-layout`, 1,587 lines; do not quote from it).
- Command receipts R1–R7: `.ufo/waves/round-50/w1/T50ScribePkgDD/receipts.md`.
- Independent corroboration: T50ExecSrcZeller fetched the same URL and reported the same sha256/byte count/17
  pages, the same raw-grep failure, and the 82 + 57 = 139 decomposition; that seat states it is opening no
  registry row (`.ufo/waves/round-50/w1/T50ExecSrcZeller/`). The S271 adoption is the L1's call.
- Scratch `/fast/scratch/hyaku/tameshi-r50/T50ScribePkgDD` deleted before this seat finished.

## Summary

- **Admit** `delta-debugging-minimization-contract.md` (F6) with 14 edits; **refuse** its 139-runs cost attribution — the source's own counts are 82 (actions, 21 min) + 57 (896 lines→1 line) = 139 (receipts R7).
- Decisive gate: QUALITY 10 clause 2 — `source: S167` names no lane row (reserved S161–S255); open **S271** with the pinned snapshot `7ed0c812…` (HTTP 200, 247,738 B, 17 pp).
- Also fail as written: QUALITY 2 (locators, recheck returns 0), 9/79 (no snapshot), 34 (page anchors unverifiable on a 17-page mirror), 91 (fold is `-layout`-specific), 97 (dangling `CANNOT-ANSWER.md`).
- The F6 move the document proposes (B5) is already dead: round 29 spent 171 oracle tests and found B5 masked under the pinned declaration; round 50's `tools/shrink-case.py` over the round-49 generator's cases is the live path.
- Coverage delta, not a new contract: 1-minimality was held from tier-B S024; this adds the tier-A origin, Definition 10 / Proposition 11, and a per-reduction cost datum.
- Receipts: `w1/T50ScribePkgDD/receipts.md` (R1–R7); pinned bytes and both extracts in `w1/T50ScribePkgDD.src/`; scratch deleted before exit.
