# FalsifyJSON — wave 2: duplicate-key fixtures vs the delivered parser

Seat: `TameshiR15.FalsifyJSON` (critic, leaf). Static source review only. I executed nothing: no gate, no selftest, no fixture, no Python probe. Every behaviour stated below comes from reading the source and is not an observed run.

Tools installed or updated: none.

## Source read

`tools/context-capture.py` (read snapshot tag `472A`, 2116 lines), these ranges:

- `:308-327` `_no_duplicate_keys`, `parse_json_strict`
- `:459-475` `validate_top`
- `:756-762` `embedded_json`
- `:1186-1216` `validate_expected`, `load_expected`
- `:1298-1344` `run_check`
- `:1611-1682` `SelftestHarness.check_case`
- `:1728-2002` `run_selftest_cases`
- `:2083-2112` `main`

Context for the requirement: `.ufo/waves/round-15/w1/SpecTamper.md:163,224-226`, `ReviewJSON.md:54` (J9), `AttackJSON.md:56-80`, `SpecJSON.md:217`, and the round-12 precedent `.ufo/evidence/round-12/SnapshotReview/probe-output.txt:10` (row F: "parsers disagree on the pin; strict must refuse duplicates").

## Axes

- **Parse reach:** does the duplicate fixture actually reach the strict parser, or does it stop at the digest gate first?
- **Discrimination:** if the hook were removed, would the fixture's pinned ID change?
- **Coverage of claimed parsers:** the receipt parser and the expected-pin parser.

## Receipt side — bounded agreement (no hole)

The `duplicate-key` case is at `:1887-1891`. Its receipt bytes are `{"schema": R, "schema": R}`. It passes no `expected_override`, so `check_case` pins `receipt_sha256 = sha256(receipt_bytes)` (`:1624-1630`). `run_check` therefore clears the digest gate (`:1323-1324`) and reaches `parse_json_strict(raw, "receipt_json_invalid", …)` (`:1335`). The hook raises `ValueError` there, which becomes `receipt_json_invalid`/2.

The fixture does discriminate. Without the hook, the bytes would parse to `{"schema": R}`. That has no `status`, so `validate_top` (`:463-467`) would raise `receipt_structure_invalid`, which is a different pinned ID. Removing the hook from the receipt path is therefore caught. This answers the AttackJSON B trap (digest masking) for the receipt.

## Expected-pin side — one falsifiable hole

**Claim at risk:** the expected pin is parsed without ambiguity. W1 requirement: SpecTamper R5 (`:224-226`), "else a second key shadows the pin"; ReviewJSON J9. This is the round-12 F lesson.

**Source state:** the code is correct today. `load_expected` uses `parse_json_strict(raw, "expected_invalid", …)` (`:1215`).

**Gap:** no selftest case pins that behaviour. The harness cannot even express it:

- `check_case` always writes the expected file with `json.dump(expected_document, …)` (`:1633-1636`).
- A Python dict cannot carry a duplicate key.
- There is no `expected_bytes` parameter.

**Mutant that survives the whole selftest:** M replaces `:1215` with `document = json.loads(raw)` (last value wins). Each expected-touching case, read against M:

| Case | Lines | Outcome under M | Why |
|---|---|---|---|
| `expected-missing` | `:1916` | unchanged | fails in `read_regular` first |
| `expected-invalid` | `:1920` | unchanged | schema check |
| `expected-digest-invalid` | `:1983` | unchanged | `require_hex` |
| `snapshot-tampered` | `:1907` | unchanged | well-formed pin |
| `expected-verdict-mismatch` | `:1929` | unchanged | well-formed pin |
| every other `check_case` | — | unchanged | the pin comes from `json.dump`, so it has no duplicates |

So the selftest stays fully green under M.

**Concrete CLI counterexample** (not executed). Take a clean receipt `R` and any other receipt `R'`. Use this expected file:

```json
{"schema":"tameshi-context-expected-v1","receipt_sha256":"<sha256(R')>","id":"context_consistent","exit":0,"receipt_sha256":"<sha256(R)>"}
```

Invoke:

```
context-capture.py --check --receipt R --expected E --json
```

- **Delivered code:** `expected_invalid`/2.
- **Under M:** `context_consistent`/0. The digest matches `R`, while a first-wins reader of the pin sees `R'` pinned.

This is exactly the "first-pin=good → BAD" disagreement in round-12 row F. It is a false clean that the selftest cannot detect.

**Impacted axes:** coverage of claimed parsers (expected pin); integrity of the pin.

**Classification:** fixable test-pinning defect, not a tradeoff. The source needs no change.

## Smallest safe correction

1. Add an optional `expected_bytes=None` to `check_case`. When it is set, write those bytes verbatim instead of calling `json.dump`.
2. Add one case, `expected-duplicate-key`:
   - receipt `clean`;
   - `expected_bytes` = the counterexample above, with `<sha256(R)>` set to `sha256(clean bytes)` as the **last** `receipt_sha256` and `"0"*64` as the first;
   - pinned result: `expected_invalid`, exit 2.

Under M, the last-wins digest matches, the verdict is `context_consistent`/0, and the case fails. So M is killed.

Nothing else is required. Out of scope here: nested receipt duplicates (SpecJSON J4) and duplicate rejection in `runs.*.stdout` (`embedded_json`, `:756-762`). Both are real paths with no dedicated case, but this seat reports one hole only and does not inflate scope.
