# Round 29 wave 1 — candidate Mistakes rows

Scope: calibration-facing candidate rows only; these are report findings, not edits to `corpus/lessons/round-29.md`. I read the round-27/28 spot-checks, the cited review receipts, and `corpus/QUALITY.md` at `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`. No gate, counter, selftest, sweep, or external fetch was run for this report. One read-only history command was run and is identified below. No tools were installed.

## Candidate rows

### 1. Self-inflicted cold-read credit loss from late input edits

- **class:** self-inflicted calibration credit loss.
- **evidence:** `.ufo/evidence/round-28/append-probe.txt:1-9`; `corpus/lessons/round-28-verifier-spotcheck.md:87-90`. A one-blank-line append to `corpus/SOURCES.md` changes the recorded monitor result from `60/64` to `50/64`; all six tested files together yield `47/64`. The spot-check routes doing widely read input edits before the cold-read content revision.
- **captured-by:** QUALITY 56 (at the frozen revision).
- **fix:** land edits to `SOURCES.md`, `README.md`, `QUALITY.md`, and `SHONEN.md` no later than the cold reads' content revision; keep later work to the stated append-only files.
- **old-state check:** the receipt records the frozen C1 counter result for `corpus_SOURCES.md` at `074d30b1a67883ca3d16424b97fff20085354833`: `C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9`, versus its base `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c`: `covered=60/64`. The receipt does **not** retain the full argv or scratch clone path; the cited round-27 command form is `python3 .ufo/evidence/round-27/c1-measure.py --repo <scratch clone> --rev <rev>`. Thus the failing result is retained, but the exact executed command is not. Do not present a reconstructed argv as an observed transcript.

### 2. Re-opened source digest drift left without an erratum

- **class:** stale source provenance / unresolved digest drift.
- **evidence:** `corpus/lessons/round-28.md:12-17`; `corpus/lessons/round-28-verifier-spotcheck.md:71, 87-90`. The lesson pins HTML `9e3a2ebb…` and markdown `0d362d11…`; the re-opened versions measured `4fe02a79…` and `266915c5…`. The spot-check routes a supersedes row or an explicit non-determinism record.
- **captured-by:** QUALITY 35 covers append-only correction mechanics for a stale citation; it does not require a live external page to retain a digest.
- **fix:** preserve the old observation and append a dated superseding record with both revisions and digests, or document the observed non-determinism; do not silently replace the pinned value.
- **old-state check:** the spot-check records `curl -sL https://bazel.build/remote/caching` as the re-open command and records the live-versus-pinned hash mismatches above. It does not retain the exact hashing argv or raw hash-command stdout, so an exact command that itself prints the mismatch cannot be supplied from the evidence. The mismatch is report-observed, not re-run here.

### 3. Closure head drift and post-filing report rewrite

- **class:** closure moved after its stated head.
- **evidence:** `corpus/lessons/round-28-verifier-spotcheck.md:6-9,19,27-28`; routed item 3 at `:87-92`. The report was first committed as `2012146`, later rewritten as `38ae0ff`; the lane landed `41da22a3` and then `1dde85f3` after the prompt head `1076914a`.
- **captured-by:** QUALITY 57.
- **fix:** close and file the report against the final lane head, then stop landing lane commits and rewriting the fleet report.
- **old-state check:** I ran `GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline 1076914abf513c723d454b9d35b7f04d9101d3af..1dde85f3af3dfeae777c1ca4eed26aaf18df1167`. Output was:
  ```
  1dde85f round-28: final C1 reading 63/64 (honest stop)
  41da22a round-28: late read Read14B re-assembled with the other 16; ledger 354 -> 371
  ```
  The report rewrite is separately reported by the spot-check's `git log --format='%an %H' -- .ufo/reports/round-28/tameshi.md` observation: `tameshi-shokunin 2012146…`, then `tameshi-shokunin 38ae0ff`.

### 4. README overstates how independently anchored the F8 result is

- **class:** evidence-strength overclaim.
- **evidence:** `corpus/lessons/round-27-verifier-spotcheck.md:197-201`; `.ufo/waves/round-27/w1/CriticAnchors.md:188-200`; `corpus/knowledge/oracle-anchored-survivors.md:62-72, 95-107`. Only S_USAGE has its whole expectation fixed by an outside source; the other cases rely on header text or convention, including one convention-only classification. Round 28 still routes the README and QUALITY issues (`round-28-verifier-spotcheck.md:92`).
- **captured-by:** none. QUALITY 55 amends C1/C2 checks, but does not make this README wording accurate.
- **fix:** bound the README claim to what the entry actually establishes, separating the counter's four classifications from the one fully outside-source anchor. Do not count the wording repair as verified until a check distinguishes the overstated claim from that bounded wording.
- **old-state check:** the old C2 counter command, run on the anchor-mutated clone, was `python3 .ufo/evidence/round-27/c2-measure.py --repo . --rev HEAD`. In V1, all anchors were replaced with copied-from-pristine/state-anchored statements; it still printed `classified=4 anchored_holes=4`, exit 0 (`CriticAnchors.md:204-214`). This is a falsifier for the old claim that the counter establishes anchor quality, not proof that the README repair has been implemented.

### 5. QUALITY 53's independence and trigger clauses were not checkable as written

- **class:** checkability gap in the calibration rule.
- **evidence:** `.ufo/waves/round-27/w1/ReviewQuality.md:20-30,41-46,98-110`; `corpus/lessons/round-27-verifier-spotcheck.md:199-201`; frozen QUALITY 55 at `corpus/QUALITY.md:613-626`.
- **captured-by:** QUALITY 55, which adopts the crediting-entry reading and requires independence to be checked against entry `seats`/`reports` and the committed roster, outside the monitor.
- **fix:** use the criterion-55 wording; do not describe monitor input credit as evidence of seat independence. For a claim of independent re-reading, check the entry seat/report binding against the roster.
- **old-state check:** ReviewQuality documents the command form `cd /tmp/tq27-rq && python3 bin/c1-measure.py --repo <clone> --rev <rev>`. E10 changed a credit-carrying entry's `seats` from `CR06` to `NOBODY`; the monitor left the section `credited` and its uncovered list unchanged (`ReviewQuality.md:43-46,100,110`). E9 also shows the literal trigger reading was not discriminated: an edit to a file traced only by failing sibling entries leaves `covered=62/62 restraint=8 box3_mismatch=0`, exit 0 (`:27-30,100,109`). The review preserves those results, but not the concrete `<clone>` pathname in the command table.

### 6. QUALITY 54 treated a named digest as evidence that the probe ran

- **class:** receipt provenance overclaim.
- **evidence:** `.ufo/waves/round-27/w1/ReviewQuality.md:34-39,98-116`; `corpus/lessons/round-27-verifier-spotcheck.md:199-201`; frozen QUALITY 55 at `corpus/QUALITY.md:622-626`.
- **captured-by:** QUALITY 55.
- **fix:** require a re-run at the measured revision, or a result digest recomputed by the counter; digest-name matching alone is not execution evidence.
- **old-state check:** the review records `cd /tmp/tq27-rq && python3 bin/c2-measure.py --repo <clone> --rev <rev>`; E4 rewrote the receipt's probe digest to match the changed probe without rerunning it. At `10d4496`, the old counter nevertheless returned `classified=4 anchored_holes=4`, exit 0 (`ReviewQuality.md:36-39,100,115`). The report does not retain the exact clone pathname in the command table.

### 7. Regression runner can pass with a missing leg status

- **class:** false-green regression summary.
- **evidence:** `corpus/lessons/round-27-verifier-spotcheck.md:202-203`; `.ufo/waves/round-26/w1/MutateRunnerSelftest.md:316-354`; `.ufo/evidence/round-27/contract.json:28-30` records the item as not fixed.
- **captured-by:** none for the missing `npass + nfail + nsetup == nlegs` runtime invariant. QUALITY 48 governs evidence needed to count a routed hardening repair, but does not itself require this runner invariant.
- **fix:** account for every declared leg exactly once and reject a regression run when the status total differs from `nlegs`; retain single-trigger tests for a wrong `nlegs` and an omitted status.
- **old-state check:** the archived command is `bash /tmp/mrs26/fleet-m1/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep`. With the cite-check pin intentionally broken and the cite-check status omitted, it printed `REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0; the pristine runner reported `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`, exit 2 (`MutateRunnerSelftest.md:316-354`).

## Scope, gates, and limits

- **Axis:** calibration. No numeric score, promotion, or producer-authentication claim is made.
- **Gates:** none run by me. Existing command/output results above are attributed to their archived reports and receipts; only the closure-history query is newly observed in this assignment.
- **Touched surface:** this report only: `.ufo/waves/round-29/w1/ScribeMistakes.md`.
- **Out of scope:** no lesson, QUALITY, README, source row, runner, counter, fleet report, lane index, or sibling file was changed. No `jj` command was run; no fleet-repo write was performed.
- **Unresolved evidence limits:** append-probe and ReviewQuality preserve result rows but omit exact scratch clone paths / full argv; the source-digest report omits the digest command and raw stdout. I have left those limits explicit rather than inventing executions. Round-27 routed items 1-3 and 7-8 are not promoted to additional mistake rows here: item 1 is reported as an honest miss, item 3 receives the round-28 S092 append, item 2 lacks a final-head no-harm command in the cited spot-check, item 7 is a wording/formatting observation, and item 8 is cross-lane owner work.
