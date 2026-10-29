# T57W1CritC2 — falsification of C2 (round 57, wave 1)

Seat: T57W1CritC2 (critic, leaf). Lane: tameshi. Base: `5e3569969b532310d2b8a3d130901757a3df356b`.
Scope: attack the C2 contract (`.ufo/evidence/round-57/contract.json`, `claims.C2`) before any
counter exists. The contract was not edited. No lane file was edited; no git mutation ran in the
lane. Work ran in a scratch clone (`git clone --shared`, toplevel asserted) and a fixture commit
made in that clone only (`fixture <fixture@example.invalid>`).

## Verdict

C2 as written is **not falsified by a cheap do-nothing tree alone**, because its mutant arm forces a
row that exercises the drift branch. It **is** falsifiable through four loopholes that the counter
text must close before it is built:

1. The mutant arm is satisfied by the **pre-existing** `receipt-revision-gate-selftest` row and by any
   selftest-in-disguise row, unless kill credit is restricted to admitted gate rows.
2. Needle strength: `stdout_contains` values that are a prefix (`RECEIPT_REV`) or generic
   (`verdict=REFUSED`) let mutant M2 (wrong refusal code) survive.
3. The code-truth arm is vacuous when the Standing-rules table names no code (verified: all four code
   cells replaced -> zero tokens -> `all(...)` is True), and its "defined" test as literal source text
   cannot tell an emitted code from a docstring mention.
4. Mutants applied to a *copy* of the gate, or applied in place and then graded with `--rev`, are
   invisible to the rows (verified). Only in-place mutation under `--root`, or a committed mutant graded
   with `--rev`, is seen.

## Sweep and evidence (commands run; outputs under `T57W1CritC2-receipts/`)

Receipts directory: `.ufo/waves/round-57/w1/T57W1CritC2-receipts/`
- `registry-check-matrix.txt` — every row set x every root (unmutated, M1, M2, M3), in-place and committed
- `gate-exit-probes.txt` — the gate's exit/code for each probe receipt at the scratch fixture commit
- `mutant-diffs.txt` — the three mutant diffs (committed scratch commits)
- `cheap-registry.json`, `proposed.json`, `weak.json` — the exact row sets tested

Mutants (exact single replacements; each asserted `count == 1` in the gate source):
- M1 accept-on-drift: `if drift:` -> `if drift and False:`
- M2 wrong refusal code: `codes.append('RECEIPT_REV_CONTENT_DRIFT')` -> `codes.append('RECEIPT_REV_MISMATCH')`
- M3 exit 0 on unresolvable: `return 2\n` -> `return 0\n` (the only `return 2` in the gate, in the `--certified` branch)

Baseline gate exits in the scratch clone (`gate-exit-probes.txt`):
`self-as-receipt` exit 3 `RECEIPT_REV_UNRESOLVABLE`; `--certified deadbeefdeadbeef` exit 2
`RECEIPT_REV_UNRESOLVABLE`; drift with `--paths` exit 3 `RECEIPT_REV_CONTENT_DRIFT`; identical surface
exit 0 `codes=none verdict=PASS`; drift with an EMPTY `--paths` file exit 3 `RECEIPT_REV_CONTENT_DRIFT`;
drift with NO `--paths` exit 3 `RECEIPT_REV_MISMATCH`.

### (1) Do-nothing trees

Eight cheap rows, none needing a new fixture or gate change (`cheap-registry.json`):

| row | argv shape | expect | what it does |
|---|---|---|---|
| cheap-echo-gate | `sh -c "echo GATE:...verdict=PASS; echo tools/receipt-revision-gate.py"` | 0, `verdict=PASS` | runs no gate |
| cheap-selftest-disguise | `python3 -c "subprocess.call(... --selftest)"` | 0, `GATE_SELFTEST: 19/19 pass` | selftest in disguise |
| cheap-self-receipt-exit3 | `--receipt tools/receipt-revision-gate.py:verdict` | 3, `RECEIPT_REV_UNRESOLVABLE` | the gate's own source is the receipt (its selftest literal names `rev=deadbeefdead`) |
| cheap-any-refusal-exit3 | `--receipt tools/registry.json:verdict` | 3, `verdict=REFUSED` | any refusal passes |
| cheap-prefix-needle-exit3 | same | 3, `RECEIPT_REV` | prefix of three codes |
| cheap-unresolvable-exit2 | `--certified deadbeefdeadbeef` | 2, `RECEIPT_REV_UNRESOLVABLE` | exit 2 never reads the receipt |
| cheap-exit0-existing-r56-control | `--certified BASE --receipt .ufo/evidence/round-56/control/controls-a.stdout:control` | 0, `verdict=PASS` | exit 0 on an existing committed receipt |
| cheap-missing-exit3 | `--receipt nope-missing.txt:positive` | 3, `RECEIPT_MISSING` | binds nothing |

Results:
- Live (`--root` clone) and `--rev BASE`: **held=8/8** both (matrix).
- Against mutants (in-place, `--root`): M1 -> only `cheap-selftest-disguise` turns red (7/8); M2 -> only
  `cheap-selftest-disguise` (7/8); M3 -> `cheap-unresolvable-exit2` and `cheap-selftest-disguise` (6/8).
- So the cheap set gives arm (a) (>=3 gate rows with exits 0, 2, 3) by surface count, but **arm (c)
  fails**: M1 and M2 survive unless the selftest-in-disguise row is counted as a kill. A counter that
  credits any row whose argv merely mentions the gate, or any row containing `--selftest`, would then
  PASS this cheap tree with zero new gate semantics. Such a counter is falsified by row
  `cheap-selftest-disguise`.

Also: the **existing** `receipt-revision-gate-selftest` row (base registry) is red under M1, M2 and M3
(`existing gate selftest row vs M1/M2/M3 in-place`: held=0/1 each). A counter that credits it toward
arm (c) passes arm (c) with no new row at all.

Minimal non-cheap tree that does pass the mutant arm (`proposed.json`, 3 rows, all exit-coded with
named codes, no selftest):
- `g-exit0-identical-surface`: `--certified HEAD --paths fixtures/c2/surface-same.paths --receipt fixtures/c2/verdict-base.txt:verdict`, expect 0 `verdict=PASS`
- `g-exit3-content-drift`: `--certified HEAD --paths fixtures/c2/surface-drift.paths --receipt fixtures/c2/verdict-old.txt:verdict`, expect 3 `RECEIPT_REV_CONTENT_DRIFT`
- `g-exit2-unresolvable-certified`: `--certified deadbeefdeadbeef ...`, expect 2 `RECEIPT_REV_UNRESOLVABLE`

Fixture facts: `verdict-old.txt` names `c3e2ca9` (an ancestor where `tools/receipt-revision-gate.py`
differs from BASE); `surface-drift.paths` lists that gate; `surface-same.paths` lists
`tools/registry-check.py` (byte-identical from c3e2ca9 to BASE, `git diff --name-only` empty).
Results: unmutated **held=3/3** live and at `--rev F1`; M1 -> drift row differs (2/3); M2 -> drift row
differs (2/3); M3 -> exit-2 row differs (2/3). **3/3 killed**, with each mutant killed by a distinct
named row family.

Verdict on (1): cheap trees reach `C2_R57_PASS=true` only if the mutant arm is credited by a
non-selftest row. Do-nothing does not reach PASS through the drift arm; it reaches PASS through
(a) selftest-disguise credit or (b) the pre-existing selftest row, both of which the counter must
exclude explicitly (see rewrites).

### (2) Mutant routing: how a mutant reaches the rows

The rows' argv is `python3 tools/receipt-revision-gate.py ...` (relative). `registry-check` executes
it with `cwd = root`. So a mutant is seen **only** if the file at `<root>/tools/receipt-revision-gate.py`
is the mutant at the moment the row runs. A copy elsewhere is never executed.

Verified:
- **Copy route: wrong.** Mutated a copy (`$S/copy-trap/tools/receipt-revision-gate.py`, M1); rows ran
  against the unmutated clone: held=3/3.
- **Uncommitted in-place mutation + `--rev`: wrong.** `registry-check --rev REV` re-clones REV from the
  lane's commit, so the working-tree mutant disappears. M1 in its mutant clone graded with `--rev F1`:
  held=3/3 (drift row green).
- **In-place mutation + `--root` (live mode): right.** M1/M2/M3 each in a fresh `git clone --shared`
  checked out at F1 with one replacement: 2/3 held each, the named row red (matrix).
- **Committed mutant + `--rev <mutant sha>`: right and hermetic.** M1 (`94ec8ff2c4cd`), M2
  (`3a35b90967c1`), M3 (`4b7634cfbfdb`) committed in their scratch clone and graded with `--rev`:
  2/3 held each, the same rows red as the in-place route.

Exact mechanism for the counter (recommended, verified):
1. Baseline first: `git clone --shared LANE W/base`; `git -C W/base checkout --detach REV`;
   `python3 W/base/tools/registry-check.py --root W/base --tag <gate tag>` must be held N/N.
2. Per mutant k: `git clone --shared LANE W/mut-k`; `checkout --detach REV`; one replacement with
   `assert text.count(old) == 1`, written into `W/mut-k/tools/receipt-revision-gate.py` in place.
3. Assert `git -C W/mut-k status --porcelain` lists exactly `tools/receipt-revision-gate.py`
   (the registry must NOT differ, or the mutant can change its own expectations).
4. Run `W/mut-k/tools/registry-check.py` **from the mutant clone** (its own checker copy at REV), with
   `--root W/mut-k` and the REV registry (`--registry` omitted, so `W/mut-k/tools/registry.json`, which is
   unchanged). Record which admitted rows go red. Expect >=1 per mutant.
5. Hermetic alternative: commit the mutant in `W/mut-k` (fixture identity) and run `--rev <sha>`.

### (3) Code-truth arm (SKILL `## Standing rules` table; the gate's CODES)

Measured facts:
- Table rows (SKILL.md:51-56): row 1 (`a verdict receipt names another revision`) code cell
  `RECEIPT_REV_MISMATCH` (line 53); row 2 (`a positive control was scored at the freeze`) cell
  `RECEIPT_REV_CONTENT_DRIFT (no --paths: RECEIPT_REV_MISMATCH)` (line 54) — row 2 also contains
  `--paths`, so a "contains --paths" locator hits it; row 3 `RECEIPT_REV_UNRESOLVABLE`; row 4
  `RECEIPT_REV_ABSENT`.
- The gate emits CONTENT_DRIFT for role=verdict with `--paths` on drift (`gate-exit-probes.txt`).
  Row 1 is therefore false in the case it names. (Matches lesson round-56 F2.)
- Vacuity (verified in-process): replace every code cell with `refused` -> 0 RECEIPT tokens remain in
  `## Standing rules`; `all(t in CODES for t in tokens)` is True. The "every token is a defined code"
  arm passes an absent table.
- "Defined" by text: the gate text contains `RECEIPT_REV_CONTENT_DRIFT` 4 times in both the base and
  M1 (`emit sites: 1` in both, since M1 only edits the condition). A text grep cannot tell M1 from base.
- Empty surface: `--paths` on a file with only comments gives `RECEIPT_REV_CONTENT_DRIFT` with detail
  `<no --paths given: content identity is not checkable>` (verified). The row 2 parenthetical "no
  `--paths`: MISMATCH" is true only for an absent flag, and the detail text contradicts its own code.
- Unresolvable listed paths: `drifted_paths` turns a path present in neither revision into
  `<unresolvable-path:P>`, which is reported as drift. A counter fixture that names a bogus path proves
  nothing about content drift.
- Needle strength: under M2 (drift -> MISMATCH), needles `verdict=REFUSED` and `RECEIPT_REV` both
  held (`weak needles vs M2 in-place: held=2/2`). Exit-3 rows need an exact CODES member.

## Proposed exact rewrites (for the counter author; contract not edited)

### C2 counter, mutant arm
- Kill credit only from admitted rows: `kind == "gate"`, `status == "active"`, `argv[0]` in
  `{python3, python}`, `argv[1] == "tools/receipt-revision-gate.py"` exactly, `"--selftest" not in argv`,
  no argv element in `{"-c", "-m"}`. (Rejects `cheap-echo-gate` and `cheap-selftest-disguise`; the
  pre-existing `receipt-revision-gate-selftest` row is therefore not admitted.)
- Expectations come from the REV registry only; the mutant never touches `tools/registry.json`
  (assert `git status` lists just the gate file).
- Mutant route: the in-place `--root` clone (step 2-4 above) or a committed mutant with `--rev`.
  Forbidden: a copy, and `--rev REV` with an uncommitted mutation.
- Scoring: baseline held N/N first; then each of M1, M2, M3 must redden >=1 admitted row; report the
  red row names per mutant.

### C2 counter, row-expectation arm
- `expect.exit` in {0, 2, 3}; every `expect.exit == 3` row's `stdout_contains` contains an element
  equal (not substring) to a member of CODES; `expect.exit == 2` rows contain exactly
  `RECEIPT_REV_UNRESOLVABLE`. Reject `verdict=REFUSED`, `RECEIPT_REV`, `codes=` as needles.
- Counter recomputes each row's gate exit on its own fixtures and compares with `expect` (rows are not
  trusted to self-describe).

### C2 counter, code-truth arm
1. Locate the row: exactly one table row inside `## Standing rules` whose first cell, backticks stripped
   and trimmed, equals `a verdict receipt names another revision`. Zero or many -> FAIL (not skip).
2. Its code cell (last cell, backticks stripped, trimmed) must equal exactly `RECEIPT_REV_CONTENT_DRIFT`,
   compared to the code the gate emits on a counter-built verdict fixture with a non-empty `--paths`
   surface and real drifting bytes (the `drift=<path>` detail names that path, not `<unresolvable-path`).
3. Non-vacuity: the section holds >=4 table data rows and >=4 distinct `RECEIPT_*` tokens; zero -> FAIL.
4. CODES from the gate by AST (`ast.literal_eval` of the `CODES = (...)` assignment), not text grep.
5. Every `RECEIPT_*` token in the section is in that CODES set.

SKILL line 53, in-line replacement (no line-count change; keeps the three-column row):
`| a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared `--paths` surface; with no `--paths` the code is `RECEIPT_REV_MISMATCH` | `RECEIPT_REV_CONTENT_DRIFT` |`

Line 54 (row 2) is not the C2 target; a strict counter that applies "cell equals one code" to every
row would fail it. Either leave row 2 under its own rule, or state in the counter that only row 1 is
equality-checked (the cannot-see list must say so).

### C2 counter, gate/probe table row
The `#### Gate/probe registry — round 51` table (header at SKILL.md ~2181-2183:
`| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |`).
Counter check: the row whose Name cell is `receipt-revision-gate`, and its `Verdict map` cell matches
`\b0\b` ... `\b2\b` ... `\b3\b` AND contains the literal `RECEIPT_REV_UNRESOLVABLE`. Plain "0/2/3" anywhere in the
line is not enough. Adding this row lies below the Standing-rules section (line count change below
~2196 shifts `:NNN` anchors after it; the no-harm arm has to account for that at C0).

## Cannot see (not checked here)
- Whether the three mutants are the defects that matter (the contract already says so).
- Whether `c3e2ca9` is the right drift ancestor for the lane's permanent fixtures (it is used for the
  falsification only; a permanent fixture needs its own choice and commit).
- Row 2 of the Standing-rules table under equality; coverage of CODES (4 of 11 named; the lesson F2
  records it; the target does not require coverage).
- The round-56 docs arm counts CODES names in `tools/registry.json` text; the selftest row's prose already
  names all 11 codes, so that arm is satisfied by prose (noted for the round-56 counter; not re-attacked).
- `WITNESS` flags and the `registry-check` non-hermetic argv rule under `--rev` for the proposed rows
  (all rows used relative argv only; no non_hermetic_argv was reported).

## Tools
No tools installed or updated. Used the host's `git` and `python3` (stdlib). No pacman, no uv, no npm
installs. Scratch tree `$HYAKU_SCRATCH/tameshi-r57/T57W1CritC2` removed on exit.
