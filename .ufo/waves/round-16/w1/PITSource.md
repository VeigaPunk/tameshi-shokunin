# PITSource — round 16 wave 1 (C1 secondary source: PIT mutation operators)

Seat: TameshiR16.PITSource (leaf, no delegation). Lane: tameshi-shokunin. Date: 2026-10-20.
Scope: open https://pitest.org/quickstart/mutators/, record the source, draft a SOURCES row, judge what PIT's Java operators do or do not transfer to a JS gate. No SOURCES.md edit, no mutant run, no selftest run, no commit.

## 1. Access record (observed)

| Field | Value | Evidence |
|---|---|---|
| URL | https://pitest.org/quickstart/mutators/ | distinct from the registered incremental-analysis URL (`pitest.org/quickstart/incremental_analysis/`, rows S041/S047/S048 in `corpus/SOURCES.md`) |
| Access (UTC) | 2026-10-20T13:24:57Z | `date -u`, same shell as curl |
| Method | `curl -fsSL -o mutators.html <url>` → exit 0, 67,033 B | `/tmp/tameshi-r16-PITSource-1MzY/mutators.html` |
| sha256 (fetched HTML bytes) | `a31331daf89f246f3e02c0da92578d4ad2163c53741c3700437e75b9a1602da2` | `sha256sum mutators.html` |
| Reader cross-check | `read` of the same URL returned the page's markdown source (frontmatter title "Mutation operators", "Improve this page" link to `hcoles/pitest-site` `quickstart/mutators.markdown`); quote text below matches both renderings | reader output |
| Page version | not stated on the page (same as the incremental-analysis row) | page text |

Quote-presence checks on the fetched bytes (`grep -c`, all = 1):
- `The conditionals boundary mutator replaces the relational operators` → HTML line 317.
- `replace non-<code ...>null</code> return values` → HTML line 628 (Return Values table, `Object` row).
- `Replaces primitive and boxed boolean return values with false.` → HTML line 714 (`FALSE_RETURNS`).
- `less <strong>stable</strong> i.e these` → HTML line 588 (`NEGATE_CONDITIONALS` closing paragraph; markdown source wording "less **stable** i.e these").

Anchors on the page (HTML `id=`, verified by grep): `CONDITIONALS_BOUNDARY` (h2 line 313), `NEGATE_CONDITIONALS` (h2 532), `RETURN_VALS` (h2 593, marked superseded), `EMPTY_RETURNS` (686), `FALSE_RETURNS` (710), `TRUE_RETURNS` (720), `NULL_RETURNS` (730), `PRIMITIVE_RETURNS` (740), `REMOVE_CONDITIONALS` (966).

Pin check for C1 (observed, not a mutant run): `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs` → exit 0, 1511 lines, sha256 `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`, matching the pinned blob. Materialized to `/tmp/tameshi-r16-PITSource-hnne/round-gate.mjs`. The hermetic selftest was not run here (pre-registration precedes any sweep; L1 owns it).

## 2. Quotes for the row (plain text; HTML `<code>` markup removed, backticks as in the source)

Q1 — CONDITIONALS_BOUNDARY, location: #CONDITIONALS_BOUNDARY, HTML line 317 (markdown "Conditionals Boundary Mutator" section, reader line 73). 21 words:
> The conditionals boundary mutator replaces the relational operators `<, <=, >, >=` with their boundary counterpart as per the table below.

Q2 — NEGATE_CONDITIONALS stability caveat, location: #NEGATE_CONDITIONALS, HTML line 588. 16 words:
> but is less stable i.e these mutations are generally easier for a test suite to detect.

Q3 — RETURN_VALS, Object row, location: #RETURN_VALS table, HTML line 628. 17 words:
> replace non-`null` return values with `null` and throw a `java.lang.RuntimeException` if the unmutated method would return `null`

Q4 — FALSE_RETURNS, location: #FALSE_RETURNS, HTML line 714. 10 words:
> Replaces primitive and boxed boolean return values with false.

Q5 — RETURN_VALS status, location: #RETURN_VALS, HTML line 593 section body. 11 words:
> This mutator has been superseded by the new returns mutator set.

Q6 — PIT's equivalence filter for returns, location: #FALSE_RETURNS and #NULL_RETURNS bodies (HTML 710–740). 16 words:
> Pitest will filter out equivalent mutations to methods that are already hard coded to return false.

Q7 — PIT's rationale for keeping REMOVE_CONDITIONALS out of defaults, location: #REMOVE_CONDITIONALS body (HTML 966+). 25 words; a prefix of a longer sentence that continues "and those required to kill mutations from other default operators":
> The reason these are not enabled by default is that there is a large degree of overlap in the tests required to kill these mutations

Default-group membership (page table at top, verified in reader rendering): CONDITIONALS_BOUNDARY, NEGATE_CONDITIONALS, MATH, INCREMENTS, INVERT_NEGS, VOID_METHOD_CALLS are in DEFAULTS; FALSE/TRUE/NULL/EMPTY/PRIMITIVE returns in DEFAULTS; RETURN_VALS only in OLD_DEFAULTS; REMOVE_CONDITIONALS in none of the default groups (STRONGER only for EQUAL_ELSE).

## 3. Draft SOURCES row (NOT written to corpus/SOURCES.md; lane owner to fold in)

Note: the lane's registry is `tameshi-shokunin/corpus/SOURCES.md` (no root-level SOURCES.md exists in the lane). Last id is S051, so the next id here is S052. Draft row in the registry's 11-column shape:

```
| S052 | Mutation operators (PIT docs) — https://pitest.org/quickstart/mutators/ | docs | A | PIT's own operator definitions for Java bytecode mutation; evidence that the default operators are stable, not a JS operator catalogue | §CONDITIONALS_BOUNDARY, §NEGATE_CONDITIONALS (closing paragraph), §RETURN_VALS (superseded note, Object row), §FALSE_RETURNS, §REMOVE_CONDITIONALS; page as accessed 2026-10-20T13:24:57Z UTC, version unstated, sha256 a31331daf89f246f3e02c0da92578d4ad2163c53741c3700437e75b9a1602da2 (67,033 B HTML) | PIT states the conditionals-boundary operator is active by default and that negate-conditionals is less stable (easier to detect); the stability is PIT-author assertion on Java bytecode, not measured on any JS gate | queued | 2026-10-20 | 90d | — |
```

Status is `queued` (not `mined`) because no lane artifact cites it yet; the lane owner promotes it to `mined` when a pre-registration or ledger line uses it. Recheck 90d mirrors S041/S047 (same docs site, same cadence); the recheck command would be `curl -fsSL https://pitest.org/quickstart/mutators/ | sha256sum` and a comparison against the sha256 above (drift = 0 is the registry test).

## 4. Transfer analysis: PIT operators → the JS gate (`mutate-and-run.sh` + round-gate.mjs)

Hard constraints on the JS side (observed):
- `tools/mutate-and-run.sh` mutants are exact-text edits; `@old` must occur exactly once in the pinned blob (`mutate-and-run.sh:48` "The old string must occur exactly once (asserted before any suite run)"; `:63` "count==1 — any failure exits 2 before a single suite run").
- PIT operates on compiled bytecode and says so: "Mutations are performed on the byte code generated by the compiler rather than on the source files… it can sometimes be difficult to simply describe how the mutation operators map to equivalent changes to a Java source file." (PIT mutators page, Overview.) A JS gate has no bytecode stage; every operator must be re-expressed as a source-text edit.

Transfers (source-text expressible, no type information needed):
- CONDITIONALS_BOUNDARY (`<`↔`<=`, `>`↔`>=`): textual in JS. round-gate.mjs code sites (comment/arrow lines excluded, `grep -nP`): 249 `i < argv.length`; 307 `i < lines.length`; 310 `i < lines.length`; 345 `bytes >= REPORT_MIN_BYTES`; 347 `headings >= 2`; 535 `filed.length < 2`. Lines 307 and 310 share the text `i < lines.length` (count 2), so a spec must add context to make @old unique.
- NEGATE_CONDITIONALS: JS analogue is `===`↔`!==` (and relational flips). round-gate.mjs has 0 loose `==` code sites (`grep -P "(?<![=!])==(?!=)"` → 0) and strict `===`/`!==` throughout. PIT's own page calls this operator less stable; for this gate treat it as a control, not a default.
- TRUE/FALSE_RETURNS: boolean flip transfers directly. round-gate.mjs line 218 `if (statKind(repo) !== 'dir') return false;` is the only `return true|false` site in the file (`grep -c` = 1).
- NULL_RETURNS: transfers as text (`return readFileSync(p, 'utf8');` → `return null;`, line 203 region), but PIT's exclusion rule ("Methods that can be mutated by the EMPTY_RETURNS mutator or that are directly annotated with NotNull will not be mutated") has no JS analogue; the equivalence filter ("already hard coded to return null") also needs a per-site judgment.

Does not transfer (or transfers only with type information the gate lacks):
- INCREMENTS / REMOVE_INCREMENTS (`iinc` is a JVM local-variable opcode) — no JS counterpart.
- INVERT_NEGS (JVM primitive negation) and PRIMITIVE_RETURNS (int/long/float/double families) — JS has one number type.
- EMPTY_RETURNS (type-specific empties: `String`→`""`, `Optional`, `List`→`emptyList()`, `Set`) — requires static types JS does not carry.
- MATH: PIT's `+`→`-` etc. is well-typed for Java primitives; JS `+` is also string concatenation, so a textual swap can produce a different runtime error rather than a semantic mutant. Needs per-site type reading; not single-edit clean.
- VOID_METHOD_CALLS / NON_VOID_METHOD_CALLS / CONSTRUCTOR_CALLS — implemented in PIT on invoke bytecode; the JS analogue is removing a statement or replacing a call expression per site, which is an AST-level edit (`xd://ast_edit` territory), not a `@old`/`@new` text edit.
- REMOVE_CONDITIONALS — text-expressible (`if (X) {` → `if (true) {`), but PIT itself excludes it from defaults because its kill tests overlap the boundary operator's. Recommendation below: do not add it to the default JS set.
- INLINE_CONSTS / CRCR / AOR / AOD / ROR / UOI / OBBN (EXPERIMENTAL group) — Java-typed or bytecode-shaped; out of scope for a single-edit JS gate.

## 5. Candidate single-edit defects (identified and count-checked only; NOT run; NOT predictions)

Each @old below was counted against the pinned blob `f890e277…` (`grep -cF`, result = 1 unless noted). Run prediction pre-registration remains L1's job.

| Candidate | Operator class (PIT anchor) | @old (exact, count) | Proposed @new | round-gate.mjs line |
|---|---|---|---|---|
| K1 | CONDITIONALS_BOUNDARY | `bytes >= REPORT_MIN_BYTES` (1) | `bytes > REPORT_MIN_BYTES` | 345 |
| K2 | CONDITIONALS_BOUNDARY | `headings >= 2` (1) | `headings > 2` | 347 |
| K3 | CONDITIONALS_BOUNDARY | `filed.length < 2` (1) | `filed.length <= 2` | 535 |
| K4 | TRUE/FALSE_RETURNS (boolean flip) | `if (statKind(repo) !== 'dir') return false;` (1) | `if (statKind(repo) !== 'dir') return true;` | 218 |
| K5 | NEGATE_CONDITIONALS (control) | `return r.status === 0 && String` (1) | `return r.status !== 0 && String` | 220 region |

Non-candidate: the `catch { return null; }` at line 203 already returns null on the error branch; a PIT-style NULL_RETURNS flip there is a no-op on that path and would need the success branch instead.

[INFERENCE] K1 and K2 are the most informative boundary edits for a gate whose selftest exercises exact-size and exact-count thresholds (1024-byte REPORT_THIN and the >=2 filed-report floor); whether the suite pins those exact boundaries was not observed here and must be measured by L1.

## 6. Recommendations (bounded)

1. Fold S052 (section 3) into `corpus/SOURCES.md` at lane review; do not edit it from this seat.
2. Cite S052 for the claim "boundary is the PIT default-stable operator" only as PIT's assertion about Java bytecode; any JS claim needs the measured sweep.
3. For the seventh-leg predictions, choose from the transferable set only: boundary (K1–K3), boolean flip (K4), and optionally one negation control (K5). Exclude MATH, EMPTY/PRIMITIVE/NULL-by-type, and the call-removal operators: they do not express as exact-text single edits without type or AST knowledge.
4. Do not default-enable REMOVE_CONDITIONALS in the JS set (PIT's own overlap rationale, Q7).
5. If the lane wants a PIT-named operator catalogue for JS, it needs its own registry row per operator class with a transfer verdict, not a claim that PIT's list carries over.

## 7. Tools

None installed. Used existing `curl`, `sha256sum`, `git`, `grep`, `date`.

## 8. Opened paths (for the no-contamination record)

- https://pitest.org/quickstart/mutators/ (via `read`, and `curl` to `/tmp/tameshi-r16-PITSource-1MzY/mutators.html`)
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin` object `364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs` (read-only `git show` to `/tmp/tameshi-r16-PITSource-hnne/round-gate.mjs`)
- `tameshi-shokunin/corpus/SOURCES.md` (rows S041, S047, S048, S051; header and registry shape)
- `tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md` (grep only, line 1–5, for the registered PIT URL)
- `tameshi-shokunin/tools/mutate-and-run.sh` (lines 1–40 read; grep for uniqueness rule, lines 26, 48, 63)
- `tameshi-shokunin/corpus/knowledge/arm-class-matrix.md` (lines 1–300 read, incidental; no content used beyond the matrix shape, not cited in the findings)
- grep-only incidental hits in `.ufo/evidence/round-15/*.json` (SOURCES stdout echo), `.ufo/reports/round-12/SOURCES.md` (name only, not opened)

No file was written except this report. No mutant was run against round-gate.mjs. No commit, no git add, no edit to SKILL.md/SCORECARD.md/LOG.md/SHONEN.md/PROVINCE.md/QUALITY.md/SOURCES.md/README.md.

## 9. Findings summary

- PIT mutators page fetched 2026-10-20T13:24:57Z; sha256 recorded; four quotes verified present in the fetched bytes; anchors verified.
- C1 pin verified: round-gate.mjs at 364f1d5 has blob sha256 f890e277… (matches the claim).
- PIT's Java operators transfer to a JS gate only for boundary (`<`/`>` family), boolean-return flip, and equality-pair negation; the remaining default operators depend on bytecode, static types, or AST-level call edits, and do not fit single-edit exact-text mutants.
- Five count-checked candidate defects (K1–K5) identified for the lane's prediction step; none was run.
- Verdict on the source: usable as a secondary, docs-tier source for operator *definitions* and PIT's own stability and default-set claims; not usable as evidence that any operator is stable on a JS suite.
