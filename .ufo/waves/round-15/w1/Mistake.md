# Mistake — round 15 wave 1: gate-misclassification checklist

**Axes:** calibration (primary; C1 lowest tied axis). **Authority:** lane-local evidence mining and checklist only. Not an admission, gate verdict, promotion, or independent review. Status is `[INFERENCE]` wherever a point was derived from source reading and not executed.

**Execution boundary:** nothing was executed. No gate, selftest, probe, runner, or repo script was run. Actions taken: file reads, `sha256sum`, `git status`/`git log` (read-only), and string-only `os.path` arithmetic. Sibling peer reports in this wave (`GateClassification.md`, `OutsideAuthority.md`) were not read, to keep this seat independent. Tool installs or updates: **none**. `~/.omp/agent/RULES.md` was read; no helper was needed.

## 1. Failure-backed mistakes (mined from files)

| ID | Mistake | Evidence (file:line, lane-relative) | Fix already landed or open |
|---|---|---|---|
| M1 | Gate classified as probe. `capture-context.py` compares digests and runner mapping against committed round-13 pins, and `decide()` returns `mismatch`/exit 1. The registry labels it `probe` with "no standalone selftest". | `.ufo/evidence/round-14/capture-context.py:476-515` (pins), `:553-580` (decide, exit 1). `SKILL.md:1602` (registry row, kind `probe`). `PROTOCOL.md:377-389` (Gate standard: a tool that can fail is a gate; self-test must be a standalone self-invocation). `corpus/lessons/round-14-verifier-spotcheck.md:160` (Routed defect 5). | Open. Routed to round 15 (`corpus/lessons/round-15.md:45`). |
| M2 | Exit-class mapping incomplete. `capture-context.py` returns 64 for unexpected arguments, but its registry row lists only 0/1/2. The disposition gate's row says "64 usage" without mapping it to a class. `PROTOCOL.md:380-382` requires every nonzero code to map onto clean/failed/could-not-evaluate. | `capture-context.py:605-613` (returns 64). `SKILL.md:1602` (no 64). `SKILL.md:1601` ("64 usage"). `evidence-disposition.py:1932,1941` (returns 64). | Open. Routed as item 5, second half; planned in `round-15.md:46`. |
| M3 | Helper-only checks recorded as self-invocation. The three guardrail controls never execute the CLI: two parse the receipt JSON with `python3 -c`, one imports the script with `runpy` and calls its functions. | `.ufo/evidence/round-14/guardrails.json` checks `context_setup_positive`, `context_setup_missing_field`, `runner_variable_swap_discriminator`. `PROTOCOL.md:385-389` ("a helper-only or model-only self-check does not satisfy this clause"). | Stands as historical evidence. Does not satisfy the gate clause. |
| M4 | Exit agreement treated as mechanism proof. Round-13 `producer_before` exited 1 from a `FileNotFoundError` before its assertion. The same class of error exits 1 uncaught, so exit code alone cannot distinguish them. | `corpus/lessons/round-14-verifier-spotcheck.md:98,123-125`. `SKILL.md:1572`. `tools/repeat-control.py:48` (same hazard, documented). | Addressed by the round-14 disposition gate. Applies to any new selftest: exit plus stable finding ID, both asserted. |
| M5 | Failing selftest run must stay retained. `evidence-disposition.py --selftest` failed 18/34 at `0c6e36d` and passed 34/34 at `6431478`. | `.ufo/evidence/round-14/verification.json` (`disposition_selftest` exit 1), `verification-final.json` (exit 0). Commit `6431478` subject "retain failing run and repair two selftest fixtures". | Closed in round 14. Checklist keeps the same rule for the new selftest: keep any initial failure. |
| M6 | Path-root derivation breaks on promotion. `LANE_ROOT` is `dirname` applied four times to `__file__`, which only works at `.ufo/evidence/round-14/`. `FLEET_ROOT` follows from it. | `capture-context.py:45-47`. String arithmetic: the four-level formula on the historical path gives `…/tameshi-shokunin` (correct). The same formula on `tools/context-capture.py` gives `/home/vgpnk/Projects` (wrong). Two levels is correct. `[INFERENCE]` until L1 runs the promoted selftest. | Open. Promotion must change this derivation. |
| M7 | No stable finding IDs. `decide()` emits free-text reason strings. Only `InvalidContext.kind` values are stable identifiers. | `capture-context.py:127-131` (`InvalidContext`), `:561-577` (reasons), `:618-620,629-630` (output). `PROTOCOL.md:385-388` (stable expected finding-id required). | Open. |
| M8 | Output path hard-coded to round 14, and writes overwrite. `write_receipt` uses `os.replace`, so a re-run silently replaces the file. | `capture-context.py:58` (`OUTPUT_REL` round-14), `:583-602` (atomic replace). | Open. A round-15 writer must refuse to overwrite and must never touch round-14. |
| M9 | No root override. Every input and output path derives from `__file__`. The required isolated CLI selftest therefore has no documented way to redirect inputs without copying the tree. | `capture-context.py:45-47,54-58,141-142`. `SKILL.md:1595` (described only as a probe). | Open. Decision for ContextGate (see R1). |
| M10 | Snapshot mode is required by the gate standard but absent. Verdict depends on mutable runner, probe, manifest, and expected files. `PROTOCOL.md:390-397` requires a digest-pinned snapshot run for that case. | `capture-context.py:476-479`. `PROTOCOL.md:390-397` ("Two evidences"). The receipt stores probe stdout (`runs.baseline/injected.stdout`), `positive_control`, `comparison`, `mapping`, and `environment`, so `decide()` can be recomputed from the receipt alone. It does **not** store runner or probe bytes, only their digests (`sources.*.sha256`), so a mapping cannot be re-derived offline. | Open. Decision for L1 (see R5). |
| M11 | Positive control depends on git in the lane. `positive_control_block` runs `git rev-parse --git-dir` at `LANE_ROOT`. In a synthetic temp tree without `git init`, the control is ineffective and the run exits 1 for the wrong reason. | `capture-context.py:395-411`, `:524-547`. | Open. Selftest fixtures must `git init` the temp lane. |
| M12 | Ambient environment leaks into the record. `ambient_git_keys_removed` reflects the caller's `GIT_*` variables. | `capture-context.py:184-187,466-469`. `[INFERENCE]` that a selftest asserting this field would be host-dependent. | Selftest must not assert host-dependent fields. |
| M13 | Help text returns exit 0 with no receipt, which the gate standard reads as `clean`. | `capture-context.py:605-609` (`-h`/`--help` → 0). `PROTOCOL.md:380` (0 = clean). | Open. Declare it in the registry or change it (see R2). |

## 2. Evidence checklist for L1 (run once after seats return; do not run now)

Each item is checkable from files. Pass conditions are stated.

- **C1 Historical bytes preserved.** `sha256sum .ufo/evidence/round-14/capture-context.py` = `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` (observed by this seat; matches `context-receipt.json` `tool_sha256` and `verification-final.json` `inputs`). `git diff --name-only` for `.ufo/evidence/round-14` is empty. Historical `context-receipt.json` and `context-missing-env.json` unchanged.
- **C2 Probe and runner digests recorded.** Observed this seat: `tools/pin-disposition.py` = `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`; `tools/mutate-and-run.sh` = `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; `.ufo/evidence/round-13/pin-manifest.json` = `64eaa43e…2920af6`; `.ufo/evidence/round-13/expected.json` = `a016079438e96f39…5e09394336`. **Not compared by this seat:** whether `sources.probe.sha256` in the receipt equals the probe digest above. L1 must compare.
- **C3 New tool exists.** `tools/context-capture.py` present with `--selftest`. Currently **absent** (checked: `ls tools/` lists six tools, none context-related).
- **C4 Historical `--selftest` invocation recorded separately.** Source predicts the historical script exits 64 with usage on `--selftest` (`capture-context.py:610-613`). `[INFERENCE]`. L1 may record this as an observed artifact in the round-15 evidence directory; the historical bytes must not be edited.
- **C5 Selftest asserts exit and stable finding ID.** Every case asserts both. Literal expectations live in the tool, not computed from the code under test (`PROTOCOL.md:385-388`). Cases invoke only public CLI subprocesses against isolated temp trees. No live path, network, or write outside temp roots.
- **C6 Coverage of each verdict class.** At minimum, one case each for: clean (0); observation mismatch (1); payload digest mismatch (1); env delta mismatch (1); baseline has `GIT_DIR` (1); positive control ineffective (1); probe-digest mismatch (1); runner-digest mismatch (1); mapping mismatch (1); each `InvalidContext` kind (2); poison path exists (2); usage (64); help (declared, see R2). If snapshot mode is adopted: snapshot-tampered (2) and recomputed mismatch (1).
- **C7 Registry row round 15.** A new `SKILL.md` section and gate row with: kind `gate`; entry command; verdict map with 64 → could-not-evaluate; self-test command; pinned values; write scope; owner `tameshi`. Pre-existing round-14 rows are not rewritten, since errata are append-only; a supersession note cross-references them.
- **C8 No overwrite.** `.ufo/evidence/round-15/context-receipt.json` is absent before the run (currently **absent**: only `claims.json` exists). Round-14 `context-receipt.json` is byte-identical after the run.
- **C9 Retained run.** One integrated run of the promoted tool's selftest and one prospective capture, each retained with exit and stdout. Initial failures, if any, retained (M5 rule).
- **C10 Documentation pointers.** `corpus/QUALITY.md` contains a QUALITY17 entry that cites M1/M2 (currently an uncommitted working-tree edit; L1 confirms its text). `LOG.md` gets a round-15 entry with motivating evidence (`AGENTS.md`: every change appends a LOG entry). `corpus/SOURCES.md` diff is status-only or append-only (currently uncommitted; L1 confirms).
- **C11 Helper-only controls not counted.** The round-14 guardrail checks are cited as historical evidence only. They are not counted as the standalone self-invocation.

## 3. Missing pointers for L1 (exact, as observed now)

| Missing | Checked how | Needed by |
|---|---|---|
| `tools/context-capture.py` | `ls tools/` | C3 |
| Round-15 section and gate row in `SKILL.md` | `grep -n 'round.15' SKILL.md` → no hits | C7 |
| `.ufo/evidence/round-15/` retained receipts, selftest transcript, expected file | directory contains only `claims.json` | C8, C9 |
| `LOG.md` round-15 entry | `grep -n 'round 15\|round-15' LOG.md` → no hits | C10 |
| `SCORECARD.md` round-15 measurement | no hits | scorecard closure (not this seat) |
| `corpus/QUALITY.md` QUALITY17 text | present in working tree only (`git status`: modified) | C10 |
| Outside verifier for round 15 (`corpus/lessons/round-15-verifier-spotcheck.md`) | absent | admission (not L1 precondition) |
| Declared 64 mapping for `evidence-disposition.py` row | `SKILL.md:1601` reads "64 usage" | M2 |
| Declaration of `-h`/`--help` exit 0 | no registry mention | M13 |
| Receipt `sources.probe.sha256` vs the probe digest in C2 | not compared by this seat | C2 |

## 4. Bounded recommendations

- **R1 — root override (ContextGate decision).** Prefer a selftest that builds a temp lane containing `tools/context-capture.py` at the two-level layout, with synthetic `tools/pin-disposition.py` (stub emitting an `ok` `pin-disposition-v1` document; an injected variant that changes output under `GIT_DIR`), `tools/mutate-and-run.sh` with six header rows, six `PIN_`/`REV_` constants, six `regression_case_git` calls, `pin-manifest.json`, `expected.json`, and `git init`. This keeps the CLI surface unchanged. An explicit `--root` flag is the alternative; it adds public surface and needs a write-scope statement.
- **R2 — exit map.** Declare exits: 0 clean; 1 failed; 2 could-not-evaluate (every `InvalidContext.kind`, including `poison_path_exists`); 64 could-not-evaluate (usage). For `-h`/`--help`: either declare "usage text, no verdict, no receipt" in the registry, or change help to 64. L1 chooses one and cites it.
- **R3 — finding IDs.** Keep `InvalidContext.kind` as the stable IDs for exit 2. Add fixed IDs for `decide()` reasons (for example `context_clean`, `comparison_mismatch`, `payload_digest_mismatch`, `env_delta_mismatch`, `baseline_has_git_dir`, `positive_control_ineffective`, `probe_source_digest_mismatch`, `runner_source_digest_mismatch`, `mapping_mismatch`, `invalid_usage`). Keep free text as detail. Selftest pins the exact ID strings.
- **R4 — selftest shape.** Model on `tools/evidence-disposition.py` (`--selftest` at `:1510-1857` runs `SELF` as subprocess, `:1831`). Print `SELFTEST_CASE <name> PASS|FAIL (exit=… expects=…)` and `SELFTEST: PASS (n/m)`. Exit 0 on pass, 1 on failure, following that tool's convention.
- **R5 — snapshot mode (required by the gate standard).** Add `--snapshot DIR` (or `--check RECEIPT`) that copies the runner, probe, manifest, and expected bytes into the snapshot, pins each with a sha256 in a `snapshot.json`, and recomputes `decide()` from stored `runs.*.stdout`. Digest mismatch → exit 2 `snapshot_tampered`. Recomputed verdict differs from recorded → exit 1. This follows `tools/repeat-control.py` `--snapshot` semantics (`corpus/knowledge/repeated-control-precondition.md:52`). Without stored runner bytes, mapping cannot be re-derived, so the snapshot must store them.
- **R6 — output.** Write only `.ufo/evidence/round-15/context-receipt.json`. Refuse if it exists (exit 2 with an ID). Never touch round 14. Keep atomic write.
- **R7 — registry correction.** Append a round-15 row; do not rewrite the round-14 `probe` row. Add one supersession line citing M1 and M2, so both records remain readable.
- **R8 — no new claims.** Keep `not_compared` and `result_reuse: not_established` fields. Do not claim environment independence, safe result reuse, suite execution, or any sweep.

## 5. Falsification

- A selftest case that asserts only exit code fails C5 (M4).
- A "snapshot" that reads the live runner or probe fails R5 and C6.
- A promoted tool whose `LANE_ROOT` resolves outside the tameshi tree fails M6, regardless of selftest result.
- Any edit to `.ufo/evidence/round-14/` or to historical `capture-context.py` bytes fails C1.

## 6. Artifacts

- This report: `.ufo/waves/round-15/w1/Mistake.md` (only write by this seat).
- Sources read: `AGENTS.md`, `corpus/lessons/round-14-verifier-spotcheck.md`, `corpus/lessons/round-15.md`, `SKILL.md` (lines 17–30, 58–70, 1517–1607), `.ufo/evidence/round-14/{capture-context.py, context-receipt.json, context-missing-env.json, guardrails.json, verification.json, verification-final.json, verification-verdict.json, expected-runtime-final.json}`, `tools/{pin-disposition.py, evidence-disposition.py, repeat-control.py, witness-metadata.py, mutate-and-run.sh}` (targeted lines), `corpus/QUALITY.md`, `PROTOCOL.md:375-410` (fleet root), `.ufo/waves/round-15/{spec1.json, assignments1.json}`.
- No runtime evidence exists for any item above; every "passes" is the checklist to be run by L1.
