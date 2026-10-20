# Round 13 `producer_before`: reconstructed intent

## Axes in scope

- **Calibration (primary):** distinguish a setup failure from evidence about the producer assertion; reconcile the frozen expectation without grading an unrelated failure as a mechanism result.
- **Depth:** preserve a traceable link from the original observation to the replacement before/after oracle evidence.
- No evidence in this assigned surface establishes a change to coverage, operability, freshness, or adjacency.

## Evidence chain

1. The immutable expectation `.ufo/evidence/round-13/expected.json#/expected_checks/producer_before` requires exit `1` **and** stdout containing `summary preserves top-level exposed declaration kind`.
2. The raw `.ufo/evidence/round-13/verification.json` record named `producer_before` ran `python3 .ufo/evidence/round-13/producer-before.py selftest`. It returned exit `1` (`exit_matches: true`), but stdout has no required assertion. After the selftest's printed checks, stderr shows `FileNotFoundError` while `sha256_file(RUNNER)` opens the wrongly resolved path `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/tools/mutate-and-run.sh`. Thus the frozen row is **not satisfied**: exit equality alone does not satisfy its `contains` predicate, and this run never reached the target assertion.
3. `.ufo/evidence/round-13/verification-verdict.json#/excluded_initial_failure` explicitly classifies this as a path-layout failure before the target assertion and says it is superseded only by `producer-oracle-repair.json`. Its `checks` list includes the before/after oracle checks as matched but has no `producer_before` match. `input_digests_match: true` does not mean the stale stdout predicate passed.
4. `.ufo/evidence/round-13/producer-oracle-repair.json` identifies its purpose as superseding the path-layout crash, pins oracle SHA-256 `d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b`, and describes the single source delta: the summary-kind getter changes from nested `declared.kind` to top-level `kind`; the literal regression check is identical in both producer versions. Its `producer_before_oracle` check runs the retained historical source with the runner path supplied explicitly; it exits `1` and prints the exact assertion followed by `FAIL` (`WITNESS_SELFTEST: 40/41 pass`). `producer_after_oracle` uses the current source with the same oracle/runner, exits `0`, prints the same assertion `ok`, and reports `41/41 pass`.
5. The round-13 closure lesson states the same intent and remedy: item 1 says the stale expected row remains, the initial relocated command crashed before the assertion, and a next-round effective/superseded disposition or replacement receipt is required; it forbids erasing the initial failure or treating exit-only matching as mechanism proof (`corpus/lessons/round-13-verifier-spotcheck.md:175-180`).

## Reconstructed contract and decision

The historical `producer_before` execution is a retained setup-failure observation, **not** red-before mechanism evidence. The actual mechanism evidence is the repair receipt's paired oracle comparison: the same exact regression assertion fails for the pinned historical producer and passes for the corrected producer. This supports the narrow kind-getter repair; it does not convert the old relocated invocation into a successful check.

**Use a new explicit expectation disposition; do not rewrite round-13 bytes.** A further receipt is unnecessary for this defect because the repair receipt already contains the replacement observations, commands, outputs, exits, and oracle identity. A replacement receipt by itself would leave the frozen `expected_checks.producer_before` row unexplained to any reader/checker that evaluates every frozen predicate. In new round-14 evidence:

- retain/pin the original `verification.json` raw `producer_before` check and report it as **superseded**, with the path-layout failure as the reason and both `producer_before_oracle` and `producer_after_oracle` as replacements;
- retain/pin `producer-oracle-repair.json`; make those two replacement expectations effective and require each to pass its original frozen predicates (before: exit `1` plus exact failing assertion; after: exit `0` plus `WITNESS_SELFTEST: 41/41 pass`);
- pin the frozen `expected.json` and all used receipts, and verify its original input digests before evaluating structured predicates;
- leave `expected.json`, `verification.json`, `verification-verdict.json`, and `producer-oracle-repair.json` untouched. Do not execute their recorded argv as part of reconciliation.

This is consistent with the lesson's preference for a new auditable disposition and with its explicit no-history-rewrite constraint. It preserves both the invalid first setup and the valid replacement experiment instead of silently substituting one for the other.

## Count note / risk

The frozen `expected.json` has **12** `expected_checks` keys (lines 19-74) and **13** `inputs` paths (lines 4-17); the lesson also calls out 13 expected-input digests (line 87). If the round-14 plan's “13 expected rows” means checks, that count is off by one: disposition rows must enumerate the 12 actual frozen check names exactly once, with `producer_before` superseded. Do not invent a thirteenth check. The distinction between 13 pinned inputs and 12 expected checks is the only source-contract ambiguity found here.

## L1 follow-up checks

After all seats land, L1 should run the new disposition CLI and its isolated selftest, for example from the lane root:

```sh
python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions.json --json
python3 tools/evidence-disposition.py --selftest
```

Confirm the gate accounts for every frozen check exactly once, preserves and pins the raw failed observation, accepts the two effective replacement checks only against their original expectations, detects input/receipt digest mismatches, and does not execute recorded argv. These checks were **not run** in this research seat.

**Confidence: high** for the stale predicate mismatch and intended supersession: the raw check, explicit verdict exclusion, replacement receipt, and prior lesson agree. No historical evidence was modified; this seat writes only this report.
