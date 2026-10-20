# Round 15 · w1 · ClaimEvidence — C1 before→after evidence checklist (report-only)

Seat: `TameshiR15.ClaimEvidence` (scribe, leaf). Lane: tameshi-shokunin. Baseline HEAD: `a9cf4da78f2514c7bedd91a850a88590009d7df0`.
Claim under review: `.ufo/evidence/round-15/claims.json` C1 — calibration capability; score `6→6`, no promotion points.

**Execution boundary.** No check, selftest, gate, probe, capture, guardrail, measure script, build or test was executed by this seat. Observations below come from reading files, reading git-tracked state (`git ls-files`, `git log`, `git status`), and computing SHA-256 of bytes and parsing JSON. Anything not observed on disk is marked `[INFERENCE]`. Historical source behaviour (exit codes of `main`, branch outcomes) is read from source text and labelled `[SOURCE]`.

**Tool installs/updates:** none. **Writes:** this report only.

---

## 1. Axes named

| Axis | Round-15 role | Pinned now | Evidence rule for this round |
|---|---|---|---|
| calibration | C1 target (lowest tied axis with depth) | 6 (`SCORECARD.md`, round-14 row; `measure.py` `calibration_restraint_score`) | Capability credit only; scalar must read 6 before and after |
| depth | must stay unchanged | 6 (recorded cases = 6) | No new mutation case; `tools/mutate-and-run.sh` sha unchanged |
| coverage | unchanged | — | No new covered target surface |
| operability | capability credited to calibration once | — | Runner unchanged; new tool is not a separate axis move |
| freshness | unchanged | — | No successor sweep, no intake |
| adjacency | unchanged | — | Siblings read-only; no sibling gate run |

---

## 2. Files actually read (this seat)

- `AGENTS.md` (LOG entry required per change; commits carry lane identity).
- `corpus/lessons/round-14-verifier-spotcheck.md` lines 1–173, incl. Routed defect 5 at line 160 (full text read raw).
- `SKILL.md` lines 58–73 (gate-shape table, hermetic/live/audit rules), 1499–1510 (round-12 registry), 1548–1560 (round-13 registry), 1574–1576 (decision-table rows), 1581–1602 (round-14 procedure + registry).
- `SCORECARD.md` lines 64–76 (depth/calibration rubric and counting commands), 296–345 (round-12/13 rows), 398–470 (round-14 section).
- `SHONEN.md` (four boxes, all `[~]`); `PROVINCE.md` (Core/Frontier/Adjacent).
- `LOG.md` tail (round-14 entries, lines describing capture-context and registry).
- `.ufo/evidence/round-14/`: `capture-context.py` (647 lines, read in full), `context-receipt.json`, `context-missing-env.json`, `verification-final.json`, `verification-verdict.json`, `guardrails.json`, `expected-outcomes.json`, `expected-runtime-final.json`, `after-committed.json`, `measure.py`.
- `.ufo/evidence/round-13/`: `pin-manifest.json`, `expected.json` (top-level keys and `inputs`).
- `tools/pin-disposition.py` (rubric lines 1–10, 175–181, 406–412, 602–606, 1191–1247 via grep/range), `tools/evidence-disposition.py` (selftest and subprocess pattern, lines 1228–1262, 1510–1540), `tools/repeat-control.py` (lines 36–60 finding-ID table and snapshot rules, selftest subprocess pattern lines 592–613).
- `.ufo/evidence/round-15/claims.json`; `.ufo/waves/round-15/assignments1.json`, `spec1.json` (seat prompt only).
- `corpus/SOURCES.md` rows S003, S049, S050 (grep).

Not read or touched: `~/.omp/agent/agent.db*`, credential/auth files, sibling trees, `omp` CLI.

---

## 3. Observed before-state (static, from committed bytes at HEAD `a9cf4da`)

| # | Before-fact | Observation | Pointer |
|---|---|---|---|
| B1 | Active tool `tools/context-capture.py` absent | `git ls-files` shows no such path; `tools/` holds `bash-witness-study.py evidence-disposition.py mutate-and-run.sh pin-disposition.py repeat-control.py witness-metadata.py` | `tools/` listing |
| B2 | Historical instrument lives only under round-14 evidence | `.ufo/evidence/round-14/capture-context.py`, sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` (matches `verification-final.json` input pin) | `git ls-files .ufo/evidence/round-14` |
| B3 | Registry classifies it as a probe with no selftest | `SKILL.md:1602`: kind `probe`; self-test column "no standalone selftest; integrated negative receipt and injection controls retained" | `SKILL.md:1602` |
| B4 | Registry row has no exit 64 | `SKILL.md:1602` verdict map lists 0/1/2 only; source docstring declares `64 usage error, no receipt` | `capture-context.py:26–29`, `:117–124`, `:605–613` |
| B5 | Disposition gate lists 64 only as "usage" | `SKILL.md:1601`: "…2 could-not-evaluate…; 64 usage" | `SKILL.md:1601` |
| B6 | Routed defect 5 names the exact gaps | (a) probe→gate classification; (b) standalone isolated self-invocation with literal exit/finding pairs; (c) map exit 64 to could-not-evaluate and declare the context harness 64 path | `corpus/lessons/round-14-verifier-spotcheck.md:160`; `:96` |
| B7 | Historical `--selftest` has no meaning | `main()` returns 64 for any argv other than `-h/--help` | `capture-context.py:605–613` `[SOURCE]` |
| B8 | Calibration scalar pinned | `calibration_restraint_score = 6` = 2 × count of `[~]` in boxes 1, 2, 4 (box 3 excluded) | `measure.py` line 42; `SHONEN.md` (4× `[~]`); `SCORECARD.md:300`, `:336` |
| B9 | Round-15 evidence dir has only the claim | `.ufo/evidence/round-15/claims.json` only | `git status` (untracked) |
| B10 | Round-14 raw evidence clean | `git status --porcelain` shows only `?? .ufo/evidence/round-15/` and `?? .ufo/waves/round-15/`; no tracked file modified | `git status` |

Round-14 pins that already exist and must stay byte-stable:

| File | SHA-256 (observed by reading bytes now) |
|---|---|
| `.ufo/evidence/round-14/capture-context.py` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` |
| `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` |
| `.ufo/evidence/round-14/context-missing-env.json` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` |
| `.ufo/evidence/round-14/verification-final.json` | `e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2` |
| `.ufo/evidence/round-14/guardrails.json` | `cca670b54f5da70873daec8d1bd54749ea63be99582f21138d43c8c715eaf784` |
| `tools/pin-disposition.py` (probe) | `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` (= `expected.json` input pin = receipt `sources.probe.sha256`) |
| `tools/mutate-and-run.sh` (runner) | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (= manifest `derived_from.sha256`; = `after-committed.json` `runner_sha256`) |
| `.ufo/evidence/round-13/pin-manifest.json` | `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` |
| `.ufo/evidence/round-13/expected.json` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` |
| `tools/evidence-disposition.py` | `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95` |

---

## 4. Facts about the historical receipts that constrain the gate

| # | Fact | Pointer |
|---|---|---|
| R1 | Real receipt: `status ok`, `exit 0`, `reasons []`; `comparison.equal true` (both canonical sha `22e79150…61f9`), `positive_control.effective true` (baseline exit 0, injected exit 128), `mapping.all_match true` (six legs), `env_delta_keys ["GIT_DIR"]`, `result_reuse not_established` | `context-receipt.json` |
| R2 | **Tampered control receipt also reads `status ok / exit 0 / reasons []`.** `context-missing-env.json` lacks `environment.injected_env`, yet a decide-only replay would accept it. The round-14 guardrail rejects it only through an external one-line predicate (`guardrails.json` check `context_setup_missing_field`, exit 1). | `context-missing-env.json` lines 14–26; `guardrails.json` |
| R3 | `decide()` never reads `injected_env`; `evaluate()` always writes it (`capture-context.py:531–536`). A replay must therefore check the field itself, not infer it. | `capture-context.py:531`, `:553–580` |
| R4 | The historical tool writes `OUTPUT_REL = .ufo/evidence/round-14/context-receipt.json` via `os.replace` (`:58`, `:583–602`). Running it with no argv overwrites the round-14 receipt. The round-14 registry row (SKILL:1602) invites exactly that no-arg run. | `capture-context.py:58`, `:583–602`; `SKILL.md:1602` |
| R5 | `LANE_ROOT` derives from `SELF` by **four** `dirname` calls (`:46`). Correct for `.ufo/evidence/round-14/`. Under `tools/` the correct depth is **two**; four lands on the fleet root `/home/vgpnk/Projects/shokunin`, and the probe path then resolves wrong. | `capture-context.py:45–47` |
| R6 | Exit 2 path writes a receipt (`status invalid_input`); exit 64 writes nothing. Exit-2 reason text is `kind + ": " + message` (`:618–620`), so a stable ID can be derived from `kind` without changing semantics. | `capture-context.py:605–643` |
| R7 | Positive control needs `git -C LANE_ROOT rev-parse --git-dir` to succeed under the baseline env. A synthetic lane root must therefore be a git repo. | `capture-context.py:395–411` |
| R8 | The `/nonexistent/tameshi-round14-poison` check is hard-coded (`:60–61`, `:469–472`). Hermetic selftest cannot create it without root, so the `poison_path_exists` exit-2 branch is not reachable from a hermetic selftest unless a test seam is added. | `capture-context.py:60–61`, `:469–472` |
| R9 | Historical guardrail `runner_variable_swap_discriminator` loads `.ufo/evidence/round-14/capture-context.py` via `runpy` and calls `parse_runner_mapping`, `mapping_block`, `RUN_REGRESSION_RE`. Any promoted copy must keep those names or the guardrail must be re-pointed. | `guardrails.json` check 3 |
| R10 | `measure.py` reads committed blobs only (`git show REV:path`); its `gate_artifact` counter is hard-wired to `tools/evidence-disposition.py` (line 34). A new untracked tool cannot change the scalar, and a count cannot claim the new gate without a changed measure. | `measure.py:17–34` |

---

## 5. Evidence checklist for C1 (L1 runs each item once after the seats return)

Status column = state at this seat's reading. "Missing" means no file or pointer exists yet.

| ID | Check (observable) | Pass condition (exact) | Retain at | Status now |
|---|---|---|---|---|
| E0 | Historical bytes preserved | `git diff --exit-code a9cf4da -- .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14 corpus/lessons/round-14-verifier-spotcheck.md SHONEN.md PROVINCE.md tools/mutate-and-run.sh tools/pin-disposition.py tools/evidence-disposition.py tools/repeat-control.py` exits 0 **and** sha256 of the round-14 files in §3 unchanged | `.ufo/evidence/round-15/` (new file, e.g. `historical-integrity.txt`) | Missing (no file); tracked state clean now (B10) |
| E1 | Promoted tool exists, historical bytes untouched | `tools/context-capture.py` present; `sha256sum .ufo/evidence/round-14/capture-context.py` = `7313e9a2…fe7d89` | `.ufo/evidence/round-15/context-capture.sha256` | Missing |
| E2 | Promoted tool derives lane root at two `dirname`s and the probe/runner/manifest paths resolve under it | Source check: LANE_ROOT line uses 2 `dirname` calls; `PROBE_REL`, `RUNNER_REL`, `MANIFEST_REL`, `EXPECTED_R13_REL` unchanged | source + selftest case S1 | Missing (hazard R5) |
| E3 | Output path is round-15 only | `OUTPUT_REL` = `.ufo/evidence/round-15/context-receipt.json`; no path reference to `round-14` in tool except the historical-digest constant | source grep | Missing |
| E4 | Stable finding IDs and exit classes declared in tool | Table in §7 present in source docstring and printed by selftest | selftest stdout | Missing |
| E5 | Standalone selftest exits 0 with literal case lines and closing verdict | `python3 tools/context-capture.py --selftest` → exit 0; every case line prints `exit=<n> id=<ID>`; final line `CONTEXT_SELFTEST: PASS (N/N)`; N pinned in tool | `.ufo/evidence/round-15/selftest.stdout` + `.exit` | Missing |
| E6 | Selftest hermeticity by env poisoning | `GIT_DIR=/nonexistent/tameshi-r15-poison python3 tools/context-capture.py --selftest` → same PASS line and exit 0 | `.ufo/evidence/round-15/selftest-poisoned.stdout` + `.exit` | Missing |
| E7 | Selftest writes only under temp roots | After E5, no file under the live lane changed (`git status --porcelain` identical before/after; no `.ufo/evidence/round-15/context-receipt.json` created by selftest) | same | Missing |
| E8 | Usage class: unexpected argv → 64, no receipt | Case `usage-extra-arg` in selftest: exit 64, id `context_invalid_usage`, no file written | selftest | Missing |
| E9 | Retained-receipt replay check (no subprocess, no live read) | `python3 tools/context-capture.py --check .ufo/evidence/round-15/context-receipt.json` → exit 0, id `context_replay_match`; replay also requires `environment.injected_env == {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` and `env_delta_keys == ["GIT_DIR"]` (guards R2/R3) | `.ufo/evidence/round-15/check.stdout` + `.exit` | Missing |
| E10 | Tampered-receipt replay rejected | Run `--check` on a copy of the round-14 `context-missing-env.json` (copied into a temp root, never edited in place) → exit 2, id `context_receipt_malformed` | selftest case, not a live file | Missing |
| E11 | Digest binding of retained receipt | `--check` refuses (exit 2, id `context_receipt_tool_digest_mismatch`) when `tool_sha256` ≠ disk sha of the tool that produced it; a pin file records receipt sha256 | `.ufo/evidence/round-15/context-expected.json` (new, see §8) | Missing |
| E12 | Normal prospective capture writes round-15 only | `python3 tools/context-capture.py` → exit recorded as observed (do not predict); writes only `.ufo/evidence/round-15/context-receipt.json`; round-14 receipt sha256 unchanged | `.ufo/evidence/round-15/capture.stdout` + `.exit`; round-14 sha re-read | Missing |
| E13 | Round-15 receipt replays clean | E9 on the E12 receipt | `check.stdout` | Missing |
| E14 | Registry row for round-15 gate (kind gate, not probe) with explicit 0/1/2/64 | `SKILL.md` round-15 section has a row: kind `gate`; verdict map lists 0, 1, 2 and 64 with classes; selftest command; pinned values; write scope; owner `tameshi` | `SKILL.md` | Missing |
| E15 | 64 classes explicit for both gates | `SKILL.md` round-15 row for evidence-disposition states "64 usage/could-not-evaluate" (or split, see R-decision D1); context row states `64 usage` with no receipt | `SKILL.md` | Missing |
| E16 | Calibration scalar stays 6 at the measured commit | `python3 .ufo/evidence/round-14/measure.py --rev <measured>` → `calibration_restraint_score: 6`, `recorded_cases: 6`, `runner_sha256 = 75ed934d…`; `SHONEN.md`, `PROVINCE.md` byte-identical to HEAD | `.ufo/evidence/round-15/after-committed.json` (new name; measure reads committed blob only) | Missing; measure must target a commit containing the tool |
| E17 | Before/after counting pinned | `before` = `a9cf4da` measure output (must be produced; round-14 `before.json` is for d6809df, not a9cf4da) | `.ufo/evidence/round-15/before.json` | Missing |
| E18 | Frozen digest-bound run pins | `context-expected.json` lists: measured commit, sha256 of tool, probe, runner, manifest, expected_r13, receipt, expected exit 0, expected ID `context_match`, and checked selftest count N | `.ufo/evidence/round-15/context-expected.json` | Missing |
| E19 | Source census for any new source row | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0; W04 warnings only | `.ufo/evidence/round-15/sources-census.txt` | Missing; S003/S049/S050 are existing rows (round-14). Add rows only if new docs are opened |
| E20 | Depth stays at 6 | `SCORECARD` command D: `recorded_cases=6 depth_score=6` at measured commit | E16 output | Pending E16 |
| E21 | LOG entry with motivating evidence | `LOG.md` appended with the round-15 evidence pointers (AGENTS.md rule) | `LOG.md` | Missing |
| E22 | SCORECARD round-15 row, no scalar move | Row: C1, calibration, before (no tool, no selftest, 64 ambiguous) → after (E5/E9/E12 outputs); `6→6`, delta 0 | `SCORECARD.md` | Missing |
| E23 | Non-author closure is separate | Closure note is not authored by this seat or L1 | future `corpus/lessons/round-15-…` | Out of seat scope |

---

## 6. Implementation-critical hazards (ranked, for the gate executor)

1. **H1 — lane root depth.** `tools/context-capture.py` must derive LANE_ROOT with two `dirname` calls, not four (R5). Four calls resolve to the fleet root and send the probe path wrong.
2. **H2 — round-14 receipt overwrite.** Do not run the historical script at all. The promoted tool must write only the round-15 path (R4). Pin the round-14 receipt sha before and after.
3. **H3 — replay must check `injected_env`.** `decide()` alone accepts `context-missing-env.json` (R2, R3). The replay path must check `environment.injected_env == INJECTED_ENV` and `env_delta_keys == ["GIT_DIR"]` before calling `decide()`, and treat failure as `context_receipt_malformed` (exit 2).
4. **H4 — poison-path branch not hermetic.** `/nonexistent/...` cannot be created without root. Do not claim a selftest case for `poison_path_exists`. Record it as an unexercised branch, or add a test seam (decision D3).
5. **H5 — synthetic probe contract.** A stub `tools/pin-disposition.py` must emit one JSON object with `schema "pin-disposition-v1"`, `status "ok"`, top-level `observed_at`, `tool_sha256` equal to its own disk sha, and exactly six `legs`, each with `pinned.status == "verified"` and `content_status` not `"unavailable"` (`capture-context.py:350–361`; probe rows `pin-disposition.py:406–458`). The fixture's `expected.json` `inputs` must carry the stub's digest and `pin-manifest.json` `derived_from.sha256` must carry the synthetic runner digest. Compute those digests inside the selftest; never reuse round-13/14 bytes.
6. **H6 — isolate the mapping discriminator.** In the synthetic variable-swap case (`REV_BASH` → `REV_CHECKLIST` in one leg call), recompute `derived_from.sha256` after the swap. Otherwise `context_runner_digest_mismatch` masks `context_runner_mapping_mismatch`.
7. **H7 — git control in temp root.** The synthetic lane root needs `git init`; selftest must strip inherited `GIT_*` for its own git commands (`safe_env()` pattern, `:184–187`).
8. **H8 — stable IDs are new code.** `decide()` emits free text (`:559–580`). IDs must be a mapping table over existing reasons, not new predicates. Keep verdicts identical to the historical `decide()`.
9. **H9 — `--help`.** Historical `-h/--help` returns exit 0 (`:607–609`). Either pin it as informational in the selftest or remove it. Do not leave it unpinned.
10. **H10 — guardrail names.** Keep `parse_runner_mapping`, `mapping_block`, `RUN_REGRESSION_RE`, `CHECKS` names in the promoted copy, or re-point round-14's guardrail (R9).

---

## 7. Exit classes and finding IDs (proposal, derived from existing source)

| Exit | Class | Finding ID (stable) | Source origin |
|---|---|---|---|
| 0 | match | `context_match` | `decide()` `ok` branch `:580` |
| 1 | observation mismatch (incl. injected run unusable) | `context_observation_unequal` | `decide()` `:560–563` |
| 1 | payload tool digest ≠ disk | `context_payload_digest_mismatch` | `:564–565` |
| 1 | env delta not exactly GIT_DIR | `context_env_delta_mismatch` | `:566–567` |
| 1 | baseline carries GIT_DIR | `context_baseline_has_git_dir` | `:568–569` |
| 1 | poison control ineffective | `context_poison_control_ineffective` | `:570–571` |
| 1 | probe source digest ≠ r13 declared | `context_probe_digest_mismatch` | `:572–573` |
| 1 | runner digest ≠ manifest declaration | `context_runner_digest_mismatch` | `:574–575` |
| 1 | runner mapping mismatch (leg set/order/checks) | `context_runner_mapping_mismatch` | `:576–577` |
| 2 | could-not-evaluate: one ID per `InvalidContext.kind` | `context_missing_input`, `context_unreadable_input`, `context_invalid_utf8`, `context_invalid_json`, `context_invalid_manifest`, `context_invalid_expected`, `context_invalid_fleet_root`, `context_poison_path_exists`, `context_missing_executable`, `context_timeout`, `context_exec_failed`, `context_non_utf8_output`, `context_runner_unparsed`, `context_probe_baseline_unusable` | `InvalidContext` raises; `main` `:617–628` |
| 2 | cannot write receipt | `context_write_failed` (stderr only, no receipt) | `main` `:631–636` |
| 64 | usage (unexpected argv) | `context_invalid_usage` (no receipt) | `main` `:605–613` |
| 0/1/2 | `--check` replay (new mode) | `context_replay_match` (0), `context_replay_mismatch` (1), `context_receipt_malformed` (2), `context_receipt_tool_digest_mismatch` (2) | new (decision D2) |

Exit-1 findings may be multiple; emit IDs sorted and pin the sorted set in the selftest.

---

## 8. Selftest case proposal (literal exit and ID per case)

Each case runs `sys.executable SELF ...` in a `tempfile.mkdtemp(prefix="tameshi-r15-context-capture-selftest.")` tree containing a copy of the tool at `tools/context-capture.py`, a synthetic `tools/pin-disposition.py`, a synthetic `tools/mutate-and-run.sh` (six header rows, six PIN_/REV_ constants, six `regression_case_git` calls inside `run_regression`), synthetic `.ufo/evidence/round-13/pin-manifest.json` and `expected.json` with computed digests, and `git init`.

| Case | Mutation of fixture | Expected exit | Expected ID |
|---|---|---|---|
| S1 `ok-synthetic` | none | 0 | `context_match` |
| S2 `usage-extra-arg` | argv `["x"]` | 64 | `context_invalid_usage` |
| S3 `missing-probe` | delete stub probe | 2 | `context_missing_input` |
| S4 `invalid-manifest-dup-key` | duplicate JSON key in manifest | 2 | `context_invalid_json` |
| S5 `invalid-manifest-schema` | schema ≠ `pin-manifest-v1` | 2 | `context_invalid_manifest` |
| S6 `probe-baseline-unusable` | stub prints status `invalid_input` | 2 | `context_probe_baseline_unusable` |
| S7 `observation-unequal` | stub echoes `GIT_DIR` into a non-`observed_at` field | 1 | `context_observation_unequal` |
| S8 `poison-control-ineffective` | remove `git init` | 1 | `context_poison_control_ineffective` |
| S9 `probe-digest-mismatch` | edit stub after digests computed | 1 | `context_probe_digest_mismatch` |
| S10 `runner-digest-mismatch` | edit runner without updating manifest | 1 | `context_runner_digest_mismatch` |
| S11 `runner-variable-swap` | `REV_BASH`→`REV_CHECKLIST`, manifest digest recomputed | 1 | `context_runner_mapping_mismatch` |
| S12 `replay-match` | `--check` on S1 receipt | 0 | `context_replay_match` |
| S13 `replay-missing-injected-env` | `--check` on S1 receipt with `injected_env` removed | 2 | `context_receipt_malformed` |
| S14 `replay-tool-digest` | `--check` with tool edited after capture | 2 | `context_receipt_tool_digest_mismatch` |
| S15 `write-scope` | after S1, assert only the temp round-15 receipt exists; no round-14 path | 0 | — (assertion inside S1) |

Not selftested (state as limits): `poison_path_exists` (H4), `context_timeout` (120 s probe budget), `context_write_failed`. Pin them as "not exercised" in the verdict line rather than silently omitting them.

---

## 9. Missing pointers for L1 (exact)

| # | Missing | Where it must land | Why |
|---|---|---|---|
| M1 | `tools/context-capture.py` | `tools/` | No tracked active tool (B1) |
| M2 | Literal exit/ID table in source | tool docstring | §7 |
| M3 | Selftest harness and case literals | tool `--selftest` | §8 |
| M4 | `--check` replay mode and its digest-bound pin | tool + `.ufo/evidence/round-15/context-expected.json` | E9–E11, E18 |
| M5 | Round-15 receipt (`context-receipt.json`) | `.ufo/evidence/round-15/` | E12–E13 |
| M6 | Selftest stdout/exit transcripts | `.ufo/evidence/round-15/selftest*.{stdout,exit}` | E5–E6 |
| M7 | Historical integrity + round-14 sha pins at round-15 baseline | `.ufo/evidence/round-15/historical-integrity.txt` | E0 (current pin list is in §3) |
| M8 | Round-15 SKILL registry section with gate row and four-class verdict map | `SKILL.md` (new `### Round-15 gate/probe registry`) | E14–E15 |
| M9 | Decision on 64 wording (D1) | `SKILL.md` round-15 rows | Routed defect 5 |
| M10 | Measure output at the measured commit (after) and at `a9cf4da` (before) | `.ufo/evidence/round-15/{before,after-committed}.json` | E16–E17 |
| M11 | Source census output if new docs are opened | `.ufo/evidence/round-15/sources-census.txt` | E19 |
| M12 | LOG.md entry | `LOG.md` | E21 (AGENTS.md) |
| M13 | SCORECARD round-15 row | `SCORECARD.md` | E22 |
| M14 | Commit containing tool before measure | git | R10: measure reads committed blobs only |
| M15 | Round-15 guardrail equivalent for the variable-swap discriminator | `.ufo/evidence/round-15/guardrails.json` (new) or re-point | R9 |

---

## 10. Bounded recommendations for L1 (exact)

- **D1 — 64 wording.** Use `64 usage` for `context_invalid_usage` (no receipt; no evaluation attempted). For evidence-disposition, change the round-14 row's "64 usage" to "64 could-not-evaluate (argv refused before evaluation)" in the round-15 section, not by editing the round-14 text. This matches the repeat-control precedent `invalid_usage 64` with the registry note "2 and 64 could-not-evaluate". L1 must choose one wording and pin it; this seat does not decide it.
- **D2 — `--check` mode.** Add one read-only mode that reuses `decide()` unchanged, plus the `injected_env` and `env_delta_keys` checks from H3, and a receipt sha256 pin. Executes nothing. Matches repeat-control's `--snapshot` rule.
- **D3 — poison branch.** Do not add a test seam. Record `poison_path_exists` as an unexercised branch in the selftest verdict line.
- **D4 — round-14 history.** Keep `.ufo/evidence/round-14/capture-context.py` and its receipts untouched. The round-14 registry row (`SKILL.md:1602`) stays as history; the round-15 section supersedes it by explicit reference, not by editing it.
- **D5 — no scalar motion.** Report calibration `6→6`, delta 0, depth `6→6`. Do not add new recorded cases; `tools/mutate-and-run.sh` must keep sha `75ed934d…` and `recorded_cases = 6`.
- **D6 — pins.** Compute and record sha256 of every file the round-15 receipt names (`sources.*`), taken from the measured commit's blobs (`git show REV:path | sha256sum`), not the working tree, so the pinned bytes match committed bytes.
- **D7 — evidence wording.** Describe the round-15 run as "prospective, observed once, not rerun" as round 14 did, and keep "no broad environment independence" and "no retrospective proof of round-13 setup" bounds.

---

## 11. Findings, limits, and blockers

- **F1 (confirmed by source reading):** `tools/context-capture.py` does not exist at `a9cf4da`; C1's "before" is therefore satisfied by absence and the registry text (B1, B3).
- **F2 (confirmed by reading bytes):** `context-missing-env.json` reads `status ok` (R2). A decide-only replay would accept a receipt the round-14 guardrail rejects. H3 and E10 close this.
- **F3 (confirmed by source reading):** the historical LANE_ROOT depth is four and must change to two under `tools/` (R5, H1).
- **F4 (confirmed by source reading):** exit 64 in the historical source is usage only (B4, B7). Registry has no 64 row for the context harness (B4).
- **Limit:** every "after" pass/fail in §5 is future L1 output. This seat has not executed any of it, and it does not predict its results.
- **Limit:** freshness, depth, coverage and operability stay unchanged by design; nothing in this report moves them.
- **Blockers for the seat:** none. Implementation-critical details (H1, H3) were sent to the coordinating peer `TameshiR15`.
- **Tool installs/updates:** none.
