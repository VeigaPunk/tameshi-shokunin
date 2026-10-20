# AttackUnavailable — round15 w1 critic: missing receipt / missing source input → exit2

Seat: `TameshiR15.AttackUnavailable` (critic, leaf). Source read only; nothing executed except read-only
`git log -1` and `sha256sum` to bind the read revision. No edits outside this report. No installs.

## Read revision

- Lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0` (2026-10-20T03:54:12-03:00); 8 dirty/untracked paths in the worktree at read time (other seats).
- `tools/context-capture.py` **did not exist** at read time, so every finding below targets the *planned* C1 (spec1.json `ContextGate` item + Contract "Integration interface"), checked against historical source.
- Historical digests (sha256, unchanged by this seat):
  - `.ufo/evidence/round-14/capture-context.py` `7313e9a2…24fe7d89` (equals `tool_sha256` recorded in both round14 receipts)
  - `.ufo/evidence/round-14/context-receipt.json` `05cb55b8…87899c1a`
  - `.ufo/evidence/round-14/context-missing-env.json` `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`
  - `.ufo/evidence/round-14/guardrails.json` `cca670b54f5da70873daec8d1bd54749ea63be99582f21138d43c8c715eaf784`

## Axes

A1 exit-class correctness (0/1/2/64 per Routed defect 5) · A2 stable finding identity · A3 provenance (no verdict the run never observed) · A4 hermeticity (temp roots only) · A5 history preservation (round14 bytes and receipts untouched).

## Primary counterexample — recorded could-not-evaluate becomes "failed" (exit1)

Source facts (historical `capture-context.py`):

- Exit 2 exists **only** as an exception path: `evaluate()` raises `InvalidContext(kind, …)`; `main()` (lines 615–628) writes a receipt with `status: "invalid_input"`, `exit: 2`, `error.kind`, and prints `CONTEXT: INVALID (kind=… receipt=… exit=2)`.
- `read_lane_bytes()` (145–155) maps a missing input to kind `missing_input`, message `missing lane file: <rel>`. Inputs are read in fixed order probe → runner → manifest → expected_r13 (476–479); `receipt["sources"]` is assigned only after all four reads (480), and `comparison`, `positive_control`, `mapping` stay `{}` from `base_receipt()` (429).
- `decide()` (553–580) has **no exit-2 branch**. With `comparison == {}` it appends "injected observation differs…", "probe payload tool_sha256…", "git poison positive control is ineffective", source and mapping reasons, and returns `("mismatch", 1, reasons)`.

Counterexample: the ContextGate target says the retained-receipt check uses "actual decide predicates plus required structure". Feed it a round15 receipt produced by a capture whose `tools/pin-disposition.py` (or any other input) was missing. That receipt honestly records `status=invalid_input, exit=2, error.kind=missing_input`. A check that re-runs `decide()` on it returns **exit 1 "mismatch"** with reasons asserting an injected/baseline difference and an ineffective git control that were **never observed** (A1, A3). A nominal helper-only test — e.g. `runpy` the module and assert `read_lane_bytes("absent")` raises `InvalidContext` with kind `missing_input`, as the round14 guardrail style did — passes, because the helper is right; the defect is in the CLI's composition of check → decide. Only an actual `--check` subprocess on a recorded exit-2 receipt pinning `exit == 2` and the literal ID exposes it.

Variant (structure-first): if the check does "required structure" first and treats `comparison == {}` as malformed, it emits exit 2 but under a generic structure ID, conflating "the gate could not evaluate when it ran" with "this receipt is malformed". Exit-only pins pass; the literal ID pin catches it (A2).

## Secondary counterexamples (each evades exit-only or helper-only testing)

1. **Missing receipt → traceback exit1.** Retained precedent: `guardrails.json` `context_setup_missing_field` uses `json.load(open(sys.argv[1]))`, records `expected_exit: 1`, and records stdout but has **no expected-stdout field**. [INFERENCE, CPython semantics, not executed] if `context-missing-env.json` were absent, the uncaught `FileNotFoundError` exits 1 with empty stdout. That still satisfies `expected_exit 1`, so the "negative control" passes without its fixture existing. The same happens to a `--check PATH` built from bare `open()`/`json.load`: a missing receipt reads as exit 1 "failed", not 2.
2. **argparse usage lands in exit 2.** `tools/witness-metadata.py` imports argparse, and that registry row folds usage into 2. argparse's default `error()` exits 2. If context-capture uses argparse unmodified, `context-capture.py --check` (missing value) exits 2. A "missing receipt" case pinned on exit 2 alone passes even though the path never reached receipt loading, and the declared 64 usage class (Routed defect 5) is violated (A1).
3. **Lane-root depth makes every input "missing".** Historical `LANE_ROOT` uses four `dirname()` calls from `.ufo/evidence/round-14/`. Copied unchanged to `tools/context-capture.py`, it resolves to `/home/vgpnk/Projects` [INFERENCE from path arithmetic]. Every run then raises `missing_input: missing lane file: tools/pin-disposition.py`, which is byte-identical to a fixture that deletes the probe. A missing-input selftest pinned on exit 2 + `missing_input` + that message passes while the gate cannot evaluate anything (A1, A2, A4).
4. **Precedence masking.** `evaluate()` checks `os.path.lexists(POISON_PATH)` and `os.path.isdir(FLEET_ROOT)` *before* reading inputs (469–474). Either `poison_path_exists` or `invalid_fleet_root` produces exit 2 first. An exit-only missing-input case passes for the wrong reason. The poison `lexists` is also a fixed absolute host read, not inside the temp root (A4).
5. **Exit-2 capture still writes, by replacement.** `main()` writes the invalid receipt through `os.replace` onto `OUTPUT_REL` (583–602, 621–622). A failed-input run therefore replaces any earlier good receipt at that path. Historically that path was round14. If promoted code keeps `OUTPUT_REL`, a missing-input run overwrites `.ufo/evidence/round-14/context-receipt.json` (A5).
6. **Write-failure exit 2 has no stable ID.** If the receipt write fails, `main()` returns 2 with free-form stderr only (623–626, 633–636). Nothing can be pinned literally (A2).

## Required routed fixes (C1 / Routed defect 5 scope)

R1. `--check`: a missing receipt yields exit 2 with a literal stable ID; an unreadable one yields exit 2 with a distinct ID. Neither may raise a traceback. Reuse the existing lane convention `<label>_missing` / `<label>_unreadable` (`tools/evidence-disposition.py:239,270,277,304`), e.g. `receipt_missing` / `receipt_unreadable`. The witness-metadata family `input_unavailable` is also acceptable if the registry row names it.
R2. `--check`: branch on the recorded verdict **before** `decide()`. A receipt with `status == "invalid_input"`, `exit == 2` (int, not bool) and a string `error.kind` from the source's own kind set yields exit 2 with a stable ID such as `recorded_could_not_evaluate`, and should surface the recorded kind (e.g. `missing_input`). Only `status ∈ {"ok","mismatch"}` receipts go through `decide()`. The recomputed `(status, exit)` must equal the recorded pair, else exit 1 with a stable ID.
R3. Selftest runs the public CLI as a subprocess over temp-root fixtures and pins literal `(exit, id)` pairs for at least:
   - (a) a capture missing a **non-first** input, e.g. delete fixture `.ufo/evidence/round-13/expected.json`: exit 2, kind `missing_input`, message `missing lane file: .ufo/evidence/round-13/expected.json`, receipt `lane_root` == fixture root. This proves probe, runner and manifest resolved under the fixture root, which defeats counterexamples 3 and 4.
   - (b) `--check` on an absent receipt: exit 2, `receipt_missing` (or chosen literal).
   - (c) `--check` on the receipt produced by (a): exit 2, `recorded_could_not_evaluate` — the primary counterexample.
   - (d) a clean exit-0 case through the same root mechanism, so a wholesale `missing_input` regression fails the suite.
   No writes outside the temp root. The positive fixture needs `git init` inside temp; the git control runs `git -C LANE_ROOT rev-parse --git-dir`.
R4. Usage is exit 64 with a stable ID, never argparse's default 2. Either do not use argparse, or override `ArgumentParser.error`. Include one usage case in the selftest (e.g. `--check` with no value → 64).
R5. Prospective capture writes only under `.ufo/evidence/round-15/`; no code path names a round14 output. The selftest's temp-root fixture must prove this structurally: written files ⊆ temp root.

## Optional hardening (not required by Routed defect 5)

O1. Refuse to replace an existing round15 receipt on any capture (or on exit 2 only), or write invalid captures under a distinct name, so a later missing-input run cannot erase an earlier ok receipt.
O2. Give receipt-write failure a stable stderr token, e.g. `receipt_write_failed`, with exit 2.
O3. Make the poison path selftest-local so the missing-input case does not depend on a host absolute path. Pinning the kind (R3a) already neutralizes the masking, so this only adds hermetic purity.
O4. Snapshot mode, if added: a missing snapshot member gives exit 2 `input_unavailable`, distinct from digest-mismatch `snapshot_tampered`. The ID split is owned by the Tamper lane; listed only for consistency.

## Judge-facing distinction

- Fixable defects: the primary counterexample and items 1–3 are implementation defects that the R-items fix. They are not tradeoffs.
- Rejection rule: if the integrated C1 selftest pins exits without literal IDs, or tests only helpers via `runpy` instead of public CLI subprocesses, the canonical judge should reject the "standalone self-invocation" claim. That is exactly the clause Routed defect 5 says helper-only controls do not satisfy.
- Unearned claim to reject: any statement that round14's `context_setup_missing_field` guardrail proves a missing-input exit-2 class. It pins exit 1 on a *present* file with a missing field. It never exercised an absent receipt or input.
