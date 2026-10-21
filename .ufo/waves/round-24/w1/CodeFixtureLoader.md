# CodeFixtureLoader — round-24 W1 review of the `command-binding.py` two-fixture selftest loader

Seat: TameshiR24-2.CodeFixtureLoader (reviewer, leaf member — no subagent dispatch).
Revision inspected: `c8c5b88c8e961a929cdc351b95a7074c76958909` (delivered); base `6a1821a8897eea6e7d9669292160ec9593669409`.
Scope: `tools/command-binding.py:164-194` (the loader change), `.ufo/evidence/round-24/extra-cases.json` (new fixture),
`.ufo/evidence/round-23/extra-cases.json` (existing fixture), the round-23 38-case receipt, and the registry rows that
depend on the loader's output count.

## Verdict

**The loader change is functionally correct and it closes the routed fixture gap, but it carries six defects — two
material (M1, M2), three provenance/durability (M3, M4, M6) and one latent (M5).** None of them makes the round-24
claim false today: the loader's arithmetic matches the active registry expectation, the six new fixture rows are
statically consistent with the unchanged `evaluate()`, and the round-23 38-case evidence stays interpretable. What the
defects do is make the *next* round need a production edit again (M2), make a red selftest untriageable from its own
output (M1), and leave the new load-bearing input unpinned by any digest ledger (M3) while the successor registry row
cites a passage that says "38" and "not executed" (M4).

Explicitly **not** claimed here: producer authentication, promotion, historical R17-CMD-BIND closure, numeric score
uplift, or general mutation adequacy of the fixture suite.

## The change under review

`git show d2eaecd -- tools/command-binding.py` (5 insertions, 4 deletions) replaces one hard-coded fixture path with a
two-element loop:

```python
evidence = Path(__file__).resolve().parents[1] / '.ufo/evidence'      # command-binding.py:164
try:                                                                 # :165
    for fixtures in (evidence / 'round-23/extra-cases.json',          # :166
                     evidence / 'round-24/extra-cases.json'):
        supplemental = decode(fixtures.read_bytes())['cases']         # :167
        cases.extend((row['name'], row['bundle'], row['expected_exit'], row['finding_ids'])   # :168-169
                     for row in supplemental)
except (OSError, ValueError, KeyError, TypeError):                    # :170
    print('COMMAND_BINDING_SELFTEST: fixture-unavailable')            # :171
    return 1                                                          # :172
```

The pass denominator is `len(cases) + 2` (`:193`, `:194`), i.e. the merged fixture rows plus the two synthetic tail
cases appended at `:176-177` (`tampered`, `duplicate-json-key`).

## Findings

### M1 (material) — a missing fixture aborts the whole selftest with an opaque message

`tools/command-binding.py:165-172`. The `try` wraps *both* loads and every distinct failure mode collapses into one
string.

- Absent file → `OSError` → `fixture-unavailable`, exit 1, **zero** `CASE` lines.
- Malformed fixture (duplicate JSON key → `Invalid`, a `ValueError` subclass, `:44-49`) → same string.
- Fixture without a `cases` key → `KeyError` → same string.
- Fixture whose `cases` is not a list of dicts → `TypeError` → same string.
- A row missing `name`/`bundle`/`expected_exit`/`finding_ids` → `KeyError` raised lazily inside `cases.extend` → same
  string.

Consequence: if `.ufo/evidence/round-24/extra-cases.json` is absent, the 17 inline cases **and the 19 round-23 fixture
cases are never executed** — the round-23 corpus becomes unreachable through this tool, and the operator sees one
unattributed token. The failure is correctly *fail-closed* (exit 1, so the active registry row
`command-binding-selftest-r24` fails rather than falsely holding), but it is not triageable from its own output: the
message names neither the missing path nor the reason, so "file pruned", "fixture edited into a bad shape" and "row key
renamed" are indistinguishable.

Smallest correction: catch per file and print the offending path and reason, e.g.
`COMMAND_BINDING_SELFTEST: fixture-unavailable path=<p> reason=<type>:<msg>`, keeping exit 1; and decide explicitly
whether a missing *newer* fixture should abort or degrade the older corpus (see M2 for the recommended shape).

### M2 (material) — hard-coded per-round fixture paths couple the public selftest and the frozen ruler's control to round evidence directories

`tools/command-binding.py:164-166` names `round-23` and `round-24` literally.

1. **Every new round needs another production edit.** The round-23 critic that routed this work asked for a *data-only*
   change — `.ufo/waves/round-23/w2/ArgvExact.md`: "Add an `argv-swapped-between-names` case to `extra-cases.json` …
   Optionally add case-only and padded-token variants." The implementation instead added a second fixture file **and**
   edited the tool. The same friction recurs at round 25, 26, ….
2. **The frozen ruler's control now depends on an evidence file, not only on the instrument.** `.ufo/evidence/round-24/measure.py:59-61`
   copies the whole tree into a private clone, `:70` runs the pristine `--selftest` as the control, and `:71-72` marks
   every K1–K4 row `inconclusive` when `control['exit'] != 0`. If the round-24 fixture is missing or reshaped in a
   later tree, the control exits 1 and **all four mutant predicates become inconclusive**, so the frozen "11/11" claim
   becomes unreproducible from the frozen ruler alone. Today the dependency is satisfied (the file is committed at
   `c8c5b88`, verified with `git cat-file -e c8c5b88:.ufo/evidence/round-24/extra-cases.json`), but it is a new kind of
   coupling: a *data* file now gates an *instrument* verdict.
3. The "prune the round directory" hazard is **not new in kind** — the repo already keeps round evidence alive:
   the active rows `command-binding-frozen-clean-pinned` and `command-binding-source-read-red-pinned` both point at
   `.ufo/evidence/round-23/replay/bundle.json`. So this is a hardening of an existing convention, not a new defect
   class; I rate it material only because of point 2 (the frozen ruler) and point 1 (recurring production edits).

Smallest correction: load the cases from a stable, non-round-specific location and stop editing the tool per round —
either move the fixtures under `tools/fixtures/command-binding/` (round-suffixed names), or glob
`.ufo/evidence/round-*/extra-cases.json` sorted by round number, asserting at least one file was found and that all
found files parse. Both keep the round-23 corpus intact and make round 25 a data-only change.

### M3 (provenance) — the new fixture is the one changed file that no digest ledger pins

- Round-23's fixture is pinned: `.ufo/evidence/round-23/reader-freeze2.json` → `paths_sha256[
  ".ufo/evidence/round-23/extra-cases.json"] = 87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00`,
  and the same digest is re-pinned in the round-24 refresh ledger
  `.ufo/evidence/round-24/source-refresh-entries.json` (entry 14 `inputs`).
- The **new** fixture `.ufo/evidence/round-24/extra-cases.json` = `sha256 6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35`
  is pinned **nowhere**: `grep -rn "6ad7842f" .` returns nothing, and the round-24 ledger entry pins
  `tools/command-binding.py` (`9230c68e…`, matches the current file) and the round-23 fixture but not the round-24 one.
  This is not a timing artifact: the file landed at `d2eaecd`, before the ledger's `read_rev` `bd38c02`.

So the new file is a load-bearing input to a *production* tool's public selftest and to the frozen ruler's control, and
it is reconstructible only from git content addressing, with no explicit digest commitment in the evidence tree.

Smallest correction: add `.ufo/evidence/round-24/extra-cases.json: 6ad7842f…` to the round-24 refresh ledger's
`inputs` (and/or a round-24 `reader-freeze` equivalent), so the "44/44" claim has the same pinning discipline the
round-23 "38/38" claim has.

### M4 (provenance) — the successor registry row's `source` cites a passage that says 38 and "not executed"

`tools/registry.json`, row `command-binding-selftest-r24` (active):

```
"expect": {"exit": 0, "stdout_contains": ["COMMAND_BINDING_SELFTEST: 44/44 pass"]},
"source": ".ufo/waves/round-23/fresh-adjudication.json@6a1821a8897eea6e7d9669292160ec9593669409:53-59"
```

Lines 53–59 of that file are the *routed defect* statements:

> "A name-insensitive argv mutant … would survive all 38 selftest cases **[seat inference, not executed]**. Needs a
> swapped-name supplemental case plus that mutant."
> "An unexecuted negative-exit guard-weakening candidate. Its expected survival is a seat inference, not a measured survivor."

The row's *expectation* (`44/44 pass`) is therefore not supported by its own cited authority; the cited passage
supports the opposite numbers (38) and explicitly marks them unexecuted. The sibling rows are fine: the two pinned rows
cite line 66, which is the `bundle_sha256` defect their added expectation answers.

Compounding this: **no retained round-24 receipt records the `command-binding.py --selftest` run.**
`.ufo/evidence/round-24/replay/observations.json` contains no `command-binding` observation at all (verified: the
substring does not occur); the only executed 44/44 evidence in this wave is the wave report
`.ufo/waves/round-24/w1/RunSelftests.md` (private clone at `c8c5b88`, `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0,
44 CASE lines all PASS). A wave report is not a retained receipt under `.ufo/evidence/`.

Smallest correction: retain a round-24 selftest receipt under `.ufo/evidence/round-24/` (instrument digest + both
fixture digests + stdout) and cite it in the successor row's `source`, replacing the routed-defect citation.

### M5 (latent) — the merged case list has no name-uniqueness or schema guard

`tools/command-binding.py:166-169` merges two files' rows plus the inline cases with no uniqueness check and without
looking at the fixture's own `schema` key (both files declare `"schema": "command-binding-extra-cases-v1"`; round-24 adds
`round` and `source` metadata that the loader ignores entirely).

Verified current state — **no live collision**, computed by AST-parsing the inline names and reading both fixtures:

- 1 inline base case + 16 `changed(...)` cases + 19 round-23 rows + 6 round-24 rows + 2 tail cases = **44** printed
  `CASE` lines, **all 44 names distinct**, zero overlap between the inline names and the fixture names.
- Both fixtures contain no duplicate name internally.

The latent risk is evidentiary, not numeric: the printed evidence is name-keyed (`CASE <name> PASS|FAIL`, `:192`) while
the pass count is positional (`:193-194`). A future fixture that reuses a name (e.g. `missing` vs `argv-missing`,
`unknown` vs `unknown-added`) would print two identically-named lines, the count would still read N/N, and a reader (or
`measure.py:82`, which collects `failing_cases` as a list of names) could mis-attribute a failure. Likewise a fixture
with an incompatible `schema` but a `cases` key would be silently consumed.

Smallest correction: after the merge, assert the names are unique and that each file's `schema` is
`command-binding-extra-cases-v1`; fail with a distinct diagnostic (e.g. `duplicate-case-name <name>`) rather than
folding it into `fixture-unavailable`.

### M6 (documentation) — `SKILL.md` still lists only the round-23 fixture

`SKILL.md:2019`, the registry table row for `tools/command-binding.py`, states in the "Persisted values" cell:

> "public fixtures include `.ufo/evidence/round-23/extra-cases.json`"

The tool now loads **two** fixtures, and the round-24 fixture is required for `--selftest` to pass at all. The
Round24 addition paragraph (`SKILL.md:2054-2057`) does mention "44/44", but the row itself — the place a reader looks
for what the tool consumes and what it persists — still names one fixture and says nothing about the missing-file
behaviour (M1) that turns the selftest red.

Smallest correction: extend the cell to list both fixtures and state that an absent fixture makes `--selftest` exit 1
with `fixture-unavailable` (and that the fixture set is the pass denominator).

## Confirmations (checked, no defect found)

1. **Ordering is deterministic and the count is right.** Order is: 17 inline cases (`:143-163`) → 19 round-23 rows in
   file order → 6 round-24 rows in file order → `tampered`, `duplicate-json-key` (`:176-177`). Static count = 44, which
   matches the active registry expectation `"COMMAND_BINDING_SELFTEST: 44/44 pass"` exactly, and matches the executed
   observation in `.ufo/waves/round-24/w1/RunSelftests.md` (44 CASE lines, all PASS, exit 0, at `c8c5b88`).
2. **The round-23 38-case evidence remains interpretable.** `.ufo/evidence/round-23/selftest-A.json` pins
   `revision 496d212…` and `instrument_sha256["tools/command-binding.py"] = d533dc1e…`; the tool at `496d212` and at
   the base `6a1821a` both hash to `d533dc1e…` (verified with `git show <rev>:tools/command-binding.py | sha256sum`);
   the round-23 fixture is byte-unchanged between `496d212` and `HEAD`
   (`git rev-parse 496d212:.ufo/evidence/round-23/extra-cases.json` = `198fcced…` = the current blob) and is pinned by
   digest in `reader-freeze2.json` (`87bffdc8…`). So "38/38 pass" remains reproducible from pinned inputs; the count
   change is explained by the successor row (the round-23 critic had already flagged that the token "moves with the
   fixture count" — `.ufo/waves/round-23/w2/ArgvExact.md`). The only interpretive wrinkle: round-23's stdout is **not**
   a prefix of the current stdout any more — its last two lines (`tampered`, `duplicate-json-key`) are now lines 43–44,
   so a line-by-line comparison of the round-23 receipt against the current output diverges at line 38. The summary
   token changes 38 → 44. Both are explained by the successor row; no ambiguity in interpretation.
3. **The six new rows are internally consistent with the unchanged `evaluate()`** (`tools/command-binding.py:66-112`),
   derived statically row by row: `argv-swapped-between-names` → `ARGV_MISMATCH` only (each receipt's argv belongs to
   the *other* requirement; exit/cwd/revision/stdout all match) → exit 1; `argv-case-only` → `ARGV_MISMATCH`; 
   `argv-padded-token` → `ARGV_MISMATCH`; `argv-repeated-flag` → `ARGV_MISMATCH`; `negative-exit-mismatch` →
   `EXIT_MISMATCH` only (`type(-9) is int`, so not `INVALID_RECEIPT`); `negative-exit-declared-match` → clean, exit 0,
   `[]` (declared `-15` == receipt `-15`, and `type(-15) is int` so it is not `INVALID_REQUIREMENT`). Every
   `expected_exit`/`finding_ids` in the fixture matches the derivation, and every `finding_ids` list is sorted, as
   `evaluate()` returns `sorted(findings)`.
4. **The new fixture really closes the routed gap.** Against the frozen mutants (`.ufo/evidence/round-24/measure.py:29-36`):
   K1 (`receipt['argv'] not in [row['argv'] for row in requirements.values()]`) is killed by
   `argv-swapped-between-names` — each receipt's argv *is* in the requirements' argv list, so the mutant finds no
   mismatch and exits 0 → the case FAILs; K2 (case-folded argv) is killed by `argv-case-only`; K3
   (`receipt['exit'] >= 0 and receipt['exit'] != …`) is killed by `negative-exit-mismatch` (`-9 >= 0` is false). K4
   remains killed by round-23's `all-of-tokens`, as the lesson states. `negative-exit-declared-match` is a useful
   control: it stays green under the K3 mutant, so a fix that over-corrects (treating every negative exit as a
   mismatch) would not pass silently.
5. **No duplicate case names exist today**, in-file or across files, and none collide with the inline case names
   (computed above; `duplicates across all: []`).
6. **The `fixture-unavailable` path cannot fake a kill.** It exits 1 with no `CASE … FAIL` line, and `measure.py:82`
   requires at least one such line, so a fixture outage is scored "not discriminated", never a false pass.

## Residual risk and verification gaps

- **I executed nothing.** My item does not say "Run", so per the lane bounds I performed read-only inspection only
  (`git show/log/cat-file/rev-parse` with `GIT_OPTIONAL_LOCKS=0`, file reads, JSON/AST parsing). I did not run the
  selftest, the registry battery, the gates or `measure.py`, in the lane or in a clone. The 44/44 observation I rely on
  is the sibling's executed report `.ufo/waves/round-24/w1/RunSelftests.md`; my own derivation of the count, the
  ordering and the per-row findings is static.
- **Unverified by me:** the behaviour of the loader when the round-24 fixture is genuinely absent (the code path is
  clear from `:164-172`, but no one has executed that branch); whether `registry-check.py` surfaces the `fixture-unavailable`
  string verbatim (the active row only asserts `44/44`, so a missing fixture shows up as *exit 1*, not as the token).
- **Not mine to close:** whether the round-24 lesson's "after measurement" and the SCORECARD are updated with the
  executed 11/11 result; and the `bundle_sha256` pinning of the two gate rows (routed separately).
- **M2's remedy interacts with the wave's own conventions** (round evidence dirs are already load-bearing for two active
  registry rows), so any relocation of fixtures is a project-level decision, not a local edit.

## Smallest safe correction (ordered, cheapest first)

1. **Loader diagnostics (M1).** In the `except` branch, print the fixture path and the exception type/message and keep
   exit 1. One-line-class change, no behaviour change, no fixture change.
2. **Fixture pinning (M3).** Add `.ufo/evidence/round-24/extra-cases.json: 6ad7842f…` to
   `.ufo/evidence/round-24/source-refresh-entries.json` entry 14 `inputs` (data-only).
3. **Successor-row provenance (M4).** Retain a round-24 `command-binding.py --selftest` receipt under
   `.ufo/evidence/round-24/` (instrument digest, both fixture digests, stdout) and point
   `command-binding-selftest-r24.source` at it instead of the round-23 routed-defect passage.
4. **Merge guards (M5).** Assert unique case names across the merged list and `schema ==
   "command-binding-extra-cases-v1"` per file, with a distinct failure token. Pure addition; today's 44 names already
   satisfy it.
5. **Docs (M6).** Update `SKILL.md:2019` to list both fixtures and the missing-fixture behaviour.
6. **Structural (M2), if the project wants round 25 to be data-only.** Glob
   `.ufo/evidence/round-*/extra-cases.json` (sorted) or relocate the fixtures to `tools/fixtures/command-binding/`, so
   the tool stops naming round directories. This is the only item that touches production code shape; it should be
   decided by L1, since it changes how the frozen ruler's control resolves its fixtures.

## Axes affected

- **Calibration — mildly harmed.** The 44-case suite is honest at `c8c5b88` and the new rows are the right kills, but
  M1–M3 make the suite fragile to inputs that are not digest-pinned and not name-guarded, and M4 means the active
  registry row's expectation is not anchored to an executed receipt.
- **Reproducibility — mildly harmed.** The round-23 38-case evidence survives (item 2 of Confirmations), but the
  *current* expectation has no retained receipt under `.ufo/evidence/`.
- **Correctness of the gate — unaffected.** `evaluate()` is unchanged by this wave; the loader only feeds it cases.
- **Honesty of claims — no overclaim found.** `corpus/lessons/round-24.md` and
  `corpus/knowledge/replay-projection-hardening.md` describe the new fixtures accurately (the "declared -15 that matches
  stays clean" rule matches row 6 and the tool's own docstring), and the contract's bound "K1-K4 count selftest kills of
  four specific mutants, not general mutation adequacy" is respected.

## Tooling

No tools were installed or updated this wave; nothing beyond stock `python3` and `git` was needed, and no package,
binary or service was touched.
