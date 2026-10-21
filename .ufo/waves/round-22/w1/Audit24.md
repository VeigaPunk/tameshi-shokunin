# Audit24: callback, registry and report agreement for three frozen wave1 identities

**Verdict:** For all three identities, the persisted outcome row, the wave1 registry, the spec/run membership and the provider callback agree. Neither failed seat (SB10, SB11) has a report or a draft artifact anywhere, so no partial report exists that could rehabilitate them. SM1 has a callback status of `completed`, and its report was written before that callback arrived. I found no contradiction within this population. I found one schema observation that is relevant to the gate: wave1 `completed` rows lack the `replaced` key (see "Gate recommendation").

## Scoped population (exactly three; nothing else audited)

| name | agent id | wave |
|---|---|---|
| SB10ErrataNotes | `TameshiR21.SB10ErrataNotes-3` | wave1 |
| SB11SourcesFrontierDraft | `TameshiR21.SB11SourcesFrontierDraft-3` | wave1 |
| SM1RouteMixLean | `TameshiR21.SM1RouteMixLean-3` | wave1 |

## Per-identity agreement

| identity | outcome row (`original-outcomes-final.json`) | registry (`w1/swarm-registry.json`) | spec / dispatch | provider callback (parent session) | subagent transcript | report on disk | agreement |
|---|---|---|---|---|---|---|---|
| SB10ErrataNotes-3 | role `scribe`, `failed`, `report:null`, provider `haiku`, last_error 429 `retry-after-ms=10131000`, `replaced:false` | `agentId` exact match, role `scribe`, axes calibration+coverage | spec1 role scribe. dispatch-attempt-03 index 64, `modelRole m_haiku`. Assigned report `.ufo/waves/round-21/w1/SB10ErrataNotes.md`, draft target `w1/drafts/source-transitions.md` | `<task-result … status="failed (exit 1)" duration="4.4s">`, jobs[].status `failed`, `[anthropic/claude-haiku-5-5] 429 … retry-after-ms=10131000` | 11 lines: one user prompt, then one assistant message with `stopReason:error` (429 rate_limit_error), **zero tool calls**, then `session_exit dispose` at 12:08:08Z | **Absent.** Assigned report absent. `w1/drafts/` is empty (size 0, mtime 08:45, same as dispatch). No SB10 or Errata file anywhere under `waves/round-21` or `evidence/round-21` | **Agree: dead.** No partial artifact. |
| SB11SourcesFrontierDraft-3 | role `scribe`, `failed`, `report:null`, provider `haiku`, same 429, `replaced:false` | exact match, role `scribe`, axes calibration+coverage | spec1 role scribe. dispatch index 65, `m_haiku`. Assigned report `w1/SB11SourcesFrontierDraft.md`, draft target `w1/drafts/sources-frontier.md` | `status="failed (exit 1)" duration="4.4s"`, same 429 text | 11 lines, identical shape to SB10: one 429 error, **zero tool calls**, `session_exit` at 12:08:08Z | **Absent** (assigned report and draft both missing) | **Agree: dead.** No partial artifact. |
| SM1RouteMixLean-3 | role `simplifier`, `completed`, `report:.ufo/waves/round-21/w1/SM1RouteMixLean.md`. No `provider`, `last_error` or `replaced` keys | exact match, role `simplifier`, axes operability | spec1 role simplifier. dispatch index 66, `m_composer`. Assigned patch `w1/patches/SM1RouteMixLean.patch` | `status="completed" duration="1m34s"` at 12:02:42.615Z. Output says "Verdict: done … Full write-up: …SM1RouteMixLean.md" | 79 lines. Three assistant `error` turns come first (Grok 403 out-of-credits twice, then Cursor `PRO_USER_RATE_LIMIT_EXCEEDED`). Then one turn with 29 tool calls and `stopReason:stop`. Writes went only to its own report (3 edits) and `/tmp/tameshi-r21-SM1RouteMixLean-x/wave-route-mix-lean.py` | **Present.** Report mtime 12:02:36Z and patch mtime 12:02:28Z, both before the 12:02:42Z callback. Report text claims "Verdict: done" | **Agree: completed.** The callback, not the file, establishes completion. |

Notes:
- `run1.json` registry carries `agentId:null` for all three. This is pre-dispatch state, and the populated ids appear in `record1.json` and `w1/swarm-registry.json`. It is not a contradiction.
- `original-outcomes1.json` rows match `original-outcomes-final.json` byte-for-value for all three.
- SM1's fallback after provider errors does not count as a dead-seat replacement. It is the same agent id inside one session, and the parent received a single callback.
- SM1's self-reported selftest and refusal results (8/8, r20 exit 1) are **claims I did not verify**, because running checks is out of scope. They do not bear on accounting status.
- The parent session mentions SB10 and SB11 only at line 286 (the dispatch listing) and line 287 (the failed async-result). It contains no later `write agent://` follow-up to either seat, so no resume path exists that could have changed their status.

## Gate recommendation (bounded)

The gate SHOULD assert, for every row, that `status` equals the parent callback's `jobs[].status` for the exact `agentId`. It MUST NOT derive status from whether a report file exists. For these identities, that means:
- SB10 and SB11: `failed`, `report == null`, `replaced == false`, and counted in `provider_counts_dead.haiku`. If a file later appears at their assigned report or draft path, that MUST NOT change status. The outcome file already declares `partial_report_files_do_not_rehabilitate_failed_jobs: true`.
- SM1: `completed`, with `report` naming an existing file.

**Schema caveat:** all 28 wave1 `completed` rows (SM1 included) **omit** the `replaced` key, while all 38 wave2 `completed` rows carry it. A strict `replaced === false` check would therefore reject 28 legitimate rows. A check that treats a missing key as false would silently pass them. The gate should state which rule it applies. The smallest safe correction is to require the key to be present and false on every row, and to regenerate or annotate the wave1 completed rows accordingly, rather than giving missing keys a default.

Out of scope, flagged only: wave2 contains 2 `failed` rows with a non-null `report`. Those are the actual partial-report rehabilitation candidates and belong to another audit lane.

## Evidence (sha256)

| path | sha256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w1/swarm-registry.json` (71 members) | `7756c3b1ff7fdd6f20f4db2e0f2652742f899c945c6210756092061795a105b2` |
| `.ufo/waves/round-21/spec1.json` | `f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af` |
| `.ufo/waves/round-21/run1.json` | `ed5d201236c5471e749cc4d4eb1e2e43058f66916f9528be085abe5b81bc2480` |
| `.ufo/waves/round-21/dispatch-attempt-03.json` | `951d710aa1711a5274f8d9ae996de4ef8ebc0b08df7ffad9b6019ab1c7812674` |
| `.ufo/waves/round-21/w1/SM1RouteMixLean.md` | `778aabf38ec6dafc198a2ae891ca5f63b679a66539f7f29057bf21cbef0196cd` |
| `.ufo/waves/round-21/w1/patches/SM1RouteMixLean.patch` | `45562f5013484f315ba4733b7c2d06917651a869633e294bbcf143c9a03330a5` |
| `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-…/TameshiR21/TameshiR21.SB10ErrataNotes-3.jsonl` | `95837825e1ab8e93411f9cfb191c7b56f4560eab0725c972a9c736b9094d62cb` |
| `…/TameshiR21/TameshiR21.SB11SourcesFrontierDraft-3.jsonl` | `cc137d2b307873fb9a115d7941a44296035041a9d9b16184aed16549359cd319` |
| `…/TameshiR21/TameshiR21.SM1RouteMixLean-3.jsonl` | `742b4533ace045ace5fa26d9f7b2100a9d964d6a1623dd9834251c85bcd4ef87` |
| `…/TameshiR21.jsonl` (parent callbacks: line 287 for SB10/SB11, line 333 for SM1) | not hashed (live file) |

**Provenance limit:** the parent-session async-result is the strongest callback evidence that exists locally. It is harness-written, not cryptographically signed, so it cannot authenticate callback provenance either. That matches the gate's stated limit.

## Tool installs

None.
