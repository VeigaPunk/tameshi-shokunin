# T49ScribePkgAsFixture — assimilation triage: `pbt-generator-as-fixture.md` (theme F10)

Seat: leaf scribe, tameshi round 49 (hyaku run 9), wave 1. Base `8ca67421111fa354b47b803358391d0b07fc6db9`;
lane worktree head read-only at `455b2cd` while other seats were mid-wave (`git status --porcelain` showed
`M SCORECARD.md` and untracked wave/evidence files — none touched by this seat).
Candidate: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/pbt-generator-as-fixture.md`
(49 lines, read-only package copy).
Tooling installed or upgraded: **none**. `python3 3.14.8`, `pdftotext 26.08.0` (poppler) already present.
This seat decides nothing; the verdict below is a triage recommendation for the L1 and the round's `## Gate`.

No lane file was edited. The only writes are this report and a scratch dir under
`/fast/scratch/hyaku/tameshi-r49/T49ScribePkgAsFixture` (deleted before yielding). Nothing was read under
`/home/vgpnk/.local/state/`; no C2 control stdout was opened.

---

## 0. Verdict

**ADMIT narrowly — two rows, one method entry — conditional on the nine edits in §3.**

Decisive reason (the one criterion that alone decides it): the lane holds **no** PBT-generator ground at all, and
the entry supplies one rule no held entry states.

- Coverage ground unheld: `grep -rn "S018\|S019\|S020\|S021" corpus/knowledge/ | wc -l` → `0`;
  `grep -rli "property-based\|\bPBT\b" corpus/knowledge/*.md | wc -l` → `0`;
  `grep -n -i "property-based\|PBT" SKILL.md` → no hit; F10 is `open` (`corpus/README.md:87`:
  `| F10 | PBT generators for gate fixtures | S018, S019, S020, S021 | open | no PBT fixture method → one generator against a named fixture gate |`).
  The four F10 seed rows are `queued` with `used-by=—` (awk over `corpus/SOURCES.md:29-32`, §6 R1), so nothing
  cites them.
- The novel rule is the survivor side. `corpus/knowledge/r43-survivor-resolution-rule.md:57-60` defines
  K / D / E / U and nothing else. The candidate's second source supplies a fifth, practical class the lane does
  not hold: a survivor left **deliberately alive** because killing it would pin behaviour the specification
  never fixed (message wording ×9, a default argument ×3 — the source's own table, §2 R4), killed-mutant count
  168 → 171 after 8 property tests were added (§2 R5). That is a boundary the lane's F8/F10 work needs: a
  generator tuned to kill message-wording mutants would over-specify, and the lane's rule has no name for it.
- PROVINCE fit: the subject is fixture craft, not a product domain (`PROVINCE.md:3-11`, `:14-16`), and F10 is
  the lane's own frontier row (`PROVINCE.md:40-42`). [INFERENCE] the entry's first half (a library's own
  definition of PBT) is background, not a contribution; only the "generator drives the named gate, the property
  is the deliverable, over-specification is not a kill target" triad is admissible ground.

Flip to **refuse**: if the L1 will not open both rows in *this* round, the entry is refused by **QUALITY 10**
(`corpus/QUALITY.md:27-30` — an external source enters through a row opened in the round that writes it) under
the round-48 precedent for exactly this defect (`corpus/lessons/round-48.md:270`: refused because its `source:`
cited staged `S205` and "the lane has never opened" it). Second flip: if the entry is adopted as a **general**
claim about generator efficacy, `PROVINCE.md:14-16` refuses it (a pattern is general only from two independent
lanes) and the source's own caution forbids the numbers' transfer (§2 R6).

---

## 1. Gates applied

### 1.1 PROVINCE scope — PASS (with a product-domain caution)

- Domain is "verification-fixture craft … hermetic suites, mutation testing, fail-closed arms, verdict-line
  discipline" (`PROVINCE.md:3-6`). A property-based generator that drives a named gate fixture is that craft.
- `PROVINCE.md:14-16` refuses product domains ("every lane's gate remains its own"). The candidate's worked
  instance is a Japanese SI approval workflow with audit-log requirements — a product domain. It is admissible
  only as the *vehicle*; the entry must not claim audit-log correctness, HTTP-404/409 semantics or SI internal
  control as tameshi ground. The candidate already does this correctly (`## What this means for the lane's F10
  move`), with one slip in the parenthetical (§4 F3).
- Generic-material refusal: the S157 half is largely the library's own definition. It survives only because
  QUALITY 3 lets it stand as labelled inference and because the *pair* (definition + worked instance) states a
  design decision the lane must make this round. A third "PBT is good" entry from the same package would be
  refused.

### 1.2 QUALITY bar — every applicable criterion

| # | Criterion (line) | Status | What decides it |
|---|---|---|---|
| 1 | falsifiable or opinion (`corpus/QUALITY.md:3`) | PASS after edit E7 | claims are labelled Inference; one factual claim is false today (§4 F2) |
| 2 | a source per claim (`corpus/QUALITY.md:4-5`) | **FAIL as-is**, fixed by E1/E2 | `source:` ids are staged, not lane rows; the JOSS `recheck:` command fails today (§2 R7) |
| 3 | observation / inference / unknown separate (`corpus/QUALITY.md:6`) | PASS | the entry has `## What the sources state` / `## What this means` / "What is still unmeasured" |
| 7 | coverage-map row same round (`corpus/QUALITY.md:18-20`) | open | must land with the entry (E8); F10's status cell changes only through C2's measured move |
| 9 | evidence copied into the repo before the commit citing it (`:24-26`) | open | snapshots must be committed with the digests in §2 (E9) |
| 10 | header trio + row opened in the writing round + tier-C never sole support (`:27-30`) | **FAIL as-is**, fixed by E1/E2/E5 | staged S157/S166, opened 2026-10-23, cited by a round-49 entry |
| 26/35 | corrections are appended, never rewritten (`corpus/QUALITY.md:150`, `:262`) | n/a now | applies if the entry lands with a defect |
| 34 | citation into a moving page anchored by heading/sentence + rev (`QUALITY.md`, round 18 item 34) | open | Zenn has no commit; anchor by section number + quoted sentence + snapshot digest (E3) |
| 87 | a labelled quote length is measured (`corpus/QUALITY.md:1223`) | PASS here | every count in §2 was measured with the lane's own `fold` (method in §2 R0); the candidate labels no count |
| 94 | a refusal cites its decisive criterion + flip (`corpus/QUALITY.md:1382`) | n/a | this is an admit; the *flip to refuse* is stated in §0 with its criterion |

Tier reading for the two proposed rows (definitions `CORPUS.md:92-96`): JOSS = `paper` / **A**, scoped to "the
library's own description of its contract"; Zenn = `community` / **B** ("expert write-up with reproducible
detail": mutant counts, a per-survivor table, and a public repo `github.com/SeckeyJP/j-six`). `community` is
never A (`CORPUS.md:94`). The F10 *instance* claim therefore rests on the B row alone; §4 F5 records that the
paper was not re-run.

### 1.3 Coverage map / F10 / the S018–S021 seeds — unheld, no duplicate

Receipts in §6 (R1). The F10 seed rows are Candidate sources, not evidence: `corpus/SOURCES.md:273` states "a lead
is not evidence and never a row", and the JOSS DOI itself sits in the same Leads list at `corpus/SOURCES.md:278`.
Promoting a lead to a row by opening it is exactly CORPUS rule 1, and it is **not** a duplicate: staged S157's
document appears in the registry only as that lead (`grep -c "10.21105" corpus/SOURCES.md` → `1`, the bullet),
and `tools/staged-id-guard.py` lists staged S157 as a collision whose document is **not** held (§2 R8 `held`
map has no S157).

### 1.4 CORPUS rule 1 — re-opened today, both sources (satisfied by this seat, not by the package date)

`/home/vgpnk/Projects/shokunin/CORPUS.md:112-118`: a row is written only after opening the source in the round
that writes the row; the round lesson's `## Gate` records URL, access date and a ≤25-word quote with its
location. The package's `fetched 2026-10-23` / `verified-at: 2026-10-23` proves nothing this round. Both
documents were opened 2026-10-26 by this seat; §2 holds the access receipts, digests and located passages.

---

## 2. Receipts (access date 2026-10-26)

**R0 — quote-length method.** Token counts below are the lane's own measure: `c1.fold(quote).split()`, importing
`fold` from `.ufo/evidence/round-45/freshness/measure.py` exactly as criterion 87's falsifier does
(`corpus/QUALITY.md:1223-1260`). This imports a function; no counter was invoked with `--lane/--rev`, no claim
was scored. Letter/digit counts are given second, because criterion 87 distinguishes them. Normalization for the
Zenn text: drop `<script>/<style>`, tag → line break, HTML entity unescape, then keep non-empty lines (this is
*not* the round-48 amendment-2 "whitespace collapse"; every quote below is a single text node, so both
normalizations give the same bytes — the writing round must still re-extract with amendment 2 for the committed
snapshot).

**R1 — JOSS DOI landing page.** `curl -fsSL -m 60 'https://doi.org/10.21105/joss.01891' -o joss-01891.html`
→ exit 0, **20 076 B**, sha256 `a03e82614b96a6a263347a9b9fd45682ae097001593d3be170503acc59b27eed`.
It carries the landing metadata the entry cites: citation block
`MacIver et al., (2019). Hypothesis: A new approach to property-based testing. Journal of Open Source Software, 4(43), 1891, https://doi.org/10.21105/joss.01891`
(the string `4(43), 1891` is present in that block; the same line also appears in the page's meta description),
and `Submitted 12 November 2019 • Published 21 November 2019`.
It carries **no abstract**: `grep -ci 'property-based' joss-01891.html` → `10` (title/meta only),
`grep -c 'QuickCheck' joss-01891.html` → **`0`**, and the candidate's own recheck command
`curl -fsSL 'https://doi.org/10.21105/joss.01891' | grep -c 'QuickCheck family of libraries'` prints **`0`**
with grep exit **1** (§4 F1).

**R2 — JOSS paper PDF (the abstract's real carrier).**
`curl -fsSL -m 90 'https://joss.theoj.org/papers/10.21105/joss.01891.pdf'` → exit 0, **128 906 B**, sha256
`35a91bf389cd3b1b4700467d01da1b05378805467abf7660100882f7ba614998`; `pdftotext -layout` →
`joss-01891.txt`, abstract at lines 11-13 under the page's `Summary` heading.
Located quotes (found once each in the collapsed text):
- `Property-based testing is a style of testing popularised by the QuickCheck family of libraries` —
  **14 whitespace tokens**, 15 letter/digit words. This is the sentence the candidate paraphrases.
- `which integrates generated test cases into existing software testing workflows` — **10 whitespace tokens**,
  10 letter/digit. **Recommended Gate quote for the JOSS row**: contiguous after whitespace collapse
  (`… Johansson, & Wiger, 2006), which integrates …`), and it is the only sentence that grounds the row's
  `teaches` ("the generated cases go inside an existing workflow").
- The PDF's page furniture repeats `Submitted: 12 November 2019` and `Published: 21 November 2019` (both found),
  so the dates are verifiable on either carrier.

**R3 — Zenn article page.** `curl -fsSL -m 60 'https://zenn.dev/seckeyjp/articles/j-six-mutation-testing'`
→ exit 0, **171 806 B**, sha256 `ac6d519e1b92f918a5f3fae73e45b311cecc108d68c49e1ca1ffb98a588d7caf`;
normalized text 542 non-empty lines; author handle `SeckeyJP` (lines 2, 494); date `2026/09/20` (line 5).
Section headings are numbered, and the candidate's locator resolves: `3. 結果 ①: カバレッジ 99% で mutation
score 91.8%` (line 102) and `4. 生存ミュータントから「性質」を導く` (line 188).

**R4 — the 15-survivor table (the deliberate-survivor class).** Lines 110-146 (header at 107-109, after the line-105 sentence): five rows, 9 + 3 + 1 + 1 + 1 = 15;
the last column marks three `✓ 本物` (boundary `amount <= 0` → `<= 1`; audit-log actor
`_log(req, Action.REMAND, actor, note)` → `_log(req, Action.REMAND, note)`; audit-log reason
`… actor, note)` → `… actor, )`). The 12 non-holes are 9 message-wording mutants and 3 `note` default-argument
mutants. Located quotes (each found once): `183 ミュータント: 168 killed / 15 survived` (line 103, **7**
whitespace tokens, 5 letter/digit); `生き残った15件を分類しました` (line 105, **1** token).

**R5 — the property → mutant kill.** `PROP-nnn` properties are added to the requirement spec and converted to
Hypothesis properties (lines 193-208, 262, 287); the re-run with 8 added tests (37 → 45) reports
`183 ミュータント: 171 killed / 12 survived` (line 323, **7** whitespace tokens) = 93.44 % (+1.64 pt), and the
article states the three targeted mutants were killed exactly and no other mutant changed state (line 325:
`狙った3件を正確に殺し、それ以外のミュータントの状態は変わりませんでした`). The 12 remaining are **kept alive on
purpose** with the stated policy `文言は仕様ではない` (line 332: pinning wording that the spec does not fix makes
a correct implementation fail as soon as the wording improves). `grep -c 'PROP-'` on the raw page → `8`.

**R6 — the source's own non-generalization.** Line 31, found once:
`題材は1つの小規模なシステム（207 ステートメント）で、一般化できる数字ではありません` (**2** whitespace tokens,
2 letter/digit). Also line 455: `99% と 91.8% の差は、この題材での値にすぎない` (**4** tokens). Because
the caveat is 2 tokens, it can carry no criterion-87 style count label of its own; it belongs in the entry body,
not in a `## Gate` quote position.

**R7 — recheck commands, tested today.**
- Candidate's JOSS recheck (`curl … doi … | grep -c 'QuickCheck family of libraries'`): prints `0`, exit 1 —
  **the stated expectation `1` is false**.
- Replacement, tested: `curl -fsSL 'https://joss.theoj.org/papers/10.21105/joss.01891.pdf' | pdftotext - - |
  tr '\n' ' ' | grep -o 'QuickCheck family of libraries' | wc -l` → `1`.
- Staged Zenn recheck (`grep -c 'PROP-'`) → `8` today, non-zero as stated; `grep -c '168 killed / 15 survived'`
  → `2` on the raw page (body plus a payload copy), so a Zenn recheck must expect the observed count, not `1`.

**R8 — the staged-id guard, run read-only (not a counter, no claim scored).**
`python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json`
→ exit 0, `verdict=answered`, `registry_sha256=7e99c6a068521cf3e3d581a52a74e8f58551309ecb2c3a284dda9b9c17235c7e`
(128 rows, 109 distinct documents, max `S268`), `staged_sha256=020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807`
(103 rows, max `S255`), `collisions=[S153…S160]`, `column0_miss=[]`, `unmapped=[]`, `cascade_count=0`,
`held={S153:S105, S154:S106, S155:S261, S158:S262, S159:S155, S160:S156}`, **`next_free=S269`,
`safe_floor=S269`**. Staged **S157 collides by id and is absent from `held`** → its document is new; staged
**S166 collides with nothing** but is still a staged id, so `tools/staged-id-guard.py:33-35,187-189` puts any
partial adoption at or above the safe floor and a `--map` must be validated before appending.

---

## 3. Edits the admit needs (mandatory, in landing order)

**E1 — open two rows in the writing round; ids by document, from the guard's safe floor.**
`corpus/SOURCES.md` currently ends at `S268` and the guard's `next_free` is `S269`. The same round's C2 claim
registers QuickCheck and Smallbone (`contract.json` `claims.C2.sourced`; the scout seat
`.ufo/waves/round-49/w1/T49ScoutSrcHypothesis.md` §3 proposes staged S182→`S269`, staged S183→`S270`).
**Allocate the four ids together**; on that proposal this entry's rows take **S271** (staged S157, JOSS
Hypothesis) and **S272** (staged S166, Zenn). The ids are the L1's decision and only a guard-validated
`--map` may fix them (`.ufo/evidence/round-45/assimilation/adoption-map.json` is the precedent shape).
Both rows: `opened 2026-10-26`, `status mined`, `used-by corpus/knowledge/pbt-generator-as-fixture.md`, and a
`recheck` that passes today (R7), not the staged one.
*Superseded in part — see §7: a concurrent sibling append landed S269/S270 while this seat worked, so the floor
this seat measured first (S269) is now S271 and the proposed pair S271/S272 is unchanged.*

**E2 — re-point the entry header and re-ground it.**
`source:` line 1 becomes the two new ids (`S271`, `S272`) with new locators — JOSS: `§Abstract (Summary), p. 1,
PDF sha256 35a91bf3…`; Zenn: `§3. 結果 ① and §4 生存ミュータントから「性質」を導く @ page of 2026-09-20,
snapshot sha256 ac6d519e…`. `verified-at: 2026-10-26`. `recheck:` = the two commands in R7 with their observed
counts.

**E3 — anchor the Zenn citation against a snapshot, not a live page.**
QUALITY 34 (a moving, non-owned page) and the candidate's own section numbers: anchor by `§3` / `§4` plus the
quoted sentences in R4/R5, with the committed snapshot and digest. The staged row's anchor
(`§3. 結果 and §4. 生存ミュータントから「性質」を導く`) already resolves (R3) — keep it and add the digest.

**E4 — fix the abstract's location.** The entry's first `source:` line puts the abstract on the DOI landing page.
It is not there (R1: `QuickCheck` count 0); it is in the PDF (R2). A locator that names a page its quote is not
on fails QUALITY 2 and the `recheck:` clause of QUALITY 10.

**E5 — tier and scope per row.** JOSS `paper/A` scoped to "the library's own description of its workflow
integration"; Zenn `community/B` scoped to "one worked instance of survivor classification and property-driven
kills on a 207-statement system". `community` is never A (`CORPUS.md:94`). State the Zenn instance's limits with
the source's own caveat (R6) and say the F10 *efficacy* claim stays unmeasured until the C2 pilot's deciding run.

**E6 — the entry's Zenn half must be scoped to F10, not to F8.**
The classification table restates ground the lane holds (`r43-survivor-resolution-rule.md:57-60`). What is new is
the *deliberate survivor* class and why it is not a kill: message wording ×9 and default argument ×3 are
"semantically different but not specified", so a property that pins them over-specifies. Add that as the entry's
claim (one falsifiable sentence) and cite the table; drop the general "classify survivors one by one" sentence
to a pointer at the held rule. Also record which of the candidate's sentences are **predictions** about this
round's pilot, so QUALITY 6 can carry their outcome in the same entry.

**E7 — correct the two factual slips and the phrasing that claims held ground.** §4 F2 and F3, plus "the same
discipline the lane already holds in English (its own PBT rows S018–S021)" → "four `queued` F10 seed rows
(`corpus/SOURCES.md:29-32`, `used-by=—`) and no held PBT entry".

**E8 — coverage-map row in the same round** (`corpus/QUALITY.md:18-20`): a row for the entry with `S271, S272`;
F10's status cell changes only through C2's measured move (`contract.json` `claims.C2.predicate`).

**E9 — commit the snapshots with the digests before the commit that cites them** (QUALITY 9): R1, R2, R3 files
plus the fetch receipts, under `.ufo/evidence/round-49/…`; a scratch path is not citable.

---

## 4. Claims falsified, unverified, or imprecise

| id | claim | observed | consequence |
|---|---|---|---|
| F1 | `recheck:` — `curl … doi … \| grep -c 'QuickCheck family of libraries'` expects `1` | prints `0`, exit 1 (R1, R7) | **falsified**; the command cannot pass. Edited by E2 |
| F2 | "the lane already holds in English (its own PBT rows S018–S021)" | all four rows are `queued`, `used-by=—` (§6 R1); zero knowledge entries cite them | **falsified**; E7 |
| F3 | "at 99% **line** coverage" | the source's table says `カバレッジ 99%` with `207 ステートメント中 未到達 2` — statement coverage 205/207 (R3 line 71); the article's own contrast at line 459 speaks of lines separately | **unverified qualifier**; write "statement coverage" |
| F4 | "3 real holes (2 of them audit-log holes **where the remand reason was not recorded**)" | the two audit-log holes are (a) the actor argument shifted into the note field, (b) the remand reason dropped (R4 table) | imprecise; only one is the missing reason |
| F5 | the Zenn instance's reproducibility | the article publishes a repo (`github.com/SeckeyJP/j-six`), `mutmut 3.7.0`, and make targets (R3 lines 80, 91-94) | **not re-run by this seat** (out of triage scope). Tier B stands on "reproducible detail", not on a reproduction |
| F6 | the abstract sentence's wording | byte-exact match after whitespace collapse (R2), including the paper's British `popularised` and `& Wiger, 2006)` | verified; no edit |

Not disputed: the 207-statement size, the 183/168/15 and 171/12 counts, the 3 `本物` holes, the `PROP-nnn` →
Hypothesis conversion, and the source's caution quote — all located in R3-R6.

---

## 5. Adjacency and hazards for the L1

1. **C2 pilot overlap.** `contract.json` `claims.C2` requires `corpus/knowledge/pbt-generator-pilot.md` (measured,
   seeded 4949, 400 cases, 12 hidden mutants). The candidate's §"What this means" is a *design prediction* of that
   pilot. If both land, the pilot carries the measurement and this entry carries the method + the survivor-class
   boundary; the entry must not be read as the F10 move's evidence (QUALITY 6 binds its predictions).
2. **Id allocation is shared with C2** (E1). The guard's `next_free`/`safe_floor` is `S269` today; four new rows
   (QuickCheck, Smallbone, JOSS, Zenn) in one round must be mapped as one document-keyed set.
3. **The novel class needs a home.** "Deliberately not killed because killing it would pin an unspecified detail"
   is not in K/D/E/U (`r43-survivor-resolution-rule.md:57-60`). Either this entry names it (preferred, E6) or the
   round names it debt; leaving it unnamed is how a later generator gets tuned to kill message-wording mutants.
4. **F8 stays where it is.** The candidate's F8 half (`§3`/`§4` classification) duplicates held ground; only its
   policy boundary is new. `PROVINCE.md:40-42` moves ground to Core only through an admitted, source-headed entry
   citing a `mined` row — E1 supplies the rows; the entry must not move F8 or F10 on its own.
5. **S018–S021 stay `queued`** unless the round mines them; this entry does not make them `mined`, because the
   candidate cites neither. Its statuses and `used-by` cells are untouched by this seat.
6. **No package claim about "a second language" is a two-lane proof.** The Zenn article is one project, `B`;
   `PROVINCE.md:14-16` wants two independent *lanes* for a general pattern, so nothing here may be phrased as
   "PBT works for gate fixtures" — only "this is the shape our F10 pilot must take, and here is one instance".

---

## 6. Findings — file:line and the command that shows it

| id | finding | anchor | command |
|---|---|---|---|
| R1a | F10 is `open`; seed rows are candidate sources | `corpus/README.md:87` | `sed -n '87p' corpus/README.md` |
| R1b | S018–S021 are `queued` with no citing entry | `corpus/SOURCES.md:29-32` | `grep -rn "S018\|S019\|S020\|S021" corpus/knowledge/ \| wc -l` → 0; `grep -rli "property-based\|\bPBT\b" corpus/knowledge/*.md \| wc -l` → 0; awk over the four rows prints `used-by=—` |
| R1c | the lane holds no PBT method in its skill | `SKILL.md:810` is the only `F10` substring hit and is a sha256 | `grep -n -i "property-based\|PBT" SKILL.md` → no hit |
| R2a | the JOSS DOI is a Leads bullet, not a row; a lead is never evidence | `corpus/SOURCES.md:278`, `:273` | `sed -n '273p;278p' corpus/SOURCES.md`; `grep -c "10.21105" corpus/SOURCES.md` → 1 |
| R2b | staged S157 collides with held S157 (argparse) | `corpus/SOURCES.md:127` | `grep -n "^| S157 " corpus/SOURCES.md` |
| R8 | guard: `next_free=S269`, S157 collides without being held, S166 is a reserved staged id | `tools/staged-id-guard.py:21-47,172,187-189` | the `--registry … --staged … --json` invocation in §2 R8 |
| F1 | the candidate's recheck is false | package entry line 2 (`recheck:`) | the curl+grep in R7 → `0`, exit 1 |
| F3 | the source reports statement coverage, not line coverage | Zenn lines 66, 71, 459 | §2 R3/R4 extraction; `207 ステートメント中 未到達 2` |
| R4 | 15 survivors = 9 wording + 3 default-arg + 3 real | Zenn lines 105-146 | extraction quoted in R4 |
| R5 | 168→171 killed after 8 property tests; 12 kept intentionally | Zenn lines 323-332 | extraction quoted in R5 |
| R6 | the source forbids generalizing its numbers | Zenn line 31 | extraction quoted in R6 |
| P1 | the lane's survivor rule has no deliberate-survivor class | `corpus/knowledge/r43-survivor-resolution-rule.md:57-60` | `grep -n "K — killed\|U — unresolved" corpus/knowledge/r43-survivor-resolution-rule.md` |
| P2 | unopened staged row = decisive refusal precedent | `corpus/lessons/round-48.md:270` | `sed -n '270p' corpus/lessons/round-48.md` |
| P3 | criterion 10 requires the row in the writing round | `corpus/QUALITY.md:27-30` | `sed -n '27,30p' corpus/QUALITY.md` |
| P4 | coverage-map row is owed the same round | `corpus/QUALITY.md:18-20` | `sed -n '18,20p' corpus/QUALITY.md` |
| P5 | quote counts must be measured, not written | `corpus/QUALITY.md:1223` | `sed -n '1223,1230p' corpus/QUALITY.md` |
| P6 | the tier rule (`community` never A, B = reproducible detail) | `CORPUS.md:92-96` | `sed -n '92,96p' /home/vgpnk/Projects/shokunin/CORPUS.md` |

The two source snapshots and the guard JSON lived in `/fast/scratch/hyaku/tameshi-r49/T49ScribePkgAsFixture`
and that directory is removed before this seat yields; their digests in §2 are the checkable residue, and E9
requires the writing round to fetch and commit them.

---

## 7. Append-only note — a concurrent sibling write moved the registry floor (observed 2026-10-26)

This seat did not edit `corpus/SOURCES.md`. At its first check the file was clean (`git status --porcelain`
listed only `M SCORECARD.md` plus untracked wave/evidence files); at its last check the same command listed
`M corpus/SOURCES.md`, `git diff --stat -- corpus/SOURCES.md` → `1 file changed, 5 insertions(+)`, and the
added rows are `corpus/SOURCES.md:144` (`S269` QuickCheck, Claessen/Hughes ICFP 2000, `paper/A`) and `:145`
(`S270` Smallbone, Chalmers TR 76L, `paper/B`) — the two rows C2's `sourced` clause needs.

Re-observed guard, same read-only invocation as §2 R8, on the current working-tree bytes:

```
verdict=answered next_free=S271 safe_floor=S271 registry_max=S270
registry_rows=130 registry_docs=111 collision_count=8 unmapped=[] cascade_count=0
registry_sha256=e3978719e33c184663fe6b03fcaedc2525e471ed4e7302715272890e3ce946a9
held={S153:S105, S154:S106, S155:S261, S158:S262, S159:S155, S160:S156}
```

Consequences, stated as observation only:

- §2 R8's receipt stays as measured (`registry_sha256 7e99c6a0…`, 128 rows, `next_free=S269`); the current bytes
  are `e3978719…` with 130 rows and `next_free=S271`. Both are true of their own bytes.
- E1's proposal is unchanged and now unambiguous: this entry's rows take **S271** (staged S157, JOSS) and
  **S272** (staged S166, Zenn), beside C2's already-landed S269/S270.
- The sibling append is *not* a C2 deciding run and does not by itself make the F10 claim true; the guard's
  `held` map is identical, so staged S157 is still an id collision with a new document.
- Criterion 20/53 territory: this seat ran no lane tool that writes, so nothing here needs a correction beyond
  this note. A seat that later cites §2 R8 should cite §7 beside it.

---

## Summary

- Verdict **admit narrowly** (2 rows + 1 entry, nine edits §3): the lane holds no PBT-generator ground (F10 `open` `corpus/README.md:87`; no entry cites S018–S021) and the entry adds a deliberate-survivor class K/D/E/U lacks.
- Flip to refuse: rows not opened this round (QUALITY 10, `corpus/QUALITY.md:27-30`; precedent `corpus/lessons/round-48.md:270`), or adopted as a general efficacy claim (`PROVINCE.md:14-16`).
- Both sources re-opened 2026-10-26: JOSS page 20 076 B `a03e8261…`, PDF 128 906 B `35a91bf3…`; Zenn 171 806 B `ac6d519e…`.
- Candidate defect: its `recheck:` prints 0 and fails, and "§Abstract" names the DOI page, which carries no abstract — it is in the PDF at p.1 `Summary`.
- Gate quotes measured: JOSS `which integrates generated test cases into existing software testing workflows` (10 tokens); Zenn `183 ミュータント: 168 killed / 15 survived` (7 tokens).
- Falsified: "the lane already holds … S018–S021" (all four `queued`, `used-by=—`); "99% line coverage" is statement coverage 205/207; the audit-log parenthetical names the wrong pair.
- Guard read-only: `next_free=S271` after a concurrent sibling append of S269/S270 (§7; S269 when first measured); staged S157 collides by id with a new document, S166 is reserved — map the four rows by document, then `--map`.
