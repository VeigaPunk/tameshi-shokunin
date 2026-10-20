# repeat-control — draft registry row (GateRegistryScribe, round 12, DRAFT)

Status: DRAFT for L1 integration. Not applied to `SKILL.md`, `LOG.md`, or `corpus/*`.
Scribe lane is advisory and lane-internal; nothing here is an independent non-author
promotion or admission. Source of the interface: `.ufo/waves/round-12/spec.json`
`context` field, sentence "New gate interface" (sha256 `e13d92af…891cc2`, see
`observed-probes.txt`). The tool file `tools/repeat-control.py` was ABSENT at observation
time (`observed-probes.txt`); every behavior below that names the tool is the contract
text, not an observed run.

## 1. Registry row (proposed shape, matches `corpus/README.md` "Coverage map" columns)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/repeated-control-precondition.md` (ControlKnowledge, draft; not yet written) — gate `tools/repeat-control.py` (ControlGate, executor; not yet written) | Repeated pristine-control gate for C1: `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`. Runs the exact argv N times with stdin DEVNULL, saves numbered stdout/stderr/exit per run, compares them byte-for-byte. Stable finding IDs: `controls_match` (exit 0, clean), `controls_mismatch` (exit 1, failed), `baseline_nonzero` and `command_unavailable` (exit 2, could-not-evaluate), invalid usage (exit 64, could-not-evaluate). Snapshot check: `--snapshot DIR` → `snapshot_tampered` (exit 2). `--selftest` runs isolated fixtures. Claims: identical control evidence over N runs only; no flakiness cured; no determinism proven. | S004 (`mined`, `corpus/SOURCES.md:15`: tests must first pass reliably in a copied tree); S011 (`queued`, `corpus/SOURCES.md:22`: kill verdicts assume determinism); S026 (`queued`, `:37`); S040 (`queued`, `:49`). **Only S004 is `mined`; S011/S026/S040 must be opened and promoted to `mined` in the round that writes the knowledge entry before any of them supports a claim** (QUALITY.md 10; PROVINCE.md:40-42; corpus/README.md F3) |

## 2. Gate-interface card (for the SKILL registry entry)

| Field | Value | Basis |
|---|---|---|
| Invocation | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` | spec.json context, "New gate interface" |
| Argv handling | exact argv after `--`; no shell; stdin `/dev/null` | spec.json context ("Run exact argv with stdin DEVNULL") — shell-vs-argv boundary still open for GateSecurity |
| Bytes | stdout/stderr/exit saved per run, numbered, not normalized | spec.json context ("do not normalize bytes") |
| Required runs | N ≥ 3 for C1; lower/zero/non-integer boundary **unspecified** | spec.json context ("N>=3"); gap G-3 below |
| Exit 0 | `controls_match` — all N runs identical in exit, stdout, stderr; baseline exit 0 | spec.json context |
| Exit 1 | `controls_mismatch` — any output or exit disagreement | spec.json context |
| Exit 2 | `baseline_nonzero`, `command_unavailable`, `snapshot_tampered` — could-not-evaluate; the finding ID is the only discriminator | spec.json context |
| Exit 64 | invalid usage — could-not-evaluate | spec.json context |
| `--selftest` | isolated fixtures; must print exact IDs and exits per case; pass/fail exit code **not specified** (proposal: 0 pass / 1 fail, mirroring `tools/mutate-and-run.sh:1612,1615`) | spec.json context; proposal = [INFERENCE] |
| `--snapshot DIR` | validates committed input digests + expected ID/exit; tamper → exit 2 `snapshot_tampered` | spec.json context; DIR layout **unspecified** (gap G-2) |
| Pinned fixture | `.ufo/evidence/round-12/ControlGate/expected.json` (persisted by ControlGate) | spec.json item ControlGate, Target — ABSENT at observation time |
| Read scope | the command under test and its inputs; `--snapshot DIR` (read); selftest fixtures inside its own scratch | inference from interface |
| Write scope | `--out DIR` only (numbered run files, exit files); selftest scratch under `/tmp/tameshi-r12-repeat-control-*` (proposed, per SKILL.md "Standing rules" scratch namespace) | SKILL.md standing rules; `--out` clobber behavior **unspecified** (gap G-1) |
| Tool owner | ControlGate (executor) — `tools/repeat-control.py` only | spec.json dispatch members |
| Fixture owner | ControlGate — `expected.json` | spec.json ControlGate Target |
| Snapshot-contract owner | SnapshotReview (review only, read-only) | dispatch.json members |
| Registry row + LOG entry owner | L1 integration owner (Main) — every change needs a LOG.md round entry | spec.json context, "Every change covered by L1 LOG.md round entry" |
| Mutation runner | untouched — `tools/mutate-and-run.sh` sha256 `75ed934d…adc5`, "No edits to existing mutation runner" | observed-probes.txt; spec.json context |
| Claim boundary | repeated-control evidence ≠ determinism proof ≠ kill-rate input ≠ seventh independent gate | spec.json context ("never count reanalysis as a seventh independent gate"); S011 limitation |

## 3. Exit precedence check (what a reader must do)

1. Read the **finding ID line first**, not the exit code. Exit 2 covers three IDs.
2. Exit 2/64 are never a verdict on the child command's behaviour.
3. Exit 0 is only `controls_match`; it says the N pristine runs agreed, nothing more.
4. `snapshot_tampered` is a could-not-evaluate state, not a mismatch (exit 1 is reserved for `controls_mismatch`).

## 4. Gaps and risks (named, not smoothed)

- **G-1 `--out DIR` clobber.** Whether an existing, non-empty DIR is refused, merged, or overwritten is not in the contract. Risk: stale run files from a prior run satisfy a later comparison. Owner: ControlGate; review: GateSecurity.
- **G-2 `--snapshot DIR` layout.** The committed digest manifest path, the expected-ID/exit record, and whether DIR is read-only are not named. Owner: SnapshotReview to propose; ControlGate to implement.
- **G-3 run-count boundary.** `--runs 0`, `--runs 1`, `--runs 2`, non-integer, and negative values: contract says "invalid run count" but does not map them. Proposal: all of N < 3 → exit 64 invalid usage — [INFERENCE], needs owner decision.
- **G-4 `--selftest` exit code and summary line.** Not specified; mirrored convention is a proposal (see §2).
- **G-5 timeouts and signals.** No per-run timeout is in the contract; a hung child blocks the gate. A child killed by signal: its exit representation is unspecified. Owner: GateSecurity.
- **G-6 ambiguous exit 2.** Three finding IDs share exit 2; a consumer that keys on exit alone will conflate setup, baseline, and tamper. Risk accepted by contract; the registry row must keep the ID column.
- **G-7 source gap.** The row's `Sources` cell cannot be admitted until the ControlKnowledge draft opens S011, S026, and S040 (currently `queued`, `corpus/SOURCES.md:22,37,49`) and promotes them to `mined`; S004 is already `mined` (`:15`). This seat did not re-open any of them.
- **G-8 tool absence.** `tools/repeat-control.py` absent at 2026-10-20T02:14Z; the row describes intent, not an observed gate. No run performed by this seat (contract forbids mid-flight tests).

## 5. Exact owned paths (this seat)

- write: `.ufo/evidence/round-12/GateRegistryScribe/registry-row-draft.md` (this file)
- write: `.ufo/evidence/round-12/GateRegistryScribe/observed-probes.txt`
- write: `.ufo/waves/round-12/w1/GateRegistryScribe.md` (wave report, mandated by the assignment)
- read only: `.ufo/waves/round-12/spec.json`, `.ufo/waves/round-12/dispatch.json`, `tools/mutate-and-run.sh`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `PROVINCE.md`
- not touched: `LOG.md`, `SKILL.md`, `corpus/*`, `tools/*`, any sibling seat directory
