The gate's revision check works as specified: it compares each receipt's revision with the revision the bundle declares. Nothing in it ties that revision to anything outside the bundle, as its docstring says. The real calibration gaps are in what surrounds the gate, not in it. The two new registry rows don't pin the "frozen" bundle. Two of the 43 replayed receipts depend on live state that their revision field doesn't capture. Some recorded runner digests come from the working tree rather than the code that actually ran.

As the wave rules require, I did not write `.ufo/waves/round-23/w2/RevisionDeclared.md`; the findings are here only. I ran no Git, tests, builds or formatters, and installed nothing. My only executions were `sha256sum` and read-only Python scripts that parse JSON.

**Revision chain** (taken from the receipts, not looked up in Git):
- Base `28cae179`: `before.json` shows the tool absent; the requirements source registry has digest `ebd2e69a`.
- `496d212b`: `c1-after-A` (10/10 cases discriminated), `selftest-A`, `mutations-A`, the three `*-gate-A` receipts, `mixed-invalid-*`, `actual-*`, and the replay bundle (43 of 43 receipts all declaring `496d212b`).
- `8f66b5d9`: `monitor-intermediate-B`.
- Delivered `336565fc`: `registry-C` (46 rows held), `monitor-current-C` and `reader-freeze2`.

**Finding 1 (fixable, most important): the registry does not enforce "frozen".** The `command-binding-frozen-clean` row in `tools/registry.json` only requires `"finding_ids": []` in stdout. Its `expected.json` lives in the same tree as the bundle, so anyone changing the bundle can regenerate it in the same commit.
- **Counterexample:** replace `replay/bundle.json` with `correct-command-bundle.json` (one requirement instead of 43), or with any bundle whose own revision and receipts all say `aaaa…`, then regenerate `expected.json`. The row still holds. The selftest fixture `receipt-order-clean` is already such a bundle and comes back clean.
- `command-binding-source-read-red` has the same gap.
- **Impacted axes:** false provenance, identity change, calibration.
- **Smallest correction:** add the exact digest token to each row's `stdout_contains`: `"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9"` and `"bundle_sha256": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf"`. The report is sorted-key JSON, so this is an exact substring. Pinning the bytes also pins the declared revision `496d212b` and the 43 requirements.

**Finding 2 (tradeoff): for 2 of the 43 receipts, the revision doesn't pin the inputs.**
- `pin-disposition-read` reads `--root /home/vgpnk/Projects/shokunin` (the live workspace). The runner flagged it with `non_hermetic_argv`, and `observations.json` keeps that flag. The bundle receipt drops it, because the gate's receipt schema rejects extra keys, so it shows only revision `496d212b` and the gate passes it as clean.
- `verify-round15` is also declared `external: true`.
- The replay clone also symlinks to the live sibling repos.
- **Correction:** either describe the claim as 41 revision-pinned receipts plus 2 that depend on live external state, or add a declared `external` field to the bundle schema. Don't present all 43 as reproducible from `496d212b` alone.

**Finding 3 (fixable): runner digests are taken from the working tree, but the clone's copy is what runs.**
- `replay.py` records `runner_sha256` from `args.repo / 'tools/registry-check.py'`, but it imports and executes `clone / 'tools/registry-check.py'`.
- The `instrument_sha256` fields in `replay-command-A` and `registry-C` have the same pattern.
- The values do agree (`cba16646…` in the working tree and in `reader-freeze2` at `336565fc`). But nothing establishes the copy at `496d212b` that actually ran.
- **Correction:** hash the copy inside the clone.

**Finding 4 (calibration wording): the delivered gate's identity holds by content digest, not by matching revisions.**
- Every capability receipt runs against the live working tree (`cwd` is the lane root itself) and declares `496d212b`. That is a label, not proof the checkout matched; `measure.py` has no `--rev` option at all.
- What ties these receipts to the delivered `336565fc` gate is `tool_sha256 = d533dc1e…`:
  - `reader-freeze2` asserts the committed file at `336565fc` has that digest.
  - `registry-C` ran inside a clone at `336565fc` and shows the selftest at 38/38, bundle `3d6c99b7`, and registry digest `afeb6cb6`, which matches `reader-freeze2`.
  - Current working-tree hashes match every recorded instrument digest.
- The claim should cite `d533dc1e`, not `496d212b`, as the delivered gate's identity.
- The replay bundle covers the 43 baseline requirements from `28cae179`, not the 46 active rows in the delivered registry.
- Historical R17-CMD-BIND is not closed by any of this.

**Minor tradeoffs:**
- The revision pattern accepts only 40-hex SHA-1, so a SHA-256 repository would get `INVALID_BUNDLE`.
- The selftest reads `extra-cases.json`, but `selftest-A` doesn't list it as an input. `reader-freeze2` pins it at `87bffdc8…`.

**Main agent should run:** after the Finding 1 correction, re-run `registry-check` with `--rev` at the new revision. Also run one counterexample: swap in a regenerated bundle and confirm `command-binding-frozen-clean` turns red.
