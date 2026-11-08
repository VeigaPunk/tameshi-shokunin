---
author: hyaku closure (non-author integrator, @m_zfl)
---

# Round 96 verifier spot-check — non-author closure (tameshi r96)

Lane HEAD verified: `07e50d6d0142b21e8443b5417b8edc4d1dd76455` (branch `master`, `ahead=0 behind=0` via `jj-lane.sh state`).
Report: `.ufo/reports/round-96/tameshi.md` (fleet repo, committed by lane identity `tameshi-shokunin`, `git log --format='%an %H' -- <report>` → `tameshi-shokunin aac45ecf…` + `tameshi-shokunin 9b917e2a…`; two commits, both lane-authored).
Prompt: `.ufo/prompts/tameshi-round-96.md` carries the template contract (§1 MISSION/AXES binding, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit/push scope, §6 hyaku addendum).

Dispatch digest (`.ufo/watchdog.log`, copied verbatim, mutable log):
- `2026-11-08T09:11:05-03:00 launch tameshi round=96 pgid=1345449 driver=hyaku-inline attempt=1`
- `2026-11-08T10:46:09-03:00 complete tameshi round=96; hyaku-inline attempt=1`

## Conformance (step-1)

- Report committed in fleet repo by lane identity: PASS.
- `SHONEN` heading present with one `[~]` line per box (4 boxes): PASS.
- Cited lane commits exist and are ancestors of `master` (`git merge-base --is-ancestor 07e50d6d0142b21e8443b5417b8edc4d1dd76455 master` → ok; base `c8de77f3de0fd4bf619ebe78fa0b28adaf320d3e` an ancestor; 12 commits `c8de77f3..07e50d6d`): PASS.
- Lane repo clean and pushed: `jj-lane.sh state` → `branch=master local=07e50d6d remote=07e50d6d ahead=0 behind=0`; `git status --porcelain` → empty: PASS.
- Prompt carries the template contract: PASS.
- Markers: report names real committed work (12 :: table rows with hashes) — not a marker.
- Verdict: **status ok**. Defects are status-neutral, named below.

Status-neutral conformance defects noted:
- D-a (path drift): report cites `.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt` as the 50/50 battery summary; that file is not in the committed tree at `07e50d6d` (only the 50 per-state receipts `pre-freeze/controls/*.out` are committed). The battery's `C1_CONTROLS states=50 matched=50` line is attested by the seat re-grade (`w1/R96SC1.md`, `R96SC1-regrade.txt`) and the 50 committed receipts each carry a `counter_sha=` line — evidence-verified, not re-run to completion by this closure (the full 50-state run exceeds a single verdict window). Route to lane: commit the summary or cite the re-grade file.
- D-b (dead seat): R96L1 (revenger) delivered no report; absent from the wave record, disclosed in the report. The falsification ledger covers 7 attack seats and passes. The "guards are inert" hypothesis is reported unmeasured. Status-neutral; routed for the lane to re-dispatch or record as a permanent gap.
- D-c (L1-constructed wave accounting): `w1-results.json` was written by the L1 (`_source: l1-constructed`) because the orchestrator's dispatcher wrote no `done tameshi w1` line. Disclosed in the report. Status-neutral.
- D-d (SCORECARD wave note): the round-95 SCORECARD wave parenthetical claims "all settled, no dead seat" while round 96 records a dead seat in its own wave — the round-95 note is superseded by the round-96 record; no action, noted for accuracy.

## Per-claim re-check

Claims are evidence-verified against committed receipts (protocol §Gate standard: lane-owned gate/selftest evidence is verified from its committed bytes, never re-executed by the closure except for plain measurements below). Both claims rest on the lane's own instruments and selftests — graded as **evidence-verified** (committed receipts re-read + targeted plain measurements), not as full independent re-runs of the 50-state battery.

### R96-C1 (calibration) — evidence-verified, re-measured in part

Commands run by this closure (committed bytes at `07e50d6d`):
```
python3 -I .ufo/evidence/round-96/conjunct-disposition-v96.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b --min-falsifiable 17
python3 -I .ufo/evidence/round-96/conjunct-disposition-v96.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev master --min-falsifiable 17
```
Observed:
```
DISPOSITION_INSTRUMENT rev=8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b sha256=69ee68b6fa230e29ef5ddc4e02d619562d5fe5f3620fb2355903c7f9f09a18d9 conjuncts=19
DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0          (exit 0)
DISPOSITION_SETUP rev-not-a-commit-id                                  (--rev master, exit 2)
```
Committed `landing/c1-positive.out` carries the identical `DISPOSITION_INSTRUMENT rev=8ed9c526…` line and `rows=19 falsifiable=17 unfalsifiable=2 findings=0`. `landing/c1-rev-branch.out`, `c1-rev-empty.out`, `c1-rev-unresolvable.out` print the three refusal codes. `landing/forge-matrix.txt`: `summary: 8 checks, 0 failed` (hand-written exit 1, wrong `counter_sha=` exit 1, `refs/replace` exit 2; the round-95 checker printed `findings=0` exit 0 on all three). `landing/c2-selftest.out`: `DISPOSITION_SELFTEST: 13/13 pass`, with the two new cases running the real main path (`hostile-path-cheat` exit 2 under poisoned `PATH`; `branch-revspec-cheat` exit 2 `rev-not-a-commit-id`).
No axis harmed: `git diff c8de77f3..07e50d6d -- SCORECARD.md` shows score deltas 0 (depth 10, calibration 8, freshness 9 unchanged), plus the `revision-identity seal` capability row added with evidence pointers.
Verdict: **improved** (verified under amended wording A1-A5).

### R96-C2 (operability) — evidence-verified, re-measured in part

Commands run by this closure:
```
python3 -I .ufo/evidence/round-96/c1/make-pins96.py --lane '' --rev 8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b
python3 -I .ufo/evidence/round-96/c1/make-pins96.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b --check
```
Observed: `PINS_SETUP lane-empty` (exit 2, nothing written); `--check` prints `PINS_DERIVED …` + `PINS_CHECK OK`.
Committed receipts re-read: `landing/c2-pins-symlink.out` (`pins-symlink-refused`, target sha256 `9660b330…` unchanged), `landing/c2-rerun-plant.out` (`pos-real MATCH exit=0`, `C1_CONTROLS states=1 matched=1` with the planted `counter_sha=000…` file beside the driver's own write), `landing/c2-outdir-symlink.out` (`outdir-symlink-refused`). Battery: 50 committed per-state receipts in `pre-freeze/controls/*.out`, every one carrying a `counter_sha=` line (counted: `receipts=50 with_counter_sha=50`). The `states=50 matched=50 mismatches=0 missing=0` verdict itself is attested by the seat re-grade (`w1/R96SC1.md`) and is **evidence-verified**, not re-run by this closure; the pre-A6 44/50 do-nothing contrast is recorded by R96E4 (`independent_match=44/50`) and R96SN1 F5.
No axis harmed (see SCORECARD delta above).
Verdict: **improved** (verified under amended wording A6-A9).

### Prefile falsification ledger (step-2b)

Command run by this closure:
```
python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tameshi --round 96
```
Observed: `PREFILE-FALSIFICATION: pass claims=2 rows=11 attack_seats=7 findings=0`, exit 0. Matches the report's filed claim. No `falsifies-wording` row was found real-but-unreconciled: the four falsifying rows point at pre-data amendments A1/A2/A3/A5/A6/A7/A9, which are the lane's recorded repairs; the ledger row citing the dead seat (R96L1) names the narrowing (the probe is reported absent). No adjudication needed.

## Discernment spot-check

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0 (`ok`), warnings only (pre-existing duplicate-URL and tier-C W01/W04 advisories).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S320 sha256sum(1) admit (mined) | admit | `.ufo/evidence/round-96/sources/s320.html`, rendered per lane renderer; line 88 | agree | quote "Print or check SHA256 (256-bit) checksums." (6 words, ≤25) sits at line 88 under the named rendering; grounds the counter-digest semantics the claim uses |
| S320 sha256sum(1) exit-code line | admit | same file; line 116 | agree | "don't output anything, status code shows success" (7 words) at line 116; grounds reading `git rev-parse` by exit code in the C1 seal |
| S323 CommonMark indented code | admit | `.ufo/evidence/round-96/sources/s322.html` (same page bytes); lines 2358-2359 | agree | after the 2355→2358 correction, "An indented code block is composed of one or more / indented chunks separated by blank lines." (16 words) is at 2358-2359 under the canonical renderer; D1 closure verified in the registry row |
| GitHub REST "Get a commit" | reject | round-96 fetch (547 847 B, located line 733) per `w1/R96S1.md` §4 | agree | a hosted-API `ETag`-comparison statement is not the `<rev>` grammar / `^{commit}` dereference the seal needs; refusal carries a flip condition (future claim about the `application/vnd.github.sha` media type) |

Source-row check (newly written `corpus/SOURCES.md` rows): no row was added this round (rows 183 → 183; mined 149, queued 23, rejected 11 — census exit 0 before and after). The only touched cell is S323's `anchor` (`line 2355` → `line 2358`, D1 closure), verified above against the committed snapshot bytes.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1 sealed revision identity: `DISPOSITION_INSTRUMENT rev=8ed9c526…`, hostile-PATH never green, forge matrix 8/8 |
| operability | improved | C2 hardened write path: pins refuses empty/relative/symlink lanes, driver grades its own receipts, battery receipts 50/50 attested |
| depth | unchanged | no depth-claim this round; scores 10 unchanged |
| coverage | unchanged | no new domain surface; SOURCES 183 → 183, frontier rows unchanged |
| freshness | unchanged | re-verification via the battery/selftest, no stale item left unmarked; 9 unchanged |
| adjacency | unchanged | no cross-domain bleed; connector sweep found no duplicate implementation |

Admitted: true — both claims verified (evidence-verified, with the C1 columns re-measured by this closure), no axis harmed.

## Trend verdicts (must agree with MANIFEST entry)

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | census 183 → 183; frontier unchanged; the one admission candidate (GitHub REST) refused |
| quality | improved | QUALITY 173-174 record both new criteria with failing receipts; seal + write-path governed where round-95 accepted both |
| discernment | improved | the round's own wave falsified 9 atomic assertions pre-data (R96R1 ×2, R96C1 ×5, R96E4 number 44/50, R96SN1 F4/F5/F9-F11); all amended pre-data (A1-A9) with artifacts cited; SC1 caught two unbacked citations repaired at `cdc7f1b`; this closure's sample agrees on all 4 gate decisions |

## Routed defects (lane must fix next round)

1. D-a: commit or correctly cite the 50/50 battery summary (`pre-freeze/controls/C1-summary.txt` cited but uncommitted).
2. D-b: R96L1 dead seat — the "guards are inert" probe is unmeasured; re-dispatch or record as a permanent gap.
3. D-c: `w1-results.json` L1-constructed — orchestrator dispatch-stall class (host incident 5); no lane action, recorded for fleet-level follow-up.
4. Inert risk note (non-blocking): the 50-state battery is ~185s/state of wall time; a single-closure re-run is impractical — the committed-receipts + seat re-grade evidence is the verifiable record, and closures should continue to evidence-verify rather than re-run it.
