# AttackMismatch — falsifying planned C1 on comparison-mismatch exit1 + stable ID

Seat: `TameshiR15.AttackMismatch` (critic, leaf). This is a source-only review: I executed no gate, no selftest, and no capture.
Read revision: lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0`. `tools/context-capture.py` did **not exist** when I read the lane, so this review covers the contract and the historical source only.
Historical inputs and their sha256:
- `.ufo/evidence/round-14/capture-context.py` `7313e9a2…7d89`
- `.ufo/evidence/round-14/context-receipt.json` `05cb55b8…99c1a`

Other sources:
- `PROTOCOL.md:375-397` (fleet root), the Gate standard
- `SKILL.md:1602` (registry row)
- `corpus/lessons/round-14-verifier-spotcheck.md:160` (Routed defect 5)
- `corpus/lessons/round-15.md:31-36`
- the lane convention in `tools/evidence-disposition.py:1510-1573`

I ran two read-only host facts (not checks of any change):
- `git -C /tmp rev-parse --git-dir` gave rc=128 ("not a git repository"). `TMPDIR` is unset.
- `git -C /home/vgpnk rev-parse --git-dir` gave rc=0 and `.git`. **`$HOME` is itself a git repository.**

## What the historical source actually provides

- `decide()` (`capture-context.py:553-580`) returns `("mismatch", 1, reasons)`. Here `reasons` are **prose strings** and some are interpolated:
  - `comparison.get("error")` embeds `exit={}` (`:372-374`).
  - Mapping reasons embed leg names (`:323`).
- **No stable finding ID exists for any exit-1 condition.** The only stable tokens are:
  - `status: "mismatch"`, exit `1`
  - the stdout line `CONTEXT: MISMATCH (… probe-equal=… poison-control=… runner-mapping=…)` (`:637-642`)
  - the exit-2 `InvalidContext.kind` values (`probe_baseline_unusable`, `missing_input`, …)
- `decide()` folds **eight independent conditions** into one status:
  1. comparison not equal
  2. payload `tool_sha256` mismatch
  3. env delta not exact
  4. baseline has `GIT_DIR`
  5. control ineffective
  6. probe digest mismatch
  7. runner digest mismatch
  8. mapping mismatch
- Every guard uses `is not True` or falsy tests. A missing key therefore **fires** its condition.
- The positive control runs `git -C LANE_ROOT rev-parse --git-dir` and depends on ambient repository discovery (`:395-411`). `CONTROL_ENV_ADDITIONS` does not bound discovery, so no `GIT_CEILING_DIRECTORIES` is set. `safe_env()` also strips any ambient `GIT_*` (`:184-187`).
- `SKILL.md:1602` still registers the instrument as a `probe` with "no standalone selftest" and no code-64 class. That is the routed misclassification.

## Headline counterexample (CE-1): exit 1 is reached with comparison checking deleted

**Mutant M1.** Delete the first condition in `decide()` (the `comparison.get("equal") is not True` branch), or force `comparison_block` to `result["equal"] = True` and leave `decide()` alone. Comparison mismatch is then no longer a verdict input.

**Fixture F-mis.** The obvious hermetic fixture is a temp lane under `/tmp` containing:
- a stub `tools/pin-disposition.py` whose JSON includes `"git_dir": os.environ.get("GIT_DIR")`
- a valid six-leg runner, manifest and expected file with matching digests

There is **no `git init`**, because the fixture "only needs files".

**What each style of test observes under M1:**

| Test style | Observation | Verdict on M1 |
|---|---|---|
| Helper-only: `decide({"comparison": {"equal": False}})` → assert `("mismatch", 1)` | Missing control, env, sources and mapping keys fire 7 other reasons. The helper returns 1 whether or not the comparison branch exists, so the test passes even against M1's deletion. | **evades** |
| Helper-only: `comparison_block(base_run, inj_run, sha)["equal"] is False` | Holds under the decide-deletion form of M1, because `comparison_block` is untouched. | **evades** |
| CLI subprocess asserting only `rc == 1` and/or `"MISMATCH"` in stdout | In `/tmp`, the control's baseline `git rev-parse` exits 128, so `baseline_ok` is False and `effective` is False. Condition 5 fires and the CLI exits 1 for every fixture. Under the decide-deletion form, stdout still prints `probe-equal=False`. | **evades** |
| CLI subprocess asserting the **exact sorted finding-ID set** equals `{<comparison-ID>}` | Observes `{<control-ID>}` (plus nothing for comparison). | **caught** |

There is a host-specific twist. If the fixture is created under `$HOME` (for example a lane-relative temp dir, or `~/.cache`), discovery finds `/home/vgpnk/.git`. The baseline control then succeeds by reading the **live home repository**. The test goes green, but it is non-hermetic: it reads outside the temp tree, which breaks the Gate-standard "isolated fixtures (temp trees …)" requirement. Its correctness also depends on whether some ancestor is a repository.

**Why this matters to C1.** `PROTOCOL.md:385-389` requires the self-invocation to assert both the exit and a stable expected finding ID, with "a helper-only … self-check does not satisfy this clause". `round-15.md:31-34` sets the same admit/reject criterion. CE-1 shows that a CLI-level exit-only test is as vacuous as a helper test for this case: exit 1 is over-determined by sibling conditions.

## Secondary counterexamples

- **CE-2: exit masking in `main()` (helper-only evades; CLI catches).** A mutant in `main()` can return a different code after `decide()`. Separately, the historical path converts a `decide()` result of 1 into exit **2** whenever `write_receipt` fails (`:631-636`). A `decide()` unit test still sees 1, while the CLI exits 2. Only a subprocess assertion of `rc == 1` *and* the receipt's `"exit": 1` catches it.
- **CE-3: the injected-unusable branch substitutes for the comparison branch.** If the mismatch fixture's stub fails under the poison (for example it shells out to git and exits non-zero), `comparison_block` returns `equal=False` with a non-null `error` (`:371-375`). The canonical-JSON comparison (`:384-391`) is never reached. A mutant that breaks canonicalization survives. The historical docstring says "1 mismatch (including injected run unusable)" (`:27`), so both paths share exit 1 and the reason prefix.
- **CE-4: the top-level `observed_at` exclusion is untested.** If the clean fixture's stub prints a constant `observed_at`, then baseline and injected stdout are byte-identical. A mutant that sets `equal = raw_stdout_equal` (or skips the `observed_at` pop) passes both the clean and mismatch fixtures. The normalization the receipt advertises (`:365`) then carries no evidence.
- **CE-5: subset assertion with a co-firing digest finding.**
  - Setup: a mismatch fixture whose stub bytes differ from `expected.json` `inputs["tools/pin-disposition.py"]`.
  - Historical result: exit 1 with reasons [comparison, probe-digest].
  - Failure mode: a test asserting "comparison ID ∈ IDs" passes, yet the verdict rests on a mismatched persisted pin.
  - Protocol conflict: `PROTOCOL.md:395-397` says pinned-input digest failure is `snapshot_tampered` (could-not-evaluate), not a compared verdict. That classification belongs to the snapshot/tamper seats. For this case it means exact set equality is required, and the comparison fixture must keep every pinned digest matching.
- **CE-6: duplicate-key masking yields a false clean.** `parse_probe_document` uses plain `json.loads` (`:344`), unlike `parse_json`, which uses `_no_duplicate_keys` (`:158-181`). If the injected stdout contains `"legs":[<poisoned>] … "legs":[<baseline>]`, the last value wins, `equal` is True and the exit is **0**. `raw_stdout_equal=False` is recorded (`:367`) but `decide()` ignores it. The real `pin-disposition.py` emits through `json.dumps`, so the retained round-14 receipt (`raw_stdout_equal: true`, equal comparable digests `22e79150…61f9`) is unaffected.

## Required (Routed defect 5 / Gate standard) versus optional hardening

### Required for C1 to be admissible on this case

R1. Give each `decide()` condition a **stable literal finding ID**, emitted in the receipt and on stdout (for example `findings: [{"id": …}]`, as `tools/evidence-disposition.py` does). At minimum there must be a dedicated ID for "normalized injected observation ≠ baseline". It must not be shared with control, env, digest or mapping conditions.

R2. Add a public `--selftest` that invokes the **actual CLI via `subprocess`** (`sys.executable`, the tool path, and a fixture root or copied script) on a comparison-mismatch fixture. Requirements:
- **Literal** expectations, committed in the source and not recomputed: `rc == 1`, receipt `exit == 1`, `status == "mismatch"`.
- `sorted(ids) == [<comparison-ID>]`, using **exact set equality** as in `evidence-disposition.py:1571-1572`, not subset or contains.

R3. **Non-vacuity pair under the same harness.** A clean fixture that differs from F-mis only in the stub's GIT_DIR sensitivity must exit `0` with IDs `[]`. If both fixtures share one stub selected by a fixture data file, all pinned digests stay identical. The pair's receipts must show:
- `positive_control.effective is True`
- `environment.env_delta_matches_declared is True`
- `sources.*.matches_*` all true
- `mapping.all_match is True`

This makes the comparison the *sole* varied cause.

R4. **Hermetic control.** The fixture root lives under a `tempfile.mkdtemp(dir="/tmp")` tree. The selftest makes it a git repository itself (for example `git init -q` run with `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`). It asserts that the control baseline's `--git-dir` output resolves **inside** the temp root. This rules out the `$HOME/.git` leak. Two more conditions:
- Keep the derived `FLEET_ROOT` (`dirname(LANE_ROOT)`) inside the temp tree too, so the stub's `--root` never names `/tmp` or the live fleet.
- Write the receipt only under the temp root. No path under the live lane may be written, and `.ufo/evidence/round-14/*` must never be touched.

R5. **No change to historical bytes or meaning.** The historical script and receipt stay byte-identical (digests above). The new receipt schema and ID set belong to the promoted tool only. The round-14 receipt must not be reinterpreted as carrying IDs it never emitted.

R6. **Registry row for the promoted tool.** Kind `gate`; entry command; self-test spelling; a verdict map that names every nonzero code, including **64 → could-not-evaluate** (and 2 → could-not-evaluate). This is the routed defect itself. It belongs to the registry seats; I list it only so that C1 is not admitted with the probe row still describing the active tool.

### Optional hardening (not routed; do not claim it as part of Routed defect 5)

O1 (closes CE-3). Split `injected_unusable` from the normalized mismatch as a distinct ID, or have the selftest assert `comparison.error is None` and differing `*_comparable_sha256` for F-mis. One of the two is strongly recommended. Without either, R2's ID could be satisfied through the unusable branch.

O2 (closes CE-4). The clean fixture's stub emits a top-level `observed_at` that differs between runs (for example derived from GIT_DIR presence). The clean fixture then proves that the exclusion is exactly top-level `observed_at`. An optional third fixture changes only a nested `observed_at` and expects exit 1 with the comparison ID.

O3 (closes CE-6). Use `_no_duplicate_keys` in `parse_probe_document`. A duplicate in the baseline then goes through the existing `probe_baseline_unusable` path (exit 2); a duplicate in the injected run becomes injected-unusable (exit 1). This is a semantics change, so it needs its own literal fixture and an explicit note that the retained round-14 verdict is not re-derived.

O4 (CE-2). Add a receipt-write-failure fixture expecting exit 2. This is optional because the receipt-exit cross-check in R2 already catches the `main()` remapping mutant.

## Impacted axes

- **Calibration (C1, axis 6).** A green selftest that fails R1–R4 would be a renamed count rather than the missing experiment (`round-15.md:37-38`). Admit only if R1–R4 hold in the integrated L1 run.
- **No existing axis is harmed** by R1–R6: historical bytes are preserved and the scalar is unchanged.
- **O3 is the only proposal that changes verdict semantics.** It must be declared separately if adopted.

## Smallest safe correction (single sentence)

Emit a dedicated literal comparison-mismatch finding ID and assert `rc==1` and receipt exit 1 with **exact** IDs `[<comparison-ID>]`, through a subprocess CLI call on a git-initialised `/tmp` fixture. The fixture must be paired with a same-harness clean fixture showing `rc==0`, IDs `[]`, control effective, every digest and mapping true, and control `--git-dir` inside the temp root.

Tools installed/updated: none.
