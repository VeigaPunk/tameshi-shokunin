# ScoutWaveSpecs — round-36 wave-spec policy recon

## Attacked

Policy-v1 validation of the two committed wave specs in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-36/` —
`spec-w1.json` and `spec-w2.json` — against
`/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`, plus the
§3 L2 floor-role presence check inside w1 (floor defined by dispatch and by
`scripts/hyaku/lane-addendum.md` line 74: "The §3 L2 floor is met inside wave 1").

## Sources read

- `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json` —
  `sighting.dispatch.swarm`: `waveMinLanes: 32`, `waveMaxLanes: 64` (lines 89-90);
  `nativeProfiles."omp-native-v1".proposalRoles` (lines 104-115) = the role
  vocabulary: `{scout, reviewer, critic, connector, sentinel, executor,
  mutation-tester, revenger, simplifier, scribe}`; `planner` (lines 99-103) is a
  frozen-topology seat, not a proposal role; `lanes[]` (256-307) enumerates the
  same ten-registered-role set minus sentinel.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-36/spec-w1.json`,
  `spec-w2.json`, `dispatch-w1.json`, `dispatch-w2.json`,
  `validate-w{1,2}.stdout` (schema `ufo-swarm-wave-v1`, non-empty) and
  `validate-w{1,2}.stderr` (0 bytes both).
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md` §3
  (lines 39-83): v1 band 32-64, `reportDir:
  ".ufo/waves/round-{{ROUND}}/<wave>"` lane-relative (line 69), L2 floor inside
  wave 1 (line 74), validator rejects `planner` (lines 75-78), never pass
  `model` (lines 79-81).
- `/home/vgpnk/Projects/shokunin/MISSION.md` §L2 concurrency (53-75).

## Commands run (all read-only)

1. `ls -la` + `find` on `.ufo/waves/round-36/` — inventory: 2 specs, 2 dispatches, 2 validate-stdout, 2 validate-stderr.
2. `python3` JSON parse of both specs: top-level keys, item keys, role counts, `model` key scan (recursive), `reportDir` check.
3. `grep -n "band|wave|role"` on the policy file; `read` of lines 85-140 and 256-344.
4. `grep`/`read` of `lane-addendum.md` §3 and `MISSION.md` §L2 for floor semantics.
5. `python3` per-check harness (band, vocabulary, planner, model, reportDir, floor) over both specs.
6. `python3` dispatch-vs-spec set comparison: task `name`+`agent` sets identical to spec `name`+`role` sets; `context` byte-identical; every `task` string embeds the spec `prompt`.

## Per-check verdicts

| Check | w1 | w2 |
|---|---|---|
| Seats in band 32-64 | **PASS** — 39 items | **PASS** — 39 items |
| Role vocabulary ⊆ `proposalRoles` | **PASS** — all 9 roles used are in the 10-role set | **PASS** — all 7 roles used are in the set |
| No `planner` role | **PASS** — zero planner items | **PASS** — zero planner items |
| No `model` field (top level or item level, recursive key scan) | **PASS** — zero hits; item keys are exactly `{axes, name, prompt, role}` | **PASS** — zero hits; same key set |
| `reportDir` lane-relative | **PASS** — `.ufo/waves/round-36/w1` | **PASS** — `.ufo/waves/round-36/w2` |
| §3 L2 floor roles inside w1: connector ≥1, executor ≥3, scribe ≥1, scout ≥1, reviewer ≥1, critic ≥1 | **PASS** — connector 1 (`ConnectorSiblingOverlap`), executor 6, scribe 1 (`ScribeGateAudit`), scout 6, reviewer 4, critic 4 | n/a — floor is a w1 obligation (addendum line 74); w2 roles: connector 0, scribe 0, executor 3 — noted for the record, not a violation |
| Validator artifacts consistent | **PASS** — `validate-w1.stdout` non-empty JSON `ufo-swarm-wave-v1`, stderr empty | **PASS** — same |
| Dispatch fidelity (`dispatch-w{N}.tasks` == spec items by (name, role), context identical) | **PASS** — 39/39, set-equal, context byte-identical | **PASS** — 39/39, set-equal |

### w1 role mix (39 seats)
mutation-tester 10, scout 6, executor 6, revenger 5, reviewer 4, critic 4,
simplifier 2, connector 1, scribe 1.

### w2 role mix (39 seats)
mutation-tester 9, reviewer 7, scout 7, critic 6, revenger 5, executor 3,
simplifier 2. Zero connector, zero scribe — inside vocabulary, no floor
obligation applies to w2 per addendum §3 line 74.

## Facts vs inference vs gaps

- **Observed:** every verdict above is a direct JSON read; both specs are
  structurally clean under policy v1.
- **Observed:** `dispatch-w{N}.json` `tasks[]` uses key `agent` where the spec
  uses `role` — the names/roles set-matched 39/39 in both waves; this is the
  validator's `taskCall` shape, not a divergence.
- **Inference:** `sentinel` is in `proposalRoles` but used in neither spec —
  permitted, vocabulary is a superset not a quota. `[INFERENCE]`
- **Observation for the record:** w2 omits connector/scribe entirely. This
  passes policy v1 (vocabulary is permissive) and the floor is explicitly a
  wave-1 check, but if any downstream invariant expects per-wave floor coverage
  it would flag w2. No such invariant was found in `lane-addendum.md` or
  `MISSION.md`.
- **Gap:** none remaining for this ticket — "§3 L2 floor" resolved to the
  dispatch's own enumerated role set (connector, ≥3 executors, scribe, scout,
  reviewer, critic), consistent with addendum §3's "met inside wave 1" clause
  and MISSION.md's ≥8-lanes-in-one-call requirement (39 ≥ 8, single batched
  `taskCall`).

## Verdict

**PASS** — `spec-w1.json` and `spec-w2.json` both satisfy policy v1 on every
checked dimension: band 32-64 (39/39 seats), `proposalRoles` vocabulary, zero
`planner` items, zero `model` fields, lane-relative `reportDir`. The §3 L2
floor roles are all present inside w1 (connector 1, executors 6 ≥ 3, scribe 1,
scout 6, reviewer 4, critic 4). No edits made; no tools installed.
