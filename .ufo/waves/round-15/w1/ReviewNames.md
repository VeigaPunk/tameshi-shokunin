# Round 15 W1 — ReviewNames: equal-valued REV variable-name mismatch

Seat: TameshiR15.ReviewNames (reviewer, leaf). Scope: review the bounded planned C1 check that binds the runner's leg calls to their *variable names*, not only to resolved values, for the equal-valued REV pairs. Source reading only. No gate, selftest, probe, runner, or checker was executed. No tool installed or updated.

## Read revision and state

- Lane HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0`.
- Working tree at read: untracked `.ufo/evidence/round-15/` (contains `claims.json`) and `.ufo/waves/round-15/` (contains `swarm-registry.json` only at read time). No tracked file modified.
- `tools/context-capture.py` **does not exist** at this revision. All analysis of the promoted tool is against the historical source and the planned contract. Any implementation must be re-read before it is accepted.
- Historical source read: `.ufo/evidence/round-14/capture-context.py` (647 lines; read in full at lines 1–647 across ranges), `guardrails.json`, `tools/mutate-and-run.sh` lines 519–579 and 1061–1173, `.ufo/evidence/round-13/pin-manifest.json`, `corpus/lessons/round-14-verifier-spotcheck.md` (routed defect 5 at line 160).

## Evidence: what the runner actually does

Recorded runner constants (`tools/mutate-and-run.sh`):

| Name pair | Value | Equal-valued partner |
|---|---|---|
| `REV_BASH` (l.545) | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `REV_CHECKLIST` (l.551), same value |
| `REV_JS` (l.543) | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `REV_CLAIMS` (l.553), same value |
| `REV_TSUKUROI` (l.547), `REV_MADO` (l.549) | distinct | none |

Leg call sites inside `run_regression()` (body starts l.1074, ends at first column-0 `}` at l.1173):

- l.1113 `js-kimi-census` … `"$PIN_JS" "$REV_JS"`
- l.1118 `bash-surface-census` … `"$PIN_BASH" "$REV_BASH"`
- l.1133 `bash-checklist-run` … `"$PIN_CHECKLIST" "$REV_CHECKLIST"`
- l.1138 `js-claims-check` … `"$PIN_CLAIMS" "$REV_CLAIMS"`

`"$REV_BASH"` and `"$REV_CHECKLIST"` each occur exactly once in the body. The same holds for the JS pair. The selftest `regression_case_git` calls at l.1455+ are outside the body and are not parsed by design.

Checker behavior (`capture-context.py`, historical):

- `CALL_RE` (l.92–101) requires the quoted form `"$REV_<SUFFIX>"` after the pin argument. Continuation lines are joined (`CONTINUATION_RE`, l.223).
- `EXPECTED_SUFFIX` (l.74–81) is code-resident: `js-kimi-census→JS`, `bash-surface-census→BASH`, `bash-tsukuroi-census→TSUKUROI`, `bash-mado-verify→MADO`, `bash-checklist-run→CHECKLIST`, `js-claims-check→CLAIMS`.
- `mapping_block` (l.259–337) computes five checks per leg in this order: `header_matches_manifest`, `pin_name_and_value_match_manifest`, `rev_name_and_value_match_manifest`, `leg_call_matches_manifest`, `constant_names_match_leg`. The last two rely on the name check. The first two are not affected by a REV swap.
- `decide()` (l.553–580) emits mapping reasons last, after the probe/comparison/env/control/digest reasons.

Manifest (`pin-manifest-v1`) carries **no variable names**. It pins `pinned_commit` and `expected_sha256` per leg, and `derived_from.sha256` for the whole runner file (`75ed934d…c5`, as recorded). Names are therefore pinned only indirectly, through the whole-file runner digest, and that digest is checked in `evaluate()`/`decide()` (l.504–509, l.574–575).

Round-14 guardrail (`guardrails.json`, recorded `exit 0`, `measured_commit 64314783…`): `runner_variable_swap_discriminator` runs an in-process `runpy` of the historical script, replaces the single `"$REV_BASH"` in the body with `"$REV_CHECKLIST"`, and asserts `not all_match` and `not constant_names_match_leg` for `bash-surface-census`. It prints `runner_variable_swap_rejected: equal REV values do not hide wrong binding`. This was not re-executed here.

## Derived outcome for each swap (source-derived; [INFERENCE] until run)

For a quoted single-occurrence swap, only the swapped leg's row changes. Its failing checks are exactly `rev_name_and_value_match_manifest` and `constant_names_match_leg`. The value check passes because the values are equal. The pin, header, and call-identity checks pass.

| Swap (in run_regression body) | Leg whose row fails | Expected mapping reason string (exact) |
|---|---|---|
| l.1118 `"$REV_BASH"` → `"$REV_CHECKLIST"` | bash-surface-census | `leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg` |
| l.1133 `"$REV_CHECKLIST"` → `"$REV_BASH"` | bash-checklist-run | `leg bash-checklist-run: rev_name_and_value_match_manifest, constant_names_match_leg` |
| l.1113 `"$REV_JS"` → `"$REV_CLAIMS"` | js-kimi-census | `leg js-kimi-census: rev_name_and_value_match_manifest, constant_names_match_leg` |
| l.1138 `"$REV_CLAIMS"` → `"$REV_JS"` | js-claims-check | `leg js-claims-check: rev_name_and_value_match_manifest, constant_names_match_leg` |

Full CLI consequence of any runner byte change (including a swap): `decide()` also emits `runner source digest does not match the manifest declaration` **before** the mapping reason, because the manifest's `derived_from.sha256` pins the unmodified runner. A CLI fixture's expected finding list must therefore be `[runner-digest reason, leg reason]` in that order, unless the fixture rewrites the manifest's `derived_from.sha256` to the mutated runner's digest. Pick one and pin it; do not leave it implicit.

Exit class for a swap spelled so `CALL_RE` cannot match (unquoted `$REV_X`, `${REV_X}`, or reordered positional arguments): `parse_runner_mapping` leaves 5 calls and raises `runner_unparsed` (l.244–245), so exit **2** (could-not-evaluate), not exit 1. The historical exit map (docstring l.26–29) already says this. The acceptance must pin it.

## Exact acceptance criterion (recommended)

Within the promoted `tools/context-capture.py`, the selftest must invoke the public CLI as a subprocess on a hermetic temp lane root and assert all of the following:

1. **Unmodified runner fixture** → exit 0, and `mapping.all_match == true` for all six legs.
2. **Quoted equal-valued swap, four directions**: the four rows in the table above, one fixture each. Each asserts exit **1**, `status` MISMATCH, and the exact reason list `[runner digest reason, leg reason]` (or the leg reason alone if the fixture rewrites the manifest digest). The leg reason string must match the table exactly.
3. **Value-only control must not be sufficient**: in each swap fixture, assert that `pin_name_and_value_match_manifest` and `rev_value == pinned_commit` are still true for the swapped leg. This proves the name check, not the value check, is what fails.
4. **Unparseable spelling** (`${REV_CHECKLIST}` or unquoted) → exit **2**, `error.kind == runner_unparsed`.
5. Selftest runs only inside `tempfile` roots; no read of the real lane or fleet; no write of `.ufo/evidence/round-14/`.

## Likely false positives (reject or bound; do not admit as defects in the gate)

- **FP1 — consistent constant rename flagged.** A correct refactor that renames `REV_BASH`→`REV_KAGI` in both the definition and call sites will exit 1, because `EXPECTED_SUFFIX` still expects `BASH`, and the runner digest also changes. This is a *changed baseline* (per the manifest note), not a false positive to be silenced. The spec must say "exit 1 mismatch, update baseline", not "admit".
- **FP2 — equal values imply equal bindings.** Treating `REV_BASH == REV_CHECKLIST` as harmless would be wrong. The name check is the only detector for this class. Do not relax `constant_names_match_leg` to value-only.
- **FP3 — control reason masquerading as a variable finding.** The positive control runs `git -C <LANE_ROOT> rev-parse --git-dir` (l.400–409). If the fixture lane root is not a git repository, `baseline_ok` is false and the reason `git poison positive control is ineffective` appears alongside the leg reason. A hermetic fixture must `git init` its temp lane root, or the expected list must include that reason explicitly.
- **FP4 — probe reasons masquerading.** The fixture must supply a deterministic probe that emits a valid `pin-disposition-v1` document with six ok legs, and an `expected.json` whose `inputs[tools/pin-disposition.py]` equals that probe's digest. Otherwise `probe-equal` or `matches_declared` reasons fire and the swap finding is not isolated.

## Defect found in the planned promotion (implementation-critical)

**LANE_ROOT depth.** `capture-context.py` derives `LANE_ROOT` by four `dirname` calls from `SELF` (l.46). That is correct at `.ufo/evidence/round-14/capture-context.py`, where the fourth dirname is the lane root. At `tools/context-capture.py` it resolves to `/home/vgpnk/Projects`, one level too high. Consequences if copied unchanged:

- `read_lane_bytes` of `tools/pin-disposition.py` and the manifest fails: `missing_input`, exit 2 on every run.
- Positive control runs `git -C /home/vgpnk/Projects rev-parse --git-dir`, which is not the lane repo, so the control becomes ineffective.
- `OUTPUT_REL` writes land outside the lane.

Required: the promoted tool must derive `LANE_ROOT` as `dirname(dirname(SELF))`. The selftest must copy the tool to `<tmp>/tools/context-capture.py` so that rule holds inside the temp root. The historical file must stay byte-identical.

## Unearned claims to reject

1. **"The manifest pins variable names"** (historical docstring l.11–13: "compared value-for-value and variable-name-for-variable-name to the round-13 pin manifest"). The manifest has no name fields. Names come from `EXPECTED_SUFFIX` in code and are pinned only through the whole-file runner digest. Reword to that.
2. **"Variable-name-swap rejection" as a satisfied control for routed defect 5.** The lesson itself (l.160) states helper-only missing-field/variable-swap controls "do not satisfy that clause". The discriminator is in-process, one leg, one direction, and does not go through the CLI, `decide()`, or exit map. It does not satisfy the standalone self-invocation requirement.
3. **Coverage of the whole equal-valued class.** The guardrail covers only `bash-surface-census`→`CHECKLIST`. It does not cover the reverse direction, nor the JS pair `REV_JS`/`REV_CLAIMS`. Claim "equal-valued REV swaps are rejected" only after all four rows in the table pass.
4. **"Equal REV values do not hide wrong binding" as a general runner property.** It is true of the checker for quoted single swaps only. Any claim about unquoted, reordered, or multi-occurrence spellings is outside what the checker's regex covers, and such spellings exit 2 instead.
5. **Any statement that this seat executed the discriminator or any selftest.** It did not. Recorded round-14 results are historical evidence only.

## Residual risks and verification gaps

- The checker's name table `EXPECTED_SUFFIX` is code-side. A coordinated edit of runner plus table, with the manifest digest updated, is not detected beyond the digest change itself. Recommend the round-15 spec record the expected name table in the frozen expected file, so an edit to it is also visible. [INFERENCE: this strengthens but does not replace the digest check.]
- `RUN_REGRESSION_RE` ends at the first column-0 `}`. A future call added after such a line escapes the parse, and the leg count still reads six, so the check could pass while missing a leg. Low risk today (verified by reading l.1074–1173 only).
- No new tool, dependency, or install was used or required for this review. Tool installs/updates: none.

## Handoff

- Implementation owner (gate executor, `tools/context-capture.py`) must fix `LANE_ROOT` depth and pin the four swap fixtures and the unparseable-spelling exit-2 fixture. Main agent runs the checks once after seats return.
- No check was run by this seat. Expected results above are derived from source reading and are `[INFERENCE]` until the L1 run.
