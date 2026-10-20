# C02 — lesson carry: routed-defect closure at `98bea7da`

Seat: `TameshiR17.C02LessonCarry` (leaf; no delegation). Round 17 wave 1.
Pin: `98bea7da5801f4bc58e4187690ee1687c8a5061f` (branch `master`; lane HEAD = pin, no round-17 commit exists at it).
Scope: the routed-defect sections of `corpus/lessons/round-13/14/15/16-verifier-spotcheck.md` — every numbered item, checked for closure in the committed bytes at the pin.

Method: all lane bytes read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 98bea7da:<path>`. Executions (lane tools and their selftests) ran in one clone at the pin, `mktemp -d /tmp/tameshi-r17w1-C02LessonCarry-2QnWbK`, never in the live lane; the only git writes were inside that /tmp clone (`clone`, `checkout`). No lane instrument was edited; this file is the only lane write. No `jj`, no tool install/upgrade, no pacman/uv/npx/cargo transaction.

## 0. Counts

- **21 top-level routed items**: r13 5, r14 5, r15 5, r16 6.
- **8 closed, 1 partial, 12 open.** The partial is r13.4 (its dispatch-text half closed; the operator closure-checker half is open). Split at the spot-check's own semicolon, 22 rows: **9 closed / 13 open**.
- **All six round-16 defects are open at the pin.** Uncommitted wave-1 work is visible in the live worktree for R16-OP1 (`.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`) and R16-EV1 (an appended correction in `runner-sha256.txt`); `.ufo/evidence/round-17/` and `.ufo/waves/round-17/` are untracked. Per the committed-bytes rule those are excluded from every status below.
- The carried-debt sub-items (B1–B6, §5) are **6/6 open**.

## 1. Round 13 — `corpus/lessons/round-13-verifier-spotcheck.md:179-183`

| ID | Routed item (scope) | Status at pin | Landing commit and evidence at the pin |
|---|---|---|---|
| R13.1 | `expected.json expected_checks.producer_before` demands an assertion the run never reached; add an effective/superseded disposition | **closed** | `0c6e36d`. `.ufo/evidence/round-14/dispositions.json:35-41`: `producer_before` `state=superseded`, `raw_receipt`/`raw_check` retained, `superseded_by=["producer_before_oracle","producer_after_oracle"]`, reason names the `FileNotFoundError` setup failure. |
| R13.2 | GIT_DIR-poisoning check records no injected environment; retain bounded setup and explicit mapping results | **closed** | `6431478`. `.ufo/evidence/round-14/context-receipt.json`: `environment.injected_env.GIT_DIR=/nonexistent/tameshi-round14-poison`, `baseline_has_GIT_DIR=false`, `env_delta_keys`/`env_delta_matches_declared`, and a `mapping` block (`runner-leg-mapping-v1`, six legs, `leg_set_equal: true`, `leg_order_equal: true`). |
| R13.3 | Knowledge §6 is a deferred-at-write account; add an empirical backlink and prefer S048 wording | **closed** | `0c6e36d` and `4d409d7`. `corpus/knowledge/incremental-pin-disposition.md:314-316` §8 "supersedes only section6's **deferred-at-write** status"; `:368` `### Round14 execution backlink (after integration)` (added by `4d409d7`). |
| R13.4a | Retain the relative seat-`Report:` trailer correction in the validated future context/body | **closed** | `c699c8c`. `.ufo/waves/round-16/spec1.json` `context` line 7: "Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/tameshi-shokunin — write it at …/<that path>". |
| R13.4b | The append helper is not the canonical frozen closure-status/history-pin checker | **open** (operator) | `/home/vgpnk/Projects/shokunin/scripts/closure-check.py` absent; `scripts/hyaku/` holds only `append-closure.py` etc. Outside the lane write scope. |
| R13.5 | Carried debt: box-3, legacy provenance headers, F1 interop, kimi/tsukuroi/mado successor sweeps, runbook | **open** | §5 rows B1–B5. |

## 2. Round 14 — `corpus/lessons/round-14-verifier-spotcheck.md:156-160`

| ID | Routed item (scope) | Status at pin | Landing commit and evidence at the pin |
|---|---|---|---|
| R14.1 | Status record: "prior routed items 1–3 addressed within their bounded scopes" | **closed** | `13c1367` (record). All three closing artifacts present at the pin: `dispositions.json` (0c6e36d), `context-receipt.json` (6431478), `incremental-pin-disposition.md:314` (0c6e36d/4d409d7). |
| R14.2 | Operator: append helper is not a frozen closure-status/pin checker | **open** | Same evidence as R13.4b. |
| R14.3 | Carried debt: box-3, legacy provenance, F1, successor sweeps, runbook | **open** | §5 rows B1–B5. |
| R14.4 | Preserve the no-mid-flight-check instruction next round | **closed** | `c699c8c`. `.ufo/waves/round-16/spec1.json` `context` line 10: "no build/lint/test/formatter runs on lane code mid-flight unless your Target says to execute something". Caveat: the same round breached the adjacent in-place-instrument rule (`QUALITY.md:102`, criterion 20) — a different rule, and it is bound now. |
| R14.5 | Register `capture-context.py` as a gate; standalone isolated selftest; map exit 64 to could-not-evaluate | **closed** | `0494c24`. `SKILL.md:1680` gate row (kind `gate`, `--selftest`, exit map "2 and 64 could-not-evaluate … 64 `usage_error`"); `tools/context-capture.py --selftest` at the pin → `SELFTEST: PASS (49/49)`, exit 0 (clone). |

Record correction: the round-16 lane ledger claims this spot-check line 160 is "truncated inside the committed file at 844 chars, ending …defects in the non-cla…". It is not: at both `c699c8c` and the pin, line 160 is 846 bytes and ends with the complete sentence "…not a failure of C1 or harm to an existing axis." (`.ufo/waves/round-16/w2/RoutedLedger.md` §0). The observed 768-byte cut was a display limit, not file content. The operative instruction is intact either way; no status above depends on the claim.

## 3. Round 15 — `corpus/lessons/round-15-verifier-spotcheck.md:159-163`

| ID | Routed item (scope) | Status at pin | Landing commit and evidence at the pin |
|---|---|---|---|
| R15.1 | Complete the uncredited sibling-overlap connector scan; preserve failed-seat accounting | **closed** | `05a2247`. `.ufo/evidence/round-16/Overlap1/manifest.sha256` is committed (`git cat-file -e 98bea7da:.ufo/evidence/round-16/Overlap1/manifest.sha256` → exit 0); the `w1/Overlap1.md:34` erratum is appended at `:219`. The lane's own ledger (`c699c8c`) called this open; both unmet conditions land only at `05a2247`. Round-15 bytes were not rewritten (`git diff --stat 28aeef4 98bea7da -- .ufo/evidence/round-15` → empty), so the 56/66 accounting stands. |
| R15.2 | Repair usage-finding attribution; same fixture/argv old-vs-new; name the two rows; retain `verification-3.json` | **closed** | `c699c8c`. `.ufo/evidence/round-16/attribution/correction.json` (sha256 `1caf1237…`) names exactly `usage-proof-new` and `gate-usage`, `context_consistent → usage_error`, `coverage_changes: []`, source receipt sha `3c419055…`. `verify.py` untouched (`7e4519d9…`). At the pin, `reattribute.py --selftest` → `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)`, exit 0 (clone). |
| R15.3 | Continue execution discipline; the SpecClean mid-flight class stays a process incident | **open (standing)** | No criterion binds the class at the pin: `corpus/QUALITY.md:88` is criterion 18 (attribution), `:102` is 20 (in-place instrument edits — a different incident), `:116` is 22 (attribution proof). The dispatch clause exists (`spec1.json` `context` line 10) but no artifact/gate discharges it. |
| R15.4 | Operator: inherited closure-checker debt | **open** | Same evidence as R13.4b. |
| R15.5 | Prior bounded residuals: box-3, legacy provenance, F1, whole-F7 reuse, runbook, successor sweeps; note defect 5 resolved | **open** | §5 rows B1–B6; prior defect 5 (R14.5) is confirmed resolved above. |

## 4. Round 16 — `corpus/lessons/round-16-verifier-spotcheck.md:196-214` (all routed to round 17)

| ID | Routed item (scope) | Status at pin | Evidence at the pin |
|---|---|---|---|
| R16-OP1 | Restore a clean-capable live-tree verdict for `tools/evidence-disposition.py`; ship red-before (exit 2) and green-after; keep historical bytes immutable | **open** | Executed in the clone at the pin, both manifests: `evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` → **exit 2** `expected_input_digest_mismatch`, "observed `0673d2e5…` expects `75ed934d…`"; the `dispositions-before.json` run is also **exit 2**. The recipe's step 2 (`SKILL.md:1581-1583`) says it "must fail the unresolved `producer_before` assertion" with exit 1 explicitly insufficient — that documented exit 1 no longer reproduces either. `tools/evidence-disposition.py` carries only `evidence-dispositions-v1` (`:15`, `:1133`); no v2 schema/`historical_inputs`. |
| R16-C2a | Correct `SKILL.md` round-14 recipe steps 2–3 for the moved runner, or mark it historical with the working invocation; re-read the bucket | **open** | `SKILL.md:1581-1583` (step 2) and `:1584-1586` (step 3) still assert the pre-round outcomes. Only the round-15 registry row at `:1681` carries the workaround ("use `--root` on `git archive 28aeef4`"); the recipe itself is neither corrected nor marked historical. |
| R16-C2b | Input-keyed cold-read credit: invalidate a bucket when a surface its commands ran against changes; show red-before on the round-14 bucket | **open** | `.ufo/evidence/round-16/measure.py:178-215` `entry_credit_reason()` checks only verdict, `blocking_gaps`, `wrong_expectations`, class and `commands_executed_count`; no input digests. Executed `measure.py --rev 98bea7da --repo <clone>` → `calibration_restraint_score: 8`, `box3_full_page: true`, `sections_covered: 54`, `sections_total: 54`. The credited bucket `## Effective expectation reconciliation — round 14` (section sha `e8720037…`, ledger entry class `instruction`, verdict `gap-minor`, `commands_executed_count: 4`) rests on CR26, run against snapshot `97cf436b` while the runner was `75ed934d`; `c699c8c`/`05a2247` moved it to `0673d2e5`. That is the red-before the v2 rule must uncredit. No `.ufo/evidence/round-17/measure.py` is committed. |
| R16-C2c | Box-3 text overclaims until R16-C2a/C2b land; correct by appending | **open** | `SHONEN.md:9-10` still says "…wrong expectations repaired and re-read; ledger …/ledger.json…". |
| R16-EV1 | Stale receipt `runner-sha256.txt` (`89722ddb…`) vs landed runner `0673d2e5…`; append a dated correction | **open** | `git show 98bea7da:.ufo/evidence/round-16/round-gate/runner-sha256.txt` is one line, `89722ddb… tools/mutate-and-run.sh`. The landed runner is `0673d2e5…` (also named by `runner-regression.txt`/`runner-selftest.txt`). An uncommitted worktree append exists; it is not at the pin. |
| R16-MON1 | Add registered entry commands to the no-harm monitor | **open** | `git cat-file -e 98bea7da:tools/registry.json` → exit 128; `git cat-file -e 98bea7da:tools/registry-check.py` → exit 128. Neither file exists at the pin. |

## 5. Carried debt B1–B6 (the idea's named residuals; all open)

| ID | Residual | Status at pin | Evidence at the pin |
|---|---|---|---|
| B1 | Full-page SKILL cold-read / box 3 | **open** | The lane counter says 8 (`sections_covered: 54/54`), but the round-16 closure's input-aware re-read gives one credited instruction bucket stale → 53/54 → 6. `SHONEN.md:9-10` remains `[~]`. R16-C2a/C2b/C2c are the repairs. |
| B2 | 19 legacy provenance headers | **open** | `corpus/knowledge/` has 24 files; 19 lack a leading `^source:` (loop over `git show 98bea7da:<f>`). `corpus/README.md:91-95` still routes the repair to the operator. |
| B3 | F1 interop (ledger leg as schema JSON + validator) | **open** | `corpus/README.md:78`: next move "emit one ledger leg as schema JSON and validate it (validator unavailable this round: U)". `tools/mutate-and-run.sh` has no `--json` (only the text `PIN_*` legs). |
| B4 | Stale-successor ledger / owner-approved successor sweeps (kimi, tsukuroi, mado) | **open** | `corpus/README.md:96-97`: "Stale ledger successors — tsukuroi and mado legs read `stale`; re-sweeps owed". No re-sweep artifact under `.ufo/evidence/round-16/`. |
| B5 | Operator runbook corrections (ER-R3) | **open** | `corpus/knowledge/operator-runbook.md:173` and `:374` still say the harness "carries four legs; cases 5/6 are **not embedded**", while the runner carries 7 recorded cases at the pin (`measure.py` → `recorded_cases: 7`). `corpus/README.md:98` names ER-R3 open. |
| B6 | Whole-F7 per-leg reuse decisions | **open** | `corpus/README.md:84` F7 `open`; no reuse-decision artifact exists. |

## 6. Cross-checks and contradictions

1. **Lane-side ledger is stale at the pin and must not be copied.** `.ufo/waves/round-16/w2/RoutedLedger.md` is pinned at `c699c8c`; it calls R15.1 open (closed at `05a2247`), and its "committed" `reattribute.py` sha `b81086b0…` is the pre-wave-2 value — at the pin it is `eaf564e4…` (changed by `05a2247` "hardened attribution … selftests"); `correction.json` is unchanged at `1caf1237…`.
2. **Display-vs-file confusion corrected.** The round-14 line-160 "truncation" is a display artifact (see §2). A closure that copied the lane ledger's claim would record a non-existent record defect.
3. **Round-16 operability harm is confirmed by execution, not inference.** Both the after- and before-manifests return exit 2 at the pin. The round-16 spot-check's step-2 note was `[INFERENCE]`; it holds.
4. **No round-17 bytes count.** Lane HEAD equals the pin; `.ufo/evidence/round-17/` and `.ufo/waves/round-17/` are untracked, and the worktree carries an uncommitted `op1-redbefore-98bea7d.txt` and an uncommitted append to `runner-sha256.txt`. None is evidence of closure at `98bea7da`.
5. **r14.5 selftest and r15.2 selftest re-ran green at the pin** (49/49 and 8/8 new / 14/14 old-fidelity), so those closures are artifact-backed, not just record-backed.

## 7. Commands and exits (representative)

| Command | Exit | Key line |
|---|---|---|
| `git -C …/tameshi-shokunin rev-parse HEAD` | 0 | `98bea7da5801f4bc58e4187690ee1687c8a5061f` |
| `git show 98bea7da:SKILL.md \| grep -n …` | 0 | recipe steps at `:1581-1586`; registry rows `:1680`/`:1681` |
| `git show 98bea7da:SHONEN.md` | 0 | box 3 at `:9-10`, `[~]` |
| `git show 98bea7da:.ufo/evidence/round-16/round-gate/runner-sha256.txt \| wc -l` | 0 | `1`; content `89722ddb…` |
| `git cat-file -e 98bea7da:tools/registry.json` / `…/tools/registry-check.py` | 128 / 128 | `does not exist in '98bea7da'` |
| clone: `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | **2** | `expected_input_digest_mismatch`, observed `0673d2e5…` expects `75ed934d…` |
| clone: same with `dispositions-before.json` | **2** | same finding; recipe step 2's exit 1 does not reproduce |
| clone: `python3 .ufo/evidence/round-16/measure.py --rev 98bea7da… --repo <clone>` | 0 | `calibration_restraint_score: 8`, `box3_full_page: true`, `54/54`, `recorded_cases: 7` |
| clone: `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` |
| clone: `python3 tools/context-capture.py --selftest` | 0 | `SELFTEST: PASS (49/49)` |

Verdict: **8 of 21 routed items closed at `98bea7da` (9 of 22 split rows); the six round-16 defects — including the operability gate, the input-keyed cold-read hole, and the box-3 overclaim — are all still open at the pin.**
