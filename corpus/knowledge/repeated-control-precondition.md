source: S004 — https://mutants.rs/using-results.html — §§“Tests fail in an clean tree?”, “Mutant outcomes”; fetched 2026-10-20T02:13:47Z, sha256 5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334 (29,579 B); S026 — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html — post body by John Micco, published 2016-05-27; fetched 2026-10-20T02:13:47Z, sha256 ca1145fbe56de30b43b66baf7372206a38abe08a55b3db13f6c7a0114d7a6c8c (236,385 B). Located excerpts: `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`
verified-at: 2026-10-20
recheck: 730d — S026's registry cadence; S004's registry cadence is `on-release`, so re-open it at each mutants.rs release: `curl -fsSL https://mutants.rs/using-results.html | grep -c 'passes reliably when copied to a temporary directory'` → 1 and `curl -fsSL https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | grep -c 'hardly a perfect solution'` → 2 (ran 2026-10-20T02:17:02Z; S026 serves its post body twice — a `text/template` copy and a `<noscript>` copy — so 2 is the healthy count and 0 is drift)
ground: F3 — determinism precondition, flaky-aware verdicts (tameshi-art.md §4)

# Repeated matching controls: what the gate observes, and what it does not establish

## 1. The sources, located (O)

S004 `§Tests fail in an clean tree?` (`S004.html:184-187`) states the precondition in reliability terms:

> Fix this first: cargo-mutants can’t do anything until you have a tree where `cargo test` passes reliably when copied to a temporary directory.

S004 `§Mutant outcomes` (`S004.html:193-208`): `caught` = “A test failed with this mutant applied”; `unviable` = “The attempted mutation doesn’t compile. This is inconclusive about test coverage and no action is needed”; `timeout` = “The mutation caused the test suite to run for a long time, until it was eventually killed” (`:208`).

S026 post body (`S026.html:1130-1137`; the same bytes are served again in a `text/template` copy at `:1095-1102`):

- definition (`:1130`): “We define a "flaky" test result as a test that exhibits both a passing and a failing result with the same code.”
- rate (`:1130`): “a continual rate of about 1.5% of all test runs reporting a "flaky" result”; “Almost 16% of our tests have some level of flakiness associated with them!”
- transitions (`:1132`): “about 84% of the transitions we observe from pass to fail involve a flaky test”; monitors “wait for additional CI cycles to run this test again”.
- retry family, and S026's own verdict on it (`:1136`): “the ability to re-run only failing tests, and an option to re-run tests automatically when they fail”; a flaky-marked test “report[s] a failure only if it fails 3 times in a row. This reduces false positives, but encourages developers to ignore flakiness in their own tests unless their tests start failing 3 times in a row, which is hardly a perfect solution.”
- cost (`:1137`): for a 15-minute test, “The breakage will not be discovered until 3 executions of the test complete, or 45 minutes”.

## 2. What the observation does and does not establish (I)

- **Stream agreement is stronger than pass/fail stability — and still weaker than determinism.** Requiring identical stdout and stderr as well as an identical exit is a stricter test than requiring the same pass/fail outcome, so the gate's observation is the stronger of the two. Both are statements about the runs actually taken: the control's reported behaviour was stable in the observed stream. Determinism is a property of the program across runs, including runs not taken. `controls_match` records observed stability; no line in either source upgrades it to determinism.
- **Retries do not repair.** S026's own verdict on its re-run / fail-3-in-a-row family is that it reduces false positives while encouraging people to ignore flakiness, and that it delays detection. It changes what is reported, not what the program does. A mismatch among runs is therefore a finding, and the gate does not re-run until the runs agree.
- **An unusable baseline yields no verdict.** S004 refuses to proceed until the tree passes reliably and calls `unviable` “inconclusive about test coverage”; the lane's own rule stops on a red control (`SKILL.md:148-149`). Exit-2 is that shape — a refusal to evaluate, never a kill and never a clean pass.
- **The evidence is finite, so the claim is finite.** `controls_match` states that the N runs actually taken produced identical `(exit, stdout, stderr)` tuples, back to back, on one host, in one environment. It is not a universal over runs, not a cross-host or cold-start claim, and not a statistical estimate. Neither source prescribes a repeat count for a control — S026's fail-3-in-a-row is a retry-mitigation rule, not a control-repeat rule — so the floor of 3 is lane policy, not a sourced threshold. The gate's own limitation text says the same (`tools/repeat-control.py:79-87`): no timeout and no process supervisor, and a clean match is "not a determinism proof and it cures no flakiness". Measured in-lane: a control failing 10% of the time still produced three exit-0 runs in 223/300 triples; `date +%s` matched 50/50 back to back; and a cold first run gave exits `[1,0,0]` while a warm repeat gave an identical `[0,0,0]` triple (`.ufo/waves/round-12/w1/ControlThreats.md:45-56`; probe output `.ufo/evidence/round-12/ControlThreats/probes.out`).

## 3. The gate: interface, implementation, retained receipts

### 3.1 Interface (contract)

`python3 tools/repeat-control.py --runs N --out DIR -- COMMAND ARG...` — runs the exact argv N times with stdin `/dev/null`, saves numbered stdout, numbered stderr and each exit status under `DIR`, writes `command.txt` (argv, cwd, runs, interpreter, tool path and sha256) and, last, `finding.txt`, and compares the captured bytes without normalizing them. `--runs` must be at least 3 (`tools/repeat-control.py:245-247`); `DIR` must not already exist. Keep `DIR` outside any tree the command inspects: the gate writes its own observations during the run, and a command that reads that tree disagrees with itself (`:24-29`).

| finding | exit | class |
|---|---|---|
| `controls_match` | 0 | clean |
| `controls_mismatch` | 1 | failed |
| `baseline_nonzero` | 2 | could-not-evaluate |
| `command_unavailable` | 2 | could-not-evaluate |
| `setup_error` | 2 | could-not-evaluate |
| invalid usage | 64 | could-not-evaluate |
| `snapshot_tampered` (from `--snapshot DIR`) | 2 | could-not-evaluate |

Reading rules:

- `baseline_nonzero` applies only to **identical nonzero tuples** — every run exited with the same nonzero status and matching streams. Differing tuples are `controls_mismatch` first: a disagreement is a finding, not a baseline class (`tools/repeat-control.py:191-205`).
- `command_unavailable` — the argv could not be executed; nothing was measured.
- `setup_error` — the gate's own failure (evidence directory not writable, unexpected exception). It has its own ID so that no uncaught exception exits 1 and is read as `controls_mismatch` (`tools/repeat-control.py:185-188`).
- `--snapshot DIR` validates **saved observations**, never executing the recorded argv: it parses `expected.json` (schema, `runs` ≥ 3, a stable expected ID/exit pair, a sha256 per saved run file), recomputes the finding from the stored bytes, and compares. A verified snapshot exits with its recorded ID; stored bytes that recompute to a different finding exit 1 `controls_mismatch`; a missing, changed, symlinked or unlisted input, a malformed record, or any shape error exits 2 `snapshot_tampered` (`tools/repeat-control.py:337-435`).
- Scope: no timeout semantics — the gate declares no timeout and no process supervisor (`tools/repeat-control.py:79-81`); `--runs` is caller-supplied above the floor of 3; the unnormalized-byte comparison is the gate's own policy. Neither the run count nor the byte policy is source-prescribed.
- `--selftest` exercises the IDs above against isolated fixtures. The mutation runner is not edited (pin unchanged: `tools/mutate-and-run.sh` sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, six recorded legs at `:84-89`).

### 3.2 Implementation and retained receipts (O)

- [O] `tools/repeat-control.py` exists: 30,557 B, sha256 `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`, `VERSION` `repeat-control.py r12 (tameshi-shokunin, 2026-10-20)`. The finding map is `:115-123`, the precedence `:191-205`, the snapshot validator `:337-435`, the selftest `:545`. Read by this note's writer at 2026-10-20T03:45Z; not executed by it.
- [O] Retained receipts, produced by other round-12 seats (data, not this note's runs):

| receipt | path | observed |
|---|---|---|
| pristine control | `.ufo/evidence/round-12/FailureOracle/actual-pristine/gate-runs/` and `gate.stdout` | `REPEAT_CONTROL: controls_match`, `REPEAT_EXIT: 0`, `REPEAT_COMPARE identical=yes runs=3`, tool-sha `29d80254…`; the sibling `manifest.json` records `expected_finding_observed: true` |
| byte-boundary matrix | `.ufo/evidence/round-12/BytesReview/cli/C01–C20` | 20 CLI cases at tool-sha `d45d8e39…` (an earlier revision than the `29d80254…` now in the tree): 6 `controls_match`, 5 `controls_mismatch`, 5 `baseline_nonzero`, 4 `command_unavailable`; every `finding.txt` matched its case's expected class |

- [O] The snapshot directories `.ufo/evidence/round-12/ControlGate/` and `.../mismatch/` hold bare `run-<k>.{stdout,stderr,exit}` files only. No `expected.json` exists anywhere under `.ufo/evidence/round-12/` at this write (`find . -name expected.json` → no hits), so no snapshot verdict is claimed here.

## 4. Boundaries

- **Not a seventh gate leg** — the fleet's recorded kill-rate legs stay the six at `tools/mutate-and-run.sh:84-89` (`--regression`, expectation line `:1103`; S031 row). A repeat-control run is a precondition observation, not a mutation leg, and re-running it never counts as an independent gate.
- **Not a repair or a cure** — it measures agreement among runs; it does not remove nondeterminism, converts no mismatch into a pass, and the standing summary is: **no flakiness cured or determinism proven**.
- **Not an admission** — this note and the wave's reports are advisory and lane-internal: the wave contract labels them advisory, not independent non-author admission or promotion. A `controls_match` line is evidence a later claim may cite; it is not itself an admitted claim.
- **Not a verdict on sibling code** — gate code is read-only here; defects found in another lane's gate travel as recommendations, never as patches (`PROVINCE.md:16-17`).

## 5. Open arms and the command that closes each

- **Snapshot arm.** No retained run. Command: `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` after `expected.json` is authored to schema `repeat-control-snapshot-v1` (`runs`, `expected_id`, `expected_exit`, a sha256 per run file). Expected: exit equals the recorded ID's exit; any defect in the record or inputs yields `snapshot_tampered`, exit 2.
- **Selftest transcript.** No retained transcript for this gate. Command: `python3 tools/repeat-control.py --selftest > .ufo/evidence/round-12/ControlGate/selftest.txt 2>&1; echo exit=$?`. Expected: exit 0 and every embedded case at its recorded ID/exit.
- **A fleet gate through the control.** No retained receipt runs any of the six recorded gates through this gate. Command shape: `python3 tools/repeat-control.py --runs 3 --out /tmp/rc-kimi -- node kumitate-shokunin/scripts/kimi-census.mjs --selftest` (bash gates: `-- bash <gate> --selftest`); copy the output directory into `.ufo/evidence/` before citing it. Expected: one of the finding IDs; a `controls_mismatch` there is a finding about that gate's own output stability, never a kill-rate result.
- **Volatile output.** A gate that prints durations or timestamps reads `controls_mismatch` on an honest repeat under the unnormalized-byte rule. Unmeasured for all six recorded gates; the first such run decides it.

## 6. Final round-12 runtime addendum (supersedes open-arm state above)

Final gate sha256: `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`.
`python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`,
exit 0; both committed observation snapshots verified (match exit 0,
mismatch exit 1), including selftest byte-tamper and missing-input refusals.
`verification-final.json` under `.ufo/evidence/round-12/` retains the exact
argv, output, expected/observed exits and the real bash pristine control:
three zero-exit samples with identical streams; raw files in
`replayed-controls/`. This supersedes the absent-manifest and unrun-arm
observations above, which describe the earlier writer's time.

The same mismatch oracle on the same changing fixture fails over a
one-line single-control mutant (verifier exit 1, observed `controls_match`)
and passes after restoring repetition (verifier exit 0, observed
`controls_mismatch`). Retained fixture, mutant and outputs:
`.ufo/evidence/round-12/oracle-repair/`; exact command/output:
`oracle-repair.json`. The first integration used the restored stable
fixture by mistake; `verification.json` records that honest failed oracle
and `verification-final.json` replaces only its repaired rows.
The other passing checks were not rerun merely to prettify the evidence.
No finite-sample or cross-host reliability claim is added.
