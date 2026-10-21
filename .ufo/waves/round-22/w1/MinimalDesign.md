# MinimalDesign — advisory calibration review

## Axes and disposition

Axes: calibration, identity fidelity, evidence retention, and model simplicity. Recommendation: one immutable accounting bundle, one independently persisted digest expectation, and one deterministic validator. No production edits or deletions made. Existing round21 admission and its two claims remain untouched.

## Smallest contract-preserving model

Use the existing frozen fixture vocabulary rather than inventing a second convention:

- Bundle: `schema: wave-accounting-v1`, `waves`.
- Each wave: `name`, `members: [{name,id,role}]`, `outcomes: [{name,id,role,status,replaced}]`, `reports: [name]`, `claimed: {seats,completed,dead}`.
- Independent expectation: `schema: wave-accounting-expected-v1`, `bundle_sha256`, as already exercised by the frozen measurement's input construction. Persist the source paths and byte digests for both registries and the original outcome snapshot alongside the production bundle's provenance; the aggregate bundle hash alone does not bind a projection to its declared original inputs. Do not rewrite historical sources.

The registry projection owns expected membership and exact identities; the outcome projection owns declared terminal callback status. Retained report names are evidence attachment metadata only. The existing source snapshot keeps report paths and full original material, so a new report-content database or second report-success flag is unnecessary.

Validation order should preserve these distinctions:

1. Check expected byte digest before accepting bundle content; pin original-source byte digests as well. Hashes establish snapshot consistency, not provider authenticity.
2. Reject duplicate agent IDs before using a map that could collapse them. Require exact one-to-one membership per wave and exact `name`, `id`, and `role` equality with registry projection. Do not reconstruct an ID from a name or drop suffixes.
3. Require explicit `replaced: false`; do not coerce truthy strings or treat missing replacement data as false.
4. Accept only the explicitly supported terminal statuses. The frozen fixture and inspected retained callbacks use exact `completed` and `failed`. For this finalized snapshot, propose those two values; never classify arbitrary non-completed values as dead, or infer completion from a report. Missing, running, and unknown are validation errors rather than implicit failures.
5. Derive seats from validated membership, completed from exact `completed`, and dead from exact `failed`; compare all three claimed integers to derived values. Derive overall totals by summing validated waves. Claimed totals are assertions to check, never a second accounting authority.
6. Keep `reports` orthogonal. A failed seat with a retained report remains failed/dead. A report is not an outcome, replacement, completion callback, or independent-review admission.

Do not eliminate the separate members/outcomes collections: their apparent duplication is necessary to expose missing outcomes and identity mismatches. Do not eliminate the claimed triple: it is the frozen input whose false assertions must be rejected. Do not eliminate the independent digest expectation: it is necessary for snapshot-tampering discrimination.

## Observed evidence and contradiction

All paths below are repository-relative.

- `.ufo/evidence/round-22/contract.json:1-22` freezes base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`, target eight rejected malformed/mismatched fixtures, and the explicit non-authentication bound.
- `.ufo/evidence/round-22/measure.py:12-37,42-79` fixes the eight finding IDs, the model above, and a control containing both `pass` and `dead` reports while the dead outcome is `failed`. It expects `TOTAL_MISMATCH`, `MEMBERSHIP_MISMATCH`, `DUPLICATE_AGENT`, `UNKNOWN_STATUS`, `IDENTITY_MISMATCH`, `REPLACEMENT_FORBIDDEN`, and `SNAPSHOT_TAMPERED` in their corresponding cases. No alternative schema is needed.
- `.ufo/waves/round-21/original-outcomes-final.json` declares wave1 71 seats / 28 completed / 43 dead; wave2 75 / 38 / 37; overall 146 / 66 / 80. These are observed declared totals, not a newly executed independent count.
- Exact inspected wave2 identities are `TameshiR21.V01WitnessTests` and `TameshiR21.ProfileBashTsukuroiCensus`, both role `reviewer`, both original-outcome `status: failed`, `replaced: false`, and both carrying retained report paths. Their matching entries in `.ufo/waves/round-21/w2/swarm-registry.json` bind precisely those IDs; `spec2.json:444-451,586-593` binds their names and reviewer roles.
- `.ufo/waves/round-21/wait2-recovered-07.json:415-445` records `TameshiR21.V01WitnessTests` with structured `status: failed`; its retained error text describes failed exit 1 and exhausted rate-limit retries. `.ufo/waves/round-21/wait2-recovered-11.json:198-228` records the analogous exact census identity and failed status. These are retained declared callback snapshots, not authenticated provider telemetry.
- `.ufo/waves/round-21/w2/V01WitnessTests.md:1-3` nevertheless says `Verdict: done`; `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md:1-11` opens `done` and reports no actionable falsification. This is the relevant apparent contradiction: report-level prose and available work products coexist with failed terminal callbacks. Preserve both; do not rehabilitate either seat or erase the useful partial work.
- `.ufo/waves/round-21/w1/swarm-registry.json:8-16` binds `E01BwEnvScrub` to `TameshiR21.E01BwEnvScrub-3`; the original outcome snapshot agrees at lines 8-15. The `-3` is part of the exact declared identity, not permission to manufacture a replacement or normalize IDs.

## Weight rejected and no-harm boundary

Reject new process telemetry, retry automation, provider-authentication infrastructure, provider/model-based status inference, report-content verdict parsing, and duplicated mutable totals. Provider labels, duration, retry text, model routing, and `actual_result` can remain in historical source evidence without becoming required accounting fields. No history is proposed for deletion. This is a design exclusion, not a semantic no-caller claim about existing code; no source deletion candidates were analyzed and no LSP absence proof is asserted.

Tradeoff: this model deliberately proves consistency of declared frozen inputs, not callback authenticity or report quality. Removing any of the membership/outcome distinction, exact identity triple, explicit replacement marker, checked totals, digest binding, or orthogonal report attachment would harm calibration or evidence retention; stop simplification there.

## Verification and write boundary

Read-only inspection only; no build, lint, formatter, tests, data-count commands, alternate runtime, installs, or updates were run. No success or improvement claim is made for the evolving production implementation. The previously persisted `before.json` reports 0/8 with tool absent at capture time; that is historical baseline evidence, not a claim about current files. The integrator's narrow existing acceptance check is the frozen `measure.py` public-CLI control plus eight predicates; this lane did not execute it.

Only this new assigned report was written. No shared source/evidence was edited and no git/jj/index/ref mutation was performed. A whole-tree byte-identity check was not run under the lane's no-check boundary, so no global byte-identity claim is made while other lanes are active.
