# T57W1SimplScope — deletion candidates (round 57, wave 1)

Lane base 5e3569969b532310d2b8a3d130901757a3df356b. Read-only: no lane, fleet, or staged file was edited; no installs; no git mutation (fixture repo under scratch, removed on exit). Receipts: `T57W1SimplScope-receipts/`.

Two inputs named in the item were not available when I read: `T57W1CritDoNothing.md` (absent from the wave dir) and the C2 counter at `.ufo/evidence/round-57/c2/measure.py` (not yet in the lane; I read the staged copy's source and its recorded selftest receipt, `T57W1ExecC2Counter-receipts/selftest.stdout`, and did not re-run the staged selftest).

## Axes

- A: SKILL `## Standing rules` receipt table is true to the gate (R56.2; C2 cell arm).
- B: C2 arms each have a control that nothing else catches (C2 operability).
- C: ledger rows carry only fields the counters read (C1 operability; no counter score moves).
- No-harm: SKILL.md line counts above and below the table; ledger bytes for rounds 40-49.

## Ranked deletions

Ranked by (control lost = 0) first, then by bytes removed, then by no-harm cost.

### D1. Delete SKILL table row 2 (the "positive control" row) — preserves all behaviour

- Row, SKILL.md:52-54: `a positive control was scored at the freeze | refused: the freeze predates ... | RECEIPT_REV_CONTENT_DRIFT (no --paths: RECEIPT_REV_MISMATCH)`.
- The gate has one branch for both roles: `tools/receipt-revision-gate.py` `check()`, `if role_name in ('positive', 'verdict'):`. Measured on a fixture (receipts `c1`–`c6`, `c12`):

| receipt | positive | verdict |
|---|---|---|
| names A, certified B, `--paths` covers only the unchanged file | exit 0, PASS (`c1`) | exit 0, PASS (`c2`) |
| names A, `--paths` covers the changed file | exit 3, CONTENT_DRIFT (`c3`) | exit 3, CONTENT_DRIFT (`c4`) |
| names A, no `--paths` | exit 3, MISMATCH (`c5`) | exit 3, MISMATCH (`c6`) |

- Row 2's "refused" is unconditional in form; the gate accepts a positive control whose bytes match on the declared surface (`c1`, exit 0). Row 1 already states that condition correctly.
- Control lost: none. The staged cell arm reads only the row whose first cell starts `a verdict receipt names another revision` (per the C2 counter's doc). Keep that prefix in row 1 and append "(positive controls take the same branch)".
- No-harm: deleting one table row moves every line below SKILL.md:54 up by one. Page-local `:NNN` anchors below the table shift; state this in the L1 integration.

### D2. Replace row 1's parenthetical with a condition; set its code to the one the gate emits — preserves the cell arm, fixes R56.2

- Current row 1 (SKILL.md:53): `RECEIPT_REV_MISMATCH`. The gate emits `RECEIPT_REV_CONTENT_DRIFT` whenever `--paths` lists a path (`c4`). This is the R56.2 defect; the base cell is the one the C2 counter reports as `WRONG:RECEIPT_REV_MISMATCH`.
- Row 2's parenthetical `(no --paths: RECEIPT_REV_MISMATCH)` is not the right condition. An empty `--paths` file (comments only) reads as "no path", and the gate emits `RECEIPT_REV_CONTENT_DRIFT` with `drift=<no --paths given...>` (`c7`), not MISMATCH. So "no --paths" is the wrong condition. Use "`--paths` lists at least one path" in the situation cell and keep `RECEIPT_REV_CONTENT_DRIFT` alone in the code cell.
- Keep the no-paths branch (MISMATCH, `c5`/`c6`) in the gate docstring, not the table. Adding a second row with the same first-cell prefix would make the C2 counter's row lookup ambiguous; do not do it.
- The C2 counter's `cell` arm requires exactly one code token in that cell; this edit satisfies it.

### D3. Ledger: stop storing `seat` (new rows only) — zero counter reads

- Reads: `.ufo/evidence/round-50/c1/measure.py` reads `id, status, evidence, commit, reason` (lines 199, 227-228, 261). It does not read `seat` or `note`. The staged round-57 C1 counter has the same branches (lines 189, 213, 244). `grep` for `['seat']`, `get('seat')`, `['note']`, `get('note')` over `.ufo/evidence/round-50`, `.ufo/evidence/round-57` and `tools/` returns nothing (`ledger-field-triage.txt`).
- Derivation: `.ufo/evidence/round-50/integrate/merge-ledger.py:35` sets `seat` to `T50Disp<r>` from the disposer's file name. The 9 `TameshiR50 (L1)` rows are L1 overrides.
- Cost: 49 rows, 11 distinct seat strings (10 `T50DispNN` + `TameshiR50 (L1)`). Provenance moves to the overrides file and the agreement table; it is not lost.

### D4. Ledger: do not write dead payloads (new rows only) — 8 field instances in 6 existing rows

- Dead under the counter: `commit` is read only in the `fixed` branch (line 227-228); `reason` only in the else (declined) branch (line 261). Dead instances in the existing ledger:
  - `commit` on declined: R40.5, R44.2, R45.3.
  - `commit` on open: R45.1, R45.4.
  - `reason` on open: R45.1, R45.4.
  - `reason` on fixed: R44.1.
- Apply to R50-R56 rows only. Rewriting R40-R49 changes historical bytes for no counter gain; the counter reads both schemas identically.

### D5 (not recommended now). `note` — read by nothing, but it is the only human rationale

- 48 of 49 rows have a non-empty `note`. Keep it. It is last in rank because deleting it saves the most bytes and loses the most reader value.

## Not deletable (checked)

- Ledger `status`: not derivable from payload presence today. Counts over 49 rows: fixed 31 (all carry `commit`; R44.1 also carries `reason`); declined 11 (all carry `reason`; R40.5, R44.2, R45.3 also carry `commit`); open 7 (5 carry neither; R45.1 and R45.4 carry both). After D4 the presence mapping is bijective on the current data (commit ↔ fixed 31, reason ↔ declined 11, neither ↔ open 7). Still keep `status` explicit: the counter branches on it, and a row with both payloads is not rejected today.
- `evidence[].path`, `lines`, `excerpt`: each is read (the path to resolve, the window to bound `b-a<=30`, the excerpt to match).
- `commit` on fixed rows; `reason` (>= 40 chars) on declined rows; `id`.

## C2 arms: no arm is droppable

The C2 counter arms (staged, `T57W1ExecC2Counter`): rows, executed, mutants, skill_row, codes, cell. Each has a breaker in the staged selftest receipt that no other arm catches (`c2-staged-selftest-breakers-quoted.txt`):

| arm | breaker that only this arm catches (staged selftest) |
|---|---|
| rows | no exit-2 row → rows shortfall; selftest-argv rows are not gate rows |
| executed | a row expecting the wrong exit → held 2/3 |
| mutants | exit-0-only row → 0/3; without the drift row → 1/3; non-unique `old` → 2/3 |
| skill_row | no gate row → 0; verdict map without the 2 → 0 |
| codes | a token the gate does not define in another row → codes_known 2/3 |
| cell | stale MISMATCH cell → WRONG; cell with no code → WRONG:none; gate emitting MISMATCH flips the verdict |

Nearest candidate: `codes` (N1). It is droppable only together with a pointer in rows 3 and 4 (below). As the table stands it is the only arm that catches a bogus code in a non-verdict row.

### N1. `codes` arm — conditional

- Drop only if rows 3 and 4 stop stating codes. Then the only code token is the verdict cell, which the cell arm already pins to the emitted code, so `codes` adds nothing.
- Cost: a row 3/4 mapping error (a condition paired with the wrong code) is then unchecked. That is the tradeoff; I recommend not doing it this round.

### N2. Delete the whole table — not allowed

- The round-57 contract's `surface` requires the verdict-receipt cell to state the code the gate emits (R56.2). A pointer-only cell fails the cell arm: "cell with no code" → `WRONG:none` in the staged selftest.

## Corrections (not deletions)

- `--help` does not exist. `python3 tools/receipt-revision-gate.py --help` prints the usage line and exits **1** (`gate-exits-and-help.txt`). The table cannot point at `--help`; if a pointer is wanted, it points at the docstring (lines 1-33).
- Exit codes are undocumented for two paths. The docstring says "Exit 0 iff PASS" and "each a named refusal, exit 3". Measured: unresolvable certified REV → exit **2** (`c13`), usage error → exit **1**. The SKILL gate row must name 0/2/3; the gate header should name 2 too (one docstring line; this changes gate bytes, so check the mutant `old` strings stay unique).
- Table row 3 (SKILL.md:55) is narrower than the gate: "a control set's CTL lines name a revision absent" — the gate emits `RECEIPT_REV_UNRESOLVABLE` for any role (`c9`, verdict). Reword to "a receipt names a revision that does not resolve".
- The table has no rows for `RECEIPT_CONTROL_NOT_ANCESTOR` (`c11`), `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_REQUIRED_LINE_MISSING`, `RECEIPT_DIGEST_MISMATCH`. These are additions, out of scope here.

## Evidence index

- Gate matrix (fixture, scratch, removed): `receipts/c1`–`c13`, `revs.txt`.
- Exit codes and help: `gate-exits-and-help.txt`.
- Ledger field reads and dead-field rows: `ledger-field-triage.txt`.
- SKILL table, lines 51-56 as read: `skill-standing-rules-table-lines51-56.txt`.
- Staged C2 selftest breaker receipt, quoted: `c2-staged-selftest-breakers-quoted.txt`.
- Ledger generator: `.ufo/evidence/round-50/integrate/merge-ledger.py:17,35`.

## What I did not check

- The staged selftest was not re-run; the breaker table quotes its receipt.
- Whether the cell arm's row lookup stays unambiguous after D1+D2 is inferred from its documented rule, not from running the staged counter on the edited table.
- Whether SKILL.md is in the coldread monitor's pinned set (no-harm). If it is, the L1 must re-measure after D1; I did not measure it.
- `T57W1CritDoNothing.md` was not available; the C2 arm analysis rests on the staged selftest receipt alone.
