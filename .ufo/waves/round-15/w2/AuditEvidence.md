# AuditEvidence — round 15 integration artifacts: runnable command and evidence gaps

Seat: `TameshiR15.AuditEvidence` (leaf, static review). Lane: tameshi-shokunin. Target: inventory actual runnable command and evidence gaps; report missing evidence honestly; absent-yet runtime receipts are not defects.

## Scope and method

- **Static only.** No selftest, check, measure, census, build, test, formatter, or sibling gate was executed. Only read-only operations were used: `read`, `grep`/`awk`/`sed`, `sha256sum`, `wc`, `stat`, `ls`, `git status --porcelain`. Byte-digest comparisons are digests of retained bytes, not gate runs.
- **Moving target.** `tools/context-capture.py` and `SKILL.md` changed during this audit. Observed snapshots, in order: `context-capture.py` 2116 lines (read at snapshot tag `#472A`); 2123 lines (`#6F31`); 2129 lines, sha256 `95f20467…`, mtime 05:22:15 (`#5BA8`); an intermediate sha `a2e8cfa2…` that I hashed but did not re-read in full; and finally 2178 lines, sha256 `e55f8b06223824a7682a89c6dcf50417e6385f18a69fa7f72d4075120957fcb1` (`#FE96`). **The final audited snapshot is `e55f8b06…`.** Findings about the earlier snapshots were re-checked against `e55f8b06…` where they still apply. Any L1 run must pin the sha256 it actually runs.
- **Installs or updates:** none.
- **Sibling gates executed:** none.
- **Writes:** this report only. Coordination message sent to `agent://TameshiR15` (one critical defect and one contract defect).

## Exact sources read

- `AGENTS.md`; `corpus/lessons/round-14-verifier-spotcheck.md` (Routed defects, item 5); `corpus/lessons/round-15.md` (Gate, Mistakes, Admit criteria, Dispatch).
- `tools/context-capture.py` at `e55f8b06…`: docstring 1–120; constants 121–250; `USAGE` and `KNOWN_ARGUMENTS` 251–280; validators 459–808; recomputation 808–1154; `check_receipt`, `expected` pin, `apply_expected`, `run_check` 1155–1350; fixtures and `SelftestHarness` 1350–1786 (`check_case` 1654–1741, `usage_case`, `finish`); `run_selftest_cases` 1786–2061; `run_selftest`, `parse_argv`, `main` 2063–2178.
- `.ufo/evidence/round-14/capture-context.py` (archived): `OUTPUT_REL` line 58; `write_receipt` 583–602; `main` 605–647; `decide` 553–580.
- `SKILL.md` round-15 section (about lines 1609–1691, including the round-15 registry row at 1680). Read at `29689eb37a7865c7dbd2f67325e257d3aaeab152ee5934ea19d86d5a413723a9`; the archived-script wording (about line 1592) changed during the audit, see F6.
- `LOG.md` round-15 entry (about 927–960); `corpus/QUALITY.md` criterion 17 (about 75–80); `corpus/SOURCES.md` rows S049–S051 (lines 58–60); `corpus/README.md` (about 196–203).
- `.ufo/evidence/round-15/`: `claims.json`, `integration-decisions.json`, `sources-before.json`, `measure.py` (lines 1–340).
- `.ufo/evidence/round-14/context-receipt.json`, `context-missing-env.json`.
- `scripts/sources-census.sh` existence and mode.
- `git status --porcelain` (read-only): modified `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `tools/context-capture.py`; untracked `.ufo/evidence/round-15/`, `.ufo/waves/round-15/`, `corpus/lessons/round-15.md`. Historical round-12..14 paths are not modified.

## Digest pins observed (byte reads, not gate runs)

| Artifact | sha256 observed | Pinned where | Agreement |
|---|---|---|---|
| `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` | `FROZEN_RECEIPT_SHA256`; SKILL row | equal |
| receipt `tool_sha256` field | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | `FROZEN_TOOL_SHA256` | equal |
| `.ufo/evidence/round-14/capture-context.py` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | receipt tool field | equal (historical bytes intact) |
| `.ufo/evidence/round-14/context-missing-env.json` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` | SKILL row; registry expected inline | equal |

Static content of the negative fixture: no `injected_env` key anywhere in the file; top-level `status` `"ok"` and `exit` `0`; `env_delta_matches_declared` `true`. Static reading of `recompute_environment` and `verify_recorded_verdict` predicts the primary finding `missing_injected_environment` with a secondary `receipt_verdict_mismatch`, exit 1. This agrees with the registry pin. It is **not** a run result.

Round-15 `measure.py` and `claims.json` cite `sources-census.sh`, S049–S051, QUALITY17, and LOG. Verbatim check: `tools/context-capture.py` docstring line 12 contains "writes nothing; the only writes are --selftest fixtures under mkdtemp.", matching S051 and the lesson. S049 quote and word count were not re-fetched; no network was used.

## Findings

Severity: **critical** blocks an acceptance criterion; **high** blocks evidence integrity; **medium** is an unpinned or untested contract; **low** is documentation or measurement wording.

### F1 — critical: selftest harness asserts `verdict_matches_expected` for every case, and five cases fail by static trace

- Evidence: `check_case` signature (around line 1659) has `expected_match=True`. Lines 1718–1725 run `ok = ok and observed_match is expected_match` when `expected_match is not None`, and for `True` also require `"expected_verdict_mismatch" not in ids`. No call in the file passes `expected_match`; `grep` shows only the signature and the body.
- Counterexample (static trace, not executed): `apply_expected` (1314) sets `verdict_matches_expected` to `False` when the pinned id or exit differs from the recomputed verdict, and `make_result` sets it to `None` when no expected pin was loaded.
  - `snapshot-tampered`: pin `context_consistent`/0 against emitted `snapshot_tampered`/2 → `False` → fails.
  - `expected-verdict-mismatch`: pin `comparison_mismatch`/1 against emitted clean → `False` → fails.
  - `expected-missing`, `expected-invalid`, `expected-digest-invalid`: no pin loaded → `None` → fails.
- Consequence: the selftest would print `SELFTEST: FAIL (5/38 failed …)` on this snapshot. The id/exit pairs in those cases still agree with the emitted primary, so the failure is the new assertion alone.
- Fix suggestion (for the executor): `expected_match=False` for `snapshot-tampered` and `expected-verdict-mismatch`; `expected_match=None` for the three no-pin cases. The `expected_verdict_mismatch` in-ids branch then gains real coverage.
- Status: reported to `TameshiR15`.

### F2 — medium: `-h`/`--help` exit 0 contradicts the documented clean exit 0

- Evidence: `parse_argv` (2084–2085) returns `{"help": True}` for `["-h"]` or `["--help"]`; `main` (2156–2158) prints `USAGE` and returns 0. The docstring exit map (line ~285), `USAGE`, and SKILL row all define exit 0 as "clean retained receipt (`context_consistent`)".
- Counterexample: `python3 tools/context-capture.py -h; echo $?` → 0, no `CONTEXT:` line. A script treating 0 as clean gets a false clean.
- Coverage: no selftest case; SKILL does not mention help.
- Status: reported to `TameshiR15`. Fix is either a non-clean code for help or an explicit registry note.

### F3 — medium: pin id mismatch at exit 1 is indistinguishable from a matched exit-1 pin by exit code, and untested

- Evidence: `apply_expected` else-branch (around line 1316–1320) collects `expected_verdict_mismatch` but leaves `exit` at 1 when the recomputed exit is 1. The docstring states that an exit-1 pin matches the retained mismatch and exits 1.
- Counterexample (static): negative fixture with pin `comparison_mismatch`/1 → exit 1, primary id `missing_injected_environment`, findings contains `expected_verdict_mismatch`. Exit-code-only consumers see the same exit 1 as the matched pin `missing_injected_environment`/1.
- Coverage: no selftest case passes `expected_match=False` for this path (see F1).
- Status: design observation plus missing coverage; not a separate message.

### F4 — medium: nine documented stable finding IDs have no selftest pin

Documented in the docstring; no `check_case` pins the literal pair (checked against `run_selftest_cases` only):

`environment_delta_mismatch`, `environment_baseline_git_dir`, `run_argv_mismatch`, `run_cwd_mismatch`, `run_env_delta_mismatch`, `tool_declaration_mismatch` (frozen only, not reachable from fixtures), `receipt_unreadable`, `expected_unreadable`, `internal_error`.

Pinned by selftest: 19 of 28 documented IDs (including `context_consistent` and `usage_error`). The lesson's admit criterion is "literal exit and stable finding pairs"; the unpinned nine are not asserted by the selftest. Also not covered: `KNOWN_ARGUMENTS` refusal (lines 2114–2117), `given twice`/`needs a value` branches, and `-h`/`--help`. The five usage cases cover only no-args, receipt-without-expected, expected-without-receipt, unknown flag, and `--selftest` extras.

### F5 — medium: the "old unsupported invocation" retention and distinction are absent

- Requirement: QUALITY17 (`corpus/QUALITY.md` criterion 17) says "retain the unsupported old invocation alongside the same-command repaired result." The round-15 lesson says the public selftest "must distinguish old unsupported invocation from new isolated exit/finding cases, with observed receipts retained."
- Evidence: no selftest case invokes `.ufo/evidence/round-14/capture-context.py`. No retained output exists under `.ufo/evidence/round-15/` for either the old or the repaired invocation.
- Safe old invocation for L1 (static reading): `python3 .ufo/evidence/round-14/capture-context.py --selftest`. `main` (605–613) sees a non-help argument, writes `unexpected argument(s): --selftest` to stderr, and returns 64 before `evaluate` or `write_receipt`. This is safe to retain.
- **Do not run** the archived script with no arguments: `OUTPUT_REL` (line 58) is `.ufo/evidence/round-14/context-receipt.json`, and `write_receipt` (583–602) `os.replace`s it, which would break the frozen pin.
- Status: absent-yet (L1), not a proven defect.

### F6 — low (partly fixed during audit): archived script's output path is the frozen receipt

- Earlier SKILL read (about line 1592): "opt-in prospective probe … writes only its new round14 receipt." At `29689eb3…` SKILL now reads "Archived experiment, not an entry point … must not be run again because its historical output path replaces that frozen receipt." The documentation is corrected.
- Residual: the archived file remains runnable and overwrites the pinned receipt by `os.replace` with no guard. The frozen replay would then fail `snapshot_tampered` (exit 2), so the damage is detectable, not silent.

### F7 — low: `measure.py` standalone-selftest flag is textual; self-invocation counter is statically zero

- Evidence: `context_standalone_selftest_present` (measure.py line ~283) is `count('--selftest') > 0` and `'SELFTEST: PASS' in source`, with no subprocess requirement.
- `context_selftest_self_invocation_lines` (line ~226) counts lines containing both `sys.executable` and `selftest`. In the final snapshot, the two `sys.executable` lines (about 1688 and 1745) do not contain `selftest`, so the counter is statically 0. It is printed but not used in the flag.
- Counterexample: a helper-only selftest that prints `SELFTEST: PASS` and mentions `--selftest` in its docstring would still score `context_standalone_selftest_present` 1. The flag name overstates what it checks. `measure.py` itself says it is not a selftest run.
- Sequencing: `measure.py` reads committed blobs at `--rev`. The round-15 tool, SKILL, and evidence are uncommitted, so measuring the working tree is not possible. At HEAD, `context_capture_present` would be 0.

### F8 — low: selftest exit classes are not declared

- `run_selftest` returns 0 (`SELFTEST: PASS`), 1 (case failure, `SELFTEST: FAIL (n/m failed …)`), 2 (setup error, `SELFTEST: FAIL (setup error …)`). The SKILL round-15 registry names the self-test command with no exit map. The lesson requires every nonzero class to be named.

### F9 — absent-yet (L1), not defects

Under `.ufo/evidence/round-15/` only `claims.json`, `integration-decisions.json`, `sources-before.json`, and `measure.py` exist. Missing for L1 (not predicted):

1. Selftest transcript and exit (`python3 tools/context-capture.py --selftest`).
2. Frozen replay output (`python3 tools/context-capture.py --check`).
3. Negative-counterpart expected pin and run output. SKILL says "caller-committed expected pin", but no such file is committed. Registry expected JSON is inline with `receipt_sha256` `1ee9d09b…`, `id` `missing_injected_environment`, `exit` 1. L1 must create or commit it.
4. `verification.json`, which SKILL names (about line 1616).
5. Post-change census. `sources-before.json` is retained (exit 0, round-start, including S047/S048 W04 warnings); there is no `sources-after.json`, which round 14 had.
6. Old-invocation receipt (F5).
7. `measure.py` output at a committed revision (F7).

## Command inventory

| Command | Declared in | Static state | Retained output | Status |
|---|---|---|---|---|
| `python3 tools/context-capture.py --selftest` | SKILL r15 row; LOG; lesson | entry exists; F1 predicts five failures | none | blocked by F1; L1 run pending |
| `python3 tools/context-capture.py --check` | SKILL r15 row; lesson | pins agree (digests above) | none | absent-yet, L1 |
| `python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected <pin>` | SKILL 1654–1658; registry inline pin | pin file not committed | none | gap: pin not in repo (F9.3) |
| `python3 tools/context-capture.py -h` | not in registry | exit 0, no verdict (F2) | none | medium gap |
| `python3 .ufo/evidence/round-14/capture-context.py --selftest` | QUALITY17; lesson | static exit 64, no write (F5) | none | absent-yet; safe for L1 to retain |
| `python3 .ufo/evidence/round-14/capture-context.py` (no args) | archived | overwrites frozen receipt path | n/a | do not run (F6) |
| `python3 .ufo/evidence/round-15/measure.py --rev <committed>` | evidence dir | needs a commit first; text-only flag (F7) | none | sequencing gap |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | `sources-before.json` | round-start retained, exit 0; executable present | post-change absent | absent-yet, L1 |

## Bounded agreements (checked, not predicted)

- Digest pins above agree with their literals and retained bytes.
- Statically traced primary-ID and exit pairs in these selftest cases match the recomputation order: `clean`, `missing-injected-env`, `null-injected-env`, `comparison-raw-mismatch`, `comparison-observed-at-lie`, `payload-digest-lie`, `control-ineffective`, `control-flag-lie`, `mapping-check-lie`, `mapping-constant-swap`, `mapping-order-lie`, `probe-source-lie`, `runner-source-lie`, the structural cases (`truthy-*`, `bool-exit`, `exclusions-widened`, `comparison-container`), the parse cases, `receipt-missing`, `stored-verdict-lie`, `retained-invalid-input`, `baseline-unusable`, and `expected-digest-invalid`/`expected-invalid`/`expected-missing` for id/exit. The only disagreement is the F1 verdict-match assertion.
- Static count of recorded selftest assertions at `e55f8b06…`: 31 `check_case` + 5 `usage_case` = 36 case calls + 2 hermetic records = 38. This is a source count, not a run result.
- Exit 64 is named in the docstring, `USAGE`, SKILL round-15 row, and `measure.py` regex (`TOOL_64_NEAR_RE`), consistently as could-not-evaluate/usage.
- The round-15 registry row names 0/1/2/64 and the entry, selftest, pins, write scope, and owner columns; the documented gate row is parseable by `measure.py`'s `registry_rows` (`kind` gate, eight cells).

## Not verified (absent-yet or out of scope)

- Any runtime outcome of selftest, frozen check, negative-pin check, measure, census, or the old invocation. None has been run by this seat.
- S049's live text (not re-fetched); S050 and S051 wording beyond the rows and docstring line 12.
- Other wave-1/wave-2 seats' reports, except as they touch these artifacts.
