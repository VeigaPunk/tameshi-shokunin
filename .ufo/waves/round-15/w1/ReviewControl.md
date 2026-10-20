# ReviewControl — round-15 C1 positive git control failure (exit 1)

Lane: tameshi-shokunin. Seat: TameshiR15.ReviewControl (leaf reviewer; no delegation, no execution).

## Read revision and state

- Read revision: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (`git rev-parse HEAD`, read-only).
- `tools/context-capture.py` **does not exist** at this revision. Everything below about it is a planned-contract review, not a review of source.
- Untracked `.ufo/evidence/round-15/` and `.ufo/waves/round-15/` exist. Their contents were not read beyond spec, assignments, and the wave registry.
- No gate, selftest, probe, or script was executed. The only commands run were read-only: `git rev-parse HEAD`, `git status --porcelain` on three paths, and an existence `ls`.
- Tools installed or updated: none.

## Evidence read

- Historical script: `.ufo/evidence/round-14/capture-context.py` (647 lines). Read in full: `main` L605–643, `evaluate` L465–550, `decide` L553–580, `positive_control_block` L395–411, `comparison_block` L350–392, `mapping_block` L259–337.
- Retained positive control, `.ufo/evidence/round-14/context-receipt.json` `.positive_control`: argv `/usr/bin/git -C <lane> rev-parse --git-dir`; baseline exit 0, stdout `.git\n`; injected exit 128, stderr `fatal: not a git repository: '/nonexistent/tameshi-round14-poison'\n`; `baseline_ok`, `injected_reflects_poison`, `effective` all true.
- Pin probe `tools/pin-disposition.py`: `git_env()` (L197–212) scrubs every `GIT_*` key; `git_run()` (L214–232) runs bare `git` via PATH; probe git calls are `rev-parse --show-toplevel`, `rev-parse --verify`, `cat-file -t`, `cat-file blob`.
- Routed defect 5, `corpus/lessons/round-14-verifier-spotcheck.md` L160, and AGENTS.md.
- Spec: `.ufo/waves/round-15/spec1.json` and `assignments1.json`.

## Exact acceptance criterion (positive control ineffective → exit 1)

The historical semantics are kept: `decide()` appends `"git poison positive control is ineffective"` when `control.effective is not True`, and the status is `mismatch`, exit 1.

**Case P — `positive_control_ineffective` (must exit 1):**
1. Build an isolated temp root `T`. Copy the new `tools/context-capture.py` to `T/tameshi-shokunin/tools/`. Add a synthetic probe stub, a synthetic six-leg runner, a synthetic `.ufo/evidence/round-13/pin-manifest.json` and `expected.json` (only what `evaluate()` parses), and `git init` in `T/tameshi-shokunin`. Create no commits and write nothing outside `T`.
2. Create shim dir `S` containing an executable `git`: `#!/bin/sh` / `unset GIT_DIR` / `exec <ABS real git> "$@"`. Resolve `<ABS real git>` with `shutil.which("git")` before PATH is changed.
3. Run `sys.executable T/tameshi-shokunin/tools/context-capture.py` with cwd `T/tameshi-shokunin`, env = `PATH=S:<original PATH>`, and no `GIT_*` keys.
4. Expect exit **1**, stdout starting `CONTEXT: MISMATCH`. The receipt at `T/tameshi-shokunin/.ufo/evidence/round-15/context-receipt.json` must show:
   - `status` = `mismatch`, `exit` = 1
   - `reasons` = `["git poison positive control is ineffective"]` (exactly one)
   - `positive_control.baseline_ok` = true, `positive_control.injected.exit` = 0, `positive_control.effective` = false
   - `comparison.equal` = true, `mapping.all_match` = true, `environment.env_delta_matches_declared` = true
5. Stable finding ID set = `{CTX-POSITIVE-CONTROL-INEFFECTIVE}`. The ID string is a proposal; it must be a fixed constant and must be mapped from the `decide()` branch, not from reason text.

**Case C — clean counterpart (must exit 0):** identical fixture with the shim removed. Expect exit 0, `status` = `ok`, `reasons` = `[]`, `positive_control.injected.exit` = 128, and `injected.stderr` contains the literal `/nonexistent/tameshi-round14-poison`. C and P differ **only** by the shim; that pair is the non-vacuity proof.

Do not pin receipt bytes. `observed_at`, `invocation.argv`, `cwd`, and temp paths vary. Pin exit codes, status, reason count, and finding IDs only.

## Findings by severity

### High

**H1 — LANE_ROOT derivation: a naive port makes a healthy lane fail the control (false positive, exit 1).**
The historical file sits at `.ufo/evidence/round-14/`, so `LANE_ROOT` = `dirname` ×4. The new file at `tools/context-capture.py` needs `dirname` ×**2**. Keeping ×4 gives `LANE_ROOT` = `/home/vgpnk/Projects` (verified by path arithmetic; not executed). Consequences on the real lane:
- `positive_control_block` runs `git -C /home/vgpnk/Projects rev-parse --git-dir`. If that directory is not a repository, baseline exit ≠ 0 → `baseline_ok` false → `effective` false → **exit 1 with the control reason for a healthy lane**. This is the exact false positive the spec must prevent.
- `FLEET_ROOT` and the probe `--root` also shift one level up.
- `OUTPUT_REL` must change to `.ufo/evidence/round-15/context-receipt.json`. Keeping round-14 violates the "never overwrite round14" rule.

Acceptance: a single assertion in selftest that `LANE_ROOT` equals the temp lane root (the parent of `tools/`). Case C would fail under ×4 when `T` is not inside a git tree, so the pair catches it.

**H2 — A blanket fake `git` shim is the wrong fixture (wrong exit, not exit 1).**
`pin-disposition.py` calls bare `git` through PATH. A shim that always prints success breaks the probe too. The probe then emits non-ok, `comparison_block` raises `probe_baseline_unusable`, and the CLI exits **2**. A selftest pinned to 1 would fail for the wrong reason. The shim must only remove the injected variable: `unset GIT_DIR` before exec of the real git. The probe scrubs `GIT_*` itself, so it is unaffected. Only the control's `rev-parse --git-dir` changes.

**H3 — `effective` is the same predicate as "control exited nonzero" (false positive in the control itself).**
In `positive_control_block`, `baseline_ok` forces `baseline.exit == 0`. Then `reflects` reduces to `POISON in stdout/stderr OR injected.exit != 0`, and `effective = baseline_ok AND injected.exit != 0 AND reflects`. Since `injected.exit != 0` already implies `reflects`, the poison-path check never decides anything. Any unrelated nonzero exit from injected git (a broken wrapper, a signal, an unrelated error) is recorded as an effective control. Such a fixture would pass as "effective" when the injection never reached git.
Recommended minimum fix: `effective` requires `POISON_PATH` in `injected.stderr` (exit 128 optional). The retained round-14 receipt satisfies this (stderr contains the path), so historical `effective: true` is preserved. Planner must accept this as a control-predicate tightening; it is not a decide/comparison/mapping change. If refused, the claim must be narrowed to "injected git exited nonzero."

### Medium

**M1 — Reasons are free text; no stable finding ID exists.** Routed defect 5 requires stable expected finding IDs for a gate. Proposed: `decide()` returns `(id, text)` pairs internally, `reasons` text is unchanged, and the receipt adds `finding_ids`. Case P pins `finding_ids == ["CTX-POSITIVE-CONTROL-INEFFECTIVE"]`.

**M2 — Retained-receipt check trusts stored verdicts.** `decide()` reads `comparison.equal`, `positive_control.effective`, `mapping.all_match`, and `environment.env_delta_matches_declared` as stored booleans. A check CLI that calls `decide(receipt)` on the file therefore accepts a hand-edited receipt with `effective: true`.
Recommended: the check CLI recomputes `baseline_ok` and `effective` from the stored `baseline`/`injected` runs using the H3 predicate, recomputes `decide()`, and rejects any mismatch with stored `status`, `exit`, or `reasons`. The check must not re-run the probe or git. Digest binding of the receipt is not authentication; the corpus lesson already says so.

**M3 — Exit-class ambiguity.** A failed positive control means the injection experiment did not discriminate, so the equality result is not evidence of anything. The spec and the lead criterion say exit 1. Keep exit 1 as the spec says, but record for L1 that "could not evaluate" (2) is the alternative. The human line must not say a probe observation changed.

**M4 — Selftest must not read the live probe.** Copying the live `tools/pin-disposition.py` into a temp root is a live read, which the spec forbids. The fixture must use a synthetic probe stub that emits one `pin-disposition-v1` object: `status` ok, six legs with `pinned.status` = `verified` and no `content_status` = `unavailable`, top-level `observed_at`, and `tool_sha256` = SHA-256 of the stub's own file. Comparison and mapping semantics are reused; only the probe is stubbed. The stub's `expected.json` `inputs[PROBE_REL]` must equal the stub file's digest.

**M5 — Dispatch order.** `main()` returns 64 for any argv. `--selftest` and the check subcommand must be dispatched before that branch, or they will be reported as usage errors.

### Unearned claims to reject

- **U1.** "Effective positive control proves the probe is independent of GIT_DIR." The control runs `rev-parse --git-dir`. The probe runs `--show-toplevel` and `cat-file`, and its equality is explained by its own `git_env()` scrubber, which the control does not test. Reject, or say the control proves only that git honors the variable for that command.
- **U2.** "Exit 1 means the probe's observation changed." A control failure is a defect of the experiment, not a data divergence. Reject any wording that reports it as substantive mismatch.
- **U3.** "Selftest reproduces round-14's live result or proves the real probe." The selftest uses a stub probe and synthetic fixtures. Reject any claim about the live probe, the live runner, or round-14 receipts.
- **U4.** "The check CLI re-executed the round-14 control." It reads a retained file. Reject any claim of re-execution.
- **U5.** "Retained receipt digest proves authenticity." It proves integrity of bytes against a configured digest at most. Reject authenticity wording.

## Residual risk and verification gaps

- `tools/context-capture.py` absent at a9cf4da; all Case P/C expectations are pre-implementation and unverified.
- Whether `/home/vgpnk/Projects` is a git repository was not checked (H1 is stated conditionally, by path arithmetic).
- The exact `git` stderr wording for `GIT_DIR` pointing at a missing path is observed only in round-14 retained output on this host; other git versions may differ. The H3 tightening depends on the `POISON_PATH` literal appearing in stderr.
- Stub probe fidelity to the real probe's document shape is not measured.
- L1 must run the selftest once after all seats return. Nothing here was executed.

## Recommendation summary

1. Derive `LANE_ROOT` with `dirname` ×2 for `tools/`; set `OUTPUT_REL` to round-15. Pin both in selftest.
2. Case P shim = `unset GIT_DIR; exec <real git>`; case C = same fixture, no shim; pin exits 1 and 0 and the single finding ID.
3. Tighten `effective` to require `POISON_PATH` in injected stderr (planner decision); otherwise narrow the claim.
4. Add stable `CTX-POSITIVE-CONTROL-INEFFECTIVE`, emitted from the `decide()` branch.
5. Check CLI recomputes `effective` and `decide()` from stored runs; does not trust stored verdicts; does not re-run anything.
6. Use a synthetic probe stub with self-digest; never copy the live probe.
7. Dispatch `--selftest` and the check subcommand before the usage branch.
