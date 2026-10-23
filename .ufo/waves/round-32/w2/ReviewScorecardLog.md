# ReviewScorecardLog — round-32 SCORECARD/LOG block review (wave 2)

- Seat: `ReviewScorecardLog`
- Date: 2026-10-23
- Reviewed revision: `a4f718138bdad20de741faeca57891645e5a64d9` ("round-32: content revision — knowledge entry runner-tally-audit, README row, S097/S099 + S094 re-open, receipt checker, SCORECARD/LOG round-32 blocks, wave-1 reports")
- Base revision: `e24688b2ff6cca1c9ad20e112f02c629b8597ff8`
- Scope: the round-32 blocks appended to `SCORECARD.md` and `LOG.md` at a4f7181; every cited hash, path and count; the append-only property. Read-only review: no production file edited, no gate/selftest/sweep run in the lane, no subagent, no tool installed (nothing to record under the tooling directive).
- Method: read-only `git -C <lane> cat-file / rev-parse --verify <h>^{commit} / ls-tree / show --stat / diff` from the seat scratch dir `/fast/scratch/hyaku/tameshi-r32-seats/ReviewScorecardLog/`; receipts read from `.ufo/evidence/round-32/` and `.ufo/waves/round-32/w1/`. GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; no `jj` command run anywhere.

## Findings by severity

### F1 [Medium] LOG round-32 motivation cites a stale count: "270 of 480" — the ledger says 282 of 480

- Statement (LOG.md, appended block, line 3): "`tools/mutate-and-run.sh` is an input of 270 of 480 cold-read entries".
- Measured: parsing `.ufo/evidence/round-21/coldread/ledger.json` at a4f7181 (the canonical ledger; blob unchanged 83c001a5 → a4f7181, verified by `git rev-parse` equality): **480 entries, 282 with `tools/mutate-and-run.sh` among `inputs` keys** (all 282 carry the exact key; 6 further entries additionally carry staged/@sha key variants — the 282 count is exact-key entries; any-variant count is also 282 because every variant-key entry also has the exact key... precisely: 282 entries have the exact key; 7 extra variant key occurrences co-occur inside those same entries).
- Drift reconstructed: at r31 base `36c1d393` and r31 content `2da841bd` the ledger is **456 entries / 270 runner-input** (so "270 of 456" was true in round 31); at r31 final `83c001a5` it is **480 / 282**. The LOG (and the frozen `contract.json` surface string, line 12) updated the denominator to 480 but kept the round-30/31 numerator 270. 12 of the 24 round-31 entries list the runner.
- Independent concurrence: `.ufo/waves/round-32/w2/ReviewEntry.md` flags the same defect ("[High] ... the ledger count is 282 at this revision"); `w1/ScoutDeferrals.md` lines 37–39 had already documented the 456→480 drift before the LOG was written.
- Smallest safe correction (recommendation, not applied): the LOG sentence should say 282 of 480 (or drop the numerator). The identical stale string inside the frozen `contract.json` is frozen-before-data: flag it to the closure/judgment rather than editing it mid-round; the C1 predicate does not depend on this motivational figure.

### F2 [Low] One of the 35 wave-1 reports is uncommitted: DriftSim.md

- `a4f7181` tree contains 34 `.md` reports under `.ufo/waves/round-32/w1/`; `swarm-registry.json` lists **35 members** (so LOG's "Wave 1 (35 seats)" is registry-backed and not false), and `w1/DriftSim.md` exists in the worktree (mtime 08:17, after the 08:01:58Z commit) but is absent from the a4f7181 tree and from HEAD's w1 tree. Note for the L1: the 35th report still needs committing.

### F3 [Low] CtlHeaderV2's surviving shape against the round-31 repair counter is unreported in the round-32 blocks

- `w1/CtlHeaderV2.md` (committed at a4f7181): "Verdict: the expected all-reject v2 pattern was not established. **Shape B survived v2.**" — a negative result about the round-31 repair counter `repair/c1-r31-measure-v2.py` (the `Score (0–10)` header repair). The round-32 SCORECARD block describes the repair factually (it exists, has the exact header and a byte-prefix test — both verified) and makes no completeness claim, and the LOG block does not mention CtlHeaderV2 at all; so no stated claim is false. But a calibration-relevant surviving shape from a committed wave-1 report is absent from the wave summary. Recommend the closure surface it.

### F4 [Info] mutant-fidelity.txt pins nine MutateHead mutants, the LOG says "eight"

- `before/mutant-fidelity.txt` lists T07, T08, H03, H04, H05, N01, N02, N03, N05 (nine rows, sha-equal to the round-30 MutateHead column). The LOG/SCORECARD "eight MutateHead selftest survivors" matches `corpus/lessons/round-31-verifier-spotcheck.md` ("the 8 MutateHead guard survivors ... deferred twice") and `w1/ReplaySurvivors.md` (names exactly T08, N05, H03, H04, H05, N01, N02, N03 as the eight survivors). T07 is a fidelity extra, not a claimed survivor. No contradiction.

## Append-only property — PASS

Command (per file), run with both blobs materialized in scratch:

- `git cat-file blob e24688b2…:SCORECARD.md` (127,356 B) is a byte prefix of `git cat-file blob a4f7181…:SCORECARD.md` (129,500 B): `new.startswith(base)` → True; appended block = 2,144 B beginning `## Round 32 — runner tally audit…`.
- LOG.md: base 123,886 B, new 125,229 B, prefix True; appended block = 1,343 B beginning `## Round 32 — 2026-10-23 (TameshiR32)`.

## Cited hashes exist — PASS (all)

`git rev-parse --verify <h>^{commit}` resolved (short → full, commit time -03): c3181497 → c31814978969… (07:38:24), b50a18f0 → b50a18f009df… (07:54:42), 528f8dee → 528f8deec8d6… (08:01:24), 67c0e013 → 67c0e01380a2… (07:10:07), 08125328 → 08125328f87d… (07:13:24), e24688b2 → e24688b2ff6c… (07:23:47), 36c1d393 (receipt filename) → 36c1d3933f68… (05:49:19). Content revision a4f7181 → a4f718138bda… (08:01:58). Sha256 pins verified against blobs: `tools/mutate-and-run.sh` = `a7d3f2dd7d47…2eb9` (identical at base and a4f7181 → "byte-identical" PASS); `tools/tally-audit.py` = `9639c458002c…99ef`, pinned in the v2 counter text and in `contract-amendment-2.json` (amendment-1 pins the earlier freeze `158202f8`, matching the "re-frozen" narrative).

## Cited paths exist at a4f7181 — PASS (all)

`tools/tally-audit.py` (absent at base — "no tool" PASS), `tools/mutate-and-run.sh`, `corpus/knowledge/runner-tally-audit.md`, `corpus/lessons/round-31-verifier-spotcheck.md`, `.ufo/evidence/round-32/{c1-measure.py, contract.json, receipt-check.py}`, `.ufo/evidence/round-32/v2/{c1-measure-v2.py, contract-amendment-1.json, contract-amendment-2.json}`, `.ufo/evidence/round-32/before/c1-at-base.stdout`, `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py`, `.ufo/evidence/round-31/c1-measure.py` — all present in `git ls-tree -r a4f7181`. `corpus/README.md` gained the `knowledge/runner-tally-audit.md` row at a4f7181 (absent at base); `corpus/SOURCES.md` diff adds S097 and S099 rows and re-opens S094 (adds the `corpus/knowledge/runner-tally-audit.md` used-by and "S094 re-opened" note).

## Statements and verdicts

### SCORECARD.md round-32 block

| # | Statement | Verdict | Evidence |
|---|---|---|---|
| S1 | Byte-prefix append-only vs base e24688b2 | PASS | prefix check above (2,144 B appended) |
| S2 | Depth 9 and calibration 8 at/above saturation line 8 | PASS | base SCORECARD re-stated rows (`recorded_cases=9 wired_legs=9 depth_score=9`; "numeric calibration 8 → 8"); `## Saturation` declares "saturation line 8/10 … depth is 9 and calibration 8, both at or above" |
| S3 | No capability row since round 25 (window 2) | PASS | standing capability table's last first-working round = 25 (`mutation report interop`); `## Saturation`: "Stagnation window N = 2 completed rounds without a capability entering the table" |
| S4 | New versioned tool `tools/tally-audit.py` audits the runner without editing it (per-leg `--regression` tally presence; tally oracle over every status 0–255 with stress; harness panel vs faulty blocks) | PASS | tool in tree, absent at base; tool text: "status 0..255", per-leg presence check, stress vectors, "panel of known-faulty tally blocks built from the pinned reference block" |
| S5 | Closes the runner items deferred since round 30 (per-leg check; eight MutateHead survivors) | PASS | lesson item 3 "now deferred twice (rounds 30 → 31 → 32)"; ReplaySurvivors confirms the eight (T08, N05, H03, H04, H05, N01, N02, N03) and the tool's harness panel targets exactly that harness blind spot |
| S6 | Runner byte-identical, sha256 `a7d3f2dd…2eb9` | PASS | blob sha256 equal at base and a4f7181 = `a7d3f2dd7d47511a…dd912eb9` |
| S7 | Counter v1 `.ufo/evidence/round-32/c1-measure.py` frozen `c3181497` | PASS | commit exists 07:38:24; blob equal c3181497 ↔ a4f7181 |
| S8 | v1 met before data by CriticC1's allowlist | PASS | `w1/CriticC1.md`: `C1_R32: kill=18/18 accept=8/8 other=0 … C1_R32_PASS=true` |
| S9 | Counter v2 `v2/c1-measure-v2.py`, amendment 1 `b50a18f0`, amendment 2 `528f8dee`, sandbox + tool pin + sealed held-out set; label `C1_R32V2_PASS` | PASS | both commits exist and add the amendment JSONs; v2 blob equal 528f8dee ↔ a4f7181; label string present in v2 counter and amendment-1; `a7d3f2dd` runner pin in contract.json |
| S10 | Tool bytes pinned sha256 `9639c458…99ef` | PASS | actual `9639c458002c…fa699ef`; pin string in v2 counter |
| S11 | Before at base e24688b2: no tool, `kill=0/18 accept=0/8`, false | PASS | `before/c1-at-base.stdout` last line: `C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 … rev=e24688b2… C1_R32_PASS=false` |
| S12 | Target: `C1_R32V2_PASS=true`, every valid held-out copy right, ≥6 of each kind | PASS (target statement, no data claimed) | held-out set is wave-2 work; no measurement receipt exists yet, and the block appends none |
| S13 | Repairs: r31-counter v2 with exact `Score (0–10)` header + byte-prefix test (`repair/c1-r31-measure-v2.py`); frozen r31 counter unchanged | PASS | repair file in tree and in c3181497; `.ufo/evidence/round-31/c1-measure.py` blob equal base ↔ a4f7181 |
| S14 | Repair receipt `c1monitor-at-r31-base-36c1d393.*`, `covered=64/64 restraint=8` | PASS | stdout: `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=36c1d393…`; exit file `0` |
| S15 | Command D receipts with exit files at `67c0e013` and `08125328` | PASS | `repair/commandD-at-r31-67c0e013.exit` = `0`, `repair/commandD-at-r31-final-08125328.exit` = `0`; both stdout `recorded_cases=9 depth_score=9` (matches round-31 "Depth 9 → 9") |
| S16 | "Measured results are appended below only after execution" | PASS | no results table in the appended block — honest pending state |

### LOG.md round-32 block

| # | Statement | Verdict | Evidence |
|---|---|---|---|
| L1 | Per-leg tally check and eight MutateHead survivors "deferred twice" | PASS | lesson routed item 3: "now deferred twice (rounds 30 → 31 → 32)" |
| L2 | Runner "is an input of 270 of 480 cold-read entries" | **FAIL** | ledger at a4f7181: **282 of 480** (F1 above); 270/456 was the round-31 figure |
| L3 | `corpus/lessons/round-31-verifier-spotcheck.md` routed item 3 | PASS | lesson item 3 is exactly the runner per-leg check + 8 survivors |
| L4 | Stagnation nudge (no capability since round 25) | PASS | see S3 |
| L5 | `c3181497` froze counter v1, contract, base and repair receipts before any seat | PASS | commit stat includes c1-measure.py, contract.json, `before/*`, `repair/*` (incl. c1monitor + both commandD triples, c1-r31-measure-v2.py); commit 07:38:24 predates registry createdAt 07:42:11 and earliest report 07:44 |
| L6 | Wave 1 (35 seats) | PASS | `swarm-registry.json` members = 35; 34 reports committed at a4f7181, DriftSim.md uncommitted (F2) |
| L7 | Do-nothing, always-pass/fail, junk, sha pin, region diff, line count, sha table, text-keyed, sibling consensus, static/runtime/harness-only, old selftest, combo shortcut — all read false | PASS | each of CtlDoNothing, CtlAlwaysPass, CtlAlwaysFail, CtlJunk, CtlShaPin, CtlRegionDiff, CtlLineCount, CtlShaTable, CtlTextKeyed, CtlSiblingConsensus, CtlStaticOnly, CtlRuntimeOnly, CtlHarnessOnly, CtlOldSelftest, CtlComboShortcut (15 seats) reports `C1_R32_PASS=false` / "rejected as expected" |
| L8 | CriticC1's allowlist read true (18/18, 8/8) | PASS | `kill=18/18 accept=8/8 other=0 … C1_R32_PASS=true` |
| L9 | v1 re-designed before data as v2 (`b50a18f0`, sandbox + tool freeze + sealed held-out set) | PASS | b50a18f0 07:54:42 adds v2 counter + amendment-1 + first tool freeze; no v2 measurement receipt predates the final freeze |
| L10 | DeterminismProbe found a harness-panel blind spot (singleton positions 0 and 1) | PASS | `w1/DeterminismProbe.md`: "These drive **positions 0 and 1** directly", selftest "self-confirming on exactly the blind spot" |
| L11 | Tool gained position-only faults, re-frozen with two counter hardenings before any v2 run (`528f8dee`, amendment 2) | PASS | 528f8dee 08:01:24: tool +9 lines ("# Position-only faults…"), counter hardened ("copy-order side channel closed"), amendment-2, dev-sweep receipts in-commit; tool blob equal a4f7181; RunCounterV2 only diff-verified, ran no measurement |
| L12 | Content: tool, knowledge entry + README row, S097/S099 added, S094 re-opened, `receipt-check.py` | PASS | a4f7181 commit subject and diff match item for item |
| L13 | Cited hashes c3181497, b50a18f0, 528f8dee | PASS | all resolve (see hash section) |

## Residual risk and verification gaps

- I did not execute `tools/tally-audit.py` or any counter (outside this item's scope; also bounds prohibit running gates/selftests in the lane). Tool-surface statements (0–255 oracle, per-leg check, panel, position-only faults) are verified by reading the tool's text, not by execution; the fault-panel size (27 per the wave spec) is not asserted in either block and was not checked.
- The sealed held-out set is written in this wave by HeldOut seats; its validity/counts (≥6 of each kind) are not yet receivable and were not audited here.
- CriticC1's receipt lines reference a seat-sandbox clone rev `d1b22ed8…` not cited by the blocks; left unresolved (not needed for any block statement).
- F1's "smallest safe correction" touches LOG.md, a production file — I did not apply it; it belongs to the L1. The same stale "270 of 480" inside the frozen `contract.json` should go to the closure as disclosure, not be edited.
- "Attempt 1" and the seat roster semantics are taken from the registry and wave files as written.
