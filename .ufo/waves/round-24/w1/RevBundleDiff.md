# RevBundleDiff: round-23 vs round-24 command-binding replay bundles

Lane: TameshiR24-2.RevBundleDiff (leaf; read-only; no subagents; no replay, gate, selftest, or battery run; no tool installs or upgrades).
Judged on: calibration.

- A = `.ufo/evidence/round-23/replay/bundle.json`, receipts at revision `496d212bc46789cdf8cafab72978bdb7f4182963`
- B = `.ufo/evidence/round-24/replay/bundle.json`, receipts at revision `d2eaecd443bf5f4e387e7e5331282e3d11dea047`

## Verdict

- **Exit codes:** 43/43 identical in A and B. Each equals its requirement's `expect.exit`.
- **Argv:** 43/43 identical in A and B, and identical to the frozen `requirements[i].argv`.
- **Stdout tokens:** every `stdout_contains` token is present in both A and B. 40 rows carry token expectations; rows 0, 1, 14 are exit-only. Token-level differences: none. No pass/fail verdict changes.
- **Body differences:** 17 of 43 rows differ in stdout and/or stderr bytes. Every one is attributed below: 14 rows are run-scoped noise, 2 rows (18, 22) reflect a real SOURCES.md change from commit d2eaecd (S084, S085), and 1 row (5) reads live fleet HEADs that moved between runs.
- **Flags:** row 5 is not hermetic (F1). The bundle bytes are not reproducible at a fixed revision, and `live_dependent` under-classifies this (F2). The round-24 label `d2eaecd` is not the delivered `c8c5b88`, though tools and corpus are identical between them (F3).

## Results by field

| field | A vs B | evidence |
|---|---|---|
| exit | 43/43 equal; all match `expect.exit` | `bundle.json` receipts[i].exit vs requirements[i].expect.exit |
| argv | 43/43 equal; equal to `requirements` and to `round-23/requirements.json` `requirements` (43) | receipts[i].argv |
| stdout tokens | all expected tokens present in both; 0 token-level diffs | requirements[i].expect.stdout_contains |
| receipt `revision` | differs in 43/43 (intended: 496d212 vs d2eaecd) | receipts[i].revision |
| receipt `cwd` | differs in 43/43 (replay temp root) | receipts[i].cwd |
| stdout/stderr bytes | identical in 26 rows; differ in 17 rows | normalized comparison, section "Cause analysis" |

No `Traceback` appears in any stdout or stderr. No `…[+N]` truncation markers appear in the files. Stdout lengths: +5 bytes in rows 3, 5, 7, 9, 10, 21 (one replay-root occurrence each, 37-char vs 32-char root); +45 bytes in row 17 (9 occurrences x 5); equal length in rows 18 and 22 (values changed in place).

## Row table (43 rows)

Cause codes (see "Cause analysis"): **M** receipt metadata only (`cwd`, `revision`), stdout and stderr byte-identical; **C** replay temp root embedded in stdout; **T** mktemp scratch names; **D** wall-clock timestamp; **E** elapsed seconds; **H** commit SHA minted in a run-time scratch repo; **S** SOURCES.md census change; **L** live fleet HEAD change. "tokens" = count of `stdout_contains` tokens. Full argv: `requirements[i].argv` (identical in A and B).

| # | receipt | argv (abbrev.) | exp exit | tokens | exit A | exit B | stdout+stderr | cause |
|--:|---|---|:--:|--:|:--:|:--:|:--:|---|
| 0 | repeat-control-snapshot-clean | `python3 tools/repeat-control.py --snapshot .ufo/evidence/...` | 0 | 0 | 0 | 0 | = | M |
| 1 | repeat-control-snapshot-mismatch | `python3 tools/repeat-control.py --snapshot .ufo/evidence/...` | 1 | 0 | 1 | 1 | = | M |
| 2 | repeat-control-selftest | `python3 tools/repeat-control.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 3 | bash-witness-count | `python3 tools/bash-witness-study.py count` | 0 | 1 | 0 | 0 | differs | C |
| 4 | bash-witness-selftest | `python3 tools/bash-witness-study.py selftest` | 0 | 1 | 0 | 0 | = | M |
| 5 | pin-disposition-read | `python3 tools/pin-disposition.py --manifest .ufo/evidence...` | 0 | 1 | 0 | 0 | differs | C, D, L |
| 6 | pin-disposition-selftest | `python3 tools/pin-disposition.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 7 | witness-metadata-check | `python3 tools/witness-metadata.py --check --companion .uf...` | 0 | 1 | 0 | 0 | differs | C |
| 8 | witness-metadata-selftest | `python3 tools/witness-metadata.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 9 | evidence-disposition-round18 | `python3 tools/evidence-disposition.py --root . --disposit...` | 0 | 3 | 0 | 0 | differs | C |
| 10 | evidence-disposition-round18-before | `python3 tools/evidence-disposition.py --root . --disposit...` | 1 | 2 | 1 | 1 | differs | C |
| 11 | evidence-disposition-selftest | `python3 tools/evidence-disposition.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 12 | context-capture-frozen | `python3 tools/context-capture.py --check --json` | 0 | 1 | 0 | 0 | = | M |
| 13 | context-capture-missing-env | `python3 tools/context-capture.py --check --receipt .ufo/e...` | 1 | 1 | 1 | 1 | = | M |
| 14 | context-capture-mapping-suffix | `python3 tools/context-capture.py --check --receipt .ufo/e...` | 1 | 0 | 1 | 1 | = | M |
| 15 | context-capture-selftest | `python3 tools/context-capture.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 16 | mutate-and-run-selftest | `bash tools/mutate-and-run.sh --selftest` | 0 | 2 | 0 | 0 | = | M |
| 17 | mutate-and-run-regression | `bash tools/mutate-and-run.sh --regression` | 0 | 1 | 0 | 0 | differs | C, T, D |
| 18 | measure-round16-rev | `python3 .ufo/evidence/round-16/measure.py --rev HEAD --re...` | 0 | 2 | 0 | 0 | differs | S |
| 19 | measure-round16-selftest | `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | 1 | 0 | 0 | differs | T |
| 20 | assemble-round16-selftest | `python3 .ufo/evidence/round-16/coldread/assemble.py --sel...` | 0 | 1 | 0 | 0 | differs (stderr) | T |
| 21 | reattribute-round16-selftest | `python3 .ufo/evidence/round-16/attribution/reattribute.py...` | 0 | 1 | 0 | 0 | differs | C |
| 22 | sources-census | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | 0 | 1 | 0 | 0 | differs | S |
| 23 | verify-round15 | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db8...` | 0 | 1 | 0 | 0 | differs | T |
| 24 | registry-check-selftest | `python3 tools/registry-check.py --selftest` | 0 | 1 | 0 | 0 | differs | E |
| 25 | measure-round17-selftest | `python3 .ufo/evidence/round-17/measure.py --selftest` | 0 | 1 | 0 | 0 | differs | T, H |
| 26 | assemble-round17-selftest | `python3 .ufo/evidence/round-17/coldread/assemble.py --sel...` | 0 | 1 | 0 | 0 | differs | T, H |
| 27 | trace-inputs-selftest | `python3 tools/trace-inputs.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 28 | measure-round18-selftest | `python3 .ufo/evidence/round-18/measure.py --selftest` | 0 | 1 | 0 | 0 | differs | T, H |
| 29 | assemble-round18-selftest | `python3 .ufo/evidence/round-18/coldread/assemble.py --sel...` | 0 | 1 | 0 | 0 | differs | T, H |
| 30 | defect-probes-selftest | `python3 .ufo/evidence/round-18/defect-probes.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 31 | round19-correction-ruler-selftest | `python3 .ufo/evidence/round-19/measure.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 32 | round19-coldread-selector-selftest | `python3 .ufo/evidence/round-19/coldread/measure.py --self...` | 0 | 1 | 0 | 0 | = | M |
| 33 | receipt-window-selftest | `python3 tools/receipt-window.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 34 | receipt-measure-selftest | `python3 tools/receipt-measure.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 35 | round20-coldread-selector-selftest | `python3 .ufo/evidence/round-20/coldread/measure.py --self...` | 0 | 1 | 0 | 0 | = | M |
| 36 | env-diff-selftest | `python3 tools/env-diff.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 37 | wave-route-mix-selftest | `python3 tools/wave-route-mix.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 38 | round21-measure-selftest | `python3 tools/round21-measure.py --selftest` | 0 | 1 | 0 | 0 | = | M |
| 39 | round21-coldread-selector-selftest | `python3 .ufo/evidence/round-21/coldread/measure.py --self...` | 0 | 1 | 0 | 0 | = | M |
| 40 | wave-accounting-frozen-entry | `python3 tools/wave-accounting.py --bundle .ufo/evidence/r...` | 0 | 4 | 0 | 0 | = | M |
| 41 | wave-accounting-selftest | `python3 tools/wave-accounting.py --selftest` | 0 | 3 | 0 | 0 | = | M |
| 42 | wave-accounting-wrong-count-entry | `python3 tools/wave-accounting.py --bundle .ufo/evidence/r...` | 1 | 3 | 1 | 1 | = | M |

## Cause analysis

Method: for each differing stdout/stderr, replace the replay root (`/tmp/tameshi-r23-replay-naxu6fzi` in A, `/tmp/tameshi-registry-replay-dzo3ypiq` in B) with a placeholder, then compare per-class patterns separately: timestamps, `/tmp/<name>` scratch directories, `elapsed=` values, and 40-hex commit SHAs. SHA placeholders apply only to the scratch-repo selftest rows (20, 25, 26, 28, 29), so row 5's live HEAD changes stay visible. Rows whose content still differs after all placeholders are residuals; there are exactly three: rows 5, 18, 22.

**C, replay temp root (rows 3, 5, 7, 9, 10, 17, 21).** The `cwd` of each replay appears in stdout. Replacing it makes these rows equal, except as noted for D, L, S. The 5-byte delta is exact: `/tmp/tameshi-r23-replay-naxu6fzi` is 32 chars and `/tmp/tameshi-registry-replay-dzo3ypiq` is 37 chars. Row 17 contains 9 occurrences (9 x 5 = 45 bytes).

**T, mktemp scratch names (rows 17, 19, 20 stderr, 23, 25, 26, 28, 29).** Examples: row 17 `REGRESSION_WORKDIR ...tameshi-r4-2-regression.znDrgQ` vs `.n3oaDW` (`tools/mutate-and-run.sh:1289` `mktemp -d`); row 19 `tameshi-r16-CRMeasure-2uj39g0g` vs `-f5c0w6q7`; row 20 stderr `assemble-selftest-fegd019w` vs `-3kj4mbv1`; row 23 `tameshi-r15-verify-2aeav6pv` vs `-fq19b9ra`; rows 25, 28 `tameshi-r17-MeasureV2-nt9qhyzq` vs `-zrg9esoz`, `kwa2esv8` vs `ihzdp654`; rows 26, 29 `assemble-v2-selftest-s8jhruxt` vs `5_ov4r43`, `x38_zs31` vs `uy5vd4ia`.

**D, wall-clock time (rows 5, 17).** Row 5 `observed_at` `2026-10-21T14:42:24Z` vs `15:56:45Z`. Row 17 `REGRESSION_DATE` `14:42:36Z` vs `15:57:06Z` (`tools/mutate-and-run.sh:1300`, `date -u`).

**E, elapsed seconds (row 24).** `timeout-kills-setsid-pipe` `elapsed=1.085s` vs `1.393s`; `timeout-kills-setpgid-pipe` `elapsed=1.083s` vs `1.397s`. Both PASS in both. Timing is measured with `time.monotonic()` (`tools/registry-check.py:672-703`); the selftest only asserts `elapsed < 3.5` (`:1209`).

**H, run-time commit SHAs (rows 25, 26, 28, 29).** Row 25 and 28: `PASS revision-40hex <sha>` (`measure.py:1379-1382` checks only the format; the SHA is the HEAD of a scratch repo that `measure.py:892-903` creates with `git init` and `git commit`). Rows 26 and 29: `read_rev` and `rev` values from scratch repos created by `assemble.py:1077, 1083, 1518`. All 12 cited commit SHAs are absent from the tameshi repository (`git cat-file -t` fatal for each). Content hashes in the same rows (for example `sha256=982967b0...`, `7313e9a2...`) are identical in A and B. [INFERENCE] Commit IDs embed author and committer timestamps, so they change per run. Not re-run.

**S, SOURCES.md census (rows 18 and 22).** Census counts move from 81 to 83 rows, tier A from 72 to 74, status mined from 52 to 54. Queued (23), rejected (6), tiers B (7), and C (2) are unchanged. The sources-census verdict is `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` in both. The added IDs are exactly S084 (`corpus/SOURCES.md:93`, docs, tier A, mined) and S085 (`corpus/SOURCES.md:94`, own-work, tier A, mined). The only commit in `496d212..d2eaecd` that touches `corpus/SOURCES.md` is `d2eaecd` itself. A recount with the census regex reproduces 81 and 83 exactly. Row 18 is `measure.py --rev HEAD --repo .` and reads the clone's HEAD, not the registry.

**L, live fleet HEAD (row 5).** The argv is `tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`, which reads the live fleet, not the replay clone. Four `legs[i].head.commit` values changed:

| leg | repo | pinned.commit (A and B) | head A | head B |
|---|---|---|---|---|
| legs[1] bash-surface-census | kagi-shokunin | fecee874... | 0a47dd1 | 144babc |
| legs[2] bash-tsukuroi-census | tsukuroi-shokunin | 165307fe... | 415ac3a | ae01e50 |
| legs[3] bash-mado-verify | mado-shokunin | eead56b2... | 9185f1f | 8c74209 |
| legs[4] bash-checklist-run | kagi-shokunin | fecee874... | 0a47dd1 | 144babc |

Pinned commits, `content_status`, `result_reuse`, `counts` (`{legs 6, unchanged 1, changed 5, unavailable 0}`), and `status` (`ok`) are identical. The round-24 `live-dependent.json:3` already lists this row.

## Flags

**F1 (medium; confirmed). Row 5 is not hermetic.** Its stdout depends on four live sibling HEADs. The bundle SHA-256 covers that content, so a future re-run cannot reproduce the same bytes. Keep it in `live_dependent`. Do not cite row 5 as revision evidence.

**F2 (medium). Bundle bytes are not reproducible at a fixed revision, and the classification understates this.** `live-dependent.json` says `revision_pinned: 41`, `live_dependent: [pin-disposition-read, verify-round15]`. Of the 41 revision-pinned rows, 13 carry run-scoped bytes: rows 3, 7, 9, 10, 21 (replay root), 17 (root, scratch, date), 19, 20, 24, 25, 26, 28, 29 (scratch names, elapsed, or run-time SHAs). Row 23 is listed live, but its only visible difference is a scratch name. The bundle SHA pins (`3d6c99b7...`, `4f424023...`) therefore attest one stored capture, not a reproducible result. [INFERENCE] Any re-run would embed different mktemp names and timestamps; not re-run.

**F3 (medium-low; provenance label). Round-24 is labelled `d2eaecd`, while the delivered implementation is `c8c5b88`.** `c8c5b88` is two commits later (`bd38c02`, `c8c5b88`). `git diff --name-only d2eaecd c8c5b88` lists 26 files, all under `.ufo/`; none under `tools/` or `corpus/`. The replayed tools and corpus are therefore the delivered ones. The label is accurate for code but should say so.

**F4 (low; scope of comparison). Round-23 was captured before round-23 closed.** `496d212` is an ancestor of `6a1821a` (the round-24 wave base); `git rev-list --count 496d212..6a1821a` = 5, counting `6a1821a`, and `merge-base --is-ancestor` = true. So A-to-B spans 7 commits. Within `496d212..d2eaecd`, the only changes under `tools/` are `tools/registry.json` (+74, 0 deletions), `tools/command-binding.py` (`:161-173`, second fixture file), and new `tools/registry-replay.py`; the only `corpus/SOURCES.md` change is in `d2eaecd`. Other evidence changes in the window (for example `.ufo/evidence/round-21/coldread/ledger.json`) produce no row output difference.

**F5 (low; scope). Neither bundle exercises the round-24 registry additions.** The 43 requirements equal the 47-row round-23 baseline's active rows; the four extra baseline rows are superseded (`evidence-disposition-round17`, `-round17-before`, `evidence-disposition-round14-superseded`, `trace-inputs-round17-selftest`). `d2eaecd` adds 7 registry rows (4 active: `command-binding-selftest-r24`, `command-binding-frozen-clean-pinned`, `command-binding-source-read-red-pinned`, `registry-replay-selftest`; 3 superseded: `command-binding-selftest`, `command-binding-frozen-clean`, `command-binding-source-read-red`). The replay consumes the frozen baseline: `registry-replay.py:138-139` refuses a baseline whose SHA differs, and `observations.json` `registry_sha256` is `ebd2e69a...` (the round-23 registry). No receipt output is attributable to the registry delta. The 44/44 command-binding selftest and `registry-replay-selftest` are not covered by either bundle.

**F6 (low; expectation strength, does not change this diff).** Exit-only rows: 0, 1, 14 (row 14 prints `mapping_mismatch`, but the expectation does not require it). Label-only token rows: 4, 19, 25, 27, 28, 29, 31, 32 (for example `"SELFTEST: "`), which would still match `SELFTEST: FAIL` if exit were 0. Row 18 checks key presence only (`"calibration_restraint_score":`, `"coldread":`); its value changes (rows 81 to 83, mined 52 to 54, A 72 to 74) are unconstrained, and `calibration_restraint_score` itself is unchanged.

**F7 (info; census interpretation).** S085 is own-work at tier A, and its text says it records "adjudicated, unexecuted hardening defects ... not their truth." The repo already tiers own-work as A (5 rows at round 23; 6 at round 24, with S085 the new one). The A increase (72 to 74) therefore comprises one docs row and one own-work row. Census A counts should not be read as independent evidence strength.

**F8 (info).** Rows 18 and 22 are HEAD- or cwd-relative (`--rev HEAD --repo .`; `corpus/SOURCES.md`). The same argv denotes different content at different revisions, so the per-receipt `revision` is the only pin.

## Integrity checks that passed

- `sha256(round-23/replay/bundle.json)` = `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9`. Matches `round-23/replay/expected.json` and the expected stdout of registry row `command-binding-frozen-clean-pinned`.
- `sha256(round-24/replay/bundle.json)` = `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`. Matches `round-24/replay/expected.json`, and `replay-gate.json` stdout (exit 0, `finding_ids: []`).
- `sha256(tools/registry-replay.py @d2eaecd)` = `9fcd2dbb...` = `replay-command.json` `instrument_sha256`. `sha256(tools/command-binding.py @d2eaecd)` = `9230c68e...` = `replay-gate.json` `tool_sha256`.
- Runner: `tools/registry-check.py` is `cba16646...` at both revisions, matching `runner_sha256` (A) and `runner_sha256_clone_copy` (B). `round-23/replay.py` is `adb41716...` at both revisions (unchanged).
- Per-row observations (`observations.json`, 43 rows per round): exit (`runner_result.got`), stdout, stderr, and argv equal the bundle receipt for every row. All rows `held: true`.
- `replay-command.json` stdout: 43 verdict lines, all `True`; exit codes agree with the bundle.

## Not established

- No producer authentication, promotion, historical R17-CMD-BIND closure, or numeric score uplift is claimed.
- The live `CENSUS_TOOL` reference at `.ufo/evidence/round-15/verify.py:105` exists in code. I did not trace whether this argv executes it; no drift is visible in this pair.

## Smallest safe correction (documentation and classification only; no replay re-run)

1. Keep the bundle SHA pins. Annotate the round-24 bundle: revision `d2eaecd`, tools and corpus identical to delivered `c8c5b88` (only `.ufo/` changed).
2. Re-describe `revision_pinned` as "revision-pinned, run-varying bytes excluded" or add the 13 run-scoped rows (3, 7, 9, 10, 17, 19, 20, 21, 24, 25, 26, 28, 29) to a non-reproducible class. State that `bundle_sha256` attests the stored capture only.
3. Keep row 5 in `live_dependent`.
4. In census reporting, state that tier A includes own-work rows (6 at round 24).

None of these changes exit, argv, or token results.

## Confidence

- High (directly observed in files, hashes, or git objects): all verdict items; the C, T, D, E, S, L attributions; F3 and F4 ancestry; F5 registry facts; row 5 leg values.
- Medium-high [INFERENCE]: H-class commit IDs change per run; F2 non-reproducibility holds for any re-run. Both follow from the producing code and observed values; neither was re-run.

## Commands and tooling

Read-only only: Python 3 stdlib (`json`, `hashlib`, `subprocess`, `re`) for reading files and hashing; git with `GIT_OPTIONAL_LOCKS=0` for `show`, `log`, `diff`, `diff --name-only`, `rev-list --count`, `merge-base --is-ancestor`, `cat-file -t`, `grep`, `ls-tree`, `status --porcelain`. Nothing installed, upgraded, cloned, or executed from the tameshi tooling.
