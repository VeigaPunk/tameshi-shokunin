# OpenStrykerMutators — C1 sourced claim: the ten round-26 defects against Stryker's mutator classes

Seat: TameshiR26.OpenStrykerMutators (leaf, no subagents). Date 2026-10-22.
Question: map each of the ten pre-registered `cite-check.mjs` defects to the closest
Stryker mutator class (or "no Stryker mutator"), and say which survivors Stryker's
default mutators would also generate.

## Verdict

**Class level: 7 of the 10 defects mutate a node whose form a named Stryker class owns;
3 have no Stryker mutator at all** (`S_OOR_EDGE`, `S_STRICT`, `S_USAGE`, whose edited
tokens are an identifier-to-`n+1` insertion and two numeric literals — the page has no
numeric-literal category). **Transformation level: 0 of 10.** No edit in the ten defects
is one the documented StrykerJS operator set produces — the spec uses word-to-word string
replacement, quantifier-bound rewrite, conjunct deletion, `n+1` insertion and
`startsWith`→`includes`, none of which appear in the operator table I opened.

**Survivors Stryker would also generate: 4.** Hand-translating the nearest documented
operator at each surviving defect's site, then running the hermetic suite, gives four
survivors (62/62, exit 0): the strict-mode boundary `warn > 0`→`>= 0` (mirrors
`S_STRICT`), the verdict guard `filesScanned > 0`→`>= 0` (equivalent to `S_EMPTY_GUARD`),
the mirror guard `resolved > 0`→`>= 0` (a hole the pre-registered table does **not**
list), and `digest.startsWith`→`digest.endsWith` (adjacent to `S_PIN_INCLUDES`).
`S_OOR_EDGE`'s Stryker neighbour is **killed** (61/62) — Stryker's `>`→`>=` at that
comparison dies on a last-line citation, so the hand-picked `n+1` shift reaches a hole
no documented Stryker operator reaches. `S_USAGE` has no Stryker neighbour to probe.

So: the spec is Stryker-*class*-shaped at 7 of 10 sites but Stryker-*operator*-shaped at
none; of the five recorded survivors, three have Stryker-reachable survivor neighbours,
one does not, and one cannot be expressed in Stryker's operator set.
These 14 runs are **out-of-sweep probes**, not a mutation score and not part of the
frozen table: `.ufo/evidence/round-26/cite-check/sweep/results.tsv` (5 killed / 5
survived) is untouched and remains the leg-9 record.

## Sources opened this session (2026-10-22)

| ID | URL | Sections used |
|---|---|---|
| S052 (already registered at `corpus/SOURCES.md:61`) | https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ | §Support, §String Literal, §Equality Operator, §Logical Operator, §Conditional Expression, §Regex, §Method Expression → StrykerJS, §Object literal, §Boolean Literal; full page read (387 lines), no numeric-literal category exists |
| new, unregistered | https://stryker-mutator.io/docs/stryker-js/configuration/ | §Configuration Options → `mutator`, `ignoreStatic` (full page read, 704 lines) |

Both pages are Docusaurus builds with no commit pin (S052 already records this for the
first). Quotes below are verbatim from that reading, each ≤25 words.

Default-set evidence: the configuration page documents `mutator` as "Default: `{}`" and
states "Stryker now supports mutating of JavaScript and friend files out of the box,
without the need for a mutator plugin" (§`mutator`). No enabled-mutator list is
documented; `excludedMutations` is the only documented narrowing. **Inference, labelled
as such:** with the default config, the active set is the StrykerJS column of the
§Support table (14 of the 16 categories marked ✅; Assignment Expression ❌, Checked
Statement n/a).

## Mapping (pin = kumitate rev 1205c662…, blob sha256 40573448…c10c9f, 2537 lines)

Site line numbers are the pinned bytes, verified this session (`git -C
kumitate-shokunin show <rev>:scripts/cite-check.mjs` → 2537 lines, sha256
`40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`).

| # | Defect | Site | Closest Stryker class | Exact edit generated? | Nearest documented operator | Probe verdict |
|---|---|---|---|---|---|---|
| 1 | `K_UNRESOLVED_SEV` | `:221` `UNRESOLVED: 'error'`→`'warn'` | **String Literal** (site owner: Object literal `{…}`) | no | `FilledStringToEmpty` → `''` | KILLED 55/62 |
| 2 | `K_PIN_KIND` | `:1127` `kind = 'sha256'`→`'rev'` | **String Literal** | no | `''` | KILLED 61/62 |
| 3 | `K_FENCE_TILDE` | `:471` ``(`{3,}|~{3,})``→``(`{3,}|~{4,})`` | **Regex** | no | quantifier removal → ``(`|~)`` | KILLED 57/62 |
| 4 | `K_MISSING_WORD` | `:2519` `'missing'`→`'absent'` | **String Literal** | no | `''` | KILLED 61/62 |
| 5 | `K_EMPTY_VERDICT` | `:1590` drops two conjuncts | **Logical Operator** (+ Equality Operator at both guards) | no (no deletion operator) | `AndNegation` per occurrence | KILLED (P5a 61/62, P5b 60/62) |
| 6 | `S_OOR_EDGE` | `:1312` `n`→`n + 1` | **no Stryker mutator** (insertion); nearest class Equality Operator | no | `GreaterThanBoundary` `>`→`>=` | KILLED 61/62 |
| 7 | `S_STRICT` | `:1589` `warn > 0`→`> 1` | **no Stryker mutator** (no numeric literal); nearest class Equality Operator | no | `warn >= 0` | **SURVIVED 62/62** |
| 8 | `S_EMPTY_GUARD` | `:1590` drops scanned-files guard | no deletion operator; nearest Equality Operator | no | `filesScanned >= 0` ≡ dropping it | **SURVIVED 62/62** |
| 9 | `S_USAGE` | `:2512` `return 64`→`65` | **no Stryker mutator** | no | none exists | not probed |
| 10 | `S_PIN_INCLUDES` | `:1195` `startsWith`→`includes` | **Method Expression** (StrykerJS) | no | `StartsWithToEndsWith` | **SURVIVED 62/62** |

Class quotes, section names, ≤25 words each:

- §Support: "All Stryker versions support a variety of different mutators. We've aligned
  on a standard naming scheme".
- §String Literal (table): `FilledStringToEmpty | "foo" (filled string) | "" (empty string)`.
  Corroborated in configuration §`ignoreStatic`: "In this example, `'👋'` on line 1 would
  be mutated to an empty string by the StringLiteral mutator." — this is why #1/#2/#4
  (word→word) are *not* generated even though the class owns the site.
- §Object literal: `ObjectPropertiesRemoval | { foo: 'bar' } | { }` — the `SEVERITY`
  object literal whose `UNRESOLVED` entry is at `:221` is a second, coarser class owner
  for #1.
- §Regex: "Regular expressions are parsed and mutated separately." Operator rows are
  anchor removal (`^abc`→`abc`), class negation, escape flips, and quantifier removal
  (`a{1,3}`→`a`); there is **no** quantifier-bound row, so `{3,}`→`{4,}` is out of set.
- §Equality Operator: `GreaterThanBoundary | a > b | a >= b` (also
  `GreaterThanNegation`, `LessThanBoundary`, …).
- §Logical Operator: `AndNegation | a && b | a || b`.
- §Conditional Expression: rows are illustrated on a comparison that *is* the condition
  (`if (a > b)`, `while`, `var x = a > b ? …`). In #5/#6/#8 the comparisons are operands
  of `&&`, not the condition, so whether StrykerJS treats them as condition positions is
  not stated by the page. Either reading leaves my survivor conclusion unchanged:
  comparison→`false` is equivalent to dropping that conjunct (survives, see #8), and
  comparison→`true` is the `>=`-for-a-count case (survives, #7/#8).
- §Method Expression → StrykerJS: `StartsWithToEndsWith | startsWith() | endsWith()`.
  There is no `startsWith`→`includes` row, so #10 is out of set; `endsWith` is the
  nearest and it survives.
- §Boolean Literal: `NotRemoval | !(a == b) | a == b`. Applying it to `!drift` (`:1590`)
  gives `drift` — extra probe P11, KILLED 61/62. (The page illustrates NotRemoval on a
  comparison; `!drift` is a plain identifier, so this is a class-neighbour, not a listed
  transformation.)
- No Stryker mutator for #6/#7/#9: the §Support table's 16 categories contain no
  number/numeric-literal row and no section for one (full page read). `S_USAGE`'s
  `64`→`65` and `S_STRICT`'s `>0`→`>1` and `S_OOR_EDGE`'s `n`→`n+1` are therefore
  outside the taxonomy, not merely outside a supported subset.

## Which survivors Stryker's default mutators would also generate

Nearest-operator mutants, hand-built on fresh copies of the pinned pristine, one edit
each (the `@old` text occurs exactly once; no baseline byte was written):

| Probe | Site in the pinned bytes | Mutation | Suite result |
|---|---|---|---|
| P7 | `:1589` `(opts.strict && totals.warn > 0)` | `> 0` → `>= 0` | **SURVIVED**, 62/62, exit 0 |
| P8 | `:1590` `totals.filesScanned > 0` | `> 0` → `>= 0` | **SURVIVED**, 62/62, exit 0 |
| P9 | `:1590` `totals.resolved > 0` | `> 0` → `>= 0` | **SURVIVED**, 62/62, exit 0 |
| P10 | `:1195` `digest.startsWith(pin.hex)` | `startsWith` → `endsWith` | **SURVIVED**, 62/62, exit 0 |

Why these are true equivalents of the recorded survivor classes:

- **P7 ≡ `S_STRICT`'s hole.** `warn >= 0` is vacuously true, so `--strict` would flag
  drift on any run. No hermetic case passes `--strict`, so nothing observes it. This is
  the same unasserted arm `S_STRICT` already records.
- **P8 ≡ `S_EMPTY_GUARD`.** `filesScanned` is a counter (`:1556` increments it), so
  `filesScanned >= 0` is always true: the conjunct is removed, semantically identical to
  the recorded mutant. That both forms survive is independent corroboration of the
  recorded explanation (the `resolved > 0` guard still fails an empty scan set, `:1626`).
- **P9 is a survivor the pre-registered table does not list.** `resolved >= 0` is also
  vacuously true, i.e. the *mirror* removal — the suite does not require at least one
  resolved citation either. The recorded table tests only the scanned-files guard. This
  is an addition from this probe set, not a correction to the frozen 5/10.
- **P10 survives for a reason that is *not* `S_PIN_INCLUDES`'s.** `includes` and
  `endsWith` are different mutants. `S_PIN_INCLUDES` fails because the mismatch hex is
  not a substring. `endsWith` breaks the sha256 OK arm outright (the fixture's sha256 pin
  is a 10-char prefix, so `digest.endsWith(prefix)` is false and the matching pin grades
  PIN_MISMATCH) — yet the case still passes, because its "match" probe at `:1896`
  accepts `/matches sha256/` **or** `/resolved-by-content/`, and the rev-marked
  12-char pin at the same fixture resolves by content through the unchanged `:1219`
  path. The assertion therefore does not isolate the sha256 OK arm. Whether the sibling
  `ProbeSPININCLUDES` witness for `includes` also separates `endsWith` was not tested
  here.

Killed neighbours, for contrast (same harness): P1 55/62, P2 61/62, P3 57/62, P4 61/62,
P5 60/62, P5a 61/62 (first `&&`→`||` only), P5b 60/62 (second only), P6a 61/62
(`ref.start >= n`), P6b 61/62 (`ref.end >= n`), P11 61/62. **`S_OOR_EDGE` is the
interesting negative:** Stryker's boundary mutant at `:1312` is killed not by the
`:999` fixture but by the symbol case, whose `gate.rs:3` citation is the last line of a
3-line file (`gate.rs` is 3 lines) — with `>=`, that citation grades LINE_OOR and the
"on-line → OK" assertion fails. The suite is defended at the last-line boundary but not
one line past it, which is exactly why the hand-written `n+1` shift survives where
`>=` does not.

## Exact commands and observed output

Pin materialization and pin check (read-only against the sibling repo):

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/citecheck-pin.mjs
$ wc -l /tmp/citecheck-pin.mjs && sha256sum /tmp/citecheck-pin.mjs
2537 /tmp/citecheck-pin.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/citecheck-pin.mjs
```

Harness (scratch: `/tmp/strykerprobe`, 13 mutant copies cut from that one pin, one edit
each applied by the `edit` tool, suite run in `/tmp/strykerprobe/run`; the control is the
unmutated copy):

```
for f in control.mjs P1_… P11_…; do
  out=$(cd run && TMPDIR=/tmp timeout 300 env -i \
        PATH=/run/user/1000/fnm_multishells/3758_1792655796355/bin:/usr/bin:/bin \
        node "/tmp/strykerprobe/$f" --selftest 2>&1)
  rc=$?
done
```

Observed (`awk` over `run/results.tsv`; `results2.tsv` holds P5a/P5b):

```
control                        exit=0  62/62 cases passed (hermetic)
P1_strlit_unresolved_empty     exit=1  FAIL … far[UNRESOLVED/[source]] 55/62 cases passed (hermetic)
P2_strlit_pinkind_empty        exit=1  FAIL content pin match → OK; mismatch → PIN_MISMATCH — match=yes mismatch=no 61/62
P3_regex_quantifier_remove     exit=1  FAIL R28 quote: a «…» inside a fence is never a span … 57/62
P4_strlit_missing_empty        exit=1  FAIL bare run (no --src): both candidates absent … is 61/62
P5_logical_and_to_or           exit=1  FAIL fail-closed: empty scan set — filesScanned=0 verdict=PASS 60/62
P5a_or_first                   exit=1  FAIL bogus-path → UNRESOLVED error 61/62
P5b_or_second                  exit=1  FAIL fail-closed: empty scan set — filesScanned=0 verdict=PASS 60/62
P6a_ge_start                   exit=1  FAIL symbol off-line … online=no 61/62
P6b_ge_end                     exit=1  FAIL symbol off-line … online=no 61/62
P7_ge_warn                     exit=0  62/62 cases passed (hermetic)
P8_ge_scanned                  exit=0  62/62 cases passed (hermetic)
P9_ge_resolved                 exit=0  62/62 cases passed (hermetic)
P10_starts_ends                exit=0  62/62 cases passed (hermetic)
P11_not_removal                exit=1  FAIL bogus-path → UNRESOLVED error 61/62
```

Environment: `node v24.21.0` (pre-existing, fnm multishell), `git` pre-existing; **no
tool was installed or upgraded** for this item. `env -i` carries no PATH, so the node
directory is supplied explicitly — with `env -i` alone `node` is not found (observed:
`bash: line 1: node: command not found`), a detail worth knowing if a later seat
replays this harness.

## Smallest safe correction (recommendation to the L1 integrator; I edited nothing)

Nothing measured needs correcting: the frozen sweep and its 5/10 verdict table are
unchanged, and every prediction-level claim in `predictions.json` is untouched by these
probes. Three wording constraints for whatever cites this:

1. If the round-26 entry cites Stryker for these defects, cite **S052 for class names
   only**. State that no documented StrykerJS operator reproduces any of the ten edits
   (opened 2026-10-22). Do not write "the spec's mutators are Stryker mutators".
2. If it claims Stryker's default mutators would find the same holes, limit the claim to
   the four probed sites and say "nearest documented operator", never "the same mutant".
   `S_OOR_EDGE` is the counter-example to a general claim and is worth one sentence:
   Stryker's boundary operator there is killed, so the `n+1` shift is a hole found *past*
   the standard operator set. If the "beyond fixed operators" framing is reused, it
   belongs to S044 (`corpus/SOURCES.md:53`), not to my mapping.
3. Citing the configuration page (for StringLiteral's empty-string direction or the
   `mutator` default) needs a new registry row first; it is not in `corpus/SOURCES.md`.
   That is the integrator's call, not mine.

## Remaining unknowns

- The supported-mutators page does not enumerate StrykerJS's *default* set; "default =
  the ✅ column" is my labelled inference, not a page claim. `excludedMutations` may
  narrow it in ways the page does not default-document.
- The four "Stryker would generate" mutants are hand transcriptions of the operator
  table, not StrykerJS output; I did not install or run Stryker.
- The page is internally inconsistent in one place (Assignment Expression is ❌ for
  StrykerJS in §Support, while `NullCoalescingAssignmentToAndAssignment` is footnoted
  "Only supported by Stryker-JS"). No round-26 defect touches an assignment operator, so
  the inconsistency does not affect this mapping.
- `ProbeSOOREDGE`, `ProbeSPININCLUDES` and `ProbeSUSAGE` (sibling seats) own the
  off-suite witnesses for three of these survivors; I read only the opening of
  `ProbeSPININCLUDES.md` and make no claim about their findings.
