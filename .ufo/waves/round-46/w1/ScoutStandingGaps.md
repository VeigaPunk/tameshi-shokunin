seat: ScoutStandingGaps
item: Standing capability gaps and stale selftest rows

## Scope and method

Read the round-46 contract first. Ran selftests in a scratch clone checked out at `745a583181648cfc7f9c1b476cd1be7dc68f7433`; scratch files stayed under `/tmp/tameshi-r46-ScoutStandingGaps/`. Also ran the C1 counter at that frozen revision into scratch. Its output is an observation, not a deciding verdict. I skipped standalone runs of the two assigned heavy commands (`tally-audit-v3.py --selftest` and `mutate-and-run.sh --regression`); the scratch counter invoked both as frozen statements. No tools were installed.

The standing capability set is the union of proper `| Capability |` tables: 13 rows in the round-31 restatement (SCORECARD.md:1512-1526), plus round-34/35/37/40/41/43 additions (1655, 1696, 1807, 1887, 1918, 2072). The counter’s `last_rows` logic takes the last data row per id in such tables.

## Listed capabilities: frozen-command observations

These are the tools/capabilities already represented by a standing capability row. “C1 form” refers to the frozen counter's required `→ \`PRINTED LINE\`, exit N` and, where a tool is pinned, `, tool sha256 \`12hex\`` syntax. A row can have a currently correct tally and still be unparsed by C1.

| Status | Tool / capability; standing row | Frozen command → observed printed tally (exit) |
|---|---|---|
| listed; C1 unparsed | `.ufo/evidence/kaika-round-1/sources-census-v2.sh` / sources-registry (effective proper-table row SCORECARD.md:1609) | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` (0) |
| listed; C1 unparsed | `tools/mutate-and-run.sh` / mutation sweep runner (SCORECARD.md:1515) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass` (0); tool SHA prefix `a7d3f2dd7d47` |
| listed; stale literal / C1 mismatch | `tools/mutate-and-run.sh` / six-leg regression ledger (SCORECARD.md:1516) | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9` (0; counter capture). Full line: `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| listed; C1 unparsed | `tools/repeat-control.py` / repeated pristine-control gate (SCORECARD.md:1517) | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)` (0); SHA `296fe566dc59` |
| listed; C1 unparsed | `tools/pin-disposition.py` / six-leg content-disposition probe (SCORECARD.md:1518) | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)` (0); SHA `331529eadafe` |
| listed; C1 unparsed | `tools/witness-metadata.py` / exposed witness provenance correction (SCORECARD.md:1519) | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39` (0); SHA `df3390682a04` |
| listed; C1 unparsed | `tools/evidence-disposition.py` / effective expectation reconciliation (SCORECARD.md:1520) | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)` (0); SHA `39ee5c5effd9` |
| listed; C1 unparsed | `.ufo/evidence/round-15/verify.py` / retained invocation-context gate (SCORECARD.md:1521) | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → captured `SELFTEST: PASS (49/49)` (0); SHA `7e4519d9a0ea` |
| listed; C1 unparsed | `tools/env-diff.py` / hermetic env-differential probe (SCORECARD.md:1522) | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass` (0); SHA `e8b47ab7cf23` |
| listed; C1 unparsed | `tools/wave-accounting.py` / callback-authoritative wave accounting (SCORECARD.md:1523) | `python3 tools/wave-accounting.py --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`; extra tally `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass` (0); SHA `96b3038a77f8` |
| listed; C1 unparsed | `tools/command-binding.py` / required-command-receipt-binding (SCORECARD.md:1524) | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass` (0); SHA `9230c68e53a5` |
| listed; C1 unparsed | `tools/registry-replay.py` / refusing-registry-replay (SCORECARD.md:1525) | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass` (0); SHA `9fcd2dbba737` |
| listed; C1 unparsed | `tools/mte-interop.py` / mutation report interop (SCORECARD.md:1526) | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass` (0); SHA `193ea6e32f89` |
| listed; C1 unparsed | `tools/tally-audit-v2.py` / tally-audit-v2 runner audit (SCORECARD.md:1657) | `python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` (0); SHA `7b11ba25aead` |
| listed; stale pin; C1 unparsed | `tools/tally-audit-v3.py` / tally-audit-v3 runner audit (SCORECARD.md:1698) | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` (0; observed via scratch counter, not standalone); SHA `da8c1ef4b30c` |
| listed; C1 unparsed | `tools/tally-audit-v3.py` / bounded ANSI-C code_view (SCORECARD.md:1809) | Same frozen selftest → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` (0; scratch counter observation); SHA `da8c1ef4b30c` |
| listed; C1 unparsed | `tools/write-path-census-v2.py` / write-path-census-v2 (SCORECARD.md:1889) | `python3 tools/write-path-census-v2.py --selftest` → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` (0); SHA `402285329588` |
| listed; C1 unparsed | `tools/write-path-census-v3.py` / write-path census destination resolution (SCORECARD.md:1920) | `python3 tools/write-path-census-v3.py --selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` (0); SHA `095924a7a165` |
| listed; C1 unparsed | `tools/staged-id-guard.py` / staged-id adoption guard (SCORECARD.md:2074) | `python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` (0); SHA `03a796c5726c` |

The capability row for `six-leg regression ledger` is the only cap row the counter parsed; its literal mismatch is due to the ellipsis. The other 18 cap statements were unparsed: 17 pin a tool but their effective row lacks the required 12-hex SHA suffix; sources-registry uses a different evidence shape. Total scratch C1 observation: `mismatches=2 unparsed=19 unobservable=0 total=21` (not a verdict).

## Unlisted tools with a passing selftest

These tools run but have no standing `| Capability |` row. The round evidence is the demonstration/admission context; explicit no-row decisions are identified rather than treated as accidental omissions.

| Status | Tool / capability | Selftest command → printed tally (exit) | Round evidence / SCORECARD disposition |
|---|---|---|---|
| unlisted | `tools/bash-witness-study.py` | `python3 tools/bash-witness-study.py selftest` → `WITNESS_SELFTEST: 51/51 pass` (0) | Round 12 C2 “bash witness detail” (SCORECARD.md:303-304; round-12-verifier-spotcheck.md:95-96); later mention at SCORECARD.md:645, no capability row. |
| unlisted | `tools/context-capture.py` | `python3 tools/context-capture.py --selftest` → `SELFTEST: PASS (49/49)` (0) | Round 15 registered command (SCORECARD.md:508; round-15.md:4). Standing “retained invocation-context gate” instead names `.ufo/evidence/round-15/verify.py` (SCORECARD.md:1521). |
| unlisted; explicit no-row decision | `tools/receipt-measure.py` | `python3 tools/receipt-measure.py --selftest` → `RECEIPT_MEASURE_SELFTEST: 10/10 pass` (0) | Round 20 command (SCORECARD.md:784); no new capability-table row (778-780). |
| unlisted; explicit no-row decision | `tools/receipt-window.py` | `python3 tools/receipt-window.py --selftest` → `RECEIPT_WINDOW_SELFTEST: 20/20 pass` (0) | Round 20 receipt-window enforcement (SCORECARD.md:773-784); no row (778-780). Filename itself is absent from SCORECARD.md. |
| unlisted | `tools/registry-check.py` | `python3 tools/registry-check.py --selftest` → `SELFTEST: PASS (51 cases)` (0) | Round 17 registered-outcomes monitor (SCORECARD.md:611, 660; round-17.md:54); no capability row. |
| unlisted; sibling-dependent | `tools/round21-measure.py` | `python3 tools/round21-measure.py --selftest` → `ROUND21_MEASURE_SELFTEST: 13/13 pass` (0 with sibling lane repos linked) | Round 21 tool (commit `370f2df`); no SCORECARD filename mention. A bare clone fails without sibling repositories; not standalone/hermetic. |
| unlisted | `tools/trace-inputs.py` | `python3 tools/trace-inputs.py --selftest` → `SELFTEST: 30/30` (0) | Added as round-18 trace collector (`58e5d53`); no SCORECARD filename mention. Later use appears in round-30.md:95 and round-31.md:56. |
| unlisted | `tools/wave-route-mix.py` | `python3 tools/wave-route-mix.py --selftest` → `ROUTEMIX_SELFTEST: 8/8 pass` (0) | Round 21 mention at SCORECARD.md:879; no capability row. |
| unlisted; explicit no-row decision | `tools/golden-verdict.py` | `python3 tools/golden-verdict.py --selftest` → `GOLDEN_VERDICT_SELFTEST: 3/3 pass` (0) | Round 38; SCORECARD.md:1840-1841 says no row because it is a C2 instrument, not a repertoire capability. |
| unlisted; predicate missed | `tools/write-path-census-v4.py` | `python3 tools/write-path-census-v4.py --selftest` → `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0` (0) | Round 42 C2 (SCORECARD.md:2006); verifier spotcheck confirms run (round-42-verifier-spotcheck.md:52), but declared claim missed (SCORECARD.md:2038-2045), so no row was admitted. |
| unlisted; explicit no-row decision | `tools/tally-audit.py` | `python3 tools/tally-audit.py --selftest` → `TALLY_AUDIT_SELFTEST: 11/11 pass` (0) | Round 32, SCORECARD.md:1588-1590 says no row because the tool did not meet its frozen predicate. Later v2/v3 have rows. |
| unlisted; explicit no-row decision | `tools/wave-parent-settle.py` | `python3 tools/wave-parent-settle.py --selftest` → `WAVE_PARENT_SELFTEST: 3/3 pass` (0) | Round 39; SCORECARD.md:1866 explicitly says it is not a capability-table claim. |
| unlisted; explicit no-row decision | `tools/write-path-census.py` (v1) | `python3 tools/write-path-census.py --selftest` → `WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1` (0) | Round 39; SCORECARD.md:1866 says the census tool is an instrument, not a new repertoire capability. v2/v3 have rows. |

`tools/registry.json` is data, not a tool.

## Stale or missing standing rows

| Status | Row / evidence | Observation at freeze | Finding |
|---|---|---|---|
| stale value; table structure also unreadable | sources-registry, effective proper-table row SCORECARD.md:1609 | Census `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0 | Effective row says 99 rows at round 35. Later source-registry lines at 1851, 1993, 2020, 2081, 2146, 2164 are headerless single-row blocks, not data rows under a `Capability` header, so the counter ignores them. Latest (2164) says 117, but effective proper-table row remains 1609. |
| stale literal (counter mismatch) | six-leg regression ledger, SCORECARD.md:1516 | Counter observed `REGRESSION: PASS (cases=9 passed=9`; full output `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` | Standing literal includes `…` in `REGRESSION: PASS (cases=9 passed=9 …)`; counter reports MISMATCH. |
| stale tool pin | tally-audit-v3 runner audit, SCORECARD.md:1698 | Freeze tool SHA prefix `da8c1ef4b30c` | Row pins round-35 bytes `6188db16…`; tool changed in round 37 (`ae9b771`). Round-37 row at 1809 is the later evidence. |
| stale axis value | calibration axis, SCORECARD.md:1537 | Cold-read monitor: `calibration_restraint_score: 6` | Standing row says 8; round-36 prose records 8→6 (SCORECARD.md:1703). |
| missing axis row | freshness axis | Round-45 counter: `fresh=71 score=9`, exit 0 | No freshness data row occurs in either `Axis | Score ...` table (SCORECARD.md:64 and 1534). Round-44/45 state the axis/score in prose only. |

## Admission sweep

The round-46 contract freezes 19 existing capability ids; additional ids do not change those statements. Rounds 44-45 add no proper capability table; last proper admission table is round 43 at SCORECARD.md:2072. Explicit no-row decisions above are reported as such, not silently reclassified as repertoire. No row is proposed for anything not observed running.
