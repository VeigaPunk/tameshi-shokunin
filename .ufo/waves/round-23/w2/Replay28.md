**Scope note:** per the wave's read-only constraint, I did not write `.ufo/waves/round-23/w2/Replay28.md` or touch any file; L1 persists this. No tools installed. No builds/tests/formatters run; only file reads, two checksum/diff facts, and read-only JSON parsing.

## Evidence — row `trace-inputs-selftest`

| Field | Frozen requirement (`requirements.json:405-418`) | Baseline (`registry-baseline.json:699-714`) | Bundle receipt (`bundle.json:390-393`) | Observation (`observations.json:1258-1272`) |
|---|---|---|---|---|
| name | `trace-inputs-selftest` | same | same | same |
| argv | `["python3","tools/trace-inputs.py","--selftest"]` | identical | identical | identical |
| expect | `exit 0`, `stdout_contains ["SELFTEST: "]` | identical | identical | identical |
| cwd | — | — | `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` = `bundle.cwd` | identical |
| revision | `source_revision 28cae179…` | — | `496d212b…` = `bundle.revision` | identical |
| exit | 0 | — | 0 | got 0, expect 0, held true |
| stdout | token required | — | 31 lines: 30×`PASS <check>` + `SELFTEST: 30/30`; stderr `""` | byte-identical to receipt; `stdout_tail` also identical |
| timing | — | — | — | interval 1.337253 s; `elapsed_s` 1.337 |

- Frozen requirements **exactly equal** baseline active rows (order-sensitive, 43/43) and equal `bundle.requirements`; `registry-baseline.json` digest = `ebd2e69a…` = `requirements.registry_sha256`; `bundle.json` bytes hash to `3d6c99b7…` = `expected.bundle_sha256`.
- The 30 retained check names occur in `tools/trace-inputs.py` in the same order, and `trace-inputs.py:964-967` prints `SELFTEST: %d/%d` then returns 0 only when `passed == len(checks)`. So exit 0 + token is internally coherent for this row.
- Full stream, not tail: `run_row(..., retain_streams=True)` sets `fragment["stdout"]` from the complete `communicate()` bytes (`registry-check.py:717-726`), while `_tail` is a separate 4096-byte slice (`:386-388`). For this row full == tail only because output is ~0.8 KiB; 12 other bundle rows have `stdout != stdout_tail`, proving the full field is distinct and used.
- Independent corroboration at the frozen delivered revision: `registry-C.json` (run at `336565fc…`) records the row `got 0, held true, elapsed_s 1.315`, tail ending `SELFTEST: 30/30`.

**Present (digest-pinned):** argv, cwd, revision, exit, full stdout, stderr. **Present but not digest-pinned:** measurement interval, `held`, `elapsed_s`, `stdout_tail` (observations.json only). **Inferred, not witnessed:** that a process actually ran (no process/strace witness for this replay); that clone HEAD was `496d212` (checkout success implies it, but replay.py records no post-checkout HEAD equality — registry-check's own clone path does). The recorded cwd is gone (`/tmp/tameshi-r23-replay-naxu6fzi` absent), so checkout identity cannot be re-inspected.

## Binding verdict for this row

**Static field binding is exact for the retained artifact.** No receipt field is accepted loosely against a mismatched requirement, and the pinned bundle is internally consistent with its declared requirement, cwd, and revision. I did not find a mismatch in argv/expect/revision/cwd/exit/stdout for this row.

## One field-level false acceptance (and concrete delta)

`evaluate()` accepts `stdout` purely by substring (`command-binding.py:96-113`), and this row's required token `SELFTEST: ` is a literal substring of the command's **own source** at `tools/trace-inputs.py:965` (`sys.stdout.write("SELFTEST: %d/%d\n" % ...)`). A receipt that carries a *source read* of the tool as its stdout with the correct argv/exit is therefore indistinguishable from execution.

**Concrete delta:** in `bundle.json`, keep `trace-inputs-selftest` receipt `argv/cwd/revision/exit=0/stderr=""`, replace `stdout` with the exact contents of `tools/trace-inputs.py` (which contains `SELFTEST: ` at line 965), regenerate `expected.json`'s digest. Traced statically through `evaluate()`, the result is `exit 0, finding_ids []` — a source read accepted as the required command's output. (The minimal variant — `stdout: "SELFTEST: \n"`, exit 0 — also passes.) The actual retained stdout is not this, so the artifact is not falsely accepted *today*; the acceptance channel exists.

**Second-order structural gap, stated separately:** `bundle.requirements` is bundle-local. `command-binding.py` never reads `requirements.json`, `registry-baseline.json`, or `source_revision`; `check()` only hashes the bundle against `expected.json` (`:117-131`). A consistent substitution of **both** requirement and receipt to `["cat","tools/trace-inputs.py"]` with the source text as stdout also yields `(0, [])`. No selftest or `extra-cases.json` case exercises a consistent requirement+receipt substitution; every adversarial case mutates only the receipt side or requirement *shape*.

## Contradictions (not smoothed)

1. **Revision:** bundle/receipts = `496d212b…`; contract `base_revision` = `28cae179…`; frozen delivered implementation = `336565fc…`; `.git/HEAD` = `336565fc…`. Reflog shows the lineage `28cae179 → 15ae6029 → 496d212 → 8f66b5d9 → 336565fc`, so the replay ran on an *ancestor* of the delivered revision. The gate cannot see this: it only requires `receipt.revision == bundle.revision`. The row's behavior is corroborated at `336565fc` by `registry-C.json`, but the replay artifact itself does not prove the delivered revision.
2. **Trust anchor:** `replay.py` writes both `bundle.json` and `expected.json`; `replay-gate-A.json` then feeds those same files to the gate. The docstring calls `expected.json` the "caller-owned commitment," but in this run it is producer-generated. CLEAN proves byte-stability since replay, not execution authenticity — reject it as producer authentication.
3. **Requirement anchoring:** the actual bundle's requirements equal the frozen requirements exactly (verified), but only `replay.py` performed that check at generation time; the gate itself cannot establish it.
4. **Historical metadata:** the baseline's `source: SKILL.md@58e5d53:1923-1932` and `source_revision 28cae179` are authoring/provenance declarations, not execution evidence; I did not retrofill them as such. Current `SKILL.md:1933` is the trace-inputs row (line shift between revisions).
5. **`held`:** the pinned bundle omits `held`/`cleanup_error`; those live only in un-pinned observations. The gate ignores them by design (docstring: held flags never establish execution). For this row `held=true`, so no conflict materializes.

## Axes

- **AX1** execution evidence vs source-read substitution (contract axis)
- **AX2** field-level binding exactness (argv/cwd/revision/exit/stdout)
- **AX3** evidence provenance boundary (retained/declared vs authenticated)
- **AX4** frozen-contract anchoring (requirements set and revision)
- **AX5** revision fidelity across base → delivered → replay
- **AX6** calibration honesty (claim scope vs demonstrated checks)

## Proposed move (one bounded proposal)

**Make this row's required token output-only.** Change `trace-inputs-selftest.expect.stdout_contains` from `["SELFTEST: "]` to `["SELFTEST: 30/30"]`. Verified: the literal `SELFTEST: 30/30` does **not** occur in `tools/trace-inputs.py` (0 matches), while the current token does (line 965). This closes the demonstrated field-level source-read/stdout substitution for this row with a one-token frozen-contract edit and no gate code change.

**Paired structural slice (optional, same move):** add `source_revision` + `requirements_sha256` to `command-binding-v1` and require them against the frozen file in `check()`, closing the both-sides requirement substitution. If schema churn is unwanted now, the token edit stands alone.

The move improves **AX1** and **AX2** for this row; it leaves **AX3/AX5** unchanged and cannot harm them. It does not by itself close **AX4** or make the gate authenticate producers.

## Risks

- The literal freezes the selftest count; a legitimate check added/removed later fails the row until the contract is deliberately revised (intended freeze, but must be recorded).
- It fixes this row only; other rows with generic tokens are not audited here and are not claimed fixed.
- The digest-anchor slice is only meaningful if `expected.json` (or its requirement digest) is written independently of `replay.py`; otherwise it remains producer authentication. Without it, the gate's honest claim is "receipt vs declared requirement binding," not "required registry command binding."
- Applying either change while this wave reads is forbidden; L1 must apply after all seats return, then regenerate receipts/expected and rerun the committed fact commands.

## Verification (for L1, after integration; not run now)

- Static: `grep -n 'SELFTEST: 30/30' tools/trace-inputs.py` → no match; `grep -n 'SELFTEST: '` → line 965.
- Negative: bundle with source-text stdout under the new token → `exit 1, ["STDOUT_MISMATCH"]`.
- Positive: current replay receipt already contains `SELFTEST: 30/30` → unchanged `exit 0, []`.
- If the anchor slice lands: both-sides `cat` bundle → `exit 1` with the new drift finding; unchanged 43-row bundle → `exit 0, []`.
