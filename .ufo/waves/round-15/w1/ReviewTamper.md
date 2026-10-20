# ReviewTamper — round 15 C1, snapshot digest mismatch → exit 2 `snapshot_tampered`

Seat: `TameshiR15.ReviewTamper` (reviewer, leaf). Lane: tameshi-shokunin. Wave: `tameshi-r15-w1`.
Scope: review of the planned C1 clause only. No gate, selftest, build, test, or formatter was executed. No source was edited. No commits.

## Read revision (honesty statement)

- Repo HEAD at read time: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (equals round-15 `claims.json` baseline).
- `tools/context-capture.py` **does not exist** in the working tree at read time (`exists = False`). The ContextGate seat owns it and has not landed it. Every claim about the new tool below is a *specification review*, not an observation of implemented code.
- Untracked: `.ufo/evidence/round-15/`, `.ufo/waves/round-15/`.
- Historical source (correct path): `.ufo/evidence/round-14/capture-context.py`, tracked, 647 lines, sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`. (The assignment's "historical source" is this file; there is no `tools/capture-context.py`.)
- Retained receipt: `.ufo/evidence/round-14/context-receipt.json`, sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`.
- Read-only digests taken at read time (not gate execution): `tools/pin-disposition.py` `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`; `tools/mutate-and-run.sh` `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; `.ufo/evidence/round-13/pin-manifest.json` `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6`; `.ufo/evidence/round-13/expected.json` `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`.

## Axes

1. **Acceptance exactness** — can the clause be checked by running the CLI and reading literal exit + token?
2. **False-positive exposure** — does the snapshot-tamper path flag legitimate states?
3. **Unearned-claim exposure** — what wording would overstate what a digest check proves?
4. **Consistency with precedent** — SKILL.md gate standard and existing tools.

## Evidence

### E1. The historical script has no snapshot concept and its own digest-mismatch exit is 1, not 2

- Exit map, `capture-context.py:26-29`: 0 equal; 1 mismatch "(including injected run unusable)"; 2 could-not-evaluate "(missing/unparsable input, poison path exists, baseline not a six-leg ok document)"; 64 usage, no receipt.
- `decide()`, lines 553-580: source digest mismatch (`sources.probe.matches_declared` false, line 572-573; `sources.runner.matches_manifest_declaration` false, line 574-575) appends to `reasons` and returns `("mismatch", 1, reasons)` (line 578-579).
- Source digests of **live** probe and runner are computed at `evaluate()` lines 480-486 and compared to declared values at 499-509.
- Therefore, in the existing code, *live* source-digest drift is exit 1. Only invalid inputs are exit 2 (`InvalidContext`, `main()` lines 615-628).

### E2. Existing stable token `snapshot_tampered` = exit 2 in two tools (precedent)

- `tools/repeat-control.py`: `EXIT_BY_ID["snapshot_tampered"] = 2` (line 127). Snapshot mode (`snapshot_mode`, 449-471) runs `load_snapshot` + `recompute_snapshot`; any `TamperError` emits `SNAPSHOT_TAMPER …` and returns `finish("snapshot_tampered")` **before** recomputing any finding (lines 453-458). Digest check is `read_checked` (411-422): `sha256_bytes(data) != record["inputs"][name]` over **raw bytes**. `lstat`-based symlink refusal (364-367, 414-418). Unlisted files refused (402-407).
- `tools/witness-metadata.py`: `_fail()` (259-268) maps exit 2 to `snapshot_tampered` when `reason.endswith("_digest_mismatch")` or reason ∈ `SNAPSHOT_TAMPER_REASONS`; `expected_id: "snapshot_tampered", expected_exit: 2` literal pairs in its selftest cases (703-931).
- `SKILL.md:1574`: "Snapshot input or receipt bytes differ from their pinned digest | Could-not-evaluate | Do not reinterpret an edited receipt as a new historical verdict."
- `SKILL.md:1553` (witness-metadata row) and `:1503` (repeat-control row) both list `snapshot_tampered` under exit 2.

**Conclusion:** mapping *pinned-byte* mismatch → exit 2 `snapshot_tampered` is consistent with the gate standard and both precedents. The planned clause is **correct in principle**. The risk is in *which* mismatch gets that label.

### E3. The round-14 receipt pins the historical script, not any new tool

- `context-receipt.json` `tool_sha256` = `7313e9a2…` = sha256 of `.ufo/evidence/round-14/capture-context.py` (`base_receipt()` lines 414-418 hashes `SELF`). Match confirmed read-only.
- `sources.probe.sha256` = `297253…` = current `tools/pin-disposition.py` (matches_declared true). `sources.runner` = `75ed934…` = current runner. Match.
- `status: ok`, `exit: 0`, `reasons: []`, `result_reuse: not_established`, `not_compared` lists leg execution, suite environment, sibling movement.

### E4. Path-derivation hazard when the script moves to `tools/`

- Historical `LANE_ROOT = dirname ×4 (SELF)` (`capture-context.py:45-47`). Correct only because SELF is at `<lane>/.ufo/evidence/round-14/`.
- Copied verbatim to `<lane>/tools/context-capture.py`, `dirname ×4` yields `LANE_ROOT = /home/vgpnk/Projects`, `FLEET_ROOT = /home/vgpnk` (computed read-only). Every `lane_path(PROBE_REL)` / `RUNNER_REL` / `MANIFEST_REL` then points outside the lane → `missing_input` exit 2 for **every** invocation, including the one the clause depends on.
- Correct for `tools/`: `LANE_ROOT = dirname(dirname(SELF))` → `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; `FLEET_ROOT = dirname(LANE_ROOT)` → `/home/vgpnk/Projects/shokunin`. (`repeat-control.py:113-116` uses the `tools/`-relative form `dirname(dirname(SELF))` successfully.)

### E5. Historical write path overwrites by design

- `write_receipt()` (583-602) uses `mkstemp` in the target dir then `os.replace(temporary, path)`; `OUTPUT_REL` is hard-coded to the **round-14** receipt (line 58). A naive promotion that keeps this constant overwrites the frozen round-14 receipt; changing it without a refusal guard allows silent round-15 overwrite, which would invalidate its own pin.

### E6. Preflight reads in selftest are a hermeticity violation pattern

- `witness-metadata.py` `run_selftest()` (1096-1120) reads live pinned lane inputs before running fixtures and returns `SETUP_FAIL` if they differ. The planned C1 clause requires "no live reads … outside temp roots." Copying that preflight for the round-14 receipt would violate the contract.

### E7. Helper-only tests do not satisfy the clause

- Round-14 lesson `corpus/lessons/round-14-verifier-spotcheck.md:160` (defect 5): "a standalone isolated self-invocation testing exits and stable expected finding IDs; the helper-only missing-field/variable-swap controls are useful evidence but do not satisfy that clause."
- Precedent for the required shape: `repeat-control.py:610-618` (`run_child` → `subprocess.run([sys.executable, SELF] + args, cwd=scratch …)`) and `cli_case` (625-634) asserting `returncode == expect_exit and last_finding_id(stdout) == expect_id`.

## Exact acceptance criterion (C1, snapshot clause)

The clause passes only when **all** hold on the implemented revision. Each item is checkable by reading source and by the L1 single run after seats return (not by this seat):

| # | Criterion | Observable |
|---|---|---|
| A1 | `tools/context-capture.py` exists; `LANE_ROOT = dirname(dirname(SELF))`. | Source line; L1 run resolves `tools/pin-disposition.py` (no `missing_input`). |
| A2 | Snapshot digest = sha256 of **raw file bytes**, compared to a 64-lowercase-hex pin **stored outside the receipt** (committed pin file or tool-literal constant). | Source; no `json.dumps` canonicalization in the digest path. |
| A3 | Digest mismatch on the snapshot receipt ⇒ process exit **2**, last stdout line is the literal token `snapshot_tampered` (recommended form `CONTEXT_CAPTURE: snapshot_tampered`), **before** any `decide()` predicate is evaluated, and **no file is written**. | Selftest case: 1-byte flip → `2` + `snapshot_tampered`. |
| A4 | Digest intact + `decide()` ok ⇒ exit 0; digest intact + `decide()` mismatch ⇒ exit 1 with the existing reason strings. | Selftest case: digest-correct but predicate-failing fixture → exit `1`, token not `snapshot_tampered`. |
| A5 | Live source digest drift (probe/runner vs r13 declared; mapping false) remains exit **1** `mismatch`, not `snapshot_tampered`. | Code keeps `decide()` reasons unchanged; no suffix heuristic like `_digest_mismatch`. |
| A6 | Setup/invalid input (missing receipt, missing pin, unparsable pin, non-UTF-8, poison path exists, unusable baseline) is exit 2 with a **distinct** token from `snapshot_tampered`. | Selftest literal pairs. |
| A7 | `--selftest` runs only in an isolated `tempfile.mkdtemp` root; invokes `[sys.executable, SELF, …]` per case; asserts literal `(exit, token)` pairs; performs **no** preflight read of lane or round-14/15 files. | Source; selftest prints each case with expected/observed. |
| A8 | Normal prospective capture writes `.ufo/evidence/round-15/…` only; refuses to overwrite an existing round-14 path and refuses to overwrite an existing round-15 receipt unless the design states an explicit overwrite policy. | Source. |
| A9 | Historical bytes unchanged vs HEAD `a9cf4da`: `.ufo/evidence/round-14/capture-context.py` sha `7313e9a2…`; `context-receipt.json` sha `05cb55b8…`. | `git diff --quiet a9cf4da -- .ufo/evidence/round-14/` after landing. |
| A10 | Exit 64 for unexpected arguments is registered as could-not-evaluate in the SKILL registry row (round-14 defect 5). | `SKILL.md` registry row lists 64. |

## Likely false positives to reject or guard

- **FP1 — live drift mislabelled as tamper.** Mapping probe/runner/declared-digest mismatch to exit 2 `snapshot_tampered` changes the historical `decide()` semantics (E1). A legitimate sibling-source edit would then read as tamper. Reject. Keep exit 1 (A5).
- **FP2 — self-hash pin on the receipt's `tool_sha256`.** Requiring `receipt.tool_sha256 == sha256(tools/context-capture.py)` flags the **retained round-14 receipt** as tampered (its `tool_sha256` is `7313e9a2…` = historical script, E3). It also makes every future edit to the tool invalidate all frozen receipts. Reject. Treat `tool_sha256` as recorded provenance only.
- **FP3 — canonical-JSON digest.** Hashing re-serialized JSON yields false positives on any formatting change and false negatives on reformatting. Use raw bytes (A2).
- **FP4 — self-referential pin.** A pin stored inside the receipt is vacuous (always matches or always fails by construction). Reject; the pin must live in a file the receipt does not contain.
- **FP5 — directory "unlisted file" scan.** `write_receipt` leaves `.context-receipt.*.tmp` on crash (`:586-602` cleanup is best-effort). A repeat-control-style unlisted-file scan would flag a leftover temp as tampered. Recommended: check named files only, or ignore `.context-receipt.*.tmp` explicitly and say so.
- **FP6 — re-capture changes bytes.** `observed_at` and `invocation` change on every run (`base_receipt` 417-436). A pin taken on one run is "tampered" after any re-run. This is correct behaviour (a new capture is a new snapshot, not tampering); the implementation must repin and must not overwrite silently (A8).
- **FP7 — wrong LANE_ROOT** (E4). Every invocation becomes exit 2 `missing_input`. This is a false *could-not-evaluate* on all inputs, not a tamper verdict, but it defeats the clause. Required fix (R1).
- **FP8 — precedence.** If the snapshot check runs *after* `decide()`, a tampered receipt that still satisfies predicates exits 0 or 1, not 2. Reject; order is digest → shape → decide (A3).

## Unearned claims to reject (wording)

- **U1 — authenticity/tamper-proof.** "`snapshot_tampered` proves the receipt is authentic / was not tampered with by anyone." The pin lives in the same repo and is author-written. A digest proves *byte equality with the committed pin*, not authorship. SKILL.md:1604-1605 already disclaims this for dispositions ("configured authority, not cryptographic proof of author authenticity"); the same limit applies. Use: "bytes differ from the committed pin."
- **U2 — digest ⇒ result reuse / reproduction.** "The round-14 receipt passes the snapshot check, so the historical context result is reproduced or safe to reuse." Byte integrity is not environment, dependency, or suite identity; the receipt itself records `result_reuse: not_established`.
- **U3 — selftest ⇒ live verification.** "The selftest proves the round-15 receipt." The selftest uses synthetic fixtures; the live receipt check is a separate single L1 run and must be reported as such.
- **U4 — snapshot covers probe/runner.** "exit 2 `snapshot_tampered` means probe or runner was tampered." Unless the design adds pins for those files, they are live inputs compared in `decide()` (exit 1 path), not snapshot-pinned.
- **U5 — helper tests satisfy C1.** A check function tested in-process does not meet the clause (E7). Only the CLI exit + literal token counts.
- **U6 — digest match ⇒ mapping true.** Receipt replay proves recorded predicates only, not the live mapping (SKILL.md:1605 analogue).

## Required fixes (blocking for C1 acceptance)

- **R1.** Use `LANE_ROOT = dirname(dirname(SELF))` for `tools/`. Do not copy the historical 4× derivation (E4).
- **R2.** Snapshot check before any predicate evaluation; mismatch → exit 2, token `snapshot_tampered`, no receipt write (A3).
- **R3.** Raw-byte sha256 over the receipt; pin stored outside the receipt (A2).
- **R4.** Explicit ID→exit table with literal strings. Do not copy witness-metadata's `_digest_mismatch` suffix heuristic (A5, FP1).
- **R5.** Selftest: subprocess per case, literal `(exit, token)` pairs, isolated temp root, zero live preflight reads (A7, E6, E7). Must include: one-byte-flip → `2 snapshot_tampered`; digest-correct + predicate-failing → `1`; intact + ok → `0`.
- **R6.** Normal capture writes round-15 only; refuse round-14 path; define round-15 overwrite policy (A8, E5).
- **R7.** SKILL registry (owned by the Registry seat, not this seat): the context row at `SKILL.md:1602` must list the new command, `--selftest`, exit 0/1/2/64 with `snapshot_tampered` under 2, and supersede the old "no standalone selftest" text. The historical row must remain visible.

## Optional hardening (not required for the clause)

- **O1.** `lstat`-based symlink refusal for the receipt and pin, matching `repeat-control.py:364-367,414-418`.
- **O2.** Explicitly ignore `.context-receipt.*.tmp` (FP5) and state so in the output.
- **O3.** Print `tool-sha256=<own digest>` in its banner as provenance only (like repeat-control's `REPEAT_CONTROL_TOOL …`), never as a pin.

## Residual risk and verification gaps

- No implemented source was available; all judgements above are on the specified contract and the historical script. Re-review after the ContextGate seat lands `tools/context-capture.py`.
- No gate, selftest, or live receipt check was run (per assignment). The following are unverified claims until L1 runs them once: A1 path resolution, A3 exit/token, A7 selftest literal pairs, A9 byte identity.
- The historical script's `main()` writes a receipt on exit 2 (`:615-628`). The new snapshot-mode must not copy that behaviour (write-on-invalid). Confirm in the implementation.
- The round-14 lesson notes the historical script was landed in the same commit as its expected rows and oracle repairs (lesson line 98), so its frozen expectations are not independently pre-registered. That limits what any snapshot pin can claim about the historical receipt.

## Tooling

No tools installed or updated. Only read, grep, `sha256sum`, and stdlib `python3` path arithmetic were used. No gate, selftest, build, test, or formatter ran.

## Recommendation summary

Accept the planned mapping (pinned-byte mismatch → exit 2 `snapshot_tampered`) as consistent with SKILL.md:1574 and the repeat-control/witness-metadata precedent. Reject: live-drift-as-tamper (FP1), self-hash on `tool_sha256` (FP2), canonical-JSON digest (FP3), self-referential pin (FP4), and the authenticity/reuse/live-verification wording (U1–U4). Require R1–R7 before C1 is credited.
