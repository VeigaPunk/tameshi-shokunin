# RowAudit01 — round-24 replay: six-row requirement/receipt audit

**Verdict: no false acceptance found in the six audited rows.** Every row's recorded
requirement is byte-identical to its entry in the frozen
`.ufo/evidence/round-23/requirements.json`; every receipt exit/stdout/stderr is identical to
the retained `observations.json` runner_result; every required stdout token is present in the
full, untruncated stdout; and the two computed predicates (wave-accounting totals, repeat-control
snapshot digests) reproduce independently from the frozen inputs. Two frozen predicates are weak
(see Calibration findings) but neither was exercised in a failing direction in this replay.

Scope: rows `repeat-control-snapshot-clean`, `witness-metadata-selftest`,
`mutate-and-run-selftest`, `registry-check-selftest`, `round19-coldread-selector-selftest`,
`wave-accounting-frozen-entry`. Artifacts:
`.ufo/evidence/round-24/replay/{observations,bundle,expected,live-dependent}.json`,
`.ufo/evidence/round-24/replay-{command,gate}.json`, `.ufo/evidence/round-23/{requirements,registry-baseline}.json`.
All checks below are read-only inspection; no registry battery, gate or selftest was executed
(bounds prohibit it), so these are consistency + independent-recomputation findings, not producer
authentication.

## 1. Requirement binding vs round-23/requirements.json

Observed [read]:

- `observations.json` has 43 rows; `requirements.json` has 43 requirements; name sets equal,
  duplicate-free, and the full requirement list (name/argv/expect, in order) is identical:
  `[r['requirement'] for r in rows] == req['requirements']` → `True`.
- Each of the six requirements is an exact dict match against `requirements.json` (name, argv,
  expect), including `stdout_contains` lists — `True` for all six.
- Freeze integrity: `sha256(requirements.json) = cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3`,
  and `git show d2eaecd:.ufo/evidence/round-23/requirements.json | sha256sum` yields the same
  digest; `git diff 6a1821a c8c5b88 -- .ufo/evidence/round-23/requirements.json` is empty.
- `requirements.registry_sha256 = ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a`
  equals `sha256(.ufo/evidence/round-23/registry-baseline.json)` (same digest at d2eaecd).
- The registry-baseline active projection (47 rows, 43 active) equals `requirements['requirements']`
  in order (`True`), which is exactly the refusal check the runner enforces at
  `tools/registry-replay.py:144`. The six rows are `status: active` in the baseline with the same
  argv/expect.
- `observations.source_requirements_revision = 28cae179e4dc2c1fa7f032a79cdddf0b5d862d76`
  equals `requirements.source_revision`; it resolves to a real commit (`28cae17`).

## 2. Receipts vs observations runner_result (exit, full stdout, held)

Observed [read/compared programmatically]:

- `bundle.json` (43 receipts, 43 requirements) is byte-canonical (`json.dumps(sort_keys=True,
  indent=2)+"\n"` round-trips) and its sha256 is
  `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`, exactly the
  `bundle_sha256` pinned by `replay/expected.json`.
- For each of the six (and, as a sanity sweep, for all 43 rows): `(receipt.exit, receipt.stdout,
  receipt.stderr) == (runner_result.got, runner_result.stdout, runner_result.stderr)` → all equal.
- All six rows: `held: true`, `got == expect.exit == 0`, no `stdout_missing`, no `cleanup_error`,
  `stderr == ""`; `status`/`tags`/`kind` agree with the baseline row; none is listed in
  `live-dependent.json` (which lists only `pin-disposition-read`, `verify-round15`); `external` false.
- `measurement_interval` delta equals `elapsed_s` for each row (e.g. 0.357/0.357, 2.378/2.378,
  7.188/7.188, 16.03/16.03, 0.69/0.69, 0.376/0.376) and row intervals are monotonic and serial.
- Instrument cross-check: `.ufo/evidence/round-24/replay-command.json` stdout has 43
  `<name> <got> <held>` lines; each of the six reads `<name> 0 True`, matching observations; its
  final report line is `{"bundle_sha256": "4f4240…", "finding_ids": [], "live_dependent":
  ["pin-disposition-read","verify-round15"], "refused_rows": [], "rows": 43, …}`.
- Gate cross-check: `.ufo/evidence/round-24/replay-gate.json` records `exit: 0`, stdout
  `{"bundle_sha256": "4f4240…", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}`,
  and `tool_sha256: 9230c68e…` which equals `sha256(tools/command-binding.py)`. The binding check
  itself validates exit and tokens over full receipt stdout (`tools/command-binding.py:109-111`).

## 3. Per-row token / content audit

| row | frozen expect | got/held | required tokens in full stdout | discriminating content observed | verdict |
|---|---|---|---|---|---|
| `repeat-control-snapshot-clean` | `exit 0` (no tokens) | 0 / true | n/a | 294-byte stdout: `SNAPSHOT_INPUTS 9 verified`, `SNAPSHOT_EXPECTED id=controls_match exit=0`, `SNAPSHOT_OBSERVED id=controls_match exit=0`, `REPEAT_CONTROL: controls_match` | hold |
| `witness-metadata-selftest` | `exit 0`, `SELFTEST: PASS` | 0 / true | present (1×, full and 4096-B tail) | 6002-B stdout: 39 `SELFTEST_CASE … OK` lines, final `SELFTEST: PASS 39/39` | hold |
| `mutate-and-run-selftest` | `exit 0`, `MUTATE_SELFTEST:`, `VERDICT: PASS` | 0 / true | both present (1× each) | 4515-B stdout: 96 `PASS …` lines, no line starting `FAIL`, `MUTATE_SELFTEST: 96/96 pass`, final `VERDICT: PASS` | hold |
| `registry-check-selftest` | `exit 0`, `SELFTEST: PASS` | 0 / true | present (1×) | 2700-B stdout: 51 `SELFTEST_CASE … PASS` lines, final `SELFTEST: PASS (51 cases)` | hold |
| `round19-coldread-selector-selftest` | `exit 0`, `SELECTOR_SELFTEST: ` | 0 / true | present (1×) | 145-B stdout: three `CASE … PASS` lines, `SELECTOR_SELFTEST: 3/3 pass` | hold |
| `wave-accounting-frozen-entry` | `exit 0`, `"completed": 66`, `"dead": 80`, `"seats": 146`, `"finding_ids": []` | 0 / true | all four present (1× each; `66` only in the total object, waves show 28/38) | 752-B JSON parses; `total {"completed":66,"dead":80,"seats":146}`, `finding_ids []`, `findings []`, `bundle_sha256 dfb1027f…` | hold |

Additional stream hygiene: no `\r`, ESC, or other control characters; no duplicate summary lines;
no `SELFTEST: FAIL`, `VERDICT: FAIL`, or failing selector summary in any of the six stdouts.
Failure paths are genuinely distinguishable in the tools: witness prints `SELFTEST: FAIL …` and
returns 1 (`tools/witness-metadata.py:1209-1211`); mutate prints `VERDICT: FAIL` and exits 1
(`tools/mutate-and-run.sh:1906-1912`); registry-check prints `SELFTEST: FAIL (…)` and returns 1
(`tools/registry-check.py:1811-1817`); the selector selftest returns 1 unless all cases pass
(`.ufo/evidence/round-19/coldread/measure.py:80-83`).

## 4. Independent recomputation (not trusting the receipt's own arithmetic)

- **wave-accounting-frozen-entry.** Parsed `.ufo/evidence/round-22/bundle.json` and re-derived the
  accounting per wave (seats = len(members), completed/failed from statuses, membership and
  claimed-total checks): totals `{"seats":146,"completed":66,"dead":80}`, findings `[]`, waves
  `wave1 {seats71,completed28,dead43,report_artifacts28,failed_with_report[]}`,
  `wave2 {seats75,completed38,dead37,report_artifacts40,failed_with_report["ProfileBashTsukuroiCensus","V01WitnessTests"]}`
  — identical to the printed JSON. The printed `bundle_sha256 dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e`
  equals the actual file digest, and `.ufo/evidence/round-22/expected.json` pins that same digest.
  Note the printed result is a *declared-callback* accounting (its own `authority` field says so);
  the `"finding_ids": []` token is the tool's deterministic finding set, and it is empty for this
  frozen bundle.
- **repeat-control-snapshot-clean.** `expected.json` in `.ufo/evidence/round-12/ControlGate`
  declares `expected_id controls_match`, `expected_exit 0`, and 9 input digests; I recomputed all
  nine sha256 values from the files — zero mismatches. The paired `mismatch/` snapshot declares
  `controls_mismatch`/1 and its nine digests also all match; its separate row
  (`repeat-control-snapshot-mismatch`) recorded `got 1`, held. Tool exit semantics map
  `controls_match→0`, `controls_mismatch→1`, `baseline_nonzero→2` (`tools/repeat-control.py:32-42`),
  and a stored-snapshot byte disagreement is reported as mismatch, not success (lines 208-220).
- **Tool identity.** `repeat-control.py` self-reports `tool-sha256=296fe566…` and
  `sha256(git show d2eaecd:tools/repeat-control.py) = 296fe566…`. All six tool blobs at d2eaecd
  equal the current working-tree blobs (witness `df3390…`, mutate-and-run `d22c40…`,
  registry-check `cba166…`, round-19 measure `4c9c74…`, wave-accounting `96b303…`).

## 5. Revision pinning

Replay revision is `d2eaecd443bf5f4e387e7e5331282e3d11dea047`; delivered revision is
`c8c5b88c8e961a929cdc351b95a7074c76958909`. `d2eaecd` is an ancestor of `c8c5b88`
(`merge-base --is-ancestor` exit 0). `git diff --name-only d2eaecd c8c5b88 | grep -v '^\.ufo/evidence/'`
is empty, and `git diff --name-only d2eaecd c8c5b88 -- tools .ufo/evidence/round-12
.ufo/evidence/round-19 .ufo/evidence/round-22 .ufo/evidence/round-23` is empty, so the two later
commits added only evidence and the receipts remain applicable to the delivered tree for these six
rows.

## 6. Calibration findings (no false acceptance; residual weaknesses)

1. **`repeat-control-snapshot-clean` is exit-only.** Its frozen expect has no `stdout_contains`
   (unlike sibling rows). Concrete counterexample that would be falsely accepted: a repeat-control
   build that prints `REPEAT_CONTROL: controls_mismatch` (or skips snapshot verification) yet exits
   0. Mitigation present, but partial: the paired `repeat-control-snapshot-mismatch` row would catch
   an *always-0* regression, not a clean-path-only skip. The observed receipt is not this case
   (stdout shows `controls_match` and all nine digests verify), so this is a predicate-strength
   gap, not an acceptance defect in this replay.
2. **`round19-coldread-selector-selftest` token is `SELECTOR_SELFTEST: ` only.** It would also be
   satisfied by a failing summary such as `SELECTOR_SELFTEST: 2/3 pass` if the tool also exited 0.
   The discriminator here is exit 0, and `measure.py:83` currently returns 1 on any failed case;
   the observed output is `3/3 pass` with three `CASE … PASS` lines. Freeze `SELECTOR_SELFTEST: 3/3
   pass` in a successor predicate if the calibration wants the token itself to discriminate.
3. **Runner documentation vs behavior.** `tools/registry-check.py:36-38` says `stdout_contains` is
   matched "over the retained tail", but `run_row` matches against the *full* decoded stdout
   (`tools/registry-check.py:718`, `TAIL_BYTES = 4096` at line 110, `_tail` at line 388). The
   implementation is more permissive than documented; no impact on these six rows (their required
   tokens also occur inside the last 4096 bytes: witness 6002 B and mutate 4515 B stdouts were
   checked in both full and tail), but the doc sentence is inaccurate.

No other mismatch was found. In particular there is no case among the six where a required token
is absent, where `got` differs from `expect.exit`, where `held` is true without the predicates
holding, or where the bundle receipt diverges from the retained observation.

## 7. Smallest safe correction

None required for these six rows. If L1 chooses to close the two predicate-strength gaps, add
successor rows in a round-25 requirements file (pinning `REPEAT_CONTROL: controls_match` and
`SELECTOR_SELFTEST: 3/3 pass`) rather than rewriting the frozen
`.ufo/evidence/round-23/requirements.json`; and correct the `registry-check.py:36-38` docstring to
say stdout matching is over the full retained stdout (documentation-only change).

## 8. Residual unknowns

- No producer authentication is claimed. The runner docstring itself states receipt argv/cwd are
  invocation parameters, not independently observed process metadata
  (`tools/registry-replay.py:14-20`), and the fleet mirror is symlinked to live siblings (not used
  by these six rows, which read only the clone and `/tmp`).
- I did not re-execute the rows (bounds forbid running the battery/gates/selftests in the lane);
  acceptance here rests on artifact consistency, frozen-digest verification and independent
  recomputation from the frozen data.

## 9. Tooling

No tools installed or upgraded; no pacman/uv/npm/cargo transactions were performed.
