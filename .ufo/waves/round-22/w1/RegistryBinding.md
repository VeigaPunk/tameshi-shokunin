# RegistryBinding — round-22 C1 advisory

## Axes and scope

Axes: calibration (exact seat identity and callback status), auditability (frozen input binding), and simplicity (one accounting authority, no report-derived success path). Inspection only; no dispatch, production edits, installations, builds, tests, lint, formatters, git/jj mutation, or existing-evidence writes. Only this new report was written. No deletion was made or source deletion candidate asserted; therefore semantic-reference proof is not applicable. No shared-tree byte-identity check was run: this lane is expressly barred from running checks. Existing round-21 admission and its two claims are unchanged.

Contract read first: `.ufo/evidence/round-22/contract.json` (base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`). Its inputs are declared retained callbacks, not authenticated provider telemetry. Recommendations below do not turn this advisory report into admission.

## Exact retained member shape

Both `.ufo/waves/round-21/w1/swarm-registry.json` and `w2/swarm-registry.json` use:

- top-level `schema: "ufo-swarm-registry-v1"`, `wave: null`, string `createdAt`, string `updatedAt`, string `reportDir`, and object `members`;
- member **object key** = assignment name, not full runtime ID;
- each observed member value has exactly `kind`, `agentId`, `role`, `item`, `axes`;
- `kind: "spawn"`, exact runtime-ID string `agentId`, role string, `item: null`, and axes array;
- no member-level status, report, replacement, or completion field. A registry entry establishes the declared dispatched identity, not successful completion.

The specs instead use `items: [{name, role, axes, prompt}, ...]`, with named `wave` values `tameshi-r21-w1` and `tameshi-r21-w2`. Their `reportDir` values match the corresponding registry directories. Consequently, `registry.wave == spec.wave` would incorrectly reject these retained inputs: the registry wave is actually null. Bind wave membership with explicitly paired immutable input paths/digests and matching report directory; do not invent a registry wave value or require non-null `item`.

Runtime identity is not reconstructible by prefix alone. In w1, `E01BwEnvScrub` maps to `TameshiR21.E01BwEnvScrub-3`; in w2, `Section0001` maps to `TameshiR21.Section0001`. The exact suffix is significant. All displayed spec/member name-role projections align; no name/role contradiction was observed in those projections. This is inspection, not an executed validator or an authentication claim.

## Refused attempts are not jobs

Evidence under `.ufo/waves/round-21/`:

| Retained input | Observed result | Accounting treatment |
|---|---|---|
| `dispatch-refusal-01.json` | Text says failed to start jobs because background limit 100; `details.results: []`, `projectAgentsDir: null`, `totalDurationMs: 0` | Refused pre-dispatch attempt; no dispatched seat from this response |
| `dispatch-attempt-02.json` | Same refusal structure, but attempted IDs carry `-2` | Refused attempt; do not count these as dead jobs or replacements |
| `dispatch-attempt-03.json` | Text explicitly says spawned 71 agents; `details.progress` supplies indexed IDs and agents; `details.async` is running task `TameshiR21.E01BwEnvScrub-3` | Actual w1 dispatch, with registry-bound `-3` IDs |
| `dispatch2-attempt-01.json` | Text explicitly says spawned 75 agents; populated `details.progress`; async task `TameshiR21.Section0001` | Actual w2 dispatch |

Critical distinction: the successful asynchronous dispatch responses also have no first/last `details.results` element. Empty `results` alone does **not** prove refusal. Use the response's explicit failure versus spawned text and populated asynchronous progress/identity records together. Likewise a progress row initially marked `pending` and an async envelope marked `running` are dispatch-stage observations, not final callbacks. Do not admit either as final `completed` or `failed`.

A refused allocation can consume a name suffix without creating a job. Thus w1's successful `-3` identity does not itself prove two prior running seats, and it does not violate `replaced: false`. Keep both refused attempts as historical provenance; exclude them from the actual-seat denominator.

## Callback versus report contradiction

`original-outcomes-final.json` declares w1 seats/completed/dead = **71/28/43**, w2 = **75/38/37**, total = **146/66/80**. These are the retained source's values, not a newly executed count. Its top-level `partial_report_files_do_not_rehabilitate_failed_jobs` is true.

Two exact w2 rows demonstrate why report existence/content cannot be another completion authority:

- `ProfileBashTsukuroiCensus` / `TameshiR21.ProfileBashTsukuroiCensus` / `reviewer`: callback row says `status: "failed"`, `replaced: false`, with non-null `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md`. That report begins `done` and describes a successful scoped reproduction.
- `V01WitnessTests` / `TameshiR21.V01WitnessTests` / `reviewer`: callback row says `status: "failed"`, `replaced: false`, with non-null `.ufo/waves/round-21/w2/V01WitnessTests.md`. Its opening verdict says `done` and review complete.

Both rows also show `actual_result: null`, empty `last_error`, `resolved_model: "zai/glm-5.3-flash:max"`, and `provider: "codex"`. That model/provider-label discrepancy is retained metadata, not permission to infer another status or authenticate the provider. Status remains failed. Report prose is usable historical partial evidence, never rehabilitation. No report content was rerun or independently verified here.

## Strict, narrow binding recommendation

Use a single frozen accounting join, with these requirements:

1. Persist and validate exact byte digests for outcome input and each paired registry/spec input before accepting accounting; a changed registry must not become a new authority merely because an outcome was changed with it. Digest consistency does not authenticate original callbacks.
2. Validate the expected registry schema and member value types/shape above. Require nonempty exact names and IDs, `kind == "spawn"`, valid declared roles, axes arrays, and the observed null `item`. Do not coerce booleans, numbers, nulls, or strings into identities/statuses.
3. Within each wave, require the outcome name set to equal registry member keys and spec item names. Reject duplicate outcome names and IDs before building maps, and duplicate spec names before joining. Reject duplicate JSON keys at parsing rather than silently accepting last-write-wins. Require registry IDs globally unique across the paired waves. Cardinality equality alone is insufficient.
4. For every row, require `row.id == registry.members[row.name].agentId` and `row.role == registry.members[row.name].role == matchingSpecItem.role`. Compare full IDs, preserving `-3`; do not strip suffixes, derive IDs, zip by order, accept basename matches, or use report paths as identity. Match axes against the spec if validating full registry/spec integrity; axes are not status evidence.
5. For this frozen final snapshot, permit only the observed terminal status enum `completed` and `failed`; reject unknown, missing, pending, or running status. Require `replaced` to be the JSON boolean false, not false-like text/numbers, and require one outcome per original dispatched seat. No replacement identity may fill a missing outcome.
6. Derive completed from exact `status == "completed"`, dead from exact `status == "failed"`, and seats from the bound original member set. Validate per-wave and aggregate declared totals against those derived values. Never branch on report existence, report verdict text, provider label, model label, or empty error text when classifying completion.
7. Keep refused attempts outside that set; bind actual dispatched IDs to the retained dispatch progress/registry evidence rather than treating attempted names as jobs. The public gate need not add a general dispatch-history parser to meet C1: freeze the actual registry authority and document why refused attempts are excluded.

The proposed simplification is removal of a **conceptual alternate authority** (report-derived completion), not deletion of historical report files. It preserves exact original seats, failed partial evidence, no-replacement semantics, and round-21 admission. Tradeoff: strict frozen binding intentionally rejects later schema/status evolution and cannot establish callback provenance. Generalizing that boundary or deleting retained provenance would harm calibration/auditability; stop there.

## Evidence and verification limits

Inspected with read-only file/JSON projections: contract; both registries; `spec1.json`, `spec2.json`; refusal/attempt files listed above; `record1.json` (same observed registry member shape plus path envelope); final outcome identity/status tuples; and the two failed-with-report files. No checks or data-count commands were run. No tools installed/updated. All original evidence and production paths were left unwritten by this lane; byte-identity of a concurrently shared tree is not claimed.

Report: `.ufo/waves/round-22/w1/RegistryBinding.md`
