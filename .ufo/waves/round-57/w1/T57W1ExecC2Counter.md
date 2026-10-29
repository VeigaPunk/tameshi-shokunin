# T57W1ExecC2Counter - C2 counter (staged)

Staged (not installed), under `.ufo/waves/round-57/w1/T57W1ExecC2Counter/stage/`:

- `.ufo/evidence/round-57/c2/measure.py` (stdlib + git; `--lane --rev [--work] [--explain]`, `--selftest [--lane] [--rev]`)
- `.ufo/evidence/round-57/c2/mutants.json` (3 mutants; sha256 `d51f558ca7a4f32c301eccd3bc5ce0814b11da8e16dac539058fbb843448e6de`, pinned in measure.py as `MUTANTS_SHA256`)

Both must be copied into the lane together and frozen before anything scores. The counter reads
`mutants.json` from git at REV and refuses it (mutants=0/3) when its sha256 differs from the pin; editing
mutants.json after the pin therefore needs the pin edited in measure.py as well.

## Behaviour (arms; total = sum of integer shortfalls)

| arm | tally printed | shortfall |
|---|---|---|
| rows | `gate_rows=n exits=0,2,3` | max(0,3-n) + missing exits of {0,2,3} + refusal (exit 2/3) rows with no `RECEIPT_*` code in `stdout_contains` that the gate's CODES defines. A qualifying row: active, kind `gate`, argv `[python*, tools/receipt-revision-gate.py, ... --receipt ...]`, no `--selftest`. |
| executed | `held=h/n` | n-h. Each row via `registry-check.py --root LANE --rev REV --only NAME` (registry-check bytes at REV, clone under --work). |
| mutants | `mutants=k/3` | 3-k. Gate copy edited inside a `git clone --shared` of REV; each row that held on the unedited clone is rerun live (`--root CLONE --only`); killed = it now `differs` with an integer exit. `old` must occur exactly once in the gate at REV, else the mutant is unappliable and not killed. |
| skill_row | `skill_row=0|1` | 1-skill_row. Row in the `### Gate/probe registry` section (until the next heading of level <= 3, so the round-12 table and any `####` under it) naming `receipt-revision-gate.py`, whose `Verdict map` column cell carries whole tokens 0, 2 and 3. |
| codes | `codes_known=n/m` | m-n, +1 if the section holds no token. Tokens = distinct `RECEIPT_[A-Z_]+` inside `## Standing rules`; known = member of the gate's `CODES` parsed with `ast` from the REV source. |
| cell | `standing_cell=ok|WRONG:<x>` | 0/1. Counter builds a scratch repo (A, then B changing the one path in a `--paths` file), a receipt naming A, runs the gate (REV bytes) `--certified B --paths FILE --receipt R:verdict`; the row whose first cell starts `a verdict receipt names another revision` must carry exactly `{emitted code}` in its last cell. `<x>` = codes the cell carries, `none`, or `fixture` when the gate did not refuse with exactly one code. |

Verdict line and exit exactly as in the contract (`C2_R57: self=<sha12> rev=<rev12> gate_rows=... total=<n> C2_R57_PASS=<bool>`, exit 0 iff pass, 1 fail, 2 setup error: unresolvable REV or non-empty `--work`). No committed receipt is read; expected exits come from registry-check running the committed rows and from running the gate on a counter-built fixture. `--work` is left empty on exit; TMPDIR of every child points under it.

## Evidence (receipts in `T57W1ExecC2Counter-receipts/`)

- `base-run.stdout` / `.exit`: counter at base 5e356996: `gate_rows=0 exits=none held=0/0 mutants=0/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=11 C2_R57_PASS=false` (rows 6 = 3 missing rows + 3 missing exits; mutants 3; skill 1; cell 1). mutants=0/3 there is also because `mutants.json` is not committed at base; with no rows it is 0 anyway. The cell arm confirms the base defect by running the gate: it emits `RECEIPT_REV_CONTENT_DRIFT`, the SKILL cell says `RECEIPT_REV_MISMATCH`.
- `selftest.stdout` / `.exit`: `C2_R57_SELFTEST: 14/14 pass` (needs `--lane LANE --rev REV` when run from a stage dir; default lane is the lane holding the file, `parents[4]`). Fixtures: good (all arms 0) plus per-arm breakers: no exit-2 row, forged selftest-argv rows (gate_rows=0), wrong expected exit (held 2/3), exit-0-only row (0/3 mutants), no drift row (1/3), non-unique old string (2/3), no SKILL row, verdict map missing the 2, a `RECEIPT_BOGUS_CODE` token (codes 2/3), stale `RECEIPT_REV_MISMATCH` cell (WRONG), cell with no code (WRONG:none), a gate that emits MISMATCH (cell truth moves because the gate is run), a gate that does not refuse (WRONG:fixture).
- `target-sim-run.stdout`: end-to-end positive on a scratch clone of base with three registry rows (`python3 tools/receipt-revision-gate.py --lane . --certified HEAD|deadbeef... --paths fx/*.paths --receipt fx/r.txt:verdict`, receipt naming 5e356996, expects exits 0 / 3 + `RECEIPT_REV_CONTENT_DRIFT` / 2 + `RECEIPT_REV_UNRESOLVABLE`), the cell fixed to `RECEIPT_REV_CONTENT_DRIFT`, a gate row added to the round-12 table (`0 PASS; 2 unresolvable certified; 3 refused`) and mutants.json: `total=0 C2_R57_PASS=true`, M1 killed by the drift row (got 0), M2 by the drift row (got 3 with the wrong code), M3 by the unresolvable row (got 0). Row shape there is a working template for the row author.

## Risks / for the L1

- The SKILL gate row must sit under `### Gate/probe registry` (line ~1541 base; or a `####` below it before the next `##`/`###`); a row in `### Round-NN gate/probe registry` tables does not count (literal reading of the contract).
- The verdict-cell must carry exactly one code: `` `RECEIPT_REV_CONTENT_DRIFT` `` alone. The adjacent row's `(no --paths: RECEIPT_REV_MISMATCH)` style in the verdict row would fail equality. Other tokens elsewhere in Standing rules only need to be in CODES.
- Gate rows must run `python3 tools/receipt-revision-gate.py` (argv[0] python*, argv[1] that relative path) with `--receipt`, `--lane .`, and a certified rev that stays resolvable in the clone (`HEAD`); `registry-check --rev` rejects absolute live-fleet paths. A row's `--paths` surface must be stable across later commits (exit 0 row) / actually change between the receipt's rev and HEAD (drift row), or the row stops holding when the lane moves.
- The mutation arm runs rows live in a scratch clone (`--root`, registry-check prints its live-mode stderr warning; nothing in the lane is touched).
- Runtime: base run 0.4 s (no rows); target-sim 35 s wall; selftest ~3 min wall on the loaded host (14 full measures, each clones and runs rows ~10x). Host reported very high user-CPU for registry-check runs (28 min user in 35 s wall: the host was storm-loaded; not investigated).
- Not covered (contract `cannot_see`): that M1-M3 are the defects that matter.
- No tools installed. No lane or fleet file edited; no mutating git outside scratch clones.
