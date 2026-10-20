# ReviewMapping — planned C1 against mapping false exit1

Lane: tameshi-shokunin · Wave: tameshi-r15-w1 · Seat: TameshiR15.ReviewMapping (reviewer, leaf)
Scope: review of the planned round-15 C1 context gate (`tools/context-capture.py`) for mapping-driven false exit 1.

## Read revision and evidence state

- Lane HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (round-14 verifier spot-check). Baseline in `.ufo/evidence/round-15/claims.json` is the same revision.
- Worktree at read time is dirty and not mine: `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` modified; `.ufo/evidence/round-15/`, `.ufo/waves/round-15/`, `corpus/lessons/round-15.md` untracked.
- **`tools/context-capture.py` does not exist at this revision or in the worktree** (`ls`: no such file). No new source was reviewed. Everything below is against the historical source `.ufo/evidence/round-14/capture-context.py` (sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, matching the `tool_sha256` in the retained receipt) and the retained round-14 receipts.
- No gate, selftest, probe, or capture was executed. Reads were file views, `grep`, and read-only `sha256sum` / `git rev-parse HEAD` / `git status --porcelain`. Labels: **[OBSERVED]** = read from bytes; **[SOURCE-DERIVED]** = follows from reading code, not executed; **[INFERENCE]** = unobserved.
- Tooling: none installed or updated.

Digests read (observed):

| File | sha256 |
|---|---|
| `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` |
| `.ufo/evidence/round-14/context-missing-env.json` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` |
| `.ufo/evidence/round-14/guardrails.json` | `cca670b54f5da70873daec8d1bd54749ea63be99582f21138d43c8c715eaf784` |
| `.ufo/evidence/round-13/expected.json` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` |
| `.ufo/evidence/round-13/pin-manifest.json` | `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` |
| `tools/pin-disposition.py` | `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` |
| `tools/mutate-and-run.sh` | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |

The receipt's recorded probe, runner, manifest and expected digests equal these current bytes **[OBSERVED]**.

## How mapping can currently return exit 1 (historical source)

Exit 1 is the single code for "mismatch". In the historical script `decide()` (`capture-context.py:553-580`) returns 1 when any of these hold:

1. `comparison.equal` is not true (`:560-563`), including "injected probe run produced no JSON" and "no top-level observed_at" (`:371-379`).
2. `payload_tool_sha256_matches_disk` is not true (`:564-565`).
3. `environment.env_delta_matches_declared` is not true, or baseline has `GIT_DIR` (`:566-569`).
4. `positive_control.effective` is not true (`:570-571`).
5. `sources.probe.matches_declared` is not true (`:572-573`).
6. `sources.runner.matches_manifest_declaration` is not true (`:574-575`).
7. `mapping.all_match` is not true (`:576-577`), appending mapping reasons.

Mapping-specific exit-1 surface (`mapping_block`, `:259-337`):

- Six per-leg checks, `CHECKS` at `:109-115`: `header_matches_manifest`, `pin_name_and_value_match_manifest`, `rev_name_and_value_match_manifest`, `leg_call_matches_manifest`, `constant_names_match_leg`.
- Set equality and **order equality** of runner legs against manifest legs (`:313-319`), folded into `all_match` (`:335`).
- Variable names are checked against a hard-coded table `EXPECTED_SUFFIX` (`:74-81`), not against the manifest.
- Parse-shape failures are exit 2, not 1: header count ≠ 6, call count ≠ 6, pin/rev constant count ≠ 6, leg-name set mismatch, unparseable `run_regression` body (`parse_runner_mapping`, `:213-256`, raises `runner_unparsed` at `:219-253`), all via `InvalidContext`.

`evaluate()` ordering matters: the mapping is computed (`:515`) before the probe runs (`:538-540`), but `decide()` is reached only after `comparison_block` (`:548-550`). A baseline probe that is unusable raises `probe_baseline_unusable` (exit 2, `:351-361`) **before** any mapping verdict can be issued. Therefore **every mapping fixture needs a usable six-leg probe baseline** (see recipe below).

## Likely false exit 1 — ranked

**F1. Benign leg reorder → exit 1 (`runner leg order differs from manifest`).** [SOURCE-DERIVED] `:313-319`, `:335`. Each of the six bindings can be correct while the runner reorders its six `regression_case_git` calls; exit 1 results. Whether that is "false" depends on whether order is a binding claim. Reuse mandates "reuse decide/comparison/mapping semantics", so keep order-binding, but the acceptance must say so and pin it with a literal finding ID. A silent change to order-insensitive comparison is a semantic change and must not be smuggled in. Current runner order equals manifest order **[OBSERVED]** (receipt `mapping.runner_leg_order` = `manifest_leg_order`).

**F2. Any byte change to `tools/mutate-and-run.sh` → exit 1 even when all six mappings match.** [SOURCE-DERIVED] `evaluate` `:504-509` sets `matches_manifest_declaration` from the file's full SHA-256; `decide` `:574-575` makes it fatal. A comment-only or whitespace-only runner edit yields exit 1 with a mapping that is value-for-value equal. Under pinned-source semantics this is a source-pin drift, and that is correct behavior, but it must be a **distinct finding ID** (`source:runner_digest`), never reported as `mapping:*`. Without that separation, a mapping-only selftest cannot reproduce the live exit-1 cause. Live state today: digest equal **[OBSERVED]**.

**F3. Positive-control baseline failure reported as mismatch.** [SOURCE-DERIVED] `positive_control_block` `:395-411` sets `effective = baseline_ok and ...`. If `git -C LANE_ROOT rev-parse --git-dir` fails without poison (not a git repo, unreadable `.git`), `effective` is False and `decide` returns exit 1 at `:570-571`. Retained registry text says exit 2 = "could-not-evaluate setup" and exit 1 = "observed mismatch or failed control" (SKILL.md round-14 registry row, line 1602). An unusable **baseline** control is setup failure; it should be exit 2 with its own ID. The mapping lane would otherwise absorb a setup problem into a mapping verdict. (Overlaps SpecControl/ReviewControl; included because it produces the same exit-1 class.)

**F4. Unhandled exception → exit 1 (no stable ID, no receipt).** [SOURCE-DERIVED] `main` (`:615-628`) catches only `InvalidContext` around `evaluate()`. `decide()` (`:629`) and `comparison_block`/`mapping_block` are not wrapped. In comparison, `any(row.get("content_status") ... or row.get("pinned", {}).get("status") ...)` (`:354-356`) raises `AttributeError` if a leg row is not an object, or `pinned` is `null`. Python's uncaught-exception exit status is 1 **[INFERENCE: standard interpreter behavior, not executed]**. A could-not-evaluate condition therefore appears exactly as a mismatch. Recommend an explicit catch-all in `main` that maps unexpected exceptions to exit 2 with an internal-error ID, so that exit 1 means only a decided finding. This is the smallest change that makes the exit-1 class mean what the registry says.

**F5. Injected probe unusable → exit 1, not exit 2.** [SOURCE-DERIVED] `comparison_block` `:371-379` sets `error`, `decide` `:560-563` gives exit 1. The docstring (`:26-29`) says "1 mismatch (including injected run unusable)". The registry row says 2 = could-not-evaluate setup. This conflict is a classification choice, not a bug in the arithmetic. Historical behavior is the reuse target, so keep exit 1 **only if** the acceptance pins it with literal ID (e.g., `comparison:injected_probe_unusable`) and the registry text says so. Do not describe it as "could-not-evaluate" without changing the code. Decision owner: ContextGate/Gate executor.

**F6. Mapping exit 1 from variable-name changes with identical values.** [SOURCE-DERIVED] `constant_names_match_leg` and `EXPECTED_SUFFIX` (`:74-81`, `:288-294`) require the constant *name* suffix to match the leg. A value-preserving rename (e.g., `REV_BASH` → `REV_KAGI`) is exit 1 by design ("variable-name-for-variable-name", `:71-73`). Acceptable under reuse; pin it, and say in the registry it is a name-binding check, not a value check.

**F7. Two-run window drift → exit 1 indistinguishable from injection effect.** [SOURCE-DERIVED] `comparison_block` compares two sequential probe runs with "no retry and no A-B-A" (`:4-8`). A sibling worktree change between runs yields `equal: false` → exit 1. This is inherent; the acceptance must describe exit 1 as "observed difference in this window", not "GIT_DIR effect". Not reproducible in a selftest; residual.

**F8. Historical-receipt replay against the new tool's own digest → false exit 1 for every historical receipt.** [SOURCE-DERIVED] `base_receipt` hashes `SELF` (`:414-418`). Any check CLI that compares a retained receipt's `tool_sha256` with `tools/context-capture.py` will fail for `context-receipt.json` (recorded `7313e9…`). The check must bind each receipt to the digest of the tool that produced it (historical script for round-14, new tool for round-15), not the current file.

**F9. Path depth on promotion → wrong root (exit 2, mislabelled).** [SOURCE-DERIVED] `LANE_ROOT = dirname^4(SELF)` (`:46`) is correct for `.ufo/evidence/round-14/capture-context.py` only. Applied to `tools/context-capture.py` (four `dirname` steps) it resolves to `/home/vgpnk/Projects`, and `FLEET_ROOT` to `/home/vgpnk`. The probe path `tools/pin-disposition.py` then resolves under `/home/vgpnk/Projects/tools`, and reads fail as `missing_input` (exit 2). **[OBSERVED]** `/home/vgpnk/Projects/tools` and `/home/vgpnk/tools` do not exist, so the failure is exit 2, not exit 1; it is still a blocker that hides every real check. The promoted tool must use `dirname(dirname(SELF))` for `LANE_ROOT`. Exit 2 is correct classification for the wrong reason, so the selftest must pin the reason ID too.

**F10. Overwrite of the historical receipt.** [SOURCE-DERIVED] `OUTPUT_REL` is round-14 (`:58`) and `write_receipt` uses `os.replace` (`:595`). Promotion that keeps this path overwrites the retained round-14 receipt. Not an exit-1 defect, but a contract violation. Require round-15 output path and refuse-if-exists.

## Unearned claims to reject

- **"Mapping exit 0 proves the runner executes or validates its six legs."** Mapping is static text parsing; the runner is never run (docstring `:11-14`). Result reuse is "not_established" (`:414-415`). Reject any wording beyond "constants and calls match the pinned manifest as text".
- **"A helper-only check closes routed defect 5."** The lesson states the helper controls "do not satisfy that clause" (`corpus/lessons/round-14-verifier-spotcheck.md`, Routed item 5). `guardrails.json` `context_setup_missing_field`, `context_setup_positive`, and `runner_variable_swap_discriminator` are `python3 -c` helpers, not CLI invocations. Reject any claim that they establish gate exit semantics.
- **"Retained-receipt check proves the receipt is authentic."** Receipts carry no self-digest; `decide()` replays recorded booleans (`:553-580`). The registry (SKILL.md, line 1604–1606) already says configured pins are not cryptographic proof. Reject "authentic"; allow "digest-bound to the pinned bytes".
- **"`decide()` replay of `context-missing-env.json` returns exit 1."** [SOURCE-DERIVED] That file has no `injected_env` key (lines 14–26) but `env_delta_matches_declared: true`, `baseline_has_GIT_DIR: false`, and records `status: ok, exit: 0`. Replaying `decide()` on it yields exit 0. The guardrail's "missing_injected_environment" verdict (exit 1) exists only in the helper. A retained-receipt CLI that reuses `decide()` therefore **cannot** claim to enforce the missing-field rule; adding that rule is new semantics and must be declared, or the file must be explicitly out of scope.
- **"Exit 64 is could-not-evaluate."** Historical source has only "64 usage" (`:117-124`). Repo precedent differs: `repeat-control.py` registry lists "2 and 64 could-not-evaluate" and `bash-witness-study` lists "64 usage/could-not-evaluate" (SKILL.md, round-12 registry, lines 1503–1504). Reject a single unexplained meaning; the new registry must state the 64 class explicitly and the selftest must pin usage errors to 64 (not argparse's default 2).
- **"Round-15 C1 is a capability at 6→6 with routed defect 5 resolved"** is not earned while F4 (exception → 1) and F3 (control-baseline → 1) stand; they are exit-class defects in the same family.

## Exact acceptance criterion (proposed, bounded)

Acceptance for the mapping family is met only when all hold:

1. `python3 tools/context-capture.py --selftest` runs **public CLI subprocesses** in a temp root only, and pins literal `(exit, finding-ID)` pairs. Each mapping case below must appear in that list with its literal pair.
2. Exit 1 is emitted only for a **decided** finding. Each finding carries a stable ID, emitted in the receipt `reasons` as an ID string (not prose), with variable parts (exit codes, leg names) normalized out of the ID or carried as separate fields.
3. Mapping IDs are separate from source-pin IDs (F2), control IDs (F3), and comparison IDs (F5).
4. A test-only fixture proves the new tool refuses an existing round-14 output path (F10) and reads roots from `dirname(dirname(SELF))` (F9).
5. Receipt check CLI binds each receipt to the tool digest it records (F8), and does not claim authenticity or missing-field enforcement it does not implement (unearned-claim list).

Recommended literal pairs (IDs are proposed; ContextGate chooses final spelling):

| Case | Fixture change (synthetic temp root only) | Expected exit | Expected ID(s) |
|---|---|---|---|
| M0 control | all six legs, names, pins, revs, order equal to manifest | 0 | none |
| M1 reorder | swap two `regression_case_git` calls, all bindings correct | 1 | `mapping:runner_leg_order_differs` (order binding kept; pinned) |
| M2 pin value | one `PIN_*` hex value changed | 1 | `mapping:leg=<leg>:pin_name_and_value_match_manifest` |
| M3 name swap | one call uses another leg's `$TABLE_*` suffix | 1 | `mapping:leg=<leg>:constant_names_match_leg` |
| M4 comment-only runner edit | runner bytes changed, six mappings unchanged | 1 | `source:runner_digest` only; no `mapping:*` ID |
| M5 missing header | five header rows only | 2 | `runner_unparsed` (reason ID) |
| M6 malformed leg row in probe baseline | baseline `legs` row not an object, or `pinned: null` | 2 after F4 fix (currently 1 with traceback) | `probe_baseline_unusable` / internal-error ID |

M1 and M4 are the two most likely "false exit 1" perceptions; the pairs above make them distinct and explicit.

## Minimal fixture recipe (implementation-critical)

Because the probe baseline must be usable before any mapping verdict (see above), each synthetic run needs, in a temp lane root `R` and temp fleet root `F = dirname(R)`:

- `R` is a `git init`-ed directory containing `tools/context-capture.py` (copy), `tools/pin-disposition.py` (copy of the historical probe or a fixture that emits pin-disposition-v1 for six legs), `tools/mutate-and-run.sh` (synthetic runner with six header rows, six PIN/REV constants, `TABLE_*` vars, `run_regression` with six `regression_case_git` calls), `.ufo/evidence/round-13/pin-manifest.json` (pin-manifest-v1, six legs), and `.ufo/evidence/round-13/expected.json` with `inputs` pins for the copies.
- `F` contains six git repos named by the manifest's `repo` field, each with the leg's file committed at `pinned_commit`, and `expected_sha256` equal to that file's digest.
- `R/.git` must resolve, so the positive control's baseline succeeds.
- No path outside `mkdtemp` is read or written. `GIT_*` is stripped by the tool itself.

This recipe is larger than a helper test. If the Gate executor judges it too heavy, the honest alternative is to narrow the claim to "mapping parse and decision are covered by the CLI only for the leg-level cases M0–M5", and say so; do not claim full CLI coverage of the probe path.

## Residuals and verification gaps

- No new source was read; all findings are against the historical script and retained receipts. Re-review is required once `tools/context-capture.py` exists; record its digest then.
- F1, F2, F4, F5, F7 are policy or semantic choices. They are not bugs in the historical arithmetic; they are unlabeled exit-1 classes that the acceptance must name.
- F4 (uncaught exception → 1) is **[INFERENCE]** that Python exits 1 on uncaught exceptions; not executed.
- F9 result (exit 2 `missing_input`) is **[SOURCE-DERIVED]**; not executed.
- I did not verify whether the historical `pin-disposition.py` emits `content_status`/`pinned` shapes that could trigger F4 on live data; no live probe was run.
- Unchanged lane state: working tree dirty by other seats; not touched by this review.

Report only; no sibling gate or selftest run; no commits; no tool installs.
