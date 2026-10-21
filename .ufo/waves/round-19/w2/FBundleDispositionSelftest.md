# FBundleDispositionSelftest — 2026-10-21

Scope: w1 `BundleDispositionSelftest.md`, its disposition receipt, and frozen C1 ruler at `55e1d312c4e8ac67aefad80099bd27581ff805c9`. Read-only; no receipt argv, ruler, or selftest was executed.

## Strongest assertion

W1 §Verdict calls the row a “sound current receipt, not a failed raw attempt” and says it is outside routed R18-1…R18-5, with no erratum owed.

## Verdict

**Agree about the receipt and its C1 classification; disagree only with treating its historical-byte preservation as enforced by the frozen ruler.** No stale correction to the disposition row itself was found. The delivered ruler has a separate enforcement gap described below; this does not make the row a sixth C1 defect.

## Evidence

- At delivered `55e1d312`, `final/checks.json` SHA-256 is `fed3c8e6…c5c671d`; its disposition row remains `argv=[python3, tools/evidence-disposition.py, --selftest]`, `revision=921ef807…`, integer `exit=0`, `stdout_sha256=a5b86be8…ef091`. The checks blob and stdout/stderr blobs are identical to the cited earlier revisions; the row was not repaired or rewritten.
- Delivered stdout is 3,925 bytes, SHA-256 `a5b86be8…ef091`, with 63 `SELFTEST_CASE` lines, zero `FAIL`, and final `SELFTEST: PASS (63/63)`; stderr is empty (SHA-256 `e3b0c442…b855`). Its digest is unique among the 38 `final/*.stdout` files at `55e1d312`.
- `tools/evidence-disposition.py` accepts `--selftest` alone (`:3120-3157`) and dispatches it to `selftest()` (`:3186-3187`). The retained `registry.stdout` at `55e1d312` identifies `rev=921ef807…`; its `evidence-disposition-selftest` row is expect 0 / got 0 / held true, and its 3,925-byte `stdout_tail` is byte-equal to the retained stream. These support byte/argv/exit consistency, not proof of the historical process environment.
- Frozen ruler `measure.py` at `55e1d312` is blob `d13dc4fb…`; the current worktree file is different (`2505d930…`). The read-only diff shows the worktree adds `OLD_CHECKS_PIN` and `historical-bundle-byte-tamper`; neither is present in the frozen blob. Frozen `evaluate()` checks the `bash-witness-selftest` row in `OLD_CHECKS`, but does not hash-pin the entire file. The old before/after receipts record the checks-file digest; they are historical input records, not a frozen-ruler equality assertion.
- This matches the scope of `measure.py`: its five IDs are R18-1…R18-5, with R18-4 the bash-witness correction. The disposition row itself is not a routed correction. QUALITY 39’s both-digest rule applies if this receipt is reused as a new final-success claim; it does not require rewriting this historical receipt.

## Concrete falsifier / missing enforcement

Static counterexample (not executed): change only `disposition-selftest.stdout_sha256` in `final/checks.json`, leaving the bash-witness row and all other inputs intact. The frozen 55e1 R18-4 predicate reads the bash-witness row but does not compare `digest(OLD_CHECKS)`; so this mutation would not reopen R18-4. The current worktree’s added whole-file pin and `historical-bundle-byte-tamper` case explicitly address that gap, but they are absent from delivered `55e1d312`. Thus the row needs no erratum, while frozen ruler enforcement of the report’s byte-preservation rationale is incomplete.

## Residual unknowns

Historical execution identity, cwd, and environment remain unproved; the report itself notes the same-tool-blob `e08271a` attribution counterexample. Whether the worktree hardening will be included in a later delivered revision is outside this read-only review.