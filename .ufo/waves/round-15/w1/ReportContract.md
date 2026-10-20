# Tameshi round 15 — w1 ReportContract evidence checklist (C1 context gate)

Scope: report-only checklist for the six required report sections and the four SHONEN boxes, built from the files as they exist now. No predicted outcomes. No selftest, capture, build, git verification, or hashing was executed by this seat. Only `read`, `grep`, `glob` and `write` were used. Tool installs/updates: none.

Legend: **Present** = file/line observed by this seat. **Missing** = pointer absent in the lane at read time, so L1 must create or supply it. **[INFERENCE]** = not observed directly.

Read set: `AGENTS.md`; `corpus/lessons/round-14-verifier-spotcheck.md` (Routed defects, lines 154–162); `.ufo/evidence/round-14/capture-context.py` (lines 1–124, 127–130, 145–155, 184–260, 264–338, 340–412, 465–647; `base_receipt`/`validate_manifest` at 414–464 not read); `SKILL.md` 1502–1607; `SHONEN.md`; `.ufo/reports/round-14/tameshi.md`; `LOG.md` 837–919; `.ufo/evidence/round-14/guardrails.json`, `context-receipt.json`; `.ufo/evidence/round-15/claims.json`; `.ufo/waves/round-15/spec1.json`; `tools/` listing; `tools/pin-disposition.py` (probe status vocabulary only); PROTOCOL Gate standard at `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:388-437` (read-only, outside lane).

Mapping to the six round-report sections (round-14 format): Work performed = §1 · Landed changes = §3 · Before→after measurements = §5 (C1 evidence) · Sources & frontier = §3 missing rows · Trend verdicts = §5 · SHONEN = §7. The six scribe returns are §1–§6 below.

---

## §1 Behavior (Work performed) — what the historical instrument actually does

| # | Observation | Pointer | Status |
|---|---|---|---|
| B1 | CLI accepts only `-h/--help` (exit 0). Any other argv prints usage and returns **64**. No `--selftest`, no `--root`, no `--check`, no `--snapshot`. | `capture-context.py:605-613`, `USAGE` 117-124 | Present |
| B2 | Writes one receipt at the **round-14** path, atomically (tempfile → fsync → `os.replace`). Re-running overwrites it. | `OUTPUT_REL` line 58; `write_receipt` 583-602 | Present |
| B3 | Lane root is derived by **four** `dirname` calls from the script path. That is correct only for `.ufo/evidence/round-14/`. For `tools/context-capture.py` the correct depth is **two**; copying the literal would point LANE_ROOT at the wrong directory. | `capture-context.py:45-47` | Present |
| B4 | FLEET_ROOT = `dirname(LANE_ROOT)`. The probe reads the sibling fleet via `--root FLEET_ROOT`. A selftest that does not redirect this reads live sibling repos. | lines 47, 538 | Present |
| B5 | Exit-2 "kinds" are **existing stable tokens** (`InvalidContext.kind`). These are the only stable identifiers in the tool. | `read_lane_bytes` 145-155; `parse_json` 167-181; `run_bounded` 190-210; `parse_runner_mapping` 213-256; `evaluate` 465-550 (`poison_path_exists` 471, `invalid_fleet_root` 474, `invalid_expected` 492, `invalid_manifest` 495, `invalid_utf8` 514); `probe_baseline_unusable` 359; `missing_executable` 520/522 | Present |
| B6 | Exit-1 reasons are **free text** from `decide()` (no IDs). Mapping reasons are also free text (`leg X: ...`). | `decide` 553-580; `mapping_block` 315-323 | Present |
| B7 | `main()` write-failure path returns 2 with **stderr only** (no token). | 631-636 | Present |
| B8 | Positive control runs `git -C LANE_ROOT rev-parse --git-dir` twice (baseline env, then injected `GIT_DIR`). Effective requires baseline exit 0 with non-empty stdout, injected exit ≠ 0, and poison text reflected. A non-git synthetic lane therefore reports `git poison positive control is ineffective` (exit 1) for the wrong reason. | `positive_control_block` 395-411; `decide` 570-571 | Present |
| B9 | Baseline probe must be a six-leg `ok` `pin-disposition-v1` document where every leg has `pinned.status == verified` and `content_status != unavailable`, plus `observed_at`. Otherwise exit 2. A clean synthetic fixture therefore needs six canonical sibling repos with pinned blobs that hash to the manifest values. | `comparison_block` 352-357; `evaluate_leg` 406-435 in `pin-disposition.py` | Present for the check; **[INFERENCE]** for exact canonical repo/path layout — executor must read `pin-disposition.py` `CANONICAL_BY_LEG` before fixture design (not read in full here) |
| B10 | `runner` parse needs exactly six header rows, six `PIN_`, six `REV_` constants and six `regression_case_git` calls inside `run_regression`. The synthetic runner must be generated from the manifest, not copied from the live runner, to honour "no live reads". | 213-256, 259-337 | Present |
| B11 | Historical `context-receipt.json` records `tool_sha256 = 7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, `status: ok`, `exit: 0`, `observed_at 2026-10-20T06:35:01Z`, `result_reuse: not_established`. | `.ufo/evidence/round-14/context-receipt.json:3-4,414-423` | Present. **Missing check**: disk digest of `capture-context.py` equals 7313e9… — not hashed by this seat; L1 must confirm |

## §2 Gates — classification and conformance

| # | Finding | Pointer | Status |
|---|---|---|---|
| G1 | Registry classifies `invocation context capture` as **probe**, with **no standalone selftest**. The tool emits `mismatch`/exit 1 against persisted expectations (round-13 manifest digest, expected.json digests). Under Gate standard "Verdict" + "Self-test", this is a **gate**. | `SKILL.md:1602`; `decide` 553-580; `PROTOCOL.md:388-402` | Present (defect confirmed by lesson routed defect 5) |
| G2 | Registry verdict map for the context row is `0/1/2` only. Exit 64 is "usage" in the docstring/USAGE, not mapped. Gate standard requires every declared nonzero code to be mapped to `clean | failed | could-not-evaluate`. | `SKILL.md:1602`; `capture-context.py:26-29,123` | Present |
| G3 | Precedent for mapping 64: `knowledge/repeated-control-precondition.md:40-45` maps invalid usage to exit 64 and setup_error/command_unavailable/baseline_nonzero to exit 2, all could-not-evaluate; `SKILL.md:1503` states "2 and 64 could-not-evaluate" for repeat-control; `SKILL.md:1504` gives `64 usage/could-not-evaluate` for bash-witness-study. Use the same wording for the new context row. | `SKILL.md:1503-1504`; `corpus/knowledge/repeated-control-precondition.md:40-45`; `tools/repeat-control.py:44-48` | Present |
| G4 | Disposition gate registry row also reads `2 could-not-evaluate ...; 64 usage` with no could-not-evaluate label for 64. Tool bytes (`evidence-disposition.py:69,131`) say "64 usage error". Registry-only fix; no tool change needed. | `SKILL.md:1601`; `tools/evidence-disposition.py:66-69,120-135` | Present |
| G5 | Gate standard "Two evidences": a gate whose verdict depends on mutable fleet artifacts ships a run over a committed input snapshot. `expected.json` must pin the digest of every snapshot input; an edited snapshot is `snapshot_tampered` (could-not-evaluate). The context verdict depends on live fleet/git state, so snapshot mode is required. | `PROTOCOL.md:403-410`; precedent `SKILL.md:1503` (`repeat-control.py --snapshot`) | Present (protocol); **Missing**: any round-15 snapshot directory or expected.json |
| G6 | Self-test must invoke actual CLI, use isolated fixtures, and check literal expected exit + finding ID. A helper-only control does not satisfy the clause. The guardrails `context_setup_missing_field` and `runner_variable_swap_discriminator` are helper/script-level controls and remain evidence only. | `PROTOCOL.md:398-402`; `guardrails.json:20-48` | Present |
| G7 | Historical round-14 bytes must remain unedited. `guardrails.json` `historical_integrity` diffs the round-12/13 evidence trees, not round-14 `capture-context.py`; the round-14 tool's own bytes are protected only by its recorded `tool_sha256`. | `guardrails.json:49-72`; receipt line 4 | Present |

## §3 Touched surfaces — current state

**Present (keep byte-identical unless the report says otherwise):**
- `.ufo/evidence/round-14/capture-context.py` (historical, do not edit).
- `.ufo/evidence/round-14/context-receipt.json`, `context-missing-env.json`, `guardrails.json`, `verification.json`, `verification-final.json`, `expected-runtime*.json`, `dispositions*.json`.
- `SKILL.md` round-14 section 1563–1607 (decision table, recipe steps 1–5, registry at 1599–1602).
- `SHONEN.md` lines 5, 7, 10, 11 (four `[~]` boxes; lines 6, 8, 10 are citations).
- `.ufo/evidence/round-15/claims.json` (C1 declaration: calibration 6→6, capability, no promotion points).
- `.ufo/waves/round-15/spec1.json` and `w1/swarm-registry.json`.
- `tools/` contains: `evidence-disposition.py`, `pin-disposition.py`, `witness-metadata.py`, `bash-witness-study.py`, `repeat-control.py`, `mutate-and-run.sh`.

**Missing pointers for L1 (must be created or supplied; none exist at read time):**

| Missing pointer | Why L1 needs it |
|---|---|
| `tools/context-capture.py` | The new active gate. Its absence is confirmed by the `tools/` listing. |
| `.ufo/evidence/round-15/` expected/snapshot (`expected.json`, snapshot inputs) | Digest-bound snapshot mode (G5). Only `claims.json` exists in round-15 evidence. |
| `.ufo/evidence/round-15/` retained receipt and selftest transcript | Proof of the integrated run. Not created by this seat. |
| `SKILL.md` round-15 section and registry row(s) | No round-15 entries exist. Grep of `SKILL.md`, `corpus/`, `reports/`, `plans/`, `LOG.md` and `SCORECARD.md` for round-15/R15/context-capture finds no round-15 hits. |
| `LOG.md` round-15 entry | `AGENTS.md:3` requires a LOG entry with motivating evidence for every change. The latest entries are round-14 (`LOG.md:837–919`). |
| `.ufo/reports/round-15/tameshi.md` | The lane report (L1 writes it). Only the round-14 report exists. |
| `corpus/lessons/round-15-*.md` | Not present. |
| Lane-local `PROTOCOL.md` | Not present in the tameshi root. The Gate standard resolves only at `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` (read-only). Cite that path explicitly. |

## §4 Out-of-scope items (do not touch)

- Successor sweep, seventh mutation case, scalar change, promotion, SHONEN edit, PROVINCE edit, source-row changes beyond what the lane already has.
- Historical `capture-context.py` bytes, round-14 receipts and round-12/13 evidence trees.
- `evidence-disposition.py` code. Only its registry label changes (G4).
- `pin-disposition.py` probe row (`SKILL.md:1552`) has exit map 0/2 only. Under the Gate standard an undeclared code reads as could-not-evaluate. This is a separate probe; the routed defect does not cover it. Leave unchanged and note it only.
- No installs. `pacman` dry-run and tool procedures apply only if a tool is needed later; none was needed.

## §5 Findings and before→after evidence (C1)

**Routed defects from `round-14-verifier-spotcheck.md:160`, with status against current files:**

| Defect | Current state | Evidence pointer |
|---|---|---|
| D1 classification probe → gate | Still probe (open) | `SKILL.md:1602` |
| D2 standalone isolated self-invocation with literal exit + finding pairs | Absent (open). The only selftests are for other tools. | `SKILL.md:1602` ("no standalone selftest") |
| D3 map exit 64 explicitly to could-not-evaluate | Open. Registry omits 64 for the context row. | `SKILL.md:1602`; `capture-context.py:123` |
| D4 declare the context harness 64 path (present in source, absent from registry) | Open. | `capture-context.py:605-613` vs `SKILL.md:1602` |

**Proposed exit and finding map (for the executor; the exact names are a recommendation, not an observation):**

| Class | Exit | Stable ID (proposed) | Source of the condition |
|---|---|---|---|
| clean | 0 | `context_consistent` | `decide` returns `ok` |
| failed (mismatch) | 1 | one of: `injected_observation_differs`, `payload_tool_sha256_mismatch`, `env_delta_undeclared`, `baseline_has_GIT_DIR`, `git_control_ineffective`, `probe_source_digest_mismatch`, `runner_source_digest_mismatch`, `runner_mapping_mismatch` | the eight predicates in `decide` lines 560–577 (one-to-one) |
| could-not-evaluate (input/setup) | 2 | existing tokens: `missing_input`, `unreadable_input`, `invalid_json`, `invalid_utf8`, `invalid_expected`, `invalid_manifest`, `invalid_fleet_root`, `poison_path_exists`, `missing_executable`, `exec_failed`, `timeout`, `non_utf8_output`, `runner_unparsed`, `probe_baseline_unusable`; new: `receipt_write_failed`, `snapshot_tampered` | `InvalidContext` kinds (B5) and G5 |
| usage (could-not-evaluate in registry) | 64 | `invalid_usage` | `main()` 605-613 |

Order matters in `evaluate()`: `poison_path_exists` (471) precedes `invalid_fleet_root` (474). Selftest pins must respect this order.

Measured counts of existing tokens are not claimed. The `validate_manifest` body (439–462) was not read, so its exact kinds are unverified.

## §6 Artifact paths and what each proves

| Artifact | Proves | Does not prove |
|---|---|---|
| `.ufo/evidence/round-14/context-receipt.json` | Historical round-14 run recorded `ok`, exit 0, `GIT_DIR` injection, mappings all true | Round-13 context setup retroactively; broad environment independence |
| `.ufo/evidence/round-14/guardrails.json` | Four discriminator checks against the round-14 receipt and helper | Gate standard self-test (it is helper-level, not CLI selftest) |
| `.ufo/evidence/round-15/claims.json` | Declared C1 before/after strings | Any executed result |
| `tools/context-capture.py` (missing) | Would prove the gate after L1 runs `--selftest` and `--snapshot` | Nothing until executed |

Retained-receipt check and snapshot tampering must be exercised by L1, not by this seat.

## §7 SHONEN — four restrained boxes

All four remain `[~]` (lane assertion, no independent promotion verifier). This seat recommends no promotion.

| Box (`SHONEN.md` line) | Evidence present now | Missing for round 15 | Restrained recommendation |
|---|---|---|---|
| 1. SKILL.md decision tables, error patterns, checklists, sources (5) | Round-14 section `SKILL.md:1563–1607` (decision table, recipe, registry). Round-14 report cites S049/S050. | Round-15 registry row for the context gate and the 64 mapping; any round-15 lesson; explicit supersession note for "opt-in prospective probe" (`SKILL.md:1592-1595`). | Keep `[~]`. Add the registry row and supersession note by append only. |
| 2. End-to-end domain task executed and logged (7) | Round-14 `LOG.md:837–919`. | Round-15 `LOG.md` entry; L1 run record of `--selftest`/`--snapshot` and a retained round-15 receipt. | Keep `[~]` until L1 runs the gate once and logs it. |
| 3. Instructions executable without oral context (10) | `reports/round-1-kaika-coldread.md` (round-1 appendix A/B only). Round-14 says box 3 is unscored. | Cold-read of the new round-15 registry row and tool usage text. | Keep `[~]`. Do not extend the claim to the full SKILL page. |
| 4. No cross-domain bleed, PROVINCE.md accurate (11) | Round-14 lesson: PROVINCE.md unchanged, sibling reads only (`corpus/lessons/round-14-verifier-spotcheck.md:115`). | Round-15 statement that writes stayed within the tameshi tree (tools, SKILL, `.ufo/evidence/round-15`, LOG, report). | Keep `[~]`. L1 checks write scope only (no sibling gate execution). |

## §8 Exact bounded recommendations for L1

1. **Create `tools/context-capture.py`** as a new file. Do not edit `.ufo/evidence/round-14/capture-context.py`. Derive `LANE_ROOT = dirname(dirname(realpath(__file__)))` (depth two, not four). Keep `FLEET_ROOT = dirname(LANE_ROOT)`. Redirect both through a `--root` argument used by selftest children.
2. **Output path**: change `OUTPUT_REL` to `.ufo/evidence/round-15/context-receipt.json` only. The round-14 receipt is never overwritten.
3. **Subcommands**: keep the normal capture. Add `--selftest` (isolated `tempfile` fixtures only, child processes running the public CLI, literal expected exit/ID pairs). Add `--check RECEIPT` (re-applies `decide()` and structure checks to a retained receipt, read-only, no git or probe). Add `--snapshot DIR` (digest-bound: `expected.json` pins a sha256 for every snapshot input, plus expected ID and exit; tampered input → `snapshot_tampered`, exit 2).
4. **Stable IDs**: add finding IDs for the eight `decide()` predicates and the mapping reasons without changing predicate semantics. Keep the free-text reason as a detail field.
5. **Exit 64**: `invalid_usage`, documented in the registry as could-not-evaluate. Do not change the tool's own exit 64.
6. **Selftest cases** (exact pairs to pin; the executor decides the fixture, but each must be listed): clean → 0/`context_consistent`; one each for the eight mismatch predicates → 1; each `InvalidContext` kind → 2; usage → 64; `snapshot_tampered` → 2. The clean case needs a synthetic six-leg fleet and a synthetic runner generated from the manifest [INFERENCE — confirm with `pin-disposition.py` `CANONICAL_BY_LEG`].
7. **Registry (`SKILL.md`)**: add a round-15 section. Change the context row to `gate`, with entry `python3 tools/context-capture.py`, self-test `python3 tools/context-capture.py --selftest`, verdict map `0 clean; 1 failed; 2 could-not-evaluate; 64 could-not-evaluate (usage)`. Add the same 64 label to the disposition row. Supersede the round-14 "probe" text by append only.
8. **Evidence**: L1 runs `--selftest` once and captures one round-15 receipt. Record exit codes and finding IDs in the round-15 report. No seat runs them.
9. **Log**: add a `LOG.md` round-15 entry with motivating evidence (round-14 routed defect 5, `SKILL.md:1602`, `capture-context.py:605-613`).
10. **Report**: write `.ufo/reports/round-15/tameshi.md` with the six sections in order (Work performed, Landed changes, Before→after measurements, Sources & frontier, Trend verdicts, SHONEN), each box `[~]`.

## Tool installs/updates

None. This seat used only `read`, `grep`, `glob` and `write`. No checks, builds, tests, formatters, git commands or hashing were run.

## Blocker or implementation-critical detail sent to TameshiR15

Sent separately (see the message log). Summary: the four-level `LANE_ROOT` derivation must not be copied; the baseline probe needs six verified legs before any clean fixture can pass.
