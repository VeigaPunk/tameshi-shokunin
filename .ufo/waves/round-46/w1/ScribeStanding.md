seat: ScribeStanding
item: drafted the round-46 "Standing self-assessment — re-stated at round 46" block (19 capability rows + depth/calibration/freshness) from the committed before-state, and listed every row whose stated value drifted or whose old evidence cell the counter cannot parse.

# Report — ScribeStanding (round 46, w1)

## What I produced

Deliverable beside this report: `.ufo/waves/round-46/w1/ScribeStanding.draft.md` (9397 bytes), a drop-in
markdown block whose two tables the C1 counter parses: `| Capability | What it can now do | Evidence pointer |
First-working round |` (19 rows, statement order of `statements.json`) and `| Axis | Score (0–10) | Evidence /
counting rule | Measured commit | Last-change round |` (depth, calibration, freshness).

Every capability evidence cell has the form `` `CMD` → `PRINTED LINE`, exit N[, tool sha256 `12hex`] `` with
U+2192. Every value in the draft was read from an observation file, never inferred:

- `.ufo/evidence/round-46/before/c1-at-freeze.stdout` — the counter's own per-statement `observed=` tuples at
  `745a583181648cfc7f9c1b476cd1be7dc68f7433` (this file exists, so no counter run was needed).
- `/tmp/r46/c1-before/obs-*.stdout` — 21 files for 22 statements; I re-applied `measure.py`'s `pick_line()` to
  each file with a copy of the counter imported from `/tmp` (`build.py`), and the re-derived value, exit and
  sha256 prefix agree with the `observed=` tuples in `before/c1-at-freeze.stdout` for all 21 statements that
  have a file of their own.
- Tool sha256 prefixes: `git -C LANE show REV:<sha_file>` piped through sha256, truncated to 12 hex.

### The 22 observed values (as written into the draft)

| statement | printed line | exit | tool sha256 `12` |
|---|---|---|---|
| sources-registry | `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | 0 | — |
| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass` | 0 | `a7d3f2dd7d47` |
| six-leg regression ledger | `REGRESSION: PASS (cases=9 passed=9` | 0 | — |
| repeated pristine-control gate | `SELFTEST: PASS (29 cases)` | 0 | `296fe566dc59` |
| six-leg content-disposition probe | `SELFTEST: PASS (19/19)` | 0 | `331529eadafe` |
| exposed witness provenance correction | `SELFTEST: PASS 39/39` | 0 | `df3390682a04` |
| effective expectation reconciliation | `SELFTEST: PASS (66/66)` | 0 | `39ee5c5effd9` |
| retained invocation-context gate | `SELFTEST: PASS (49/49)` | 0 | `7e4519d9a0ea` |
| hermetic env-differential probe | `ENVDIFF_SELFTEST: 9/9 pass` | 0 | `e8b47ab7cf23` |
| callback-authoritative wave accounting | `ACCOUNTING_SELFTEST: 8/8 pass` | 0 | `96b3038a77f8` |
| required-command-receipt-binding | `COMMAND_BINDING_SELFTEST: 44/44 pass` | 0 | `9230c68e53a5` |
| refusing-registry-replay | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 | `9fcd2dbba737` |
| mutation report interop | `MTE_SELFTEST: 17/17 pass` | 0 | `193ea6e32f89` |
| tally-audit-v2 runner audit | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | 0 | `7b11ba25aead` |
| tally-audit-v3 runner audit | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | 0 | `da8c1ef4b30c` |
| bounded ANSI-C code_view | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | 0 | `da8c1ef4b30c` |
| write-path-census-v2 | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` | 0 | `402285329588` |
| write-path census destination resolution | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` | 0 | `095924a7a165` |
| staged-id adoption guard | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` | 0 | `03a796c5726c` |
| depth (axis) | `9` | 0 | — |
| calibration (axis) | `6` | 0 | — |
| freshness (axis) | `9` | 0 | — |

## Rows whose old value differs from the observed value (old → new)

Only two rows had a *parseable* old value, and both differ:

| row | SCORECARD.md line at REV | old (parsed claim) | new (observed) |
|---|---|---|---|
| six-leg regression ledger | 1516 | `REGRESSION: PASS (cases=9 passed=9 …)`, exit 0 | `REGRESSION: PASS (cases=9 passed=9`, exit 0 |
| calibration (axis) | 1537 | score `8` | score `6` |

The regression-ledger delta is the ellipsis `…` inside the claimed printed line: the frozen regex
`^(REGRESSION: \w+ \(cases=\d+ passed=\d+)` stops at `passed=9`, so the claimed string can never equal the
observed one. The calibration delta is a genuine stale score: the round-21 cold-read monitor printed 6 at
`745a5831…` and `.ufo/evidence/round-46/before/no-harm-at-base.stdout` independently prints
`NOHARM coldread score=6 box3_full_page=False ok`, while the standing row has carried 8 since round 29.

Two rows with *unparseable* old cells also carry a visibly stale figure, flagged here rather than counted
above:

| row | SCORECARD.md line at REV | stale visible figure | observed |
|---|---|---|---|
| tally-audit-v3 runner audit | 1698 | tool `tools/tally-audit-v3.py` @ `6188db16…` (round-35 receipt) | tool sha256 `da8c1ef4b30c` at REV |
| sources-registry | 1609 | "99 rows at round 35" from a `grep -cE` row pattern over `corpus/SOURCES.md` (the pattern itself contains pipe alternation) | census prints `rows=117` (different command; not a like-for-like value diff) |

## Rows whose old cell could not be parsed (18 capability rows + freshness)

`claim_of()` returns `None` for these, so the counter scored them `UNPARSED`. For 15 of them the value and
exit a reader can see in the old cell agree with the observed value; the failure is format, not content.

| row | SCORECARD.md line at REV | why unparsed | old evidence cell (verbatim, truncated where long) |
|---|---|---|---|
| sources-registry | 1609 | value printed *before* `exit`, no `→ `value`, exit N`` shape; cell also contains an unescaped pipe character inside a backticked regex, so `cells_of` splits the row into 6 cells | `` `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; row count from the re-derivable command `grep -cE …` → 99 rows at round 35 … `` |
| mutation sweep runner | 1515 | value+exit correct, no `, tool sha256 `12hex`` (statement pins `sha_file`, so `CLAIM_SHA` is required) | `` `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 `` |
| repeated pristine-control gate | 1517 | value not backticked and missing the printed `SELFTEST:` prefix; no sha | `` `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 `` |
| six-leg content-disposition probe | 1518 | no `, exit N`, no sha, value garbled | `` `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 `` |
| exposed witness provenance correction | 1519 | no `→`, no `, exit N`, no sha | `` `python3 tools/witness-metadata.py --selftest`: metadata selftest39/39 PASS0 `` |
| effective expectation reconciliation | 1520 | no `→`, no `, exit N`, no sha | `` `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 `` |
| retained invocation-context gate | 1521 | `exit0` then prose, no sha | `` `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…` → exit0, copied-source CLI selftest49/49 `` |
| hermetic env-differential probe | 1522 | value not in the `→ `…`, exit N`` shape; no sha | `` `python3 tools/env-diff.py --selftest` actual9/9 (`ENVDIFF_SELFTEST: 9/9 pass`) `` |
| callback-authoritative wave accounting | 1523 | no `, exit N`, no sha | `` `python3 tools/wave-accounting.py --selftest` → frozen counter8/8 (`ACCOUNTING_SELFTEST: 8/8 pass`; extra cases `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`) `` |
| required-command-receipt-binding | 1524 | prose after `exit 0` where the sha must follow; no sha | `` `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0 (not a C1 statement) `` |
| refusing-registry-replay | 1525 | same | `` `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 (not a C1 statement) `` |
| mutation report interop | 1526 | `exit 0 at round 33 (…)` — no sha | `` `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0 at round 33 (jsonschema 4.25.1 installed via uv; …) `` |
| tally-audit-v2 runner audit | 1657 | receipt prose, no `→ `value`, exit N``; sha as `7b11ba25…8d10` (8+4 hex, not 12 contiguous) | deciding-run receipt `C1_R33: … C1_R33_PASS=true` at `c17e593b`, counter `.ufo/evidence/round-33/c1/c1-measure.py`, tool `tools/tally-audit-v2.py` @ `7b11ba25…8d10` |
| tally-audit-v3 runner audit | 1698 | receipt prose; sha `6188db16…` and stale (see above) | deciding receipt `C1_R35: … C1_R35_PASS=true` at `34fa5b0`, counter `.ufo/evidence/round-35/c1/c1-measure.py` @ `d360a159…`, tool `tools/tally-audit-v3.py` @ `6188db16…` |
| bounded ANSI-C code_view | 1809 | receipts only, no command, no value, no exit | `.ufo/evidence/round-37/code-view/after.stdout` (2/2), `.ufo/evidence/round-37/tool-selftest-after.stdout` (35/35), `.ufo/evidence/round-37/c2-repin-after.stdout` (frozen r36 predicate PASS), S104 |
| write-path-census-v2 | 1889 | receipt prose; sha as full 64 hex | deciding receipt `C1_R40: ... C1_R40_PASS=true` at `5641ed84`, … tool `tools/write-path-census-v2.py` @ `4022853295882c5a…` |
| write-path census destination resolution | 1920 | receipt prose; sha as full 64 hex | deciding receipt `C2_R41: … C2_R41_PASS=true` at the round-41 measured commit, … tool `tools/write-path-census-v3.py` @ `095924a7a165be96…` |
| staged-id adoption guard | 2074 | receipt prose; sha as full 64 hex | deciding receipt `C3_R43: … C3_R43_PASS=true` at the round-43 measured commit, … tool `tools/staged-id-guard.py` @ `03a796c5726c3036…` |
| freshness (axis) | — (row absent) | no row named `freshness` in any table `last_rows()` recognises; the only freshness rows sit in the `Axis / trend` verdict tables (e.g. line 680, `freshness / adjacency`), whose header[1] does not start with `Score` | absent |

The 12-hex prefixes quoted for the last three receipt rows agree with the observed prefixes
(`402285329588`, `095924a7a165`, `03a796c5726c`); the tally-v2 first-8 `7b11ba25` agrees with `7b11ba25aead`.

## Gates I ran (parse-level, not the counter)

| command | result |
|---|---|
| `python3 /tmp/tameshi-r46-ScribeStanding/probe.py` (`git -C LANE show REV:SCORECARD.md`, then `last_rows`) | 21 standing rows at REV: 19 `cap` + `axis/depth` + `axis/calibration`; no `freshness` row |
| `python3 /tmp/tameshi-r46-ScribeStanding/build.py` (`pick_line` over `/tmp/r46/c1-before/obs-*.stdout`, `git show` sha256) | values, exits and sha prefixes reproduce the `observed=` tuples in `before/c1-at-freeze.stdout` |
| `python3 /tmp/tameshi-r46-ScribeStanding/validate.py` (`last_rows` + `claim_of` on the deliverable) | 22 rows parsed from the draft; 22/22 claimed tuple == observed tuple; 0 failures |
| same script, `REV SCORECARD.md` + `"\n"` + draft | 22 distinct keys, 22/22 claimed == observed — the block wins `last_rows` only when appended after every existing table |
| `diff -u draft.md <deliverable>` | identical |

I did **not** run `measure.py` in any mode (not `--selftest`, not against a rev): the deciding run is the
L1's, and the before-state file already carries the observations this draft needs. I also did not run the
round-21 cold-read monitor or the round-45 freshness counter; the axis values come from the counter's printed
observations plus `before/no-harm-at-base.stdout`.

## Findings for the L1

1. **The calibration axis row is the C1 defect.** `8` stated, `6` printed at REV, and the no-harm receipt
   agrees with `6`. This is the one axis-value mismatch; the draft states 6 and records the correction in the
   rule cell (`29 (restored 6 → 8); held 30; restated at 46 (8 → 6, observed)`).
2. **The regression-ledger mismatch is a typographic ellipsis**, not a wrong observation: the claimed line
   carries `…` inside the backticks. Dropping it (as the draft does) makes the row match without touching the
   statement.
3. **15 of 19 capability rows were correct but unparseable**, essentially all because a `sha_file` statement
   needs `, tool sha256 `12hex`` and the standing cells omit it; four more carry the value outside the
   `→ `value`, exit N`` shape. The draft's format fixes all of them without changing any What/First cell.
4. **`sources-registry`'s row has an unescaped `|`** inside a backticked `grep -cE '^| S[0-9]{3} |'`. That
   splits the row into 6 cells, so the counter reads the evidence from a fragment. The draft's evidence cell
   contains no `|`; if the L1 wants the grep mention back it must be escaped in a way `cells_of` can still
   slice (i.e. not at all — `cells_of` splits on the raw byte).
5. **`tally-audit-v3`'s stated tool digest is stale** (`6188db16…` from round 35 vs `da8c1ef4b30c` at REV).
   The draft states the observed digest.
6. **`bounded ANSI-C code_view`'s frozen statement runs the tally-audit-v3 selftest**, so its evidence pointer
   cannot evidence the What cell (code_view). The statement is frozen, so the draft reproduces the observed
   line; this is a semantic defect in the standing row that C1 cannot see.
7. **`freshness` has no standing axis row at all** — only `freshness / adjacency` verdict rows in
   `Axis / trend` tables and prose at line 2141. The draft adds `| freshness | 9 | …` with the round-45 rule
   `floor(10 * fresh / 73)` (fresh=71 → 9) and last-change round 45.
8. **Placement matters.** `last_rows()` keeps the *last* row per (kind, id). The round-31 axis table at
   SCORECARD.md:1534 is the last axis table and the standing capability table's last row is at 2074, so the
   round-46 block must be appended after both. Verified by the merged parse above.
9. **`obs-calibration.stdout` is not re-parseable**: the counter writes `out[-200000:]`, which cuts the JSON
   mid-document, and `grep -c calibration_restraint_score` on that file returns 0. The `6` rests on the
   counter's printed line in `before/c1-at-freeze.stdout` and on the no-harm receipt line, both of which I
   quote.
10. **`bounded ANSI-C code_view` has no observation file of its own.** The counter caches by
    `(argv, cwd, obs, sha_file, kind)` and this statement shares that key with `tally-audit-v3`, so only
    `obs-tally-audit-v3-runner-audit.stdout` exists (21 files for 22 statements). The draft's value for it is
    the shared observation, confirmed by `before/c1-at-freeze.stdout`.
11. The draft's axis **Measured commit** cells carry `745a583181648cfc7f9c1b476cd1be7dc68f7433`. If the
    deciding run lands at a different content revision, those three cells must be re-pointed to it.

## Touched surfaces

- Written: `.ufo/waves/round-46/w1/ScribeStanding.draft.md` (deliverable) and this report
  `.ufo/waves/round-46/w1/ScribeStanding.md`. Nothing else in the lane was written; no git/jj command that
  mutates state was run (only `git show` / `git -C LANE show` reads). `/home/vgpnk/Projects/shokuknow` was not
  touched. Scratch: `/tmp/tameshi-r46-ScribeStanding/` (`measure_copy.py`, `probe.py`, `build.py`, `gen.py`,
  `mk.py`, `validate.py`, `draft.md`, `data.json`, `rows.json`, `rows_out.json`, `sc.md`).

## Out of scope / not done

- No counter run, no verdict, no SCORECARD.md edit (the L1 inserts the block), no C2/C3 work.
- Tooling: nothing installed or upgraded.

## Artifact paths

- Deliverable: `.ufo/waves/round-46/w1/ScribeStanding.draft.md`
- Observations: `.ufo/evidence/round-46/before/c1-at-freeze.stdout`,
  `.ufo/evidence/round-46/before/no-harm-at-base.stdout`, `/tmp/r46/c1-before/obs-*.stdout`
- Statement list: `.ufo/evidence/round-46/calibration/statements.json`; counter
  `.ufo/evidence/round-46/calibration/measure.py` (imported from a copy, never edited)
- Scratch: `/tmp/tameshi-r46-ScribeStanding/`
