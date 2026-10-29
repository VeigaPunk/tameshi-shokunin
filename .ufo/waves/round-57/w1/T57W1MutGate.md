# T57W1MutGate — C2 gate mutant bank (staged; no lane edits)

Item: 8 single-edit mutants of `tools/receipt-revision-gate.py` at base `5e3569969b532310d2b8a3d130901757a3df356b`, each scored by the lane's 19-case `--selftest` and by three candidate `gate` rows. Machine output: `T57W1MutGate.json` (list of `{id, old, new, selftest_kills, rows_kill}`). Receipts: `T57W1MutGate-receipts/`.

## Method
- Base bytes: `git -C <lane> show 5e35699…:tools/receipt-revision-gate.py` equals the lane working-tree file (`diff -q` identical); base selftest 19/19 pass (`T57W1MutGate-receipts/baseline-selftest.stdout`).
- Each mutant: `git clone -q --shared <lane> <S>/clone-<id>`, `git -C <clone> checkout -q --detach 5e35699…`, `--show-toplevel` asserted equal to the clone, the old string asserted to occur exactly once (`str.count == 1`), one replace, written to the clone's `tools/receipt-revision-gate.py`. The diff is kept at `T57W1MutGate-receipts/mutant-<id>.diff`; the ast parse of every mutant succeeded.
- `selftest_kills`: `python3 tools/receipt-revision-gate.py --selftest` in the mutant clone exits non-zero. Failing case names: `mutant-<id>-selftest.stdout`.
- `rows_kill`: the three candidate rows of `T57W1ExecRegistryRows.md` (staged fixtures `tools/fixtures/receipt-gate/{accept.receipt,drift.receipt,drift.paths}`, sha256 in `spec-fixture-sha256.txt`, copied into each scratch clone only), run with the spec argv (`--lane .`, cwd = clone). A row kills a mutant when its (exit code, codes, verdict token) differs from the base gate's (`baseline-spec-*.stdout`). Rows: `accept` (exit 0, PASS), `drift` (exit 3, RECEIPT_REV_CONTENT_DRIFT, REFUSED), `unres` (exit 2, RECEIPT_REV_UNRESOLVABLE, REFUSED).

## Results

| id | old → new | selftest | rows killing (observed) |
|---|---|---|---|
| accept-on-drift | `if drift:` → `if False:` | KILLED (content-drift-refused) | drift (rc 0, PASS) |
| wrong-refusal-code | `RECEIPT_REV_MISMATCH` → `RECEIPT_REV_ABSENT` | KILLED (strict-mismatch-refused) | none |
| exit0-instead-of-2 | `return 2` → `return 0` | KILLED (unresolvable-certified-refused) | unres (rc 0, same codes/verdict) |
| exit0-instead-of-3 | `else 3` → `else 0` | KILLED (11 cases) | drift (rc 0) |
| drop-ambiguity-check | `if len(revs) > 1:` → `if False:` | KILLED (ambiguous-refused) | none |
| swap-ancestor-test | `is_ancestor(lane, full, certified)` → `(lane, certified, full)` | KILLED (control-ancestors-accepted) | none |
| always-print-pass-line | `or 'none', verdict))` → `or 'none', 'PASS'))` | **SURVIVES** (19/19 pass, rc 0) | drift (verdict line says PASS on a REFUSED run) |
| return-before-paths-read | inserts `if paths: return 0` before the `--paths` read | KILLED (content-drift-refused, ambiguous-refused) | drift (rc 0, no GATE line) |

Full old/new strings are in the JSON.

## Findings
1. **Selftest gap, verdict line.** `always-print-pass-line` passes the whole 19-case suite. Only case 1 inspects `verdict=PASS`, and it is a PASS case, so no case asserts `verdict=REFUSED` on a refused run. Only a row that pins the verdict token (`drift`) catches it. Suggested (not applied; lane is not mine): one selftest case asserting `verdict=REFUSED` on a refusal.
2. **Row coverage gap.** The three rows never reach the strict-mismatch branch (`paths is None`), the ambiguity branch, or the control-ancestor branch. `wrong-refusal-code`, `drop-ambiguity-check` and `swap-ancestor-test` are killed only by `--selftest` (rows_kill empty). For the C2 counter a `gate` row for each of those is needed to make the rows independent of selftest.
3. **Silent-exit mutant.** `return-before-paths-read` prints no GATE line on the drift row (exit 0, `NO_GATE_LINE`). The `drift` row's `stdout_contains` substring would catch it; an exit-code-only check would not.

## Choice for `mutants.json` (C2 counter takes three)
Recommended three, each killed by selftest and by at least one row: `accept-on-drift`, `exit0-instead-of-2`, `exit0-instead-of-3`. A stronger alternative set that also covers the verdict-line blind spot needs a selftest or row change first (finding 1), which is outside this seat.

## Checks run and not run
- Run: base selftest; 8 mutant selftests; 3 spec rows at base and at each of the 8 mutants (24 row runs); ast parse of each mutant; `sha256sum` of staged fixtures.
- Earlier, a first row pass used my own synthetic fixtures; it is superseded by the spec-fixture pass above. Its outputs are in `T57W1MutGate-receipts/baseline-row-*` and `mutant-<id>-row-*` and are not cited.
- Not run: the full `registry-check` on the 3 rows (the registry seat owns it), and any counter.

## Lane and tool hygiene
- Lane: read-only git only (`show`, `status`, `rev-parse`, `clone --shared` source). No writes in the lane or fleet root.
- Edits: none to any lane file. Mutations were in scratch clones under `/fast/scratch/hyaku/tameshi-r57/T57W1MutGate/`, removed at exit.
- Tools installed: none.
