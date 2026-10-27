# T52W1Corr20 — correction record for round-51 cold-read re-key entry `### Round-26 gate/probe registry — report interop`

Seat: scribe, C2 m4 (correction record). Lane `tameshi-shokunin`. Item: round-51 cold-read re-key entry, read_rev `02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read20`.

## Behaviour

1. Read the frozen contract `.ufo/evidence/round-52/contract.json` (claims, predicate, `no_harm.coldread_note`; never edited) and the frozen counter `.ufo/evidence/round-52/c2/measure.py` (m4/m6 and `check_findings` rules read at source).
2. Located the ledger entry for this heading at the `02ec217c` family: `.ufo/evidence/round-21/coldread/ledger.json` entry with `heading` = `### Round-26 gate/probe registry — report interop`, `read_rev` `02ec217c4d0afabe727fde2e261b7951d28fb4e9`, `seats` `["T51W2Read20", "L1 TameshiR51a3 integration (attempt 3)"]`, span 2132–2171, `wrong_expectations: 0`, `minor_gaps: 0`, `class: record`. Command: `python3 -c` over the ledger (see receipt below). The ledger's top-level `corrections` list currently holds 0 entries; this seat produces the record the L1 appends (one per re-key entry, 20 total).
3. Read the reader file in full (101 lines) and the section at read_rev (`git -C . show 02ec217c…:SKILL.md`, lines 2132–2171) and recorded every statement the reader marked false / stale-pointer / unsupported / stale-count. Reader's own verdict: "section mostly holds; 2 HIGH + 2 MED stale-by-tenth-leg/TMPDIR findings, 3 LOW prose/literal drifts". Reader's "holds" rows and its disclosed/historical notes (NOTE-A runner-pin drift, NOTE-B round21-measure fresh-clone exit 1) are excluded, per the item; the reader marks both as disclosed.
4. Cross-checked the reader's four substantive claims at read_rev before recording them (read-only `git show`, no writes):
   - `tools/mte-interop.py` `LEG_TABLE` has **10** keys (…, `bash-drift-pins`) and `:318` says "differs from the **ten** ledger legs"; `:343` prints `legs_conforming=%d/%d`.
   - `tools/registry.json:1011-1016` `mte-interop-check` (status `active`) expects `"MTE_INTEROP: PASS legs_conforming=9/9"`.
   - `tools/mutate-and-run.sh:1432` `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")`; `:1555` `tameshi-r4-2-selftest.XXXXXX`; `:149` "(r51 honours TMPDIR)"; no bare `mktemp -d /tmp` anywhere in the runner. `:1357-1365` is a verdict-comparison loop, not the auto-root construction.
   - `tools/mutate-and-run.sh:104` names `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec (leg 10)`; `:1155` heredoc writes `bash-drift-pins.spec`.
   - `tools/registry-check.py:1816` prints only `SELFTEST: PASS ({passed} cases)`; `tools/context-capture.py:1785` prints `SELFTEST: PASS ({}/{})` with no " cases" suffix.

## Deliverable

`.ufo/waves/round-52/w1/T52W1Corr20.json` — keys exactly `heading`, `read_rev`, `reader`, `reader_file`, `wrong_expectations`, `findings`; `wrong_expectations` = `len(findings)` = **7**.

## Findings (7)

1. **HIGH-1** — class `stale-count`. Reader line 62: `**HIGH-1 — SKILL.md:2136, Round-26 row: "leg set not equal to the nine ledger legs" is false at CAND.**`
   Skill statement (SKILL.md:2136 at `02ec217c`): `leg set not equal to the nine ledger legs`. Shows it: the number is nine while `tools/mte-interop.py:318` says ten and `LEG_TABLE` (`:74-77`) has 10 entries. Command: `python3` AST walk of `git show 02ec217c…:tools/mte-interop.py` + grep for "ten ledger legs" (output in `.ufo/waves/round-52/w1/T52W1Corr20.check.txt` sibling run below).
2. **HIGH-2** — class `stale-count`. Reader line 65: `**HIGH-2 — tools/registry.json:1011-1016 `mte-interop-check` row (status active) is unsatisfiable at CAND, and SKILL.md:2136 repeats its stale "(9/9)".**`
   Skill statement (SKILL.md:2136): `Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9).` Shows it: `tools/registry.json` at `02ec217c` lines 1013-1015 carry `"stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]` with `"status": "active"`, and `mte-interop.py:343` prints the denumerator as `len(legs)` (10).
3. **MED-1** — class `false`. Reader line 68: `**MED-1 — SKILL.md:2149 (fleet mutation runner row):` (recorded without the reader's own in-line "…" so the quote carries no ellipsis; the reader's full line reads `… : "auto mktemp under /tmp … selftest under /tmp" is stale.**`).
   Skill statement (SKILL.md:2149): `caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show`. Shows it: `mutate-and-run.sh:149` "(r51 honours TMPDIR)", `:157/:217/:491/:1432/:1555` all `"${TMPDIR:-/tmp}/…"`. Command: python scan of runner lines containing `mktemp` (no bare `/tmp` form).
4. **MED-2** — class `stale-pointer`. Reader line 71: `**MED-2 — tools/tally-audit-v3.py:34,408 (echoed by SKILL.md:2161 "witness the runner shape"): stale model of the runner's auto root.**`
   Skill statement (SKILL.md:2161): `plus one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX allocated to witness the runner shape and removed at exit`. Shows it: cited range `mutate-and-run.sh:1357-1365` is a verdict-comparison loop at `02ec217c`; the auto root is built at `:1431-1433` as `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX`.
5. **LOW-1** — class `false`. Reader line 74: `**LOW-1 — SKILL.md:2154 (entry-registry walk row): "last line SELFTEST: PASS (51 cases) at 84aa673".**`
   Skill statement (SKILL.md:2154): `last line SELFTEST: PASS (51 cases) at 84aa673`. Shows it: `tools/registry-check.py:1816` is `emit(f"SELFTEST: PASS ({passed} cases)")` — no rev is printed; `84aa673` is provenance.
6. **LOW-2** — class `false`. Reader line 77: `**LOW-2 — SKILL.md:2144 (context receipt replay row): claimed literal "SELFTEST: PASS (49/49 cases)".**`
   Skill statement (SKILL.md:2144): ``python3 tools/context-capture.py --selftest`` → `SELFTEST: PASS (49/49 cases)`. Shows it: `tools/context-capture.py:1785` prints `SELFTEST: PASS ({}/{})` — no " cases" suffix.
7. **LOW-3** — class `stale-pointer`. Reader line 80: `**LOW-3 — SKILL.md:2149 (fleet mutation runner row) pinned-values cell omits the tenth leg's spec.**`
   Skill statement (SKILL.md:2149 pinned-values cell): ``corpus/knowledge/fleet-kill-rate-ledger.md``, ``.ufo/evidence/round-18/sources-check/sources-check.defects.spec``, ``.ufo/evidence/round-26/cite-check/cite-check.defects.spec``; leg sha256 pins and verdict tables are literals in the tool. Shows it: `mutate-and-run.sh:104` names `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec (leg 10)` and `:1155` writes it into the spec dir, so the pinned-values enumeration predates the tenth leg.

Excluded, per the item (reader "holds" / disclosed): `tools/round21-measure.py` row (NOTE-B, disclosed environment bound), `round12/BashWitness` declaration pin drift (NOTE-A, declared 2-class input drift), `wave-parent-settle` "records SETTLED" (reader verdict holds; verdict derived from `parent_exit_unix`), and every `verdict: "holds"` pointer row.

## Gates (observed output)

Frozen-counter rule applied via the frozen module itself (`importlib` load of `.ufo/evidence/round-52/c2/measure.py`, no edits), reader text = `.ufo/evidence/round-51/coldread/reads/T51W2Read20.md`, floors = `FLOORS['T51W2Read20']`:

```
WROTE .ufo/waves/round-52/w1/T52W1Corr20.json wrong_expectations=7
FROZEN check_findings -> None
quote len=103 verbatim=True ellipsis=False skill_statement_in_section=True :: **HIGH-1 — SKILL.md:2136, Round-26 row: "leg set not equal to the nine ledger legs" is fal
quote len=153 verbatim=True ellipsis=False skill_statement_in_section=True :: **HIGH-2 — tools/registry.json:1011-1016 `mte-interop-check` row (status active) is unsati
quote len=52 verbatim=True ellipsis=False skill_statement_in_section=True :: **MED-1 — SKILL.md:2149 (fleet mutation runner row):
quote len=135 verbatim=True ellipsis=False skill_statement_in_section=True :: **MED-2 — tools/tally-audit-v3.py:34,408 (echoed by SKILL.md:2161 "witness the runner shap
quote len=102 verbatim=True ellipsis=False skill_statement_in_section=True :: **LOW-1 — SKILL.md:2154 (entry-registry walk row): "last line SELFTEST: PASS (51 cases) at
quote len=103 verbatim=True ellipsis=False skill_statement_in_section=True :: **LOW-2 — SKILL.md:2144 (context receipt replay row): claimed literal "SELFTEST: PASS (49/
quote len=100 verbatim=True ellipsis=False skill_statement_in_section=True :: **LOW-3 — SKILL.md:2149 (fleet mutation runner row) pinned-values cell omits the tenth leg
SECTION-SPAN lines 41 heading found: ### Round-26 gate/probe registry — report interop
ALL-OK True
FLOORS ['HIGH-1', 'HIGH-2', 'MED-1', 'MED-2'] covered: True
```

Receipt saved at `.ufo/waves/round-52/w1/T52W1Corr20.check.txt`. `verbatim=True` is `squash(quote) in squash(reader_text)`; lengths are `squash(quote)` lengths (20 ≤ len ≤ 200); `skill_statement_in_section=True` is `squash(skill_statement) in squash(section(02ec217c:SKILL.md, heading))`. `check_findings` returned `None` (no violation), which is the frozen counter's own m4 precondition for this reader.

## Touched surfaces

- Written (mine only): `.ufo/waves/round-52/w1/T52W1Corr20.json`, `.ufo/waves/round-52/w1/T52W1Corr20.md`, `.ufo/waves/round-52/w1/T52W1Corr20.check.txt`.
- Read only: `SKILL.md` via `git show 02ec217c…`, `tools/mte-interop.py`, `tools/registry.json`, `tools/mutate-and-run.sh`, `tools/registry-check.py`, `tools/context-capture.py` (all via `git show 02ec217c…`), `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-51/coldread/reads/T51W2Read20.md`, `.ufo/evidence/round-52/contract.json`, `.ufo/evidence/round-52/c2/measure.py`.
- No lane file edited, no git/jj mutating command, no fixture repo created, no counter `--selftest`/claim run. Scratch root `/fast/scratch/hyaku/tameshi-r52/T52W1Corr20` created and deleted (`mkdir -p` + `rm -rf`; `ls` confirms absent). No tool installed or upgraded.

## Out of scope / not done

- No SKILL.md fix, no `tools/registry.json` edit, no append to the ledger `corrections` list: the L1 owns m1/m2/m3/m5 text edits, the C1 registry row, and appending the 20 records (m4 requires exactly one record per `02ec217c` entry).
- No claim decided; C2's total is the deciding run's to print. Nothing here asserts the corrected pointers the L1 chooses.
- `wrong_expectations` counts the reader's seven labelled findings; it does not re-audit the reader's ~50 pointer rows beyond the four labels + notes cross-checked at read_rev. The five "LOW prose drift" rows the reader hedged (e.g. `wave-parent-settle` SETTLED derivation, `tally-audit-v2:266` comment) are not counted because the reader graded those rows holds and attributed the drift to tool comments, not to section statements.

## Summary

Correction record for `### Round-26 gate/probe registry — report interop` (`02ec217c`, reader `T51W2Read20`): `wrong_expectations` 7, not the 0 the round-51 refresh wrote from code.
Findings: HIGH-1 and HIGH-2 stale leg count (nine/9/9 vs the tool's ten); MED-1 false `/tmp`-only write scope (runner honours TMPDIR); MED-2 stale auto-root pointer (`:1357-1365` moved, real build at `:1431-1433`); LOW-1/LOW-2 false printed-literal claims; LOW-3 pinned-values cell missing the tenth leg's spec.
Every quote is byte-exact from one reader line, no ellipsis; the frozen `check_findings` returns `None` and all four floors (HIGH-1/HIGH-2/MED-1/MED-2) are covered.
Reader's "holds" verdicts and disclosed notes (NOTE-A, NOTE-B) are excluded; all four substantive claims were re-verified at `02ec217c` with read-only `git show`.
Deliverable: `.ufo/waves/round-52/w1/T52W1Corr20.json`; receipt `.ufo/waves/round-52/w1/T52W1Corr20.check.txt`.
