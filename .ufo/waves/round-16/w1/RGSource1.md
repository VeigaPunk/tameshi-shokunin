# RGSource1 — C1 source row: Stryker "Supported mutators" → arm classes A–E

Seat: RGSource1 (source scout, wave 1). Scope: open the StrykerJS **supported-mutators** page
this round (not the mutant-states page S001), record it as a source with URL/date/revision/
anchor/quote, and map every StrykerJS operator class onto the arm-class matrix A–E
(`corpus/knowledge/arm-class-matrix.md`, rows A–E; §13 for the `round-gate.mjs` projection).
**No mutant was run. No gate mode was executed.** Reads of the pinned artifact are byte
reads of a scratch copy; scratch `/tmp/tameshi-r16-RGSource1-O2Dq/`. Report-only seat: wrote
this file and nothing else.

Anchors: **O** = observed (command + exit + key line, or file:line at the pinned blob);
**I** = inference (class membership is inference by the matrix's own U6/§10 rule); **U** =
unknown.

## 1. Source record

| field | value |
|---|---|
| URL | https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ |
| access date | 2026-10-20 (HTTP `date: Tue, 20 Oct 2026 13:25:23 GMT`) |
| HTTP | `HTTP/2 200`, `content-type: text/html; charset=utf-8`, `server: cloudflare`, `x-proxy-cache: MISS`, `last-modified: Mon, 19 Oct 2026 18:02:59 GMT` |
| revision | Docusaurus build **v3.10.2** (`meta-generator`), `docsearch:version=current`, `docusaurus_version=current`; **no commit SHA / no version number is exposed** — the page footer's `lastUpdated` div is empty (`<div class="col lastUpdated_Knpw"></div>`) |
| anchor | §Equality Operator (primary), with §Support and §Conditional Expression, §String Literal, §Boolean Literal, §Regex, §Block Statement, §Array Declaration, §Method Expression, §Logical Operator, §Object literal, §Unary Operator, §Update Operator |
| quote (≤25 words) | "We've aligned on a standard naming scheme so it is easy to switch and compare implementations." |
| quote location | §Supported mutators, opening paragraph, sentence 2 (immediately before §Support); 16 words |

Quote verification (O):
`curl -sS <url> -o page.html` then `grep -c 'aligned on a standard naming scheme' page.html`
→ `2` (the sentence is byte-identical in the `meta-og:description` and in the rendered body;
`grep -o 'aligned on a standard naming scheme[^<]*'` → `…so it is easy to switch and compare
implementations. The difference in support is listed below.`). The sentence grounds choosing
operator classes **by standard name** rather than by ad-hoc edits; the per-class tables below
supply the single-edit shape for each name.

## 2. What the page says (O, extracted from the fetched HTML)

Section §Support is a 16-row × 3-language table. Extracted programmatically from the raw
HTML (`python3` regex over `<tr><td><a href=#…>` rows), StrykerJS column:

| class | StrykerJS | .NET | 4s |
|---|---|---|---|
| Arithmetic Operator | ✅ | ✅ | ❌ |
| Array Declaration | ✅ | ✅ | ❌ |
| Assignment Expression | **❌** | ✅ | n/a |
| Block Statement | ✅ | ✅ | ❌ |
| Boolean Literal | ✅ | ✅ | ✅ |
| Checked Statement | n/a | ✅ | n/a |
| Conditional Expression | ✅ | ✅ | ✅ |
| Equality Operator | ✅ | ✅ | ✅ |
| Logical Operator | ✅ | ✅ | ✅ |
| Method Expression | ✅ | ✅ | ✅ |
| Object literal | ✅ | ✅ | n/a |
| Optional chaining | ✅ | ❌ | n/a |
| Regex | ✅ | ✅ | ✅ |
| String Literal | ✅ | ✅ | ✅ |
| Unary Operator | ✅ | ✅ | ❌ |
| Update Operator | ✅ | ✅ | n/a |

**14 of 16 classes are StrykerJS-supported**; `Assignment Expression` is explicitly **❌ for
StrykerJS** and `Checked Statement` is `n/a`. Single-edit shapes (exact rows, quoted):

- §Equality Operator: `GreaterThanEqualBoundary` — `a >= b` → `a > b`; `StrictEqualityNegation` — `a === b` → `a !== b`.
- §Conditional Expression: `GreaterThanToTrue` — `if (a > b) { }` → `if (true) { }`; `GreaterThanToFalse` — `if (a > b) { }` → `if (false) { }`.
- §String Literal: `FilledStringToEmpty` — `"foo"` → `""`; `EmptyStringToFilled` — `""` → `"Stryker was here!"`.
- §Boolean Literal: `TrueNegation` — `true` → `false`; `FalseNegation` — `false` → `true`; `NotRemoval` — `!(a == b)` → `a == b`.
- §Logical Operator: `AndNegation` — `a && b` → `a || b`; `OrNegation` — `a || b` → `a && b`.
- §Regex: `^abc` → `abc` (anchor removal), `\d` → `\D`, `[abc]` → `[^abc]`, `a{1,3}` → `a`.
- §Block Statement: `BlockRemoval` removes the content of every block statement.
- §Array Declaration: `ArrayLiteralItemsRemoval` — `[1, 2, 3, 4]` → `[ ]`.
- §Object literal: `ObjectPropertiesRemoval` — `{ foo: 'bar' }` → `{ }`.
- §Method Expression (StrykerJS): `StartsWithToEndsWith`, `TrimToTrimEnd`, `SortRemoval`, `ContainsRemoval`-family (`includes`), `SliceRemoval`, `FilterRemoval`.
- §Unary Operator: `MinusNegation` — `-a` → `+a`. §Update Operator: `PostfixIncrementNegation` — `a++` → `a--`.

## 3. Artifact under mutation (O) — the targets each class can move

Pinned blob, read from a scratch copy: `git -C kumitate-shokunin show
364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > /tmp/…/round-gate.mjs`;
`sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` (matches C1's
blob sha and matrix §13.10 #1); `wc -l` → `1511` (matches §13.10 #1). The file at kumitate
HEAD `1770305f` and at `364f1d5` is the same blob; `git status --porcelain` printed no lines
(tree clean), so the working-tree read is the same bytes.

Lexical operator census on the pinned blob (O; `grep -oF … | wc -l`, lexical not semantic):

| token | count | token | count | token | count |
|---|---|---|---|---|---|
| `===` | 192 | `!==` | 35 | `&&` | 180 |
| `\|\|` | 10 | `??` | 55 | `?.` | **0** |
| `<=` | 1 | `>=` | 4 | `+=` | 1 |
| `++` | 5 | `%` | 4 | `new Array(` | **0** |
| `if (` | 80 | `for (` | 14 | `?` (all) | 165 |

Named targets used in the mapping below (O, `file:line` at the pin):

- `:140` `const CONTRACT = 'kumitate-round-gate-v1';`
- `:171-176` `const FINDING_KINDS = [ … 14 kinds … ];` — referenced **only** at `:1488`.
- `:218` `if (statKind(repo) !== 'dir') return false;`
- `:238-241` option defaults `close:false, tracked:false, json:false, strict:false`
- `:246` `if (v.startsWith('--')) throw …` (flag-like dir value; §13.6 #4)
- `:249` `for (let i = 0; i < argv.length; i++) {`
- `:277-279` env-lane guard `envLane !== undefined && !/^[A-Za-z][A-Za-z0-9-]*$/.test(envLane)` (§13.6 #4)
- `:345` `add('REPORT_THIN', 'error', bytes >= REPORT_MIN_BYTES, …)` (bytes floor, `:167` = 1024)
- `:346` `report.match(/^#{1,3} /gm)` (headings count)
- `:347` `add('REPORT_HEADINGS', 'error', headings >= 2, …)`
- `:476` `if (rel.startsWith('..') || isAbsolute(rel)) {`
- `:487-488` `token: 'UPSTREAM_MISSING'` (main-repo site; §13.6 #3)
- `:512` `/^round-(\d+)$/`
- `:527` `return failClosed(opts, 'tracked', 'REPORTS_DIR_MISSING', …` (tracked site; §13.6 #2)
- `:535` `if (filed.length < 2) {`
- `:683` `return failClosed(opts, mode, 'INTERNAL_ERROR', …` (zero fixtures; §13.3/§13.6 #1)
- `:730` `seq += 1;` (the only `+=`)
- `:863` `const m = /^ROUND_GATE: (CLEAN|DRIFT) \(round=(\d+) lane=(\S+) checks=(\d+) errors=(\d+) warnings=(\d+)\)$/u.exec(line);`
- `:1487-1493` meta-check; its equality is at **`:1490`** `ok: missing.length === 0,`

## 4. Mapping: StrykerJS class → arm class A–E (I; class membership is a reading)

Rows A–E are the matrix's `## 2`–`## 6` surfaces: A verdict paths, B fail-closed arms,
C counts, D reported-but-unasserted, E unreached arms. **G** is the matrix's added
behavior-predicate row; where a Stryker class can only move a predicate, G is named and no
A–E row is claimed (the matrix's own ledger does the same for 6 of its 20 mutants).

| # | StrykerJS class | Primary A–E row | Also | Concrete single-edit at the pin | Channel (why that row) |
|---|---|---|---|---|---|
| 1 | Equality Operator | **C** | G | `:345` `bytes >= REPORT_MIN_BYTES` → `>`; `:535` `filed.length < 2` → `<=` | Floors/counts: §13.4's `REPORT_MIN_BYTES` interval; kills land on the thin/non-thin fixtures |
| 2 | Conditional Expression | **E** | G, A | `:277` `if (envLane !== undefined && …)` → `if (true)`; `:246` guard → `if (false)` | §13.6 #4 names the env-lane invalid and flag-like `dirValue` branches as fixture-absent → an arm no case reaches |
| 3 | String Literal | **A** | D, E | `'INTERNAL_ERROR'` `:683` → `''`; `'UPSTREAM_MISSING'` `:488` → `''` | A token is the asserted stem of the FAIL-CLOSED verdict (fcA–fcF); the `:683` token has no fixture → also E |
| 4 | Boolean Literal | **B** | E, G | `:635` `if (opts.selftest) return selfTest();`; defaults `:238-241` `false`→`true` | Fail-closed/flag arms; defaults are read only after `--selftest` short-circuits → default flips are E-shaped |
| 5 | Logical Operator | **B** | G | `:277` `&&`→`\|\|`; `:476` `\|\|`→`&&` | Compounding a fail-closed guard changes which refusal fires; `:476`'s path-escape check guards report-path bookkeeping |
| 6 | Array Declaration | **C** | D | `:171` `FINDING_KINDS` → `[]` | Collection emptied: the meta-check's one-sided `missing.length === 0` (`:1490`) cannot notice; `observed.size` is detail-only (§13.4) |
| 7 | Block Statement | **E** | D | `BlockRemoval` on an `add(...)`/message block (e.g. `:401-404`, `:425-428`) | Dropped arm, the matrix's canonical E-shape; the meta-check only catches deleted *enum* emissions, not detail lines |
| 8 | Object literal | **D** | A | `ObjectPropertiesRemoval` on the JSON object (`:1252-1257` key-set) vs a text-only object | Top-level key set is equality-pinned → kill; nested `citations.*` fields are read by no check (§13.5 #4) → D |
| 9 | Regex | **A** | G, E | `:863` drop `$` / drop `^`; `:863` `\d`→`\D`; `:346` `^#{1,3} ` → `#{1,3} ` | A: the verdict line is the asserted stem, full-line anchored; parse accepts trailing junk only if a fixture emits it |
| 10 | Method Expression | **E** | D, G | `:246` `v.startsWith('--')` → `endsWith('--')`; `:518` `out.sort(…)` removal | `:246` guards a §13.6-named uncovered branch; slice/sort edits touch displayed-but-unread lists (D) |
| 11 | Arithmetic Operator | **C** | G | `%` sites (4 lexical) and numeric formatting | Exact-count pins (§13.4) are the count reader; most arithmetic edits elsewhere are equivalence-prone |
| 12 | Update Operator | **C** | — | `:249` `i++` → `i--` | Counter edit, but **non-terminating**: pre-register as timeout/unknown, not kill (see R5) |
| 13 | Unary Operator | **C** | — | `-a` → `+a` at any signed numeric (rare; no `-`-heavy arithmetic block) | Likely **inapplicable**, not equivalent-by-measurement: no probe moves a fixture |
| 14 | Optional chaining | **none** | — | `?.` count = **0** at the pin | Class cannot be instantiated on this artifact; selecting it would be an unapplied mutant, not a row test |

Not mapped: **Assignment Expression** (StrykerJS ❌ per §Support; the artifact's single `+=`
at `:730` would be a hand-cut operator, not a Stryker class) and **Checked Statement**
(`n/a` outside .NET).

Coverage of the named example classes from the assignment: equality → C (§4 #1),
conditional → E (#2), string-literal → A (#3), boolean → B (#4). So the four example classes
land on four *different* rows — A, B, C, E — while Block/Array/Method contribute to E, C and D.
The taxonomy therefore spans the whole matrix, which is the craft point for a 10-mutant sweep.

## 5. Candidate pre-registrations (I, **not run**; each with a falsifier)

These are offered as pre-registration material for L1's sweep. Every line is a projection
from a static read; none is a measurement.

| id | Stryker class | edit | predicted verdict | falsifier |
|---|---|---|---|---|
| P1 | Equality (boundary) | `:345` `>=`→`>` | **survive** (C): no fixture sits at exactly 1024 B (§13.4 fixtures 25 B and 1059 B) | any fixture with `bytes=1024` |
| P2 | Array Declaration | `:171` enum → `[]` | **survive** (C): meta-check `:1490` is one-sided; nothing else reads the enum | a check comparing `FINDING_KINDS` length/order |
| P3 | Regex (anchor) | `:863` remove `$` | **survive** (A): `verdictLine` trims and takes the last line; no fixture appends text | a fixture whose stdout has trailing text after the verdict |
| P4 | Regex (class) | `:863` `\d`→`\D` | **killed** (A): every verdict fixture fails to parse | a fixture that never parses a verdict |
| P5 | String Literal | `:683` `'INTERNAL_ERROR'`→`''` | **survive** (E): no fixture reaches the catch-all | any fixture forcing an internal throw |
| P6 | Conditional | `:277` guard → `if (true)` | **survive** (E): invalid env lane never exercised (§13.6 #4) | a fixture setting an invalid `KUMITATE_LANE` |
| P7 | Method Expression | `:246` `startsWith('--')`→`endsWith('--')` | **survive** (E): flag-like dir value has no fixture (§13.6 #4) | a fixture passing `--repo --json` |
| P8 | Boolean | `:238` `close:false`→`true` | **survive** (E): selftest returns at `:635` before `close` is read | a fixture running close mode without `--selftest` |
| P9 | Update | `:249` `i++`→`i--` | **timeout**, not kill (C) | any bounded termination |

## 6. SOURCES.md row draft (L1 owns the file; do not edit from this seat)

11 columns matching `corpus/SOURCES.md` header (`id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by`). Next free id is **S052** (max seen `S051`).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S052 | Supported mutators (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ | docs | A | StrykerJS's named single-edit operator classes and per-language support — the vocabulary a JS mutant set is chosen from | §Supported mutators opening paragraph, §Support table, and §Equality Operator / §Conditional Expression / §String Literal / §Boolean Literal / §Regex / §Block Statement / §Array Declaration / §Method Expression / §Object literal @ page fetched 2026-10-20; Docusaurus v3.10.2, docsearch version=current, last-modified 2026-10-19, no commit pin exposed | 16 operator families with exact original→mutated single edits; StrykerJS supports 14 and is explicit that Assignment Expression is ❌; each family is one textual substitution (equality boundary/negation, conditional true/false, string filled/empty, boolean negation, logical, regex anchors/classes, block/array/object removal, method-expression, update) — the stated basis for picking single-edit JS mutants and for naming them consistently | mined | 2026-10-20 | 180d | .ufo/waves/round-16/w1/RGSource1.md; corpus/knowledge/arm-class-matrix.md §13 (projection predictions; this row is the operator vocabulary behind them) |

Notes on the row (honesty):
- `tier: A` mirrors S001 (same publisher, same docs surface, first-party operator definitions). The page states **no StrykerJS version** — `180d` recheck, not `on-release`, because no release marker is exposed to key off.
- `status: mined` because this round reads it to choose operators (row is a claim opened in the round that writes it, per the file's own registry preamble).
- The artifact row for `round-gate.mjs` is **not** in the registry today (grep for `round-gate` in `corpus/SOURCES.md` → no rows). If L1 wants the C1 leg fully sourced, a companion row in S032/S033's shape (`kumitate-shokunin/scripts/round-gate.mjs @ 364f1d5…, blob sha256 f890e277…`) would be S053; that is L1's call — not drafted here because it is a different source (artifact, not docs) and my Target names only the Stryker row.

## 7. Bounded recommendations

- **R1 (coverage).** Pick the 10 mutants so rows A–E each get ≥1 and the four named example classes are not all aliased into one row: the mapping above sends equality→C, conditional→E, string-literal→A, boolean→B, and Block/Array/Method→E/C/D. Two row-E mutants are justified because §13.6 lists five arm species.
- **R2 (citation precision).** When pre-registering from matrix §13, cite the **range** `:1487-1493`; the meta-check equality is at **`:1490`**, not `:1489` as §13.4 writes. (O: `sed -n '1490p'` → `ok: missing.length === 0,`.)
- **R3 (vocabulary honesty).** Do not describe an `Assignment Expression` edit as Stryker-grounded: the page marks it ❌ for StrykerJS. The single `+=` at `:730` is hand-cut if used.
- **R4 (inapplicable ≠ equivalent).** `Optional chaining` (`?.`=0) and `Unary Operator` have no target in this artifact. Record them as *not instantiated*, not as survivors — an unapplied mutant is not a row test (the matrix already distinguishes this from the "unreached arm" species in §6).
- **R5 (timeout pre-registration).** The Update-operator edit on `:249` cannot terminate; its expectation must be `timeout/unknown`, so the harness does not book a hang as a kill.
- **R6 (ledger naming).** Use the Stryker operator name in each `@defect` description (e.g. `GreaterThanEqualBoundary`, `ArrayLiteralItemsRemoval`) so the class→row mapping in the round's note is machine-checkable against §4.

## 8. Evidence log (O)

Scratch: `/tmp/tameshi-r16-RGSource1-O2Dq/` (`mktemp -d`). No lane file written except this
report; sibling repo untouched (reads only; `git status --porcelain` empty).

| # | command (abridged) | exit | key line |
|---|---|---|---|
| 1 | `curl -sSI https://…/supported-mutators/` | 0 | `HTTP/2 200`, `last-modified: Mon, 19 Oct 2026 18:02:59 GMT`, `date: Tue, 20 Oct 2026 13:25:23 GMT` |
| 2 | `grep -c 'aligned on a standard naming scheme' page.html` | 0 | `2` |
| 3 | `python3` extract of §Support rows | 0 | 16 rows; `Assignment Expression … JS=❌`; `Checked Statement JS=n/a` |
| 4 | `git -C kumitate-shokunin show 364f1d5…:scripts/round-gate.mjs > /tmp/…`; `sha256sum` | 0 | `f890e277…a834d3e9` |
| 5 | `wc -l /tmp/…/round-gate.mjs` | 0 | `1511` |
| 6 | `git -C kumitate-shokunin rev-parse HEAD`; `git status --porcelain` | 0 | `1770305f…`; no output (clean) |
| 7 | operator census (`grep -oF … \| wc -l`) | 0 | `?.`=0, `new Array(`=0, `+=`=1, `===`=192, `&&`=180, `if (`=80 |
| 8 | `sed -n` at `:140,:167,:218,:238-241,:246,:249,:277-279,:345,:346,:347,:488,:527,:635,:683,:730,:863,:1487-1493,:1253-1257` | 0 | the lines quoted in §3 |
| 9 | `grep -n 'FINDING_KINDS'` | 0 | `:171` (definition), `:1488` (only use) |
| 10 | `sed -n '1490p'` | 0 | `ok: missing.length === 0,` |

## 9. Unknowns

- **U1.** The page exposes no StrykerJS version and no commit pin; the `180d` recheck is a
  freshness policy, not a version key. The support cells could change under a docs edit
  without any version signal.
- **U2.** Operator-class membership in A–E is (I) by §10/U6 rule; borderline cells exist
  (equality boundary sits on the counts/predicate seam, method-expression on the
  predicate/report seam). A different reader could move #1 or #10.
- **U3.** All predicted verdicts in §5 are static projections; none is measured this round.
  The falsifiers are exact and should be attached to the pre-registration so a disagreement
  is the finding, not an erratum.
- **U4.** The lexical census counts `>` 176 including `=>`; arithmetic/update counts are
  lexical, not semantic — "# of possible mutants" is not estimated here.
- **U5.** Whether §13's `:1489` was a transcription slip or a different byte revision is
  unknown; the blob sha is identical, so the line is `:1490` at the pinned bytes.
